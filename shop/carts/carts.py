from flask import redirect ,render_template,url_for,flash,request,session,current_app
from shop import db ,app
from shop.products.models import Addproduct,Brand,Category
from num2words import num2words 



def MergeDict(dict1,dict2):
    if isinstance(dict1 ,list) and isinstance(dict2,list):
        return dict1+dict2

    elif isinstance(dict1,dict) and isinstance(dict2,dict):

        return dict(list(dict1.items())+ list(dict2.items()))

    return False


@app.route('/addcart',methods=['POST'])

def AddCart():

    try:

        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        color = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()

        if product_id and quantity and color and request.method=="POST":
            DictItems = {product_id:{'name':product.name,'price':float(product.price),'discount':product.discount,'color':color,'quantity':quantity,'image':product.image_1, 'colors':product.colors,'colors':product.colors,'stock':product.stock}}

          

            if 'Shoppingcart'in session:
                print(session['Shoppingcart'])

                if product_id in session['Shoppingcart']:
                    print('This product is already in your cart')
                    flash('Product already exists in your cart','danger')

                if product.stock<0:
                    flash("Product is out of stock",'danger')
                    return redirect(request.referrer)


            


                else:
                    session['Shoppingcart']=MergeDict(session['Shoppingcart'],DictItems)
                    flash('Product was added to your cart','success')

                    return redirect(request.referrer)

            else:

                session['Shoppingcart']=DictItems
               
                return redirect(request.referrer)

                

            
    except Exception as e:

        print(e)

    finally:

        return redirect(request.referrer)


@app.route('/carts')

def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:

        return redirect(url_for('product_page'))
    subtotal=0
    grandtotal=0

    for key,product in session['Shoppingcart'].items():
        brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
        categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()

        discount=(product['discount']/100)*float(product['price'])
        subtotal+=float(product['price'])*int(product['quantity'])
        subtotal-=discount
        tax=("%.2f"%(.06 *float(subtotal)))
        grandtotal=float("%.2f" %(1.06 * subtotal))
        #convert to words
        to_words=(num2words(int(grandtotal), to = 'ordinal'))+" "+"only"

  

    return render_template('products/carts.html',tax=tax,grandtotal=grandtotal,to_words=to_words,brands=brands,categories=categories)


@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method =="POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key , item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item was updated','success')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))



   

   
#empty cart codee

@app.route('/empty')

def empty_cart():
    try:
        session.clear()
        flash('Entire Cart was cleared','success')
        return redirect(url_for('product_page'))

    except Exception as e:

        print(e)


@app.route('/deleteitem/<int:id>')

def deleteitem(id):

    if "Shoppingccart" not in session and len(session['Shoppingcart'])<=0:
    

        return redirect(url_for('product_page'))

    

    try:
        session.modified=True
        for key,item in session['Shoppingcart'].items():

            if int(key)==id:

                session['Shoppingcart'].pop(key,None)
                flash('Item deleted from your cart','success')
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))


    