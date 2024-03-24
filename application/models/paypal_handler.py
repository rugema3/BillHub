"""
paypal_handler.py

This module provides a class for handling PayPal payments.

"""

import paypalrestsdk
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()


class PayPalHandler:
    def __init__(self, mode, client_id, client_secret):
        """
        Initialize the PayPalHandler class.
        """
        paypalrestsdk.configure({
            "mode": os.getenv("PAYPAL_MODE"),
            "client_id": os.getenv("PAYPAL_CLIENT_ID"),
            "client_secret": os.getenv("PAYPAL_CLIENT_SECRET")
        })

    def create_payment(self, usd_amount, customer_msisdn, request):
        """
        Create a PayPal payment.

        Args:
            usd_amount (float): The amount of the payment in USD.
            customer_msisdn (str): The customer's mobile phone number.
            request (flask.Request): The Flask request object to access
                                        host and port information.

        Returns:
            str: The PayPal redirect URL for the created payment.
                 Returns None if the payment creation fails.
        """
        host = request.host
        return_url = (
                f"http://{host}/execute_payment?"
                f"customer_msisdn={customer_msisdn}&"
                f"amount={str(usd_amount)}"
                )
        cancel_url = f"http://{host}/cancel_payment"

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": str(usd_amount),
                    "currency": "USD"
                }
            }],
            "redirect_urls": {
                "return_url": return_url,
                "cancel_url": cancel_url
            }
        })

        if payment.create():
            for link in payment.links:
                if link.method == "REDIRECT":
                    return str(link.href)

        return None

    def execute_payment(self, payment_id, payer_id):
        """
        Execute a PayPal payment.

        Args:
            payment_id (str): The PayPal payment ID.
            payer_id (str): The PayPal payer ID.

        Returns:
            tuple: A tuple containing a boolean indicating whether the payment
                    execution was successful (True for success,
                    False for failure)
                   and an optional error message as a string
                   (None if the payment was successful).
        """
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            return True, None
        else:
            return False, str(payment.error)
