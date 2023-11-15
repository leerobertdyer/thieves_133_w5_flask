from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class SignupForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
class LoginForm(FlaskForm):
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Login: ')