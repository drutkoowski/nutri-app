from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = "saj21#12da!s321@das*(aas$as6"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nutridatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    activity_level = db.Column(db.Integer)
    exercises = db.relationship('Exercise', backref="user")
    meals = db.relationship('Meal', backref="user")
    reviews = db.relationship('Review', backref="user")


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    duration = db.Column(db.Integer)
    calories_burnt = db.Column(db.Integer)
    date = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String)
    overall_rate = db.Column(db.Integer)
    simplicity_rate = db.Column(db.Integer)
    features_rate = db.Column(db.Integer)
    date = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    calories = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    saturated_fat = db.Column(db.Integer)
    cholesterol = db.Column(db.Integer)
    sodium = db.Column(db.Integer)
    total_carbohydrate = db.Column(db.Integer)
    dietary_fiber = db.Column(db.Integer)
    sugars = db.Column(db.Integer)
    nf_protein = db.Column(db.Integer)
    nf_potassium = db.Column(db.Integer)
    date = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


db.create_all()


def create_tables():
    db.create_all()


def add_to_datebase(value):
    db.session.add(value)
    db.session.commit()
