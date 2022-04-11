from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json

import dbmodels
from dbmodels import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import SignUp, Login, AddExercise, ProfileInfo, AddMeal

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
API_ENDPOINT_MEALS = "https://trackapi.nutritionix.com/v2/natural/nutrients"
API_ENDPOINT_EXERCISE = "https://trackapi.nutritionix.com/v2/natural/exercise"
query = ""

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

params = {
    "query": query,
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

        if user:
            flash(f'User with these credentials already exists!', category="warning")
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


@app.route("/login", methods=["GET", "POST"])
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
    flash(f'You logged out successfully!', category="info")
    logout_user()
    return redirect(url_for('home'))


@app.route("/profile")
@login_required
def profile():
    return render_template("profilepage.html")


@app.route("/profile/exercises")
@login_required
def exercises():
    return render_template("exercises.html")


@app.route("/profile/exercises/add", methods=["GET","POST"])
@login_required
def add_exercises():
    add_exercises = AddExercise()
    if request.method == "POST":
        exercise_query = add_exercises.exercise_query.data
        exercise_duration = add_exercises.exercise_duration.data
        gender = current_user.gender
        weight = current_user.weight
        height = current_user.height
        age = current_user.age
        headers_exercise = {
            "x-app-id": APP_ID,
            "x-app-key": API_KEY,
            "Content-Type": 'application/json',
        }
        params_exercise = {
            "query": exercise_query,
            "gender": gender,
            "weight_kg": weight,
            "height_cm": height,
            "age": age,
        }
        json_object = json.dumps(params_exercise, indent=4)
        response = requests.post(API_ENDPOINT_EXERCISE, headers=headers_exercise, data=json_object)
        data = response.json()
        print(data)
    return render_template("add_exercise.html", form=add_exercises)


@app.route("/profile/exercises/show")
@login_required
def show_exercises():
    return render_template("show_exercise.html")


@app.route("/profile/info")
@login_required
def profile_info():
    profileInfo = ProfileInfo()
    return render_template("profile_info.html", form=profileInfo)


@app.route("/profile/meals")
@login_required
def meals():
    return render_template("meals.html")


@app.route("/profile/meals/add")
@login_required
def add_meal():
    meal_form = AddMeal()
    return render_template("add_meal.html", form=meal_form)


@app.route("/profile/meals/show")
@login_required
def show_meals():
    return render_template("show_meal.html")




if __name__ == '__main__':
    app.run(debug=True)
