from flask import Flask 

app = Flask('TeobaldoGames')
app.config.from_object('config')

from TeobaldoGames import views