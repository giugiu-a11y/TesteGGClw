#!/usr/bin/env bash
set -euo pipefail

# Starts a local static server for pokemon-game and exposes it via localtunnel.
# Intended to be run on the AWS box (not in a restricted sandbox).
#
# Important: localtunnel is flaky. In WATCH mode, this script restarts the tunnel if it dies
# and re-sends the URL/password via Telegram.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${PORT:-8000}"
TUNNEL_WAIT_SECONDS="${TUNNEL_WAIT_SECONDS:-60}"
WATCH="${WATCH:-1}"            # 1: restart tunnel if it dies (recommended)
WATCH_SLEEP_SECONDS="${WATCH_SLEEP_SECONDS:-2}"

LOG_DIR="${ROOT_DIR}/.runtime"
mkdir -p "${LOG_DIR}"

SERVER_LOG="${LOG_DIR}/http-server.log"
TUNNEL_LOG="${LOG_DIR}/tunnel.log"
PID_SERVER="${LOG_DIR}/http-server.pid"
PID_TUNNEL="${LOG_DIR}/tunnel.pid"
URL_FILE="${LOG_DIR}/tunnel.url"
PORT_FILE="${LOG_DIR}/port.txt"

# Optional: auto-send the tunnel URL/password via OpenClaw Telegram.
# You can override by setting SEND_TELEGRAM_TARGET="telegram:<id>" (or "@channel").
# If unset, we'll try to auto-detect the last Telegram recipient from OpenClaw state.
SEND_TELEGRAM_TARGET="${SEND_TELEGRAM_TARGET:-}"

port_is_free() {
  local p="$1"
  python3 - "$p" 2>/dev/null <<'PY'
import socket, sys
p=int(sys.argv[1])
s=socket.socket()
try:
  s.bind(("0.0.0.0", p))
except OSError:
  sys.exit(1)
finally:
  try: s.close()
  except Exception: pass
sys.exit(0)
PY
}

pick_free_port() {
  local start="$1"
  local p="$start"
  local max=8100
  while [[ "$p" -le "$max" ]]; do
    if port_is_free "$p"; then
      echo "$p"
      return 0
    fi
    p=$((p + 1))
  done
  return 1
}

extract_tunnel_url() {
  local log_path="$1"
  python3 - "$log_path" 2>/dev/null <<'PY'
import re, sys, os
p=sys.argv[1]
if not p or not os.path.exists(p):
  sys.exit(0)
try:
  s=open(p,'r',encoding='utf-8',errors='ignore').read()
except Exception:
  sys.exit(0)
m=re.search(r'https://[a-z0-9-]+\.loca\.lt', s)
if m:
  print(m.group(0))
PY
}

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
  # Prefer env, else read from OpenClaw config files.
  if [[ -n "${TELEGRAM_BOT_TOKEN:-}" ]]; then
    echo "${TELEGRAM_BOT_TOKEN}"
    return 0
  fi
  local p1="${HOME}/.openclaw/openclaw.json"
  local p2="${HOME}/.openclaw/clawdbot.json"
  python3 - <<'PY' "$p1" "$p2" 2>/dev/null || true
import json, sys, os
paths=[p for p in sys.argv[1:] if p and os.path.exists(p)]
for p in paths:
  try:
    d=json.load(open(p,"r",encoding="utf-8"))
  except Exception:
    continue
  tok=(((d.get("channels") or {}).get("telegram") or {}).get("botToken"))
  if isinstance(tok,str) and tok.strip():
    print(tok.strip())
    break
PY
}

send_telegram_message_curl() {
  local target="$1" # telegram:123 or numeric
  local msg="$2"
  local bot_token
  bot_token="$(detect_telegram_bot_token || true)"
  if [[ -z "${bot_token}" ]]; then
    return 1
  fi
  local chat_id="${target#telegram:}"
  if [[ -z "${chat_id}" ]]; then
    return 1
  fi
  # Best-effort; don't leak token to logs.
  curl -fsS \
    -X POST \
    -d "chat_id=${chat_id}" \
    --data-urlencode "text=${msg}" \
    -d "disable_web_page_preview=true" \
    "https://api.telegram.org/bot${bot_token}/sendMessage" \
    >/dev/null 2>&1 || return 1
  return 0
}

send_telegram_message() {
  local target="$1"
  local msg="$2"
  if [[ -z "${target}" ]]; then
    return 0
  fi
  if ! command -v openclaw >/dev/null 2>&1; then
    # Fallback to direct Telegram API call.
    send_telegram_message_curl "${target}" "${msg}" || true
    return 0
  fi
  # Best-effort. If it fails, keep the tunnel running.
  openclaw message send --channel telegram --target "${target}" --message "${msg}" >/dev/null 2>&1 || \
    send_telegram_message_curl "${target}" "${msg}" || true
}

