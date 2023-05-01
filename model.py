from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

#prevent error: working outside of the application context. To solve this, set up an application context with app.app_context()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    SECRET_KEY = "some secret key"
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

#creates the schema for the User table 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)

    #adds a backref to the User model
    writeups = db.relationship('Writeup', backref='owner')

#creates the schema for the Writeup table 
class Writeup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime, default=datetime.now)
    due_date = db.Column(db.DateTime, nullable= False)
    writer = db.Column(db.Integer,db.ForeignKey('user.id'))
    
    