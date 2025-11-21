import os
from sqlalchemy import create_engine, desc, asc, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Pega o caminho absoluto do diretório onde este arquivo está
basedir = os.path.abspath(os.path.dirname(__file__))
# Define o caminho completo para o arquivo do banco de dados
db_path = os.path.join(basedir, "//servidor/Compartilhada/siscomofy/siscomofi.db")

# Cria o "motor" que vai se conectar ao nosso banco de dados SQLite
# O 'echo=True' é ótimo para desenvolvimento, pois imprime no console o SQL que está sendo gerado.
engine = create_engine(f"sqlite:///{db_path}", echo=True)

# Cria uma "fábrica" de sessões para interagir com o banco
Session = sessionmaker(bind=engine)

# Base para nossos modelos ORM
Base = declarative_base()


def init_db():

    print("Criando tabelas no banco de dados, se necessário...")
    Base.metadata.create_all(engine)
    print("Tabelas verificadas/criadas.")


def add(classe, dados):
    # Adiciona um novo cliente ao banco de dados.
    session = Session()
    try:
        novo = classe(
            **dados
        )  # Cria um Cliente a partir do dicionário
        session.add(novo)
        session.commit()
        print(f"Lancamento adicionado com sucesso. ID: {novo.id}")
        return novo.id
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
        dados = session.query(classe).filter_by(id=id).first()
        if dados:
            for key, value in dados_update.items():
                setattr(dados, key, value)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erro ao atualizar: {e}")
        return False
    finally:
        session.close()

def get_all(classe, order_by = False):
    session = Session()
    if order_by:
        lancamento = session.query(classe).order_by(asc(order_by))
    else:
        lancamento = session.query(classe).order_by(classe.id).all()
    session.close()
    return lancamento

def get_all_filter(classe, **filters):
    session = Session()
    lancamento = session.query(classe).order_by(classe.id).filter_by(**filters).all()
    session.close()
    return lancamento

def filter_date(classe, classe_date, date_inicio, date_fim):
    session = Session()
    if date_inicio != False and date_fim != False:
        lancamento = session.query(classe).order_by(asc(classe_date)).filter(classe_date >= date_inicio).filter(classe_date <= date_fim)
    elif date_inicio and date_fim == False:
        lancamento = session.query(classe).order_by(asc(classe_date)).filter(classe_date >= date_inicio)
    elif date_fim and date_inicio == False:
        lancamento = session.query(classe).order_by(asc(classe_date)).filter(classe_date <= date_fim)
    else:
        lancamento = get_all(classe, order_by=classe_date)
    return lancamento

def count_total(classe):
    # Conta o número total de clientes para a paginação.
    session = Session()
    total = session.query(classe).count()
    session.close()
    return total

def get_paginate(classe, order_by , page=1, per_page=10):
    # Busca uma 'página' de clientes do banco de dados.
    session = Session()
    offset = (page - 1) * per_page
    lancamentos = session.query(classe).order_by(order_by).limit(per_page).offset(offset).all()
    session.close()
    return lancamentos

def get_for_id(classe, id):
    # Busca um único cliente pelo seu ID.
    session = Session()
    dados = session.query(classe).filter_by(id=id).first()
    session.close()
    return dados if dados else None

def get_busca(classe, busca: str, colunas):
    session = Session()
    query = session.query(classe)
    if busca and busca.strip():
        busca = f"%{busca}%"
        filtros = [coluna.ilike(busca) for coluna in colunas]
        dados = query.filter(or_(*filtros))
        return dados
    else:
        return get_all(classe)

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
