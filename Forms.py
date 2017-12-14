from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

'''flask forms for logging in and registration'''


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired(), Length(min=3, max=50)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=6, max=100)])


class SignupForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired(), Length(min=3, max=50)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=6, max=100)])
    email = StringField('Email:', validators=[InputRequired(), Length(min=8, max=50)])


