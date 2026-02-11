#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./send_to_telegram.sh "mensagem"
# Optional:
#   SEND_TELEGRAM_TARGET="telegram:<id>" ./send_to_telegram.sh "mensagem"

MSG="${1:-}"
if [[ -z "${MSG}" ]]; then
  echo "usage: $0 \"message\""
  exit 2
fi

SEND_TELEGRAM_TARGET="${SEND_TELEGRAM_TARGET:-}"

detect_telegram_target() {
  local sessions_json="${HOME}/.openclaw/agents/main/sessions/sessions.json"
  if [[ ! -f "${sessions_json}" ]]; then
    return 1
  fi
  python3 - <<'PY' "${sessions_json}" 2>/dev/null || true
import json, sys
p = sys.argv[1]
try:
  data = json.load(open(p, "r", encoding="utf-8"))
except Exception:
  sys.exit(0)
sess = data.get("agent:main:main") or {}
to = sess.get("lastTo") or sess.get("last_to") or ""
if isinstance(to, str) and to.startswith("telegram:"):
  print(to)
PY
}

if [[ -z "${SEND_TELEGRAM_TARGET}" ]]; then
  SEND_TELEGRAM_TARGET="$(detect_telegram_target || true)"
fi

if [[ -z "${SEND_TELEGRAM_TARGET}" ]]; then
  echo "ERROR: nao consegui detectar o target do Telegram. Use:"
  echo "  SEND_TELEGRAM_TARGET=\"telegram:<id>\" $0 \"mensagem\""
  exit 1
fi

if ! command -v openclaw >/dev/null 2>&1; then
  echo "ERROR: openclaw nao encontrado no PATH"
  exit 1
fi

openclaw message send --channel telegram --target "${SEND_TELEGRAM_TARGET}" --message "${MSG}" --json >/dev/null
echo "OK"

