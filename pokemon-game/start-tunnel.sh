#!/usr/bin/env bash
set -euo pipefail

# Starts a local static server for pokemon-game and exposes it via localtunnel.
# Intended to be run on the AWS box (not in a restricted sandbox).

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${PORT:-8000}"

LOG_DIR="${ROOT_DIR}/.runtime"
mkdir -p "${LOG_DIR}"

SERVER_LOG="${LOG_DIR}/http-server.log"
TUNNEL_LOG="${LOG_DIR}/tunnel.log"

cleanup() {
  if [[ -n "${SERVER_PID:-}" ]] && kill -0 "${SERVER_PID}" 2>/dev/null; then
    kill "${SERVER_PID}" 2>/dev/null || true
  fi
}
trap cleanup EXIT

echo "[pokemon-game] Starting http.server on port ${PORT} (dir: ${ROOT_DIR})"
nohup python3 -m http.server "${PORT}" --directory "${ROOT_DIR}" >"${SERVER_LOG}" 2>&1 &
SERVER_PID="$!"

sleep 0.5

if ! kill -0 "${SERVER_PID}" 2>/dev/null; then
  echo "[pokemon-game] ERROR: server failed to start. Log:"
  tail -n 50 "${SERVER_LOG}" || true
  exit 1
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "[pokemon-game] ERROR: npx not found. Install Node.js/npm first."
  exit 1
fi

echo "[pokemon-game] Starting localtunnel for port ${PORT} (this requires network access)"
echo "[pokemon-game] Tunnel log: ${TUNNEL_LOG}"

# localtunnel prints the public URL to stdout.
set +e
TUNNEL_URL="$(npx --yes localtunnel --port "${PORT}" 2>>"${TUNNEL_LOG}" | head -n 1)"
set -e

if [[ -z "${TUNNEL_URL}" ]]; then
  echo "[pokemon-game] ERROR: localtunnel did not return a URL. Last log lines:"
  tail -n 50 "${TUNNEL_LOG}" || true
  exit 1
fi

echo "[pokemon-game] Tunnel URL: ${TUNNEL_URL}"

PASS=""
if command -v curl >/dev/null 2>&1; then
  PASS="$(curl -fsSL https://loca.lt/mytunnelpassword 2>/dev/null || true)"
elif command -v wget >/dev/null 2>&1; then
  PASS="$(wget -q -O - https://loca.lt/mytunnelpassword 2>/dev/null || true)"
fi

if [[ -n "${PASS}" ]]; then
  echo "[pokemon-game] Tunnel password (public IP): ${PASS}"
else
  echo "[pokemon-game] Tunnel password not fetched automatically."
  echo "[pokemon-game] Run: curl https://loca.lt/mytunnelpassword"
fi

echo "[pokemon-game] Press Ctrl+C to stop."
wait

