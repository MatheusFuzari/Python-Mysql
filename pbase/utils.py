import mysql.connector
from mysql.connector import errorcode

def conectar(''):
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
    print('Listando produtos...')
    conn = conectar()
    cursor = conn[0].cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    if(len(produtos)>0):
        print("--- Listando produtos ---")
        for produto in produtos:
            print(f"Id: {produto[0]}\nDiscriminação: {produto[1]}\nPreço unitário: {produto[2]}")
        print("--- Fim Listagem ---")
    else:
        print("--- Não foi encontrado dados nesta tabela! ---")
def inserir():
    """
    Função para inserir um produto
    """  
    print('Inserindo produto...')
    conn = conectar()
    cursor = conn[0].cursor()
    discriminacao = input("Informe a discriminação do produto: ")
    preco = float(input("Digite o valor unitário do produto: "))
    cursor.execute(f"INSERT into produtos(discrimanacao,p_unitario) value ('{discriminacao}',{preco});")
    conn[0].commit()
    if cursor.rowcount == 1:
        print(f"O produto {discriminacao} foi inserido!!")
    else:
        print(f"Erro ao cadastrar o produto: {discriminacao}")
    desconectar(conn)
def atualizar():
    """
    Função para atualizar um produto
    """
    print('Atualizando produto...')
    conn = conectar()
    cursor = conn[0].cursor()
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
    print('=========Gerenciamento de Produtos==============')
    print('Selecione uma opção: ')
    print('1 - Listar produtos.')
    print('2 - Inserir produtos.')
    print('3 - Atualizar produto.')
    print('4 - Deletar produto.')
    opcao = int(input())
    if opcao in [1, 2, 3, 4]:
        if opcao == 1:
            listar()
        elif opcao == 2:
            inserir()
        elif opcao == 3:
            atualizar()
        elif opcao == 4:
            deletar()
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')
