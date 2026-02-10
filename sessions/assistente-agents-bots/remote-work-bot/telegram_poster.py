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
                        globals()['TELEGRAM_BOT_TOKEN'] = value.strip().strip('"').strip("'")
                    elif key == 'TELEGRAM_GROUP_ID':
                        globals()['TELEGRAM_GROUP_ID'] = value.strip().strip('"').strip("'")
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_GROUP_ID:
        print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_GROUP_ID not found in .env")
        sys.exit(1)

def _get_first(job, keys, default="N/A"):
    for key in keys:
        if key in job and job[key] not in (None, ""):
            return job[key]
    return default

def _get_nested(job, keys, default="N/A"):
    value = job
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    return value if value not in (None, "") else default

def _strip_html(text):
    if not isinstance(text, str):
        return text
    cleaned = re.sub(r"<[^>]+>", " ", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

def _is_direct_job_link(url):
    if not isinstance(url, str) or not url.strip():
        return False
    lower = url.strip().lower()
    # Block generic career landing pages
    generic_patterns = [
        r"/careers/?$",
        r"/jobs/?$",
        r"/work-with-us/?$",
        r"/join-us/?$",
        r"/careers#",
        r"/jobs#",
    ]
    for pattern in generic_patterns:
        if re.search(pattern, lower):
            return False
    # Require some path depth to indicate a specific role
    return "/" in lower[8:] if lower.startswith("https://") else "/" in lower

def format_job_message_plain(job):
    # Simplified formatting for plain text, with schema fallbacks
    title = _get_first(job, ["title", "titulo"])
    company = _get_first(job, ["company", "empresa"])
    country = _get_first(job, ["country", "pais"])
    salary_usd_month = _get_first(job, ["salario_usd_month", "salario_usd_mes", "salary_usd_month"])
    description = _get_nested(job, ["requisitos", "descricao"], default=_get_first(job, ["description", "descricao"]))
    description = _strip_html(description)
    if isinstance(description, str) and len(description) > 240:
        description = description[:237].rstrip() + "..."
    link = _get_first(job, ["official_link", "link"], default="#")

    # Ensure plain text is safe, avoid problematic characters if possible, though not strictly necessary for plain text.
    # For plain text, Telegram is usually more permissive.
    message = f"Vaga: {title}\n"
    message += f"{company}\n"
    message += f"Local: {country}\n"
    message += f"Salário: USD ${salary_usd_month}/mês\n"
    message += f"Descrição: {description}\n"
    message += f"Aplicar: {link}"
    
    return message

def send_to_telegram(job):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_GROUP_ID:
        print("Telegram credentials not loaded. Cannot send message.")
        return False

    link = _get_first(job, ["official_link"], default="#")
    if not link or link == "#" or str(link).strip() == "":
        print(f"Skipping job without valid link: {job.get('title', job.get('titulo', 'N/A'))}")
        return False
    if not _is_direct_job_link(link) and not job.get("allow_generic"):
        print(f"Skipping job without direct link: {job.get('title', job.get('titulo', 'N/A'))}")
        return False
    if job.get("link_valid") is False:
        print(f"Skipping job with invalid link: {job.get('title', job.get('titulo', 'N/A'))}")
        return False

    formatted_message = format_job_message_plain(job)
    print("---")
    print("Formatted Message (Plain Text):")
    print(formatted_message)
    print("--- End Formatted Message ---")
    
    telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_GROUP_ID,
        "text": formatted_message,
        # Removed parse_mode to send as plain text
        "disable_web_page_preview": True
    }
    
    for attempt in range(1, 4):
        try:
            response = requests.post(telegram_api_url, data=payload, timeout=15)
            response.raise_for_status()
            result = response.json()
            
            if result.get("ok"):
                print(f"Successfully posted job: {job.get('title', job.get('titulo', 'N/A'))}")
                return True
            else:
                print(f"Telegram API error: {result.get('description')}")
                print(f"Raw API response: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Error sending message via Telegram API (attempt {attempt}/3): {e}")
            if attempt == 3:
                return False
        except json.JSONDecodeError:
            print(f"Error decoding Telegram API response: {response.text}")
            return False

if __name__ == "__main__":
    jobs_file = os.path.join(PROJECT_ROOT, 'simulated_jobs_final.json')
    
    if not os.path.exists(jobs_file):
        print(f"Error: Final jobs file not found at {jobs_file}")
        sys.exit(1)

    with open(jobs_file, 'r') as f:
        final_jobs_data = json.load(f)

    load_env_vars()

    job_index_to_post = None
    if len(sys.argv) > 1:
        try:
            job_index_to_post = int(sys.argv[1])
            if not (0 <= job_index_to_post < len(final_jobs_data)):
                print(f"Error: Invalid job index {job_index_to_post}. Must be between 0 and {len(final_jobs_data)-1}. Total jobs: {len(final_jobs_data)}.")
                sys.exit(1)
        except ValueError:
            print(f"Error: Invalid argument. Expected an integer job index, but got {sys.argv[1]}.")
            sys.exit(1)
    else:
        print("Usage: python telegram_poster.py <job_index>")
        sys.exit(1)

    job_to_post = final_jobs_data[job_index_to_post]
    send_to_telegram(job_to_post)
