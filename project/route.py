from project import app
from flask import render_template, request, flash, redirect, url_for
from project.model import UserAccount, db_session
# from project.forms import SignupForm

# Route for the home page
@app.route('/')
@app.route('/home')
def home():
	flash("Flask app message")
	return render_template('home.html')


# Route for the contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/user-panel/<string:type>', methods=['GET', 'POST'])
def signup(type):
	# flash("Fill this form","info")
	if type == 'signup':
		if request.method == "POST":
			username = request.form.get('username')
			email = request.form.get('email_address')
			phone = request.form.get('phone_number')
			password = request.form.get('password')
			confirm_password = request.form.get('confirm_password')
			if '@gmail.in' not in email:
				flash("Incorrect Email address")
				return render_template('login.html')
			user = UserAccount(username=username, email=email, phonenumber=phone, password=password)
			db_session.add(user)
			db_session.commit()
			return redirect(url_for('home'))
	elif type == 'signin':
		if request.method == "POST":
			email = request.form.get('email')
			password = request.form.get('password')
			ret = db_session.query(UserAccount).filter_by(email=email).first()
			# print(f"{email}={ret.email} {password}={ret.password}")
			try:
				if ret.email == email and ret.password==password:
					return redirect(url_for('about'))
			except:
				flash("Incorrect Username or Password")

	return render_template('login.html')