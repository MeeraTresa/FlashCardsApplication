from flask import (Flask, render_template, abort,
                   request, redirect, url_for, g, flash)
from model import db, save_db
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField


class NewCardForm(FlaskForm):
    question = StringField("Question")
    answer = TextAreaField("Answer")
    submit = SubmitField("Create")


app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"


@app.route("/")
def welcome():
    c = get_cursor()
    cards_from_db = c.execute("SELECT c.question, c.answer FROM cards as c")
    items = []
    for row in cards_from_db:
        item = {
            "question": row[0],
            "answer": row[1]
        }
        items.append(item)
    return render_template("welcome.html", cards=items)


@app.route("/card/<int:index>")
def card_view(index):
    c = get_cursor()
    cards_from_db = c.execute("SELECT c.question, c.answer FROM cards as c")
    items = []
    for row in cards_from_db:
        item = {
            "question": row[0],
            "answer": row[1]
        }
        items.append(item)
    try:
        card = items[index]
        return render_template("card.html", card=card, index=index, max_index=len(items)-1)
    except IndexError:
        abort(404)


@app.route("/add_card", methods=["GET", "POST"])
def add_card():
    c = get_cursor()
    cards_from_db = c.execute("SELECT c.question, c.answer FROM cards as c")
    items = []
    for row in cards_from_db:
        item = {
            "question": row[0],
            "answer": row[1]
        }
        items.append(item)
    form = NewCardForm()
    if request.method == "POST":
        # form has been submitted, process data

        card = {"question": form.question.data,
                "answer": form.answer.data}
        db.append(card)
        save_db()
        c.execute("INSERT INTO cards (question,answer) VALUES (?,?)",
                  (form.question.data, form.answer.data))
        get_db().commit()
        print("commited")
        flash("The Flashcard was successfully saved", "success")
        return redirect(url_for('card_view', index=len(items)))
    else:
        return render_template("add_card.html", form=form)


@app.route("/remove_card/<int:index>", methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method == "POST":
            del db[index]
            save_db()
            return redirect(url_for('welcome'))
        else:
            return render_template("remove_card.html", card=db[index])
    except:
        IndexError: abort(404)
    return redirect(url_for('welcome'))

# Database integration


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("db/quizwiz.db")
    return db


def get_cursor():
    connection = get_db()
    c = connection.cursor()
    return c


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# Adding REST API endpoints


@app.route("/api/card/")
def api_card_list():
    return db


@app.route("/api/card/<int:index>")
def api_card_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)
