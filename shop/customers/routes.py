from flask import render_template,session, request,redirect,url_for,flash,current_app,jsonify
from shop import app,db,photos,brcypt
from .forms import CustomerRegisterForm,CustomerLoginFrom,Battery_form,roadside_form,reqpart_form,feedback_form,install_ser_form,seller_form
from flask_login import login_required, current_user, logout_user, login_user,current_user
from .models import Register,Battery,CustomerOrder,roadside,reqpart,feedback,Install_ser,seller
from shop.products.models import Brand,Category,Addproduct
from shop.products.forms import Addproducts
import secrets
import os 
import json
import pdfkit
import requests
import stripe

publishable_key='pk_test_51IW275F3uPaIHCIbrtZOdk8KUASeIxEzAl2T1wVg4fVP6uVxlN5BThqkYjqqfxAUzKdatK6VGJsNButwSPUCEl6Y00YN7cZP4H'

stripe.api_key ='sk_test_51IW275F3uPaIHCIb9hukHNYJp29XRt4FLxJ3LCDeNW0LZC7lrbMxqL4hFyWzj49eqGrLRfbeA6YDBImqw4ELyJtH00njkyxOxh'


@app.route('/payment',methods=['POST'])
@login_required
def payment():
    invoice=request.form.get('invoice')
    amount=request.form.get('amount')

    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
)

    charge = stripe.Charge.create(
        customer=customer.id,
        description='SpareMate',
        amount=amount,
        currency='inr',
)
    orders = CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()

    orders.status="Paid"

    db.session.commit()
    return redirect(url_for('thanks'))



@app.route('/thanks')
def thanks():
    return render_template('customer/thank.html')

@app.route('/thanks')
def thanks_cod():
    return render_template('customer/thank.html')













@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password=brcypt.generate_password_hash(form.password.data).decode('utf-8')
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,country=form.country.data, city=form.city.data,contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form,brands=brands,categories=categories)





@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and brcypt.check_password_hash(user.password,form.password.data):

            login_user(user)
            flash(f'You are logged in', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('product_page'))
        flash(f'Incorrect email and password','danger')
        return redirect(url_for('customerLogin'))
            
    return render_template('customer/login.html', form=form,brands=brands,categories=categories)


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('customerLogin'))







# remove unwanted details from shoppingcart

def updateshoppingcart():

    for _key,product in session['Shoppingcart'].items():
        session.modified=True

        del product['image']
        del product['colors']


    return updateshoppingcart


