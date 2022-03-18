from data.user import *
from data.dbwork import *


class Post:
    def __init__(self, id):
        self.id = id
        self.author = 'TODO' # User object
        self.text = 'TODO' # string
        self.replied_to = 'TODO' # Post object or NoneType
        self.date = 'TODO' # DateTime object

    def __repr__(self):
        return f'{self.author.username}: "{(self.text[:20] + "...") if len(self.text) > 25 else self.text}"'
