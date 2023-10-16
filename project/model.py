from sqlalchemy import create_engine, Column, String, Integer,UniqueConstraint,Date,ForeignKey,Time,Boolean
from flask_login import UserMixin
from sqlalchemy.orm import declarative_base, Session

# Create an SQLAlchemy engine for MySQL.
engine = create_engine("mysql://root:arijit@localhost/minor_project", echo=True)

# Create a declarative base class for defining models.
Base = declarative_base()

# Define your UserAccount model.
class UserAccount(Base, UserMixin):
	__tablename__ = 'useraccountlist'
	id = Column(Integer,unique = True,autoincrement=True)
	username = Column(String(255))
	email = Column(String(255),primary_key=True, nullable=False,unique=True)
	phonenumber = Column(String(10), nullable=False,unique=True)
	password = Column(String(255), nullable=False)

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

class Therapists(Base):
	__tablename__= 'therapists'
	id = Column(Integer, primary_key=True)
	th_id = Column(String(5), unique=True, nullable=False)
	th_name = Column(String(225), nullable=False)
	address = Column(String(225),unique=True, nullable=False)
	phone = Column(String(10),unique=True, nullable=False)
	email = Column(String(50), nullable=False)
	degree = Column(String(225), nullable=False)
	specialty = Column(String(225), nullable=False)

	def __repr__(self):
		return f"<Contact name={self.th_name}>"

class Schedule(Base):
	__tablename__ = 'schedule'

	schedule_id = Column(Integer, primary_key=True)
	th_id = Column(String(5),ForeignKey('therapists.th_id'), nullable=False)
	appointment_day = Column(String(20), nullable=False)
	start_time = Column(Time, nullable=False)
	end_time = Column(Time, nullable=False)
	is_available = Column(Boolean, default=True, nullable=False)

	def __repr__(self):
		return f'Schedule(id={self.id}, th_id={self.th_id}, appointment_day={self.appointment_day}, start_time={self.start_time}, end_time={self.end_time}, is_available={self.is_available})'


class Admin(Base,UserMixin):
	__tablename__ = 'admins'
	id = Column(Integer,unique = True,autoincrement=True)
	username = Column(String(20),primary_key=True)
	password = Column(String(20))

	def __repr__(self):
		return f'<username ={self.username}'

class TherapistLoginCredentials(Base):
	__tablename__ = 'therapist_credentials'

	# Add fields for login credentials
	th_id = Column(String(5),ForeignKey('therapists.th_id'), nullable=False)
	username = Column(String(30), primary_key=True,unique=True, nullable=False)
	password = Column(String(255), nullable=False)
	# Define a relationship with the Therapists table
	# therapist = relationship("Therapists", foreign_keys=[therapist_id])

if __name__ == '__main__':
# Create the table in the database.
	Base.metadata.create_all(bind=engine)

# Create a session to interact with the database.
db_session = Session(bind=engine)
# # ret = db_session.query(UserAccount).filter_by(email='annandy2002@gmail.com').first()
# print(ret.email)