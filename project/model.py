from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, Session

# Create an SQLAlchemy engine for MySQL.
engine = create_engine("mysql://root:arijit@localhost/minor_project", echo=True)

# Create a declarative base class for defining models.
Base = declarative_base()

# Define your UserAccount model.
class UserAccount(Base):
    __tablename__ = 'useraccount'
    username = Column(String(255), primary_key=True)
    email = Column(String(255), nullable=False)
    phonenumber = Column(String(10), nullable=False)
    password = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<UserAccount username={self.username}>"

# Create the table in the database.
Base.metadata.create_all(bind=engine)

# Create a session to interact with the database.
db_session = Session(bind=engine)
ret = db_session.query(UserAccount).filter_by(email='annandy2002@gmail.com').first()
print(ret.email)