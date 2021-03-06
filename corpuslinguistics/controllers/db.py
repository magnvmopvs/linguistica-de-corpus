# -*- coding: utf-8 -*-
from bottle import Bottle, jinja2_view, post, request
from wtforms import StringField, PasswordField, Form, fields, SubmitField
from ..models.base import Base
from hashlib import sha512

# -------------- Controle das views de concordancia
cl_db = Bottle(True)

"""
### --------------  Form Cadastro -------------- ###
"""
class Cadastro(Form):
    username = StringField('Username')
    email = StringField('Email')
    password = PasswordField('Password')
    butt = SubmitField('OK!')

"""
### --------------  Páginas Administrativas -------------- ###
"""

# -------------- Página: Cadastro
@cl_db.route('/cadastro')
@jinja2_view('adm/cadastro.html')
def cadastro():
    return dict(title = 'Cadastro', form = Cadastro())

# -------------- Insere: Cadastro
@cl_db.post('/cadastro')
#@jinja2_view()
def cadastro():
    db = Base()
    form = Cadastro(request.POST)   # ----- POST METHOD
    name = form.username.data
    email = form.email.data
    password = form.password.data
    password = sha512(password.encode()) # ----- Hashed password

    try:
        assert name!= ''
        assert email != '' and "@" in email
        db.inserir_dados(name,email, password.hexdigest())
        db.commit()
        return "ok"
    except:
        return "error"

"""
### --------------  Pagina de visualização dos dados do banco   -------------- ###
"""
@cl_db.route('/base')
@jinja2_view('adm/base.html')
def base():
    try:
        db = Base()
        data = db.busca()
        assert data[0]
        return dict(rows=data)
    except:
        return "ERROR"
