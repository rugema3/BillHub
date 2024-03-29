"""Define Services module.

This module contains a class with different methods
handling a couple of operations regarding the operations of the services.
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import json
import uuid
import time

# Load environment variables from the .env file
load_dotenv()


class GlobalServices:
    """Define GlobalServices class.

    A class to handle various global services, such as mobile number lookup,
    listing operators, listing products, etc.
    """

    def __init__(self):
        """Initialize the GlobalServices instance.

        To be initialized with the base URL of the API
        and authentication credentials retrieved from environment variables.
        """
        base_url = os.getenv("BASE_URL")
        username = os.getenv("services_username")
        password = os.getenv("services_password")

        if not base_url:
            raise ValueError("BASE_URL environment variable is not set.")
        if not username:
            raise ValueError("USERNAME environment variable is not set.")
        if not password:
            raise ValueError("PASSWORD environment variable is not set.")

        self.base_url = base_url.rstrip('/')
        self.auth = HTTPBasicAuth(username, password)

    def _make_get_request(self, endpoint, params=None):
        """Make a GET request to the specified endpoint."""
        url = f"{self.base_url}/{endpoint}"
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                auth=self.auth
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error occurred during GET request: {e}")
            return None

    def _make_post_request(self, method, endpoint, payload=None):
        """Authenticate requests.

        Makes an HTTP request to the specified endpoint with the given method,
        payload, and authentication.

        Args:
            method (str): The HTTP method ("GET", "POST", "PUT", "DELETE")
            endpoint (str): The endpoint URL.
            payload (dict, optional): The data to include in the request.

        Returns:
            dict or None: The JSON response from the server,
                            or None if an error occurs.
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.request(
                method,
                url,
                json=payload,
                headers=headers,
                auth=self.auth
                )
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None

    def lookup_mobile_number(self, mobile_number):
        """
        Perform a lookup for the given mobile number using the Dtone API.

        Args:
            mobile_number (str): The mobile number to lookup.

        Returns:
            Operator_id(int): The Operator ID that identifies the operator.
        """
        endpoint = "lookup/mobile-number"
        payload = {
            "mobile_number": mobile_number,
            "page": 1,
            "per_page": 50
        }
        try:
            result = self._make_post_request("POST", endpoint, payload)
            print("Inside Try brock")
            for item in result:
                if item.get('identified'):
                    operator_id = item.get('id')
                    print("Operator ID:", operator_id)
            return operator_id
        except Exception as e:
            print("Invalid Number")

    def get_products(self, operator_id):
        """
        Retrieve products from the API, filtered by operator ID.

        Args:
            operator_id (int): The operator ID to filter products.

        Returns:
            list or None: A list of product objects, or None if an error occurs
        """
        endpoint = "products"
        params = {"operator_id": operator_id}

        try:
            products = self._make_get_request(endpoint, params=params)
            if products is not None:
                if operator_id is not None:
                    return products
                else:
                    return None
            else:
                print("No products received from the API.")
                return None
        except Exception as e:
            print(f"Error retrieving products: {e}")
            return None

    def create_transaction(self, mobile_number, trx_id, product_id):
        """Create a transaction."""
        endpoint = "async/transactions"
        payload = {
            "external_id": trx_id,
            "product_id": product_id,
            "auto_confirm": True,
            "credit_party_identifier": {
                "mobile_number": mobile_number
            }
            }
        try:
            response = self._make_post_request("POST", endpoint, payload)
            return response
        except requests.RequestException as e:
            print("Create transaction failed:", e)
            return None

    def generate_transaction_id(self):
        """Generate a unique transaction ID."""
        # Generate a UUID to ensure uniqueness
        unique_id = str(uuid.uuid4()).replace('-', '')[:10]

        # Get current timestamp (in milliseconds)
        timestamp_ms = str(int(time.time() * 1000))

        # Concatenate the timestamp and unique ID to create the transaction ID
        transaction_id = timestamp_ms + unique_id

        return transaction_id


# Example usage:
if __name__ == "__main__":
    global_services = GlobalServices()

    mobile_number = input("Enter the mobile number to lookup: ")
    result = global_services.lookup_mobile_number(mobile_number)
    if result:
        print("Mobile number lookup result:", result)
    else:
        print("Mobile number lookup failed.")
    products = global_services.get_products(result)
    print("Products available:", products)
    print()
    print()
    print(type(products))

    for product in products:
        if product['prices']['retail'] is not None:
            retail_amount = product['prices']['retail']['amount']
            fee = product['prices']['retail']['fee']
            unit = product['prices']['retail']['unit']
        else:
            retail_amount = None
            fee = None

        destination_amount = product['destination']['amount']
        destination_currency = product['destination']['unit']
        product_id = product['id']
        print(
            f"Retail amount: {retail_amount} {unit}, "
            f"Fee: {fee} {unit}, "
            f"Destination amount: {destination_amount} {destination_currency},"
            f"Product_id : {product_id}")
    print()
    print()
    trx_id = global_services.generate_transaction_id()
    print("Transaction ID:", trx_id)
    transact = global_services.create_transaction(mobile_number, trx_id, 33162)
