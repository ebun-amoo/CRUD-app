from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateTimeLocalField,  EmailField

#creates the form to signup
class RegisterForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')
    
#creates the form to login
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

#creates the form to add writeups
class WritingForm(FlaskForm):
    title = StringField('Writing Title', validators=[DataRequired()])
    due_date = DateTimeLocalField('Due Date', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Add')
    