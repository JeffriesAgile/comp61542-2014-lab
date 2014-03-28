__author__ = 'CipherHat'

from comp61542 import auth_db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(auth_db.Model):
    id = auth_db.Column(auth_db.Integer, primary_key = True)
    username = auth_db.Column(auth_db.String(64), unique = True)
    password = auth_db.Column(auth_db.String(100), unique=False)
    email = auth_db.Column(auth_db.String(120), unique = True)
    role = auth_db.Column(auth_db.SmallInteger, default = ROLE_USER)
    posts = auth_db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Post(auth_db.Model):
    id = auth_db.Column(auth_db.Integer, primary_key = True)
    body = auth_db.Column(auth_db.String(140))
    timestamp = auth_db.Column(auth_db.DateTime)
    user_id = auth_db.Column(auth_db.Integer, auth_db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)