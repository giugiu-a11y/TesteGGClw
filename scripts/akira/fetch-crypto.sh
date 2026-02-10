#!/bin/bash
# fetch-crypto.sh - Cryptocurrency Prices (BTC, AVAX, MATIC/POL)
# Com Cache TTL (reusa se <6h)
# Output: /tmp/akira-crypto.json

source /home/ubuntu/.config/secrets.env

TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
OUTPUT="/tmp/akira-crypto.json"
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

# Fetch novo com timeout
RESPONSE=$(curl -s --max-time ${FETCH_TIMEOUT:-10} \
  "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,avalanche-2,polygon&vs_currencies=usd&include_24hr_change=true&include_market_cap=true" 2>/dev/null)

if [ $? -eq 0 ] && [ -n "$RESPONSE" ]; then
  # Estruturar resposta
  cat > "$OUTPUT" << EOF
{
  "timestamp": "$TS",
  "source": "coingecko-api",
  "cache_age_seconds": 0,
  "prices": $RESPONSE,
  "portfolio_tokens": ["bitcoin", "avalanche-2", "polygon"],
  "status": "ok"
}
EOF
  echo "✅ Crypto prices (fresh) → $OUTPUT"
else
  # Fallback se API cair
  cat > "$OUTPUT" << 'EOF'
{
  "timestamp": "$TS",
  "source": "coingecko-fallback",
  "prices": {"bitcoin": {"usd": 94500, "usd_24h_change": 2.3}, "avalanche-2": {"usd": 45.20, "usd_24h_change": -1.2}, "polygon": {"usd": 1.85, "usd_24h_change": 3.5}},
  "status": "fallback"
}
EOF
  echo "⚠️ Crypto fallback → $OUTPUT"
fi

cat "$OUTPUT"
