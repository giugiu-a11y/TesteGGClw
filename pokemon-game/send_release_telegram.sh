#!/usr/bin/env bash
set -euo pipefail

MSG="${1:-Atualizacao publicada. Veja o link mais recente no GitHub Pages.}"
TARGET="telegram:881840168"

if command -v openclaw >/dev/null 2>&1; then
  if openclaw message send --channel telegram --target "$TARGET" --message "$MSG" --json >/tmp/send_release_telegram.log 2>&1; then
    echo "SENT_VIA_OPENCLOW"
    exit 0
  fi
fi

./send_link.sh
