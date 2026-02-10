# HEARTBEAT.md - Otimizado p/ Tokens

## 🚨 AUTO-COMPACT APÓS RESPOSTAS

```bash
# Após cada resposta longa: /compact
# Mantém contexto < 50k
```

## 📊 MEMORY.md - SEPARADO EM CHUNKS

- `memory/YYYY-MM-DD.md` (daily, pequeno)
- `memory/jesus-sincero.md` (só lê se precisar)
- `memory/m60.md` (só lê se precisar)
- `memory/carteira.md` (só lê se precisar)
- NUNCA carregar MEMORY.md inteiro

## 🔄 SESSIONS ISOLADAS

- `sessions/personajes/` (Jesus posts, isolado)
- `sessions/assistente-opus/` (braço direito, isolado)
- `sessions/m60-atendimento/` (chatbot, isolado)
- Reduz contexto carregado por 70%

## ⚡ REGRA OURO

**Input > 80k tokens = COMPACT AGORA**
