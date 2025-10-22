from flask import render_template, request, Blueprint, redirect, url_for
from models.lancamento import adicionar_lancamento

caixa_bp = Blueprint(
    name="caixa_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


@caixa_bp.route("/caixabanco", methods=["GET"])
def get_lancamentos():
    return render_template("lancamentos_caixa_banco.html")


@caixa_bp.route("/caixabanco", methods=["POST"])
def create_lancamento():
    lancamento = {
        "movimento_data_lancamento": request.form["data_lancamento"],
        "movimento_n_doc": request.form["n_doc"],
        "movimento_historico_lancamento": request.form["historico_lancamento"],
        "agenfa_data_pagamento": request.form["agenfa_data_pagamento"],
        "agenfa_n_cheque": request.form["agenfa_n_cheque"],
        "agenfa_descricao_pagamento": request.form["agenfa_descricao_pagamento"],
        "agenfa_valor_pagamento": request.form["agenfa_valor_pagamento"],
        "iagro_data_pagamento": request.form["iagro_data_pagamento"],
        "iagro_n_cheque": request.form["iagro_n_cheque"],
        "iagro_descricao_pagamento": request.form["iagro_descricao_pagamento"],
        "iagro_valor_pagamento": request.form["iagro_valor_pagamento"],
        "pagamentos_data_pagamento": request.form[
            "pagamentos_pagamentos_data_pagamento"
        ],
        "pagamentos_n_cheque": request.form["pagamentos_n_cheque"],
        "pagamentos_descricao_pagamento": request.form[
            "pagamentos_descricao_pagamento"
        ],
        "pagamentos_valor_pagamento": request.form["pagamentos_valor_pagamento"],
        "outros_data_pagamento": request.form["outros_data_pagamento"],
        "outros_n_cheque": request.form["outros_n_cheque"],
        "outros_descricao_pagamento": request.form["outros_descricao_pagamento"],
        "outros_valor_pagamento": request.form["outros_valor_pagamento"],
    }
    adicionar_lancamento(lancamento)

    return redirect(url_for("get_lancamentos"))
