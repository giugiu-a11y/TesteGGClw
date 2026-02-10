#!/bin/bash
# compile-market.sh - Formata dados em linhas separadas
# Input: /tmp/market.json
# Output: stdout + /tmp/briefing-market.txt

market=$(cat /tmp/market.json)

btc=$(echo "$market" | jq -r '.btc.usd')
btc=$(echo "$btc" | awk '{if ($1 > 1000) printf "%.1fk", $1/1000; else print $1}')
btc_ch_raw=$(echo "$market" | jq -r '.btc.change_24h')
btc_ch=$(echo "$btc_ch_raw" | awk '{printf "%.1f", $1}')

avax=$(echo "$market" | jq -r '.avax.usd')
avax_ch_raw=$(echo "$market" | jq -r '.avax.change_24h')
avax_ch=$(echo "$avax_ch_raw" | awk '{printf "%.1f", $1}')

matic=$(echo "$market" | jq -r '.matic.usd')
if [ "$matic" = "N/A" ]; then
  matic_ch="N/A"
else
  matic_ch_raw=$(echo "$market" | jq -r '.matic.change_24h')
  matic_ch=$(echo "$matic_ch_raw" | awk '{printf "%.1f", $1}')
fi

sp500=$(echo "$market" | jq -r '.sp500.change_24h')
if [ "$sp500" != "N/A" ]; then
  sp500=$(printf "%.2f" "$sp500")
fi

usdbrl=$(echo "$market" | jq -r '.usd_brl')
selic=$(echo "$market" | jq -r '.selic')

# Formata conforme template solicitado
btc_format="N/A"
avax_format="N/A"
matic_format="N/A"

[ "$btc" != "N/A" ] && btc_format="\$$btc ($btc_ch%)"
[ "$avax" != "N/A" ] && avax_format="\$$avax ($avax_ch%)"
[ "$matic" != "N/A" ] && matic_format="\$$matic ($matic_ch%)" || matic_format="\$?"

# S&P/FX
sp500_format="sem dados"
[ "$sp500" != "N/A" ] && sp500_format="$sp500%"

# Selic
selic_format="sem dados"
[ "$selic" != "N/A" ] && selic_format="$selic%"

# Análise de risco/oportunidade baseada nos dados
risk_opp="⚠️ Risco/Oportunidade:"

# Parse números para análise
btc_num=$(echo "$btc_ch" | tr -d '()%')
avax_num=$(echo "$avax_ch" | tr -d '()%')
matic_num=$(echo "$matic_ch" | tr -d '()%N/A')
sp500_num=$(echo "$sp500" | tr -d '%')

# Conta negativos
neg_count=0
[ $(echo "$btc_num < 0" | bc 2>/dev/null) -eq 1 ] && ((neg_count++))
[ $(echo "$avax_num < 0" | bc 2>/dev/null) -eq 1 ] && ((neg_count++))

# Gera insight
if [ "$neg_count" -ge 2 ]; then
  # Maioria em queda = correção
  if [ "$sp500_num" != "N/A" ] && [ $(echo "$sp500_num < 0" | bc 2>/dev/null) -eq 1 ]; then
    risk_opp="$risk_opp Correção geral (cripto + S&P); oportunidade em acúmulo BTC sub-70k"
  else
    risk_opp="$risk_opp Cripto em correção; AVAX acumula abaixo de $10; BTC suporta em $72k"
  fi
else
  # Mercado misto
  risk_opp="$risk_opp Mercado misto; AVAX resiliente; Selic elevada reduz apetite risco"
fi

{
  echo "₿ BTC: $btc_format"
  echo "🔺 AVAX: $avax_format"
  echo "🔷 MATIC/POL: $matic_format"
  echo "📈 S&P/FX: $sp500_format"
  echo "🏦 Selic: $selic_format"
  echo "$risk_opp"
} | tee /tmp/briefing-market.txt
