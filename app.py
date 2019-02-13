# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import hashlib
# importar operações CRUD
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# importar classes do arquivo "database_setup"
from setupdb import User, Category, Item

from flask import Flask, request, redirect, url_for, jsonify, abort

app = Flask(__name__)

# selecionar banco de dados
engine = create_engine(
    'sqlite:///catalog.db',
    connect_args={'check_same_thread': False}
)
# estabelecer conexão
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Variaves usadas para teste inicial
categoriesNames = ['sport', 'social', 'casual']
ids = [1, 2, 3, 4, 5]


@app.route("/")
@app.route("/catalog")
@app.route("/catalog.html")
def catalog():
    # checar argumento category
    categoryName = request.args.get('category', '')

    try:
        category = session.query(
            Category).filter_by(name=categoryName.title()).first()
        # mostrar itens de acordo com a categoria requisitada
        return ("Show categories and items of category " + category.name)
    except AttributeError:
        # mostrar itens recentes
        return "Show categories and latest items"


@app.route("/item")
@app.route("/item.html")
def showItem():
    # checar argumento id
    itemID = request.args.get('id')

    # retornar ao catalog se o id for invalido
    if ((itemID is '' or itemID is None) or (int(itemID) not in ids)):
        return redirect(url_for('catalog'))

    # mostrar item requisitado
    return ("Show item " + itemID)


@app.route("/create", methods=['GET', 'POST'])
@app.route("/create.html", methods=['GET', 'POST'])
# @login_required
def createItem():
    if request.method == 'POST':
        # criar novo item
        return "Create item"
    else:
        # direcionar para a pagina de criacao de item
        return "Page to create item"


@app.route("/edit", methods=['GET', 'POST'])
@app.route("/edit.html", methods=['GET', 'POST'])
# @login_required
def editItem():
    # checar argumento id
    itemID = request.args.get('id')

    # retornar ao catalog se o id for invalido
    if ((itemID is '' or itemID is None) or (int(itemID) not in ids)):
        return redirect(url_for('catalog'))

    if request.method == 'POST':
        # alterar informacoes do item
        return ("Update item" + itemID)
    else:
        # direcionar para a pagina de edicao de item
        return "Page to update item"


@app.route("/delete", methods=['POST'])
@app.route("/delete.html", methods=['POST'])
# @login_required
def deleteItem():
    # checar argumento id
    itemID = request.args.get('id')

    # retornar ao catalog se o id for invalido
    if ((itemID is '' or itemID is None) or (int(itemID) not in ids)):
        return redirect(url_for('catalog'))

    # deletar item
    return ("Delete item" + itemID)


#    ENDPOINTS JSON   #

# mostrar categorias e itens
@app.route("/catalog.json")
def catalogJSON():
    # retornar json com informacoes de todo o catalogo
    return jsonify({'message': 'Show all catalog categories and items'}), 200


# mostrar todas as categorias
@app.route("/categories.json")
def categoriesJSON():
    # retornar json com todas as categorias
    return jsonify({'message': 'Show categories'}), 200


# mostrar itens de uma categoria
@app.route("/category.json")
def categoryJSON():
    # checar argumento id
    category = request.args.get('name')

    # retornar erro 400(bad request) se a categoria for invalida
    if ((category is '' or category is None)
       or (category not in categoriesNames)):
        abort(400)

    # retornar json com todos os itens de uma categoria
    return jsonify({'message': 'Show category items'}), 200


# mostrar informacoes de um item especifico
@app.route("/item.json")
def itemJSON():
    # checar argumento id
    itemID = request.args.get('id')

    # retornar erro 400(bad request) se o id for invalido
    if ((itemID is '' or itemID is None) or (int(itemID) not in ids)):
        abort(400)

    # retornar json com as informacoes de um item especifico
    return jsonify({'message': 'Show item info'}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY')
        or hashlib.sha256(os.urandom(1024)).hexdigest()
    )
    app.debug = True
    app.run(host='0.0.0.0', port=port)
