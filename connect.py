import sqlite3

BANCO_DE_DADOS = "banco.db"

def banco(sql: str):
    with sqlite3.connect(BANCO_DE_DADOS) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    return cursor.lastrowid

def verifica_existencia():
    banco('''
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
                valor_honorario_padrao REAL,
                observacoes TEXT
            )
    ''')