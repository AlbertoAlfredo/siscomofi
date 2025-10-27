from flask import Flask, render_template, url_for, redirect
from routes import route_caixa, route_clientes
from models.base import init_db
import os, webview


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(basedir, "static"),
    template_folder=os.path.join(basedir, "templates"),
)
# Cria a janela do pywebview, passando o servidor Flask
window = webview.create_window(
    'SisCoMoFi - Sistema de Controle Financeiro',
    app,
    width=1200,
    height=800,
    confirm_close=True,
    resizable=True
    )
app.register_blueprint(blueprint=route_clientes.cliente_bp)
app.register_blueprint(blueprint=route_caixa.caixa_bp)


# Cria a janela do pywebview, passando o servidor Flask
# window = webview.create_window(
#     "SisCoMoFi - Sistema de Controle Financeiro",
#     app,
#     width=1200,
#     height=800,
#     confirm_close=True,
#     resizable=True,
# )


@app.route("/")
def home():
    return render_template("index.html")
    # return redirect(url_for('cliente_bp.clientes_lista'))


if __name__ == "__main__":
    # Garante que o banco de dados e as tabelas existam
    init_db()

    # Inicia o programa
    webview.start(
        debug=False,
        icon="static/logo.png"
    )

    # app.run(debug=True)
