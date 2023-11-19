from flask import render_template, request, flash, redirect, url_for, Blueprint, jsonify, session,Response
from project.model import UserAccount, db_session, Contacts, ImageUpload,Appointment, Doctor,Preferences
from flask_login import login_required, current_user
from flask_mail import Message
from . import mail
from project.helpers import custom_login_required
from .runchatbot import chatbot_response
import datetime
# from datetime import datetime
from PIL import Image
import io
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import jaccard_score
from sklearn.metrics.pairwise import euclidean_distances

# from project.forms import SignupForm
route = Blueprint('route', __name__)
# Route for the home page


def load_data():
	return pd.read_sql(db_session.query(Doctor).statement, db_session.bind)

@route.route('/')
@route.route('/home')
def home(email='guestuser'):
	# flash("Flask app message")
	doctors = db_session.query(Doctor).all()
	recommendations = []
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
	docids_list = []

	if 'registered_user' in session:
		now = datetime.datetime.now()
		tomorrow = now + datetime.timedelta(days=1)
		tomorrow_day_name = tomorrow.strftime("%A")
		preferences = db_session.query(Preferences).filter_by(email=session['registered_user']).all()

		if preferences:
			user_location = preferences[0].user_location
			user_preferred_days = "['Monday', 'Friday']"

			# Assuming there is only one language preference
			user_languages_spoken = [preferences[0].user_languages_spoken.strip()]

			user_specialty = [preference.user_specialty.strip() for preference in preferences]

			data = load_data()

			# Encode categorical features
			label_encoders = {}
			for column in ["specialty", "location"]:
				le = LabelEncoder()
				data[column] = le.fit_transform(data[column])
				label_encoders[column] = le

			# Convert user preferences to numerical values using label encoders
			user_specialty_encoded = label_encoders["specialty"].transform(user_specialty)
			user_location_encoded = label_encoders["location"].transform([user_location])[0]

			# Assuming there is only one language preference
			user_language_encoded = 1 if user_languages_spoken[0] in set(language for languages_list in data["languages_spoken"].apply(eval) for language in languages_list) else 0

			# Create a vector for the user's preferences
			user_vector = [user_specialty_encoded[0], user_location_encoded]

			# Check the lengths of the user-preferred days and doctor availability lists
			user_preferred_days_list = eval(user_preferred_days)
			data["availability_list"] = data["availability"].apply(eval)
			data["availability_length"] = data["availability_list"].apply(len)

			# Filter out doctors with availability lists of the same length as the user's preferred days list
			filtered_data = data[data["availability_length"] == len(user_preferred_days_list)]

			# Filter out doctors with the same location as the user's preferred location
			filtered_data = filtered_data[filtered_data["location"] == user_location_encoded]

			# Calculate Jaccard similarity between the user's preferred days and each doctor's availability
			filtered_data["jaccard_similarity"] = filtered_data["availability_list"].apply(
				lambda x: jaccard_score(user_preferred_days_list, x, average='micro')
			)

			# Features used for Euclidean distance
			distance_features = ["specialty", "location"]
			filtered_data["distance"] = euclidean_distances([user_vector], filtered_data[distance_features])[0]

			# Combine Jaccard similarity and Euclidean distance to get a combined score
			filtered_data["combined_score"] = 0.7 * (1 - filtered_data["distance"]) + 0.3 * filtered_data["jaccard_similarity"]

			# Sort the DataFrame by experience, rating, and combined score
			recommendations = filtered_data.sort_values(by=["combined_score"], ascending=[False])
			print(recommendations)
			docids = recommendations['docid']
			docids_list = docids.astype(str).tolist()

	return render_template('home.html', user=current_user,profile_image=image_url, recommendations=recommendations,doctors=doctors,docids = docids_list)


# Route for the contact page
@route.route('/contact', methods=["GET", "POST"])
def contact(email='guestuser'):
	image_record = None
	if 'registered_user' in session:
		image_record = db_session.query(ImageUpload).filter_by(email=session['registered_user']).first()
	db_session.close()
	default_image_url = url_for(
		'static', filename='img/default-avatar-icon-of-social-media-user-vector.jpg')
	if image_record:
		image_url = url_for('route.user_image', user_email=image_record.email)  # Use user.email, not image_record.email
	else:
		image_url = default_image_url
	if request.method == "POST":
		# image_record = None
		# image_record = db_session.query(ImageUpload).filter_by(email=session['registered_user']).first()
		# db_session.close()
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
	if 'registered_user' in session:
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
# # @route.route('/book/<string:docid>')
# # @custom_login_required('auth.login', login_type='signin')
# # def book(docid):
# # 	# Your code to collect user data
# # 	doctor = db_session.query(Therapists).filter_by(docid=docid).first()
# # 	# Fetch available appointment times from the schedule table


