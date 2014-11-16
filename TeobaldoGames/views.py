from TeobaldoGames import app, db, login_manager
from flask import render_template, flash, redirect, session, url_for, request, g , current_app, send_from_directory
from .forms import LoginForm, CadastroForm, GameForm, AddDetonadoForm, FeedbackForm, SearchForm
from models import User, Detonado, Game
from flask.ext.login import login_user, logout_user, current_user, login_required
import datetime
from werkzeug import secure_filename
import os
from flask.ext.sqlalchemy import get_debug_queries
from config import DATABASE_QUERY_TIMEOUT

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
	games = Game.query.order_by('data').all()[::-1][0:9]
	return render_template('home.html', title='Home - TeobaldoGames', games = games, form = form)

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
		if form.photo.data.filename:
			filename = form.nickname.data + secure_filename(form.photo.data.filename)
			form.photo.data.save('TeobaldoGames/static/uploads_images/' + filename)
			user = User(name=form.name.data,
						nickname=form.nickname.data,
						email=form.email.data,
						password=form.password.data,
						photo = filename,
						coin = 0)
		else:
			user = User(name=form.name.data,
						nickname=form.nickname.data,
						email=form.email.data,
						password=form.password.data,
						coin = 0)
		try:
			db.session.add(user)
			db.session.commit()
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
							detonados=detonados,)
@app.route('/addgame', methods=['GET', 'POST'])
@login_required
def addgame():
	form = GameForm()
	if form.validate_on_submit():
		if form.photo_game.data.filename:
			filename = g.user.nickname + form.name.data + secure_filename(form.photo_game.data.filename)
			form.photo_game.data.save('TeobaldoGames/static/uploads_images/' + filename)
			game = Game(name = form.name.data,
						    description = form.description.data,
						    price = float(form.price.data),
							data = datetime.datetime.utcnow(),
							own = g.user,
							photo = filename)
		else:
			game = Game(name = form.name.data,
						    description = form.description.data,
						    price = float(form.price.data),
							data = datetime.datetime.utcnow(),
							own = g.user,
							)
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

@app.route('/game', methods=['GET','POST'])
@app.route('/game/<name>')
@app.route('/game/<name>/<int:id>')
def game(name = None, id = None):
	form = SearchForm()
	if name and id:
		games = Game.query.get(id)
		games = [games]
	elif name:
		games = Game.query.filter_by(name=name).all()
	else:
		if len(g.form.words.data):
			games = Game.query.filter_by(name = g.form.words.data).all()
		else:
			games = Game.query.all()
	return render_template('game.html', 
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

@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/media/<path:filename>')
def media(filename):
    print send_from_directory('static', 'uploads_images/' + filename)
    return 'asdf'

@app.route('/searchgame', methods=['POST'])
def searchgame():
	form = SearchForm()
	print('from')
	return form

@app.route('/buy/<int:id>')
def buy(id = None):
	#Verificando se o id foi informado.
	if id:
		#Obtendo o game informado pelo id.
		game = Game.query.get(id)
		# Verificando se o game existe.
		if game:
			#Verificando se a quantidade de coins e suficiente
			if g.user.coin >= game.price:
				game.own.coin += game.price
				g.user.coin -= game.price
				game.own = g.user
				db.session.add(game)
				db.session.commit()
				db.session.add(g.user)
				db.session.commit()
			else:
				return redirect(url_for('home'))
		else:
			return redirect(url_for('home'))
	return redirect(url_for('mylistgames'))