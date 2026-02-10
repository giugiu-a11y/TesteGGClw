#!/bin/bash
# cron-runner.sh - Lock wrapper para rodar briefing (evita execuções simultâneas)

LOCK_FILE="/tmp/market-briefing.lock"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Obtém lock (timeout 60s)
exec 200>"$LOCK_FILE"
flock -n 200 || {
  echo "Market briefing já em execução. Aguarde..." >&2
  exit 1
}

# Carrega secrets de lugar seguro (chmod 600)
if [ -f ~/.config/secrets.env ]; then
  export $(cat ~/.config/secrets.env | grep "BOT_ASSISTENTE\|^[^#]" | xargs)
fi

# Executa briefing
bash "$DIR/run-market-briefing.sh"

# Libera lock
flock -u 200
