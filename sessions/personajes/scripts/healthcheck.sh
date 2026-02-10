#!/bin/bash
set -e

DIR="/home/ubuntu/clawd/sessions/personajes"
LOG_DIR="$DIR/logs"
ERROR_LOG="$LOG_DIR/error.log"

mkdir -p "$LOG_DIR"

# DNS check (no LLM)
if ! resolvectl query api.twitter.com >/dev/null 2>&1; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] DNS_FAIL: api.twitter.com" >> "$ERROR_LOG"
  exit 1
fi

# Simple API reachability (no post)
if ! curl -s --max-time 10 https://api.twitter.com/2/ >/dev/null 2>&1; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] API_UNREACHABLE: api.twitter.com" >> "$ERROR_LOG"
  exit 1
fi

exit 0
