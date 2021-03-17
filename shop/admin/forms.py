from wtforms import Form, BooleanField, StringField, PasswordField, validators,TextField,TextAreaField,SubmitField,IntegerField

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')    
class LoginForm(Form):
    email = StringField('', [validators.Length(min=6, max=35)])
    password = PasswordField('',[validators.DataRequired()])    
#add same way for other forms
class ContactForm(Form):
    name = TextField('Name',[validators.Length(min=4, max=25)])
    email = TextField("Email",[validators.Length(min=6, max=35),validators.Email()])
    subject = TextField("Subject",[validators.Length(min=4, max=100)])
    message = TextAreaField("Message",[validators.Length(min=4, max=500)])
    submit = SubmitField("Send")



class SellForm(Form):
    name = TextField('Name',[validators.Length(min=4, max=25)])
    email = TextField("Email",[validators.Length(min=6, max=35),validators.Email()])
    Shop_Address = TextField("Shop Address",[validators.Length(min=4, max=500)])
    category = TextAreaField("Category of parts",[validators.Length(max=20)])
    budget=IntegerField("what's your budget?",[validators.DataRequired()])
    question = TextAreaField("Do you provide mechanic services?",[validators.Length(max=3)])
    phone=IntegerField('Phone No.(Include STD code)',[validators.DataRequired()])
    submit = SubmitField("Send")