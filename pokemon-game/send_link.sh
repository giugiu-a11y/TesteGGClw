#!/usr/bin/env bash
set -euo pipefail

# Send the GitHub Pages link to Telegram.
# Usage:
#   ./send_link.sh
# Optional:
#   TELEGRAM_CHAT_ID=881840168 ./send_link.sh
#
# Note: requires outbound network access from this machine.

CHAT_ID="${TELEGRAM_CHAT_ID:-881840168}"
URL="https://giugiu-a11y.github.io/TesteGGClw/"
MSG="Link do jogo (GitHub Pages): ${URL}

Se nao abrir ainda, espera 2-5 min e tenta de novo (Actions pode estar deployando)."

if ! command -v curl >/dev/null 2>&1; then
  echo "ERROR: curl nao encontrado."
  echo "${URL}"
  exit 1
fi

TOKEN="$(
python3 - <<'PY'
import json, os
paths = [
  os.path.expanduser("~/.openclaw/openclaw.json"),
  os.path.expanduser("~/.openclaw/clawdbot.json"),
]
for p in paths:
  if not os.path.exists(p):
    continue
  try:
    d = json.load(open(p, "r", encoding="utf-8"))
  except Exception:
    continue
  tok = ((d.get("channels") or {}).get("telegram") or {}).get("botToken")
  if isinstance(tok, str) and tok.strip():
    print(tok.strip())
    break
PY
)"

if [[ -z "${TOKEN}" ]]; then
  echo "ERROR: nao achei botToken em ~/.openclaw/{openclaw.json,clawdbot.json}"
  echo "${URL}"
  exit 1
fi

curl -fsS \
  -X POST \
  -d "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${MSG}" \
  -d "disable_web_page_preview=true" \
  "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  >/dev/null

echo "SENT"

