from TeobaldoGames import app
from flask import render_template, flash, redirect
from .forms import LoginForm

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home - TeobaldoGames')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login sucessu.')
		return redirect('/home')
	return render_template('login.html', 
							title='Sign In',
							form = form)