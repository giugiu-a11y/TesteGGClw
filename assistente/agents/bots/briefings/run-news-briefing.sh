#!/bin/bash
# run-news-briefing.sh - Orquestrador notícias (fetch → compile → send)

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/news-briefing-$(date +%Y%m%d_%H%M%S).log"

# Carrega secrets
if [ -f ~/.config/secrets.env ]; then
  export $(cat ~/.config/secrets.env | grep "BOT_ASSISTENTE\|NEWSAPI" | xargs)
fi

{
  echo "=== News Briefing - $(date '+%Y-%m-%d %H:%M:%S') ==="
  
  # 1. Fetch notícias
  echo "[1/3] Fetching news data..."
  bash "$DIR/fetch/fetch-news.sh" > /dev/null
  
  # 2. Compile
  echo "[2/3] Compiling news briefing..."
  bash "$DIR/compile/compile-news.sh"
  
  # 3. Send
  echo "[3/3] Sending to Telegram..."
  bash "$DIR/send/send-news-telegram.sh"
  
  echo "=== Done ==="
  
} | tee -a "$LOG_FILE"
