import requests
import html
from config import TELEGRAM_TOKEN, CHAT_ID
from logger import logger

MAX_TELEGRAM_MSG_LENGTH = 4096

def send_to_telegram(message):
    logger.info("Starting to connect to Telegram .")

    try:
        escaped_message = html.escape(message)
        
        if len(escaped_message) > MAX_TELEGRAM_MSG_LENGTH:
            logger.warning(f"Telegram message too long ({len(escaped_message)} chars), truncating.")
            escaped_message = escaped_message[:MAX_TELEGRAM_MSG_LENGTH - 100] + "\n\n[Message truncated...]"
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": escaped_message,
            "parse_mode": "HTML"
        }

        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logger.info("Telegram message sent successfully.")
        else:
            logger.warning(f"Telegram message failed with status: {response.status_code}, text: {response.text}")
        return response
    except Exception as e:
        logger.error(f"Telegram notification failed: {e}")
        return None
