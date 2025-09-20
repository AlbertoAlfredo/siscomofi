import sqlite3
import os

DB_NAME = "siscomofi.db"


def init_db():
    # Inicializa o banco de dados e cria a tabela de clientes se não existir.
    # Garante que o banco de dados seja criado na mesma pasta do script
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_NAME)
    
    conexao = sqlite3.connect(db_path)
    cursor = conexao.cursor()
    
    # Usamos TEXT para todos os campos por simplicidade. Validações serão feitas na lógica.
    query = '''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_cliente TEXT NOT NULL,
        nome_propriedade TEXT,
        endereco TEXT,
        numero TEXT,
        bairro TEXT,
        cidade TEXT,
        uf TEXT,
        tipo_pessoa TEXT,
        cpf_cnpj TEXT UNIQUE,
        inscricao_estadual TEXT,
        telefone TEXT,
        celular TEXT,
        valor_honorario REAL,
        observacoes TEXT
    );
    '''
    cursor.execute(query)
    conexao.commit()
    conexao.close()
    print("Banco de dados inicializado com sucesso.")

def get_conexao():
    # Retorna uma nova conexão com o banco de dados.
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_NAME)
    return sqlite3.connect(db_path)

def get_clientes():
    # Busca e retorna todos os clientes do banco de dados.
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome_cliente, cpf_cnpj FROM clientes ORDER BY nome_cliente")
    clientes = cursor.fetchall()
    conexao.close()
    return clientes

def get_clientes_paginados(page, per_page=10):
    #Busca uma 'página' específica de clientes do banco de dados.
    offset = (page - 1) * per_page
    conexao = sqlite3.connect('siscomofi.db')
    conexao.row_factory = sqlite3.Row # Facilita o acesso aos dados
    cursor = conexao.cursor()
    
    query = f"SELECT id, nome_cliente, cpf_cnpj FROM clientes ORDER BY nome_cliente LIMIT {per_page} OFFSET {offset}"
    cursor.execute(query)
    
    clientes = cursor.fetchall()
    conexao.close()
    return clientes

def count_total_clientes():
    #Conta o número total de clientes no banco.
    conexao = sqlite3.connect('siscomofi.db')
    cursor = conexao.cursor()
    
    query = "SELECT COUNT(id) FROM clientes"
    cursor.execute(query)
    
    total = cursor.fetchone()[0] # Pega o primeiro valor da primeira linha
    conexao.close()
    return total


def get_cliente_por_id(id_cliente):
    # Busca e retorna os dados de um cliente específico pelo seu ID
    conexao = get_conexao()
    # Usar row_factory para retornar resultados como dicionários
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute(f"SELECT * FROM clientes WHERE id = {id_cliente}")
    cliente = cursor.fetchone()
    conexao.close()
    return cliente # Retorna um objeto tipo Row (acessível como um dicionário) ou None

def adicionar_cliente(dados_cliente):
    # Adiciona um novo cliente ao banco de dados.
    conexao = get_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute(f"""
            INSERT INTO clientes (nome_cliente, nome_propriedade, endereco, numero, bairro, cidade, uf, tipo_pessoa, cpf_cnpj, inscricao_estadual, telefone, celular, valor_honorario, observacoes)
            VALUES ('{dados_cliente["nome"]}', '{dados_cliente["nome_propriedade"]}', '{dados_cliente["endereco"]}', '{dados_cliente["numero"]}', '{dados_cliente["bairro"]}', '{dados_cliente["cidade"]}', '{dados_cliente["uf"]}', '{dados_cliente["tipo_pessoa"]}', '{dados_cliente["cpf_cnpj"]}','{dados_cliente["inscricao_estadual"]}', '{dados_cliente["telefone"]}', '{dados_cliente["celular"]}', '{dados_cliente["valor_honorario"]}','{dados_cliente["observacoes"]}')
        """)
        conexao.commit()
    except sqlite3.IntegrityError:
        print(f"Erro: CPF/CNPJ '{dados_cliente['cpf_cnpj']}' já existe.")
        return False
    finally:
        conexao.close()
    return True

def atualizar_cliente(id_cliente, dados_cliente):
    # Atualiza os dados de um cliente existente.
    query = f"""
                UPDATE clientes
                SET
                    {"nome_cliente = '" + dados_cliente['nome'] + "'"  if dados_cliente['nome'] else ''}
                    {", nome_propriedade = '" + dados_cliente['nome_propriedade'] + "'"  if dados_cliente['nome_propriedade'] else ''}
                    {", endereco = '" + dados_cliente['endereco'] + "'"  if dados_cliente['endereco'] else ''}
                    {", numero = '" + dados_cliente['numero'] + "'"  if dados_cliente['numero'] else ''}
                    {", bairro = '" + dados_cliente['bairro'] + "'"  if dados_cliente['bairro'] else ''}
                    {", cidade = '" + dados_cliente['cidade'] + "'"  if dados_cliente['cidade'] else ''}
                    {", uf = '" + dados_cliente['uf'] + "'"  if dados_cliente['uf'] else ''}
                    {", tipo_pessoa = '" + dados_cliente['tipo_pessoa'] + "'"  if dados_cliente['tipo_pessoa'] else ''}
                    {", cpf_cnpj = '" + dados_cliente['cpf_cnpj'] + "'"  if dados_cliente['cpf_cnpj'] else ''}
                    {", inscricao_estadual = '" + dados_cliente['inscricao_estadual'] + "'"  if dados_cliente['inscricao_estadual'] else ''}
                    {", telefone = '" + dados_cliente['telefone'] + "'"  if dados_cliente['telefone'] else ''}
                    {", celular = '" + dados_cliente['celular'] + "'"  if dados_cliente['celular'] else ''}
                    {", valor_honorario = '" + dados_cliente['valor_honorario'] + "'"  if dados_cliente['valor_honorario'] else ''}
                    {", observacoes = '" + dados_cliente['observacoes'] + "'" if dados_cliente['observacoes'] else ''}
                WHERE
                    id = '{dados_cliente['id']}'
            """
    try:
        conexao = get_conexao()
        cursor = conexao.cursor()

        cursor.execute(query)
        print(f"query = {query}")
        conexao.commit()
            
        # Verifica se alguma linha foi realmente alterada
        if cursor.rowcount > 0:
            print(f"Cliente com ID {id_cliente} atualizado com sucesso.")
            return True
        else:
            print(f"Nenhum cliente encontrado com o ID {id_cliente}.")
            return False

    except Exception as e:
        print(f"Ocorreu um erro ao atualizar o cliente: {e}")
        print(f"query = {query}")
        return False
    finally:
        if 'conexao' in locals() and conexao:  # pyright: ignore[reportPossiblyUnboundVariable]
            conexao.close()    

def deletar_cliente(id_cliente):
    #Deleta um cliente do banco de dados.
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute(f"DELETE FROM clientes WHERE id = {id_cliente}")
    conexao.commit()
    conexao.close()