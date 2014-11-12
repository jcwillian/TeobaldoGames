from TeobaldoGames import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomeUsuario = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    detonados = db.relationship('Detonado', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Detonado(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    conteudo = db.Column(db.String(140))
    data = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    def __repr__(self):
        return '<Post %r>' % (self.conteudo)