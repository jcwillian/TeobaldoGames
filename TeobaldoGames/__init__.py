from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask('TeobaldoGames')
app.config.from_object('config')
db = SQLAlchemy(app)

from TeobaldoGames import views, models