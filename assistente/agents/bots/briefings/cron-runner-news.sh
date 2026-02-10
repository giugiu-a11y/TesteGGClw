#!/bin/bash
# cron-runner-news.sh - Lock wrapper para notícias

LOCK_FILE="/tmp/news-briefing.lock"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Obtém lock
exec 200>"$LOCK_FILE"
flock -n 200 || {
  echo "News briefing já em execução. Aguarde..." >&2
  exit 1
}

# Carrega secrets
if [ -f ~/.config/secrets.env ]; then
  export $(cat ~/.config/secrets.env | grep "BOT_ASSISTENTE\|NEWSAPI" | xargs)
fi

# Executa
bash "$DIR/run-news-briefing.sh"

# Libera lock
flock -u 200
