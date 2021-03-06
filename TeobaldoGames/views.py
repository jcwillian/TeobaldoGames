from TeobaldoGames import app, db, login_manager
from flask import render_template, flash, redirect, session, url_for, request, g , current_app, send_from_directory
from .forms import *
from models import *
from flask.ext.login import login_user, logout_user, current_user, login_required
import datetime
from werkzeug import secure_filename
import os
from flask.ext.sqlalchemy import get_debug_queries
from config import DATABASE_QUERY_TIMEOUT
from random import randint, shuffle

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
app.config['MEDIA_ROOT'] = os.path.join(PROJECT_ROOT, 'media_files')

@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (query.statement, query.parameters, query.duration, query.context))
    return response

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
    g.form = SearchForm()

@login_manager.user_loader
def load_user(userid):
	return User.query.get(int(userid))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@app.route('/home',methods=['GET', 'POST'])
def home():
	form = SearchForm()
	games = Game.query.order_by('data').all()[::-1][0:6]
	return render_template('home.html', title='Home - TeobaldoGames', games = games, form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(nickname=str(form.nickname.data)).first()
		if user == None:
			flash('Usuario ou Senha incorretos.')
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
					password=form.password.data,
					photo = form.photo.data,
					coin = 0)
		try:
			db.session.add(user)
			db.session.commit()
		except:
			flash('Erro no cadastro Tente novamente')
			return redirect(url_for('singup'))
		login_user(user, remember=True)
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
	jc = jogoscomprados(user)
	jv = jogosvendidos(user)

	return render_template('user.html',
							user=user,
							jc=jc,
							jv=jv)
@app.route('/addgame', methods=['GET', 'POST'])
@login_required
def addgame():
	form = GameForm()
	if form.validate_on_submit():
		game = Game(name = form.name.data,
				    description = form.description.data,
				    price = float(form.price.data),
					data = datetime.datetime.utcnow(),
					own = g.user,
					photo = form.photo_game.data)
		
		db.session.add(game)
		db.session.commit()
		flash('%s adicionado com sucesso!' %(form.name.data))
		return redirect(url_for('mylistgames'))
	return render_template('addGame.html',
							title = 'Add Game',
							form = form)

@app.route('/mylistgames')
@login_required
def mylistgames():
	games = g.user.games.all()
	return render_template('mylistgames.html', title='My list game', games = games)

@app.route('/game', methods=['GET','POST'])
@app.route('/game/<name>')
@app.route('/game/<name>/<int:id>')
def game(name = None, id = None):
	form = SearchForm()
	if request.method == 'POST':
		word = request.form['search']
		games = Game.query.filter(Game.name.contains(word)).all()
	else:
		if name and id:
			game = Game.query.get(id)
			return render_template('game.html', 
								title=name,
								game = game)
		elif name:
			games = Game.query.filter_by(name=name).all()
		else:
			if g.form.words.data:
				games = Game.query.filter_by(name = g.form.words.data).all()
			else:
				games = Game.query.all()
	return render_template('games.html', 
								title=name,
								games = games)

@app.route('/criardetonado', methods=['GET','POST'])
def criardetonado():
	form = AddDetonadoForm()
	if form.validate_on_submit():
		detonado = Detonado(title=form.title.data,
							body = form.body.data,
							data = datetime.datetime.utcnow(),
							author = g.user)
		db.session.add(detonado)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('criardetonado.html', title='Criar Detonado', form=form)


@app.route('/buy/<int:id>')
def buy(id = None):
	#Verificando se o id foi informado.
	if id:
		#Obtendo o game informado pelo id.
		game = Game.query.get(id)
		# Verificando se o game existe.
		if game and not g.user.nickname == game.own.nickname:
			#Verificando se a quantidade de coins e suficiente
			if g.user.coin >= game.price:
				purchase = Purchase(buyer = game.own,
									data = datetime.datetime.utcnow())
				sale = Sale(buyer = g.user,
							data = datetime.datetime.utcnow())
				items = Item_of_purchase(buy = purchase, purchaser=sale)
				game.bu = items

				game.own.coin += game.price
				g.user.coin -= game.price
				db.session.add(game.own)
				db.session.commit()
				game.own = g.user
				db.session.add(game)
				db.session.commit()
				db.session.add(g.user)
				db.session.commit()
				db.session.add(purchase)
				db.session.commit()
				db.session.add(sale)
				db.session.commit()
				db.session.add(items)
				db.session.commit()
			else:
				flash('Quantidade de TGCoins insuficiente!')
				return redirect(url_for('home'))
		else:
			return redirect(url_for('home'))
	flash('%s foi comprado com sucesso!' %(game.name))
	return redirect(url_for('mylistgames'))

@app.route('/addcoin', methods=['GET', 'POST'])
def addcoin():
	form = AddCoinForm()
	if form.validate_on_submit():
		qtd_coin = int(form.qtd_coin.data)
		g.user.coin += qtd_coin
		db.session.add(g.user)
		db.session.commit()
		flash('%d TGCoins foram adicionado em seu perfil' %(qtd_coin))
		return redirect(url_for('user', nickname=g.user.nickname, id=g.user.id))
	return render_template('addcoin.html', form=form, title='Add coin')

@app.route('/editeperfil', methods=['GET', 'POST'])
def editeperfil():
	form = EditePerfilForm()
	if form.validate_on_submit():
		g.user.name = form.name.data;
		g.user.email = form.email.data;
		db.session.add(g.user)
		db.session.commit()
		flash('Perfil atualizado com sucesso!')
		return redirect(url_for('user', nickname=g.user.nickname, id=g.user.id))
	return render_template('editaruser.html', form=form, title='Edite Perfil')

@app.route('/editephoto', methods=['GET','POST'])
def editephoto():
	form = AtualizePhotoForm()
	if form.validate_on_submit():
		if form.photo.data:
			g.user.photo = form.photo.data
			db.session.add(g.user)
			db.session.commit()
			flask('Foto atualizada com sucesso')
			return redirect(url_for('user', nickname=g.user.nickname, id = g.user.id))
	return render_template('editphoto.html', form=form, title='Edite photo')	

@app.route('/editgame/<int:id>', methods=['GET', 'POST'])
def editgame(id = None):
	form = AtualizeGameForm()
	if id:
		game = Game.query.get(id)
		if form.validate_on_submit():
			game.name = form.name.data
			game.description = form.description.data
			game.price = form.price.data
			if form.photo_game.data:
				game.photo = form.photo_game.data
							
			db.session.add(game)
			db.session.commit()
			flask('Jogo atualizado com sucesso!')
			return redirect(url_for('mylistgames'))

		return render_template('editgame.html', title='edit Game', form=form, game=game)
	else:
		return redirect(url_for('home'))

@app.route('/deletegame/<int:id>', methods=['GET', 'POST'])
def deletegame(id = None):
	if id:
		game = Game.query.get(id)
		db.session.delete(game)
		db.session.commit()
		flask('Jogo deletado com sucesso')
		return redirect(url_for('mylistgames'))
	return redirect(url_for('home'))


def jogoscomprados(user):
	compras = user.sales.all()
	games = games = [x.items_of_purchase.all()[0].game for x in compras]
	games = [x[0] for x in games if len(x)]
	return games

def jogosvendidos(user):
	compras = user.buy.all()
	games = games = [x.items_of_purchase.all()[0].game for x in compras]
	games = [x[0] for x in games if len(x)]
	return games