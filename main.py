from flask import Flask, render_template, url_for, redirect
from routes import route_caixa, route_clientes, route_receitas_despesas, route_relatorios
from models.base import init_db
from utils import format_phone
import os, webview


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(basedir, "static"),
    template_folder=os.path.join(basedir, "templates"),
)

app.jinja_env.filters['phone_format'] = format_phone

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
app.register_blueprint(blueprint=route_receitas_despesas.receitas_despesas_bp)
app.register_blueprint(blueprint=route_relatorios.relatorios_bp)



@app.route("/")
def home():
    return render_template("index.html")
    # return redirect(url_for('cliente_bp.clientes_lista'))


if __name__ == "__main__":
    # Garante que o banco de dados e as tabelas existam
    init_db()

    # Inicia o programa
    # webview.start(debug=False, icon="static/logo.png")

    app.run(debug=True)
