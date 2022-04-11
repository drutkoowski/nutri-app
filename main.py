from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json

import dbmodels
from dbmodels import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import SignUp, Login



app = Flask(__name__)
app.config['SECRET_KEY'] = "saj21#12da!s321@das*(aas$as6"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nutridatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
API_KEY = "6ef17d9385fb15dc61e51ebb0047ec39"
APP_ID = "9a3526fc"
API_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/nutrients"

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
params = {
    "query": "3oz Apple",
    "x-remote-user-id": "0",
}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    # calorie_eaten_json = json.dumps(calorie_eaten, indent=4)
    # calorie_burnt_json = json.dumps(calorie_burnt,indent=4)

    return render_template("index.html")




@app.route("/signup", methods=["GET", "POST"])
def signup():
    signup = SignUp()
    if request.method == "POST" and signup.validate_on_submit():
        email_data = request.form.get("email")
        password_data = request.form.get("password")
        name_data = request.form.get("name")
        age_data = request.form.get("age")
        gender_data = request.form.get("gender")
        height_data = request.form.get("height")
        weight_data = request.form.get("weight")
        user = User.query.filter_by(email=email_data).first()
        is_name = User.query.filter_by(name=name_data).first()
        if user or is_name:
            flash(f'User with these credentials already exists!', category="info")
            return render_template("signup.html", form=signup)
        else:
            hash_and_salted_password = generate_password_hash(
                password_data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = User(
                email=email_data,
                password=hash_and_salted_password,
                name=name_data,
                age=age_data,
                gender=gender_data,
                height=height_data,
                weight=weight_data,
            )
            flash(f'Welcome in Nutri {name_data}', category="info")
            dbmodels.adduser(new_user)
            login_user(new_user)
        return redirect(url_for('home'))
    return render_template("signup.html", form=signup)

@app.route("/login", methods=["GET","POST"])
def login():
    login = Login()
    if request.method == "POST" and login.validate_on_submit():
        email_data = request.form.get("email")
        password_data = request.form.get("password")
        user = User.query.filter_by(email=email_data).first()
        user_exists = False
        if user is None:
            user_exists = False
        elif user is not None:
            user_exists = True
        if user_exists:
            is_password_right = check_password_hash(user.password, password_data)
            if is_password_right:
                flash(f'Welcome again {user.name}!', category="info")
                login_user(user)
                return redirect(url_for('home'))
            elif not is_password_right:
                flash(f'Provided credentials are not matching any account!', category="warning")
                return render_template("login.html", form=login)
        elif not user_exists:
            flash(f'Provided credentials are not matching any account!', category="warning")
            return render_template("login.html", form=login)

    return render_template("login.html", form=login)


@app.route("/logout")
def logout():
    flash(f'You logged out successfully!', category="warning")
    logout_user()
    return redirect(url_for('home'))
# response = requests.get(API_ENDPOINT, headers=headers,params=params)
# data = response.json()
# print(data)

if __name__ == '__main__':
    app.run(debug=True)
