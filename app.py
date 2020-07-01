from flask import Flask, render_template, url_for, flash, redirect
from forms import Registration, Login
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '29f625651624cb373965b968e5a33ccb'

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route("/register", methods=["GET", "POST"])
def register():
    form = Registration()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", 'success')
        return redirect(url_for('home'))
    return render_template("Register.html", title='Register', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    if form.validate_on_submit():
        flash(f"Logged in for {form.email.data}!", 'success')
        return redirect(url_for('home'))
    return render_template("Login.html", title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)