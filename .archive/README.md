# Briefings (econômico)

## Coleta (zero-IA)
```
python3 /home/ubuntu/clawd/scripts/briefings/fetch_trends_virais.py
python3 /home/ubuntu/clawd/scripts/briefings/fetch_noticias.py
python3 /home/ubuntu/clawd/scripts/briefings/fetch_mercado.py
```

Saídas:
- /tmp/briefing-virais.json
- /tmp/briefing-noticias.json
- /tmp/briefing-mercado.json

## Prompts
- /home/ubuntu/clawd/memory/briefings/prompts.md

## Nota sobre YouTube
- Usa `YOUTUBE_API_KEY` (ou `GOOGLE_API_KEY`).
- Se não existir, o bloco `youtube_top` retorna erro e o briefing usa só Google Trends.

## Geração de prompts (LLM)
```
python3 /home/ubuntu/clawd/scripts/briefings/build_prompt_virais.py
python3 /home/ubuntu/clawd/scripts/briefings/build_prompt_noticias.py
python3 /home/ubuntu/clawd/scripts/briefings/build_prompt_mercado.py
```

Prompts gerados:
- /tmp/briefing-virais.prompt.txt
- /tmp/briefing-noticias.prompt.txt
- /tmp/briefing-mercado.prompt.txt

## Envio (Telegram Assistente)
```
python3 /home/ubuntu/clawd/scripts/briefings/send_telegram.py /tmp/briefing-virais.out.txt
```

O envio usa o bot configurado no Clawdbot e o primeiro chat_id allowFrom.
Você pode sobrescrever com:
- TELEGRAM_ASSISTENTE_BOT_TOKEN
- TELEGRAM_ASSISTENTE_CHAT_ID

## Rodar tudo (clawdbot + envio Assistente)
```
bash /home/ubuntu/clawd/scripts/briefings/run_briefings_clawdbot.sh
```
