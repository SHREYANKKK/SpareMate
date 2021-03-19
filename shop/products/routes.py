from flask import redirect ,render_template,url_for,flash,request,session,current_app
from shop import db ,app,photos
from flask_login import login_required, current_user, logout_user, login_user
from .models import Brand,Category,Addproduct,Review
from .forms import Addproducts
import secrets,os
from sqlalchemy.sql import exists
from sqlalchemy.exc import IntegrityError


@app.route("/product_page")
def product_page():
    page=request.args.get('page',1,type=int)
    products=Addproduct.query.order_by(Addproduct.id.desc()).paginate(page=page,per_page=8)
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    return render_template('products/car.html',products=products,brands=brands,categories=categories)


@app.route('/result')
def result():
    searchword = request.args.get('q')

    products = Addproduct.query.msearch(searchword, fields=['name','description'] , limit=8)
    

    return render_template('products/result.html',products=products,searchword=searchword)
    


@app.route("/product/<int:id>")
def single_page(id):

    product=Addproduct.query.get_or_404(id)
    search = product.category.name
    reviews=Review.query.filter_by(category=search).order_by(Review.rating.desc()).all()
    id_list = [r.product_id for r in reviews]
    unique_id = list(set(id_list))
    result = (
    db.session.query(Addproduct)
    .filter(Addproduct.id.in_(unique_id[0:5]))
    .all()
    )
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    return render_template('products/single_page.html',product=product,brands=brands,categories=categories,results = result)




@app.route('/brand/<int:id>')
def get_brand(id):
    get_b=Brand.query.filter_by(id=id).first_or_404()
    page=request.args.get('page',1,type=int)
    brand=Addproduct.query.filter_by(brand=get_b).paginate(page=page,per_page=8)
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    return render_template('products/car.html',brand=brand,brands=brands,categories=categories,get_b=get_b)


@app.route('/categories/<int:id>')

def get_category(id):
    page=request.args.get('page',1,type=int)
    get_cat=Category.query.filter_by(id=id).first_or_404()
    get_cat_prod=Addproduct.query.filter_by(category=get_cat).paginate(page=page,per_page=6)
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    return render_template('products/car.html',get_cat_prod=get_cat_prod, categories=categories,brands=brands,get_cat=get_cat)






@app.route('/addbrand', methods=['GET','POST'])

def addbrand():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))

    if request.method=="POST":
        try:
            getbrand=request.form.get('brand')
            brand=Brand(name=getbrand)

            if len(request.form.get('brand'))>0:
                db.session.add(brand)
                db.session.commit()

            else:
                flash('Field cannot be empty','danger')
                return redirect(url_for('addbrand'))
                
        except IntegrityError:
            db.session.rollback()
            flash(f'Brand {getbrand} already exists','danger')
            return redirect('addbrand')
        flash(f'Brand {getbrand} was added to database','success')   
        return redirect(url_for('addcat'))

        getbrand=request.form.get('brand')
        brand=Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addcat'))

    return render_template('products/addbrand.html', brands='brands')

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])

def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first','danger')

    updatebrand=Brand.query.get_or_404(id)
    brand=request.form.get('brand')
    if request.method=="POST":
        updatebrand.name=brand
        if len(updatebrand.name)>0:
            flash(f'Your brand has been updated','success')
            db.session.commit()
            return redirect(url_for('brands'))

        else:
             

            flash("Field cannot be empty",'danger')
            return redirect(url_for('brands'))
    
        flash(f'Your brand has been updated','success')
        db.session.commit()
        return redirect(url_for('brands'))
    brand = updatebrand.name
    
    return render_template('products/updatebrand.html',title='Update brand page',updatebrand=updatebrand)



