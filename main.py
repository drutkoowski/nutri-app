from flask import Flask, render_template
import requests
import json
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




@app.route("/signup")
def signup():
    signup = SignUp()
    return render_template("signup.html", form=signup)

@app.route("/login")
def login():
    login = Login()
    return render_template("login.html", form=login)

# response = requests.get(API_ENDPOINT, headers=headers,params=params)
# data = response.json()
# print(data)

if __name__ == '__main__':
    app.run(debug=True)
