from sqlalchemy import create_engine, Column, String, Integer, UniqueConstraint, Date, ForeignKey, Time, Boolean, BLOB, DateTime, Float, JSON
# from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import declarative_base, Session, relationship
import pandas as pd
# Create an SQLAlchemy engine for MySQL.
engine = create_engine(
    "mysql://root:arijit@localhost/minor_project", echo=True)

# Create a declarative base class for defining models.
Base = declarative_base()

# Define your UserAccount model.





class UserAccount(Base):
    __tablename__ = 'useraccountlist'
    id = Column(Integer, unique=True, autoincrement=True)
    username = Column(String(255))
    email = Column(String(255), primary_key=True, nullable=False, unique=True)
    phonenumber = Column(String(10), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    dob = Column(Date, nullable=True)
    gender = Column(String(7), nullable=True)
    blood_group = Column(String(5), nullable=True)
    full_name = Column(String(45), nullable=True)

    def __repr__(self):
        return f"<UserAccount username={self.username}>"


class Contacts(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    phonenumber = Column(String(10), nullable=False)
    email = Column(String(255), nullable=False)
    dateofbirth = Column(Date(), nullable=False)
    message = Column(String(1000), nullable=False)

    def __repr__(self):
        return f"<Contact name={self.name}>"


# class Therapists(Base):
# 	__tablename__ = 'therapists'
# 	id = Column(Integer, primary_key=True)
# 	th_id = Column(String(5), unique=True, nullable=False)
# 	th_name = Column(String(225), nullable=False)
# 	address = Column(String(225), unique=True, nullable=False)
# 	phone = Column(String(10), unique=True, nullable=False)
# 	email = Column(String(50), nullable=False)
# 	degree = Column(String(225), nullable=False)
# 	specialty = Column(String(225), nullable=False)

# 	def __repr__(self):
# 		return f"<Contact name={self.th_name}>"


# class Schedule(Base):
# 	__tablename__ = 'schedule'

# 	schedule_id = Column(Integer, primary_key=True)
# 	th_id = Column(String(5), ForeignKey('therapists.th_id'), nullable=False)
# 	appointment_day = Column(String(20), nullable=False)
# 	start_time = Column(Time, nullable=False)
# 	end_time = Column(Time, nullable=False)
# 	is_available = Column(Boolean, default=True, nullable=False)

# 	def __repr__(self):
# 		return f'Schedule(id={self.id}, th_id={self.th_id}, appointment_day={self.appointment_day}, start_time={self.start_time}, end_time={self.end_time}, is_available={self.is_available})'


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, unique=True, autoincrement=True)
    username = Column(String(20), primary_key=True)
    password = Column(String(20))

    def __repr__(self):
        return f'<username ={self.username}'


# class TherapistLoginCredentials(Base):
# 	__tablename__ = 'therapist_credentials'

# 	# Add fields for login credentials
# 	th_id = Column(String(5), ForeignKey('therapists.th_id'), nullable=False)
# 	username = Column(String(30), primary_key=True,
# 					  unique=True, nullable=False)
# 	password = Column(String(255), nullable=False)
# 	# Define a relationship with the Therapists table
# 	# therapist = relationship("Therapists", foreign_keys=[therapist_id])


class ImageUpload(Base):
    __tablename__ = 'imageuploader'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), ForeignKey(
        'useraccountlist.email'), nullable=False)
    image = Column(BLOB)


class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), ForeignKey(
        'useraccountlist.email'), nullable=False)
    docid = Column(String(10), ForeignKey('doctors.docid'), nullable=False)
    appointment_date = Column(Date, nullable=False)
    # appointment_time = Column(Time, nullable=False)
    appointment_reason = Column(String(255))
    medical_history = Column(String(1000))
    other_details = Column(String(1000))
    created_at = Column(DateTime, default=datetime.now)
    # user = relationship("UserAccount")
    # therapist = relationship("Therapists")


class Preferences(Base):
    __tablename__ = 'userpreferences'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), ForeignKey('useraccountlist.email'))
    user_specialty = Column(String(255))
    user_location = Column(String(255))
    user_languages_spoken = Column(String(255))


class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer)
    docid = Column(String(10), primary_key=True)
    name = Column(String(50))
    specialty = Column(String(50))
    phonenumber = Column(String(20))
    location = Column(String(50))
    experience_years = Column(Integer)
    patient_reviews = Column(Float)
    availability = Column(String(50))
    languages_spoken = Column(String(50))


# if __name__ == '__main__':
# Create the table in the database.
Base.metadata.create_all(bind=engine)

# Create a session to interact with the database.
db_session = Session(bind=engine)
# # ret = db_session.query(UserAccount).filter_by(email='annandy2002@gmail.com').first()
# print(ret.email)
# encoding = 'ISO-8859-1'
# data = pd.read_csv('doctors_data.csv', encoding=encoding)
# for _, row in data.iterrows():
#     doctor = Doctor(
# 		id = row['id'],
# 		docid = row['docid'],
#         name=row['name'],
#         specialty=row['specialty'],
# 		phonenumber = row['PhoneNumber'],
#         location=row['location'],
#         experience_years=row['experience_years'],
#         patient_reviews=row['patient_reviews'],
#         availability=row['availability'],
#         languages_spoken=row['languages_spoken']
#     )
#     db_session.add(doctor)

# db_session.commit()
