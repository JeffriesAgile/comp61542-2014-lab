from comp61542 import app
from comp61542.database import (database, mock_database)
import sys
import os

data_file = 'comp61542/static/data/dblp_curated_sample.xml'
path, dataset = os.path.split(data_file)
print "Database: path=%s name=%s" % (path, dataset)
db = database.Database()
if db.read(data_file) == False:
    sys.exit(1)

app.config['DATASET'] = dataset
app.config['DATABASE'] = db

if "DEBUG" in os.environ:
    app.config['DEBUG'] = True

if "TESTING" in os.environ:
    app.config['TESTING'] = True

app.debug = True
app.run(host='0.0.0.0', port=5000)
