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
    gender = SelectField(u'Gender', choices=[('m', 'Male'), ('f', 'Female')])
    height = IntegerField("Height: ", validators=[DataRequired()])
    weight = IntegerField("Weight: ", validators=[DataRequired()])
    submit = SubmitField("Submit Sign Up")
