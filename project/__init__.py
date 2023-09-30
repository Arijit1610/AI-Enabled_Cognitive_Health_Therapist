from flask import Flask
# from project.forms import SignupForm,SigninForm
from project.model import db_session

app = Flask(__name__)
app.secret_key = 'super-secret-key'

from project import route

