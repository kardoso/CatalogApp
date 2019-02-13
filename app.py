# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import hashlib
# importar operações CRUD
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# importar classes do arquivo "database_setup"
from setupdb import User, Category, Item

from flask import Flask, request, redirect, render_template, url_for, jsonify, abort

import json

app = Flask(__name__)

# selecionar banco de dados
engine = create_engine(
    'sqlite:///catalog.db',
    connect_args={'check_same_thread': False}
)
# estabelecer conexão
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
@app.route("/catalog")
@app.route("/catalog.html")
def catalog():
    # checar argumento category
    categoryName = request.args.get('category', '')

    categories = session.query(Category).all()

    try:
        category = session.query(
            Category).filter_by(name=categoryName.title()).first()
        items = session.query(
            Item).filter_by(category_id=category.id).all()
        # mostrar itens de acordo com a categoria requisitada
        return render_template('catalog.html',
                                category_title=category.name,
                                categories=categories,
                                items=items)
    except AttributeError:
        # TODO: mostrar apenas os 5 itens mais recentes
        # mostrar itens recentes
        items = session.query(Item).all()
        return render_template('catalog.html',
                                category_title="Latest items",
                                categories=categories,
                                items=items)


@app.route("/item")
@app.route("/item.html")
def showItem():
    # checar argumento id
    itemID = request.args.get('id')

    # armazenar todos os itens por id
    list_of_id = [i.id for i in session.query(Item).all()]

    # retornar ao catalog se o id for invalido
    if ((itemID is '' or itemID is None) or (int(itemID) not in list_of_id)):
        return redirect(url_for('catalog'))

    item = session.query(Item).filter_by(id=itemID).first()

    # mostrar item requisitado
    return render_template('item.html', item=item)


@app.route("/create", methods=['GET', 'POST'])
@app.route("/create.html", methods=['GET', 'POST'])
# @login_required
def createItem():
    if request.method == 'POST':
        # criar novo item
        category_name = request.form["category"]
        category = session.query(Category).filter_by(name=category_name.title()).first()
        name = request.form["name"]
        image = request.form["image"]
        description = request.form["description"]

        #teste
        user = session.query(User).first()

        item = Item(name=name,
             description=description,
             category=category,
             image=image,
             user=user)
        session.add(item)
        session.commit()

        # mostrar item criado
        return redirect(url_for('showItem', id=item.id))
    else:
        # direcionar para a pagina de criacao de item
        categories = session.query(Category).all()
        return render_template('create.html', categories=categories)


@app.route("/edit", methods=['GET', 'POST'])
@app.route("/edit.html", methods=['GET', 'POST'])
# @login_required
def editItem():
    # checar argumento id
    itemID = request.args.get('id')

    # armazenar todos os itens por id
    list_of_id = [i.id for i in session.query(Item).all()]

    # retornar ao catalog se o id for invalido
    if ((itemID is '' or itemID is None) or (int(itemID) not in list_of_id)):
        return redirect(url_for('catalog'))

    categories = session.query(Category).all()

    if request.method == 'POST':
        # alterar informacoes do item
        item = session.query(Item).filter_by(id=itemID).first()
        category_name = request.form["category"]
        item.category = session.query(Category).filter_by(name=category_name.title()).first()
        item.name = request.form["name"]
        item.image = request.form["image"]
        item.description = request.form["description"]
        session.add(item)
        session.commit()
        
        return redirect(url_for('showItem', id=item.id))
    else:
        item = session.query(Item).filter_by(id=itemID).first()
        # direcionar para a pagina de edicao de item
        return render_template('edit.html', categories=categories, item=item)


@app.route("/delete", methods=['POST'])
@app.route("/delete.html", methods=['POST'])
# @login_required
def deleteItem():
    # checar argumento id
    itemID = request.args.get('id')

    # armazenar todos os itens por id
    list_of_id = [i.id for i in session.query(Item).all()]

    # retornar ao catalog se o id for invalido
    if ((itemID is '' or itemID is None) or (int(itemID) not in list_of_id)):
        return redirect(url_for('catalog'))

    # deletar itemchemy.orm.query.Query' is not map
    item = session.query(Item).filter_by(id=itemID).first()
    session.delete(item)
    session.commit()

    return redirect(url_for('catalog'))


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
