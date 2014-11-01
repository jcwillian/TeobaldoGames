from TeobaldoGames import app

@app.route('/')
@app.route('/home')
def home():
    return 'Home - Teobaldo Games.'