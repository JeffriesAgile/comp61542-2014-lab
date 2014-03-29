from flask import Flask, redirect
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.admin import Admin, AdminIndexView, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext import login
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

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

class MyBaseView(BaseView):
    @expose('/')
    def index(self):
        return redirect('/')

    def is_accessible(self):
        return login.current_user.is_authenticated()

class MyModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

class MyFileAdmin(FileAdmin):
    def is_accessible(self):
        return login.current_user.is_authenticated()

admin = Admin(app, index_view=MyAdminIndexView(endpoint=None))

admin.add_view(MyModelView(User, auth_db.session))
admin.add_view(MyModelView(Post, auth_db.session))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(MyFileAdmin(path, '/static/', name='Static Files'))
admin.add_view(MyBaseView(name='Return to JEFFRIES'))