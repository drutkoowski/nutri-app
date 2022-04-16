from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField, Label, TextAreaField
from wtforms.validators import DataRequired, Email


class Login(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email()],
                        render_kw={'placeholder': 'Enter your email', 'style': 'font-size:1.5em;'})
    password = PasswordField(validators=[DataRequired()],
                             render_kw={'placeholder': 'Enter your password', 'style': 'font-size:1.5em;'})
    submit = SubmitField("Submit Login", render_kw={'style': 'font-size:1.5em;margin-top:1rem!important;'})


class SignUp(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email()],
                        render_kw={'placeholder': 'Enter your email', 'style': 'font-size:1.5em;'})
    password = PasswordField("Password: ", validators=[DataRequired()],
                             render_kw={'placeholder': 'Enter your password', 'style': 'font-size:1.5em;'})
    name = StringField("First Name: ", validators=[DataRequired()],
                       render_kw={'placeholder': 'Enter your first name', 'style': 'font-size:1.5em;'})
    age = IntegerField("Age: ", validators=[DataRequired()],
                       render_kw={'placeholder': 'Enter your age', 'style': 'font-size:1.5em;'})
    gender = SelectField(u'Gender', choices=[('male', 'Male'), ('female', 'Female')],
                         render_kw={'style': 'font-size:1.5em;'})
    height = IntegerField("Height (cm): ", validators=[DataRequired()],
                          render_kw={'placeholder': 'Enter your height (cm)', 'style': 'font-size:1.5em;'})
    weight = IntegerField("Weight (kg): ", validators=[DataRequired()],
                          render_kw={'placeholder': 'Enter your weight (kg)', 'style': 'font-size:1.5em;'})
    activity_level = SelectField(u"How active are you? ", choices=[('0', 'Sedentary'), ('1', 'Light activity'),
                                                                   ('2', 'Moderate Activity'), ('3', 'Active'),
                                                                   ('4', 'Very active')],
                                 render_kw={'style': 'font-size:1.5em;'})
    submit = SubmitField("Submit Sign Up", render_kw={'style': 'font-size:1.5em;margin-top:1rem!important;'})


class ProfileInfo(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    name = StringField("First Name: ", validators=[DataRequired()])
    age = IntegerField("Age: ", validators=[DataRequired()])
    gender = SelectField(u'Gender', choices=[('male', 'Male'), ('female', 'Female')])
    height = IntegerField("Height: ", validators=[DataRequired()])
    weight = IntegerField("Weight: ", validators=[DataRequired()])
    submit = SubmitField("Edit your profile info", render_kw={'style': 'font-size:1.5em;margin-top:1rem!important;'})


class AddExercise(FlaskForm):
    exercise_query = StringField("Describe what have you done today: ", validators=[DataRequired()], render_kw={
        'placeholder': 'For example: Ran 2 km, walked 3.5 km, 10 push-ups and 30 squats ', 'style': 'font-size:1.5em;'})
    exercise_duration = IntegerField("Duration in minutes: ", validators=[DataRequired()],
                                     render_kw={'placeholder': 'Total exercise duration in minutes',
                                                'style': 'font-size:1.5em;'})
    submit = SubmitField("Submit Exercise", render_kw={'style': 'font-size:1.5em;margin-top:1rem!important;'})


class AddMeal(FlaskForm):
    meal_query = StringField("Describe what have you eaten today: ", validators=[DataRequired()], render_kw={
        'placeholder': 'For example: One apple with a teaspoon of peanut butter', 'style': 'font-size:1.5em;'})
    submit = SubmitField("Submit meal", render_kw={'style': 'font-size:1.5em;margin-top:1rem!important;'})


class EditForm(FlaskForm):
    name = StringField("First Name: ", validators=[DataRequired()],
                       render_kw={'placeholder': 'Type your new name', 'style': 'font-size:1.5em;'})
    age = IntegerField("Age: ", validators=[DataRequired()],
                       render_kw={'placeholder': 'Type your new age', 'style': 'font-size:1.5em;'})
    gender = SelectField(u'Gender', choices=[('male', 'Male'), ('female', 'Female')],
                         render_kw={'style': 'font-size:1.5em;'})
    height = IntegerField("Height (cm): ", validators=[DataRequired()],
                          render_kw={'placeholder': 'Type your new height', 'style': 'font-size:1.5em;'})
    weight = IntegerField("Weight (kg): ", validators=[DataRequired()],
                          render_kw={'placeholder': 'Type your new weight', 'style': 'font-size:1.5em;'})
    activity_level = SelectField(u"How active are you? ", choices=[('0', 'Sedentary'), ('1', 'Light activity'),
                                                                   ('2', 'Moderate Activity'), ('3', 'Active'),
                                                                   ('4', 'Very active')],
                                 render_kw={'style': 'font-size:1.5em;'})
    submit = SubmitField("Edit your profile", render_kw={'style': 'font-size:1.5em;margin-top:1rem!important;'})
