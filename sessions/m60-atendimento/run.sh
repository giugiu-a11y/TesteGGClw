#!/bin/bash
set -euo pipefail

LOCK=/tmp/m60-atendimento.lock
LOG=/tmp/m60-atendimento.log
PY=/home/ubuntu/clawd/sessions/venv/bin/python
BOT=/home/ubuntu/clawd/sessions/m60-atendimento/bot.py

exec 9>$LOCK
if ! flock -n 9; then
  exit 0
fi

while true; do
  "$PY" "$BOT" >> "$LOG" 2>&1 || true
  sleep 5
done
