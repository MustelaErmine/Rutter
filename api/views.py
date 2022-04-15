from flask import make_response, request, Flask, redirect, render_template
from consts import *

import data.user, data.post


def internal_error():
    res = make_response('Internal server error. Please, text to developer.')
    res.status_code = 500
    return res


def ok():
    res = make_response()
    res.status_code = 200
    return res


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
        return render_template('register.html')

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
        return render_template('news.html', username=user.username, path='/', title='news : rutter')

    @app.get('/post-card/<post_id>')
    @authorized
    def post_card(post_id):
        user = data.user.User(session['username'])
        post = data.post.Post(post_id)
        if not post.get_info():
            res = make_response('Page does not exist')
            res.status_code = 404
            return res
        return render_template('post-card.html', idn=post_id, replies=len(post.replies), text=post.text,
                               author=post.author.username, date=post.date.strftime("%H:%M:%S %d %b %Y"))

    @app.get('/post/<post_id>')
    @authorized
    def post_view(post_id):
        user = data.user.User(session['username'])
        post = data.post.Post(post_id)
        if not post.get_info():
            res = make_response('Page does not exist')
            res.status_code = 404
            return res
        return render_template('post.html', post_id=post_id, username=user.username, path='/post/' + post_id,
                               title='post ' + str(post_id) + ' : rutter')

    @app.get('/<user_id>')
    @authorized
    def user_page(user_id):
        user = data.user.User(session['username'])
        tuser = data.user.User(user_id)
        if not tuser.get_info():
            res = make_response('Page does not exist')
            res.status_code = 404
            return res
        return render_template('user_page.html', tusername=user_id, path='/' + user_id,
                               title=str(user_id) + ' : rutter', joined=tuser.joined.strftime("%H:%M:%S %d %b %Y"),
                               bio=tuser.bio, edit=user.username == tuser.username, username=user.username)


def init_following_actions(app: Flask):
    pass
