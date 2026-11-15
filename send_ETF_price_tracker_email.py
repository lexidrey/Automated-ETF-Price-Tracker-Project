import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

"""
EmailMessage() creates your email using MIME formatting.
set_content() adds the email body.
smtplib.SMTP() connects to Gmail's SMTP server.
starttls() establishes an encrypted connection.
login() authenticates your Gmail account.
send_message() sends the email.
"""

# Locally: It looks for a .env file and loads its variables into your environment.
# On GCP: If there is no .env file, it simply does nothing. It does not throw an error.
load_dotenv()

def send_email(subject, body):
    # Retrieve credentials and email addresses
    sender_email = os.getenv("GMAIL_ADDRESS")
    app_password = os.getenv("GOOGLE_APP_PASSWORD")
    recipient_email_1 = os.getenv("EMAIL_RECIPIENT_1") # Required
    recipient_email_2 = os.getenv("EMAIL_RECIPIENT_2")
    recipient_email_3 = os.getenv("EMAIL_RECIPIENT_3")
    recipient_email_4 = os.getenv("EMAIL_RECIPIENT_4")

    # Check that all required values exist
    if not all([sender_email, app_password, recipient_email_1]):
        raise ValueError("Missing email configuration.")

    # Construct the email
    message = EmailMessage()
    message["From"] = sender_email
    recipients = [recipient_email_1, recipient_email_2, recipient_email_3, recipient_email_4]
    message["To"] = ", ".join(recipients)
    #message["To"] = recipient_email_1
    message["Subject"] = subject
    message.set_content(body)

    # Connect to Gmail's SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:

        # Establish TLS encryption
        server.starttls()

        # Authenticate with Gmail
        server.login(sender_email, app_password.replace(" ", ""))

        # Send the email
        server.send_message(message)

    print("Email successfully sent!")