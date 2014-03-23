__author__ = 'CipherHat'
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, BooleanField, validators, ValidationError


class ContactForm(Form):
    name = TextField("Name", [validators.Required("Please enter your name.")])
    email = TextField("Email", [validators.Required("Please enter your email address."),
                                validators.Email("Please enter a valid email address.")])
    subject = TextField("Subject", [validators.Required("Please enter a subject.")])
    message = TextAreaField("Message", [validators.Required("Please enter a message.")])
    submit = SubmitField("Send")


class LoginForm(Form):
    username = TextField("Username", [validators.Required("Please enter your username")])
    password = PasswordField("Password", [validators.Required("Please enter your password")])
    remember_me = BooleanField("Remember_Me", default=False)
    submit = SubmitField("Login")


