from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db =  SQLAlchemy()

class User(db.Model):
    # tablename will automatically be set to 'user' (note the lowercase) if not mentioned
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), unique=False, nullable=False)
    lastname = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)
    profile_picture = db.Column(db.String(50), default='image.jpg', nullable=True)
    posts = db.relationship('Note', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}')"

class Note(db.Model): 
    # tablename will automatically be set to 'note' (note the lowercase) if not mentioned
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f"Note({self.title}, '{self.date_posted}')"