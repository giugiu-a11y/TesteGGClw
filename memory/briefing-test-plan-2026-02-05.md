# 📋 PLANO DE TESTE - Sistema de Briefings Automáticos
**Data:** 2026-02-05
**Objetivo:** Rodar todos os 3 briefings e validar funcionamento completo

---

## ✅ O QUE FOI CONSTRUÍDO

### 1️⃣ **MARKET BRIEFING** (100% Funcional)
- **Horário Cron:** 09:00 BRT (12:00 UTC) — `0 12 * * *`
- **Fontes:** CoinGecko (cripto), IBGE (câmbio), BCB (economia)
- **Output:** 1 mensagem Telegram com BTC, AVAX, MATIC, USD/BRL, SELIC + análise de risco/oportunidade
- **Cache:** 1h
- **Teste Manual:** `bash /home/ubuntu/clawd/assistente/agents/bots/briefings/fetch/fetch-market.sh`

### 2️⃣ **NEWS BRIEFING** (100% Funcional)
- **Horário Cron:** 07:00 BRT (10:00 UTC) — `0 10 * * *`
- **Fonte:** NewsAPI (9 categorias: bolsas, study abroad, edtech M&A, imigração, etc)
- **Output:** 3 mensagens Telegram (Part 1, 2, 3) com 27 notícias totais
- **Cache:** 6h
- **Teste Manual:** `bash /home/ubuntu/clawd/assistente/agents/bots/briefings/fetch/fetch-news.sh`

