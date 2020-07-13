from FaceRecApp import db
import os



class Persons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(20), unique=False, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    dob = db.Column(db.Date())
    gender = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    sample_dir_path = db.Column(db.String(300),  nullable=False)
    noOfSamples =db.Column(db.Integer, nullable=False,default=0)

    def __repr__(self):
        return f"User('{self.fullname}', '{self.username}','{self.email}')"