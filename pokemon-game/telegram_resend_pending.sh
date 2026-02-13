#!/usr/bin/env bash
set -euo pipefail

# Resend pending Telegram payload saved by telegram_send.sh.
# Usage:
#   ./telegram_resend_pending.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PENDING_FILE="${ROOT_DIR}/.runtime/telegram.pending.json"

if [[ ! -f "${PENDING_FILE}" ]]; then
  echo "NO_PENDING"
  exit 0
fi

CHAT_ID="$(python3 - <<'PY' "${PENDING_FILE}"
import json, sys
d=json.load(open(sys.argv[1], "r", encoding="utf-8"))
print(d.get("chat_id",""))
PY
)"
MSG="$(python3 - <<'PY' "${PENDING_FILE}"
import json, sys
d=json.load(open(sys.argv[1], "r", encoding="utf-8"))
print(d.get("message",""))
PY
)"
RETRIES="$(python3 - <<'PY' "${PENDING_FILE}"
import json, sys
d=json.load(open(sys.argv[1], "r", encoding="utf-8"))
print(d.get("retries",18))
PY
)"
RETRY_DELAY="$(python3 - <<'PY' "${PENDING_FILE}"
import json, sys
d=json.load(open(sys.argv[1], "r", encoding="utf-8"))
print(d.get("retry_delay",2))
PY
)"

TELEGRAM_CHAT_ID="${CHAT_ID}" TELEGRAM_RETRIES="${RETRIES}" TELEGRAM_RETRY_DELAY="${RETRY_DELAY}" \
  "${ROOT_DIR}/telegram_send.sh" "${MSG}"
