import os
import datetime
import hashlib

from flask import request, session, make_response, redirect

DIRNAME = os.path.dirname(os.path.abspath(__file__))
news_piece = 10


def log(*args, sep=' '):
    dt = datetime.datetime.now()
    print(f'[{dt.strftime("%H:%M:%S %d %b %Y")}] {sep.join(str(arg) for arg in args)}')


def authorized(function):
    def decorated(*args, **kwargs):
        if 'authorized' not in session or not session['authorized']:
            return redirect('/enter')
        return function(*args, **kwargs)

    decorated.__name__ = function.__name__
    return decorated


def encode_password(password):
    return hashlib.md5((password + '@').encode('utf-8')).hexdigest()