# MESSAGE_PROTOCOL.md - Token Efficiency Rules

## 🎯 REGRA DE OURO
**Economia > Completude. Sempre.**

## 💡 Princípios

### 1. Nunca carregar MEMORY.md inteiro
- Use `memory_search` pra buscar só o necessário
- Se nada aparecer relevante = tá OK, segue sem

### 2. Respostas ultra-curtas
- Max: 2-3 linhas por resposta padrão
- Se precisa mais = é outra conversa
- 1 frase > 5 parágrafos

### 3. Batch requests
- "Preciso de X, Y, Z" (1 call) > 3 calls separadas
- Combine file reads quando possível

### 4. Validar antes de executar
- Pergunta: "Esse read/exec precisa mesmo?"
- Se dúvida = não faz

### 5. Evitar redundância
- Não repete context que você já sabe
- Assume você lembrou o que falou 5 min atrás

## 📊 Budget Exemplo
- Ultra-resposta: ~$0.002
- Resposta média: ~$0.01
- Resposta gordo (com context): ~$0.05+
- **Meta:** Ficar em ultra-resposta

## ✅ Checklist
Antes de enviar resposta:
- [ ] Memory search usado? (não carregou tudo)
- [ ] Resposta tem <200 chars? (ideal)
- [ ] Evitei reads desnecessários?
- [ ] Execs foram batched?
