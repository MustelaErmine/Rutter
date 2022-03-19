import sqlite3
from consts import *

DBPATH = DIRNAME + '\\db\\rutter.db'
db_init_commands = """CREATE TABLE users (
    username        VARCHAR (16)  NOT NULL PRIMARY KEY,
    hashed_password VARCHAR (40)  NOT NULL,
    bio             VARCHAR (255),
    joined          DATETIME      NOT NULL DEFAULT (datetime()));
    CREATE TABLE posts (
    id      INTEGER       PRIMARY KEY NOT NULL,
    author  VARCHAR (16)  REFERENCES users (username) ON DELETE CASCADE NOT NULL,
    replied INTEGER       DEFAULT NULL,
    text    VARCHAR (255) NOT NULL,
    date    DATETIME      NOT NULL DEFAULT (datetime()));
    CREATE TABLE followships (
    who  VARCHAR (16) REFERENCES users (username) ON DELETE CASCADE NOT NULL,
    whom VARCHAR (16) NOT NULL REFERENCES users (username) ON DELETE CASCADE);"""


def connect_db():
    return sqlite3.connect(DBPATH)


def execute_db(script):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.executescript(script)
    except sqlite3.Error as exception:
        log('DB Error:', exception)
        connection.close()
        return False

    connection.close()
    return True


def get_db(script):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(script)
        data = cursor.fetchall()
        connection.close()
        return data
    except sqlite3.Error as exception:
        log('DB Error:', exception)
        connection.close()
        return None