#!/usr/bin/env python3
"""Main applicatin where all routes will be run."""
from flask import Flask, render_template, url_for, current_app, request
from application.models.services import GlobalServices

app = Flask(__name__)

# Instantiate the classes needed.
service = GlobalServices()

# Add different instances to the current_app object
app.service = service

@app.route('/')
def home():
    """Define home page."""
    return render_template('index.html')

@app.route('/buy_global_airtime', methods=['GET', 'POST'],  strict_slashes=True)
def buy_global_airtime():
    """Buy airtime globally."""
    if request.method == 'POST':
        # Retrive Phone number from the form.
        phone_number = request.form['Phone_number']

        # lookup the product id based on user phone number.
        product_id = service.lookup_mobile_number(phone_number)

        # Retrieve products based on product_it.
        products = service.get_products(product_id)
        return render_template(
            'buy_global_airtime.html',
            products=products
            )
    return render_template('buy_global_airtime.html')

if __name__ == '__main__':
    app.run(debug=True)