"""Helpers module."""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Helpers():
    """Define helpers Class.
    Description:
                    This class contains methods that will be helping with
                    certain operations.
    """
    def __init__(self):
        """Define the Init method."""

    def send_receipt_email(self, transaction_info, voucher, units):
        """
        Send an email to the customer with transaction details.

        Args:
            

        Returns:
            None
        """
        

        # Compose email message
        subject = "Receipt for your recent purchase"
        html_message = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>Transaction Confirmation</title>
        </head>
        <body>
        <h1>Transaction Confirmation</h1>

        <p>Dear Customer,</p>

        <p>We are pleased to inform you that your transaction has been successfully processed.</p>

        <h2>Transaction Details:</h2>
        <ul>
        <li><strong>Confirmation Date:</strong> {{ confirmation_date }}</li>
        <li><strong>Credit Party Mobile Number:</strong> {{ credit_party_mobile_number }}</li>
        <li><strong>Retail Price:</strong> {{ retail_price }}</li>
        <li><strong>Wholesale Price:</strong> {{ wholesale_price }}</li>
        <li><strong>Operator Name:</strong> {{ operator_name }}</li>
        <li><strong>Product Description:</strong> {{ product_description }}</li>
        <li><strong>Status Message:</strong> {{ status_message }}</li>
        </ul>

        <p>Thank you for choosing our service.</p>

        <p>Sincerely,<br>Your Company Name</p>
        </body>
        </html>
        """       
        company_email = "payment@remmittance.com"

        # Retrieve email sending
        email_api_key = os.getenv('email_api')
        smtp_port = os.getenv('smtp_port')
        smtp_server = os.getenv('smtp_server')
        email_password = os.getenv('email_password')

        # Sending email
        response = self.send_email(company_email, customer_email, email_password, smtp_server, smtp_port, subject, message)
        return response
    def send_email(self, sender_email, receiver_email, password, smtp_server, smtp_port, subject, html_message):
        """
        Send an email with HTML content using SMTP.

        Args:
            sender_email (str): The sender's email address.
            receiver_email (str): The recipient's email address.
            password (str): The password for the sender's email account.
            smtp_server (str): The SMTP server address.
            smtp_port (int): The SMTP port number.
            subject (str): The subject of the email.
            html_message (str): The HTML content of the email message.

        Returns:
            None

        Raises:
            Exception: If an error occurs while sending the email.
        """
        # Connect to SMTP server
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.ehlo()
        server.login(sender_email, password)

        # Create a multipart message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Attach HTML message
        message.attach(MIMEText(html_message, "html"))

        # Send email
        try:
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email. Error: {e}")
        finally:
            server.quit()  # Close the connection

if __name__ == '__main__':
    help = Helpers()
    # Retrieve email sending
    email_api_key = os.getenv('email_api')
    smtp_port = os.getenv('smtp_port')
    smtp_server = os.getenv('smtp_server')
    email_password = os.getenv('email_password')

    sender_email = "payment@remmittance.com"
    receiver_email = "rugema61@gmail.com"
    subject = 'Test'
    message = "Trying to see if the email will be sent."
    print("Before sending emails: ")
    print()

    send_response = help.send_email(sender_email, receiver_email, email_password, smtp_server, smtp_port, subject, message)
    print("After sending: ", send_response)


