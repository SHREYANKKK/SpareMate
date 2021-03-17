from flask_wtf.file import FileAllowed,FileField,FileRequired
from wtforms import Form,IntegerField,BooleanField,TextAreaField,validators,StringField,DecimalField

class Addproducts(Form):
    
    
    name=StringField('',[validators.DataRequired()])
    price=IntegerField('',[validators.DataRequired()])
    discount=IntegerField('',)
    stock=IntegerField('',[validators.DataRequired()])
    origin=StringField('',[validators.DataRequired()])
    condition=StringField('',[validators.DataRequired()])
    description=TextAreaField('',[validators.DataRequired()])
    install_service=StringField('',[validators.DataRequired()])
    colors=TextAreaField('',[validators.DataRequired()],default=None)
    image_1 = FileField('', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image_2 = FileField('', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image_3 = FileField('', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    certificate = FileField('', validators=[FileAllowed(['jpg','png','gif','jpeg'])])

    

