import math

from flask import render_template, request, Blueprint, redirect, url_for
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.mysql import BIGINT
from datetime import date, datetime

import models.base as bd

receitas_despesas_bp = Blueprint(
    name="receitas_despesas_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


class Lancamentos(bd.Base):
    __tablename__ = "receitas_despesas"

    id = Column(Integer, primary_key=True)
    historico = Column(String)
    data_lancamento = Column(Date)
    saldo_anterior = Column(BIGINT)
    honorario = Column(BIGINT)
    tx_servico_mensal = Column(BIGINT)
    dirf = Column(BIGINT)
    dap = Column(BIGINT)
    ada_itr = Column(BIGINT)
    dec_terceiro = Column(BIGINT)
    pagamentos = Column(BIGINT)
    tx_outros_servicos = Column(BIGINT)


# lançar
# editar
# deletar
@receitas_despesas_bp.route("/receitas_despesas", methods=["GET", "POST"])
def receitas_despesas():
    lancamento = {}
    if request.method == "POST":
        lancamento = {
            "historico": request.form["historico"],
            "saldo_anterior": request.form["saldo_anterior"],
            "data_lancamento": datetime.strptime(request.form["data_lancamento"], '%Y-%m-%d').date() ,
            "tx_servico_mensal": request.form["tx_servico_mensal"],
            "honorario": request.form["honorario"],
            "dirf": request.form["dirf"],
            "dap": request.form["dap"],
            "ada_itr": request.form["ada_itr"],
            "dec_terceiro": request.form["dec_terceiro"],
            "pagamentos": request.form["pagamentos"],
            "tx_outros_servicos": request.form["tx_outros_servicos"],
        }
    if request.method == "POST" and request.args.get("id"):
        id = request.args.get("id")
        bd.update(Lancamentos, id, lancamento)
        return redirect(url_for("receitas_despesas_bp.receitas_despesas_listar"))

    elif request.method == "POST":
        bd.add(Lancamentos, lancamento)
        return redirect(url_for("receitas_despesas_bp.receitas_despesas_listar"))
    elif request.method == "GET" and request.args.get("id") and request.args.get("delete"):
        id = request.args.get("id")
        bd.delete(Lancamentos, id)
        return redirect(url_for("receitas_despesas_bp.receitas_despesas_listar"))
    elif request.method == "GET" and request.args.get("id"):
        id = request.args.get("id")
        lancamentos = bd.get_for_id(Lancamentos, id)
        return render_template("receitas_despesas.html", lancamentos=lancamentos)
    elif request.method == "GET" and request.form.get("id") == None:
        return render_template("receitas_despesas.html", lancamentos=lancamento)




# listar
@receitas_despesas_bp.route("/receitas_despesas/listar", methods=["GET"])
def receitas_despesas_listar():
    page = request.args.get('page', 1, type=int)
    ITENS_POR_PAGINA = 10
    lancamentos_da_pagina = bd.get_paginate(Lancamentos, Lancamentos.data_lancamento, page, ITENS_POR_PAGINA)
    total_lancamentos = bd.count_total(Lancamentos)
    total_paginas = math.ceil(total_lancamentos / ITENS_POR_PAGINA)

    return render_template("receitas_despesas_lista.html",
                           lancamentos=lancamentos_da_pagina,
                           pagina_atual=page,
                           total_paginas=total_paginas
                           )
