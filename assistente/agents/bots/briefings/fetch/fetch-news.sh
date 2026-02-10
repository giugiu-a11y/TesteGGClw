#!/bin/bash
# fetch-news.sh - Coleta notícias via NewsAPI (8 categorias)
# Cache: 6h | Output: /tmp/news.json

set -e

CACHE_FILE="/tmp/news.json"
CACHE_TTL=21600

# Verifica cache
if [ -f "$CACHE_FILE" ]; then
  cache_age=$(($(date +%s) - $(stat -c %Y "$CACHE_FILE" 2>/dev/null || echo 0)))
  if [ $cache_age -lt $CACHE_TTL ]; then
    cat "$CACHE_FILE"
    exit 0
  fi
fi

echo "Fetching news (NewsAPI - 8 categorias)..." >&2

# Carrega chave
if [ -f ~/.config/secrets.env ]; then
  export $(cat ~/.config/secrets.env | grep "NEWSAPI_KEY" | xargs)
fi

KEY="${NEWSAPI_KEY:-}"
if [ -z "$KEY" ]; then
  echo "Erro: NEWSAPI_KEY não configurada" >&2
  exit 1
fi

# Função para fetch
fetch_news() {
  local query="$1"
  local lang="${2:-pt}"
  local result=$(curl -s "https://newsapi.org/v2/everything?q=$query&language=$lang&sortBy=publishedAt&pageSize=5&apiKey=$KEY" 2>/dev/null)
  echo "$result" | jq -c '[.articles[0:5] | .[] | select(.title != null and .title != "") | {title: .title, source: .source.name}]' 2>/dev/null || echo '[]'
}

# ═══════════════════════════════════════════════════════════
# FETCH - 8 Categorias
# ═══════════════════════════════════════════════════════════

echo "  1/8: Bolsas Exterior..." >&2
bolsas=$(fetch_news "Fulbright%20OR%20Chevening%20OR%20DAAD%20OR%20scholarship%20international%20OR%20bolsa%20exterior" "en")
sleep 1

echo "  2/8: Intercâmbio..." >&2
intercambio=$(fetch_news "study%20abroad%20OR%20exchange%20program%20OR%20international%20student" "en")
sleep 1

echo "  3/8: Vistos & Imigração..." >&2
vistos=$(fetch_news "student%20visa%20OR%20H1B%20OR%20digital%20nomad%20visa%20OR%20immigration%20policy" "en")
sleep 1

echo "  4/8: Carreira Internacional..." >&2
carreira=$(fetch_news "remote%20work%20international%20OR%20global%20career%20OR%20work%20abroad" "en")
sleep 1

echo "  5/8: Geopolítica..." >&2
geopolitica=$(fetch_news "immigration%20policy%20USA%20OR%20Europe%20visa%20OR%20Trump%20immigration%20OR%20international%20relations" "en")
sleep 1

echo "  6/8: Economia BR..." >&2
economia=$(fetch_news "dolar%20real%20OR%20Brazil%20economy%20OR%20selic%20OR%20Brazilian%20currency" "en")
sleep 1

echo "  7/8: EdTech & M&A..." >&2
edtech=$(fetch_news "edtech%20acquisition%20OR%20education%20merger%20OR%20edtech%20funding%20OR%20education%20investment" "en")
sleep 1

echo "  8/8: Setor Educação..." >&2
educacao=$(fetch_news "higher%20education%20OR%20university%20news%20OR%20education%20sector%20OR%20college%20enrollment" "en")

# ═══════════════════════════════════════════════════════════
# COMPILAR JSON FINAL
# ═══════════════════════════════════════════════════════════

output=$(jq -n \
  --argjson bolsas "$bolsas" \
  --argjson intercambio "$intercambio" \
  --argjson vistos "$vistos" \
  --argjson carreira "$carreira" \
  --argjson geopolitica "$geopolitica" \
  --argjson economia "$economia" \
  --argjson edtech "$edtech" \
  --argjson educacao "$educacao" \
  '{
    bolsas_exterior: $bolsas,
    intercambio: $intercambio,
    vistos_imigracao: $vistos,
    carreira_internacional: $carreira,
    geopolitica: $geopolitica,
    economia_brasil: $economia,
    edtech_ma: $edtech,
    setor_educacao: $educacao,
    timestamp: now | floor
  }')

echo "$output" | tee "$CACHE_FILE"
