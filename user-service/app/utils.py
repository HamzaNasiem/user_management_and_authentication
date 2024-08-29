#utils.py
import requests
from app.settings import WHATSAPP_API_KEY


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
