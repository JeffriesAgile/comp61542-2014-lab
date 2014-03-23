__author__ = 'CipherHat'

from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField, SubmitField, validators

class LoginForm(Form):
    username = TextField("Username", [validators.Required("Please enter your username")])
    password = PasswordField("Password", [validators.Required("Please enter your password")])
    remember_me = BooleanField("Remember_Me", default = False)
    submit = SubmitField("Login")
