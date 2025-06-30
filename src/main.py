import json
import datetime
from fetch_email import fetch_unread_emails,get_service, send_email_reply
from classify_and_reply import generate_reply, classify_email, filter_recent_and_valid_emails
from notify_telegram import send_to_telegram

import re
from logger import logger

def log_reply(subject, sender, reply):
    try:
        with open("replies_log.json", "a") as f:
            json.dump({
                "timestamp": datetime.datetime.now().isoformat(),
                "sender": sender,
                "subject": subject,
                "reply": reply
            }, f)
            f.write("\n")
    except Exception as e:
        logger.warning(f"Failed to log reply: {e}")

def main():
    try:
        raw_emails = fetch_unread_emails()
        emails = []
        for subject, sender, body in raw_emails:
            emails.append({
                "subject": subject,
                "sender": sender,
                "body": body,
                "date": datetime.datetime.now().strftime("%Y-%m-%d") 
            })

        filtered_emails = filter_recent_and_valid_emails(emails)

        for email in filtered_emails:
            if "[Reply generation failed]" in email["reply"]:
                email["reply"] = "Hi there, thank you for your message. We'll get back to you shortly."

            log_reply(email["subject"], email["sender"], email["reply"])
            message = (
                f"From: {email['sender']}\n"
                f"Subject: {email['subject']}\n"
                f"Category: {email['category']}\n\n"
                f"Reply:\n{email['reply']}"
            )
            send_to_telegram(message)
            sender_match = re.search(r'<(.+?)>', email["sender"])
            to_email = sender_match.group(1) if sender_match else email["sender"]
            if "no-reply" not in to_email.lower():
                gmail_service = get_service()
                send_email_reply(gmail_service, to_email, email["subject"], email["reply"])
            

    except Exception as e:
        logger.critical(f"Unhandled exception in main: {e}")

if __name__ == "__main__":
    main()
