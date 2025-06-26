import sqlite3
import os
from flask import Flask, render_template, request
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager(app)

DATABASE_PATH = os.getenv("DATABASE_PATH")

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


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    with sqlite3.connect(DATABASE_PATH) as db:
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE id=?", [user_id])
        user_row = cursor.fetchone()
    if user_row:
        return User(user_row[0])
    else:
        return None


@app.route("/game/<game>")
def game_info(game):
    with sqlite3.connect(DATABASE_PATH) as db:
        cursor = db.cursor()

        cursor.execute(
            "SELECT cover, title, price, raiting FROM games WHERE title = ?", [game]
        )
        result = cursor.fetchone()
    if not result:
        return "Игра не найдена!"
    return render_template("game.html", game=result)


@app.route("/new_game", methods=["GET", "POST"])
@login_required
def new_game():
    if request.method == "POST":
        form_data = request.form
        with sqlite3.connect(DATABASE_PATH) as db:
            cursor = db.cursor()
            cover = form_data["cover"]
            title = form_data["title"]
            price = form_data["price"]
            raiting = form_data["raiting"]

            cursor.execute(
                "INSERT INTO games(cover, title, price, raiting) VALUES(?, ?, ?, ?)",
                [cover, title, price, raiting],
            )
            db.commit()
        return "Новая игра добавилась!"
    return render_template("new_game.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form_data = request.form
        login = form_data["login"]
        password = form_data["password"]
        repeat_password = form_data["repeat-password"]

        if password != repeat_password:
            return "Пароли не совпали"

        password_hash = generate_password_hash(password)

        with sqlite3.connect(DATABASE_PATH) as db:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users(login, password_hash) VALUES(?, ?)",
                [login, password_hash],
            )
            db.commit()
        return "Зарегестрировались!"
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form_data = request.form
        login = form_data["login"]
        password = form_data["password"]
        with sqlite3.connect(DATABASE_PATH) as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT id, password_hash FROM users WHERE login = ?", [login]
            )
            result = cursor.fetchone()

        if not result:
            return "Такого пользователя не существует"

        id, password_hash = result

        if not check_password_hash(password_hash, password):
            return "Логин или пароль не верен!"

        login_user(User(id))
        return "Успешно залогировались!"
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Успешно разлогинились"


app.run()
