# 🚀 SETUP GUIDE - Job Curator Bot v2.2

## PRÉ-REQUISITOS

- ✅ Python 3.9+
- ✅ Telegram bot token (já tem?)
- ✅ Telegram group ID (já tem?)
- ✅ Clawdbot instalado (local)

---

## INSTALAÇÃO RÁPIDA

### 1. Dependências
```bash
cd /home/ubuntu/clawd/scripts/job-curator
pip install -r requirements.txt
```

### 2. Variáveis de Ambiente
```bash
# .env ou export
export TELEGRAM_BOT_TOKEN="seu_token_aqui"
export TELEGRAM_CHAT_ID="-1003378765936"  # ID do grupo (começa com -)
```

### 3. Teste Rápido
```bash
# Dry-run (não posta, só mostra preview)
python3 main_free.py --dry-run

# Com skip cache (força pesquisa nova)
python3 main_free.py --dry-run --skip-cache
```

---

## MODO PRODUCTION

### Cron (Linux/Mac)
```bash
# Editar: crontab -e

# Pesquisa 1x/dia (00:00 UTC = 21:00 BRT)
0 0 * * * cd /home/ubuntu/clawd/scripts/job-curator && python3 main_free.py >> logs/cron.log 2>&1

# Posting 3x/dia
0 9 * * * cd /home/ubuntu/clawd/scripts/job-curator && python3 main_free.py --mode post >> logs/cron.log 2>&1
0 15 * * * cd /home/ubuntu/clawd/scripts/job-curator && python3 main_free.py --mode post >> logs/cron.log 2>&1
0 21 * * * cd /home/ubuntu/clawd/scripts/job-curator && python3 main_free.py --mode post >> logs/cron.log 2>&1
```

### Monitorar Logs
```bash
# Último run
tail -20 logs/2026-01-29.log

# Errors só
grep ERROR logs/2026-01-29.log

# Acompanhar em tempo real
tail -f logs/2026-01-29.log
```

---

## OPÇÕES DO MAIN.PY

```bash
python3 main_free.py [opções]

--mode {full,research,analyze,post}  # Padrão: full
--dry-run                            # Não posta (só preview)
--skip-cache                         # Força pesquisa nova
--limit N                            # Vagas por fonte (padrão: 15)

# Exemplos:
python3 main_free.py --mode research          # Só pesquisa
python3 main_free.py --mode post --dry-run    # Preview do que seria postado
python3 main_free.py --skip-cache --limit 20  # Pesquisa agressiva
```

---

## TROUBLESHOOTING

### "Nenhuma vaga coletada"
```bash
# Tenta com mais vagas por fonte
python3 main_free.py --skip-cache --limit 25
```

### "Nenhuma vaga passou no filtro"
- Vagas coletadas mas nenhuma em EU/AU/US/CA?
- Checar `logs/YYYY-MM-DD.log` para detalhes

### "Nenhuma vaga com link direto"
- Link resolver tem problema
- Checar se Greenhouse/Lever APIs acessíveis

### "Sem diversidade"
- Só 3 ou menos vagas com link?
- Usar `--skip-cache --limit 25` para forçar pesquisa maior

---

## ESTRUTURA DE ARQUIVOS

```
/home/ubuntu/clawd/scripts/job-curator/
├── main_free.py              ← MAIN script (use este)
├── job_sources_free.py       ← Coleta (RSS + APIs públicas)
├── job_filters.py            ← Filtros (país/setor)
├── link_resolver.py          ← Resolve links
├── job_analyzer.py           ← Análise Claude
├── diversity_validator.py    ← Validação
├── telegram_poster.py        ← Posting
├── cache_manager.py          ← Cache (48h)
├── test_data.py              ← Dados de teste
├── test_pipeline.py          ← Teste completo
├── logs/
│   ├── 2026-01-29.log
│   └── ...
├── state.json               ← Vagas já postadas
└── requirements.txt
```

---

## DEBUGGING

### Ver logs de cache
```bash
python3 -c "
from cache_manager import cache_get
cached, info = cache_get('daily_research_free')
print(f'Cached: {bool(cached)}')
print(f'Age: {info[\"age_hours\"]:.1f}h')
print(f'Expired: {info[\"expired\"]}')
if cached:
    print(f'Jobs: {len(cached)}')
"
```

### Limpar cache
```bash
rm -rf /tmp/job_curator_cache_*
```

### Testar coleta manualmente
```bash
python3 -c "
from job_sources_free import collect_from_free_sources
jobs = collect_from_free_sources(limit_per_source=5)
print(f'Total: {len(jobs)} vagas')
for job in jobs[:3]:
    print(f'  • {job[\"title\"]} @ {job[\"company\"]}')
"
```

---

## ENVIRONMENT VARIABLES

```bash
# Telegram
TELEGRAM_BOT_TOKEN=...          # Bot token (obrigatório para posting)
TELEGRAM_CHAT_ID=...            # Chat ID (obrigatório para posting)

# Optional
LOG_LEVEL=INFO                  # DEBUG/INFO/WARNING/ERROR (padrão: INFO)
CACHE_TTL_HOURS=48              # TTL do cache (padrão: 48)
REQUEST_TIMEOUT=30              # Timeout para requests (padrão: 30)
```

---

## MÉTRICAS ESPERADAS

| Métrica | Min | Típico | Máx |
|---------|-----|--------|-----|
| Vagas coletadas | 30 | 60 | 150 |
| Após filtro país | 15 | 40 | 80 |
| Com link direto | 10 | 25 | 50 |
| Aprovadas análise | 8 | 20 | 40 |
| Tempo pesquisa | 15s | 25s | 45s |
| Tokens LLM/dia | 1000 | 1500 | 2000 |
| Custo/dia | $0.001 | $0.01 | $0.02 |

---

## PRÓXIMOS PASSOS

1. ✅ Rodou o teste (`--dry-run`)? → Ir pro passo 2
2. ✅ Configurou Telegram? → Testar `python3 main_free.py --mode post`
3. ✅ Setup cron? → Monitorar logs por 1-2 dias
4. ✅ Tudo OK? → Expandir para grupos pagos

---

## SUPORTE

Ver logs: `tail -f logs/$(date +%Y-%m-%d).log`
Debug: `python3 main_free.py --skip-cache`

---

*Último update: 29 Jan 2026*
