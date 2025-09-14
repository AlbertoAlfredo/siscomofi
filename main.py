import webview
from flask import Flask, render_template, redirect, url_for, request
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
    confirm_close=True,
    resizable=True
    )


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/clientes-cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":

        cliente = {
            "nome": request.form["nome"],
            "nome_propriedade": request.form["npropriedade"],
            "endereco": request.form["endereco"],
            "numero": request.form["numero"],
            "bairro": request.form["bairro"],
            "cidade": request.form["cidade"],
            "uf": request.form["uf"],
            "tipo_pessoa": request.form["tipopessoa"],
            "cpf_cnpj": request.form["cpfcnpj"],
            "inscricao_estadual": request.form["iestadual"],
            "telefone": request.form["fone"],
            "celular": request.form["celular"],
            "valor_honorario": request.form["valorhonorario"],
            "observacoes": request.form["observacoes"],
        }
        database.adicionar_cliente(cliente)
        return render_template("clientes-cadastro.html")
    else:
        return render_template("clientes-cadastro.html")

    

if __name__ == "__main__":
    # Garante que o banco de dados e as tabelas existam
    database.init_db()

    # Inicia o programa com o debug ativado
    webview.start(
        debug=False,
        icon="static/logo.png"
        )

    # app.run(debug=False)