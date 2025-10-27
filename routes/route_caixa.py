from flask import render_template, request, Blueprint, redirect, url_for
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.cyextension.processors import to_float
from datetime import date, datetime

from sqlalchemy.dialects.mysql import BIGINT

import models.base as base
import math, utils

caixa_bp = Blueprint(
    name="caixa_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)

def calc_credito():
    return

class Lancamentos(base.Base):
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
    # agenfa_data_pagamento = Column(Date)
    # agenfa_n_cheque = Column(Integer)
    # agenfa_descricao_pagamento = Column(String(100))
    # agenfa_valor_pagamento = Column(Integer)
    # iagro_data_pagamento = Column(Date)
    # iagro_n_cheque = Column(Integer)
    # iagro_descricao_pagamento = Column(String(100))
    # iagro_valor_pagamento = Column(Integer)
    # pagamentos_data_pagamento = Column(Date)
    # pagamentos_n_cheque = Column(Integer)
    # pagamentos_descricao_pagamento = Column(String(100))
    # pagamentos_valor_pagamento = Column(Integer)
    # outros_data_pagamento = Column(Date)
    # outros_n_cheque = Column(Integer)
    # outros_descricao_pagamento = Column(String(100))
    # outros_valor_pagamento = Column(Integer)
    base.init_db()
@caixa_bp.route("/caixabanco", methods=["GET"])
def get_lancamentos():
    id = request.args.get('id')

    if id is None:
        movimento = request.args.get("movimento")
        return render_template("movimento.html", movimento=movimento)
    else:
        lancamento = base.get_for_id(Lancamentos, id)
        credito = float(lancamento.credito_deposito) - float(lancamento.debito_saque)
        credito = utils.money_for_front(int(credito))
        return render_template("movimento.html", movimento=lancamento, credito=credito, id=id)

@caixa_bp.route("/caixabanco", methods=["POST"])
def create_lancamento():
    if request.method == "POST":
        lancamento = {
            "data_lancamento": datetime.strptime(request.form["data_lancamento"], '%Y-%m-%d').date() ,
            "n_doc": request.form["n_doc"],
            "historico_lancamento": request.form["historico_lancamento"],
            "credito_deposito": utils.money_for_db(to_float(request.form["credito_deposito"])),
            "debito_saque": utils.money_for_db(to_float(request.form["debito_saque"])),
            "deposito_bloqueado": utils.money_for_db(to_float(request.form["deposito_bloqueado"])),
            "taxa_servico_mensal": utils.money_for_db(to_float(request.form["taxa_servico_mensal"])),
            "tx_servicos_diversos": utils.money_for_db(to_float(request.form["tx_servicos_diversos"])),
        }
        id = base.add(Lancamentos, lancamento)

        return redirect("/caixabanco?id={}".format(id))

@caixa_bp.route("/caixabanco/edit", methods=["POST"])
def edit_lancamento():
    lancamento = {
        "data_lancamento": datetime.strptime(request.form["data_lancamento"], '%Y-%m-%d').date(),
        "n_doc": request.form["n_doc"],
        "historico_lancamento": request.form["historico_lancamento"],
        "credito_deposito": utils.money_for_db(to_float(request.form["credito_deposito"])),
        "debito_saque": utils.money_for_db(to_float(request.form["debito_saque"])),
        "deposito_bloqueado": utils.money_for_db(to_float(request.form["deposito_bloqueado"])),
        "taxa_servico_mensal": utils.money_for_db(to_float(request.form["taxa_servico_mensal"])),
        "tx_servicos_diversos": utils.money_for_db(to_float(request.form["tx_servicos_diversos"])),
    }
    id = request.form["id"]
    base.update(Lancamentos, str(id), lancamento)

    return redirect("/caixabanco?id={}".format(id))

@caixa_bp.route("/caixabanco/listar", methods=["GET"])
def list_lancamentos():
    page = request.args.get('page', 1, type=int)
    ITENS_POR_PAGINA = 10
    lancamentos_da_pagina = base.get_paginate(Lancamentos, Lancamentos.data_lancamento, page, ITENS_POR_PAGINA)
    total_lancamentos = base.count_total(Lancamentos)
    total_paginas = math.ceil(total_lancamentos / ITENS_POR_PAGINA)

    return render_template("lancamentos_lista.html",
                           lancamentos=lancamentos_da_pagina,
                           pagina_atual=page,
                           total_paginas=total_paginas
                           )

@caixa_bp.route("/caixabanco/apagar", methods=["GET"])
def delete_lancamento():
    id = request.args.get('id')
    base.delete(Lancamentos, id)
    return redirect(url_for("caixa_bp.list_lancamentos"))



class Agenfa(base.Base):
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
    lancamento = base.get_for_id(Lancamentos, id)
    credito = float(lancamento.credito_deposito) - float(lancamento.debito_saque)
    credito = utils.money_for_front(int(credito))

    if request.method == "POST":

        lancamento_agenfa = {
            "id_lancamento": lancamento.id,
            "data_pagamento": datetime.strptime(request.form["data_pagamento"], '%Y-%m-%d').date(),
            "n_cheque": request.form["n_cheque"],
            "descricao_pagamento": request.form["descricao_pagamento"],
            "valor_pagamento": request.form["valor_pagamento"],
        }

        base.add(Agenfa, lancamento_agenfa)
    if request.args.get("apagar"):
        base.delete(Agenfa, request.args.get("apagar"))
    agenfa = base.get_all_filter(Agenfa, id_lancamento=id)

    return render_template("agenfa.html", movimento=lancamento, credito=credito, agenfa=agenfa)

class Iagro(base.Base):
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
    lancamento = base.get_for_id(Lancamentos, id)
    credito = float(lancamento.credito_deposito) - float(lancamento.debito_saque)
    credito = utils.money_for_front(int(credito))

    if request.method == "POST":

        lancamento_iagro = {
            "id_lancamento": lancamento.id,
            "data_pagamento": datetime.strptime(request.form["data_pagamento"], '%Y-%m-%d').date(),
            "n_cheque": request.form["n_cheque"],
            "descricao_pagamento": request.form["descricao_pagamento"],
            "valor_pagamento": request.form["valor_pagamento"],
        }
        base.add(Iagro, lancamento_iagro)
    if request.args.get("apagar"):
        base.delete(Iagro, request.args.get("apagar"))
    iagro = base.get_all_filter(Iagro, id_lancamento = id)

    return render_template("iagro.html", movimento=lancamento, credito=credito, iagro=iagro)

class Pagamentos(base.Base):
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
    lancamento = base.get_for_id(Lancamentos, id)
    credito = float(lancamento.credito_deposito) - float(lancamento.debito_saque)
    credito = utils.money_for_front(int(credito))

    if request.method == "POST":

        lancamento_pagamentos = {
            "id_lancamento": lancamento.id,
            "data_pagamento": datetime.strptime(request.form["data_pagamento"], '%Y-%m-%d').date(),
            "n_cheque": request.form["n_cheque"],
            "descricao_pagamento": request.form["descricao_pagamento"],
            "valor_pagamento": request.form["valor_pagamento"],
        }
        base.add(Pagamentos, lancamento_pagamentos)
    if request.args.get("apagar"):
        base.delete(Pagamentos, request.args.get("apagar"))
    pagamentos = base.get_all_filter(Pagamentos, id_lancamento=id)
    return render_template("pagamentos.html", movimento=lancamento, credito=credito, pagamentos=pagamentos)


class Outros(base.Base):
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
    lancamento = base.get_for_id(Lancamentos, id)
    credito = float(lancamento.credito_deposito) - float(lancamento.debito_saque)
    credito = utils.money_for_front(int(credito))

    if request.method == "POST":

        lancamento_outros = {
            "id_lancamento": lancamento.id,
            "data_pagamento": datetime.strptime(request.form["data_pagamento"], '%Y-%m-%d').date(),
            "n_cheque": request.form["n_cheque"],
            "descricao_pagamento": request.form["descricao_pagamento"],
            "valor_pagamento": request.form["valor_pagamento"],
        }
        base.add(Outros, lancamento_outros)
    if request.args.get("apagar"):
        base.delete(Outros, request.args.get("apagar"))
    outros = base.get_all_filter(Outros, id_lancamento=id)

    return render_template("outros.html", movimento=lancamento, credito=credito, outros=outros)