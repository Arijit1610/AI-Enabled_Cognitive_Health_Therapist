from project import app
from flask import Flask, render_template
#route for home page
@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')
	# return "This page is under development"
@app.route('/contact')
def contact():
	return render_template('contact.html')
@app.route('/about')
def about():
	return render_template('about.html')