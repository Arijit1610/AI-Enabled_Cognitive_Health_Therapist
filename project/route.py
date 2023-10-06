from flask import render_template, request, flash, redirect, url_for,Blueprint
from project.model import UserAccount, db_session,Contacts
from flask_login import login_required, current_user
from flask_mail import Message
from . import mail 
# from project.forms import SignupForm
route = Blueprint('route',__name__)
# Route for the home page
@route.route('/')
@route.route('/home')
def home():
	flash("Flask app message")
	return render_template('home.html', user = current_user)


# Route for the contact page
@route.route('/contact',methods = ["GET", "POST"])
def contact():
	if request.method == "POST":
		name = request.form.get('name')
		phonenumber = request.form.get('phonenumber')
		email = request.form.get('email')
		dateofbirth = request.form.get('dob')
		msg = request.form.get('msg')
		if '@gmail.in' not in email and len(email) < 12:
				flash("Incorrect Email address")
		elif len(name) < 6:
				flash("Username must be greater than 3 characters", category='error')
		elif len(phonenumber) != 10:
				flash("Invalid phone number")
		else:
			new_contact = Contacts(name = name, phonenumber = phonenumber, email = email, dateofbirth = dateofbirth, message = msg)
			db_session.add(new_contact)
			db_session.commit()
			flash("Your message has been sent!! ")
			email_msg = Message(
				subject="Regards",
				recipients = [email],
				body = f"Thank you {name},\nWe sincerely appreciate your interest in our services. Your inquiry is important to us, and we want to assure you that our dedicated team is actively working on addressing your query. Rest assured, we are committed to providing you with the information and assistance you need promptly. Please stay tuned, as one of our team members will be reaching out to you very soon. Your satisfaction is our top priority, and we look forward to assisting you with any questions or concerns you may have. If you need immediate assistance, please don't hesitate to contact our customer support team. Thank you again for choosing us, and we value the opportunity to serve you.",
			)
			mail.send(email_msg)
		
	return render_template('contact.html',user = current_user)

# Route for the about page
@route.route('/about')
def about():
    return render_template('about.html',user = current_user)
