# Codex Bridge - Chat com OpenAI Codex via Telegram

## Como Usar

No Telegram, basta dizer:
```
codex: [sua mensagem]
```

Exemplos:
- `codex: refatora o módulo de autenticação`
- `codex: revisa esse código e sugere melhorias`
- `codex: cria um endpoint REST para users`

## Como Funciona

```
Telegram → OpenClaw (Gemini Flash Lite) → codex-bridge.sh → Codex CLI
                                                    ↓
Telegram ← OpenClaw (repassa resposta) ← output do terminal
```

1. Você manda "codex: xxx"
2. OpenClaw (Gemini) executa o bridge script
3. Bridge envia para sessão tmux do Codex
4. Captura toda a resposta do terminal
5. Retorna para você no Telegram

## Comandos Manuais

```bash
# Ver status da sessão
/home/ubuntu/clawd/bridges/codex-bridge.sh --status

# Ver output recente
/home/ubuntu/clawd/bridges/codex-bridge.sh --output 50

# Encerrar sessão
/home/ubuntu/clawd/bridges/codex-bridge.sh --kill

# Enviar prompt direto
/home/ubuntu/clawd/bridges/codex-bridge.sh "seu prompt aqui"
```

## Configuração

Variável de ambiente para mudar diretório de trabalho:
```bash
CODEX_WORKDIR=/home/ubuntu/projects/meu-projeto ./codex-bridge.sh "faz X"
```

## Monitorar Sessão Manualmente

```bash
# Attach na sessão (Ctrl+B D para sair)
tmux -S /tmp/codex-bridge.sock attach -t codex-bridge
```

## Notas

- Sessão persiste entre mensagens (contexto mantido)
- Timeout de 120s por mensagem
- Codex roda com seus tokens OpenAI (ilimitados)
- Bridge gerenciado por Gemini Flash Lite (economia)
