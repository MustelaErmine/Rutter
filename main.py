from consts import *
from data.dbwork import *
from data.user import User
from data.post import Post

import os
import sqlite3
from flask import Flask, render_template, send_from_directory

app: Flask = None


def main():
    global app
    log('Initializing...')
    log('Path:', DIRNAME)
    if not init_db():
        log('Not started')
        return

    app = Flask(__name__)
    app.config['SECRET_KEY'] = '209cfj8238c903q'
    from api import rest, views
    rest.init_api(app)
    views.init_views(app)

    log('Started successful!')
    app.run()


def init_db():
    if os.path.exists(DBPATH):
        return True
    return execute_db(db_init_commands)


def testing():
    user = User('ermine_scout')
    user.get_info()
    posts = user.get_posts()
    for post in posts:
        post.get_info()
    print(posts)


@app.route('/static/<path:path>')
def send_report(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    main()