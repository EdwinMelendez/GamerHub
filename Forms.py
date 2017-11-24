from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, Length



# flask forms
class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired(), Length(min=3, max=50)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=6, max=100)])
    remember_me = BooleanField('Remember Me: ')


class SignupForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired(), Length(min=3, max=50)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=6, max=100)])
    confirm_password = PasswordField('Confirm Password:', validators=[InputRequired(), Length(min=6, max=100)])
    email = StringField('Email:', validators=[InputRequired(), Email(), Length(min=8, max=50)])
    submit = SubmitField("Sign In")