#!/bin/bash
# send-news-telegram.sh - Envia briefing em múltiplas partes

set -e

# Carrega secrets
if [ -f ~/.config/secrets.env ]; then
  source ~/.config/secrets.env
fi

TOKEN="${BOT_ASSISTENTE_TOKEN:-}"
CHAT="${BOT_ASSISTENTE_CHAT:-}"

if [ -z "$TOKEN" ] || [ -z "$CHAT" ]; then
  echo "Erro: BOT_ASSISTENTE_TOKEN ou BOT_ASSISTENTE_CHAT não configurado" >&2
  exit 1
fi

send_message() {
  local file="$1"
  local message=$(cat "$file")
  
  curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
    -H "Content-Type: application/json" \
    -d "{
      \"chat_id\": \"$CHAT\",
      \"text\": $(echo "$message" | jq -Rs .),
      \"disable_web_page_preview\": true
    }"
}

# Verifica se tem partes
if [ -f /tmp/briefing-news-parts.txt ]; then
  count=0
  total=$(wc -l < /tmp/briefing-news-parts.txt)
  
  while IFS= read -r partfile || [ -n "$partfile" ]; do
    if [ -f "$partfile" ]; then
      response=$(send_message "$partfile")
      
      if echo "$response" | jq -e '.ok == true' > /dev/null 2>&1; then
        count=$((count + 1))
        echo "✅ Parte $count/$total enviada"
      else
        echo "❌ Erro na parte $count: $response" >&2
      fi
      
      sleep 1
    fi
  done < /tmp/briefing-news-parts.txt
  
  echo "✅ News briefing completo ($count partes) enviado às $(date '+%Y-%m-%d %H:%M:%S')"
  
elif [ -f /tmp/briefing-news.txt ]; then
  # Fallback: arquivo único
  response=$(send_message "/tmp/briefing-news.txt")
  if echo "$response" | jq -e '.ok == true' > /dev/null 2>&1; then
    echo "✅ Briefing enviado (1 parte)"
  else
    echo "❌ Erro: $response" >&2
    exit 1
  fi
else
  echo "Erro: Nenhum arquivo de briefing encontrado" >&2
  exit 1
fi
