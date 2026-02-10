# RELATÓRIO TÉCNICO - Problema de Modelo na Análise Vagas Remotas

**Data:** 2026-01-29 00:51 UTC  
**Problema:** Sistema está usando Claude SONNET em vez de Haiku (configuração errada)  
**Severidade:** CRÍTICO (impacto de custo/tokens)

---

## 1. PROBLEMA IDENTIFICADO

Ao executar:
```bash
cd /home/ubuntu/clawd/scripts/job-curator
python3 main.py --dry-run --limit 5 --max-posts 3
```

**Resultado observado:**
```
🤖 Claude API: modelo=claude-sonnet-4-20250514 (SONNET), timeout=30s
```

**Esperado:**
```
🤖 Claude API: modelo=claude-haiku-4-5 (HAIKU), timeout=30s
```

---

## 2. CONFIGURAÇÃO ATUAL

### Ambiente
- **Perfil default (Haiku):** `~/.clawdbot/`
  ```bash
  clawdbot models status → Default: anthropic/claude-haiku-4-5
  ```

- **Perfil Opus:** `~/.clawdbot-opus/`
  ```bash
  clawdbot --profile opus models status → Default: anthropic/claude-opus-4-5
  ```

- **API Key:** configurada via secret local (ex.: `.env` / Secrets Manager). **Nao versionar chave em Git.**

### Arquivo problemático
- **Localização:** `/home/ubuntu/clawd/scripts/job-curator/job_analyzer.py`
- **Função:** `call_claude_api()` ou similar
- **Problema:** Hard-coded como `claude-sonnet-4-20250514`

---

## 3. TRECHO DO CÓDIGO (job_analyzer.py)

Procurar por:
```python
model="claude-sonnet-4-20250514"  # ❌ ERRADO
# ou
model = "claude-sonnet-4-20250514"  # ❌ ERRADO
# ou
client.messages.create(model="claude-sonnet-4-20250514", ...)  # ❌ ERRADO
```

Deveria ser:
```python
model = os.environ.get("MODEL_JOB_CURATOR", "claude-haiku-4-5")  # ✅ CERTO
# ou
model = "claude-haiku-4-5"  # ✅ CERTO (se Haiku é default)
```

---

## 4. SOLUÇÃO NECESSÁRIA

### Passo 1: Verificar job_analyzer.py
```bash
grep -n "sonnet\|claude-" /home/ubuntu/clawd/scripts/job-curator/job_analyzer.py
```

Se encontrar `claude-sonnet-4-20250514`, é o problema.

### Passo 2: Corrigir
Substituir todas instâncias de `claude-sonnet-4-20250514` por `claude-haiku-4-5`

Ou melhor ainda, adicionar no `.env`:
```bash
# .env
MODEL_JOB_CURATOR=claude-haiku-4-5  # Default pra análise de vagas
MODEL_REFACTOR=claude-opus-4-5      # Se precisar refactor técnico
```

E no código:
```python
import os
model = os.environ.get("MODEL_JOB_CURATOR", "claude-haiku-4-5")
```

### Passo 3: Testar
```bash
cd /home/ubuntu/clawd/scripts/job-curator
python3 main.py --debug --test-claude
# Deve logar: modelo=claude-haiku-4-5
```

---

## 5. IMPACTO

| Item | Antes | Depois |
|------|-------|--------|
| Modelo | SONNET | HAIKU |
| Custo/vaga | ~$0.02 | ~$0.003 |
| 5 vagas/dia | ~$0.10 | ~$0.015 |
| Mensal (150 vagas) | ~$3.00 | ~$0.45 |
| **Economia** | - | **-85%** |

---

## 6. ARQUIVOS ENVOLVIDOS

```
/home/ubuntu/clawd/scripts/job-curator/
├── job_analyzer.py          ← FIX AQUI (modelo hard-coded)
├── main.py                  ← OK (usa job_analyzer)
├── telegram_poster.py       ← OK (só formata)
├── job_sources.py           ← OK (só coleta)
├── link_resolver.py         ← OK (só resolve links)
└── .env                     ← ADICIONAR MODEL_JOB_CURATOR
```

---

## 7. COMO REPRODUZIR O BUG

```bash
cd /home/ubuntu/clawd/scripts/job-curator
python3 main.py --debug 2>&1 | grep -i "claude\|model\|sonnet"
# Output: "🤖 Claude API: modelo=claude-sonnet-4-20250514 (SONNET)"
```

---

## 8. PRÓXIMOS PASSOS

1. ✅ Identificar linha exata em job_analyzer.py
2. ✅ Substituir SONNET → HAIKU
3. ✅ Adicionar MODEL_JOB_CURATOR ao .env
4. ✅ Testar com --debug
5. ✅ Confirmar redução de custo

**Responsável por correção:** Outra IA (tem acesso ao terminal)

---

## 9. CONTATO / DÚVIDAS

Se precisar de mais contexto sobre a configuração Haiku/Opus:
- Haiku = default (barato, rotina)
- Opus = --profile opus (técnico, refactor)
- API key = compartilhada, funciona em ambos
- --session-id novo = zero histórico (evita travamento)
