from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from .forms import CreateProductForm, UpdateProductForm
from ..models import Product, User

ig = Blueprint('ig', __name__, template_folder='ig_templates')

@ig.route('/store')
# @login_required
def store():
    product = Product.query.order_by(Product.date_created).all()

    # product = Product.query.order_by(Product.date_created).all()[::-1]
    # print(product)
    return render_template('store.html', product=product)

@ig.route('/cart')
# @login_required
def cart():
    c_list= current_user.carts.all()
    # product = Product.query.order_by(Product.date_created).all()[::-1]
    # print(product)
    return render_template('cart.html', c=c_list, user=current_user)


@ig.route('/product/create', methods=['GET', 'POST'])
@login_required
def createItem():
    form = CreateProductForm()
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            body = form.body.data

            new = Product(title, img_url, body, current_user.id)
            new.saveProduct()
            print('NEW Product MADE!!!!')
            return redirect(url_for('homePage'))

    return render_template('create_product.html', form=form)


@ig.route('/product')
def indProduct():
    product = Product.query.order_by(Product.date_created).all()
    # if product:
    return render_template('product.html', product=product)
    # else:
    #     return redirect(url_for('ig.store'), product_id=product_id)

@ig.route('/iproduct/<int:product_id>')
def indPost(product_id):
    product = Product.query.get(product_id)
    my_p = current_user.carts.all()
    if product:
        return render_template('iproduct.html', p=product, my_p=my_p)
    else:
        return redirect(url_for('ig.indProduct'))
    # if product in my_p:
    #     current_user.addCart(product)
    #     flash(f"Succesfully caught!", category='success')
    # return redirect(url_for('ig.indPost', product_id=product_id) )
    
@ig.route('/product/update/<int:product_id>', methods=['GET', 'POST'])
def updateProduct(product_id):
    product = Product.query.get(product_id)
    if product.product_id != current_user.id:
        flash('Hey buddy, this is not yours to modify!')
        return redirect(url_for('ig.store'))

    form = UpdateProductForm()
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            body = form.body.data

            product.title = title
            product.img_url = img_url
            product.body = body
            print(product.title, product.body)
            product.saveChanges()

            return redirect(url_for('ig.indproduct', product_id=product.id))

    return render_template('update_product.html', form=form, product=product)

@ig.route('/product/delete/<int:product_id>')
def deletePost(product_id):
    product = Product.query.get(product_id)
    if product.user_id == current_user.id:
        product.deleteProduct()
    else:
        print("You cannot delete a post that isn't yours")
    return redirect(url_for('ig.store'))

@ig.route('/posts/like/<int:product_id>')
@login_required
def addP(product_id):
    product= Product.query.get(product_id)
    my_p = current_user.carts.all()
    print(my_p)
    if product in my_p:
        flash(f"This item is already in your cart!", category='warning')
    else:
        current_user.addCart(product)
        flash(f"Succesfully caught!", category='success')
    return redirect(url_for('ig.cart') )

@ig.route('/remove/<int:product_id>')
@login_required
def releaseP(product_id):
    product= Product.query.get(product_id)
    my_p = current_user.carts.all()
    if product in my_p:
        current_user.unCart(product)
        flash(f"Succesfully caught!", category='success')
    return redirect(url_for('ig.cart', product=product) )

@ig.route('/clear/<int:user_id>')
@login_required
def clearP(user_id):
    if current_user.id == user_id:
        current_user.clearCart()
    flash(f"Succesfully caught!", category='success')
    return redirect(url_for('ig.cart', user=current_user))

# @ig.route('/clear/<int:product_id>')
# @login_required
# def clearP(product_id):
#     user= User.query.get(product_id)
#     my_c = current_user.carts.all()
#     if user in my_c:
#             current_user.clearCart(user_id)
#     flash(f"Succesfully caught!", category='success')
#     return redirect(url_for('ig.cart', user=user))