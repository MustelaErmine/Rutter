from consts import *
from data.dbwork import *

import os
import sqlite3

from flask import Flask, render_template
from data.user import *
from data.post import *


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
    print(user)
    print(user.get_followers())
    print(user.get_following())


main()