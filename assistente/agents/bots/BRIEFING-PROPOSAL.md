# Proposta: 3 Briefings Diários (Autônomo + Economia Token)

## 📊 Arquitetura

```
~/clawd/assistente/agents/bots/briefings/
├── config.env                    # Secrets (API keys, chat IDs)
├── briefing.sh                   # Orquestrador principal
├── fetch-virals.sh               # YouTube + TikTok + Google Trends
├── fetch-news.sh                 # 9 temas x 3 notícias
├── fetch-market.sh               # BTC, AVAX, MATIC, S&P, USD/BRL, Selic
├── compile.py                    # 1 call Haiku (batch tudo)
└── cron-runner.sh                # Lock + cron wrapper
```

## ⚡ Fluxo (Economy-First)

```
┌─────────────────────────────────────────────────────────────┐
│ CRON: 07:00 BRT (10:00 UTC) & 16:00 BRT (19:00 UTC)        │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
        ┌──────────────────────────────┐
        │  bash briefing.sh             │
        │  (cron-runner.sh lock)        │
        └──────────────┬────────────────┘
                       ▼
    ┌──────────────────────────────────────────┐
    │ COLETA (3 scripts em paralelo)           │
    ├──────────────────────────────────────────┤
    │ 1. fetch-virals.sh                       │
    │    └─ Check cache (4h)                   │
    │    └─ Se expirado: Google Trends RSS,   │
    │       YouTube Popular, TikTok Discover   │
    │    └─ Output: /tmp/virals.json           │
    │                                          │
    │ 2. fetch-news.sh                         │
    │    └─ Check cache (6h)                   │
    │    └─ Se expirado: NewsAPI + RSS feeds   │
    │    └─ Filtra 9 temas, top 3 cada         │
    │    └─ Output: /tmp/news.json             │
    │                                          │
    │ 3. fetch-market.sh                       │
    │    └─ Check cache (1h - preços mudam)    │
    │    └─ APIs: CoinGecko, IBGE, SELIC      │
    │    └─ Output: /tmp/market.json           │
    └──────────────────────────────────────────┘
                       ▼
        ┌──────────────────────────────┐
        │ compile.py                   │
        │ (1 call Haiku)               │
        │ Lê 3 JSONs → formata pretty  │
        │ Output: /tmp/briefing.txt    │
        └──────────────┬───────────────┘
                       ▼
        ┌──────────────────────────────┐
        │ send-to-telegram.sh           │
        │ POST direto ao Telegram API  │
        │ Chat: bot assistente          │
        └──────────────────────────────┘
```

## 💾 Cache Strategy

| Fonte | TTL | Por quê |
|-------|-----|---------|
| Virais (YouTube/TikTok/Trends) | 4h | Muda rápido, RSS é grátis |
| Notícias (NewsAPI + RSS) | 6h | Notícias novas a cada 12h |
| Mercado (cripto/S&P/Selic) | 1h | Preços mudam constantemente |

**Implementação:**
```bash
# Em cada script
cache_file="/tmp/briefing-virals-$(date +%s).json"
cache_age=$(($(date +%s) - $(stat -c %Y $cache_file 2>/dev/null || echo 0)))

if [ $cache_age -lt 14400 ]; then  # 4h = 14400s
  cat $cache_file
else
  fetch_novo && save_cache
fi
```

## 🔌 APIs Gratuitas

### 1. Virais
- **Google Trends:** Sem API (web scrape via `curl` + jq)
- **YouTube:** RSS `/feeds/videos.xml?channel_id=...` (grátis)
- **TikTok:** Discovery API (limitado mas grátis) ou RSS simulado

### 2. Notícias
- **NewsAPI:** 1 call/dia (plano free) ou RSS feeds
- **RSS Feeds:** Medium, Dev.to, etc (grátis, sem limite)
- **Google News:** RSS agregado

### 3. Mercado
- **CoinGecko:** Grátis, sem auth
- **IBGE/API Pública:** USD/BRL
- **BCB/SELIC:** API pública
- **S&P 500:** Twelve Data (free tier) ou Yahoo Finance

## 📝 Scripts (Pseudocódigo)

