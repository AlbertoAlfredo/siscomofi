import math

from flask import render_template, request, Blueprint, redirect, url_for
from datetime import date, datetime
from routes.route_caixa import Lancamentos as lancamentos
from routes.route_caixa import soma_pagamentos_totais
from routes.route_receitas_despesas import Lancamentos as receitas
from routes.route_clientes import Clientes as clientes
from models.base import get_all, filter_date, get_busca
import utils


relatorios_bp = Blueprint(
                    'relatorios',
                          __name__,
                          template_folder='templates'
                          )

@relatorios_bp.route('/relatorios/saldo', methods=['GET'])
def relatorios_receitadespesa():
    data_inicio = datetime.strptime(request.args.get('data_inicio'), '%Y-%m-%d').date() if request.args.get('data_inicio') else False
    data_fim = datetime.strptime(request.args.get('data_fim'), '%Y-%m-%d').date() if request.args.get('data_fim') else False
    if data_inicio and data_fim and data_inicio > data_fim:
        return render_template("relatorios/rel_saldo.html", erro=True, utils=utils)
    elif data_inicio and data_fim:
        relatorio = filter_date(lancamentos, lancamentos.data_lancamento, data_inicio, data_fim)
    elif data_inicio:
        relatorio = filter_date(lancamentos, lancamentos.data_lancamento, date_inicio=data_inicio, date_fim=False)
    elif data_fim:
        relatorio = filter_date(lancamentos, lancamentos.data_lancamento, date_inicio=False, date_fim=data_fim)
    elif data_inicio and data_fim:
        relatorio = filter_date(lancamentos, lancamentos.data_lancamento, data_inicio, data_fim )
    else:
        relatorio = get_all(lancamentos, order_by=lancamentos.data_lancamento)
    pagamentos_totais = float(soma_pagamentos_totais(lancamentos.id)) * 100
    return render_template("relatorios/rel_saldo.html", receitas=relatorio, utils=utils, pagamentos=pagamentos_totais)

@relatorios_bp.route('/relatorios/honorarios_taxas', methods=['GET'])
def relatorios_honorarios():
    data_inicio = datetime.strptime(request.args.get('data_inicio'), '%Y-%m-%d').date() if request.args.get('data_inicio') else False
    data_fim = datetime.strptime(request.args.get('data_fim'), '%Y-%m-%d').date() if request.args.get('data_fim') else False
    if data_inicio and data_fim and data_inicio > data_fim:
        return render_template("relatorios/rel_taxas.html", erro=True, utils=utils)
    elif data_inicio and data_fim:
        relatorio = filter_date(receitas, receitas.data_lancamento, data_inicio, data_fim)
    elif data_inicio:
        relatorio = filter_date(receitas, receitas.data_lancamento, date_inicio=data_inicio, date_fim=False)
    elif data_fim:
        relatorio = filter_date(receitas, receitas.data_lancamento, date_inicio=False, date_fim=data_fim)
    elif data_inicio and data_fim:
        relatorio = filter_date(receitas, receitas.data_lancamento, data_inicio, data_fim )
    else:
        relatorio = get_all(receitas, order_by=receitas.data_lancamento)
    return render_template("relatorios/rel_taxas.html", receitas=relatorio, utils=utils)

@relatorios_bp.route("/relatorios/resumo-geral", methods=["GET"])
def resumo_geral():
    data_inicio = datetime.strptime(request.args.get('data_inicio'), '%Y-%m-%d').date() if request.args.get('data_inicio') else False
    data_fim = datetime.strptime(request.args.get('data_fim'), '%Y-%m-%d').date() if request.args.get('data_fim') else False
    if data_inicio and data_fim and data_inicio > data_fim:
        return render_template("relatorios/rel_resumo_geral.html", erro=True, utils=utils)
    elif data_inicio and data_fim:
        relatorio = filter_date(receitas, receitas.data_lancamento, data_inicio, data_fim)
    elif data_inicio:
        relatorio = filter_date(receitas, receitas.data_lancamento, date_inicio=data_inicio, date_fim=False)
    elif data_fim:
        relatorio = filter_date(receitas, receitas.data_lancamento, date_inicio=False, date_fim=data_fim)
    elif data_inicio and data_fim:
        relatorio = filter_date(receitas, receitas.data_lancamento, data_inicio, data_fim )
    else:
        relatorio = get_all(receitas, order_by=receitas.data_lancamento)
    return render_template("relatorios/rel_resumo_geral.html", receitas=relatorio, utils=utils)

@relatorios_bp.route("/relatorios/honorarios", methods=["GET"])
def honorarios():
    busca = request.args.get('busca')
    if busca:
        relatorio = get_busca(clientes, busca, [clientes.nome_cliente, clientes.nome_propriedade, clientes.cpf_cnpj])
    else:
        relatorio = get_all(clientes, order_by=clientes.nome_cliente)
    return render_template("relatorios/honorarios.html", clientes=relatorio, utils=utils)