from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, LoginManager

db =  SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    # tablename will automatically be set to 'user' (note the lowercase) if not mentioned
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), unique=False, nullable=False)
    lastname = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)
    setkey = db.Column(db.Text, default='ryuzaki', unique=False, nullable=False)
    profile_picture = db.Column(db.String(50), default='image.jpg', nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    anniversary = db.relationship('Anniversary', backref='relative', lazy=True)
    tasks = db.relationship('Task', backref='author', lazy=True)
    passwords = db.relationship('Password', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}')"

class Post(db.Model): 
    # tablename will automatically be set to 'post' (Note the lowercase) if not mentioned
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f"Post({self.title}, '{self.date_posted}')"

class Anniversary(db.Model):
    __tablename__ = "anniversary"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    date = db.Column(db.Date, nullable=False)
    types = db.Column(db.String(30), nullable=False)
    note = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    note = db.Column(db.Text, nullable=False)
    lastdate = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Password(db.Model):
    __tablename__ = "passwords"
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    hint = db.Column(db.String(60), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)