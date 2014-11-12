from flask.ext.wtf import Form 
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = StringField('password', validators=[DataRequired()])

class CadastroForm(Form):
	nomeUsuario = StringField('nomeUsuario', validators=[DataRequired()])
	username = StringField('username', validators=[DataRequired()])
	email = StringField('emal', validators=[DataRequired()])
	senha = StringField('senha', validators=[DataRequired()])