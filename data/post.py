import data.user as u
from data.dbwork import *


class Post:
    def __init__(self, id):
        self.id = id
        self.author = self.replied = self.text = self.date = 'undefined'

    def get_info(self):
        post = get_db(f'SELECT * FROM posts WHERE id="{self.id}"')
        if not post or len(post) < 1:
            log(f"Error: post id#{id} not found")
            return

        post = post[0]
        self.author = u.User(post[1])
        self.replied = None if post[2] is None else Post(post[2])
        self.text = post[3]
        self.date = datetime.datetime.strptime(post[4], "%Y-%m-%d %H:%M:%S")

    def delete(self):
        result = execute_db(f"""DELETE FROM posts WHERE id={self.id}""")
        return result

    def __repr__(self):
        return f'{"u@0" if self.author == "undefined" else "@" + self.author.username}: ' + \
               f'"{(self.text[:20] + "...") if len(self.text) > 25 else self.text}"'