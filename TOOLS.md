# TOOLS.md - Referência Rápida

## Codex Bridge (OpenAI)
Quando Mestre disser `codex: [prompt]`:
```bash
/home/ubuntu/clawd/bridges/codex-bridge.sh "[prompt]"
```
- Sessão tmux persistente
- Reproduz output completo do terminal
- Ver: `/home/ubuntu/clawd/bridges/CODEX_BRIDGE.md`

## Paths Críticos
- **Secrets:** `~/.config/secrets.env`
- **Briefings:** `/home/ubuntu/clawd/assistente/agents/bots/briefings/`
- **Job Curator:** `/home/ubuntu/projects/job-curator-bot/`
- **Jesus Sincero:** `/home/ubuntu/clawd/assistente/agents/personajes/jesus-sincero/`

## Secrets (.env)
```
BOT_ASSISTENTE_TOKEN, BOT_ASSISTENTE_CHAT
NEWSAPI_KEY, YOUTUBE_API_KEY, GEMINI_API_KEY
TELEGRAM_BOT_TOKEN, TELEGRAM_GROUP_ID
```

## Comandos Úteis
```bash
# Testar briefings
bash .../briefings/cron-runner-news.sh
bash .../briefings/cron-runner.sh
bash .../briefings/cron-runner-virals.sh

# Logs
tail -f /tmp/*briefing*.log
```

## Cache TTL
| Briefing | TTL |
|----------|-----|
| Market | 1h |
| News | 6h |
| Virals | 12h |
