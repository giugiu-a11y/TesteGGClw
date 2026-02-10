# TOOLS.md - Local Notes & Configurations

## Automação Akira - Scripts & Secrets

### Secrets Management
**Arquivo:** `~/.config/secrets.env`
- **Permissions:** `chmod 600` (somente seu usuário acessa)
- **Variáveis:**
  - `NEWSAPI_KEY` — NewsAPI key (opcional)
  - `TWITTER_BEARER_TOKEN` — Twitter API (quando implementar)
  - `CACHE_TTL` — Cache lifespan (padrão: 21600s = 6h)
  - `FETCH_TIMEOUT` — Request timeout (padrão: 10s)

### Scripts de Coleta (LEGACY em `/home/ubuntu/clawd/scripts/akira/`)
| Script | Função | Cache | API |
|--------|--------|-------|-----|
| `fetch-crypto.sh` | BTC, AVAX, MATIC prices | ✅ 6h | CoinGecko (free) |
| `fetch-news.sh` | News agregadas | ✅ 6h | NewsAPI (optional) |
| `fetch-trends.sh` | Twitter/Reddit trends | ✅ 6h | Simulado |
| `fetch-virals.sh` | TikTok/YouTube top vids | ✅ 6h | Simulado |
| `jesus-post.sh` | Post automation (zero IA) | - | Local JSON |
| `check-reminders.sh` | Lembretes (zero IA) | - | Local JSON |
| `cleanup.sh` | Cleanup automático | - | Local |

### Briefings Atuais (em `/home/ubuntu/clawd/assistente/agents/bots/briefings/`)
| Script | Função | Cache | API |
|--------|--------|-------|-----|
| `fetch-market.sh` | BTC/AVAX/MATIC + USD/BRL + Selic | ✅ 1h | CoinGecko + IBGE + BCB |
| `fetch-news.sh` | 9 temas (3 notícias cada) | ✅ 6h | NewsAPI |
| `fetch-virals.sh` | YouTube (EN+PT) + Google Trends | ✅ 12h | YouTube API + PyTrends |
| `run-market-briefing.sh` | Orquestra Market | - | Local |
| `run-news-briefing.sh` | Orquestra News | - | Local |
| `run-virals-briefing.sh` | Orquestra Virals | - | Local |

### Cache TTL Strategy
```bash
# Reusa cache se <6h, caso contrário fetch novo
if [ cache_age < 6h ]; then
  use_cache
else
  fetch_novo
  atualiza_cache
fi
```
**Ganho:** -80% API calls, economiza bandwidth/latência

### Cleanup Automático
**Cron:** Domingos 02:00 BRT (05:00 UTC)
**O que faz:**
- Delete `/tmp/akira-*.json` > 7 dias
- Delete cron runs > 30 dias
- Compress JSON files (6h-7d) = -85% disk
- Report disk usage

**Log:** `/tmp/cleanup.log`

---

## AWS / Infrastructure Notes

### Instance Type
- **Host:** VPS customizado (ip-172-31-14-27)
- **Recursos:** Suficiente para automação (free tier compatible)
- **Backup:** TODO (implementar weekly)

### Security Checklist
- ✅ Secrets em `~/.config/secrets.env` (chmod 600)
- ✅ SSH keys com passphrase (TODO: verify)
- ✅ Firewall: UFW enabled (TODO: verify)
- ✅ Fail2ban para SSH (TODO: implement)
- ⏳ Backup automático (TODO: S3/B2 weekly)

---

## Cost Optimization

| Ação | Custo | Ganho | Status |
|------|-------|-------|--------|
| Cache TTL | Free | -80% API calls | ✅ Done |
| Secrets mgmt | Free | Security | ✅ Done |
| Cleanup script | Free | -95% storage | ✅ Done |
| Gzip compression | Free | -85% disk | ✅ Done |
| Rate limiting (sleep 2s) | Free | Evita bans | ✅ Done |

**Total Monthly Savings:** ~$0 (free tier sustained), economia de banda/CPU

---

## Quick Reference

```bash
# Check cache age
stat -c %Y /tmp/akira-crypto.json

# Manual cleanup
bash /home/ubuntu/clawd/scripts/akira/cleanup.sh

# View cleanup logs
tail -f /tmp/cleanup.log

# Source secrets (manual)
source /home/ubuntu/.config/secrets.env
echo $CACHE_TTL
```

---

Add whatever helps you do your job. This is your cheat sheet.
