#!/bin/bash
# cron-runner-virals.sh - Lock wrapper para virais

LOCK_FILE="/tmp/virals-briefing.lock"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Obtém lock
exec 200>"$LOCK_FILE"
flock -n 200 || {
  echo "Virals briefing já em execução. Aguarde..." >&2
  exit 1
}

# Carrega secrets
if [ -f ~/.config/secrets.env ]; then
  export $(cat ~/.config/secrets.env | grep "BOT_ASSISTENTE" | xargs)
fi

# Executa
bash "$DIR/run-virals-briefing.sh"

# Libera lock
flock -u 200
