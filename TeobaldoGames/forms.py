from flask_wtf import Form 
from wtforms import StringField, PasswordField, TextAreaField, FloatField, FileField, IntegerField
from wtforms.validators import DataRequired, Email

class LoginForm(Form):
	nickname = StringField('nickname', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

class CadastroForm(Form):
	photo = FileField('photo')
	name = StringField('name', validators=[DataRequired()])
	nickname = StringField('nickname', validators=[DataRequired()])
	email = StringField('email', validators=[Email(message='Email invalido')])
	password = PasswordField('New Password', 
        validators=[DataRequired()])

class AddDetonadoForm(Form):
	title = StringField('title', validators=[DataRequired()])
	body = TextAreaField('body')
	photo = FileField('photo')

class FeedbackForm(Form):
	message = TextAreaField('message')

class GameForm(Form):
	name = StringField('name', validators=[DataRequired()])
	description = TextAreaField('description')
	price = FloatField('price', validators=[DataRequired()])
	photo_game = FileField('photo_game')

class SearchForm(Form):
	words = StringField('words')
