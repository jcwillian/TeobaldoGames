from flask_wtf import Form 
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

class CadastroForm(Form):
	nomeUsuario = StringField('nomeUsuario', validators=[DataRequired()])
	username = StringField('username', validators=[DataRequired()])
	email = StringField('emal', validators=[Email(message='Email invalido')])
	senha = PasswordField('senha', validators=[DataRequired()])