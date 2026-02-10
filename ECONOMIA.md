# ECONOMIA.md - Regras de Economia de Tokens

## 🚨 REGRAS OBRIGATÓRIAS

### Antes de qualquer mudança técnica:
1. **Planejar ANTES de executar** - listar comandos necessários
2. **Máximo 3-5 comandos** por tarefa
3. **Nunca carregar schemas/configs completos** - só o necessário
4. **Não fazer verificações intermediárias** - confiar no resultado

### Comandos proibidos em tarefas de manutenção:
- `gateway config.schema` (muito grande)
- Múltiplos `cat` de arquivos grandes
- Loops de tentativa/erro

### Padrão eficiente:
```
1. Identificar arquivo → 1 comando
2. Editar → 1 comando  
3. Restart se necessário → 1 comando
4. Confirmar → 1 comando
```

## 📊 Modelos por Contexto

| Contexto | Modelo | Profile |
|----------|--------|---------|
| Chat Telegram (humano) | Opus | anthropic:giugiu (Pro) |
| Cron jobs | Haiku | anthropic:payg (API) |
| Subagents | Haiku | anthropic:payg (API) |

## 🔄 Failover Automático

Ordem configurada: `Pro → PAYG`

Se Claude Pro travar (rate limit):
- Automaticamente usa API convencional
- Não precisa intervenção manual

## 💡 Lembrete

Tokens = dinheiro. Cada comando, cada verificação, cada output longo custa.
Ser cirúrgico > ser verboso.
