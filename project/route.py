from flask import render_template, request, flash, redirect, url_for, Blueprint, jsonify
from project.model import UserAccount, db_session, Contacts, Therapists
from flask_login import login_required, current_user
from flask_mail import Message
from . import mail
from project.helpers import custom_login_required
from .runchatbot import chatbot_response
# from project.forms import SignupForm
route = Blueprint('route', __name__)
# Route for the home page


@route.route('/')
@route.route('/home')
def home():
    flash("Flask app message")
    therapists = db_session.query(Therapists).all()
    return render_template('home.html', user=current_user, therapists=therapists)


# Route for the contact page
@route.route('/contact', methods=["GET", "POST"])
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
            new_contact = Contacts(name=name, phonenumber=phonenumber,
                                   email=email, dateofbirth=dateofbirth, message=msg)
            db_session.add(new_contact)
            db_session.commit()
            flash("Your message has been sent!! ")
            email_msg = Message(
                subject="Regards",
                recipients=[email],
                body=f"Thank you {name},\nWe sincerely appreciate your interest in our services. Your inquiry is important to us, and we want to assure you that our dedicated team is actively working on addressing your query. Rest assured, we are committed to providing you with the information and assistance you need promptly. Please stay tuned, as one of our team members will be reaching out to you very soon. Your satisfaction is our top priority, and we look forward to assisting you with any questions or concerns you may have. If you need immediate assistance, please don't hesitate to contact our customer support team. Thank you again for choosing us, and we value the opportunity to serve you.",
            )
            mail.send(email_msg)

    return render_template('contact.html', user=current_user)

# Route for the about page


@route.route('/about')
def about():
    return render_template('about.html', user=current_user)


@route.route('/chatbot')
def chat():
    return render_template('chatbot.html')

@route.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data['message']

    # Replace this with your bot's logic to generate a response
    bot_response = chatbot_response(user_message)

    return jsonify({'message': bot_response})
@route.route('/book/<string:th_id>')
@custom_login_required('auth.login', login_type='signin')
def book(th_id):
	therapist = db_session.query(Therapists).filter_by(th_id=th_id).first()
	return render_template('appointment_form.html',therapist=therapist)
@route.route('/book/<string:th_id>', methods=['GET', 'POST'])
@custom_login_required('auth.login', login_type='signin')
def submit_appointment(th_id):
	if request.method == 'POST':
		name = request.form['name']
		dob = request.form['dob']
		gender = request.form['gender']
		email = request.form['email']
		phone = request.form['phone']
		guardian_name = request.form['guardian-name']
		guardian_phone = request.form['guardian-phone']
		emergency_phone = request.form['emergency-phone']
		address = request.form['address']
		appointment_reason = request.form['appointment-reason']
		appointment_date = request.form['appointment-date']
		appointment_time = request.form['appointment-time']
		medical_history = request.form['medical-history']
		other_details = request.form['other-details']
		print(f"Name: {name}")
		print(f"Date of Birth: {dob}")
		print(f"Gender: {gender}")
		print(f"Email: {email}")
		print(f"Phone: {phone}")
		print(f"Guardian Name: {guardian_name}")
		print(f"Guardian Phone: {guardian_phone}")
		print(f"Emergency Phone: {emergency_phone}")
		print(f"Address: {address}")
		print(f"Appointment Reason: {appointment_reason}")
		print(f"Appointment Date: {appointment_date}")
		print(f"Appointment Time: {appointment_time}")
		print(f"Medical History: {medical_history}")
		print(f"Other Details: {other_details}")
	return "Appoinment booked successfully!!"

@route.route('/order-medicine')
def order_medicine():
	return "<h1><center>Comming Soon</center></h1>"
if __name__ == '__main__':
    app.run(debug=True)
