#!/bin/bash
set -euo pipefail

LOCK=/tmp/assistente-opus.lock
LOG=/tmp/assistente-opus.log
PY=/home/ubuntu/clawd/sessions/venv/bin/python
BOT=/home/ubuntu/clawd/sessions/assistente-opus/bot.py

exec 9>$LOCK
if ! flock -n 9; then
  exit 0
fi

while true; do
  "$PY" "$BOT" >> "$LOG" 2>&1 || true
  sleep 5
done
