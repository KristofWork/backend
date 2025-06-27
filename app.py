import sqlite3
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from auth import auth_bp
from games import games_bp
from config import SECRET_KEY, DATABASE_PATH
from user import load_user

load_dotenv()

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.register_blueprint(auth_bp)
app.register_blueprint(games_bp)

login_manager = LoginManager(app)
login_manager.user_loader(load_user)


def init_db():
    with sqlite3.connect(DATABASE_PATH) as db:
        cursor = db.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE,
            password_hash TEXT)""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS games(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cover TEXT,
            title TEXT,
            price REAL,
            raiting REAL)
        """)

        db.commit()


init_db()

app.run()
