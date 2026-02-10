# Secrets & IDs — Locations (no values)

## Global
- OpenClaw config: `/home/ubuntu/.openclaw/openclaw.json`
- OpenClaw allowlist: `/home/ubuntu/.openclaw/credentials/telegram-allowFrom.json`
- OpenClaw env: `/home/ubuntu/.openclaw/.env`

## Assistente Opus
- Bot env: `/home/ubuntu/clawd/sessions/assistente-opus/.env.assistente`
  - `TELEGRAM_BOT_TOKEN`
  - `ALLOWED_USER_ID`
- Bot code: `/home/ubuntu/clawd/sessions/assistente-opus/bot.py`
- Supervisor: `/home/ubuntu/clawd/sessions/assistente-opus/run.sh`

## Personajes
- Bot env: `/home/ubuntu/clawd/sessions/personajes/.env`
  - `TELEGRAM_BOT_TOKEN`
- Bot code: `/home/ubuntu/clawd/sessions/personajes/bot.py`

## M6 Atendimento
- Bot env: `/home/ubuntu/clawd/sessions/m60-atendimento/.env`
  - `TELEGRAM_BOT_TOKEN`
- Bot code: `/home/ubuntu/clawd/sessions/m60-atendimento/bot.py`

## Vagas Remotas
- Bot env: `/home/ubuntu/projects/job-curator-bot/.env`
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_GROUP_ID`
- Poster: `/home/ubuntu/projects/job-curator-bot/post_next.py`
- Cron: `crontab -l`

## Briefings (Assistente)
- Secrets: `/home/ubuntu/.config/secrets.env`
  - `BOT_ASSISTENTE_TOKEN`
  - `BOT_ASSISTENTE_CHAT`
  - `YOUTUBE_API_KEY`
  - `NEWSAPI_KEY`
- Scripts: `/home/ubuntu/clawd/assistente/agents/bots/briefings/`

## Observação
- Este arquivo guarda **apenas localizações**, nunca valores.
- Atualize aqui sempre que mover arquivos de secrets.
