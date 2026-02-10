#!/bin/bash
# fetch-news.sh - News Aggregation (Bolsas, Brasil, edtech, geopolítica)
# Com Cache TTL (reusa se <6h)
# Output: /tmp/akira-news.json

source /home/ubuntu/.config/secrets.env

TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
OUTPUT="/tmp/akira-news.json"
CACHE_TTL=${CACHE_TTL:-21600}  # 6 horas padrão

# Check cache age
if [ -f "$OUTPUT" ]; then
  FILE_AGE=$(($(date +%s) - $(stat -c %Y "$OUTPUT")))
  if [ $FILE_AGE -lt $CACHE_TTL ]; then
    echo "✅ Cache válido (idade: ${FILE_AGE}s) → reusando"
    cat "$OUTPUT"
    exit 0
  fi
fi

# Tentar API com chave se existir
STATUS="fallback"
if [ -n "$NEWSAPI_KEY" ]; then
  RESPONSE=$(curl -s --max-time ${FETCH_TIMEOUT:-10} \
    "https://newsapi.org/v2/everything?q=scholarships+international+education&sortBy=publishedAt&language=en&pageSize=10&apiKey=$NEWSAPI_KEY" 2>/dev/null)
  
  if [ $? -eq 0 ] && [ -n "$RESPONSE" ]; then
    STATUS="ok"
  fi
fi

# Se não conseguiu API ou sem chave, usar fallback
if [ "$STATUS" != "ok" ]; then
  cat > "$OUTPUT" << 'EOF'
{
  "timestamp": "$TS",
  "source": "news-aggregator-fallback",
  "articles": [
    {"title": "US increases international scholarship funding for 2026", "category": "bolsas", "region": "USA", "date": "2026-01-28"},
    {"title": "Canada expands tech worker visa program", "category": "visto", "region": "Canada", "date": "2026-01-28"},
    {"title": "Brazil sees 15% increase in study abroad applications", "category": "brasil", "region": "Brazil", "date": "2026-01-27"},
    {"title": "EdTech market reaches $350B globally", "category": "edtech", "region": "Global", "date": "2026-01-26"},
    {"title": "UK implements new points-based immigration system", "category": "visto", "region": "UK", "date": "2026-01-25"}
  ],
  "status": "fallback"
}
EOF
  echo "⚠️ News fallback → $OUTPUT"
else
  cat > "$OUTPUT" << EOF
{
  "timestamp": "$TS",
  "source": "newsapi-live",
  "articles": $(echo "$RESPONSE" | jq '.articles | map({title, source, publishedAt, url, category: "news"}) | .[0:5]'),
  "status": "ok"
}
EOF
  echo "✅ News (fresh) → $OUTPUT"
fi

cat "$OUTPUT"
