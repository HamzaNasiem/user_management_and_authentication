#utils.py
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
import random
from datetime import datetime, timedelta
from typing import Optional, Dict
from app.settings import EMAIL_HOST, EMAIL_PASSWORD, EMAIL_PORT, EMAIL_USER, WHATSAPP_API_KEY

# Existing function to send WhatsApp messages


def send_whatsapp_message(number: str, message: str):
    api_url = "https://chatify.najam.pk/api/v1/sendmessage"
    payload = {
        "number": number,
        "message": message,
        "apikey": WHATSAPP_API_KEY
    }
    try:
        response = requests.get(api_url, params=payload)
        print(f"WhatsApp API Response: {response.text}")
        response.raise_for_status()
        return {"status": "success", "detail": "Message sent successfully"}
    except requests.exceptions.RequestException as e:
        print(f"Error Sending WhatsApp Message: {e}")
        return {"status": "error", "detail": f"Failed to send message: {e}"}

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

otp_storage = {}


def send_email_otp(email: str, otp: str) -> Dict[str, str]:
    message = MIMEMultipart()
    message["From"] = EMAIL_USER
    message["To"] = email
    message["Subject"] = "Your OTP Code"

    body = f"Your OTP for registration is {otp}. It is valid for 5 minutes."
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, email, message.as_string())
        return {"status": "success", "detail": "Email sent successfully"}
    except Exception as e:
        print(f"Error sending email: {e}")
        return {"status": "error", "detail": "Failed to send email"}


def store_otp(identifier: str, otp: str, is_email: bool = False):
    expiry = datetime.utcnow() + timedelta(minutes=5)
    otp_storage[identifier] = {"otp": otp,
                               "expiry": expiry, "is_email": is_email}


def get_otp(identifier: str) -> Optional[Dict[str, any]]:
    otp_record = otp_storage.get(identifier)
    if otp_record and otp_record["expiry"] > datetime.utcnow():
        return otp_record
    return None
