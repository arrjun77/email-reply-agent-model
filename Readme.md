Email Reply Agent with Telegram Integration

Overview

The Email Reply Agent is an intelligent automation system for handling incoming emails. It uses advanced natural language processing to classify the intent of each email and generate appropriate replies. The system integrates with Gmail for reading and optionally sending emails, and with Telegram for real-time review of replies.

Key capabilities include:

Fetches unread emails from Gmail using the Gmail API

Classifies email intent using zero-shot learning with a transformer model

Generates professional replies using an instruction-tuned language model

Sends generated replies to a Telegram bot for review

Optionally sends the reply email directly back to the original sender

The project is built using Python, Hugging Face Transformers, Google OAuth2, and the Telegram Bot API.

Features

Gmail API integration using OAuth2 for read and send access

Zero-shot intent classification using facebook/bart-large-mnli

AI-based reply generation using google/flan-t5-large

Telegram bot integration for real-time reply notifications

Secure .env-based configuration for credentials and secrets

MIME-compliant plain text extraction from email bodies

Centralized logging of system activities

Optional auto-reply email functionality

Project Structure

email_reply_agent/
    README.md
    requirements.txt
    .env
    venv/
    src/
        main.py - Main execution script
        fetch_email.py - Gmail unread email fetching and body parsing
        classify_and_reply.py - Email classification and reply generation
        notify_telegram.py - Telegram bot message sending
        logger.py - Logging configuration
        config.py - Loads environment variables
        credentials.json - OAuth2 credentials for Gmail API

Setup Instructions

Clone the repository:
git clone https://github.com/arrjun77/email-reply-agent-model.git

"cd email_reply_agent"

Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate (On Windows: venv\Scripts\activate)

Install required packages:
pip install -r requirements.txt

Configure Gmail API access:

Go to Google Cloud Console

Enable the Gmail API

Create OAuth2 credentials and download credentials.json

Place credentials.json inside the src/ folder

Set up your Telegram bot:

Create a bot via @BotFather on Telegram

Use @userinfobot to get your chat ID

Create a .env file in the root directory with the following contents:
TELEGRAM_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id

Running the Bot

To run the email agent:
python src/main.py

The script will:

Connect to Gmail and fetch unread emails

Classify each email’s intent

Generate a smart reply

Send the reply to your Telegram chat

Send the email reply to the original sender

Requirements

Major dependencies used in the project:

    google-api-python-client

    oauth2client

    transformers

    torch

    nltk

    scikit-learn

    requests

    python-dotenv

See requirements.txt for the full list.
