import mysql.connector
from mysql.connector import errorcode
banco = ''

def testType(type, data):
    if(type in [1,2,3]):
        value = int(input())
        return data+str(value)+','
    elif(type in [246,0,4,5]):
        value = float(input())
        return data+str(value)+','
    else:
        value = input()
        return data+"'"+value+"'"+","

def conectar():
    """
    Função para conectar ao servidor
    """ 
    print('Conectando ao servidor...')
    try:
        conn = mysql.connector.connect(host='127.0.0.1',user='root',password='root',database='ex1')
        return conn, "Conexão realizada com o banco!",f"Usuário: {conn.user}",f"Banco de dados: {conn.database}"
    except mysql.connector.Error as e:
        if(e.errno == errorcode.ER_BAD_DB_ERROR):
            print("Banco não encontrado!")
        elif(e.errno == errorcode.ER_ACCESS_DENIED_ERROR):
            print("Usário ou senha inválido!")
        else:
            print(e)
def desconectar(conn):
    """ 
    Função para desconectar do servidor.
    """
    print('Desconectando do servidor...')
    if(conn):
        conn[0].close()

def listar():
    """
    Função para listar os produtos
    """
    print(f'Listando {banco}...')
    conn = conectar()
    cursor = conn[0].cursor()
    cursor.execute(f"SELECT * FROM {banco}")
    produtos = cursor.fetchall()
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
    if(len(produtos)>0):
        print(f"--- Listando {banco} ---")
        for produto in produtos:
            for i in range(num_fields):
                print(f"{field_names[i]}: {produto[i]}")
        print("--- Fim Listagem ---")
    else:
        print("--- Não foi encontrado dados nesta tabela! ---")
def inserir():
    """
    Função para inserir um produto
    """  
    print(f'Inserindo {banco}...')
    data = ""
    conn = conectar()
    cursor = conn[0].cursor()
    cursor.execute(f"SELECT * FROM {banco}")
    num_fields = len(cursor.description)
    field_types = [i[1] for i in cursor.description]
    field_names = [i[0] for i in cursor.description]
    for i in range(num_fields):
        if(i!=0):
            print(f"Informe o/a {field_names[i]}")
            data = testType(field_types[i],data)
        if(i==num_fields-1):
            data = data[:-1]
    print(data)
    cursor.execute(f"INSERT into {banco}({','.join(field_names[1:])}) value ({data});")
    conn[0].commit()
    if cursor.rowcount == 1:
        print(f"O {banco} {data[0]} foi inserido!!")
    else:
        print(f"Erro ao cadastrar o {banco}: {data[0]}")
    desconectar(conn)
def atualizar():
    """
    Função para atualizar um produto
    """
    print(f'Atualizando {banco}...')
    data = []
    sql = f"UPDATE {banco} set "
    conn = conectar()
    cursor = conn[0].cursor()
    id = int(input(f"Informe o id do {banco} que deseja alterar: "))
    cursor.execute(f"SELECT * FROM {banco} where id = {id}")
    produto = cursor.fetchall()
    num_fields = len(cursor.description)
    field_types = [i[1] for i in cursor.description]
    field_names = [i[0] for i in cursor.description]
    if(len(produto)>0):
        print(f"--- Listando {banco} ---")
        for i in range(num_fields):
            if(i!=0):
                choice = ''
                while(choice!='Sim' and choice!='Não'):
                    print(f"Informe o/a {field_names[i]}")
                    print(f"O valor atual de {field_names[i]} é {produto[0][i]}\nVocê deseja altera-lo? (Sim / Não)")
                    choice = input()
                    if(choice=='Não'):
                        data.append(field_types[i])
                    elif(choice=='Sim'):
                        print(f"Informe o novo falor de {field_names[i]}")
                        data.append(input())
        print(data)
        newNames = field_names[1:(len(field_names)-1)]
        print(len(newNames))
        print(len(data))
        for i in range(len(data)):
            sql = sql+str(newNames[i])+" = "+str(data[i])
            if(i==len(data)-1):
                sql = f" where id = {id}"
        print(sql)
    else:
        print("--- Não foi encontrado dados nesta tabela! ---")
    
    print("--- Qual campo você deseja alterar? ---\n\t 1 -> Discriminação\n\t 2 -> Preço unitário\n\t 3 -> Ambos")
    cod = int(input("Qual sua escolha? "))
    match cod:
        case 1:
            discriminacao = input("Informe a nova discriminação do produto: ")
            id = int(input("Informe o id do produto que deseja alterar: "))
            cursor.execute(f"UPDATE produto set discrimanacao = {discriminacao} WHERE id = {id}")
        case 2:
            preco = float(input("Digite o novo valor unitário do produto: "))
            id = int(input("Informe o id do produto que deseja alterar: "))
            cursor.execute(f"UPDATE produto set p_unitario = {preco} WHERE id = {id}")
        case 3:
            discriminacao = input("Informe a nova discriminação do produto: ")
            preco = float(input("Digite o novo valor unitário do produto: "))
            id = int(input("Informe o id do produto que deseja alterar: "))
            cursor.execute(f"UPDATE produto set discrimanacao = {discriminacao},p_unitario = {preco} WHERE id = {id}")
    conn.commit()
    if cursor.rowcount == 1:
        print(f"O produto foi atualizado!!")
    else:
        print(f"Erro ao atualizar o produto")
    desconectar(conn)

def deletar():
    """
    Função para deletar um produto
    """  
    print('Deletando produto...')
    conn = conectar()
    cursor = conn[0].cursor()
    id = int(input("Digite o id do produto que você deseja deletar: "))
    cursor.execute(f"DELETE FROM produtos WHERE id = {id}")
    conn[0].commit()
    if cursor.rowcount == 1:
        print(f"O produto foi deletado!!")
    else:
        print(f"Erro ao deletar o produto")
    desconectar(conn)
def menu():
    """
    Função para gerar o menu inicial
    """
    opcao = 0
    global banco
    while(opcao!=5):
        if(banco == ''):
            print('=========Gerenciamento de Tabelas==============')
            conn = conectar()
            cursor = conn[0].cursor()
            cursor.execute("show tables")
            tabelas = cursor.fetchall()
            if(len(tabelas)>0):
                print("--- Selecione uma tabela ---")
                i = 1
                for tabela in tabelas:
                    print(f"{i} - Tabela: {tabela[0]}")
                    i+=1
                banco = input()
                print(f"Tabela {banco} foi selecionada!")
            else:
                print("--- Não foi encontrado dados nesta tabela! ---")
        print(f'=========Gerenciamento de {banco.replace("_"," ")}==============')
        print('Selecione uma opção: ')
        print(f'1 - Listar {banco.replace("_"," ")}.')
        print(f'2 - Inserir {banco.replace("_"," ")}.')
        print(f'3 - Atualizar {banco.replace("_"," ")}.')
        print(f'4 - Deletar {banco.replace("_"," ")}.')
        print('5 - Sair do programa')
        opcao = int(input())
        if opcao in [1, 2, 3, 4, 5]:
            if opcao == 1:
                listar()
            elif opcao == 2:
                inserir()
            elif opcao == 3:
                atualizar()
            elif opcao == 4:
                deletar()
            elif opcao == 5:
                print('Saindo do programa...')
            else:
                print('Opção inválida')
        else:
            print('Opção inválida')
