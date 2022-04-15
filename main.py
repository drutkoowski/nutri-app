from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json
from datetime import datetime
import dbmodels
from dbmodels import User, Exercise, Meal
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import SignUp, Login, AddExercise, AddMeal, EditForm

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


def calc_bmr(user):
    if user.gender == "female":
        BMR = 655.1 + (9.563 * user.weight) + (1.850 * user.height) - (4.676 * user.age)
        return BMR
    elif user.gender == "male":
        BMR = 66.47 + (13.75 * user.weight) + (5.003 * user.height) - (6.755 * user.age)
        return BMR


def calc_amr(BMR, activity_level):
    if activity_level == 0:
        AMR = BMR * 1.2
        return AMR
    elif activity_level == 1:
        AMR = BMR * 1.375
        return AMR
    elif activity_level == 2:
        AMR = BMR * 1.55
        return AMR
    elif activity_level == 3:
        AMR = BMR * 1.725
        return AMR
    elif activity_level == 4:
        AMR = BMR * 1.9
        return AMR


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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    signup = SignUp()
    if request.method == "POST" and signup.validate_on_submit():
        email_data = request.form.get("email")
        password_data = request.form.get("password")
        name_data = request.form.get("name")
        age_data = request.form.get("age")
        gender_data = request.form.get("gender")
        height_data = request.form.get("height")
        weight_data = request.form.get("weight")
        activity_level = request.form.get("activity_level")
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
                activity_level=activity_level,
            )
            flash(f'Welcome in Nutri {name_data}', category="info")
            dbmodels.add_to_datebase(new_user)
            login_user(new_user)
        return redirect(url_for('home'))
    return render_template("signup.html", form=signup)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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


@app.route("/profile/exercises/add", methods=["GET", "POST"])
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
        calorie_summary = 0
        now = datetime.now()
        date_now = now.strftime("%Y/%m/%d")
        exercises_name = ''
        for exercise in data["exercises"]:
            calorie_summary = exercise['nf_calories'] + calorie_summary
            exercises_name = exercises_name + exercise['name'].title() + ", "
        exercises_name_fixed = exercises_name[:-2]
        exercise = Exercise(name=exercises_name_fixed, duration=exercise_duration, date=date_now,
                            calories_burnt=round(calorie_summary), user_id=current_user.id)
        dbmodels.add_to_datebase(exercise)

        return redirect(url_for('exercises'))
    return render_template("add_exercise.html", form=add_exercises)


@app.route("/profile/exercises/show")
@login_required
def show_exercises():
    exercises = Exercise.query.filter_by(user_id=current_user.id).all()
    return render_template("show_exercise.html", exercises=exercises)


@app.route("/profile/info")
@login_required
def profile_info():
    user = User.query.filter_by(id=current_user.id).first()
    bmi = (user.weight / user.height / user.height) * 10000
    bmi = round(bmi, 2)
    calories_burnt_sum = 0
    calories_eaten_sum = 0
    cal_dif = 0
    all_exercises = Exercise.query.filter_by(user_id=current_user.id).all()
    all_meals = Meal.query.filter_by(user_id=current_user.id).all()
    for exercise in all_exercises:
        calories_burnt_sum = exercise.calories_burnt + calories_burnt_sum
    for meal in all_meals:
        calories_eaten_sum = meal.calories + calories_eaten_sum
    cal_dif = round(calories_eaten_sum - calories_burnt_sum)
    bmr = round(calc_bmr(user), 2)
    activity_level = user.activity_level
    amr = round(calc_amr(bmr, activity_level))
    return render_template("profile_info.html", BMI=bmi, calories_burnt_sum=round(calories_burnt_sum), AMR=amr,
                           calories_eaten_sum=round(calories_eaten_sum), cal_dif=cal_dif)


@app.route("/profile/meals")
@login_required
def meals():
    return render_template("meals.html")


@app.route("/profile/meals/add", methods=["GET", "POST"])
@login_required
def add_meal():
    add_meal = AddMeal()
    if request.method == "POST":
        meal_query = add_meal.meal_query.data
        headers_exercise = {
            "x-app-id": APP_ID,
            "x-app-key": API_KEY,
            "Content-Type": 'application/json',
        }
        params_exercise = {
            "query": meal_query,
        }
        json_object = json.dumps(params_exercise, indent=4)
        response = requests.post(API_ENDPOINT_MEALS, headers=headers_exercise, data=json_object)
        data = response.json()
        print(data)
        calories = 0
        fat = 0
        saturated_fat = 0
        cholesterol = 0
        sodium = 0
        total_carbohydrate = 0
        dietary_fiber = 0
        sugars = 0
        protein = 0
        potassium = 0
        now = datetime.now()
        date_now = now.strftime("%Y/%m/%d")
        try:
            for meal in data["foods"]:
                if meal["nf_calories"] is not None:
                    calories = calories + meal["nf_calories"]
                if meal["nf_total_fat"] is not None:
                    fat = fat + meal["nf_total_fat"]
                if meal["nf_saturated_fat"] is not None:
                    saturated_fat = saturated_fat + meal["nf_saturated_fat"]
                if meal["nf_cholesterol"] is not None:
                    cholesterol = cholesterol + meal["nf_cholesterol"]
                if meal["nf_sodium"] is not None:
                    sodium = sodium + meal["nf_sodium"]
                if meal["nf_total_carbohydrate"] is not None:
                    total_carbohydrate = total_carbohydrate + meal["nf_total_carbohydrate"]
                if meal["nf_dietary_fiber"] is not None:
                    dietary_fiber = dietary_fiber + meal["nf_dietary_fiber"]
                if meal["nf_sugars"] is not None:
                    sugars = sugars + meal["nf_sugars"]
                if meal["nf_protein"] is not None:
                    protein = protein + meal["nf_protein"]
                if meal["nf_potassium"] is not None:
                    potassium = potassium + meal["nf_potassium"]
        except KeyError:
            flash("We couldn't match any of your foods")
            return render_template("add_meal.html", form=add_meal)

        meal = Meal(name=meal_query, calories=round(calories), fat=fat, saturated_fat=saturated_fat,
                    cholesterol=cholesterol, sodium=sodium, total_carbohydrate=total_carbohydrate,
                    dietary_fiber=dietary_fiber, sugars=sugars,
                    nf_protein=protein, nf_potassium=potassium, date=date_now, user_id=current_user.id)
        dbmodels.add_to_datebase(meal)

        return redirect(url_for('meals'))
    return render_template("add_meal.html", form=add_meal)

@app.route("/profile/edit", methods=["GET","POST"])
@login_required
def edit_profile():

    editform = EditForm()
    user = User.query.filter_by(id=current_user.id).first()
    if request.method == "POST":
        user.height = editform.height.data
        user.weight = editform.weight.data
        user.age = editform.age.data
        user.gender = editform.gender.data
        user.name = editform.name.data
        user.activity_level = int(editform.activity_level.data)
        db.session.merge(user)
        db.session.commit()
        return redirect(url_for('profile_info'))
    editform.height.data = user.height
    editform.weight.data = user.weight
    editform.age.data = user.age
    editform.gender.data = user.gender
    editform.name.data = user.name
    editform.activity_level.data = user.activity_level
    return render_template("edit_profile.html", form=editform)

@app.route("/profile/meals/show")
@login_required
def show_meals():
    meals = Meal.query.filter_by(user_id=current_user.id).all()
    return render_template("show_meal.html", meals=meals)


if __name__ == '__main__':
    app.run(debug=True)
