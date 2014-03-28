__author__ = 'CipherHat'

from comp61542 import auth_db
from comp61542.database import models

u = models.User(username='john', password='haha', email='john@email.com', role=models.ROLE_USER)
auth_db.session.add(u)
auth_db.session.commit()