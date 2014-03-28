__author__ = 'CipherHat'

import os
from comp61542.static import wee

basedir = os.path.abspath(os.path.dirname(wee))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'jeffries key'
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'jeffries.uom@gmail.com'
MAIL_PASSWORD = 'JeffriesCool'