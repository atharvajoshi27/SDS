from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms import validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import EmailField, DateField
from models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from datetime import datetime

class Registration(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=1, max=30)])

    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=30)])

    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=40)])

    # email = EmailField('Email', validators[DataRequired(), Email()])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password must match')])

    submit = SubmitField('Sign Up')


#  validate_username() and validate_email() are being called,
# these functions are called with the FlaskForm class that our 
# Registration class inherited from. If you look at the definition for validate_on_submit(),
#  and from there, the definition for validate(), that validate function contains the following line:
# inline = getattr(self.__class__, 'validate_%s' % name, None)

# There is a lot going on in the background, 
# Flask is checking for extra functions created with the naming pattern\:
# "validate_(field name)", and later calling those extra functions.



    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken!')


class Login(FlaskForm):
    # email = EmailField('Email', validators[DataRequired(), Email])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class Update(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=1, max=30)])

    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=30)])

    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=40)])

    email = EmailField('Email', [validators.DataRequired(), validators.Email()])

    profile =   FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) 

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists!')



class AnniversaryForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=30)])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    types = SelectField('Type', validators=[DataRequired()], choices=['Birth Anniversary', 'Marriage Anniversary'], validate_choice=False)
    note = TextAreaField('Note')
    submit = SubmitField('Add')


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=120)])
    note = TextAreaField('Note', validators=[DataRequired()])
    lastdate = DateField('Last Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Add')

