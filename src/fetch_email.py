import os
import base64
import email
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from oauth2client import file, client, tools
from logger import logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_service():
    try:
        token_path = os.path.join(BASE_DIR, 'token.json')
        credentials_path = os.path.join(BASE_DIR, 'credentials.json')
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.send']

        store = file.Storage(token_path)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(credentials_path, SCOPES)
            creds = tools.run_flow(flow, store)
        return build('gmail', 'v1', credentials=creds)
    except Exception as e:
        logger.error(f"Failed to authenticate Gmail API: {e}")
        return None




def fetch_unread_emails():
    service = get_service()
    if not service:
        return []
    try:
        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            q="is:unread",
            maxResults=10  # Limit the number of emails fetched
        ).execute()
        messages = results.get('messages', [])
        email_data = []
        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt['payload']
            headers = payload['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
            sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown Sender")
            body = extract_body(payload)
            email_data.append((subject, sender, body))
        logger.info(f"Fetched {len(email_data)} unread emails.")
        return email_data
    except Exception as e:
        logger.error(f"Failed to fetch emails: {e}")
        return []

def extract_body(payload):
    try:
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                elif part['mimeType'].startswith('multipart/'):
                    return extract_body(part)
        data = payload['body'].get('data', '')
        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore') if data else ''
    except Exception as e:
        logger.warning(f"Failed to extract email body: {e}")
        return ''
    


def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = f"Re: {subject}"
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}



def send_email_reply(service, to_email, subject, message_body):
    try:
        message = create_message(to_email, subject, message_body)
        send_result = service.users().messages().send(userId="me", body=message).execute()
        logger.info(f"Email sent to {to_email}")
        return send_result
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return None