from shop import db,login_manager
from datetime import datetime
import json
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)

class Register(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50), unique= False)
    username = db.Column(db.String(50), unique= True)
    email = db.Column(db.String(50), unique= True)
    password = db.Column(db.String(200), unique= False)
    country = db.Column(db.String(50), unique= False)
    # state = db.Column(db.String(50), unique= False)
    city = db.Column(db.String(50), unique= False)
    contact = db.Column(db.String(50), unique= False)
    address = db.Column(db.String(50), unique= False)
    zipcode = db.Column(db.String(50), unique= False)
    profile = db.Column(db.String(200), unique= False , default='profile.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password_change=db.Column(db.String(200), unique= False,nullable=True)
    new_pass_confirm=db.Column(db.String(200), unique= False,nullable=True)

    def __repr__(self):
        return '<Register %r>' % self.name


class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedDict)
    

    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice



class Battery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cust_email=db.Column(db.String(20), unique=False, nullable=False)
    battery_brand=db.Column(db.String(20),nullable=False)
    date_purchase=db.Column(db.Integer, unique=False, nullable=False)
    cust_name=db.Column(db.String(20), nullable=False)
    cust_phone=db.Column(db.String(10), nullable=False)
    battery_image=db.Column(db.String(150),nullable=False,default='image.jpg')
    battery_type=db.Column(db.String(20),nullable=False)



    def __repr__(self):
        return '<Battery %r>' % self.cust_name


class roadside(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cust_name=db.Column(db.String(20), unique=False, nullable=False)
    car_brand=db.Column(db.String(20),nullable=False)
    cust_phone=db.Column(db.Integer, unique=False, nullable=False)
    car_number=db.Column(db.Integer, unique=False, nullable=False)
    car_model=db.Column(db.String(10), nullable=False)
    cust_location=db.Column(db.String(50), unique=False, nullable=False)
    cust_landmark=db.Column(db.String(50), unique=False, nullable=False)
    cust_issue=db.Column(db.String(500), unique=False, nullable=False)

    def __repr__(self):
        return '<roadside %r>' % self.cust_name


class reqpart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cust_name=db.Column(db.String(20), unique=False, nullable=False)
    cust_phone=db.Column(db.Integer, unique=False, nullable=False)
    cust_email=db.Column(db.String(20), unique=False, nullable=False)
    part=db.Column(db.String(20), unique=False, nullable=False)
    v_brand=db.Column(db.String(20),nullable=False)
    v_model=db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return '<reqpart %r>' % self.cust_name
        

class feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cust_name=db.Column(db.String(20), unique=False, nullable=False)
    cust_phone=db.Column(db.Integer, unique=False, nullable=False)
    cust_email=db.Column(db.String(20), unique=False, nullable=False)
    res=db.Column(db.String(500), unique=False, nullable=False)
    pro_pur=db.Column(db.String(20), unique=False, nullable=False)
    

    def __repr__(self):
        return '<feedback %r>' % self.cust_name


class Install_ser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cust_name=db.Column(db.String(20), unique=False, nullable=False)
    cust_phone=db.Column(db.Integer, unique=False, nullable=False)
    cust_email=db.Column(db.String(20), unique=False, nullable=False)
    v_brand=db.Column(db.String(20),nullable=False)
    v_model=db.Column(db.String(20),nullable=False)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    

    



class seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_name=db.Column(db.String(20), unique=False, nullable=False)
    seller_phone=db.Column(db.Integer, unique=False, nullable=False)
    seller_email=db.Column(db.String(20), unique=False, nullable=False)
    shop_name=db.Column(db.String(20),nullable=False)
    shop_addr=db.Column(db.String(100),nullable=False)
    services_provided = db.Column(db.String(100), unique=False, nullable=False)
    years_service=db.Column(db.Integer, unique=False, nullable=False)
    in_ser=db.Column(db.String(50), unique=False, nullable=False)
    onl_pre=db.Column(db.String(50), unique=False, nullable=False)
    est_budget=db.Column(db.String(50), unique=False, nullable=False)



    


    



    






  

db.create_all()