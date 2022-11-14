import os
from flask import (Flask, render_template, abort,
                   request, redirect, url_for, g, flash)
from model import db
import sqlite3
from forms.RegistrationForm import RegistrationForm
from forms.LoginForm import LoginForm
from forms.NewCardForm import NewCardForm
from sqla import sqla
from models.cards import Card
from models.user import User
#from login import login_manager


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" +  os.path.join(basedir,'quizwiz.sqlite')
sqla.init_app(app)
#login_manager.init_app(app)

@app.before_first_request
def create_tables():
    sqla.create_all()

@app.route("/")
def welcome():    
    cards_using_sqla = sqla.session.execute(sqla.select(Card).order_by(Card.question)).scalars()
    return render_template("welcome.html", cards=cards_using_sqla)


@app.route("/card/<int:id>")
def card_view(id): 
    #Using SQLA
    card_from_sqla = sqla.get_or_404(Card,id)
    next_card = sqla.session.query(Card).order_by(Card.id.desc()).filter(Card.id<card_from_sqla.id).first()       
    if next_card is not None:
        next_card_available = True
        next_card_id = next_card.id
    else:
        next_card_available = False
        next_card_id = sqla.session.query(Card).order_by(Card.id.desc()).first().id
    return render_template("card.html", card=card_from_sqla,index = card_from_sqla.id, next_card_id = next_card_id,
                            next_card_available = next_card_available )


@app.route("/register", methods=["GET", "POST"])
def register_user():
    #c = get_cursor()
    form = RegistrationForm()
    if form.validate_on_submit():
        user_for_sqla = User(username = form.username.data,email = form.email.data,password    = form.password.data,
                             location    = form.location.data,description = form.description.data )       
        sqla.session.add(user_for_sqla)
        sqla.session.commit()
        print("card saved" + str(user_for_sqla.id))  
        flash("You are registered", "success")
        return redirect(url_for("welcome"))

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        error = None
        if user is None:
            error = "Incorrect username."
        elif not user.check_password(password):
            error = "Incorrect password."
        if error is None:
            flash("You are successfully logged in.", "success")
            return redirect(url_for("welcome"))
        flash(error,"warning")
    return render_template("login.html", form=form)


@app.route("/add_card", methods=["GET", "POST"])
def add_card():
    form = NewCardForm()
    if request.method == "POST":
        # form has been submitted, process data
        try:
            card_for_sqla = Card(question = form.question.data, answer= form.answer.data )
            sqla.session.add(card_for_sqla)
            sqla.session.commit()
            print("card saved" + str(card_for_sqla.id))
            return redirect(url_for('card_view', id=card_for_sqla.id))
        except ValueError as e:
            flash(str(e),"error")
            return redirect(url_for('welcome'))
    else:
        return render_template("add_card.html", form=form)


@app.route("/remove_card/<int:index>", methods=["GET", "POST"])
def remove_card(index):
    card_from_sqla = sqla.get_or_404(Card,index)
    
    if request.method == "POST":            
        sqla.session.delete(card_from_sqla)
        sqla.session.commit()
        return redirect(url_for('welcome'))
    else:            
        return render_template("remove_card.html", card=card_from_sqla)


# Database integration --- No longer needed


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
