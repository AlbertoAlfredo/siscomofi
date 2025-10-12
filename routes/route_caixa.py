from flask import Flask, render_template, request, Blueprint, redirect, url_for

caixa_bp = Blueprint(
                                name="caixa_bp",
                                import_name=__name__,
                                static_folder='static',
                                template_folder='templates'
                                )

@caixa_bp.route('/caixabanco', methods=["GET", "POST"])
def caixa_banco():
    if request.method == "POST":
        lancamento = {
            "movimento": {
                'data_lancamento': request.form.data_lancamento,
                'n_doc': request.form.n_doc,
                'historico_lancamento': request.form.historico_lancamento
            },
            "agenfa": {
                "data_pagamento": request.form.agenfa_data_pagamento,
                "data_pagamento": request.form.agenfa_n_cheque,
                "data_pagamento": request.form.agenfa_descricao_pagamento,
                "data_pagamento": request.form.agenfa_valor_pagamento
            },
            "iagro": {
                "data_pagamento": request.form.iagro_data_pagamento,
                "data_pagamento": request.form.iagro_n_cheque,
                "data_pagamento": request.form.iagro_descricao_pagamento,
                "data_pagamento": request.form.iagro_valor_pagamento
            },
            "pagamentos": {
                "data_pagamento": request.form.pagamentos_data_pagamento,
                "data_pagamento": request.form.pagamentos_n_cheque,
                "data_pagamento": request.form.pagamentos_descricao_pagamento,
                "data_pagamento": request.form.pagamentos_valor_pagamento
            },
            "outros": {
                "data_pagamento": request.form.outros_data_pagamento,
                "data_pagamento": request.form.outros_n_cheque,
                "data_pagamento": request.form.outros_descricao_pagamento,
                "data_pagamento": request.form.outros_valor_pagamento
            }
        }
    return render_template('lancamentos_caixa_banco.html')