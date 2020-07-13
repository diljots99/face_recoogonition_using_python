from flask_wtf import FlaskForm
from wtforms import  StringField,PasswordField,SubmitField,DateField,SelectField
from wtforms.validators import  DataRequired,Length,Email,EqualTo,ValidationError
import email_validator
from FaceRecApp.models import Persons

class AddNewFace(FlaskForm):
    fullName = StringField("Full Name",
                validators=[DataRequired(),Length(min=1,max=50)])
    
    username = StringField("User Name",
                validators=[DataRequired(),Length(min=1,max=50)])

    dob = DateField("Date Of Birth",format='%d-%m-%Y',description="dd-mm-YYYY")
                
    email = StringField('Email',validators=[DataRequired(),Email()])

    gender = SelectField("Gender",choices=[("Male","Male"),("Female","Female"),("Other","Other")])

    password = PasswordField("Password",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])

    submit = SubmitField("Add Face")

    def validate_username(self,username):
        person = Persons.query.filter_by(username=username.data).first()

        if person:
            raise ValidationError('Username already is taken, Please try another username')



    def validate_email(self,email):
        person = Persons.query.filter_by(email=email.data).first()

        if person:
            raise ValidationError('E-Mail already is taken, Please try another email')