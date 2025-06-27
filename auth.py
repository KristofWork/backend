from flask import Blueprint, request, render_template
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from user import User
from config import DATABASE_PATH
import sqlite3

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
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


@auth_bp.route("/login", methods=["GET", "POST"])
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


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return "Успешно разлогинились"
