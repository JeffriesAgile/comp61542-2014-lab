__author__ = 'CipherHat'

from comp61542 import auth_db
from comp61542.database import models
import sys

u = models.User(username=sys.argv[1], password=sys.argv[2], email=sys.argv[1]+'@email.com', role=models.ROLE_USER)
auth_db.session.add(u)
auth_db.session.commit()