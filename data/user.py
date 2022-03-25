from consts import *

import data.post as p
from data.dbwork import *


class User:
    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return f'u@{self.username}'

    @staticmethod
    def register(username, password):
        result = get_db(f"""SELECT username FROM users WHERE username="{username}" """)
        if len(result) > 0:
            return 'exist'
        result = execute_db(f"""INSERT INTO users(username, hashed_password)
                                VALUES ("{username}", "{encode_password(password)}")""")
        return result

    def get_info(self):
        user = get_db(f"""SELECT bio, joined FROM users WHERE username="{self.username}" """)
        if not user or len(user) < 1:
            log(f"Error: user @{self.username} not found")
            return False
        user = user[0]
        #print(user)
        self.bio = user[0]
        self.joined = datetime.datetime.strptime(user[1], "%Y-%m-%d %H:%M:%S")
        return True

    def change_bio(self, new_bio):
        result = execute_db(f"""UPDATE users SET bio={new_bio} 
                                WHERE username="{self.username}" """)
        return result

    def get_posts(self, offset=0):
        posts = get_db(f"""SELECT id FROM posts 
                           WHERE replied IS NULL AND author="{self.username}" 
                           ORDER BY date DESC LIMIT {news_piece} OFFSET {offset}""")
        return [p.Post(post[0]) for post in posts]

    def add_post(self, text):
        result = execute_db(f"""INSERT INTO posts(author, text)
                                VALUES ("{self.username}", "{text}")""")
        return result

    def reply(self, to, text):
        result = execute_db(f"""INSERT INTO posts(author, text, replied)
                                VALUES ("{self.username}", "{text}", {to.id})""")
        return result

    def get_news(self, offset=0):
        news = get_db(f"""SELECT id FROM posts 
                          WHERE replied IS NULL AND author IN 
                          (SELECT whom FROM followships WHERE who="{self.username}")
                          ORDER BY date DESC LIMIT {news_piece} OFFSET {offset}""")
        return [p.Post(post[0]) for post in news]

    def get_followers(self):
        followers = get_db(f'SELECT who FROM followships WHERE whom="{self.username}"')
        return [User(user[0]) for user in followers]

    def get_following(self):
        followings = get_db(f'SELECT whom FROM followships WHERE who="{self.username}"')
        return [User(user[0]) for user in followings]

    def unfollow(self, user):
        result = execute_db(f"""DELETE FROM followships 
                                WHERE who={self.username} AND whom={user.username}""")
        return result

    def delete(self):
        result = execute_db(f"""DELETE FROM users WHERE username={self.username}""")
        return result

    def check_password(self, password):
        real = get_db(f"""SELECT hashed_password FROM users
                          WHERE username="{self.username}" """)
        return len(real) > 0 and len(real[0]) > 0 and real[0][0] == encode_password(password)
