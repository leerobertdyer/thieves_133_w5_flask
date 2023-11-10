from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


#Create instance of sql
db = SQLAlchemy()


#uses class to push to database...
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_user_joined = db.Column(db.DateTime, default=datetime.utcnow())
    
    def __init__(self, first_name, last_name, email, password):
        self.first_name=first_name
        self.last_name=last_name
        self.email=email
        self.password=generate_password_hash(password)