# # 	return render_template('appointment_form.html', doctor=doctor, available_times=available_times)

@route.route('/book/', methods=['GET', 'POST'])
def submit_appointment():
	docid = request.args.get('docid')
	email = request.args.get('email')
	user = db_session.query(UserAccount).filter_by(email=email).first()
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

	if 'registered_user' not in session:
		return redirect(url_for('auth.login', type='singin'))
	else:
		doctor = db_session.query(Doctor).filter_by(docid=docid).first()
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
			medical_history = request.form['medical-history']
			other_details = request.form['other-details']
			image = request.files['inputfile']
			# therapist_schedule = db_session.query(Schedule).filter_by(
			# 	docid=docid, appointment_day=appointment_date).all()
			# available_times = [str(schedule.start_time)
			# 				   for schedule in doctor_schedule]		
			
			if user:
				user.full_name = name
				user.dob = dob
				user.gender = gender
				user.phone = phone
				db_session.commit()
			
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
			new_appoinments = Appointment(email = user.email, docid = doctor.docid,appointment_date = appointment_date,appointment_reason = appointment_reason, medical_history = medical_history, other_details = other_details)
			db_session.add(new_appoinments)
			db_session.commit()
			email_msg = Message(
				subject="Appointment Booked",
				recipients=[email],
				body=f"Thank you {name},\n  You have successfull booked your appointments\n Doctor Name: {doctor.name}\nSpeciality:{doctor.specialty}\nAppointment Date:{appointment_date} \n",
			)
			mail.send(email_msg)
			print("mail send")
			return redirect(url_for('route.home', email=user.email))

				
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
		return render_template('appointment_form.html', doctor=doctor, user=user,profile_image=image_url)


# @route.route('/get_available_times/<string:docid>', methods=['GET'])
# def get_available_times(docid):
# 	appointment_date = request.args.get('appointment_date')
# 	print(appointment_date)
# 	day_of_week = datetime.datetime.strptime(
# 		appointment_date, "%Y-%m-%d").weekday()
# 	days = ['Monday', 'Tuesday', 'Wednesday',
# 			'Thursday', 'Friday', 'Saturday', 'Sunday']
# 	therapist_schedule = db_session.query(Schedule).filter_by(
# 		docid=docid, appointment_day=days[day_of_week]).all()
# 	available_times = [str(schedule.start_time)
# 					   for schedule in therapist_schedule]
# 	return jsonify(available_times=available_times)


@route.route('/order-medicine')
def order_medicine(email='guestuser'):
	image_record = None
	if 'registered_user' in session:
		image_record = db_session.query(ImageUpload).filter_by(email=session['registered_user']).first()

	db_session.close()

	default_image_url = url_for(
		'static', filename='img/default-avatar-icon-of-social-media-user-vector.jpg')

	if image_record:
		image_url = url_for('route.user_image', user_email=image_record.email)  # Use user.email, not image_record.email
	else:
		image_url = default_image_url
	return render_template('order_medicine.html',profile_image=image_url,user=current_user)


@route.route('/adminpanel')
def adminpanel():
	if 'admin_username' in session:
		doctors = db_session.query(Doctor).all()
		return render_template('admin_home.html', doctors=doctors)
	else:
		return redirect(url_for('auth.admin_login'))


@route.route('/admin-doctor-details')
def admin_doc_details():
	if 'admin_username' in session:
		doctors = db_session.query(Doctor).all()
		return render_template('doctor_details.html', doctors=doctors)
	else:
		return redirect(url_for('auth.admin_login'))


@route.route('/admin-patient-details')
def admin_patient_details():
	if 'admin_username' in session:
		doctors = db_session.query(Doctor).all()
		return render_template('patient_details.html')
	else:
		return redirect(url_for('auth.admin_login'))


