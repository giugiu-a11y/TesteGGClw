#!/bin/bash
set -euo pipefail

check() {
  local name="$1"; shift
  local proc="$1"; shift
  if ! pgrep -f "$proc" >/dev/null 2>&1; then
    echo "[$(date -u +%FT%TZ)] restarting $name" >> /tmp/bot-healthcheck.log
    nohup "$@" >/tmp/${name}.supervisor.log 2>&1 &
  fi
}

check "assistente-opus" "/home/ubuntu/clawd/sessions/assistente-opus/bot.py" /home/ubuntu/clawd/sessions/assistente-opus/run.sh
check "personajes" "/home/ubuntu/clawd/sessions/personajes/bot.py" /home/ubuntu/clawd/sessions/personajes/run.sh
check "m60-atendimento" "/home/ubuntu/clawd/sessions/m60-atendimento/bot.py" /home/ubuntu/clawd/sessions/m60-atendimento/run.sh
