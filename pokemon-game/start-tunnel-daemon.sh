#!/usr/bin/env bash
set -euo pipefail

# Daemon launcher for start-tunnel.sh that survives disconnects.
# Uses setsid to detach from the current session.
#
# Usage:
#   bash ./start-tunnel-daemon.sh
#
# Stop:
#   bash ./stop-tunnel-daemon.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${ROOT_DIR}/.runtime"
mkdir -p "${LOG_DIR}"

DAEMON_LOG="${LOG_DIR}/tunnel-daemon.log"
DAEMON_PIDFILE="${LOG_DIR}/tunnel-daemon.pid"

if ! command -v setsid >/dev/null 2>&1; then
  echo "[pokemon-game] ERROR: setsid not found"
  exit 1
fi

if [[ -f "${DAEMON_PIDFILE}" ]]; then
  pid="$(cat "${DAEMON_PIDFILE}" 2>/dev/null || true)"
  if [[ -n "${pid}" ]] && kill -0 "${pid}" 2>/dev/null; then
    echo "[pokemon-game] daemon already running (pid=${pid})"
    exit 0
  fi
fi

# Run WATCH loop detached. We redirect output to a log file.
setsid -f bash -lc "cd '${ROOT_DIR}' && WATCH=1 bash ./start-tunnel.sh >>'${DAEMON_LOG}' 2>&1"

# Best-effort: find the newest start-tunnel.sh process and store it.
pid="$(ps aux | rg \"bash ./start-tunnel.sh\" | rg -v 'rg ' | tail -n 1 | awk '{print $2}' || true)"
if [[ -n "${pid}" ]]; then
  echo "${pid}" >"${DAEMON_PIDFILE}" 2>/dev/null || true
  echo "[pokemon-game] daemon started (pid=${pid})"
  echo "[pokemon-game] logs: ${DAEMON_LOG}"
else
  echo "[pokemon-game] daemon started (pid unknown). logs: ${DAEMON_LOG}"
fi

