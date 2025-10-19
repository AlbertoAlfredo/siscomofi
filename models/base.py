import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Pega o caminho absoluto do diretório onde este arquivo está
basedir = os.path.abspath(os.path.dirname(__file__))
# Define o caminho completo para o arquivo do banco de dados
db_path = os.path.join(basedir, "siscomofi.db")

# Cria o "motor" que vai se conectar ao nosso banco de dados SQLite
# O 'echo=True' é ótimo para desenvolvimento, pois imprime no console o SQL que está sendo gerado.
engine = create_engine(f"sqlite:///{db_path}", echo=False)

# Cria uma "fábrica" de sessões para interagir com o banco
Session = sessionmaker(bind=engine)

# Base para nossos modelos ORM
Base = declarative_base()


def init_db():
    # Cria as tabelas no banco de dados, se elas não existirem.
    # Base.metadata.create_all(engine)
    # print("Banco de dados e tabelas verificados/criados com sucesso.")
    from models import cliente, lancamento

    print("Criando tabelas no banco de dados, se necessário...")
    Base.metadata.create_all(engine)
    print("Tabelas verificadas/criadas.")
