import sys
from datetime import datetime
from flask import (
    render_template,
    g,
    redirect,
    session,
    url_for,
    request,
    current_app
)
from flask_login import current_user, login_required
from app.extensions import db, mail
from app.order import order
from app.models import (
    Cart,
    Category,
    CatalogItem,
    Order,
)
from flask_mail import Message
import uuid
import stripe


@order.before_app_request
def before_request():
    if 'cart_id' in session:
        g.cart_id = session['cart_id']
    else:
        g.cart_id = str(uuid.uuid4())
        session['cart_id'] = g.cart_id
    g.cart = Cart.query \
        .filter_by(id=g.cart_id) \
        .first()
    if g.cart is None:
        g.cart = Cart(id=g.cart_id)
        db.session.add(g.cart)


@order.route('/checkout/')
@login_required
def checkout():
    g.cart.cart_items = []
    db.session.commit()

    return redirect(url_for('order.complete'))


@order.route('/complete')
@login_required
def complete():
    categories = Category.query \
        .order_by(Category.name.desc())
    cart_items = g.cart.cart_items
    cart_quantity = sum([item.amount for item in cart_items])

    msg = Message("StationaryShop Confirmation",
                  recipients=["maikeulbgithub@gmail.com"])
    msg.html = render_template(
        'email/order_confirmation.html', user=current_user)
    mail.send(msg)
    print(current_user.email, sys.stdout)

    return render_template('order/complete.html',
                           title='Order Complete',
                           cart_quantity=cart_quantity,
                           categories=categories)


@order.route('/charge', methods=['POST'])
@login_required
def charge():
    amount = 500

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)
