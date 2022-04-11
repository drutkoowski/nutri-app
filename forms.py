from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email


class Login(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Submit Login")


class SignUp(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    name = StringField("First Name: ", validators=[DataRequired()])
    age = IntegerField("Age: ", validators=[DataRequired()])
    gender = SelectField(u'Gender', choices=[('male', 'Male'), ('female', 'Female')])
    height = IntegerField("Height: ", validators=[DataRequired()])
    weight = IntegerField("Weight: ", validators=[DataRequired()])
    submit = SubmitField("Submit Sign Up")


class ProfileInfo(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    name = StringField("First Name: ", validators=[DataRequired()])
    age = IntegerField("Age: ", validators=[DataRequired()])
    gender = SelectField(u'Gender', choices=[('male', 'Male'), ('female', 'Female')])
    height = IntegerField("Height: ", validators=[DataRequired()])
    weight = IntegerField("Weight: ", validators=[DataRequired()])
    submit = SubmitField("Edit your profile info")


class AddExercise(FlaskForm):
    exercise_query = StringField("Describe what have you done today: ", validators=[DataRequired()])
    exercise_duration = IntegerField("Duration in minutes: ", validators=[DataRequired()])
    submit = SubmitField("Submit Exercise")


class AddMeal(FlaskForm):
    meal_query = StringField("Describe what have you done today: ", validators=[DataRequired()])
    submit = SubmitField("Submit Exercise")
