from flask import Flask
from forms import contact

app = Flask(__name__, static_url_path = "", static_folder = "static")
app.secret_key = 'jeffries key'
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'jeffries.uom@gmail.com'
app.config["MAIL_PASSWORD"] = 'JeffriesCool'

contact.initialise(app)

from comp61542 import views
