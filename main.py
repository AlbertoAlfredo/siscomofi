import webview
from flask import Flask, render_template, redirect, url_for, request
import database
import os
import math


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,
            static_folder=os.path.join(basedir, 'static'),
            template_folder=os.path.join(basedir, 'templates')
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


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/clientes-cadastro", methods=['GET', 'POST'])
def clientes_cadastro():
    if request.method == "POST":

        cliente = {
            "nome_cliente": request.form["nome"],
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
    elif request.method == 'GET' and request.args.get('id'):
        cliente = database.get_cliente_por_id(request.args.get('id'))
        return render_template("clientes-cadastro.html", cliente = cliente)
    else:
        return render_template("clientes-cadastro.html")
    
@app.route("/clientes-atualiza", methods=['GET', 'POST'])  
def clientes_atualiza():
    cliente = {
        "id": request.form.get('id'),
        "nome_cliente": request.form.get("nome"),
        "nome_propriedade": request.form.get("npropriedade"),
        "endereco": request.form.get("endereco"),
        "numero": request.form.get("numero"),
        "bairro": request.form.get("bairro"),
        "cidade": request.form.get("cidade"),
        "uf": request.form.get("uf"),
        "tipo_pessoa": request.form.get("tipopessoa"),
        "cpf_cnpj": request.form.get("cpfcnpj"),
        "inscricao_estadual": request.form.get("iestadual"),
        "telefone": request.form.get("fone"),
        "celular": request.form.get("celular"),
        "valor_honorario": request.form.get("valorhonorario"),
        "observacoes": request.form.get("observacoes"),
    }
    database.atualizar_cliente(cliente['id'], cliente)
    return redirect(url_for('clientes_lista'))

@app.route("/cliente_apagar", methods=['GET'])
def cliente_apagar():
    cliente_id = request.args.get('id')
    database.deletar_cliente(cliente_id)
    return redirect(url_for('clientes_lista'))
    
@app.route("/clientes_lista", methods=['GET'])
def clientes_lista():
    page = request.args.get('page', 1, type=int)
    ITENS_POR_PAGINA = 10
    clientes_da_pagina = database.get_clientes_paginados(page, ITENS_POR_PAGINA)
    total_clientes = database.count_total_clientes()
    total_paginas = math.ceil(total_clientes / ITENS_POR_PAGINA)

    return render_template("clientes-lista.html",
                           clientes = clientes_da_pagina,
                           pagina_atual = page,
                           total_paginas = total_paginas
                           )
    # clientes_lista = database.get_clientes()
    # return render_template("clientes-lista.html", clientes = clientes_lista)

if __name__ == "__main__":
    # Garante que o banco de dados e as tabelas existam
    database.init_db()

    #Inicia o programa com o debug ativado
    webview.start(
        debug=False,
        icon="static/logo.png"
        )

    # app.run(debug=False)