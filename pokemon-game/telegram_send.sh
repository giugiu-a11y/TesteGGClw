#!/usr/bin/env bash
set -euo pipefail

# Unified Telegram sender with retry + fallback.
# Usage:
#   ./telegram_send.sh "mensagem"
# Optional env:
#   TELEGRAM_CHAT_ID=881840168
#   TELEGRAM_RETRIES=18
#   TELEGRAM_RETRY_DELAY=2

MSG="${1:-}"
if [[ -z "${MSG}" ]]; then
  echo "usage: $0 \"mensagem\""
  exit 2
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNTIME_DIR="${ROOT_DIR}/.runtime"
mkdir -p "${RUNTIME_DIR}"

CHAT_ID="${TELEGRAM_CHAT_ID:-881840168}"
RETRIES="${TELEGRAM_RETRIES:-18}"
RETRY_DELAY="${TELEGRAM_RETRY_DELAY:-2}"
LAST_ERR_FILE="${RUNTIME_DIR}/telegram.last_error.log"
PENDING_FILE="${RUNTIME_DIR}/telegram.pending.json"

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

detect_telegram_bot_token() {
  if [[ -n "${TELEGRAM_BOT_TOKEN:-}" ]]; then
    echo "${TELEGRAM_BOT_TOKEN}"
    return 0
  fi
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
}

send_via_curl() {
  local token chat_id
  token="$(detect_telegram_bot_token || true)"
  chat_id="${CHAT_ID}"
  if [[ -z "${token}" || -z "${chat_id}" ]]; then
    return 1
  fi
  curl -fsS \
    -X POST \
    -d "chat_id=${chat_id}" \
    --data-urlencode "text=${MSG}" \
    -d "disable_web_page_preview=true" \
    "https://api.telegram.org/bot${token}/sendMessage" \
    >/dev/null
}

send_via_openclaw() {
  if ! command -v openclaw >/dev/null 2>&1; then
    return 1
  fi
  local target
  target="$(detect_telegram_target || true)"
  if [[ -z "${target}" ]]; then
    target="telegram:${CHAT_ID}"
  fi
  openclaw message send --channel telegram --target "${target}" --message "${MSG}" --json >/dev/null
}

record_pending() {
  python3 - <<'PY' "${PENDING_FILE}" "${CHAT_ID}" "${MSG}" "${RETRIES}" "${RETRY_DELAY}"
import json, os, sys, time
p, chat_id, msg, retries, retry_delay = sys.argv[1:]
payload = {
    "at": int(time.time()),
    "chat_id": chat_id,
    "message": msg,
    "retries": int(retries),
    "retry_delay": int(retry_delay),
}
tmp = p + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)
os.replace(tmp, p)
PY
}

last_err=""
for i in $(seq 1 "${RETRIES}"); do
  if send_via_curl 2>"${LAST_ERR_FILE}"; then
    echo "SENT_CURL attempt=${i}"
    rm -f "${PENDING_FILE}" "${LAST_ERR_FILE}" || true
    exit 0
  fi
  if send_via_openclaw 2>"${LAST_ERR_FILE}"; then
    echo "SENT_OPENCLOW attempt=${i}"
    rm -f "${PENDING_FILE}" "${LAST_ERR_FILE}" || true
    exit 0
  fi
  if [[ -f "${LAST_ERR_FILE}" ]]; then
    last_err="$(tail -n 1 "${LAST_ERR_FILE}" || true)"
  fi
  sleep "${RETRY_DELAY}"
done

record_pending
echo "FAILED_TO_SEND"
if [[ -n "${last_err}" ]]; then
  echo "last_error: ${last_err}"
fi
echo "pending_saved: ${PENDING_FILE}"
exit 1
