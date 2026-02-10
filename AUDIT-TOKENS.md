# AUDIT-TOKENS.md - Mapeamento Completo (28-JAN-2026)

## 🔴 CRON JOBS (Rodando)

| Job | Frequência | Custo/Exec | Problema |
|-----|-----------|-----------|----------|
| Akira Automation (2h30m) | 8x/dia | ~$0.02 | Verbose summary |
| Heartbeat (2x/dia) | 2x/dia | ~$0.03 | Carrega contexto |
| Jesus Batch (00:00) | 1x/dia | ~$0.05 | 5-7 tweets IA |
| Jesus Post 08:05 | 1x/dia | ~$0.01 | Script bash |
| M60+Briefing (09:00) | 1x/dia | ~$0.08 | 2-part report |
| Briefing Mercado (18:00) | 1x/dia | ~$0.05 | Rate limit! |
| Cleanup (dom 02h) | 1x/semana | ~$0.01 | Script bash |
| Lembretes (auto) | 5x/mês | ~$0.01 | Script bash |
| **TOTAL** | **~15 exec/dia** | **~$0.25/dia** | **~$7.50/mês** |

## 🔵 SESSÃO MANUAL (Você + Akira)

| Item | Tokens | Problema |
|------|--------|----------|
| SOUL.md | ~600 | Carregado toda mensagem |
| USER.md | ~400 | Carregado toda mensagem |
| AGENTS.md | ~1300 | Carregado toda mensagem |
| MEMORY.md | ~1200 | Carregado toda mensagem |
| Session history | ~2000 | Creep exponencial |
| **PER MESSAGE** | **~4500** | **-75% se otimizar** |

## 🟡 CONTEXTO-ATIVO.md

| Item | Tokens | Status |
|------|--------|--------|
| Criado | ~50 | ✅ Mini version |
| Usando | Não ainda | ❌ Precisa integrar |

## 📊 Estimativa Mensal

**Se não otimizar:**
- Cron jobs: ~$7.50
- Chats manuais (80 msgs/mês): ~$32 (@$0.40/msg)
- **TOTAL: ~$40/mês** ❌ Caro

**Se otimizar (alvo):**
- Cron jobs: ~$4.00 (summaries curtos)
- Chats manuais (80 msgs/mês): ~$0.80 (@$0.01/msg) ✅
- **TOTAL: ~$4.80/mês** ✅ Viável

## 🎯 Drops Rápidos Pra Fazer

1. **Cron summaries** — 1 linha max
2. **Memory search** — não carregar MEMORY inteiro
3. **Cache session context** — carregar SOUL/USER UMA VEZ
4. **Remover AGENTS.md** — usar contexto-ativo só
5. **Batch chats** — 1 call = múltiplas perguntas
6. **Sessões isoladas** — 20 projetos = 20 sessões (zero context bleed)

## 🟢 Já Implementado

✅ Claude API (locked)
✅ contexto-ativo.md
✅ MESSAGE_PROTOCOL.md
✅ Gemini removido
✅ Fallbacks vazios

## 📝 TO-DO (Priority Order)

1. Cortar job summaries (URGENTE)
2. Integrar memory_search no runtime
3. Cache SOUL/USER por sessão
4. Criar 20 sessions framework
5. Batch Jesus + M60 em 1 call
