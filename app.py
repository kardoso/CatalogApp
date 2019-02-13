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

    # TODO: Pagina

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

    # TODO: Pegar informações
    # TODO: Pagina

    # retornar ao catalog se o id for invalido
    if ((itemID is '' or itemID is None) or (int(itemID) not in ids)):
        return redirect(url_for('catalog'))

    # mostrar item requisitado
    return ("Show item " + itemID)


@app.route("/create", methods=['GET', 'POST'])
@app.route("/create.html", methods=['GET', 'POST'])
# @login_required
def createItem():
    # TODO: Criar item
    # TODO: Pagina
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

    # TODO: editar item
    # TODO: Pagina

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

    # TODO: excluir item
    # TODO: Pagina

    # retornar ao catalog se o id for invalido
    if ((itemID is '' or itemID is None) or (int(itemID) not in ids)):
        return redirect(url_for('catalog'))

    # deletar item
    return ("Delete item" + itemID)


#    ENDPOINTS JSON   #

# mostrar categorias e itens
@app.route("/catalog.json")
def catalogJSON():
    categories = session.query(Category).all()
    # salva categorias em um dicionario
    category_dict = [c.serialize for c in categories]
    for c in range(len(category_dict)):
        items = [i.serialize for i in session.query(Item)
                 .filter_by(category_id=category_dict[c]["id"]).all()]
        if items:
            # salva itens dentro do dicionario de categorias
            category_dict[c]["items"] = items
    return jsonify(categories=category_dict), 200


# mostrar todas as categorias
@app.route("/categories.json")
def categoriesJSON():
    # retornar json com todas as categorias
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories]), 200


# mostrar itens de uma categoria
@app.route("/category.json")
def categoryJSON():
    category_name = request.args.get('name')

    try:
        category = session.query(Category).filter_by(
            name=category_name.title()).one()
        items = session.query(Item).filter_by(category=category).all()
        return jsonify(items=[i.serialize for i in items]), 200
    except Exception as e:
        print('Error: '+str(e))
        abort(400)


# mostrar informacoes de um item especifico
@app.route("/item.json")
def itemJSON():
    # checar argumento id
    itemID = request.args.get('id')

    try:
        item = session.query(
            Item).filter_by(id=itemID.title()).first()
        # mostrar itens de acordo com a categoria requisitada
        return jsonify([item.serialize]), 200
    except Exception as e:
        print('Error: '+str(e))
        abort(400)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY')
        or hashlib.sha256(os.urandom(1024)).hexdigest()
    )
    app.debug = True
    app.run(host='0.0.0.0', port=port)