@app.route('/getorder')
@login_required
def get_order():
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        updateshoppingcart()

        try:
            order = CustomerOrder(invoice=invoice,customer_id=customer_id,orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Proceed with payment','success')
            return redirect(url_for('orders',invoice=invoice,brands=brands,categories=categories))
        except Exception as e:
            print(e)
            flash('Something went wrong while getting your order', 'danger')
            return redirect(url_for('getCart'))


@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
            tax = ("%.2f" % (.06 * float(subTotal)))
            grandTotal = ("%.2f" % (1.06 * float(subTotal)))

    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', invoice=invoice, tax=tax,subTotal=subTotal,grandTotal=grandTotal,customer=customer,orders=orders,brands=brands,categories=categories)



@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        if request.method =="POST":
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
                tax = ("%.2f" % (.06 * float(subTotal)))
                grandTotal = float("%.2f" % (1.06 * subTotal))

            rendered =  render_template('customer/pdf.html', invoice=invoice, tax=tax,grandTotal=grandTotal,customer=customer,orders=orders)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type'] ='application/pdf'
            response.headers['content-Disposition'] ='inline; filename='+invoice+'.pdf'
            return response
    return request(url_for('orders'))

@app.route('/batteryexchange',methods=['GET','POST'])
def bat_exchange():
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    form =Battery_form()
    if form.validate_on_submit():
        battery=Battery(cust_email=form.cust_email.data,battery_brand=form.battery_brand.data,date_purchase=form.date_purchase.data,cust_name=form.cust_name.data,battery_image=form.battery_image.data,battery_type=form.battery_type.data,cust_phone=form.cust_phone.data)
        db.session.add(battery)
        flash(f'Your information is submitted', 'success')
        db.session.commit()
        return redirect('product_page')
    return render_template('customer/bat.html', form=form,brands=brands,categories=categories)





@app.route('/roadsideassistance',methods=['GET','POST'])
def road_assistance():
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    form=roadside_form()
    if form.validate_on_submit():
        Roadside=roadside(cust_name=form.cust_name.data,car_brand=form.car_brand.data,cust_phone=form.cust_phone.data,car_number=form.car_number.data,car_model=form.car_model.data,cust_location=form.cust_location.data,cust_landmark=form.cust_location.data,cust_issue=form.cust_issue.data)
        db.session.add(Roadside)
        flash(f'Your information is submitted', 'success')
        db.session.commit()
        return redirect('product_page')
    return render_template('customer/roadside.html', form=form,brands=brands,categories=categories)
        
   


@app.route('/reqpart',methods=['GET','POST'])
def req_part():
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    form=reqpart_form()
    if form.validate_on_submit():
        Reqpart=reqpart(cust_name=form.cust_name.data,cust_email=form.cust_email.data,cust_phone=form.cust_phone.data,part=form.part.data,v_brand=form.v_brand.data,v_model=form.v_model.data)
        db.session.add(Reqpart)
        flash(f'Your request for part was submitted','success')
        db.session.commit()
        return redirect('product_page')

    return render_template('customer/reqpart.html', form=form,brands=brands,categories=categories)


@app.route('/feedback',methods=['GET','POST'])
def feed_back():
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    form=feedback_form()
    if form.validate_on_submit():
        Feedback=feedback(cust_name=form.cust_name.data,cust_email=form.cust_email.data,cust_phone=form.cust_phone.data,res=form.res.data,pro_pur=form.pro_pur.data)
        db.session.add(Feedback)
        flash(f'Your feedback was submitted','success')
        db.session.commit()
        return redirect('product_page')

    return render_template('customer/feedback.html', form=form,brands=brands,categories=categories)



@app.route('/Installation',methods=['GET','POST'])
def install_services():
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    form=install_ser_form()
    if form.validate_on_submit():
        In_ser=Install_ser(cust_name=form.cust_name.data,cust_email=form.cust_email.data,cust_phone=form.cust_phone.data,v_brand=form.v_brand.data,v_model=form.v_model.data,invoice=form.invoice.data)
        db.session.add(In_ser)
        flash(f'Your request for installation was recieved,our representative will contact you shortly','success')
        db.session.commit()
        return redirect('product_page')

    return render_template('customer/install.html', form=form,brands=brands,categories=categories)

@app.route('/Privacy',methods=['GET','POST'])
def privacy_policy():

    return render_template('customer/policy.html')


@app.route('/Installpolicy',methods=['GET','POST'])
def install_policy():

    return render_template('customer/install_policy.html')


@app.route('/quality',methods=['GET','POST'])
def quality_assurance():

    return render_template('customer/quality.html')





@app.route('/seller',methods=['GET','POST'])
def sell_page():
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    form=seller_form()
    if form.validate_on_submit():
        sell_form=seller_form(seller_name=form.seller_name.data,seller_email=form.seller_email.data,seller_phone=form.seller_phone.data,shop_name=form.shop_name.data,shop_adde=form.shop_addr.data,services_provided=form.services_provided.data,years_service=form.years_service.data,in_ser=form.in_ser,onl_pre=form.onl_pre.data,est_budget=form.est_budget.data)
        db.session.add(sell_form)
        flash(f'Thank you for showing your intrest in selling with us,we will contact you shortly','success')
        db.session.commit()
        return redirect('product_page')

    return render_template('customer/seller.html', form=form,brands=brands,categories=categories)



