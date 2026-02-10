# 📰 Sistema de Briefings Automáticos

**Localização:** `/home/ubuntu/clawd/assistente/agents/bots/briefings/`
**Atualizado:** 2026-02-06

---

## 📋 Visão Geral

| Briefing | Horário BRT | UTC | Fonte |
|----------|-------------|-----|-------|
| 📰 News | 07:00 | 10:00 | NewsAPI + Gemini |
| 📊 Market | 09:00 | 12:00 | CoinGecko + BCB + Finnhub |
| 🔥 Virals | 12:00 | 15:00 | HackerNews + YouTube + Reddit (RSS) |

---

## 🔥 Virals Briefing (7 Tópicos)

**Objetivo**
- Para cada tema: **3–5 itens por fonte** (BR + Mundo quando aplicável)
- Fontes exibidas **separadas** no relatório e em mensagens no Telegram
- YouTube só entra se atingir **views mínimos**

**Fontes atuais:**
- **Hacker News** (API pública, sem rate limit)
- **YouTube** (BR + Mundo por região/idioma, quota 10k units/dia)
- **Reddit** (RSS público, sem login; BR e Mundo por listas de subs)
- **Twitter** (API oficial via OAuth1/Bearer; BR e Mundo por idioma)
- **Google News** (RSS por tema, BR + Mundo)

**Tópicos:**
1. Carreira
2. Internacionalização
3. Estudar fora
4. Educação
5. Trabalho remoto
6. Inglês
7. Skills

**Notas:**
- ✅ Reddit via RSS funciona (Atom feed)
- ❌ Google Trends bloqueado (PyTrends rate limited)
- ✅ HN funciona como fonte técnica extra (listada por último)

**Parâmetros úteis (virals):**
```bash
# Reddit RSS
REDDIT_MODE=rss
REDDIT_LIMIT=5
REDDIT_USER_AGENT=briefings-bot/1.0

# Twitter (API oficial)
TWITTER_MODE=api
TWITTER_LIMIT=5
TWITTER_USER_AGENT=briefings-bot/1.0
TWITTER_BEARER_TOKEN=***REDACTED***
TWITTER_MIN_SCORE=100
TWITTER_LANGS=pt,en
TWITTER_ENV_FILE=/home/ubuntu/clawd/sessions/personajes/.env

# Google News (RSS)
NEWS_MODE=rss
NEWS_LIMIT=5
NEWS_USER_AGENT=briefings-bot/1.0

# YouTube
YT_MIN_VIEWS=50000
YT_LIMIT=5
YT_REGION_BR=BR
YT_LANG_BR=pt
YT_REGION_WORLD=US
YT_LANG_WORLD=en
MAX_RESULTS=5
```

---

## 🧾 Estado Atual (2026-02-06)

**Conquistas**
- Google News BR + Mundo por tema.
- Twitter API (OAuth1/Bearer) com filtro de viralidade e idioma.
- Reddit RSS (Atom) sem API/login.
- YouTube com filtro por views mínimos.
- Saída do virals separada por fonte e por região.

**Arquivos alterados**
- `assistente/agents/bots/briefings/fetch/twitter_api.py`
- `assistente/agents/bots/briefings/fetch/fetch-virals.sh`
- `assistente/agents/bots/briefings/compile/compile-virals.sh`
- `assistente/agents/bots/briefings/compile/compile-market.sh`
- `assistente/agents/bots/briefings/compile/compile-news.sh`

---

## 🔐 Secrets

**Arquivo:** `~/.config/secrets.env` (chmod 600)

```bash
BOT_ASSISTENTE_TOKEN=xxx    # Telegram bot
BOT_ASSISTENTE_CHAT=xxx     # Chat ID
NEWSAPI_KEY=xxx             # NewsAPI
YOUTUBE_API_KEY=xxx         # YouTube Data API
GEMINI_API_KEY=xxx          # Google Gemini
```

---

## 🧪 Testes

```bash
# News
bash /home/ubuntu/clawd/assistente/agents/bots/briefings/cron-runner-news.sh

# Market  
bash /home/ubuntu/clawd/assistente/agents/bots/briefings/cron-runner.sh

# Virals
bash /home/ubuntu/clawd/assistente/agents/bots/briefings/cron-runner-virals.sh
```

---

## 📝 Logs

```bash
tail -f /tmp/briefings_*_cron.log
```

---

## 💰 Custos

| Item | Custo |
|------|-------|
| NewsAPI | Free (500/dia) |
| YouTube | Free (10k units/dia) |
| HN | Free (sem limite) |
| Gemini | ~$0.003/dia |
