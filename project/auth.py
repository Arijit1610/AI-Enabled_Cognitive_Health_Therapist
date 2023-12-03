from flask import Blueprint, render_template, request, flash, redirect, url_for,session
from flask_login import login_user, logout_user, current_user,login_required
from .model import UserAccount, db_session,Admin
# ,TherapistLoginCredentials
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
	if 'registered_user' in session:
		# If the user is already logged in, redirect them to another page (e.g., the home page)
		return redirect(url_for('route.home'))
	flash("Unlock a brighter, healthier you. Join us on your journey to better mental health. Log in and start your path to well-being today.",category='info')
	if type == 'signup':
		if request.method == "POST":
			username = request.form.get('username')
			email = request.form.get('email_address')
			phone = request.form.get('phone_number')
			password = request.form.get('password')
			confirm_password = request.form.get('confirm_password')
			user = db_session.query(UserAccount).filter_by(email=email).first()
			if '@gmail.in' not in email and len(email) < 12:
				flash("Incorrect Email address",category='error')
			elif user:
				flash('Email already exists',category='info')
			elif len(username) < 3:
				flash("Username must be greater than 3 characters",category='info')
			elif len(phone) != 10:
				flash("Invalid phone number",category='info')
			elif len(password) < 6:
				flash("Password must be at least 6 characters",category='info')
			elif password != confirm_password:
				flash("Passwords do not match",category='info')
			else:
				new_user = UserAccount(username=username, email=email, phonenumber=phone, password=password)
				db_session.add(new_user)  # Corrected from db_session.add(user)
				
				
				email_list=email
				return redirect(url_for('auth.otp_verification'))  # Corrected redirection
	elif type == 'signin':
		if request.method == "POST":
			email = request.form.get('email')
			password = request.form.get('password')
			user = db_session.query(UserAccount).filter_by(email=email).first()
			if user:
				if user.password == password:
					flash('Logged in successfully!',category='message')
					session['registered_user'] = user.email
					return redirect(url_for('route.home', email=session['registered_user']))
				else:
					flash("Incorrect Password, try again.",category='error')
			else:
				flash('Email does not exist.',category='error')

	return render_template('login.html', user=current_user)

@auth.route('/logout/<string:email>')
def logout(email):
	if 'registered_user' in session and session['registered_user'] == email:
		session.pop('registered_user',None)
		flash('Logged out successfully!',category='info')
	return redirect(url_for('route.home'))

@auth.route('/otp-verification/', methods=['GET', 'POST'])
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
			body=f"Welcome! To ensure the security of your account, we have sent you a One Time Password {otp} for login. Please do not share this OTP with anyone. It is valid for one session only. If you refresh the page or leave it, you will need to generate a new OTP. Thank you for helping us keep your account safe."
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
			db_session.commit()
			user = db_session.query(UserAccount).filter_by(email=email_recipient).first()
			session['registered_user'] = user.email
			flash("Registration successful!",category='info')
			flash("You have successfully created your account now please complete your profile!!!",category='info')	
			return redirect(url_for('route.user_profile', email=session['registered_user']))
		else:
			print("Incorrect")
			print(new_otp)
			print(otp)
			print(f"{digi_1} {digi_2} {digi_3} {digi_4} {digi_5} {digi_6} ")
			flash("invalid OTP entered!! try again",category='info')
			db_session.rollback()
	return render_template("otpverification.html")

@auth.route('/adminlogin', methods=['POST', 'GET'])
def admin_login():
	if 'admin_username' in session:
		# If an admin is already logged in, redirect them to the admin panel
		return redirect(url_for('route.adminpanel'))
	flash("Enter your login details",category="info")
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		admin = db_session.query(Admin).filter_by(username=username).first()

		if admin:
			if admin.password == password:
				# Store admin's ID in the session to track their login status
				session['admin_username'] = admin.username
				flash(f"{admin.username} logged in successfully!!", category='info')
				return redirect(url_for('route.adminpanel'))
			else:
				flash("Incorrect Password", category='error')
		else:
			flash("Incorrect admin details entered", category='error')

	# If the request method is GET or login failed, render the login page
	return render_template('adminlogin.html')

@auth.route('/adminlogout', methods=['GET'])
def admin_logout():
	if 'admin_username' in session :
		# If an admin is logged in, remove their session
		session.pop('admin_username', None)
		flash("Admin logged out successfully!", category='info')
	else: 
		return "you are not logged in!!!"
	
	return redirect(url_for('auth.admin_login'))

# @auth.route('/doctorlogin', methods=['POST', 'GET'])
# def doctor_login():
# 	if 'doctor_th_id' in session:
# 		# If an admin is already logged in, redirect them to the admin panel
# 		return redirect(url_for('route.doctor_dashboard',th_id = session['doctor_th_id']))

# 	if request.method == 'POST':
# 		username = request.form.get('username')
# 		password = request.form.get('password')
# 		doctor = db_session.query(TherapistLoginCredentials).filter_by(username=username).first()
# 		if doctor:
# 			if doctor.password == password:
# 				# Store doctor's ID in the session to track their login status
# 				session['doctor_th_id'] = doctor.th_id
# 				flash(f"Welcome, Dr. {doctor.username}!", category='info')
# 				return redirect(url_for('route.doctor_dashboard', th_id = doctor.th_id))  # Replace 'doctor.dashboard' with your doctor's dashboard route
# 			else:
# 				flash("Incorrect Password", category='error')
# 		else:
# 			flash("Incorrect doctor details entered", category='error')

# 	# If the request method is GET or login failed, render the doctor login page
# 	return render_template('Doctor login.html')

# @auth.route('/doctorlogout/<string:th_id>', methods=['GET'])
# def doctor_logout(th_id):
# 	if 'doctor_th_id' in session and session['doctor_th_id'] == th_id:
# 		# If an doctor is logged in, remove their session
# 		session.pop('doctor_th_id', None)
# 		flash("doctor logged out successfully!", category='info')
# 	else:
# 		return "Access Denied!!!!"
	
# 	return redirect(url_for('auth.doctor_login'))

