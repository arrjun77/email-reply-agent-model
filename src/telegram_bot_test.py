from dotenv import load_dotenv
import os
import requests

# Load .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_test_message():
    message = "Hello Pookie! Your bot is working perfectly! "
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    print("Status:", response.status_code)
    print("Response:", response.text)

send_test_message()
