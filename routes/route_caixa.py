from flask import render_template, request, Blueprint, redirect, url_for
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.cyextension.processors import to_float
from datetime import date, datetime

from sqlalchemy.dialects.mysql import BIGINT

import models.base as bd
import math, utils

caixa_bp = Blueprint(
    name="caixa_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


class Lancamentos(bd.Base):
    __tablename__ = "caixa_banco"

    id = Column(Integer, primary_key=True)
    data_lancamento = Column(Date)
    n_doc = Column(String)
    historico_lancamento = Column(String)
    credito_deposito = Column(String)
    debito_saque = Column(String)
    deposito_bloqueado = Column(String)
    taxa_servico_mensal = Column(String)
    tx_servicos_diversos = Column(String)
    bd.init_db()

def soma_pagamentos_totais(id):
    pagamentos_totais = 0
    agenfa = bd.get_all_filter(Agenfa, id_lancamento=id)
    iagro = bd.get_all_filter(Iagro, id_lancamento=id)
    pagamentos = bd.get_all_filter(Pagamentos, id_lancamento=id)
    outros = bd.get_all_filter(Outros, id_lancamento=id)

    if agenfa:
        for pagamento in agenfa:
            pagamentos_totais += pagamento.valor_pagamento
    if iagro:
        for pagamento in iagro:
            pagamentos_totais += pagamento.valor_pagamento
    if pagamentos:
        for pagamento in pagamentos:
            pagamentos_totais += pagamento.valor_pagamento
    if outros:
        for pagamento in outros:
            pagamentos_totais += pagamento.valor_pagamento
    tx_diversas = bd.get_for_id(Lancamentos, id)
    pagamentos_totais += float(utils.money_for_front(tx_diversas.taxa_servico_mensal))
    pagamentos_totais += float(utils.money_for_front(tx_diversas.tx_servicos_diversos))
    return "{:.2f}".format(pagamentos_totais)

def soma_honorarios(id):
    pagamentos_totais = float(soma_pagamentos_totais(id))
    credito = bd.get_for_id(Lancamentos, id)
    debito = credito.debito_saque
    debito = float(utils.money_for_front(debito))
    credito = float(utils.money_for_front(credito.credito_deposito))
    return "{:.2f}".format( credito - pagamentos_totais - debito)
@caixa_bp.route("/caixabanco", methods=["GET"])
def get_lancamentos():
    id = request.args.get('id')

    if id is None:
        movimento = request.args.get("movimento")
        return render_template("movimento.html", movimento=movimento)
    else:
        lancamento = bd.get_for_id(Lancamentos, id)

        pagamentos_totais = float(soma_pagamentos_totais(id))


        credito = float(lancamento.credito_deposito if lancamento.credito_deposito else 0) - float(lancamento.debito_saque if lancamento.debito_saque else 0)
        return render_template("movimento.html", movimento=lancamento, honorario=soma_honorarios(id), taxa_servico=pagamentos_totais, id=id)

@caixa_bp.route("/caixabanco", methods=["POST"])
def create_lancamento():
    if request.method == "POST":
        lancamento = {
            "data_lancamento": datetime.strptime(request.form["data_lancamento"], '%Y-%m-%d').date() ,
            "n_doc": request.form["n_doc"],
            "historico_lancamento": request.form["historico_lancamento"],
            "credito_deposito": utils.money_for_db(request.form["credito_deposito"]),
            "debito_saque": utils.money_for_db(request.form["debito_saque"]),
            "deposito_bloqueado": utils.money_for_db(request.form["deposito_bloqueado"]),
            "taxa_servico_mensal": utils.money_for_db(request.form["taxa_servico_mensal"]),
            "tx_servicos_diversos": utils.money_for_db(request.form["tx_servicos_diversos"]),
        }
        id = bd.add(Lancamentos, lancamento)

        return redirect("/caixabanco?id={}".format(id))

@caixa_bp.route("/caixabanco/edit", methods=["POST"])
def edit_lancamento():
    lancamento = {
        "data_lancamento": datetime.strptime(request.form["data_lancamento"], '%Y-%m-%d').date(),
        "n_doc": request.form["n_doc"],
        "historico_lancamento": request.form["historico_lancamento"],
        "credito_deposito": utils.money_for_db(to_float(request.form["credito_deposito"] if request.form["credito_deposito"] else 0)),
        "debito_saque": utils.money_for_db(to_float(request.form["debito_saque"] if request.form["debito_saque"] else 0)),
        "deposito_bloqueado": utils.money_for_db(to_float(request.form["deposito_bloqueado"] if request.form["deposito_bloqueado"] else 0)),
        "taxa_servico_mensal": utils.money_for_db(to_float(request.form["taxa_servico_mensal"] if request.form["taxa_servico_mensal"] else 0)),
        "tx_servicos_diversos": utils.money_for_db(to_float(request.form["tx_servicos_diversos"] if request.form["tx_servicos_diversos"] else 0)),
    }
    id = request.form["id"]
    bd.update(Lancamentos, str(id), lancamento)

    return redirect("/caixabanco?id={}".format(id))

@caixa_bp.route("/caixabanco/listar", methods=["GET"])
def list_lancamentos():
    page = request.args.get('page', 1, type=int)
    ITENS_POR_PAGINA = 10
    lancamentos_da_pagina = bd.get_paginate(Lancamentos, Lancamentos.data_lancamento, page, ITENS_POR_PAGINA)
    total_lancamentos = bd.count_total(Lancamentos)
    total_paginas = math.ceil(total_lancamentos / ITENS_POR_PAGINA)

    return render_template("lancamentos_lista.html",
                           lancamentos=lancamentos_da_pagina,
                           pagina_atual=page,
                           total_paginas=total_paginas
                           )

@caixa_bp.route("/caixabanco/apagar", methods=["GET"])
def delete_lancamento():
    id = request.args.get('id')
    bd.delete(Lancamentos, id)
    return redirect(url_for("caixa_bp.list_lancamentos"))



class Agenfa(bd.Base):
    __tablename__ = "caixa_banco_agenfa"

    id = Column(Integer, primary_key=True)
    id_lancamento = Column(Integer, ForeignKey('caixa_banco.id'))
    data_pagamento = Column(Date)
    n_cheque = Column(BIGINT)
    descricao_pagamento = Column(String)
    valor_pagamento = Column(BIGINT)


@caixa_bp.route("/caixabanco/agenfa", methods=["GET", "POST"])
def get_lancamentos_agenfa():
    id = request.args.get('id')
    lancamento = bd.get_for_id(Lancamentos, id)
    credito = float(lancamento.credito_deposito if lancamento.credito_deposito else 0) - float(lancamento.debito_saque if lancamento.debito_saque else 0)
    credito = utils.money_for_front(int(credito))
    pagamentos_totais = soma_pagamentos_totais(id)
    if request.method == "POST":

        lancamento_agenfa = {
            "id_lancamento": lancamento.id,
            "data_pagamento": datetime.strptime(request.form["data_pagamento"], '%Y-%m-%d').date(),
            "n_cheque": request.form["n_cheque"],
            "descricao_pagamento": request.form["descricao_pagamento"],
            "valor_pagamento": request.form["valor_pagamento"],
        }

        bd.add(Agenfa, lancamento_agenfa)
    if request.args.get("apagar"):
        bd.delete(Agenfa, request.args.get("apagar"))
    agenfa = bd.get_all_filter(Agenfa, id_lancamento=id)

    return render_template("agenfa.html", movimento=lancamento, honorario=soma_honorarios(id), credito=credito, taxa_servico=pagamentos_totais, agenfa=agenfa)

class Iagro(bd.Base):
    __tablename__ = "caixa_banco_iagro"

    id = Column(Integer, primary_key=True)
    id_lancamento = Column(Integer, ForeignKey('caixa_banco.id'))
    data_pagamento = Column(Date)
    n_cheque = Column(BIGINT)
    descricao_pagamento = Column(String)
    valor_pagamento = Column(BIGINT)
@caixa_bp.route("/caixabanco/iagro", methods=["GET", "POST"])
def get_lancamentos_iagro():
    id = request.args.get('id')
    lancamento = bd.get_for_id(Lancamentos, id)
    credito = float(lancamento.credito_deposito if lancamento.credito_deposito else 0) - float(lancamento.debito_saque if lancamento.debito_saque else 0)
    credito = utils.money_for_front(int(credito))
    pagamentos_totais = soma_pagamentos_totais(id)
    if request.method == "POST":

        lancamento_iagro = {
            "id_lancamento": lancamento.id,
            "data_pagamento": datetime.strptime(request.form["data_pagamento"], '%Y-%m-%d').date(),
            "n_cheque": request.form["n_cheque"],
            "descricao_pagamento": request.form["descricao_pagamento"],
            "valor_pagamento": request.form["valor_pagamento"],
        }
        bd.add(Iagro, lancamento_iagro)
    if request.args.get("apagar"):
        bd.delete(Iagro, request.args.get("apagar"))
    iagro = bd.get_all_filter(Iagro, id_lancamento = id)

    return render_template("iagro.html", movimento=lancamento, honorario=soma_honorarios(id), credito=credito, taxa_servico=pagamentos_totais, iagro=iagro)

class Pagamentos(bd.Base):
    __tablename__ = "caixa_banco_pagamentos"

    id = Column(Integer, primary_key=True)
    id_lancamento = Column(Integer, ForeignKey('caixa_banco.id'))
    data_pagamento = Column(Date)
    n_cheque = Column(BIGINT)
    descricao_pagamento = Column(String)
    valor_pagamento = Column(BIGINT)
@caixa_bp.route("/caixabanco/pagamentos", methods=["GET", "POST"])
def get_lancamentos_pagamentos():
    id = request.args.get('id')
    lancamento = bd.get_for_id(Lancamentos, id)
    credito = float(lancamento.credito_deposito if lancamento.credito_deposito else 0) - float(lancamento.debito_saque if lancamento.debito_saque else 0)
    credito = utils.money_for_front(int(credito))
    pagamentos_totais = soma_pagamentos_totais(id)

    if request.method == "POST":

        lancamento_pagamentos = {
            "id_lancamento": lancamento.id,
            "data_pagamento": datetime.strptime(request.form["data_pagamento"], '%Y-%m-%d').date(),
            "n_cheque": request.form["n_cheque"],
            "descricao_pagamento": request.form["descricao_pagamento"],
            "valor_pagamento": request.form["valor_pagamento"],
        }
        bd.add(Pagamentos, lancamento_pagamentos)
    if request.args.get("apagar"):
        bd.delete(Pagamentos, request.args.get("apagar"))
    pagamentos = bd.get_all_filter(Pagamentos, id_lancamento=id)
    return render_template("pagamentos.html", movimento=lancamento, honorario=soma_honorarios(id), credito=credito, taxa_servico=pagamentos_totais, pagamentos=pagamentos)


class Outros(bd.Base):
    __tablename__ = "caixa_banco_outros"

    id = Column(Integer, primary_key=True)
    id_lancamento = Column(Integer, ForeignKey('caixa_banco.id'))
    data_pagamento = Column(Date)
    n_cheque = Column(BIGINT)
    descricao_pagamento = Column(String)
    valor_pagamento = Column(BIGINT)

@caixa_bp.route("/caixabanco/outros", methods=["GET", "POST"])
def get_lancamentos_outros():
    id = request.args.get('id')
    lancamento = bd.get_for_id(Lancamentos, id)
    credito = float(lancamento.credito_deposito if lancamento.credito_deposito else 0) - float(lancamento.debito_saque if lancamento.debito_saque else 0)
    credito = utils.money_for_front(int(credito))
    pagamentos_totais = soma_pagamentos_totais(id)

    if request.method == "POST":

        lancamento_outros = {
            "id_lancamento": lancamento.id,
            "data_pagamento": datetime.strptime(request.form["data_pagamento"], '%Y-%m-%d').date(),
            "n_cheque": request.form["n_cheque"],
            "descricao_pagamento": request.form["descricao_pagamento"],
            "valor_pagamento": request.form["valor_pagamento"],
        }
        bd.add(Outros, lancamento_outros)
    if request.args.get("apagar"):
        bd.delete(Outros, request.args.get("apagar"))
    outros = bd.get_all_filter(Outros, id_lancamento=id)

    return render_template("outros.html", movimento=lancamento, honorario=soma_honorarios(id), credito=credito, taxa_servico=pagamentos_totais, outros=outros)