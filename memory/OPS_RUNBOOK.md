# OPS RUNBOOK — Bots & Briefings

## Objetivo
Operar todos os bots sem cruzar projetos, com segurança e baixo custo.

---

## 1) Start/Stop rápido (manual)

### Assistente Opus
```
/home/ubuntu/clawd/sessions/venv/bin/python /home/ubuntu/clawd/sessions/assistente-opus/bot.py
```

### Personajes
```
/home/ubuntu/clawd/sessions/venv/bin/python /home/ubuntu/clawd/sessions/personajes/bot.py
```

### M6 Atendimento
```
/home/ubuntu/clawd/sessions/venv/bin/python /home/ubuntu/clawd/sessions/m60-atendimento/bot.py
```

---

## 2) Supervisores (auto-restart)

### Assistente Opus
```
nohup /home/ubuntu/clawd/sessions/assistente-opus/run.sh > /tmp/assistente-opus.supervisor.log 2>&1 &
```

### Personajes
```
nohup /home/ubuntu/clawd/sessions/personajes/run.sh > /tmp/personajes.supervisor.log 2>&1 &
```

### M6 Atendimento
```
nohup /home/ubuntu/clawd/sessions/m60-atendimento/run.sh > /tmp/m60-atendimento.supervisor.log 2>&1 &
```

---

## 3) Briefings (cron)

Rodar manual:
```
bash /home/ubuntu/clawd/assistente/agents/bots/briefings/run-news-briefing.sh
bash /home/ubuntu/clawd/assistente/agents/bots/briefings/run-market-briefing.sh
bash /home/ubuntu/clawd/assistente/agents/bots/briefings/run-virals-briefing.sh
```

Cron atual (user):
```
0 10 * * * /home/ubuntu/clawd/assistente/agents/bots/briefings/cron-runner-news.sh >> /tmp/briefings_news_cron.log 2>&1
0 12 * * * /home/ubuntu/clawd/assistente/agents/bots/briefings/cron-runner.sh >> /tmp/briefings_market_cron.log 2>&1
0 15 * * * /home/ubuntu/clawd/assistente/agents/bots/briefings/cron-runner-virals.sh >> /tmp/briefings_virals_cron.log 2>&1
```

Logs:
```
tail -n 50 /tmp/briefings_news_cron.log
tail -n 50 /tmp/briefings_market_cron.log
tail -n 50 /tmp/briefings_virals_cron.log
```

---

## 4) Vagas Remotas

Post manual:
```
/home/ubuntu/projects/job-curator-bot/post_next.py
```

Alert test:
```
/home/ubuntu/projects/job-curator-bot/post_next.py --alert-test
```

Logs:
```
/home/ubuntu/projects/job-curator-bot/logs/post_next.log
```

---

## 5) Jesus Sincero (posting)

Cron (BRT = UTC-3):
```
0 12 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 09:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 15 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 12:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 18 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 15:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 21 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 18:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 0 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 21:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
```

Healthcheck diário (DNS + reachability):
```
/home/ubuntu/clawd/sessions/personajes/scripts/healthcheck.sh
```

DNS fix (runtime):
```
sudo resolvectl dns enp39s0 1.1.1.1 8.8.8.8
sudo resolvectl domain enp39s0 ~.
sudo resolvectl flush-caches
```

Logs:
```
/home/ubuntu/clawd/sessions/personajes/logs/posting.log
/home/ubuntu/clawd/sessions/personajes/logs/error.log
/home/ubuntu/clawd/sessions/personajes/logs/healthcheck.log
```

---

## 6) Segurança e roteamento

Arquivos de referência:
- `memory/SECRETS_LOCATIONS.md`
- `memory/BOTS_REGISTRY.md`
- `memory/ROUTING_MAP.md`

---

## 7) Checklist rápido (antes de mexer)
- [ ] Verificar que está no diretório correto do bot
- [ ] Confirmar token/chat_id do bot no `.env`
- [ ] Não usar token de outro projeto
- [ ] Confirmar logs do bot correto
