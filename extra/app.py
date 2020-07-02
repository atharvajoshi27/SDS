from flask import Flask, render_template, url_for, flash, redirect, request
from forms import Registration, Login
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from models import *
from flask_login import login_user, current_user, logout_user, login_required


URL = "postgresql://postgres:password@localhost:5432/testdatabase"



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

@app.route("/account")
@login_required
def account():
    return render_template("account.html", title=account)

    

if __name__ == '__main__':
    app.run(debug=True)