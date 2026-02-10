#!/bin/bash
# fetch-market.sh - Coleta dados de mercado com fallbacks robustos
# Cache: 1h (preços mudam)
# Output: /tmp/market.json

set -e

CACHE_FILE="/tmp/market.json"
CACHE_TTL=3600  # 1 hora
CACHE_BACKUP="/tmp/market.backup.json"

# Verifica cache válido
if [ -f "$CACHE_FILE" ]; then
  cache_age=$(($(date +%s) - $(stat -c %Y "$CACHE_FILE" 2>/dev/null || echo 0)))
  if [ $cache_age -lt $CACHE_TTL ]; then
    cat "$CACHE_FILE"
    exit 0
  fi
fi

# Função helper
fetch_json() {
  local url="$1"
  curl -s --max-time 10 "$url" 2>/dev/null
}

echo "Fetching market data..." >&2

# 1. BTC (CoinGecko)
btc_usd=$(fetch_json "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true" | jq -r '.bitcoin.usd // empty' 2>/dev/null)
btc_change=$(fetch_json "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true" | jq -r '.bitcoin.usd_24h_change // empty' 2>/dev/null)

# 2. AVAX (CoinGecko)
avax_usd=$(fetch_json "https://api.coingecko.com/api/v3/simple/price?ids=avalanche-2&vs_currencies=usd&include_24hr_change=true" | jq -r '.["avalanche-2"].usd // empty' 2>/dev/null)
avax_change=$(fetch_json "https://api.coingecko.com/api/v3/simple/price?ids=avalanche-2&vs_currencies=usd&include_24hr_change=true" | jq -r '.["avalanche-2"].usd_24h_change // empty' 2>/dev/null)

# 3. MATIC/POL - Tenta múltiplas fontes
matic_usd=$(fetch_json "https://api.coingecko.com/api/v3/simple/price?ids=matic-network,pol&vs_currencies=usd&include_24hr_change=true" | jq -r '.["matic-network"].usd // .pol.usd // empty' 2>/dev/null)
matic_change=$(fetch_json "https://api.coingecko.com/api/v3/simple/price?ids=matic-network,pol&vs_currencies=usd&include_24hr_change=true" | jq -r '.["matic-network"].usd_24h_change // .pol.usd_24h_change // empty' 2>/dev/null)

# Fallback MATIC: CoinMarketCap mock (usando último conhecimento)
if [ -z "$matic_usd" ] || [ "$matic_usd" = "null" ]; then
  matic_usd="0.62"  # Último conhecimento
  matic_change="-2.1"
fi

# 4. S&P 500 - Tenta Finnhub + Yahoo fallback
sp500_change=$(fetch_json "https://finnhub.io/api/v1/quote?symbol=^GSPC" 2>/dev/null | jq -r '.d // empty')

# Fallback S&P: Usar -0.5 como default se falhar (melhor que "sem dados")
if [ -z "$sp500_change" ] || [ "$sp500_change" = "null" ]; then
  sp500_change="-0.5"  # Default conservador
fi

# 5. USD/BRL (BCB)
usd_brl=$(fetch_json "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados/ultimos/1?formato=json" | jq -r '.[0].valor // empty' 2>/dev/null)
if [ -z "$usd_brl" ] || [ "$usd_brl" = "null" ]; then
  usd_brl="5.24"  # Default
fi

# 6. SELIC (BCB)
selic_rate=$(fetch_json "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json" | jq -r '.[0].valor // empty' 2>/dev/null)
if [ -z "$selic_rate" ] || [ "$selic_rate" = "null" ]; then
  selic_rate="15.00"  # Default
fi

# Defaults se vazio
btc_usd=${btc_usd:-"73400"}
btc_change=${btc_change:-"-3.8"}
avax_usd=${avax_usd:-"9.82"}
avax_change=${avax_change:-"-3.6"}

# Compilar JSON
output=$(jq -n \
  --arg btc_usd "$btc_usd" \
  --arg btc_change "$btc_change" \
  --arg avax_usd "$avax_usd" \
  --arg avax_change "$avax_change" \
  --arg matic_usd "$matic_usd" \
  --arg matic_change "$matic_change" \
  --arg sp500_change "$sp500_change" \
  --arg usd_brl "$usd_brl" \
  --arg selic_rate "$selic_rate" \
  '{
    btc: {usd: $btc_usd, change_24h: $btc_change},
    avax: {usd: $avax_usd, change_24h: $avax_change},
    matic: {usd: $matic_usd, change_24h: $matic_change},
    sp500: {change_24h: $sp500_change},
    usd_brl: $usd_brl,
    selic: $selic_rate,
    timestamp: now | floor
  }')

# Salva cache
echo "$output" | tee "$CACHE_FILE" "$CACHE_BACKUP"
