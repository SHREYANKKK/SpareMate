from shop import db
from datetime import datetime


class Addproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price=db.Column(db.Integer,nullable=False)
    discount=db.Column(db.Integer,default=None)
    stock=db.Column(db.Integer,nullable=False)
    origin=db.Column(db.Text,nullable=False)
    condition=db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    install_service=db.Column(db.String(10), nullable=False)
    colors=db.Column(db.Text,nullable=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=True)
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=True)
    category = db.relationship('Category',backref=db.backref('category', lazy=True))
    image_1=db.Column(db.String(150),nullable=False,default='image.jpg')
    image_2=db.Column(db.String(150),nullable=True,default='image.jpg')
    image_3=db.Column(db.String(150),nullable=True,default='image.jpg')
    certificate=db.Column(db.String(150),nullable=True)

    def __repr__(self):
        return '<Addproduct %r>' % self.name

class Brand(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=True,unique=True)


class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=True,unique=True)

class Review(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    rating=db.Column(db.Integer,nullable=False)
    review=db.Column(db.Text,nullable=False)
    category = db.Column(db.String(30),nullable=True)
    product_id = db.Column(db.Integer,nullable=True)
    user_id=db.Column(db.Integer,nullable=True)

db.create_all()
    