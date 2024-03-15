"""Define Services module.

This module contains a class with different methods
handling a couple of operations regarding the operations of the services.
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

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

    def _make_request(self, method, endpoint, payload=None):
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
        except requests.exceptions.RequestException as e:
            print("Error occurred during request:", e)
            return None

    def lookup_mobile_number(self, mobile_number):
        """
        Perform a lookup for the given mobile number using the Dtone API.

        Args:
            mobile_number (str): The mobile number to lookup.

        Returns:
            dict or None: The JSON response containing information about
                            the mobile number,or None if an error occurs.
        """
        endpoint = "lookup/mobile-number"
        payload = {
            "mobile_number": mobile_number,
            "page": 1,
            "per_page": 50
        }

        return self._make_request("POST", endpoint, payload)


# Example usage:
if __name__ == "__main__":
    global_services = GlobalServices()

    mobile_number = input("Enter the mobile number to lookup: ")
    result = global_services.lookup_mobile_number(mobile_number)
    if result:
        print("Mobile number lookup result:", result)
    else:
        print("Mobile number lookup failed.")
