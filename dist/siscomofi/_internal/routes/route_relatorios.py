import math

from flask import render_template, request, Blueprint, redirect, url_for
from datetime import date, datetime
from routes.route_caixa import Lancamentos as lancamentos
from routes.route_caixa import soma_pagamentos_totais, Agenfa, Pagamentos, Iagro, Depositos, Outros 
from routes.route_receitas_despesas import Lancamentos as receitas
from routes.route_clientes import Clientes as clientes
from models.base import get_all, filter_date, get_busca, get_for_id, get_all_filter, filter_date_and_search
import utils

relatorios_bp = Blueprint(
    'relatorios',
    __name__,
    template_folder='templates'
)


# ======================================================================
# FUNÇÃO AUXILIAR GENÉRICA PARA GERAR RELATÓRIOS POR DATA
# ======================================================================
def gerar_relatorio(model, campo_data, template, extra_context=None, colunas_busca=None):
    """
    Gera relatório com filtros de data e (opcionalmente) busca textual.
    """

    # Captura datas
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date() if data_inicio else False
    data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date() if data_fim else False

    # Captura busca textual
    busca = request.args.get("busca")

    # Validação
    if data_inicio and data_fim and data_inicio > data_fim:
        return render_template(template, erro=True, utils=utils)

    # Decide se usa busca + data OU só data
    if colunas_busca and busca:
        relatorio = filter_date_and_search(
            model,
            campo_data,
            data_inicio,
            data_fim,
            busca,
            colunas_busca
        )
    else:
        # Libera fluxo padrão (só por data)
        if data_inicio or data_fim:
            relatorio = filter_date(model, campo_data, date_inicio=data_inicio, date_fim=data_fim)
        else:
            relatorio = get_all(model, order_by=campo_data)

    # Contexto enviado pro template
    context = {
        "receitas": relatorio,
        "utils": utils
    }

    if extra_context:
        context.update(extra_context)

    return render_template(template, **context)



# ======================================================================
# ROTAS DE RELATÓRIOS 
# ======================================================================

@relatorios_bp.route('/relatorios/saldo', methods=['GET'])
def relatorios_receitadespesa():
    return gerar_relatorio(
        model=lancamentos,
        campo_data=lancamentos.data_lancamento,
        template="relatorios/rel_saldo.html",
        extra_context={"pagamentos": soma_pagamentos_totais}
    )


@relatorios_bp.route('/relatorios/geral', methods=['GET'])
def relatorios_geral():
    id = request.args.get("id")
    if id:
        receitas = get_for_id(lancamentos, id)
        agenfa = get_all_filter(Agenfa, id_lancamento=id)
        iagro = get_all_filter(Iagro, id_lancamento=id)
        pagamento = get_all_filter(Pagamentos, id_lancamento=id)
        depositos = get_all_filter(Depositos, id_lancamento=id)
        outros = get_all_filter(Outros, id_lancamento=id)
        return render_template("relatorios/rel_geral.html", receitas=receitas, utils=utils, id=id, agenfa=agenfa, iagro=iagro, pagamento=pagamento, depositos=depositos, outros=outros)
    else:
        return gerar_relatorio(
            model=lancamentos,
            campo_data=lancamentos.data_lancamento,
            template="relatorios/rel_geral.html",
            extra_context={"pagamentos": soma_pagamentos_totais,
                            "agenfa": Agenfa,
                            "iagro": Iagro,
                            "pagamento": Pagamentos,
                            "depositos": Depositos,
                            "outros": Outros,
                            "filter": get_all_filter
                            },
            colunas_busca=[
                lancamentos.historico_lancamento,
                lancamentos.n_doc
            ]
        )



@relatorios_bp.route('/relatorios/honorarios_taxas', methods=['GET'])
def relatorios_honorarios():
    return gerar_relatorio(
        model=receitas,
        campo_data=receitas.data_lancamento,
        template="relatorios/rel_taxas.html"
    )


@relatorios_bp.route("/relatorios/resumo-geral", methods=["GET"])
def resumo_geral():
    return gerar_relatorio(
        model=receitas,
        campo_data=receitas.data_lancamento,
        template="relatorios/rel_resumo_geral.html"
    )


# ======================================================================
# RELATÓRIO COM BUSCA (ESSE NÃO USA DATA)
# ======================================================================

@relatorios_bp.route("/relatorios/honorarios", methods=["GET"])
def honorarios():
    busca = request.args.get('busca')

    if busca:
        relatorio = get_busca(
            clientes,
            busca,
            [
                clientes.nome_cliente,
                clientes.nome_propriedade,
                clientes.cpf_cnpj
            ]
        )
    else:
        relatorio = get_all(clientes, order_by=clientes.nome_cliente)

    return render_template(
        "relatorios/honorarios.html",
        clientes=relatorio,
        utils=utils
    )