### fetch-virals.sh
```bash
#!/bin/bash
# Coleta 15 títulos (5 YouTube + 5 TikTok + 5 Google Trends)
# Cache: 4h
# Output: /tmp/virals.json

# YouTube (RSS + jq)
curl -s "https://www.youtube.com/feeds/videos.xml?channel_id=UCxxxxx" \
  | xmllint --format - | grep '<title>' | head -5 > yt.txt

# Google Trends (web scrape - deprecated, alternativa: RSS simulado)
# TikTok Discovery (mock ou RSS)

# Salva em JSON
jq -n '{youtube: [...], tiktok: [...], trends: [...]}' > /tmp/virals.json
```

### fetch-news.sh
```bash
#!/bin/bash
# 9 temas x 3 notícias = 27 notícias total
# Cache: 6h
# Output: /tmp/news.json

temas=(
  "bolsas de estudo exterior"
  "study abroad scholarships"
  "edtech M&A"
  "edtech funding"
  "imigração visto"
  "geopolítica"
  "Brasil economia"
)

# Para cada tema: NewsAPI + RSS
# Pega top 3, filtra por "brazilians" ou "brasileiros"
# Salva em /tmp/news.json

jq -n '{bolsas: [...], edtech_ma: [...], ...}' > /tmp/news.json
```

### fetch-market.sh
```bash
#!/bin/bash
# Cache: 1h (preços mudam)
# Output: /tmp/market.json

# CoinGecko (BTC, AVAX, MATIC)
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,avalanche-2,matic-network&vs_currencies=usd&include_24hr_change=true" \
  | jq '{btc: .bitcoin, avax: .avalanche, matic: .matic}' > /tmp/market.json

# S&P 500 + USD/BRL + SELIC
# Append ao JSON
```

### compile.py
```python
#!/usr/bin/env python3
import json, os
from datetime import datetime

virals = json.load(open('/tmp/virals.json'))
news = json.load(open('/tmp/news.json'))
market = json.load(open('/tmp/market.json'))

# Haiku call: formata em texto pretty
# 1 LLM call, não 3

prompt = f"""Formata esses 3 briefings em markdown super clean:
{json.dumps([virals, news, market])}

Regras:
- Virais: listas bullet (título só)
- Notícias: "TEMA > título (resumo 1-2 linhas)"
- Mercado: inline "BTC $xxx (+2.1%) | AVAX $yyy..."
- Risco/Oportunidade: 1 linha bem curta
- MAX 200 chars por seção"""

# Call Haiku (economia: tudo junto)
# Output: /tmp/briefing.txt
```

### send-to-telegram.sh
```bash
#!/bin/bash
briefing=$(cat /tmp/briefing.txt)
bot_token="<from .env>"
chat_id="<assistente bot chat>"

curl -X POST "https://api.telegram.org/bot${bot_token}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": \"${chat_id}\", \"text\": \"${briefing}\"}"
```

## 🕐 Cron Schedule

```bash
0 7 * * * /home/ubuntu/clawd/assistente/agents/bots/briefings/cron-runner.sh morning
0 16 * * * /home/ubuntu/clawd/assistente/agents/bots/briefings/cron-runner.sh evening
```

**Horários:**
- **07:00 BRT** (10:00 UTC) → Morning briefing (virais novas)
- **16:00 BRT** (19:00 UTC) → Evening briefing (notícias + mercado eod)

## 📊 Economia de Tokens

| Cenário | Tokens | Ganho |
|---------|--------|-------|
| 3 chamadas LLM separadas (pior) | ~3k | 0% |
| **1 chamada LLM (compilar tudo)** | ~500 | **-83%** |
| + Cache 6h (reusa 80% dias) | ~100 | **-97%** |
| **Total/mês** | ~6k (vs 90k) | **-93%** |

## ✅ Checklist Implementação

- [ ] Criar pasta `~/clawd/assistente/agents/bots/briefings/`
- [ ] `.env` com APIs/secrets
- [ ] 3 scripts fetch (bash)
- [ ] `compile.py` (1 Haiku call)
- [ ] `send-to-telegram.sh`
- [ ] `cron-runner.sh` (lock wrapper)
- [ ] Testar 1 ciclo completo
- [ ] Adicionar ao crontab
- [ ] Monitoring: `/tmp/briefing-*.log`

## 🎯 Resultado

**Entrada:** Nada (roda sozinho)
**Saída:** 1 mensagem formatada → Telegram (bot assistente) 2x/dia
**Custo:** ~100 tokens/briefing (Haiku), cache reduz 93%
**Latência:** ~30s (coleta paralela + compile)

---

Quer que eu implemente tudo ou tem dúvidas?
