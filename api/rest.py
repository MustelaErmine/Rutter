from flask import make_response, request, Flask
from consts import *

import data.user, data.post

internal_error = make_response('Internal server error. Please, text to developer.')
internal_error.status_code = 500
ok = make_response()
ok.status_code = 200


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
            return redirect('/')
        return internal_error

    @app.delete('/api/user')
    @authorized
    def delete_user():
        user = data.user.User(session['username'])
        if user.delete():
            return redirect('/')
        return internal_error

    @app.get('/api/user/logout')
    @authorized
    def logout():
        del session['username']
        session['authorized'] = False
        return ok

    @app.post('/api/user/login')
    def login():
        try:
            form = request.form
        except Exception as exception:
            res = make_response('Bad syntax')
            res.status_code = 400
            return res
        if 'username' not in form or 'password' not in form:
            res = make_response('No username or password')
            res.status_code = 400
            return res

        username, password = form['username'], form['password']
        user = data.user.User(username)
        if not user.check_password(password):
            res = make_response('Wrong password')
            res.status_code = 401
            return res
        session['username'] = username
        session['authorized'] = True

        return ok

    @app.post('/api/user/register')
    def register():
        try:
            form = request.form
        except Exception as exception:
            res = make_response('Bad syntax')
            res.status_code = 400
            return res
        if 'username' not in form or 'password' not in form or 'password2' not in form:
            res = make_response('No username or password or password2')
            res.status_code = 400
            return res
        if form['password'] != form['password2']:
            res = make_response('Passwords not similar')
            res.status_code = 400
            return res

        username, password = form['username'], form['password']
        result = data.user.User.register(username, password)
        if result == 'exist':
            res = make_response('User already exist')
            res.status_code = 400
            return res
        elif result:
            return redirect('/enter')
        return internal_error


def init_post_actions(app: Flask):
    # @app.post('/api/')
    pass


def init_following_actions(app: Flask):
    pass