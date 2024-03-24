#!/usr/bin/env python3
"""Main applicatin where all routes will be run."""
from flask import Flask, render_template, url_for, current_app, request
from flask import flash, session, redirect
from application.models.services import GlobalServices
from application.models.paypal_handler import PayPalHandler
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Set a secret key for the Flask application
app.secret_key = os.urandom(24)


# Load environment variables from the .env file
load_dotenv()

#  Retrieve Paypal credentials from environment
PAYPAL_MODE = os.getenv('PAYPAL_MODE')
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')


# Instantiate the classes needed.
service = GlobalServices()
paypal_handler = PayPalHandler(
    PAYPAL_MODE,
    PAYPAL_CLIENT_ID,
    PAYPAL_CLIENT_SECRET
)

# Add different instances to the current_app object
app.service = service
app.paypal_handler = paypal_handler


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

        # Store products in session.
        session['products'] = products
        return render_template(
            'buy_global_airtime.html',
            products=products
            )
    return render_template('buy_global_airtime.html')


@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    """
    Create a PayPal payment and redirect user to PayPal payment page.

    This route handles the initiation of a PayPal payment. It retrieves
    product and payment information from the form submitted by the user,
    creates a PayPal payment using the PayPalHandler class, and redirects
    the user to the PayPal payment page.

    Returns:
        Flask.redirect: Redirects the user to the PayPal payment page.
    """
    if request.method == 'POST':
        product_id = request.form['product_id']
        retail_price = float(request.form['retail_price'])
        transaction_fee = request.form.get('transaction_fee', None)
        destination_amount = request.form['destination_amount']
        phone_number = session.get('phone_number')

        # Store some info in session.
        session['product_id'] = product_id

        # Add the retail price and the transaction Fee.
        if transaction_fee:
            transaction_fee = float(transaction_fee)
            total = retail_price + transaction_fee
        else:
            total = retail_price

        # Create a PayPal payment
        paypal_redirect_url = paypal_handler.create_payment(
            total, 
            phone_number, 
            request
            )

        if paypal_redirect_url:
            # Redirect the user to the PayPal payment page
            return redirect(paypal_redirect_url)
        else:
            flash("Failed to create PayPal payment.")
            return redirect(url_for('home'))

@app.route('/execute_payment')
def execute_payment():
    """
    Execute PayPal payment and perform action after successful payment.

    This route is called when the user returns from PayPal after completing
    the payment. It executes the PayPal payment using the PayPalHandler class,
    and if the payment execution is successful, it credits the customer based
    on the requested service.

    Returns:
        Flask.redirect or Flask.render_template: Redirects the user to the home
        page or renders the success template based on the payment status.
    """
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')

    # Execute PayPal payment
    success, error_message = paypal_handler.execute_payment(
        payment_id, 
        payer_id
        )

    if success:
        # Retrieve the relevant info from session.
        product_id = session.get('product_id')
        phone_number = session.get('phone_number')

        # Create a unique transaction_id
        trx_id = service.generate_transaction_id()
        try:
            response = service.create_transaction(
                phone_number, 
                trx_id, 
                product_id
                )
            print("Response after sending airtime: ", response)
            flash("Transaction performed successfully.")
            return render_template('success.html', response=response)
        except Exception as e:
            flash("Something went wrong and the transaction could not be performed. ", e)
    else:
        flash(f"Failed to execute PayPal payment: {error_message}")
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