@app.route('/deletebrand/<int:id>', methods=['GET','POST'])
def deletebrand(id):
   
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        flash(f"The brand {brand.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('brands'))
    
    flash(f"The brand {brand.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))

@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    if request.method=="POST":
        try:
            getcat=request.form.get('category')
            cat=Category(name=getcat)



    
            if len(request.form.get('category'))>0:
                db.session.add(cat)
                db.session.commit()

            else:
                flash('Field cannot be empty','danger')
                return redirect(url_for('addcat'))
           
        except IntegrityError:
            db.session.rollback()
            flash(f'Category {getcat} already exists','danger')
            return redirect('addcat')
        flash(f'category {getcat} was added to database','success')   
        return redirect(url_for('addproduct'))
        getcat=request.form.get('category')
        cat=Category(name=getcat)
        db.session.add(cat)
        flash(f'The category {getcat} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addproduct'))
    return render_template('products/addbrand.html')
    return render_template('products/addbrand.html', brands='brands')



@app.route('/updatecategory/<int:id>',methods=['GET','POST'])
def updatecategory(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
    updatecategory=Category.query.get_or_404(id)

    category=request.form.get('category')
    if request.method=="POST":
        
        updatecategory.name=category

        if len(updatecategory.name)>0:
            flash(f'Your category has been updated','success')
            db.session.commit()
            return redirect(url_for('category'))

        else:
            updatecategory=Category.query.get_or_404(id)

            flash("Field cannot be empty",'danger')
            return redirect(url_for('category'))
    
    return render_template('products/updatebrand.html',title='Update category page',updatecategory=updatecategory)
@app.route('/deletecat/<int:id>', methods=['GET','POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        flash(f"The category {category.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('category'))
    flash(f"The category {category.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))

@app.route('/Addproduct',methods=['GET','POST'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brands=Brand.query.all()
    categories=Category.query.all()
    form=Addproducts(request.form)
    if request.method=="POST":
        name=form.name.data
        price=form.price.data
        discount=form.discount.data
        stock=form.stock.data
        origin=form.origin.data
        condition=form.condition.data
        description=form.description.data
        install_service=form.install_service.data
        colors=form.colors.data
        brand=request.form.get('brand')
        category=request.form.get('category')
        

        #bug fix
        #if image file missing,flash message to user

        try:
            image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
            image_2=photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
            image_3=photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
            certificate=photos.save(request.files.get('certificate'),name=secrets.token_hex(10)+".")
            addpro=Addproduct(name=name,price=price,discount=discount,stock=stock,origin=origin,condition=condition,description=description,install_service= install_service,colors=colors,brand_id=brand,category_id=category,image_1=image_1,image_2=image_2,image_3=image_3,certificate=certificate)
            db.session.add(addpro)
            flash(f'The product {name} has been added to your database','success')
            db.session.commit()
            return redirect(url_for('admin'))
            

        except Exception:

            flash(f'Please attach all images','danger')
            return redirect(url_for('addproduct'))

    return render_template('products/addproduct.html',title="Add Product",form=form,brands=brands,categories=categories)

@app.route('/updateproduct/<int:id>',methods=['GET','POST'])
def updateproduct(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brands=Brand.query.all()
    categories=Category.query.all()
    product=Addproduct.query.get_or_404(id)
    brand=request.form.get('brand')
    category=request.form.get('category')
    form=Addproducts(request.form)
    if request.method=="POST":
        product.name=form.name.data
        product.price=form.price.data
        product.discount=form.discount.data
        product.stock=form.stock.data
        product.origin=form.origin.data
        product.condition=form.condition.data
        product.description=form.description.data
        product.install_service=form.install_service.data
        product.colors=form.colors.data
        product.brand_id=brand
        product.category_id=category

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_1))
                product.image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
            except:
                product.image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_2))
                product.image_1=photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
            except:
                product.image_1=photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_3))
                product.image_1=photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
            except:
                product.image_1=photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")

        if request.files.get('certificate'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.certificate))
                product.image_1=photos.save(request.files.get('certificate'),name=secrets.token_hex(10)+".")
            except:
                product.image_1=photos.save(request.files.get('certificate'),name=secrets.token_hex(10)+".")

        db.session.commit()
        flash(f'Your product has been updated','success')
        return redirect(url_for('admin'))
    form.name.data=product.name
    form.price.data=product.price
    form.discount.data=product.discount
    form.stock.data=product.stock
    form.origin.data=product.origin
    form.condition.data=product.condition
    form.description.data=product.description
    form.install_service.data=product.install_service
    form.colors.data=product.colors
    brand=request.form.get('brand')
    category=request.form.get('category')
    return render_template('products/updateproduct.html',form=form,brands=brands,categories=categories,product=product)
@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('admin'))

@app.route('/reviews/<category>/<id>', methods=['GET', 'POST'])
@login_required
def addReviews(category,id):
    if request.method=="POST":
        rating= request.form.get("rating")
        review= request.form["reviews"]
        user_id=current_user.id
    
        if len(request.form["reviews"])>0 and current_user.is_authenticated:
            addreview=Review(rating=rating,review=review,category=category,product_id=id,user_id=user_id)
            db.session.add(addreview)
            flash(f'Product review was added','success')
            db.session.commit()

        else:
            flash("Review cannot be blank",'danger')
            return redirect(url_for('single_page', id=id))

        
    return redirect(url_for('single_page', id=id))



@app.route('/adminreviews')
def reviews_admin():

   
    reviews=Review.query.order_by(Review.id).all()
    return render_template('admin/review_admin.html',title="adminreviews",reviews=reviews)






















@app.route('/about')

def about():
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    return render_template('customer/about.html',brands=brands,categories=categories)
           
@app.route('/aboutstripe')

def aboutstripe():
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    return render_template('customer/stripeabout.html',brands=brands,categories=categories)
           
