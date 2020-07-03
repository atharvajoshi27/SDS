from flask import Flask, render_template, url_for, flash, redirect, request
from forms import Registration, Login, Update
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from models import *
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image


URL = "server://username:password@localhost:port/your_database_name"



app = Flask(__name__)
app.config['SECRET_KEY'] = '29f625651624cb373965b968e5a33ccb'
app.config["SQLALCHEMY_DATABASE_URI"] = URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route("/register", methods=["GET", "POST"])
def register():
    form = Registration()
   
    if form.validate_on_submit():
        print("\n\nForm validated!\n\n")
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash(f"Congratulations! Your account has been created successfully!", 'success')
        return redirect(url_for('login'))
    return render_template("Register.html", title='Register', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

        # Note that if I directly tried to access account route I will be directed to login
        # page and then if I looged in then I should be directed to 
        # account route and not home route so
        # to redirect user 
            next_page = request.args.get('next')
            print(type(next_page))
            if next_page:
                if next_page[0] == "/":
                    next_page = next_page[1:]
                flash(f"Login Successful!", 'success')
                return redirect(url_for(next_page))
            else:
                flash(f"Login Successful!", 'success')
                return redirect(url_for('home'))
        else:
            flash(f"Login unsuccessful! Please check email and password again!", 'danger')
    return render_template("Login.html", title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_image(profile):
    random_name = secrets.token_hex(8)
    fileName, fileExtension = os.path.splitext(profile.filename)
    image_filename = random_name +  fileExtension
    image_path = os.path.join(app.root_path, 'static/Profile', image_filename)
    image_size = (125, 125)
    
    i = Image.open(profile)
    i.thumbnail(image_size)
    i.save(image_path)

    return image_filename

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = Update()
    if form.validate_on_submit():
        if form.profile.data:
            image_filename = save_image(form.profile.data)
            current_user.profile_picture = image_filename
        current_user.firstname= form.firstname.data
        current_user.lastname=form.lastname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated!', 'success')
    elif request.method == "GET":
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for('static', filename='Profile/'+current_user.profile_picture)
    return render_template("account.html", title=account, form=form, image=image)

    

if __name__ == '__main__':
    app.run(debug=True)