from sqlalchemy import Column, Integer, String, Float, Date
from .base import Base, Session  # Importa do nosso arquivo base.py

session = Session()


class Lancamentos(Base):
    __tablename__ = "lancamentos"

    id = Column(Integer, primary_key=True)
    movimento_data_lancamento = Column(Date)
    movimento_n_doc = Column(Integer)
    movimento_historico_lancamento = Column(String(100))
    agenfa_data_pagamento = Column(Date)
    agenfa_n_cheque = Column(Integer)
    agenfa_descricao_pagamento = Column(String(100))
    agenfa_valor_pagamento = Column(Integer)
    iagro_data_pagamento = Column(Date)
    iagro_n_cheque = Column(Integer)
    iagro_descricao_pagamento = Column(String(100))
    iagro_valor_pagamento = Column(Integer)
    pagamentos_data_pagamento = Column(Date)
    pagamentos_n_cheque = Column(Integer)
    pagamentos_descricao_pagamento = Column(String(100))
    pagamentos_valor_pagamento = Column(Integer)
    outros_data_pagamento = Column(Date)
    outros_n_cheque = Column(Integer)
    outros_descricao_pagamento = Column(String(100))
    outros_valor_pagamento = Column(Integer)

    def to_dict(self):
        # Converte o objeto Cliente em um dicionário para fácil uso no front-end.
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def adicionar_lancamento(lancamento):
    try:
        novo_lancamento = Lancamentos(**lancamento)
        session.add(novo_lancamento)
        session.commit()
        return novo_lancamento.id
    except Exception as e:
        session.rollback()
        print(f"Erro ao adicionar lançamento: {e}")
        return None
    finally:
        session.close()


def atualizar_lancamento(id, dados):
    try:
        lancamento = session.query(Lancamentos).filter_by(id=id).first()
        if lancamento:
            for key, value in dados.items():
                setattr(lancamento, key, value)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erro ao atualizar cliente: {e}")
        return False
    finally:
        session.close()


def get_lancamentos():
    lancamento = session.query(Lancamentos).order_by(Lancamentos.id).all()
    session.close()
    return [lancamento.to_dict() for i in lancamento]
