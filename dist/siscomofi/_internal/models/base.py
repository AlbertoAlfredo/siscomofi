import os
from sqlalchemy import create_engine, desc, asc, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Pega o caminho absoluto do diretório onde este arquivo está
basedir = os.path.abspath(os.path.dirname(__file__))
# Define o caminho completo para o arquivo do banco de dados
db_path = os.path.join(basedir, "//servidor/Compartilhada/siscomofy/siscomofi.db")
# db_path = os.path.join(basedir, "siscomofi.db")

# Cria o "motor" que vai se conectar ao nosso banco de dados SQLite
# O 'echo=True' é ótimo para desenvolvimento, pois imprime no console o SQL que está sendo gerado.
engine = create_engine(f"sqlite:///{db_path}", echo=False)

# Cria uma "fábrica" de sessões para interagir com o banco
Session = sessionmaker(bind=engine)

# Base para nossos modelos ORM
Base = declarative_base()


def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas declaradas nos modelos ORM.

    Esta função utiliza o metadata da classe Base para criar automaticamente
    qualquer tabela que ainda não exista no banco SQLite.

    Returns:
        None
    """

    print("Criando tabelas no banco de dados, se necessário...")
    Base.metadata.create_all(engine)
    print("Tabelas verificadas/criadas.")


def add(classe, dados):
    """
    Adiciona um novo registro ao banco de dados.

    Args:
        classe (DeclarativeMeta): Classe ORM que representa a tabela.
        dados (dict): Dicionário contendo os campos e valores do novo registro.

    Returns:
        int | None: Retorna o ID do novo registro, ou None em caso de erro.
    """
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
    """
        Atualiza um registro existente.

        Args:
            classe (DeclarativeMeta): Classe ORM da tabela alvo.
            id (int): ID do registro a ser atualizado.
            dados_update (dict): Campos e novos valores que serão aplicados.

        Returns:
            bool: True se o registro foi atualizado, False caso contrário.
    """
    
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
    """
    Retorna todos os registros de uma tabela.

    Args:
        classe (DeclarativeMeta): Classe ORM da tabela.
        order_by: Campo para ordenação (opcional).

    Returns:
        list: Lista de objetos ORM.
    """
    session = Session()
    if order_by:
        lancamento = session.query(classe).order_by(asc(order_by))
    else:
        lancamento = session.query(classe).order_by(classe.id).all()
    session.close()
    return lancamento

def get_all_filter(classe, **filters):
    """
    Obtém registros filtrados com base em valores exatos.

    Args:
        classe (DeclarativeMeta): Classe ORM.
        **filters: Campos e valores para filtrar (equivalente ao filter_by).

    Returns:
        list: Lista de registros filtrados.
    """
    print(f"DEBUG FILTROS: {filters}")
    session = Session()
    lancamento = session.query(classe).order_by(classe.id).filter_by(**filters).all()
    session.close()
    return lancamento

def filter_date(classe, classe_date, date_inicio, date_fim):
    """
    Filtra uma tabela por intervalo de datas.

    Args:
        classe (DeclarativeMeta): Modelo ORM.
        classe_date (InstrumentedAttribute): Campo de data da tabela.
        date_inicio (date | False): Data inicial ou False.
        date_fim (date | False): Data final ou False.

    Returns:
        Query | list: Query filtrada ou todos os registros se não houver limites.
    """
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
    """
    Retorna o número total de registros de uma tabela.

    Args:
        classe (DeclarativeMeta): Classe ORM.

    Returns:
        int: Total de registros.
    """
    session = Session()
    total = session.query(classe).count()
    session.close()
    return total

def get_paginate(classe, order_by , page=1, per_page=10):
    """
    Retorna uma página de registros com base na paginação.

    Args:
        classe (DeclarativeMeta): Modelo ORM.
        order_by: Campo de ordenação.
        page (int): Página atual (1-indexed).
        per_page (int): Quantidade por página.

    Returns:
        list: Registros da página solicitada.
    """
    
    session = Session()
    offset = (page - 1) * per_page
    lancamentos = session.query(classe).order_by(order_by).limit(per_page).offset(offset).all()
    session.close()
    return lancamentos

def get_for_id(classe, id):
    """
    Busca um registro pelo ID.

    Args:
        classe (DeclarativeMeta): Modelo ORM.
        id (int): Identificador único.

    Returns:
        object | None: Registro encontrado ou None.
    """
    
    session = Session()
    dados = session.query(classe).filter_by(id=id).first()
    session.close()
    return dados if dados else None

def get_busca(classe, busca: str, colunas):
    """
    Realiza busca textual em várias colunas utilizando LIKE.

    Args:
        classe (DeclarativeMeta): Modelo ORM.
        busca (str): Texto a ser buscado.
        colunas (list): Lista de campos ORM a verificar.

    Returns:
        Query | list: Query filtrada ou todos os registros.
    """
    session = Session()
    query = session.query(classe)
    if busca and busca.strip():
        busca = f"%{busca}%"
        filtros = [coluna.ilike(busca) for coluna in colunas]
        dados = query.filter(or_(*filtros))
        return dados
    else:
        return get_all(classe)
    
    
def filter_date_and_search(classe, campo_data, date_inicio, date_fim, busca, colunas_busca):
    """
    Filtra registros por intervalo de datas e texto (LIKE) simultaneamente.

    Args:
        classe (DeclarativeMeta): Classe ORM.
        campo_data (InstrumentedAttribute): Campo de data.
        date_inicio (date | False): Data inicial.
        date_fim (date | False): Data final.
        busca (str | None): Texto para busca parcial.
        colunas_busca (list): Lista de colunas para aplicar o LIKE.

    Returns:
        list: Lista final filtrada.
    """
    session = Session()
    query = session.query(classe)

    # ----- FILTRO POR DATA -----
    if date_inicio and date_fim:
        query = query.filter(campo_data >= date_inicio).filter(campo_data <= date_fim)
    elif date_inicio:
        query = query.filter(campo_data >= date_inicio)
    elif date_fim:
        query = query.filter(campo_data <= date_fim)

    # ----- FILTRO POR TEXTO -----
    if busca and busca.strip():
        busca = f"%{busca}%"
        filtros = [col.ilike(busca) for col in colunas_busca]
        query = query.filter(or_(*filtros))

    query = query.order_by(campo_data)
    resultados = query.all()
    session.close()

    return resultados

def delete(classe, id):
    """
    Remove um registro do banco de dados.

    Args:
        classe (DeclarativeMeta): Classe ORM da tabela.
        id (int): Identificador do registro.

    Returns:
        bool: True se foi deletado, False caso contrário.
    """
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
