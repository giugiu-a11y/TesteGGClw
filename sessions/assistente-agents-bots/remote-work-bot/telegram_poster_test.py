#!/usr/bin/env python3

import requests
import json
import os
import sys
import re
import builtins

# Assume que o script está em sessions/assistente-agents-bots/remote-work-bot/
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Redact sensitive values from prints
_TOKEN_RE = re.compile(r"\b\d{9,}:[A-Za-z0-9_-]{20,}\b")
_SECRETS = [
    os.getenv("TELEGRAM_BOT_TOKEN"),
    os.getenv("TELEGRAM_GROUP_ID"),
    os.getenv("TELEGRAM_CHAT_ID"),
    os.getenv("GEMINI_API_KEY"),
    os.getenv("GOOGLE_API_KEY"),
]
_SECRETS = [s for s in _SECRETS if s]


def _redact_text(text: str) -> str:
    if not text:
        return text
    text = _TOKEN_RE.sub("<redacted-token>", text)
    for secret in _SECRETS:
        text = text.replace(secret, "<redacted>")
    return text


def print(*args, **kwargs):
    redacted = [_redact_text(str(a)) for a in args]
    return builtins.print(*redacted, **kwargs)

# --- Configuration ---
# Load sensitive info from .env file
TELEGRAM_BOT_TOKEN = None
TELEGRAM_GROUP_ID = None

def load_env_vars():
    env_path = os.path.join(PROJECT_ROOT, '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    if key == 'TELEGRAM_BOT_TOKEN':
                        globals()['TELEGRAM_BOT_TOKEN'] = value
                    elif key == 'TELEGRAM_GROUP_ID':
                        globals()['TELEGRAM_GROUP_ID'] = value
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_GROUP_ID:
        print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_GROUP_ID not found in .env")
        sys.exit(1)

def send_test_message():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_GROUP_ID:
        print("Telegram credentials not loaded. Cannot send message.")
        return False

    test_message = "This is a plain text test message. It should send without formatting issues."
    
    telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_GROUP_ID,
        "text": test_message,
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(telegram_api_url, data=payload, timeout=15)
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            print(f"Successfully sent test message.")
            return True
        else:
            print(f"Telegram API error: {result.get('description')}")
            print(f"Raw API response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Error sending message via Telegram API: {e}")
        return False
    except json.JSONDecodeError:
        print(f"Error decoding Telegram API response: {response.text}")
        return False

if __name__ == "__main__":
    load_env_vars()
    send_test_message()
