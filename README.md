# SisCoMoFi - Sistema de Controle de Movimentação Financeira

[![Linguagem Principal](https://img.shields.io/badge/language-Python-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask-000000.svg)](https://flask.palletsprojects.com/)
[![Licença](https://img.shields.io/badge/License-GPL%20v3-red.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Em%20Desenvolvimento-yellow.svg)]()

## 📝 Sobre o Projeto

O SisCoMoFi (Sistema de Controle de Movimentação Financeira) é uma aplicação de gestão financeira e de clientes desenvolvida em Python. A aplicação utiliza o framework Flask como servidor web e o PyWebView para empacotamento, permitindo que rode como uma aplicação desktop nativa.

Ele é projetado para centralizar o cadastro de clientes e o controle de lançamentos de receitas e despesas, oferecendo uma interface simples e funcional.

## ✨ Funcionalidades

O sistema oferece módulos de gerenciamento essenciais:

### Módulo de Clientes
* **Cadastro Completo:** Permite o registro detalhado de clientes, incluindo dados pessoais/fiscais (CPF/CNPJ, Inscrição Estadual) e contatos (Telefone, Celular).
* **Gestão de Dados:** Funções completas para Consultar, Editar e Apagar registros de clientes.
* **Listagem Paginada:** Exibição eficiente da lista de clientes com paginação.

### Módulo Financeiro (Receitas e Despesas)
* **Lançamentos Detalhados:** Permite registrar lançamentos com histórico, data, e valores específicos de honorários, taxas e impostos (DIRF, DAP, ADA/ITR, etc.).
* **Controle de Valores:** Utiliza o armazenamento de valores em centavos (para precisão) com formatação para o frontend (R$ X.XX).
* **Listagem e Edição:** Visualização e gestão dos lançamentos financeiros.

## 🛠️ Tecnologias Utilizadas

O projeto SisCoMoFi foi construído com as seguintes tecnologias:

* **Backend:** Python 3
* **Web Framework:** [Flask]
* **ORM:** [SQLAlchemy]
* **Interface Desktop:** [PyWebView]
* **Templating:** [Jinja2] (com filtros customizados para formatação de telefone e moeda)
* **Frontend/CSS:** [Bootstrap]

## 📦 Instalação e Execução

### Pré-requisitos

Certifique-se de ter o Python 3.x instalado em seu sistema.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/AlbertoAlfredo/siscomofi](https://github.com/AlbertoAlfredo/siscomofi)
    cd siscomofi
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Inicialize o Banco de Dados:**
    A aplicação usa SQLAlchemy e um arquivo de banco de dados local. A função `init_db()` em `main.py` garante que as tabelas sejam criadas na primeira execução.

4.  **Execute o SisCoMoFi:**
    Para iniciar o servidor Flask e a janela desktop PyWebView:
    ```bash
    python main.py
    ```
    *(Note: Se o `webview.start` estiver comentado no `main.py`, a linha de execução será `app.run(debug=True)`, iniciando o servidor em `http://127.0.0.1:5000`.)*

## 📄 Licença

Este projeto é distribuído sob a licença **GNU General Public License, Version 3 (GPL v3)**.

---
Desenvolvido por Alberto Alfredo.