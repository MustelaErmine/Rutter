from consts import *
from data.dbwork import *

import os
import sqlite3

from flask import Flask, render_template
from data.user import User
from data.post import Post


def main():
    log('Initializing...')
    log('Path:', DIRNAME)

    if not init_db():
        log('Not started')
        return

    log('Started successful!')

    testing()


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


main()