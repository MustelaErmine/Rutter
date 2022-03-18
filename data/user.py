from data.post import *
from data.dbwork import *


class User:
    def __init__(self, username):
        self.username = username
        self.bio = 'undefined'

    def __repr__(self):
        return f'u@{self.username}'

    def get_info(self):
        user = get_db(f'SELECT bio, joined FROM users WHERE username="{self.username}"')
        if user and len(user) < 1:
            log(f"Error: user @{self.username} not found")
            return
        user = user[0]
        #print(user)
        self.bio = user[0]
        self.joined = user[1]

    def get_news(self):
        pass

    def get_followers(self):
        followings = get_db(f'SELECT who FROM followships WHERE whom="{self.username}"')
        return [User(user[0]) for user in followings]

    def get_following(self):
        followings = get_db(f'SELECT whom FROM followships WHERE who="{self.username}"')
        return [User(user[0]) for user in followings]