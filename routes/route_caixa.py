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
            }
        }
    return render_template('lancamentos_caixa_banco.html')