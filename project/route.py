from flask import render_template, request, flash, redirect, url_for, Blueprint, jsonify, session,Response
from project.model import UserAccount, db_session, Contacts, Therapists, Schedule, ImageUpload
from flask_login import login_required, current_user
from flask_mail import Message
from . import mail
from project.helpers import custom_login_required
from .runchatbot import chatbot_response
import datetime
from PIL import Image
import io
# from project.forms import SignupForm
route = Blueprint('route', __name__)
# Route for the home page


@route.route('/')
@route.route('/home')
def home(email='guestuser'):
	# flash("Flask app message")
	therapists = db_session.query(Therapists).all()

	# Create a dictionary to store appointment days for each therapist
	therapist_appointment_days = {}
	# email='h'
	for therapist in therapists:
		schedule = db_session.query(Schedule.appointment_day).filter(
			Schedule.th_id == therapist.th_id).distinct().all()
		therapist_appointment_days[therapist.th_id] = [
			day.appointment_day for day in schedule]
	image_record = None
	default_image_url = url_for(
		'static', filename='img/default-avatar-icon-of-social-media-user-vector.jpg')
	try:
		image_record = db_session.query(ImageUpload).filter_by(email=session['registered_user']).first()

		db_session.close()


		if image_record:
			image_url = url_for('route.user_image', user_email=image_record.email)  # Use user.email, not image_record.email
		else:
			image_url = default_image_url
	except:
		image_url = default_image_url

	return render_template('home.html', user=current_user,profile_image=image_url, therapists=therapists, therapist_appointment_days=therapist_appointment_days)


# Route for the contact page
@route.route('/contact', methods=["GET", "POST"])
def contact(email='guestuser'):
	image_record = None
	image_record = db_session.query(ImageUpload).filter_by(email=session['registered_user']).first()
	db_session.close()
	default_image_url = url_for(
		'static', filename='img/default-avatar-icon-of-social-media-user-vector.jpg')
	if image_record:
		image_url = url_for('route.user_image', user_email=image_record.email)  # Use user.email, not image_record.email
	else:
		image_url = default_image_url
	if request.method == "POST":
		image_record = None
		image_record = db_session.query(ImageUpload).filter_by(email=session['registered_user']).first()
		db_session.close()
		default_image_url = url_for(
			'static', filename='img/default-avatar-icon-of-social-media-user-vector.jpg')
		if image_record:
			image_url = url_for('route.user_image', user_email=image_record.email)  # Use user.email, not image_record.email
		else:
			image_url = default_image_url
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
	

	return render_template('contact.html', user=current_user,profile_image=image_url)

# Route for the about page


@route.route('/about')
def about(email='guestuser'):
	image_record = None

	image_record = db_session.query(ImageUpload).filter_by(email=session['registered_user']).first()

	db_session.close()

	default_image_url = url_for(
		'static', filename='img/default-avatar-icon-of-social-media-user-vector.jpg')

	if image_record:
		image_url = url_for('route.user_image', user_email=image_record.email)  # Use user.email, not image_record.email
	else:
		image_url = default_image_url
	return render_template('about.html', user=current_user,profile_image=image_url)


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
# @route.route('/book/<string:th_id>')
# @custom_login_required('auth.login', login_type='signin')
# def book(th_id):
# 	# Your code to collect user data
# 	therapist = db_session.query(Therapists).filter_by(th_id=th_id).first()
# 	# Fetch available appointment times from the schedule table


# 	return render_template('appointment_form.html', therapist=therapist, available_times=available_times)

@route.route('/book/<string:th_id>', methods=['GET', 'POST'])
def submit_appointment(th_id):
	if 'registered_user' not in session:
		return redirect(url_for('auth.login', type='singin'))
	else:
		therapist = db_session.query(Therapists).filter_by(th_id=th_id).first()
		available_times = []
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

			therapist_schedule = db_session.query(Schedule).filter_by(
				th_id=th_id, appointment_day=appointment_date).all()
			available_times = [str(schedule.start_time)
							   for schedule in therapist_schedule]
			# print(f"Name: {name}")
			# print(f"Date of Birth: {dob}")
			# print(f"Gender: {gender}")
			# print(f"Email: {email}")
			# print(f"Phone: {phone}")
			# print(f"Guardian Name: {guardian_name}")
			# print(f"Guardian Phone: {guardian_phone}")
			# print(f"Emergency Phone: {emergency_phone}")
			# print(f"Address: {address}")
			# print(f"Appointment Reason: {appointment_reason}")
			# print(f"Appointment Date: {appointment_date}")
			# print(f"Appointment Time: {appointment_time}")
			# print(f"Medical History: {medical_history}")
			# print(f"Other Details: {other_details}")
		# return "Appoinment booked successfully!!"
		return render_template('appointment_form.html', therapist=therapist, available_times=available_times)


