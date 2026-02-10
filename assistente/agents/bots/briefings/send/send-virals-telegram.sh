#!/bin/bash
# send-virals-telegram.sh - Envia briefing de virais (múltiplas partes)

set -e

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

split_file() {
  local file="$1"
  local prefix="$2"
  python3 - <<'PY' "$file" "$prefix"
import sys
path, prefix = sys.argv[1], sys.argv[2]
max_len = 3500
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()
chunks = []
buf = ""
for line in lines:
    if len(buf) + len(line) > max_len and buf:
        chunks.append(buf)
        buf = ""
    buf += line
if buf:
    chunks.append(buf)
for i, chunk in enumerate(chunks, 1):
    out = f"{prefix}_{i}.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write(chunk)
print("\n".join(f"{prefix}_{i}.txt" for i in range(1, len(chunks)+1)))
PY
}

if [ -f /tmp/briefing-virals-parts.txt ]; then
  count=0
  total=$(wc -l < /tmp/briefing-virals-parts.txt)
  while IFS= read -r partfile || [ -n "$partfile" ]; do
    if [ -f "$partfile" ]; then
      split_prefix="/tmp/virals_split_$(basename "$partfile" .txt)"
      split_list=$(split_file "$partfile" "$split_prefix")
      while IFS= read -r chunkfile || [ -n "$chunkfile" ]; do
        [ -z "$chunkfile" ] && continue
        response=$(send_message "$chunkfile")
        if echo "$response" | jq -e '.ok == true' > /dev/null 2>&1; then
          echo "✅ Parte $((count+1))/$total enviada"
        else
          echo "❌ Erro na parte $((count+1)): $response" >&2
        fi
        sleep 1
      done < <(echo "$split_list")
      count=$((count + 1))
    fi
  done < /tmp/briefing-virals-parts.txt
  echo "✅ Virals briefing completo ($count partes) enviado às $(date '+%Y-%m-%d %H:%M:%S')"
elif [ -f /tmp/briefing-virals.txt ]; then
  response=$(send_message "/tmp/briefing-virals.txt")
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
