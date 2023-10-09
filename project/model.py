from sqlalchemy import create_engine, Column, String, Integer,UniqueConstraint,Date
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

# Create the table in the database.
Base.metadata.create_all(bind=engine)

# Create a session to interact with the database.
db_session = Session(bind=engine)
# # ret = db_session.query(UserAccount).filter_by(email='annandy2002@gmail.com').first()
# print(ret.email)