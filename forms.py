from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import validators
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import EmailField


class Registration(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])

    # email = EmailField('Email', validators[DataRequired(), Email()])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password must match')])

    submit = SubmitField('Sign Up')

class Login(FlaskForm):
    # email = EmailField('Email', validators[DataRequired(), Email])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')