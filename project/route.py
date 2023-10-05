from flask import render_template, request, flash, redirect, url_for,Blueprint
from project.model import UserAccount, db_session
from flask_login import login_required, current_user
# from project.forms import SignupForm
route = Blueprint('route',__name__)
# Route for the home page
@route.route('/')
@route.route('/home')
def home():
	flash("Flask app message")
	return render_template('home.html', user = current_user)


# Route for the contact page
@route.route('/contact')
def contact():
    return render_template('contact.html',user = current_user)

# Route for the about page
@route.route('/about')
def about():
    return render_template('about.html',user = current_user)