@route.route('/get_available_times/<string:th_id>', methods=['GET'])
def get_available_times(th_id):
	appointment_date = request.args.get('appointment_date')
	print(appointment_date)
	day_of_week = datetime.datetime.strptime(
		appointment_date, "%Y-%m-%d").weekday()
	days = ['Monday', 'Tuesday', 'Wednesday',
			'Thursday', 'Friday', 'Saturday', 'Sunday']
	therapist_schedule = db_session.query(Schedule).filter_by(
		th_id=th_id, appointment_day=days[day_of_week]).all()
	available_times = [str(schedule.start_time)
					   for schedule in therapist_schedule]
	return jsonify(available_times=available_times)


@route.route('/order-medicine')
def order_medicine(email='guestuser'):
	image_record = None

	image_record = db_session.query(ImageUpload).filter_by(email=session['registered_user']).first()

	db_session.close()

	default_image_url = url_for(
		'static', filename='img/default-avatar-icon-of-social-media-user-vector.jpg')

	if image_record:
		image_url = url_for('route.user_image', user_email=image_record.email)  # Use user.email, not image_record.email
	else:
		image_url = default_image_url
	return render_template('order_medicine.html',profile_image=image_url)


@route.route('/adminpanel')
def adminpanel():
	if 'admin_username' in session:
		therapists = db_session.query(Therapists).all()
		return render_template('admin_home.html', therapists=therapists)
	else:
		return redirect(url_for('auth.admin_login'))


@route.route('/admin-doctor-details')
def admin_doc_details():
	if 'admin_username' in session:
		therapists = db_session.query(Therapists).all()
		return render_template('doctor_details.html', therapists=therapists)
	else:
		return redirect(url_for('auth.admin_login'))


@route.route('/admin-patient-details')
def admin_patient_details():
	if 'admin_username' in session:
		therapists = db_session.query(Therapists).all()
		return render_template('patient_details.html')
	else:
		return redirect(url_for('auth.admin_login'))


@route.route('/doctor-dashboard/<string:th_id>')
def doctor_dashboard(th_id):
	if 'doctor_th_id' in session and session['doctor_th_id'] == th_id:
		return render_template('doc_page.html', th_id=th_id)
	else:
		return "<h1>Access Denied!!!</h1>"


@route.route('/doctor-appointment/<string:th_id>')
def doctor_appointment(th_id):
	if 'doctor_th_id' in session and session['doctor_th_id'] == th_id:
		return render_template('appointment_details.html', th_id=th_id)
	else:
		return "<h1>Access Denied!!!</h1>"


@route.route('/edit/<string:email>', methods=['GET', 'POST'])
def user_profile(email):
	if "registered_user" in session and session['registered_user'] == email:			
		user = db_session.query(UserAccount).filter_by(email=email).first()
		if request.method == 'POST':
			# Handle form data here
			name = request.form.get('name')
			date_of_birth = request.form.get('date_of_birth')
			gender = request.form.get('gender')
			blood_group = request.form.get('blood_group')
			email = request.form.get('email')
			phone = request.form.get('phone')
			user.username = name
			user.dob = date_of_birth
			user.blood_group = blood_group
			user.gender = gender
			user.phonenumber = phone
			# Handle image upload here
			image = request.files['inputfile']
			if image.filename != '':
				# Read the uploaded image
				img_data = image.read()

				# Compress the image using Pillow
				img = Image.open(io.BytesIO(img_data))

				# Resize and save the image with compression
				img = img.resize((500, 500))  # Adjust the size as needed
				img_data_compressed = io.BytesIO()
				# Adjust the format and quality as needed
				img.save(img_data_compressed, format='JPEG', quality=70)

				# Check if the user exists in the database
				if user:
					# Save the compressed image to the database
					image_record = db_session.query(
				ImageUpload).filter_by(email=user.email).first()
					db_session.commit()
					if image_record:
						image_record.image=img_data_compressed.getvalue()
					else:
						new_img = ImageUpload(
							image=img_data_compressed.getvalue(), email=user.email)
						db_session.add(new_img)
					db_session.commit()
			db_session.commit()
			# Redirect to the user's profile page or a success page
			return redirect(url_for('route.user_profile', email=user.email))

		# Render the edit profile form
		image_record = None

		if user:
			image_record = db_session.query(
				ImageUpload).filter_by(email=user.email).first()

		db_session.close()

		default_image_url = url_for(
			'static', filename='img/default-avatar-icon-of-social-media-user-vector.jpg')

		if image_record:
			image_url = url_for('route.user_image', user_email=email)  # Use user.email, not image_record.email
		else:
			image_url = default_image_url


		return render_template('editprofile.html', profile_image=image_url, user=user)
	else:
		return "Invalid Request"

@route.route('/user_image/<string:user_email>')
def user_image(user_email):
    user = db_session.query(UserAccount).filter_by(email=user_email).first()
    image_record = db_session.query(ImageUpload).filter_by(email=user.email).first()
    db_session.close()

    if image_record:
        return Response(image_record.image, content_type='image/jpeg')
    else:
        default_image = open('static/img/default-avatar-icon-of-social-media-user-vector.jpg', 'rb').read()
        return default_image



if __name__ == '__main__':
	app.run(debug=True)
