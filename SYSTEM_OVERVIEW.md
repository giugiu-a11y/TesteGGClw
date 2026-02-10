# System Overview — Clawd (2026‑02‑05)

Objetivo: visão única, profissional e replicável do sistema (bots + briefings + crons), com paths canônicos e comandos de teste rápidos.

---

## 1) Componentes principais

### A) OpenClaw (core)
- **Gateway**: `openclaw-gateway` (systemd user)
- **Config**: `/home/ubuntu/.openclaw/openclaw.json`
- **Credenciais Telegram**: `/home/ubuntu/.openclaw/credentials/`

### B) Jesus Sincero (Twitter)
- **Pasta canônica**: `/home/ubuntu/clawd/sessions/personajes/`
- **Postagem**: `scripts/post-daily.sh` (5x/dia)
- **Geração semanal**: `scripts/batch-generator.sh` (35 posts)
- **Logs**: `logs/posting.log`, `logs/error.log`, `logs/healthcheck.log`

### C) Briefings Assistente (Telegram)
- **Pasta canônica**: `/home/ubuntu/clawd/assistente/agents/bots/briefings/`
- **Briefings**: News (3 msg), Market (1 msg), Virals (2 msg)
- **Logs**: `/tmp/briefings_news_cron.log`, `/tmp/briefings_market_cron.log`, `/tmp/briefings_virals_cron.log`

### D) Vagas Remotas (Job‑Curator)
- **Projeto**: `/home/ubuntu/projects/job-curator-bot/`
- **Postagem**: `post_next.py` (3x/dia)
- **Coleta semanal**: `weekly_collect.sh`
- **Logs**: `logs/post_next.log`

---

## 2) Crons (produção)

```bash
# Vagas remotas
30 2 * * 0 /home/ubuntu/projects/job-curator-bot/weekly_collect.sh >> /home/ubuntu/projects/job-curator-bot/logs/weekly_collect.log 2>&1
0 9 * * * /home/ubuntu/projects/job-curator-bot/post_next.py >> /home/ubuntu/projects/job-curator-bot/logs/post_next.log 2>&1
0 15 * * * /home/ubuntu/projects/job-curator-bot/post_next.py >> /home/ubuntu/projects/job-curator-bot/logs/post_next.log 2>&1
0 21 * * * /home/ubuntu/projects/job-curator-bot/post_next.py >> /home/ubuntu/projects/job-curator-bot/logs/post_next.log 2>&1
10 0 * * * /home/ubuntu/projects/job-curator-bot/rotate_logs.sh >> /home/ubuntu/projects/job-curator-bot/logs/logrotate.log 2>&1

# OpenClaw health
0 * * * * /home/ubuntu/clawd/scripts/alerts/check_openclaw_health.sh >> /tmp/openclaw_health.log 2>&1

# Briefings
0 10 * * * /home/ubuntu/clawd/assistente/agents/bots/briefings/cron-runner-news.sh >> /tmp/briefings_news_cron.log 2>&1
0 12 * * * /home/ubuntu/clawd/assistente/agents/bots/briefings/cron-runner.sh >> /tmp/briefings_market_cron.log 2>&1
0 15 * * * /home/ubuntu/clawd/assistente/agents/bots/briefings/cron-runner-virals.sh >> /tmp/briefings_virals_cron.log 2>&1

# Jesus Sincero (Twitter)
0 12 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 09:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 15 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 12:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 18 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 15:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 21 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 18:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 0 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 21:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1

# Jesus Sincero healthcheck (DNS + reachability)
5 6 * * * /home/ubuntu/clawd/sessions/personajes/scripts/healthcheck.sh >> /home/ubuntu/clawd/sessions/personajes/logs/healthcheck.log 2>&1

# Jesus Sincero batch (2ª 23:00 BRT)
0 2 * * 2 cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/batch-generator.sh" >> /home/ubuntu/clawd/sessions/personajes/logs/batch-generation.log 2>&1
```

---

## 3) Secrets (sem valores)

- **OpenClaw**: `/home/ubuntu/.openclaw/openclaw.json`
- **Telegram (Assistente)**: `/home/ubuntu/clawd/sessions/assistente-opus/.env.assistente`
- **Briefings**: `~/.config/secrets.env`
- **Jesus Sincero**: `/home/ubuntu/clawd/sessions/personajes/.env`
- **Job Curator**: `/home/ubuntu/projects/job-curator-bot/.env`

---

## 4) Comandos de teste rápidos

### OpenClaw
```bash
openclaw status --plain
```

### Briefings
```bash
bash /home/ubuntu/clawd/assistente/agents/bots/briefings/run-news-briefing.sh
bash /home/ubuntu/clawd/assistente/agents/bots/briefings/run-market-briefing.sh
bash /home/ubuntu/clawd/assistente/agents/bots/briefings/run-virals-briefing.sh
```

### Jesus Sincero
```bash
cd /home/ubuntu/clawd/sessions/personajes
bash scripts/test-single-post.sh "Teste manual"
```

### Vagas Remotas
```bash
/home/ubuntu/projects/job-curator-bot/post_next.py
```

---

## 5) Observações operacionais

- **DNS**: posts do Twitter dependem de resolver estável.
  - Fix runtime (não persistente):
    ```bash
    sudo resolvectl dns enp39s0 1.1.1.1 8.8.8.8
    sudo resolvectl domain enp39s0 ~.
    sudo resolvectl flush-caches
    ```

- **Virals**: dependem de quota YouTube e rate-limit Trends.

---

## 6) Don’t cross the streams

- Nunca reutilizar tokens entre projetos.
- Sempre validar o chat_id/token do bot alvo.
- Use logs corretos por projeto para debugar.
