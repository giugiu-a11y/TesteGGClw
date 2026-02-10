#!/bin/bash
# =============================================================================
# post-daily.sh - Daily Twitter posting for Jesus Sincero
# =============================================================================
#
# USAGE:
#     bash scripts/post-daily.sh 09:00
#
# DESCRIPTION:
#     Reads posts from data/posts_current.json and posts the one matching
#     today's date and the specified time to Twitter.
#
# CRITICAL - ENVIRONMENT VARIABLES:
#     This script uses `set -a` before `source .env` to EXPORT variables.
#     Without `set -a`, Python subprocess cannot read the credentials!
#
#     CORRECT:   set -a && source .env && set +a
#     WRONG:     source .env  (variables not exported!)
#
#     This was the root cause of 401 errors on 2026-02-05.
#
# CRON SETUP:
#     0 12 * * * cd /home/ubuntu/clawd/sessions/personajes && source venv/bin/activate && bash scripts/post-daily.sh 09:00 >> logs/posting.log 2>&1
#
# =============================================================================

set -e

cd "$(dirname "$0")/.."

TARGET_TIME=$1
if [ -z "$TARGET_TIME" ]; then
  echo "❌ Usage: $0 <time> (e.g., 09:00)"
  exit 1
fi

# Prevent duplicate posts if cron or manual runs overlap
LOCK_FILE="/tmp/jesus_post_${TARGET_TIME//:/}.lock"
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  Lock active for $TARGET_TIME; skipping duplicate run"
  exit 0
fi

JSON_FILE="data/posts_current.json"
LOG_FILE="logs/posting.log"
ERROR_LOG="logs/error.log"
TODAY=$(date +%Y-%m-%d)

{
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📤 Posting @ $TARGET_TIME..."
  
  # Verify JSON exists
  if [ ! -f "$JSON_FILE" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Posts file not found: $JSON_FILE"
    exit 1
  fi
  
  # Extract post for today and this time
  POST=$(jq -r ".posts[] | select(.date == \"$TODAY\" and .time == \"$TARGET_TIME\") | .text" "$JSON_FILE" 2>/dev/null)
  
  if [ -z "$POST" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  No post for $TODAY @ $TARGET_TIME"
    exit 0
  fi
  
  # Count characters
  CHAR_COUNT=${#POST}
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📝 Text ($CHAR_COUNT chars): ${POST:0:60}..."
  
  # Activate virtual environment
  source venv/bin/activate
  
  # ==========================================================================
  # CRITICAL: Export environment variables for Python subprocess
  # ==========================================================================
  # Without `set -a`, Python cannot read these variables via os.environ.get()!
  # This was the bug that caused 401 errors on 2026-02-05.
  set -a
  source .env
  set +a
  # ==========================================================================
  
  # Post via Python
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🐦 Posting via Twitter API..."
  
  python3 scripts/post_jesus.py "$POST" >> "$ERROR_LOG" 2>&1
  
  if [ $? -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Posted successfully @ $TARGET_TIME"
  else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Post failed (see error.log)"
    exit 1
  fi
  
} | tee -a "$LOG_FILE"
