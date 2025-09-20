import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Pega o caminho absoluto do diretório onde este arquivo está
basedir = os.path.abspath(os.path.dirname(__file__))
# Define o caminho completo para o arquivo do banco de dados
db_path = os.path.join(basedir, 'siscomofi.db')

# Cria o "motor" que vai se conectar ao nosso banco de dados SQLite
# O 'echo=True' é ótimo para desenvolvimento, pois imprime no console o SQL que está sendo gerado.
engine = create_engine(f'sqlite:///{db_path}', echo=False)

# Cria uma "fábrica" de sessões para interagir com o banco
Session = sessionmaker(bind=engine)

# Base para nossos modelos ORM
Base = declarative_base()


def init_db():
    # Cria as tabelas no banco de dados, se elas não existirem.
    Base.metadata.create_all(engine)
    print("Banco de dados e tabelas verificados/criados com sucesso.")


class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nome_cliente = Column(String(100), nullable=False)
    nome_propriedade = Column(String(100))
    endereco = Column(String(150))
    numero = Column(String(10))
    bairro = Column(String(50))
    cidade = Column(String(50))
    uf = Column(String(2))
    tipo_pessoa = Column(String(10))
    cpf_cnpj = Column(String(18))
    inscricao_estadual = Column(String(20))
    telefone = Column(String(15))
    celular = Column(String(15))
    valor_honorario = Column(Float)
    observacoes = Column(String(500))
    
    def to_dict(self):
        # Converte o objeto Cliente em um dicionário para fácil uso no front-end.
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
def adicionar_cliente(dados_cliente):
    # Adiciona um novo cliente ao banco de dados.
    session = Session()
    try:
        novo_cliente = Cliente(**dados_cliente) # Cria um Cliente a partir do dicionário
        session.add(novo_cliente)
        session.commit()
        return novo_cliente.id
    except Exception as e:
        session.rollback()
        print(f"Erro ao adicionar cliente: {e}")
        return None
    finally:
        session.close()
        
def atualizar_cliente(id_cliente, dados_update):
    # Atualiza os dados de um cliente.
    session = Session()
    try:
        cliente = session.query(Cliente).filter_by(id=id_cliente).first()
        if cliente:
            for key, value in dados_update.items():
                setattr(cliente, key, value)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erro ao atualizar cliente: {e}")
        return False
    finally:
        session.close()

def get_clientes_paginados(page=1, per_page=10):
    # Busca uma 'página' de clientes do banco de dados.
    session = Session()
    offset = (page - 1) * per_page
    clientes = session.query(Cliente).order_by(Cliente.nome_cliente).limit(per_page).offset(offset).all()
    total = session.query(Cliente).count()
    session.close()
    return [cliente.to_dict() for cliente in clientes]

def get_cliente_por_id(id_cliente):
    # Busca um único cliente pelo seu ID.
    session = Session()
    cliente = session.query(Cliente).filter_by(id=id_cliente).first()
    session.close()
    return cliente.to_dict() if cliente else None

def count_total_clientes():
    # Conta o número total de clientes para a paginação.
    session = Session()
    total = session.query(Cliente).count()
    session.close()
    return total



def deletar_cliente(id_cliente):
    # Deleta um cliente do banco de dados.
    session = Session()
    try:
        cliente = session.query(Cliente).filter_by(id=id_cliente).first()
        if cliente:
            session.delete(cliente)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erro ao deletar cliente: {e}")
        return False
    finally:
        session.close()

