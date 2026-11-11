import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def send_otp_email(email, otp):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("SMTP_FROM_EMAIL")

    if not smtp_host or not smtp_port or not smtp_username or not smtp_password or not sender_email:
        print("Email settings are missing. This is a development environment and the otp will be printed to the console.")
        print("Email:", email)
        print("OTP:", otp)
        print("This is valid for 5 minutes.")
        return

    message = EmailMessage()
    message["Subject"] = "Your registration OTP"
    message["From"] = sender_email
    message["To"] = email
    message.set_content("Your OTP is " + otp + ". It expires in 5 minutes.")

    with smtplib.SMTP(smtp_host, int(smtp_port)) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)
