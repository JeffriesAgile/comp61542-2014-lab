__author__ = 'CipherHat'

from comp61542 import auth_db
from comp61542.database import models

u = models.User(username='admin', password='admin', email='admin@email.com', role=models.ROLE_ADMIN)
auth_db.session.add(u)
auth_db.session.commit()