### 3️⃣ **VIRALS BRIEFING** (Parcialmente Funcional)
- **Horário Cron:** 16:00 BRT (19:00 UTC) — `0 19 * * *`
- **Fontes:** 
  - ✅ YouTube API (EN + PT, BR + INT'L, 7 temas)
  - ⚠️ Google Trends via PyTrends (BR vs Mundo, com Tendência/Pico)
  - ❌ TikTok (removido — sem API)
- **Output:** 2 mensagens Telegram (YouTube + Google Trends)
- **Cache:** 12h
- **Teste Manual:** `bash /home/ubuntu/clawd/assistente/agents/bots/briefings/fetch/fetch-virals.sh`

---

## 🧪 PLANO DE TESTE PARA AMANHÃ (05 FEV)

### PASSO 1: Verificar Cron Jobs (antes de 07:00 BRT)
```bash
# Conferir se cron jobs estão agendados corretamente
crontab -l | grep briefing

# Esperado:
# 0 10 * * * /home/ubuntu/clawd/assistente/agents/bots/briefings/cron-runner-news.sh >> /tmp/briefings_news_cron.log 2>&1
# 0 12 * * * /home/ubuntu/clawd/assistente/agents/bots/briefings/cron-runner.sh >> /tmp/briefings_market_cron.log 2>&1
# 0 15 * * * /home/ubuntu/clawd/assistente/agents/bots/briefings/cron-runner-virals.sh >> /tmp/briefings_virals_cron.log 2>&1
```

### PASSO 2: Acompanhar News Briefing (07:00 BRT / 10:00 UTC)
```bash
# Monitorar log em tempo real:
tail -f /tmp/briefings_news_cron.log

# Espera-se:
# [1/3] Fetching news data...
# [2/3] Compiling briefing (3 parts)...
# [3/3] Sending to Telegram...
# ✅ Briefing enviado às 2026-02-05 10:00:XX

# Conferir se mensagem chegou no Telegram:
# @AssistenteClawd_OPUS deve ter recebido 3 mensagens
```

### PASSO 3: Acompanhar Market Briefing (09:00 BRT / 12:00 UTC)
```bash
# Monitorar log:
tail -f /tmp/briefings_market_cron.log

# Espera-se:
# [1/3] Fetching market data...
# [2/3] Compiling briefing...
# [3/3] Sending to Telegram...
# ✅ Briefing enviado às 2026-02-05 12:00:XX

# Conferir Telegram: BTC, AVAX, MATIC, USD/BRL, SELIC
```

### PASSO 4: Acompanhar Virals Briefing (16:00 BRT / 19:00 UTC)
```bash
# Monitorar log:
tail -f /tmp/briefings_virals_cron.log

# Espera-se:
# [1/3] Fetching virals data (YouTube + Google Trends)...
# [2/3] Compiling briefing (2 parts)...
# [3/3] Sending to Telegram...
# ✅ Briefing enviado às 2026-02-05 19:00:XX

# Conferir Telegram: 
# - Part 1: YouTube (vídeos EN + PT)
# - Part 2: Google Trends (Brasil vs Mundo, com Tendência/Pico)
```

---

## ⚠️ POSSÍVEIS PROBLEMAS & SOLUÇÕES

### PROBLEMA 1: YouTube retorna vazio
**Sintoma:** Virals briefing sem vídeos
**Causa:** YouTube API quota excedida OU chave não carregada
**Solução:**
```bash
# Verificar se chave está em secrets.env:
cat ~/.config/secrets.env | grep YOUTUBE_API_KEY

# Exportar manualmente:
export YOUTUBE_API_KEY="AIzaSyBLgL4oaAFlRKzhZu6GeQuAjhj-xQCvfxw"

# Testar fetch:
bash /home/ubuntu/clawd/assistente/agents/bots/briefings/fetch/fetch-virals.sh
```

### PROBLEMA 2: Google Trends (PyTrends) retorna erro 429
**Sintoma:** "API Error - 429" no briefing
**Causa:** Rate limit do Google (muitas requisições)
**Solução:**
1. Aumentar `time.sleep()` entre queries em `fetch-virals.sh` (de 0.5s para 2-3s)
2. Usar timeframe mais curto (`'today 1-d'` em vez de `'today 12-m'`)
3. Fazer queries 1x por dia (já está no cache de 12h)

### PROBLEMA 3: Cron não executa
**Sintoma:** Nenhuma mensagem no Telegram, logs vazios
**Causa:** Cron desligado OU path incorreto
**Solução:**
```bash
# Verificar se cron está rodando:
sudo systemctl status cron

# Checar permissões dos scripts:
ls -lah /home/ubuntu/clawd/assistente/agents/bots/briefings/*.sh

# Rodar manualmente para testar:
bash /home/ubuntu/clawd/assistente/agents/bots/briefings/cron-runner.sh
```

### PROBLEMA 4: Telegram não recebe mensagens
**Sintoma:** Scripts executam OK, mas Telegram fica vazio
**Causa:** Bot token expirado OU chat ID inválido
**Solução:**
```bash
# Testar envio manual:
curl -X POST "https://api.telegram.org/bot${BOT_ASSISTENTE_TOKEN}/sendMessage" \
  -d "chat_id=881840168" \
  -d "text=Test: $(date)"

# Se receber {"ok":true}: Token está OK
# Se receber {"ok":false}: Token expirou
```

---

## 📊 CHECKLIST FINAL

- [ ] Cron jobs agendados corretamente
- [ ] ~/.config/secrets.env com credenciais presentes
- [ ] 07:00 BRT: News briefing enviado com 3 mensagens
- [ ] 09:00 BRT: Market briefing enviado com dados reais
- [ ] 16:00 BRT: Virals briefing enviado com YouTube + Trends
- [ ] Todos os dados no Telegram estão legíveis e relevantes
- [ ] Logs em `/tmp/briefings_*_cron.log` mostram sucesso

---

## 🔗 ARQUIVOS CRÍTICOS

```
/home/ubuntu/clawd/assistente/agents/bots/briefings/
├── fetch-market.sh          (CoinGecko, IBGE, BCB)
├── fetch-news.sh            (NewsAPI)
├── fetch-virals.sh          (YouTube + PyTrends)
├── compile-*.sh             (formatação)
├── send-*.sh                (envio Telegram)
├── run-*-briefing.sh        (orquestrador)
├── cron-runner*.sh          (lock + execução)
└── venv/                    (PyTrends virtualenv)

/home/ubuntu/.config/secrets.env
├── NEWSAPI_KEY
├── YOUTUBE_API_KEY
├── BOT_ASSISTENTE_TOKEN
└── BOT_ASSISTENTE_CHAT

/tmp/
├── briefings_news_cron.log
├── briefings_market_cron.log
├── briefings_virals_cron.log
└── briefing-*.txt (outputs)
```

---

## 🎯 HORÁRIOS ESPERADOS (UTC+0)

| Briefing | BRT | UTC | Cron |
|----------|-----|-----|------|
| News | 07:00 | 10:00 | `0 10 * * *` |
| Market | 09:00 | 12:00 | `0 12 * * *` |
| Virals | 16:00 | 19:00 | `0 19 * * *` |

---

## 📝 NOTAS IMPORTANTES

1. **Creditos:** Amanhã podem aparecer 429s (rate limit) se quotas do YouTube/Google forem excedidas. Cache de 12h vai contornar isso.

2. **PyTrends:** Instalado corretamente em venv isolado. Pode precisar de backoff maior se Google bloquear.

3. **Telegram:** Bot ID `8206625095` enviando para chat `881840168` (seu Telegram pessoal).

4. **Monitoramento:** Guardar screenshots dos 3 briefings para documentação.

---

**Status:** 🟢 PRONTO PARA TESTE EM PRODUÇÃO

Preparado por: Akira Master
Data: 2026-02-04 23:56 UTC