# @route.route('/doctor-dashboard/<string:docid>')
# def doctor_dashboard(docid):
# 	if 'doctor_docid' in session and session['doctor_docid'] == docid:
# 		return render_template('doc_page.html', docid=docid)
# 	else:
# 		return "<h1>Access Denied!!!</h1>"


# @route.route('/doctor-appointment/<string:docid>')
# def doctor_appointment(docid):
# 	if 'doctor_docid' in session and session['doctor_docid'] == docid:
# 		return render_template('appointment_details.html', docid=docid)
# 	else:
# 		return "<h1>Access Denied!!!</h1>"


@route.route('/edit/<string:email>', methods=['GET', 'POST'])
def user_profile(email):
	if "registered_user" in session and session['registered_user'] == email:
		flash("You have successfully created your account now please complete your profile!!!",category='info')	
		flash("Available in these locations::  New Delhi, Kolkata, Chennai, Mumbai, Jaipur, Lucknow, Kanpur", category='info')
		user = db_session.query(UserAccount).filter_by(email=email).first()
		preferences = db_session.query(Preferences).filter_by(email = email).first()
		if request.method == 'POST':
			# Handle form data here
			name = request.form.get('name')
			date_of_birth = request.form.get('date_of_birth')
			gender = request.form.get('gender')
			blood_group = request.form.get('blood_group')
			email = request.form.get('email')
			user_specialt=[]
			phone = request.form.get('phonenumber')
			user_specialty = request.form['specialist']
			user_location = request.form['location']
			user_languages_spoken = request.form['languages_spoken']
			user.full_name = name
			user.dob = date_of_birth
			user.blood_group = blood_group
			user.gender = gender
			user.phonenumber = phone
			newpreferences = Preferences(email = user.email, user_specialty = user_specialty , user_languages_spoken= user_languages_spoken, user_location = user_location)
			db_session.add(newpreferences)
			db_session.commit()
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
			return redirect(url_for('route.home', email=user.email))

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


		return render_template('editprofile.html', profile_image=image_url, user=user,preferences=preferences)
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

@route.route('/go_back')
def go_back():
	if 'history' in session:
		if len(session['history']) > 1:
			session['history'].pop()
			return redirect(session['history'][-1])
	return redirect(url_for('route.home',email = session['registered_user']))
@route.route('/booked-appointments/<string:email>', methods=['GET','POST'])
def booked(email):
	if 'registered_user' in session and session['registered_user'] == email:
		user = db_session.query(UserAccount).filter_by(email=email).first()
		print(user.full_name)
		appointments = db_session.query(Appointment).filter_by(email = email).order_by(Appointment.appointment_date).all()
		doctors = db_session.query(Doctor).all()
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
		# for appointment in appointments:
		# 	print(appointment.email)
		current_date = datetime.date.today()
		return render_template('bookedappointment.html', current_date=current_date, profile_image=image_url, doctors=doctors,appointments = appointments,user=user)
	else:
		return "SORRY YOU CANNOT ACCESS TO THAT PAGE!!!!!"
@route.route("/cancel/<string:id>",methods = ['GET', 'POST'])
def cancelappo(id):
	if 'registered_user' in session:
		appointment = db_session.query(Appointment).filter_by(id=id).first()
		user = db_session.query(UserAccount).filter_by(email=appointment.email).first()
		doctor =db_session.query(Doctor).filter_by(docid=appointment.docid).first()
		email_msg = Message(
				subject="Cancel Appointment",
				recipients=[user.email],
				body=f"Your appoinment On {appointment.appointment_date} with {doctor.name}  has been canceled\n We will be pleased to served you again\n",
			)
		mail.send(email_msg)
		db_session.delete(appointment)
		db_session.commit()
		return redirect(url_for('route.booked',email=session['registered_user']))
	else:
		return "please login or signup"
@route.route('/view/<string:id>',methods=['GET','POST'])
def viewappo(id):
	if 'registered_user' in session:
		appointment = db_session.query(Appointment).filter_by(id = id).first()
		user = db_session.query(UserAccount).filter_by(email=appointment.email).first()
		doctor =db_session.query(Doctor).filter_by(docid=appointment.docid).first()
		return render_template('viewappointment.html', doctor=doctor,user = user, appointment=appointment)
	else:
		return "Please login or signup "
if __name__ == '__main__':
	app.run(debug=True)
