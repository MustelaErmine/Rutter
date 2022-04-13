from flask import make_response, request, Flask, redirect
from consts import *

import data.user, data.post


def init_views(app: Flask):
    init_user_actions(app)
    init_auth_actions(app)
    init_post_actions(app)
    init_following_actions(app)


def init_user_actions(app: Flask):
    @app.get('/')
    @app.get('/index')
    def index():
        return redirect('/home')

    @app.get('/home')
    @authorized
    def home():
        return '<h1>Добро пожаловать</h1>'

    @app.get('/enter')
    def enter():
        return 'enter'

    @app.get('/register')
    def new():
        return 'register new'


def init_auth_actions(app: Flask):
    pass


def init_post_actions(app: Flask):
    pass


def init_following_actions(app: Flask):
    pass