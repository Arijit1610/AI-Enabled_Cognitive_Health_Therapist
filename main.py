from flask import Flask, render_template
app = Flask(__name__)
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
@app.route('/service')
def service():
	return render_template("Services.html")
app.run(debug=True)