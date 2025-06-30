from transformers import pipeline, AutoTokenizer
from datetime import datetime, timedelta
from logger import logger

# Initialize models and tokenizers
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
classifier_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")

# Use a larger T5 model for better reply generation
generator = pipeline("text2text-generation", model="google/flan-t5-large")
generator_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")

CANDIDATE_LABELS = [
    "job inquiry", "project collaboration", "customer support", "sales", 
    "general question", "spam", "personal message", "complaint", "newsletter"
]

VALID_CATEGORIES = {"personal message", "project collaboration", "customer support", "complaint"}


def classify_email(email_text):
    try:
        tokens = classifier_tokenizer.encode(email_text, truncation=True, max_length=512)
        truncated_text = classifier_tokenizer.decode(tokens, skip_special_tokens=True)
        result = classifier(truncated_text, CANDIDATE_LABELS)
        label = result['labels'][0]
        logger.info(f"Email classified as: {label}")
        return label
    except Exception as e:
        logger.error(f"Email classification failed: {e}")
        return "unknown"


def generate_reply(email_text, category):
    try:
        style_hint = {
            "project collaboration": "Express interest and say you will respond in detail within 2 days.",
            "customer support": "Acknowledge concern and say it will be resolved within 2 days.",
            "complaint": "Apologize politely and say issue will be reviewed and addressed within 2 days.",
            "personal message": "Thank the sender and say you’ll get back soon."
        }.get(category, "Reply politely and professionally.")

        prompt = (
            f"You are a helpful assistant. Write a concise, professional email reply with a personal tone. {style_hint}\n"
            f"Original message: {email_text.strip()}"
        )

        result = generator(
            prompt,
            max_new_tokens=200,
            temperature=0.4,
            top_p=0.9,
            do_sample=True,
            no_repeat_ngram_size=3,
            early_stopping=True
        )[0]['generated_text']

        logger.info("Generated reply successfully.")
        return result
    except Exception as e:
        logger.error(f"Reply generation failed: {e}")
        return "[Reply generation failed]"


def filter_recent_and_valid_emails(email_list):
    one_week_ago = datetime.now() - timedelta(days=7)
    filtered = []
    for email in email_list:
        if email.get("date") and datetime.strptime(email["date"], "%Y-%m-%d") >= one_week_ago:
            category = classify_email(email["body"])
            if category in VALID_CATEGORIES:
                email["category"] = category
                email["reply"] = generate_reply(email["body"], category)
                filtered.append(email)
    return filtered
