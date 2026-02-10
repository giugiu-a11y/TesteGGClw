#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import os
import json
import time
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

# Timeout for HTTP requests
REQUEST_TIMEOUT = 10 # seconds

def resolve_official_link(job_data):
    print(f"Resolving official link for: {job_data.get('title', 'N/A')} at {job_data.get('company', 'N/A')}")
    
    original_link = job_data.get('link')
    if not original_link:
        print("No original link found. Cannot resolve.")
        return job_data

    try:
        # First, try to fetch the original link to see if it's valid and get context.
        # Use a User-Agent header to mimic a browser.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(original_link, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # If the link is already to an official careers page, use it.
        # This is a heuristic and might need refinement.
        # Simple checks: domain name, keywords like 'careers', 'jobs', 'joinus'
        if "careers" in response.url or "jobs" in response.url or "joinus" in response.url or urlparse(response.url).netloc.lower() == urlparse(original_link).netloc.lower():
            job_data['official_link'] = response.url
            job_data['link_valid'] = True
            print(f"Original link is likely official or valid: {response.url}")
            return job_data
        
        # If not obviously official, try to find a company careers page.
        # This is the complex part and might require more advanced scraping or searching.
        # For now, we'll simulate finding a link or consider the original valid if it's accessible.
        
        # Basic simulation: If accessible, we might consider it good enough for this example.
        job_data['official_link'] = response.url # Fallback to the accessible link
        job_data['link_valid'] = True
        print(f"Accessible link found (fallback): {response.url}")

    except requests.exceptions.RequestException as e:
        print(f"Could not access link {original_link}: {e}")
        job_data['link_valid'] = False

    return job_data

if __name__ == "__main__":
    # Load filtered jobs from job_filters.py output
    jobs_file = os.path.join(PROJECT_ROOT, 'simulated_jobs_filtered.json')
    
    if not os.path.exists(jobs_file):
        print(f"Error: Filtered jobs file not found at {jobs_file}")
        sys.exit(1)

    with open(jobs_file, 'r') as f:
        jobs_data = json.load(f)

    resolved_jobs = []
    for job in jobs_data:
        # --- IMPORTANT: We need the urlparse function here --- 
        # For demonstration, let's mock it or expect it to be available.
        # In a real script, you'd import it: from urllib.parse import urlparse
        try:
            from urllib.parse import urlparse
        except ImportError:
            print("Error: urllib.parse not found. Please ensure Python is installed correctly.")
            sys.exit(1)
        
        # Mocking urlparse for this script's execution if it fails to import properly
        if 'urlparse' not in locals():
            class MockUrlParse:
                def __init__(self, url):
                    self.url = url
                    self.netloc = url.split('/')[2] if '/' in url else url
            def urlparse(url):
                return MockUrlParse(url)
        
        resolved_job = resolve_official_link(job)
        resolved_jobs.append(resolved_job)
        # Add a small delay to be polite to servers
        time.sleep(1)

    # Save resolved jobs
    resolved_jobs_file = os.path.join(PROJECT_ROOT, 'simulated_jobs_resolved.json')
    with open(resolved_jobs_file, 'w') as f:
        json.dump(resolved_jobs, f, indent=2)
    
    print(f"Resolved jobs saved to: {resolved_jobs_file}")
