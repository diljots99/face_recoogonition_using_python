from flask_wtf import FlaskForm
from wtforms import  StringField,PasswordField,SubmitField,DateField
from wtforms.validators import  DataRequired,Length,Email,EqualTo
import email_validator
class AddNewFace(FlaskForm):
    fullName = StringField("Full Name",
                validators=[DataRequired(),Length(min=1,max=50)])
    
    dob = DateField("Date Of Birth",format='%d-%m-%Y',description="dd-mm-YYYY")
                
    email = StringField('Email',validators=[DataRequired(),Email()])

    password = PasswordField("Password",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])

    submit = SubmitField("Add Face")
