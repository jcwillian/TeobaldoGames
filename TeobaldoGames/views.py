from TeobaldoGames import app, db, login_manager
from flask import render_template, flash, redirect, session, url_for, request, g 
from .forms import LoginForm, CadastroForm
from models import Usuario
from flask.ext.login import login_user, logout_user, current_user, login_required

@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(userid):
	return Usuario.query.get(int(userid))

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', title='Home - TeobaldoGames')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Usuario.query.filter_by(username=str(form.username.data)).first()
		if user == None:
			return render_template('login.html', 
							title='Sign In',
							form = form)
			
		if user.senha == form.password.data:
			login_user(user, remember=True)
			return redirect(url_for('home'))

	return render_template('login.html', 
							title='Sign In',
							form = form)

@app.route('/Cadastro', methods=['GET', 'POST'])
def cadastro():
	form = CadastroForm()
	if form.validate_on_submit():
		user = Usuario(nomeUsuario=form.nomeUsuario.data,
						username=form.username.data,
						email=form.email.data,
						senha=form.senha.data)
		try:
			db.session.add(user)
			db.session.commit()
			session['username'] = form.username.data
		except:
			print('Erro no banco de dados')
			return redirect(url_for('Cadastro'))
		return redirect(url_for('home'))
	return render_template('cadastro.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	'''session['username'] = '''
	return redirect(url_for('home'))

@app.route('/user/<username>')
@login_required
def user(username):
	user = Usuario.query.filter_by(username=username).first()
	if user == None:
		flash('Usuario %s nao encontrado.' %(username))
		return redirect(url_for('home'))
	detonados = [
		{'author': user, 'body':'Teste detonado 1'},
		{'author': user, 'body': 'Teste detonado 2'}
	]
	return render_template('user.html',
							user=user,
							detonados=detonados)
