#!/usr/bin/env python3
"""Main applicatin where all routes will be run."""
from flask import Flask, render_template, url_for, current_app, request,
from flask import flash, session
from application.models.services import GlobalServices
import os

app = Flask(__name__)

# Set a secret key for the Flask application
app.secret_key = os.urandom(24)

# Instantiate the classes needed.
service = GlobalServices()

# Add different instances to the current_app object
app.service = service


@app.route('/')
def home():
    """Define home page."""
    return render_template('index.html')


@app.route('/buy_global_airtime', methods=['GET', 'POST'],
           strict_slashes=True)
def buy_global_airtime():
    """Buy airtime globally."""
    if request.method == 'POST':
        # Retrive Phone number from the form.
        phone_number = request.form['Phone_number']

        # lookup the product id based on user phone number.
        product_id = service.lookup_mobile_number(phone_number)

        # Store the phone number in the session
        session['phone_number'] = phone_number

        # Retrieve products based on product_it.
        products = service.get_products(product_id)
        return render_template(
            'buy_global_airtime.html',
            products=products
            )
    return render_template('buy_global_airtime.html')


@app.route('/create_transaction', methods=['GET', 'POST'], strict_slashes=True)
def create_transaction():
    """Create Transaction route and confirm."""
    print("inside the create transacion.")
    print()
    if request.method == 'POST':
       # Retrieve relevant info from the form.
        product_id = request.form['product_id']
        print("product_id: ", product_id)

        # Retrieve phone number from session.
        phone_number = session.get('phone_number')

        # Generate a unique trx_id
        trx_id = service.generate_transaction_id()

        # perform the buying of airtime.
        try:
            response = service.create_transaction(phone_number, trx_id, product_id)
            print()
            print("The class of the rsponse: ", type(response))
            print("response in create Route: ", response)
            flash("Transaction perfomed successfully.")
            return render_template('success.html', response=response)
        except Exception as e:
            flash(f"The transaction failed. please try again later. {e}")
            return e


if __name__ == '__main__':
    app.run(debug=True)
