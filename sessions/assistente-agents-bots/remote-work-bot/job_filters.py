#!/usr/bin/env python3

import json
import os
import sys  # <<< IMPORTED sys
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

ALLOWED_COUNTRIES = ["USA", "Canada", "Germany", "UK", "Australia", "France", "Netherlands", "Portugal", "Italy", "Spain"]
ALLOWED_LANGUAGES = ["English"]
ALLOWED_SECTORS = ["tech", "health", "business", "design", "management", "finance", "engineering"]

def apply_filters(jobs):
    print("Applying filters...")
    filtered_jobs = []
    
    if not isinstance(jobs, list):
        print("Warning: No jobs list provided for filtering. Returning empty list.")
        return []

    for job in jobs:
        if not all(k in job for k in ["country", "language", "sector", "link"]):
            print(f"Skipping job due to missing fields: {job.get('title', 'N/A')}")
            continue

        if job["country"] not in ALLOWED_COUNTRIES:
            continue

        job_languages = job.get("language", "English")
        if isinstance(job_languages, str):
            job_languages = [job_languages]
        
        if not any(lang in ALLOWED_LANGUAGES for lang in job_languages):
            continue

        if job.get("sector") not in ALLOWED_SECTORS:
            continue
            
        if job["country"] in ["Brazil", "India", "Philippines"]:
            continue

        filtered_jobs.append(job)

    print(f"Filtered {len(jobs)} jobs down to {len(filtered_jobs)}.")
    return filtered_jobs

if __name__ == "__main__":
    jobs_file = os.path.join(PROJECT_ROOT, 'simulated_jobs.json') # <<< CHANGED to simulated_jobs.json
    
    if not os.path.exists(jobs_file):
        print(f"Error: Jobs file not found at {jobs_file}")
        sys.exit(1)

    with open(jobs_file, 'r') as f:
        jobs_data = json.load(f)

    filtered_jobs = apply_filters(jobs_data)

    filtered_jobs_file = os.path.join(PROJECT_ROOT, 'simulated_jobs_filtered.json')
    with open(filtered_jobs_file, 'w') as f:
        json.dump(filtered_jobs, f, indent=2)

    print(f"Filtered jobs saved to: {filtered_jobs_file}")
