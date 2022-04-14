import data.user as u
from data.dbwork import *


class Post:
    def __init__(self, id):
        self.id = id
        self.author = self.text = 'undefined'
        self.replied = 1
        self.replies = []
        self.date = datetime.datetime.fromtimestamp(0)

    def get_info(self):
        post = get_db(f'SELECT * FROM posts WHERE id="{self.id}"')
        if not post or len(post) < 1:
            log(f"Error: post id#{self.id} not found")
            return False

        post = post[0]
        self.author = u.User(post[1])
        self.replied = None if post[2] is None else Post(post[2])
        self.text = post[3]
        self.date = datetime.datetime.strptime(post[4], "%Y-%m-%d %H:%M:%S")
        replies = get_db(f'SELECT id FROM posts WHERE replied="{self.id}"')
        self.replies = [Post(i[0]) for i in replies]
        return True

    def delete(self):
        result = execute_db(f"""DELETE FROM posts WHERE id={self.id}""")
        return result

    def __repr__(self):
        return f'{"u@0" if self.author == "undefined" else "@" + self.author.username}: ' + \
               f'"{(self.text[:20] + "...") if len(self.text) > 25 else self.text}"'