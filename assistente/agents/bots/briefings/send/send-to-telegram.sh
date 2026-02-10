#!/bin/bash
# send-to-telegram.sh - Envia briefing para bot assistente

# Configuração
BOT_TOKEN="${BOT_ASSISTENTE_TOKEN:-}"
CHAT_ID="${BOT_ASSISTENTE_CHAT:-}"

# Lê briefing
briefing=$(cat /tmp/briefing-market.txt)

if [ -z "$briefing" ]; then
  echo "Erro: briefing vazio" >&2
  exit 1
fi
if [ -z "$BOT_TOKEN" ] || [ -z "$CHAT_ID" ]; then
  echo "Erro: BOT_ASSISTENTE_TOKEN/BOT_ASSISTENTE_CHAT não configurados" >&2
  exit 1
fi

# Envia
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${briefing}" \
  2>/dev/null

echo "✅ Briefing enviado às $(date '+%Y-%m-%d %H:%M:%S')" >&2
