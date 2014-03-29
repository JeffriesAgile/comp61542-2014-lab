from flask import Flask, redirect
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
import os.path as op

app = Flask(__name__, static_url_path="", static_folder="static")
app.config.from_object('config')
auth_db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail()
mail.init_app(app)

from comp61542 import views
from database.models import User, Post

admin = Admin(app)

class HomeView(BaseView):
    @expose('/')
    def index(self):
        return redirect('/')

admin.add_view(ModelView(User, auth_db.session))
admin.add_view(ModelView(Post, auth_db.session))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
admin.add_view(HomeView(name='Return to JEFFRIES'))