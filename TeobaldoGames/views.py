from TeobaldoGames import app, db, login_manager
from flask import render_template, flash, redirect, session, url_for, request, g 
from .forms import LoginForm, CadastroForm, GameForm, AddDetonadoForm, FeedbackForm
from models import User, Detonado, Game
from flask.ext.login import login_user, logout_user, current_user, login_required
import datetime

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500

@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(userid):
	return User.query.get(int(userid))

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', title='Home - TeobaldoGames')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(nickname=str(form.nickname.data)).first()
		if user == None:
			return render_template('login.html', 
							title='Sign In',
							form = form)
			
		if user.password == form.password.data:
			login_user(user, remember=True)
			return redirect(url_for('home'))

	return render_template('login.html', 
							title='Sign In',
							form = form)

@app.route('/singup', methods=['GET', 'POST'])
def singup():
	form = CadastroForm()
	if form.validate_on_submit():
		user = User(name=form.name.data,
						nickname=form.nickname.data,
						email=form.email.data,
						password=form.password.data)
		try:
			db.session.add(user)
			db.session.commit()
			session['nickname'] = form.nickname.data
		except:
			print('Erro no banco de dados')
			return redirect(url_for('singup'))
		return redirect(url_for('home'))
	return render_template('cadastro.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	'''session['nickname'] = '''
	return redirect(url_for('home'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user == None:
		flash('Usuario %s nao encontrado.' %(nickname))
		return redirect(url_for('home'))
	detonados = [
		{'author': user, 'body':'Teste detonado 1'},
		{'author': user, 'body': 'Teste detonado 2'}
	]
	return render_template('user.html',
							user=user,
							detonados=detonados)
@app.route('/addgame', methods=['GET', 'POST'])
@login_required
def addgame():
	form = GameForm()
	if form.validate_on_submit():
		game = Game(name = form.name.data,
						    description = form.description.data,
						    price = float(form.price.data),
							data = datetime.datetime.utcnow(),
							own = g.user)
		db.session.add(game)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('addGame.html',
							title = 'Add Game',
							form = form)

@app.route('/mylistgames')
@login_required
def mylistgames():
	games = g.user.games.all()
	return render_template('mylistgames.html', title='My list game', games = games)

@app.route('/game')
@app.route('/game/<name>')
@app.route('/game/<name>/<int:id>')
def game(name = None, id = None):
	if name and id:
		games = Game.query.get(id)
		lista = False
	elif name:
		games = Game.query.filter_by(name=name).all()
		lista = True
	else:
		return redirect(url_for('home'))

	return render_template('game.html', 
								title=name,
								games = games,
								lista = lista)

