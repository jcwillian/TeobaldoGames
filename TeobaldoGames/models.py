from TeobaldoGames import db
from hashlib import md5

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomeUsuario = db.Column(db.String(120), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    senha = db.Column(db.String(120))
    detonados = db.relationship('Detonado', backref='author', lazy='dynamic')
    jogos = db.relationship('Jogo', backref='own', lazy='dynamic')
    
    def __repr__(self):
        return '<User %r>' % (self.nomeUsuario)
    
    def is_authenticated(self):
    	return True

    def is_active(self):
    	return True

    def is_anonymous(self):
    	return False
    def get_id(self):
    	try:
    		return unicode(self.id) #python2
    	except NameError:
    		return str(self.id) #python3
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' %(md5(self.email.encode('utf-8')).hexdigest(), size)

class Detonado(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    conteudo = db.Column(db.String(140))
    data = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    comentarios = db.relationship('Comentario', backref='author', lazy='dynamic')
    def __repr__(self):
        return '<Detonado %r>' % (self.conteudo)

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime)
    conteudo = db.Column(db.String(140))
    det_id = db.Column(db.Integer, db.ForeignKey('detonado.id'))

    def __repr__(self):
        return 'Comentario: %r' %(self.conteudo)

class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    descricao = db.Column(db.String(1000))
    preco = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    data = db.Column(db.DateTime)

    def __repr__(self):
        return 'Jogo --> %r' %(self.nome)


