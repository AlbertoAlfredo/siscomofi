import math

from flask import render_template, request, Blueprint, redirect, url_for
from datetime import date, datetime
from routes.route_caixa import Lancamentos as lancamentos
from models.base import get_all, filter_date
import utils

relatorios_bp = Blueprint(
                    'relatorios',
                          __name__,
                          template_folder='templates'
                          )

@relatorios_bp.route('/relatorios/receitadespesa', methods=['GET'])
def relatorios_receitadespesa():
    data_inicio = datetime.strptime(request.args.get('data_inicio'), '%Y-%m-%d').date() if request.args.get('data_inicio') else False
    data_fim = datetime.strptime(request.args.get('data_fim'), '%Y-%m-%d').date() if request.args.get('data_fim') else False
    if data_inicio and data_fim and data_inicio > data_fim:
        return render_template("relatorios/relatorio_receitas_despesas.html", erro=True, utils=utils)
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
    return render_template("relatorios/relatorio_receitas_despesas.html", receitas=relatorio, utils=utils)