from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=25)])
    email_address = StringField('email_address', validators=[DataRequired(), Email(), Length(min=6, max=50)])
    phone_number = IntegerField('phone_number', validators=[DataRequired(), NumberRange(min=1000000000, max=999999999999)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class SigninForm(FlaskForm):
    email_address = StringField('email_address', validators=[DataRequired(), Email(), Length(min=6, max=50)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Sign In')