cleanup_children() {
  if [[ -f "${PID_TUNNEL}" ]]; then
    local p
    p="$(cat "${PID_TUNNEL}" 2>/dev/null || true)"
    if [[ -n "${p}" ]] && kill -0 "${p}" 2>/dev/null; then
      kill "${p}" 2>/dev/null || true
    fi
  fi
  if [[ -f "${PID_SERVER}" ]]; then
    local p
    p="$(cat "${PID_SERVER}" 2>/dev/null || true)"
    if [[ -n "${p}" ]] && kill -0 "${p}" 2>/dev/null; then
      kill "${p}" 2>/dev/null || true
    fi
  fi
}
trap cleanup_children INT TERM HUP

if [[ -z "${SEND_TELEGRAM_TARGET}" ]]; then
  SEND_TELEGRAM_TARGET="$(detect_telegram_target || true)"
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "[pokemon-game] ERROR: npx not found. Install Node.js/npm first."
  exit 1
fi

first=1
while :; do
  start_port="${PORT}"
  PORT="$(pick_free_port "${PORT}" || true)"
  if [[ -z "${PORT}" ]]; then
    echo "[pokemon-game] ERROR: could not find a free port starting from ${start_port}."
    exit 1
  fi

  rm -f "${SERVER_LOG}" "${TUNNEL_LOG}" "${URL_FILE}" "${PID_SERVER}" "${PID_TUNNEL}" "${PORT_FILE}" || true

  echo "[pokemon-game] Starting http.server on port ${PORT} (dir: ${ROOT_DIR})"
  echo "${PORT}" >"${PORT_FILE}" 2>/dev/null || true
  python3 -m http.server "${PORT}" --directory "${ROOT_DIR}" >"${SERVER_LOG}" 2>&1 &
  SERVER_PID="$!"
  echo "${SERVER_PID}" >"${PID_SERVER}" 2>/dev/null || true

  sleep 0.5
  if ! kill -0 "${SERVER_PID}" 2>/dev/null; then
    echo "[pokemon-game] ERROR: server failed to start. Log:"
    tail -n 60 "${SERVER_LOG}" || true
    exit 1
  fi

  echo "[pokemon-game] Starting localtunnel for port ${PORT} (this requires network access)"
  rm -f "${TUNNEL_LOG}" "${URL_FILE}"
  npx --yes localtunnel --port "${PORT}" >"${TUNNEL_LOG}" 2>&1 &
  TUNNEL_PID="$!"
  echo "${TUNNEL_PID}" >"${PID_TUNNEL}" 2>/dev/null || true

  TUNNEL_URL=""
  deadline=$(( $(date +%s) + TUNNEL_WAIT_SECONDS ))
  while [[ -z "${TUNNEL_URL}" ]] && [[ "$(date +%s)" -lt "${deadline}" ]]; do
    TUNNEL_URL="$(extract_tunnel_url "${TUNNEL_LOG}" || true)"
    sleep 0.5
  done

  if [[ -n "${TUNNEL_URL}" ]]; then
    echo "[pokemon-game] Tunnel URL: ${TUNNEL_URL}"
    echo "${TUNNEL_URL}" >"${URL_FILE}" 2>/dev/null || true

    PASS=""
    if command -v curl >/dev/null 2>&1; then
      PASS="$(curl -fsSL https://loca.lt/mytunnelpassword 2>/dev/null || true)"
    elif command -v wget >/dev/null 2>&1; then
      PASS="$(wget -q -O - https://loca.lt/mytunnelpassword 2>/dev/null || true)"
    fi

    if [[ -n "${PASS}" ]]; then
      echo "[pokemon-game] Tunnel password (public IP): ${PASS}"
    fi

    if [[ -n "${SEND_TELEGRAM_TARGET}" ]]; then
      MSG="[pokemon-game] Tunnel pronto\nURL: ${TUNNEL_URL}"
      if [[ -n "${PASS}" ]]; then
        MSG="${MSG}\nSenha: ${PASS}"
      else
        MSG="${MSG}\nSenha: (rode: curl https://loca.lt/mytunnelpassword)"
      fi
      # Avoid spamming on the very first boot if desired. Default: send always.
      send_telegram_message "${SEND_TELEGRAM_TARGET}" "${MSG}"
    fi
  else
    echo "[pokemon-game] WARN: did not find tunnel URL within ${TUNNEL_WAIT_SECONDS}s."
    tail -n 60 "${TUNNEL_LOG}" || true
  fi

  # Wait until localtunnel dies (or we get killed). Then loop if WATCH=1.
  wait "${TUNNEL_PID}" 2>/dev/null || true
  # Stop the http server from this iteration too, to avoid leaking ports.
  if kill -0 "${SERVER_PID}" 2>/dev/null; then
    kill "${SERVER_PID}" 2>/dev/null || true
  fi

  if [[ "${WATCH}" != "1" ]]; then
    exit 0
  fi

  if [[ "${first}" == "1" ]]; then
    echo "[pokemon-game] WATCH mode ativo (vai reiniciar se cair)."
    first=0
  fi
  sleep "${WATCH_SLEEP_SECONDS}"
done
