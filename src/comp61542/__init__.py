from flask import Flask
from flask_mail import Mail

app = Flask(__name__, static_url_path="", static_folder="static")
app.config.from_object('config')

mail = Mail()
mail.init_app(app)

from comp61542 import views
