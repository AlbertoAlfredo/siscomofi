import webview
from flask import Flask
import database
import os

app = Flask(__name__)

# Cria a janela do pywebview, passando o servidor Flask
window = webview.create_window(
    'SisCoMoFi - Sistema de Controle Financeiro',
    app,
    width=1200,
    height=800,
    resizable=True
    )


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

    

if __name__ == "__main__":
    # Garante que o banco de dados e as tabelas existam
    database.init_db()

    # Nosso logo
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo.png')

    # Inicia o programa com o debug ativado
    webview.start(debug=True)