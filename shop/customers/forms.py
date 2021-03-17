from wtforms import Form, StringField, TextAreaField, PasswordField,SubmitField,validators, ValidationError,IntegerField
from flask_wtf.file import FileRequired,FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import Register

class CustomerRegisterForm(FlaskForm):
    name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    country = StringField('Country: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])
    zipcode = StringField('Zip code: ', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Image only please')])
    submit = SubmitField('Register')


    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")



class CustomerLoginFrom(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])


    

class Battery_form(FlaskForm):
    cust_email=StringField('Email: ', [validators.Email(), validators.DataRequired()])
    cust_phone=IntegerField('Contact: ', [validators.DataRequired()])
    battery_brand=StringField('Battery Brand: ')
    date_purchase=StringField('Date of purchase ', [validators.DataRequired()])
    cust_name=StringField('Name ', [validators.DataRequired()])
    battery_image=FileField('Upload Bill', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    battery_type=StringField('Battery type ', [validators.DataRequired()])
    submit = SubmitField('Submit')



class roadside_form(FlaskForm):
    cust_name=StringField('Name ', [validators.DataRequired()])
    car_brand=StringField('Car brand/Manufacturer ', [validators.DataRequired()])
    cust_phone=IntegerField('Contact: ', [validators.DataRequired()])
    car_number=IntegerField('Car number: ', [validators.DataRequired()])
    car_model=StringField('Car model ', [validators.DataRequired()])
    cust_location=StringField('Location', [validators.DataRequired()])
    cust_landmark=StringField('Landmark', [validators.DataRequired()])
    cust_issue=TextAreaField('Issue',[validators.DataRequired()])
    submit = SubmitField('Submit')



class reqpart_form(FlaskForm):
    cust_name=StringField('Name ', [validators.DataRequired()])
    cust_email=StringField('Email: ', [validators.Email(), validators.DataRequired()])
    cust_phone=IntegerField('Contact: ', [validators.DataRequired()])
    part=StringField('Part name ', [validators.DataRequired()])
    v_brand=StringField('Vehicle brand ', [validators.DataRequired()])
    v_model=StringField('Vehicle model ', [validators.DataRequired()])
    submit = SubmitField('Submit')


class feedback_form(FlaskForm):
    cust_name=StringField('Name ', [validators.DataRequired()])
    cust_email=StringField('Email: ', [validators.Email(), validators.DataRequired()])
    cust_phone=IntegerField('Contact: ', [validators.DataRequired()])
    res=TextAreaField('Feedback',[validators.DataRequired()])
    pro_pur=TextAreaField('Product purchased',[validators.DataRequired()])
    submit = SubmitField('Submit')


class install_ser_form(FlaskForm):
    cust_name=StringField('Name ', [validators.DataRequired()])
    cust_email=StringField('Email: ', [validators.Email(), validators.DataRequired()])
    cust_phone=IntegerField('Contact: ', [validators.DataRequired()])
    v_brand=StringField('Vehicle brand ', [validators.DataRequired()])
    v_model=StringField('Vehicle model ', [validators.DataRequired()])
    invoice=StringField('Invoice ', [validators.DataRequired()])
    submit = SubmitField('Submit')





