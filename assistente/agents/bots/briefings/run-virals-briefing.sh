#!/bin/bash
# run-virals-briefing.sh - Orquestrador do briefing de virais

set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[1/3] Fetching virals..."
bash "$DIR/fetch/fetch-virals.sh" > /dev/null

echo "[2/3] Compiling briefing..."
bash "$DIR/compile/compile-virals.sh" > /dev/null

echo "[3/3] Sending to Telegram..."
bash "$DIR/send/send-virals-telegram.sh"
