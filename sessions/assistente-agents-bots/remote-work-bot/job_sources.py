#!/usr/bin/env python3

import requests
import json
import os
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

def fetch_job_listings(keywords, sources, filters):
    print(f"Searching for jobs with keywords: {keywords}")
    print(f"From sources: {sources}")
    print(f"Applying filters: {filters}")

    simulated_jobs = []
    base_job_data = {
        "title": "Software Engineer",
        "company": "Tech Solutions Inc.",
        "country": "USA",
        "language": "English",
        "sector": "tech",
        "link": "https://example.com/jobs/tech-solutions-software-engineer"
    }

    for i, keyword in enumerate(keywords):
        job_data = base_job_data.copy()
        job_data["title"] = f"{keyword.split()[-2]} {keyword.split()[-1]} - Role {i+1}" # e.g., 'Engineer Remote - Role 1'
        job_data["company"] = f"Company {i+1} LLC"
        # Cycle through countries, languages, and sectors to simulate diversity
        job_data["country"] = filters.get("countries", ["USA"])[i % len(filters.get("countries", ["USA"]))] 
        job_data["language"] = filters.get("languages", ["English"])[i % len(filters.get("languages", ["English"]))] 
        job_data["sector"] = filters.get("sectors", ["tech"])[i % len(filters.get("sectors", ["tech"]))] 
        job_data["link"] = f"https://example.com/jobs/{job_data['company'].lower().replace(' ', '-')}-{job_data['title'].lower().replace(' ', '-')}"
        simulated_jobs.append(job_data)

    # Add some jobs that might be filtered out to test the filter logic
    simulated_jobs.append({
        "title": "Nurse Remote",
        "company": "HealthCare Global",
        "country": "Brazil", # Will be filtered out
        "language": "Portuguese", # Will be filtered out
        "sector": "health",
        "link": "https://example.com/jobs/healthcare-nurse"
    })
    simulated_jobs.append({
        "title": "Accountant Remote",
        "company": "Finance Masters",
        "country": "USA",
        "language": "English",
        "sector": "finance",
        "link": "https://example.com/jobs/finance-accountant"
    })
    
    print(f"Found {len(simulated_jobs)} jobs (simulated).")
    return simulated_jobs

if __name__ == "__main__":
    config_path = os.path.join(PROJECT_ROOT, 'config.json')
    env_path = os.path.join(PROJECT_ROOT, '.env')
    
    config = {}
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)

    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key] = value

    keywords = [
        "Software Engineer remote", "Designer remote", "Nurse remote",
        "Project Manager remote", "Accountant remote"
    ]
    
    job_filters = {
        "countries": ["USA", "Canada", "Germany", "UK", "Australia", "France", "Netherlands", "Portugal", "Italy", "Spain"],
        "languages": ["English"],
        "sectors": ["tech", "health", "business", "design", "management", "finance", "engineering"]
    }

    jobs = fetch_job_listings(keywords, ["Google Jobs", "LinkedIn"], job_filters)
    
    # Save jobs to the file expected by job_filters.py
    output_file = os.path.join(PROJECT_ROOT, 'simulated_jobs.json')
    with open(output_file, 'w') as f:
        json.dump(jobs, f, indent=2)
    
    print(f"Simulated jobs saved to: {output_file}")
