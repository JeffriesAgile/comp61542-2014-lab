__author__ = 'CipherHat'

from comp61542.database import models

users = models.User.query.all()
for u in users:
    print u.id, u.username, u.password, u.email, u.role