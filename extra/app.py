from flask import Flask, render_template, url_for, flash, redirect, request
from forms import Registration, Login, Update, AnniversaryForm, TaskForm, PasswordForm, CheckPassword
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, extract
from datetime import datetime
from flask_bcrypt import Bcrypt
from models import *
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image
from simplecrypt import encrypt, decrypt
from cryptography.fernet import Fernet

URL = "postgresql://username:password@localhost:5432/nameofdatabase"

key = b'-ko3jzYj8kzzHnn6epl_hrR9eS-6oag2UVn8QxwrZk8='
CIPHER = Fernet(key)


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
    message='Atharva'
    return render_template('home.html', message=message)

@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route("/events")
def events():
    current_time = datetime.now()
    month = current_time.month
    day = current_time.day
    # if day < 10:
    #     day = "0" + str(day)
    # if month < 10:
    #     month = "0" + str(month)
    # day = str(day)
    # month = str(month)
    today = datetime.today().strftime('%Y-%m-%d')
    anniversaries = Anniversary.query.filter(and_((extract('month', Anniversary.date) == month), (extract('day', Anniversary.date) == day), (Anniversary.user_id == current_user.id)))
    tasks = Task.query.filter(and_((Task.lastdate == today), (Task.user_id == current_user.id)))
    
    if anniversaries.count() == 0:
        print("came here")
        anniversaries = []
    if tasks.count() == 0:
        print("came here 2")
        tasks = []
    
    # anniversaries = Anniversary.query.filter(_and((extract('month', Anniversary.date) == month), extract('day' == day)))
    # anniversaries =  Anniversary.query.filter(Anniversary.date.like(f'%{month}'+'-'+f'{day}')).all()
    return render_template("events.html", title='Events', anniversaries=anniversaries, tasks=tasks)

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
                return redirect(url_for('events'))
        else:
            flash(f"Login unsuccessful! Please check email and password again!", 'danger')
    return render_template("Login.html", title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
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



@app.route("/anniversary", methods=["GET", "POST"])
@login_required
def anniversary():
    anniversaries = current_user.anniversary;
    
    return render_template("anniversary.html", anniversaries=anniversaries)

@app.route("/anniversary/new", methods=["GET", "POST"])
@login_required
def new_anniversary():
    form = AnniversaryForm()
    if form.validate_on_submit():
        anni = Anniversary(name=form.name.data, date=form.date.data, types=form.types.data, note=form.note.data, relative=current_user)
        db.session.add(anni)
        db.session.commit()
        flash("Anniversary Added", 'success')
        return redirect(url_for('anniversary'))
    return render_template("create_anniversary.html", title="New Anniversary", form=form, legend='Add')

@app.route("/anniversary/<int:itsid>/edit", methods=["GET", "POST"])
@login_required
def update_anniversary(itsid):
    anni = Anniversary.query.get_or_404(itsid)
    if anni.relative != current_user:
        abort(403)
    form = AnniversaryForm()
    
    if form.validate_on_submit():
        anni.name = form.name.data
        anni.date = form.date.data
        anni.types = form.types.data
        anni.note = form.note.data
        db.session.commit()
        flash("Anniversary Updated Successfully!", 'success')
        return redirect(url_for('anniversary'))
    elif request.method == "GET":
        form.name.data = anni.name
        form.date.data = anni.date
        form.types.data = anni.types
        form.note.data = anni.types
    return render_template("create_anniversary.html", title='Update Anniversary', form=form, legend='Update')

@app.route("/anniversary/<int:itsid>/delete", methods=["POST"])
@login_required
def delete_anniversary(itsid):
    anni = Anniversary.query.get_or_404(itsid)
    if anni.relative != current_user:
        print("I don't know why I am here!")
        abort(403)
    db.session.delete(anni)
    db.session.commit()
    flash("Anniversary deleted!", 'success')
    return redirect(url_for('anniversary'))


@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    tasks = current_user.tasks; 
    return render_template("tasks.html", tasks=tasks)

@app.route("/tasks/new", methods=["GET", "POST"])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, lastdate=form.lastdate.data, note=form.note.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        flash("Task Added", 'success')
        return redirect(url_for('tasks'))
    return render_template("create_task.html", title="New Task", form=form, legend='Add')

@app.route("/tasks/<int:itsid>/edit", methods=["GET", "POST"])
@login_required
def update_task(itsid):
    task = Task.query.get_or_404(itsid)
    if task.author != current_user:
        abort(403)
    form = TaskForm()
    
    if form.validate_on_submit():
        task.title = form.title.data
        task.lastdate = form.lastdate.data
        task.note = form.note.data
        db.session.commit()
        flash("Task Updated Successfully!", 'success')
        return redirect(url_for('tasks'))
    elif request.method == "GET":
        form.title.data = task.title
        form.lastdate.data = task.lastdate
        form.note.data = task.note
    return render_template("create_task.html", title='Update Task', form=form, legend='Update')

@app.route("/tasks/<int:itsid>/delete", methods=["POST"])
@login_required
def delete_task(itsid):
    task = Task.query.get_or_404(itsid)
    if task.author != current_user:
        print("I don't know why I am here!")
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted!", 'success')
    return redirect(url_for('tasks'))


# Start of Passwords
@app.route("/passwords", methods=["GET", "POST"])
@login_required
def passwords():
    passwords = current_user.passwords; 
    return render_template("password.html", passwords=passwords)

@app.route("/passwords/new", methods=["GET", "POST"])
@login_required
def new_password():
    form = PasswordForm()
    if form.validate_on_submit():
        message = form.password.data # Users real password

        message = message.encode('latin-1') # processed

        encrypted_text = CIPHER.encrypt(message) # Got the value
        encrypted_text = encrypted_text.decode()
        # original_text = CIPHER.decrypt(encrypted_text)
        # print(original_text.decode())
        # encrypted_p = encrypt(MYKEY, form.password.data).decode('latin-1')
        password = Password(site=form.site.data, password=encrypted_text, hint=form.hint.data, user=current_user)
        db.session.add(password)
        db.session.commit()
        flash("Password Added", 'success')
        return redirect(url_for('passwords'))
    return render_template("create_passwords.html", title="New Password", form=form, legend='Add')

@app.route("/passwords/<int:itsid>/edit", methods=["GET", "POST"])
@login_required
def update_password(itsid):
    password_details = Password.query.get_or_404(itsid)
    if password_details.user != current_user:
        abort(403)

    form = PasswordForm()
    
    if form.validate_on_submit():
        message = form.password.data # Users real password
        message = message.encode('latin-1') # processed
        encrypted_text = CIPHER.encrypt(message) # Got the value
        encrypted_text = encrypted_text.decode()
        password_details.site = form.site.data
        password_details.password = encrypted_text
        password_details.hint = form.hint.data
        db.session.commit()
        flash("Password Updated Successfully!", 'success')
        return redirect(url_for('passwords'))

    elif request.method == "GET":
        form.site.data = password_details.site
        form.hint.data = password_details.hint
    return render_template("create_passwords.html", title='Update Password', form=form, legend='Update')

@app.route("/passwords/<int:itsid>/delete", methods=["POST"])
@login_required
def delete_password(itsid):
    password_details = Password.query.get_or_404(itsid)
    if password_details.user != current_user:
        print("I don't know why I am here!")
        abort(403)
    db.session.delete(password_details)
    db.session.commit()
    flash("Password deleted!", 'success')
    return redirect(url_for('passwords'))


@app.route("/passwords/viewpassword/<int:itsid>", methods=["GET", "POST"])
def viewpassword(itsid):
    form = CheckPassword()
    if form.validate_on_submit():
        password_details = Password.query.get_or_404(itsid)
        # original_text = CIPHER.decrypt(encrypted_text)
        # print(original_text.decode())
        encrypted_text = password_details.password
        encrypted_text = encrypted_text.encode()
        original_text = CIPHER.decrypt(encrypted_text).decode()
        # final_password = original_text.decode()
        actual_password = Password(site=password_details.site, password=original_text, user_id=current_user.id)
        return render_template("show_password.html", actual_password=actual_password)
    return render_template("viewpassword.html", form=form, actual_password=False)




if __name__ == '__main__':
    app.run(debug=True)


#     {% for anniversary in anniversaries %}
# <div class="col-12 col-md-6 mt-4">
#     <div class="col-12">
#         <div class="card">
#             <h3 class="card-header bg-info text-white">{{ anniversary.types }}</h3>
#             <div class="card-body">
#                 <p class="h6" style="line-height: 35px;">
#                     {{ anniversary.name }} has {{ anniversary.types }} on <mark style="color: green;">{{ anniversary.date }}</mark style="color: green;">
#                 </p>
#                 {% if anniversary.note %}
#                     <strong> <mark style="color: green; line-height: 35px;"> Note: </mark></strong>
#                     <p class="h6">
#                         {{ anniversary.note }}
#                     </p>
#                 {% endif %}
#              </div>  
#              <div class="container">
#                 <div class="row row-content">
#                     <div class="col-6">
#                         <form action="">
#                             <div class="form-group ml-5">
#                                 <button class="btn btn-primary" style="width: 100px;">Edit</button>
#                             </div>
#                         </form>
#                     </div>
#                     <div class="col-6">
#                         <form action="">
#                             <div class="form-group mr-5">
#                                 <button class="btn btn-danger" style="width: 100px;">Delete</button>
#                             </div>
#                         </form>
#                     </div>
#                 </div>
#             </div> 
#         </div>
#         </form>
#     </div>
# </div>

# {% endfor %}

# {% endblock %}

