from TeobaldoGames import db
import re
from TeobaldoGames import app
from hashlib import md5

import sys
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask.ext.whooshalchemy as whooshalchemy

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
    )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    photo = db.Column(db.String(100))
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(30))
    coin = db.Column(db.Integer)
    detonados = db.relationship('Detonado', backref='author', lazy='dynamic')
    games = db.relationship('Game', backref='own', lazy='dynamic')
    buy = db.relationship('Purchase', backref='buyer', lazy='dynamic')
    sales = db.relationship('Sale', backref='buyer', lazy='dynamic')
    followed = db.relationship('User',
                                secondary= followers,
                                primaryjoin=(followers.c.follower_id == id),
                                secondaryjoin=(followers.c.followed_id == id), 
                                backref=db.backref('followers', lazy='dynamic'), 
                                lazy='dynamic')
        
    def __repr__(self):
        return '<User %r>' % (self.nickname)
    
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

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).coutn() > 0
    def followed_posts(self):
        return Game.query.join(followers, (followers.c.followed_id == Game.user_id)).filter(followers.c.follower_id == self.id).order_by(Game.data.desc())
class Detonado(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    body = db.Column(db.String(140))
    data = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    feedback = db.relationship('Feedback', backref='author', lazy='dynamic')
    def __repr__(self):
        return '<Detonado %r>' % (self.body)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime)
    message = db.Column(db.String(140))
    det_id = db.Column(db.Integer, db.ForeignKey('detonado.id'))

    def __repr__(self):
        return 'Feedback: %r' %(self.message)

class Game(db.Model):

    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bought = db.Column(db.Integer, db.ForeignKey('item_of_purchase.id'))
    data = db.Column(db.DateTime)
    photo = db.Column(db.String(100))

    def __repr__(self):
        return 'Jogo --> %r' %(self.name)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    items_of_purchase = db.relationship('Item_of_purchase', backref='buy', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.DateTime)

class Item_of_purchase(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    game = db.relationship('Game', backref='bu')
    purchase = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    seller = db.Column(db.Integer, db.ForeignKey('sale.id'))

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.DateTime)
    items_of_purchase = db.relationship('Item_of_purchase', backref='purchaser', lazy='dynamic')

if enable_search:
    whooshalchemy.whoosh_index(app, Jogo)