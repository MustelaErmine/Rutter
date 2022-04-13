from flask import make_response, request, Flask, redirect, render_template
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


def init_auth_actions(app: Flask):
    @app.get('/enter')
    def enter():
        return render_template('enter.html')

    @app.get('/register')
    def new():
        return 'register new'

    @app.get('/logout')
    @authorized
    def logout():
        del session['username']
        session['authorized'] = False
        return redirect('/')


def init_post_actions(app: Flask):
    @app.get('/home')
    @authorized
    def home():
        user = data.user.User(session['username'])
        return render_template('news.html', title=f"news : rutter", username=user.username)



def init_following_actions(app: Flask):
    pass