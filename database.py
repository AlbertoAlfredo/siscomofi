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
    cursor.execute("SELECT id, nome_cliente FROM clientes ORDER BY nome_cliente")
    clientes = cursor.fetchall()
    conexao.close()
    return clientes

def get_cliente_por_id(id_cliente):
    # Busca e retorna os dados de um cliente específico pelo seu ID
    conexao = get_conexao()
    # Usar row_factory para retornar resultados como dicionários
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (id_cliente,))
    cliente = cursor.fetchone()
    conexao.close()
    return cliente # Retorna um objeto tipo Row (acessível como um dicionário) ou None

def adicionar_cliente(dados_cliente):
    # Adiciona um novo cliente ao banco de dados.
    conexao = get_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO clientes (nome_cliente, nome_propriedade, endereco, numero, bairro, cidade, uf, tipo_pessoa, cpf_cnpj, inscricao_estadual, telefone, celular, valor_honorario, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tuple(dados_cliente.values()))
        conexao.commit()
    except sqlite3.IntegrityError:
        print(f"Erro: CPF/CNPJ '{dados_cliente['cpf_cnpj']}' já existe.")
        return False
    finally:
        conexao.close()
    return True

def atualizar_cliente(id_cliente, dados_cliente):
    # Atualiza os dados de um cliente existente.
    conexao = get_conexao()
    cursor = conexao.cursor()
    try:
        query = """
            UPDATE clientes SET
                nome_cliente = ?, nome_propriedade = ?, endereco = ?, numero = ?, bairro = ?, 
                cidade = ?, uf = ?, tipo_pessoa = ?, cpf_cnpj = ?, inscricao_estadual = ?, 
                telefone = ?, celular = ?, valor_honorario = ?, observacoes = ?
            WHERE id = ?
        """
        valores = list(dados_cliente.values()) + [id_cliente]
        cursor.execute(query, tuple(valores))
        conexao.commit()
    except sqlite3.IntegrityError:
        print(f"Erro: CPF/CNPJ '{dados_cliente['cpf_cnpj']}' já pertence a outro cliente.")
        return False
    finally:
        conexao.close()
    return True

def deletar_cliente(id_cliente):
    #Deleta um cliente do banco de dados.
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
    conexao.commit()
    conexao.close()