#!/bin/bash
# jesus-post.sh - Read from JSON and post (zero IA)
# Usage: ./jesus-post.sh 08:05

TARGET_TIME=$1
JSON_FILE="/tmp/jesus-sincero-posts.json"
LOG_FILE="/tmp/jesus-sincero-posts.log"

# Check if JSON exists
if [ ! -f "$JSON_FILE" ]; then
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ❌ JSON not found" >> "$LOG_FILE"
  exit 1
fi

# Extract post for this time
POST=$(jq -r ".posts[] | select(.time == \"$TARGET_TIME\") | .text" "$JSON_FILE" 2>/dev/null)

if [ -z "$POST" ]; then
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ⚠️ No post for $TARGET_TIME" >> "$LOG_FILE"
  exit 0
fi

# Log the post
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] 🐦 Posting @ $TARGET_TIME" >> "$LOG_FILE"
echo "TEXT: $POST" >> "$LOG_FILE"

# TODO: Integration with Twitter API
# For now, just log it
echo "✅ Ready to post @ $TARGET_TIME: $POST"
