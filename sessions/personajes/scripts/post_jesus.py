#!/usr/bin/env python3
"""
post_jesus.py - Tweet poster via OAuth 1.0a (requests_oauthlib)

USAGE:
    python3 post_jesus.py "Your tweet text..."

IMPORTANT - ENVIRONMENT VARIABLES:
    This script reads credentials from environment variables.
    The calling shell script MUST export them using:
    
        set -a          # Enable auto-export
        source .env     # Load variables
        set +a          # Disable auto-export
    
    WITHOUT `set -a`, the variables won't be visible to Python!
    This was the root cause of 401 errors on 2026-02-05.

REQUIRED ENV VARS:
    - TWITTER_CONSUMER_KEY
    - TWITTER_CONSUMER_SECRET
    - TWITTER_ACCESS_TOKEN
    - TWITTER_ACCESS_TOKEN_SECRET

AUTHENTICATION:
    Uses OAuth 1.0a User Context (NOT OAuth 2.0 App-Only).
    OAuth 2.0 Bearer tokens return 403 Forbidden for posting.
"""

import os
import sys
from requests_oauthlib import OAuth1Session

# =============================================================================
# LOAD CREDENTIALS FROM ENVIRONMENT
# =============================================================================
# CRITICAL: These must be EXPORTED by the calling script using `set -a`
# Plain `source .env` does NOT export to subprocesses!

consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
    print("❌ Missing OAuth 1.0a credentials in environment variables", file=sys.stderr)
    print("", file=sys.stderr)
    print("SOLUTION: Ensure the calling script uses:", file=sys.stderr)
    print("    set -a && source .env && set +a", file=sys.stderr)
    print("", file=sys.stderr)
    print("NOT just: source .env (this doesn't export!)", file=sys.stderr)
    sys.exit(1)

# =============================================================================
# VALIDATE INPUT
# =============================================================================

if len(sys.argv) < 2:
    print("❌ Usage: python3 post_jesus.py 'Your tweet text...'", file=sys.stderr)
    sys.exit(1)

text = sys.argv[1]

if len(text) > 280:
    print(f"❌ Tweet too long ({len(text)} > 280 chars)", file=sys.stderr)
    sys.exit(1)

if len(text) == 0:
    print("❌ Empty tweet text", file=sys.stderr)
    sys.exit(1)

# =============================================================================
# POST TWEET VIA OAUTH 1.0a
# =============================================================================

try:
    # Create OAuth 1.0a session (NOT OAuth 2.0!)
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    # Post to Twitter API v2 (retry on transient failures)
    payload = {"text": text}
    response = None
    last_err = None
    for attempt in range(3):
        try:
            response = oauth.post("https://api.twitter.com/2/tweets", json=payload, timeout=20)
            if response.status_code in (429, 500, 502, 503, 504):
                raise RuntimeError(f"Transient HTTP {response.status_code}")
            break
        except Exception as e:
            last_err = e
            if attempt < 2:
                # exponential backoff: 1s, 2s
                import time
                time.sleep(1 * (2 ** attempt))
            else:
                raise last_err

    if response.status_code == 201:
        data = response.json()
        tweet_id = data.get("data", {}).get("id")
        
        print(f"✅ Tweet posted successfully!")
        print(f"   ID: {tweet_id}")
        print(f"   URL: https://twitter.com/jesussemfiltro/status/{tweet_id}")
        
    elif response.status_code == 401:
        print("❌ 401 Unauthorized - Authentication failed", file=sys.stderr)
        print("", file=sys.stderr)
        print("POSSIBLE CAUSES:", file=sys.stderr)
        print("  1. Environment variables not exported (use `set -a`)", file=sys.stderr)
        print("  2. Tokens revoked/expired (regenerate in Twitter Developer Portal)", file=sys.stderr)
        print("  3. Wrong credentials in .env file", file=sys.stderr)
        sys.exit(1)
        
    elif response.status_code == 403:
        print("❌ 403 Forbidden - Not authorized to post", file=sys.stderr)
        print("", file=sys.stderr)
        print("POSSIBLE CAUSES:", file=sys.stderr)
        print("  1. Using OAuth 2.0 App-Only (Bearer token) - use OAuth 1.0a instead", file=sys.stderr)
        print("  2. App permissions not set to 'Read and Write'", file=sys.stderr)
        sys.exit(1)
        
    else:
        error_detail = response.text
        try:
            error_json = response.json()
            if "detail" in error_json:
                error_detail = error_json["detail"]
            elif "errors" in error_json:
                error_detail = error_json["errors"][0].get("message", response.text)
        except ValueError:
            pass
            
        print(f"❌ Twitter API error ({response.status_code}): {error_detail}", file=sys.stderr)
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Unexpected error: {e}", file=sys.stderr)
    sys.exit(1)
