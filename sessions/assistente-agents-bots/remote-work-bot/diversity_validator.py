#!/usr/bin/env python3

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

# Define criteria thresholds based on project_logic.md
MIN_COUNTRIES = 2
MIN_SECTORS = 3
MIN_REQUIRED_ENGLISH = 1
MIN_FACULTY_YES = 1
MIN_FACULTY_NO = 1
MIN_EXPERIENCE_ANY = 1
MIN_EXPERIENCE_SPECIFIC = 1 # E.g., X+ years

def validate_diversity(analyzed_jobs):
    print("Applying diversity validation...")
    
    if not isinstance(analyzed_jobs, list):
        print("Warning: No analyzed jobs list provided for validation. Returning empty list.")
        return []

    approved_jobs = []
    
    # We need to select up to 3 diverse jobs from the analyzed list
    # This selection process can be complex. For simplicity, we'll try to pick the first few that meet criteria.
    
    # Collect candidates that meet basic requirements and then select for diversity
    eligible_candidates = []
    for job in analyzed_jobs:
        if job.get('aprovada', False) == True:
            eligible_candidates.append(job)
    
    if not eligible_candidates:
        print("No jobs approved by LLM analysis. Cannot perform diversity validation.")
        return []

    # --- Diversity criteria checks --- 
    # This is a simplified selection logic. A real implementation might need more sophisticated logic 
    # to ensure the BEST combination of diverse jobs is selected.
    
    selected_for_diversity = []
    countries_seen = set()
    sectors_seen = set()
    has_english_req = False
    has_faculty_yes = False
    has_faculty_no = False
    has_experience_any = False
    has_experience_specific = False

    # Iterate through eligible candidates to pick diverse ones
    for job in eligible_candidates:
        if len(selected_for_diversity) >= 3: # Stop if we have 3 diverse jobs
            break
            
        is_diverse_enough = False

        # Check criteria against current selection
        current_selection_countries = set(j.get('country') for j in selected_for_diversity)
        current_selection_sectors = set(j.get('sector') for j in selected_for_diversity)
        current_selection_english = any(j.get('requisitos', {}).get('ingles') for j in selected_for_diversity)
        current_selection_faculty_yes = any(j.get('requisitos', {}).get('faculdade') == 'sim' for j in selected_for_diversity)
        current_selection_faculty_no = any(j.get('requisitos', {}).get('faculdade') == 'nao' for j in selected_for_diversity)
        current_selection_experience_any = any(j.get('requisitos', {}).get('experiencia_anos') is not None for j in selected_for_diversity)
        current_selection_experience_specific = any(j.get('requisitos', {}).get('experiencia_anos', 0) > 1 for j in selected_for_diversity)

        # Check if adding this job would improve diversity
        if job.get('country') not in current_selection_countries:
            is_diverse_enough = True
        if job.get('sector') not in current_selection_sectors:
            is_diverse_enough = True
        if job.get('requisitos', {}).get('ingles') and not current_selection_english:
            is_diverse_enough = True
        if job.get('requisitos', {}).get('faculdade') == 'sim' and not current_selection_faculty_yes:
            is_diverse_enough = True
        if job.get('requisitos', {}).get('faculdade') == 'nao' and not current_selection_faculty_no:
            is_diverse_enough = True
        if job.get('requisitos', {}).get('experiencia_anos') is not None and not current_selection_experience_any:
            is_diverse_enough = True
        if job.get('requisitos', {}).get('experiencia_anos', 0) > 1 and not current_selection_experience_specific:
            is_diverse_enough = True

        # If it adds diversity or if we still need more jobs and it meets basic criteria
        if is_diverse_enough or len(selected_for_diversity) < MIN_COUNTRIES: # Looser check to get at least some jobs
            selected_for_diversity.append(job)
            # Update overall seen criteria for subsequent checks if needed, but current approach picks independently first

    # Final check on the selected_for_diversity count and diversity criteria
    if len(selected_for_diversity) < MIN_COUNTRIES: # Need at least MIN_COUNTRIES
        print(f"Not enough diversity in countries. Found only {len(set(j.get('country') for j in selected_for_diversity))} unique countries.")
        # If we haven't met the minimum number of jobs, just take the first few that passed LLM approval.
        if len(selected_for_diversity) < 3: # If still need jobs, take first ones that passed LLM
            selected_for_diversity = eligible_candidates[:3] # Take first 3 as a fallback

    # If we still have fewer than 3 jobs but eligible candidates exist, fill the rest
    if len(selected_for_diversity) < 3 and len(eligible_candidates) > len(selected_for_diversity):
        for job in eligible_candidates:
            if len(selected_for_diversity) >= 3:
                break
            if job not in selected_for_diversity:
                selected_for_diversity.append(job)

    # In a more robust system, you'd re-evaluate the WHOLE SET of eligible_candidates
    # to find the best combination meeting ALL diversity criteria.
    # For this example, we'll just take the first 3 that were somewhat diverse.
    approved_jobs = selected_for_diversity[:3]

    print(f"Selected {len(approved_jobs)} jobs for posting after diversity check.")
    return approved_jobs

if __name__ == "__main__":
    jobs_file = os.path.join(PROJECT_ROOT, 'simulated_jobs_analyzed.json')
    
    if not os.path.exists(jobs_file):
        print(f"Error: Analyzed jobs file not found at {jobs_file}")
        sys.exit(1)

    with open(jobs_file, 'r') as f:
        analyzed_jobs_data = json.load(f)

    # Apply diversity validation
    final_jobs_for_posting = validate_diversity(analyzed_jobs_data)

    # Save the final list of jobs to be posted
    final_jobs_file = os.path.join(PROJECT_ROOT, 'simulated_jobs_final.json')
    with open(final_jobs_file, 'w') as f:
        json.dump(final_jobs_for_posting, f, indent=2)
    
    print(f"Final jobs for posting saved to: {final_jobs_file}")
