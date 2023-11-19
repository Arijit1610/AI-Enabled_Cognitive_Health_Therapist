from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import jaccard_score
from sklearn.metrics.pairwise import euclidean_distances

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doctors.db'
db = SQLAlchemy(app)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    specialty = db.Column(db.String(50))
    location = db.Column(db.String(50))
    experience_years = db.Column(db.Integer)
    patient_reviews = db.Column(db.Float)
    availability = db.Column(db.String(50))
    languages_spoken = db.Column(db.String(50))

encoding = 'ISO-8859-1'
data = pd.read_csv('doctors_data.csv', encoding=encoding)

# Encode categorical features
label_encoders = {}
for column in ["specialty", "location", "languages_spoken"]:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

# Store data in the database
db.create_all()
for _, row in data.iterrows():
    doctor = Doctor(
        name=row['name'],
        specialty=row['specialty'],
        location=row['location'],
        experience_years=row['experience_years'],
        patient_reviews=row['patient_reviews'],
        availability=row['availability'],
        languages_spoken=row['languages_spoken']
    )
    db.session.add(doctor)

db.session.commit()
