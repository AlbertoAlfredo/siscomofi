import os
from sqlalchemy import create_engine
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

    print("Criando tabelas no banco de dados, se necessário...")
    Base.metadata.create_all(engine)
    print("Tabelas verificadas/criadas.")

def to_dict(self):
    # Converte o objeto Cliente em um dicionário para fácil uso no front-end.
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def add(classe, dados):
    # Adiciona um novo cliente ao banco de dados.
    session = Session()
    try:
        novo_cliente = classe(
            **dados
        )  # Cria um Cliente a partir do dicionário
        session.add(novo_cliente)
        session.commit()
        return novo_cliente.id
    except Exception as e:
        session.rollback()
        print(f"Erro ao adicionar: {e}")
        return None
    finally:
        session.close()


def update(classe, id, dados_update):
    # Atualiza os dados de um cliente.
    session = Session()
    try:
        cliente = session.query(classe).filter_by(id=id).first()
        if cliente:
            for key, value in dados_update.items():
                setattr(cliente, key, value)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erro ao atualizar: {e}")
        return False
    finally:
        session.close()

def get_all(classe):
    session = Session()
    lancamento = session.query(classe).order_by(classe.id).all()
    lancamento = to_dict(lancamento)
    session.close()
    return [lancamento for i in classe]

def get_paginate(classe, page=1, per_page=10):
    # Busca uma 'página' de clientes do banco de dados.
    session = Session()
    offset = (page - 1) * per_page
    clientes = (
        session.query(classe)
        .order_by(classe.nome_cliente)
        .limit(per_page)
        .offset(offset)
        .all()
    )
    session.close()
    return [to_dict(classe) for cliente in clientes]


def get_for_id(classe, id):
    # Busca um único cliente pelo seu ID.
    session = Session()
    dados = session.query(classe).filter_by(id=id).first()
    session.close()
    return to_dict(dados) if dados else None


def count_total(classe):
    # Conta o número total de clientes para a paginação.
    session = Session()
    total = session.query(classe).count()
    session.close()
    return total


def delete(classe, id):
    # Deleta um cliente do banco de dados.
    session = Session()
    try:
        cliente = session.query(classe).filter_by(id=id).first()
        if cliente:
            session.delete(cliente)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erro ao deletar: {e}")
        return False
    finally:
        session.close()
