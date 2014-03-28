from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, static_url_path="", static_folder="static")
app.config.from_object('config')
auth_db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail()
mail.init_app(app)

from comp61542 import views
from database import models