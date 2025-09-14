import webview
from flask import Flask, render_template, redirect, url_for
import database
import os
import jinja2

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
def home():
    return render_template("index.html")

    

if __name__ == "__main__":
    # Garante que o banco de dados e as tabelas existam
    database.init_db()

    # Inicia o programa com o debug ativado
    webview.start(debug=True)

    # app.run(debug=False)