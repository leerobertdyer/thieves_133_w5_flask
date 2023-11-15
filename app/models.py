from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


#Create instance of sql
db = SQLAlchemy()

team = db.Table(
    'team',
    db.Column('player', db.Integer, db.ForeignKey('user.id')),
    db.Column('pokemon', db.String, db.ForeignKey('pokemon.name'))
)

#uses class to push to database...
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_user_joined = db.Column(db.DateTime, default=datetime.utcnow())
    team = db.relationship('Pokemon', 
                           secondary=team, 
                           backref=db.backref('team', lazy='dynamic'),
                           lazy='dynamic') 
    
    def __init__(self, username, email, password):
        self.username=username
        self.email=email
        self.password=generate_password_hash(password, method='pbkdf2:sha256')
        
class Pokemon(db.Model):
    name = db.Column(db.String, primary_key=True)
    sprite = db.Column(db.String, nullable=False)
    ability = db.Column(db.String)
    hp = db.Column(db.String, nullable=False) #maybe these last three are ints...
    att = db.Column(db.String, nullable=False)
    df = db.Column(db.String, nullable=False)
    date_pokemon_added = db.Column(db.DateTime, default=datetime.utcnow())
