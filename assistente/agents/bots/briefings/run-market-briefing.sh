#!/bin/bash
# run-market-briefing.sh - Orquestrador completo (fetch → compile → send)

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/market-briefing-$(date +%Y%m%d_%H%M%S).log"

# Carrega secrets de lugar seguro (chmod 600)
if [ -f ~/.config/secrets.env ]; then
  export $(cat ~/.config/secrets.env | grep "BOT_ASSISTENTE\|^[^#]" | xargs)
fi

{
  echo "=== Market Briefing - $(date '+%Y-%m-%d %H:%M:%S') ==="
  
  # 1. Fetch dados
  echo "[1/3] Fetching market data..."
  bash "$DIR/fetch/fetch-market.sh" > /dev/null
  
  # 2. Compile
  echo "[2/3] Compiling briefing..."
  bash "$DIR/compile/compile-market.sh"
  
  # 3. Send
  echo "[3/3] Sending to Telegram..."
  bash "$DIR/send/send-to-telegram.sh"
  
  echo "=== Done ==="
  cat /tmp/briefing-market.txt
  
} | tee -a "$LOG_FILE"
