import math
from flask import Flask, render_template, request, Blueprint, redirect, url_for
from sqlalchemy import Column, Integer, String, Float
import models.base as db
from models.base import Base

cliente_bp = Blueprint(
                        'cliente_bp',
                             __name__,
                             static_folder='static',
                             template_folder='templates'
                             )

class Clientes(Base):
    __tablename__ = "clientes"

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
    valor_honorario = Column(Integer)
    observacoes = Column(String(500))

    def to_dict(self):
        """Converte o objeto Cliente num dicionário."""
        # Usa __table__.columns para obter dinamicamente todas as colunas
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@cliente_bp.route("/clientes-cadastro", methods=['GET', 'POST'])
def clientes_cadastro():
    if request.method == "POST":

        cliente = {
            "nome_cliente": request.form["nome"],
            "nome_propriedade": request.form["npropriedade"],
            "endereco": request.form["endereco"],
            "numero": request.form["numero"],
            "bairro": request.form["bairro"],
            "cidade": request.form["cidade"],
            "uf": request.form["uf"],
            "tipo_pessoa": request.form["tipopessoa"],
            "cpf_cnpj": request.form["cpfcnpj"],
            "inscricao_estadual": request.form["iestadual"],
            "telefone": request.form["fone"],
            "celular": request.form["celular"],
            "valor_honorario": request.form["valorhonorario"],
            "observacoes": request.form["observacoes"],
        }
        db.add(Clientes, cliente)
        return render_template("clientes-cadastro.html")
    elif request.method == 'GET' and request.args.get('id'):
        cliente = db.get_for_id(Clientes, request.args.get('id'))
        return render_template("clientes-cadastro.html", cliente = cliente)
    else:
        return render_template("clientes-cadastro.html")
    
@cliente_bp.route("/clientes-atualiza", methods=['GET', 'POST'])  
def clientes_atualiza():
    cliente = {
        "id": request.form.get('id'),
        "nome_cliente": request.form.get("nome"),
        "nome_propriedade": request.form.get("npropriedade"),
        "endereco": request.form.get("endereco"),
        "numero": request.form.get("numero"),
        "bairro": request.form.get("bairro"),
        "cidade": request.form.get("cidade"),
        "uf": request.form.get("uf"),
        "tipo_pessoa": request.form.get("tipopessoa"),
        "cpf_cnpj": request.form.get("cpfcnpj"),
        "inscricao_estadual": request.form.get("iestadual"),
        "telefone": request.form.get("fone"),
        "celular": request.form.get("celular"),
        "valor_honorario": request.form.get("valorhonorario"),
        "observacoes": request.form.get("observacoes"),
    }
    db.update(Clientes, cliente['id'], cliente)
    return redirect(url_for('cliente_bp.clientes_lista'))

@cliente_bp.route("/cliente_apagar", methods=['GET'])
def cliente_apagar():
    cliente_id = request.args.get('id')
    db.delete(Clientes, cliente_id)
    return redirect(url_for('cliente_bp.clientes_lista'))
    
@cliente_bp.route("/clientes_lista", methods=['GET'])
def clientes_lista():
    page = request.args.get('page', 1, type=int)
    ITENS_POR_PAGINA = 10
    clientes_da_pagina = db.get_paginate(Clientes, Clientes.nome_cliente, page, ITENS_POR_PAGINA)
    total_clientes = db.count_total(Clientes)
    total_paginas = math.ceil(total_clientes / ITENS_POR_PAGINA)

    return render_template("clientes-lista.html",
                           clientes = clientes_da_pagina,
                           pagina_atual = page,
                           total_paginas = total_paginas
                           )
