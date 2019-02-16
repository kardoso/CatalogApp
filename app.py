# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import hashlib
# importar operações CRUD
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# importar classes do arquivo "database_setup"
from setupdb import User, Category, Item

from flask import Flask, request, redirect
from flask import render_template, url_for
from flask import jsonify, abort, make_response
import json

from flask import session as login_session
from flask_httpauth import HTTPBasicAuth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests

# selecionar banco de dados
engine = create_engine(
    'sqlite:///catalog.db',
    connect_args={'check_same_thread': False}
)
# estabelecer conexão
DBSession = sessionmaker(bind=engine)
session = DBSession()

auth = HTTPBasicAuth()

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


@app.route("/")
@app.route("/catalog")
@app.route("/catalog.html")
def catalog():
    logged=False
    state = ''
    if 'username' not in login_session:
        state = hashlib.sha256(os.urandom(1024)).hexdigest()
        login_session['state'] = state
        logged=False
    else:
        state = login_session['state']
        logged=True
    

    print(state)

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
                                items=items,
                                STATE=state,
                                logged=logged)
    except AttributeError:
        # TODO: mostrar apenas os 5 itens mais recentes
        # mostrar itens recentes
        items = session.query(Item).all()
        return render_template('catalog.html',
                                category_title="Latest items",
                                categories=categories,
                                items=items,
                                STATE=state,
                                logged=logged)


@app.route("/item")
@app.route("/item.html")
def showItem():
    logged=True
    isCreator=False
    if 'username' not in login_session:
        state = hashlib.sha256(os.urandom(1024)).hexdigest()
        login_session['state'] = state
        logged=False

    # checar argumento id
    itemID = request.args.get('id')

    # armazenar todos os itens por id
    list_of_id = [i.id for i in session.query(Item).all()]

    # retornar ao catalog se o id for invalido
    if ((itemID is '' or itemID is None) or (int(itemID) not in list_of_id)):
        return redirect(url_for('catalog'))

    item = session.query(Item).filter_by(id=itemID).first()

    if logged:
        print(login_session['email'])
        if 'email' in login_session:
            isCreator = item.user.email == login_session['email']

    # mostrar item requisitado
    return render_template('item.html',
                            item=item,
                            STATE=login_session['state'],
                            logged=logged,
                            isCreator=isCreator)


@app.route("/create", methods=['GET', 'POST'])
@app.route("/create.html", methods=['GET', 'POST'])
def createItem():
    logged=True
    if 'username' not in login_session:
        logged=False
        return redirect(url_for('catalog'))

    if request.method == 'POST':
        # criar novo item
        category_name = request.form["category"]
        category = session.query(Category).filter_by(name=category_name.title()).first()
        name = request.form["name"]
        description = request.form["description"]
        image = request.form["image"]

        if not image_exists(image):
            image = "http://www.vacationmexicobeach.com/images/no-image-available2.jpg"

        user = session.query(User).filter_by(email=login_session['email']).first()

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
        return render_template('create.html', categories=categories, logged=logged)


def image_exists(path):
    isImage = path.endswith(".png") or path.endswith(".jpg") or path.endswith("bmp") or path.endswith("gif")
    if isImage:
        result = requests.head(path)
        return result.status_code == 200
    else:
        return False


@app.route("/edit", methods=['GET', 'POST'])
@app.route("/edit.html", methods=['GET', 'POST'])
def editItem():
    logged=True
    if 'username' not in login_session:
        logged=False
        return redirect(url_for('catalog'))

    # checar argumento id
    itemID = request.args.get('id')

    # armazenar todos os itens por id
    list_of_id = [i.id for i in session.query(Item).all()]

    # retornar ao catalog se o id for invalido
    if ((itemID is '' or itemID is None) or (int(itemID) not in list_of_id)):
        return redirect(url_for('catalog'))

    categories = session.query(Category).all()

    if request.method == 'POST':
        # pegar itens do formulario
        category_name = request.form["category"]
        name = request.form["name"]
        description = request.form["description"]
        image = request.form["image"]

        item = session.query(Item).filter_by(id=itemID).first()
        
        # alterar informacoes do item
        item.category = session.query(Category).filter_by(name=category_name.title()).first()
        item.name = name
        item.description = description
        if image_exists(image):
            item.image = image
        session.add(item)
        session.commit()
        
        return redirect(url_for('showItem', id=item.id))
    else:
        item = session.query(Item).filter_by(id=itemID).first()
        # direcionar para a pagina de edicao de item
        return render_template('edit.html', categories=categories, item=item, logged=logged)


@app.route("/delete", methods=['POST'])
@app.route("/delete.html", methods=['POST'])
def deleteItem():
    #logged=True
    if 'username' not in login_session:
        #logged=False
        return redirect(url_for('catalog'))

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


#     Login, autorizacao e autenticacao     #

#Token antifraude
@app.route('/login')
@app.route('/login.html')
def showLogin():
    #state = ''.join(random.choice(string.ascii_uppercase + string.digits)
     #               for x in range(32))
    #login_session['state'] = state
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    login_session['state'] = state
    return render_template('login.html', STATE=state)
    #return "The current session state is %s" % login_session['state']


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        print('invalid state')
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        print('failed authorization')
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    #result = json.loads(h.request(url, 'GET')[1])
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    #data = answer.json()
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # check if user exists, if not create a new one
    if not getUserID(login_session['email']):
        login_session['user_id'] = createUser(login_session)

    #flash("You are now logged in as %s" % login_session['username'])
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(username=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['state']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY')
        or hashlib.sha256(os.urandom(1024)).hexdigest()
    )
    app.debug = True
    app.run(host='0.0.0.0', port=port)
