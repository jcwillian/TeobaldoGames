from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask('TeobaldoGames')
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
from TeobaldoGames import views, models