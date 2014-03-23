from flask import Flask
from forms import contact

app = Flask(__name__, static_url_path = "", static_folder = "static")
app.config.from_object('config')

print "haha", app.static_folder
contact.initialise(app)

from comp61542 import views
