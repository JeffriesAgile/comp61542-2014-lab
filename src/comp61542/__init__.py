from flask import Flask
from forms import contact, login

app = Flask(__name__, static_url_path = "", static_folder = "static")
app.config.from_object('config')

contact.initialise(app)

from comp61542 import views
