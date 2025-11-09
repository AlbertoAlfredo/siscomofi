import math

from flask import render_template, request, Blueprint, redirect, url_for
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.mysql import BIGINT
from datetime import date, datetime
from routes.route_caixa import Lancamentos as lancamentos

relatorios_bp = Blueprint(
                    'relatorios',
                          __name__,
                          template_folder='templates'
                          )

@relatorios_bp.route('/relatorios/receitadespesa', methods=['GET'])
def relatorios_receitadespesa():

    return render_template("relatorios/relatorio_receitas_despesas.html")