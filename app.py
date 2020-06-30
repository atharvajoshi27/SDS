from flask import Flask, render_template, url_for

from forms import Registration, Login


app = Flask(__name__)

app.config['SECRET_KEY'] = '29f625651624cb373965b968e5a33ccb'

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route("/register")
def register():
    form = Registration()
    return render_template("Register.html", title='Register', form=form)

@app.route("/login")
def login():
    form = Login()
    return render_template("Login.html", title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)