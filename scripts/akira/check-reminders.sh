#!/bin/bash
# check-reminders.sh - Read reminders.json and notify (zero IA)

REMINDERS_FILE="${HOME}/clawd/.reminders.json"
LOG_FILE="/tmp/reminders.log"

if [ ! -f "$REMINDERS_FILE" ]; then
  echo "[$(date)] ℹ️ No reminders file" >> "$LOG_FILE"
  exit 0
fi

TODAY=$(date +%d)

# Check today's reminders
REMINDERS=$(jq -r ".lembretes[] | select(.ativo == true and .diaLembrete == $TODAY) | \"\(.nome) (vencimento: \(.diaVencimento) de cada mês)\"" "$REMINDERS_FILE" 2>/dev/null)

if [ -n "$REMINDERS" ]; then
  echo "[$(date)] 💳 Lembretes para hoje:" >> "$LOG_FILE"
  echo "$REMINDERS" >> "$LOG_FILE"
  # Would post to Telegram here
fi
