import sqlite3
from flask_login import UserMixin
from config import DATABASE_PATH


class User(UserMixin):
    def __init__(self, id):
        self.id = id


def load_user(user_id):
    with sqlite3.connect(DATABASE_PATH) as db:
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE id=?", [user_id])
        user_row = cursor.fetchone()
    if user_row:
        return User(user_row[0])
    else:
        return None
