from flask import Blueprint, request, render_template
from flask_login import login_required
from config import DATABASE_PATH
import sqlite3


games_bp = Blueprint("games", __name__)


@games_bp.route("/game/<game>")
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


@games_bp.route("/new_game", methods=["GET", "POST"])
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
