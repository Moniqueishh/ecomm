from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from .forms import CreateProductForm, UpdateProductForm
from ..models import Product

ig = Blueprint('ig', __name__, template_folder='ig_templates')

@ig.route('/store')
# @login_required
def store():
    # product = Product.query.order_by(Product.date_created).all()[::-1]
    # print(product)
    return render_template('store.html')

@ig.route('/cart')
# @login_required
def cart():
    # product = Product.query.order_by(Product.date_created).all()[::-1]
    # print(product)
    return render_template('cart.html')


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


@ig.route('/product/<int:product_id>')
def indProduct(product_id):
    product = Product.query.get(product_id)
    if product:
        return render_template('product.html', p=product)
    else:
        return redirect(url_for('ig.store'))
    
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