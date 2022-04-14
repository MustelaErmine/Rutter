import json

from flask import make_response, request, Flask, jsonify
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


def init_api(app: Flask):
    init_user_actions(app)
    init_post_actions(app)
    init_following_actions(app)


def init_user_actions(app: Flask):
    @app.get('/api/user/info/<string:username>')
    @authorized
    def get_user(username):
        user = data.user.User(username)
        if not user.get_info():
            response = make_response()
            response.status_code = 404
            return response
        response = make_response({'username': user.username, 'bio': user.bio, 'joined': str(user.joined)})
        response.status_code = 200
        return response

    @app.put('/api/user/bio')
    @authorized
    def put_bio():
        user = data.user.User(session['username'])
        if user.change_bio(request.data):
            return ok()
        return internal_error()

    @app.delete('/api/user')
    @authorized
    def delete_user():
        user = data.user.User(session['username'])
        if user.delete():
            return ok()
        return internal_error()

    @app.post('/api/user/login')
    def login():
        try:
            js = json.loads(request.data)
        except Exception as exception:
            res = make_response('Bad syntax')
            res.status_code = 400
            return res
        if not js:
            res = make_response('Bad syntax')
            res.status_code = 400
            return res
        if js.get('username', None) is None or js.get('password', None) is None:
            res = make_response('No username or password')
            res.status_code = 400
            return res
        username, password = js['username'], js['password']
        user = data.user.User(username)
        if not user.check_password(password):
            res = make_response('Wrong password')
            res.status_code = 401
            return res
        session['username'] = username
        session['authorized'] = True

        return ok()

    @app.post('/api/user/register')
    def register():
        try:
            js = json.loads(request.data)
        except Exception as exception:
            res = make_response('Bad syntax')
            res.status_code = 400
            return res
        if not js:
            res = make_response('Bad syntax')
            res.status_code = 400
            return res
        if js.get('username', None) is None or js.get('password', None) is None or js.get('password2', None) is None:
            res = make_response('No username or password or password2')
            res.status_code = 400
            return res
        if js['password'] != js['password2']:
            res = make_response('Passwords not similar')
            res.status_code = 400
            return res

        username, password = js['username'], js['password']
        result = data.user.User.register(username, password)
        if result == 'exist':
            res = make_response('User already exist')
            res.status_code = 400
            return res
        elif result:
            return ok()
        return internal_error()


def init_post_actions(app: Flask):
    @app.post('/api/post')
    @authorized
    def add_post():
        try:
            js = json.loads(request.data)
        except Exception as exception:
            res = make_response('Bad syntax')
            res.status_code = 400
            return res
        if not js:
            res = make_response('Bad syntax')
            res.status_code = 400
            return res
        user = data.user.User(session['username'])
        if js.get('reply') is not None:
            if user.reply(data.post.Post(js['reply']), js['text']):
                return ok()
            else:
                return internal_error
        else:
            if user.add_post(js['text']):
                return ok()
            else:
                return internal_error

    @app.get('/api/posts/<user_id>/<int:offset>')
    @authorized
    def get_posts_list(user_id, offset):
        user = data.user.User(user_id)
        posts = user.get_posts(offset)
        return jsonify({'posts': [p.id for p in posts]})

    @app.get('/api/posts/news/<int:offset>')
    @authorized
    def get_news_list(offset):
        user = data.user.User(session['username'])
        posts = user.get_news(offset)
        return jsonify({'posts': [p.id for p in posts]})

    @app.get('/api/post/<post_id>')
    @authorized
    def get_post(post_id):
        p = data.post.Post(post_id)
        p.get_info()
        return jsonify({'date': p.date, 'text': p.text, 'author': p.author, 'replied': p.replied})


def init_following_actions(app: Flask):
    @app.put('/api/follow/<user_id>')
    @authorized
    def follow(user_id):
        user = data.user.User(session['username'])
        if user.follow(user_id):
            return ok()
        else:
            return internal_error()

    @app.delete('/api/follow/<user_id>')
    @authorized
    def unfollow(user_id):
        user = data.user.User(session['username'])
        if user.unfollow(user_id):
            return ok()
        else:
            return internal_error()

    @app.get('/api/followers')
    @authorized
    def get_followers():
        user = data.user.User(session['username'])
        followers = user.get_followers()
        return [u.id for u in followers]

    @app.get('/api/followings')
    @authorized
    def get_following():
        user = data.user.User(session['username'])
        followings = user.get_following()
        return [u.id for u in followings]