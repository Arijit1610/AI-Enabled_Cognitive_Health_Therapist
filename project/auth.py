from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user,login_required
from .model import UserAccount, db_session
from project.helpers import custom_login_required
from flask_mail import Message
import random
from flask_mail import Mail
auth = Blueprint('auth', __name__)
from . import mail  
email_list = None
otp = None
# otp_list = []
# mail = Mail(auth)
@auth.route('/user-panel/<string:type>', methods=['GET', 'POST'])
# @custom_login_required('auth.login', login_type='signin')
def login(type):
	global email_list
	if current_user.is_authenticated:
		# If the user is already logged in, redirect them to another page (e.g., the home page)
		return redirect(url_for('route.home'))
	flash("Please signin or Signup",category='info')
	if type == 'signup':
		if request.method == "POST":
			username = request.form.get('username')
			email = request.form.get('email_address')
			phone = request.form.get('phone_number')
			password = request.form.get('password')
			confirm_password = request.form.get('confirm_password')
			user = db_session.query(UserAccount).filter_by(email=email).first()
			if '@gmail.in' not in email and len(email) < 12:
				flash("Incorrect Email address")
			elif user:
				flash('Email already exists', category='info')
			elif len(username) < 3:
				flash("Username must be greater than 3 characters", category='info')
			elif len(phone) != 10:
				flash("Invalid phone number")
			elif len(password) < 6:
				flash("Password must be at least 6 characters", category='info')
			elif password != confirm_password:
				flash("Passwords do not match", category='info')
			else:
				new_user = UserAccount(username=username, email=email, phonenumber=phone, password=password)
				db_session.add(new_user)  # Corrected from db_session.add(user)
				db_session.commit()
				flash("Registration successful!", category='info')
				email_list=email
				return redirect(url_for('auth.otp_verification'))  # Corrected redirection
	elif type == 'signin':
		if request.method == "POST":
			email = request.form.get('email')
			password = request.form.get('password')
			user = db_session.query(UserAccount).filter_by(email=email).first()
			if user:
				if user.password == password:
					flash('Logged in successfully!', category='success')
					login_user(user, remember=True)
					return redirect(url_for('route.home'))
				else:
					flash("Incorrect Password, try again.", category='error')
			else:
				flash('Email does not exist.', category='error')

	return render_template('login.html', user=current_user)

@auth.route('/logout')
@custom_login_required('auth.login', login_type='signin')
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('route.home'))

@auth.route('/otp-verification', methods=['GET', 'POST'])
# @custom_login_required('auth.login')
def otp_verification():
	global email_list  # Declare email_list as a global variable
	global otp  # Declare otp as a global variable
	email_recipient = email_list
	if otp == None:
		otp = random.randint(100000, 999999)
		# otp_list.append(otp)
		msg = Message(
			subject="OTP VERIFICATION",
			recipients=[email_recipient],  # Use a list of recipients
			body=f"Dear Customer,\nYour One Time Password (OTP) for login: {otp}.\nDo not share this OTP with anyone.\nPlease note that the OTP is valid for only one session.\nIf you try to refresh the page or leave the Page, you will be required to regenerate a new OTP"
		)
		mail.send(msg)
	if request.method == "POST":
		digi_1 = request.form.get('input1')
		digi_2 = request.form.get('input2')
		digi_3 = request.form.get('input3')
		digi_4 = request.form.get('input4')
		digi_5 = request.form.get('input5')
		digi_6 = request.form.get('input6')
		print(otp)
		new_otp = digi_1 + digi_2 + digi_3 + digi_4 + digi_5 + digi_6
		if int(new_otp) == otp:
			print("correct")
			return redirect(url_for('route.home'))
		else:
			print("Incorrect")
			print(new_otp)
			print(otp)
			print(f"{digi_1} {digi_2} {digi_3} {digi_4} {digi_5} {digi_6} ")
			flash("invalid OTP entered!! try again")
	return render_template("otpverification.html")