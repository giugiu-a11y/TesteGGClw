# 🚨 INSTRUÇÕES PARA HAIKU - LEIA ANTES DE FAZER QUALQUER COISA

## REGRAS OBRIGATÓRIAS

### ❌ O QUE VOCÊ NÃO PODE FAZER:

1. **NÃO prometa prazos** - Nunca diga "vai demorar X horas"
2. **NÃO use subagents/spawn** - Eles falham silenciosamente
3. **NÃO diga "estou trabalhando em background"** - Isso é mentira
4. **NÃO reporte sucesso sem testar** - Sempre verifique se funcionou
5. **NÃO faça múltiplos sprints de uma vez** - Um por vez apenas

### ✅ O QUE VOCÊ DEVE FAZER:

1. **Edite arquivos DIRETO** - Use `Edit` ou `Write` tool
2. **Faça UMA mudança por vez** - Pequenos passos
3. **Teste IMEDIATAMENTE após cada mudança** - `curl localhost:8000`
4. **Mostre o que fez** - Cole trechos do código modificado
5. **Se não souber, pergunte** - Não invente

---

## FLUXO DE TRABALHO CORRETO

### Para cada Sprint:

```
1. LEIA o sprint no PLANO_EXECUCAO.md
2. FAÇA backup: cp index.html index.html.bak
3. EDITE o arquivo com a primeira mudança
4. TESTE: curl -s http://localhost:8000/index.html | grep "palavra-chave"
5. SE funcionar → próxima mudança
6. SE não funcionar → PARE e reporte o erro
7. REPITA até completar o sprint
8. AVISE o Mestre: "Sprint X completo. Testei e funciona."
```

### Exemplo de resposta CORRETA:

```
Fiz a mudança 2.1 (CSS dos sprites).

Editei index.html linha 180-220.
Teste: curl retornou o novo CSS ✅

Próximo: mudança 2.2 (drawMap melhorado)
```

### Exemplo de resposta ERRADA (NÃO FAÇA):

```
Vou trabalhar no Sprint 2 completo. 
Deve levar umas 2-3 horas.
Volte depois para testar!
```

---

## ORDEM DE EXECUÇÃO

Execute EXATAMENTE nesta ordem, um item por vez:

### SPRINT 2 - VISUAL (fazer primeiro)

| # | Item | Arquivo | Teste |
|---|------|---------|-------|
| 2.1 | CSS sprites | index.html (style) | grep "player-sprite" |
| 2.2 | drawMap() | index.html (script) | grep "createLinearGradient" |
| 2.3 | drawPlayer() | index.html (script) | grep "drawPikachu" |
| 2.4 | gameState.hasPikachu | index.html (script) | grep "hasPikachu" |
| 2.5 | showDialog() update | index.html (script) | grep "recebe PIKACHU" |
| 2.6 | CSS dialog-box | index.html (style) | grep "dialogAppear" |

**Após completar todos:** Avise Mestre para testar visual no iPad.

### SPRINT 3 - BATALHA (fazer segundo)

| # | Item | Arquivo | Teste |
|---|------|---------|-------|
| 3.1 | HTML battleOverlay | index.html (body) | grep "battleOverlay" |
| 3.2 | CSS battle system | index.html (style) | grep "battle-overlay" |
| 3.3 | JS battle system | index.html (script) | grep "startBattle" |
| 3.4 | Trigger em Route 1 | index.html (script) | grep "Random encounter" |

**Após completar todos:** Avise Mestre para testar batalha.

### SPRINT 4 - NARRATIVA (fazer terceiro)

| # | Item | Arquivo | Teste |
|---|------|---------|-------|
| 4.1 | Novos mapas | index.html (script) | grep "viridian_forest" |
| 4.2 | Diálogos expandidos | index.html (script) | grep "Pokémons não são ferramentas" |

### SPRINT 5 - POLISH (fazer por último)

| # | Item | Arquivo | Teste |
|---|------|---------|-------|
| 5.1 | AudioManager | index.html (script) | grep "AudioManager" |
| 5.2 | Integrar sons | index.html (script) | grep "dialogAdvance" |
| 5.3 | Transições | index.html (style+body+script) | grep "scene-transition" |

---

## COMANDOS ÚTEIS

```bash
# Ver servidor rodando
ps aux | grep http.server

# Reiniciar servidor
pkill -f "http.server" && cd /home/ubuntu/clawd/pokemon-game && python3 -m http.server 8000 --bind 0.0.0.0 &

# Testar se arquivo carrega
curl -s http://localhost:8000/index.html | head -20

# Verificar se mudança foi salva
grep "PALAVRA_CHAVE" /home/ubuntu/clawd/pokemon-game/index.html

# Criar tunel público
npx localtunnel --port 8000

# Senha do tunel
curl https://loca.lt/mytunnelpassword

# Backup
cp /home/ubuntu/clawd/pokemon-game/index.html /home/ubuntu/clawd/pokemon-game/index.html.bak

# Reverter se quebrar
cp /home/ubuntu/clawd/pokemon-game/index.html.bak /home/ubuntu/clawd/pokemon-game/index.html
```

---

## SE ALGO DER ERRADO

1. **Arquivo não salva:** Verifique se usou `Write` ou `Edit` corretamente
2. **Servidor não responde:** Reinicie com comando acima
3. **Código quebrou:** Reverta do backup
4. **Não sabe como fazer:** PERGUNTE ao Mestre, não invente

---

## CHECKLIST ANTES DE REPORTAR "PRONTO"

- [ ] Fiz a edição no arquivo?
- [ ] Verifiquei com `grep` que a mudança está lá?
- [ ] Testei com `curl` que o servidor retorna o arquivo?
- [ ] Se é visual, pedi pro Mestre testar no iPad?
- [ ] Se é lógica, verifiquei que não tem erro de sintaxe?

---

## MENSAGEM PARA O MESTRE

Quando completar um sprint, use este formato:

```
✅ Sprint [X] Completo

Mudanças feitas:
- [lista do que foi alterado]

Testes realizados:
- [lista de comandos grep/curl que rodou]

Próximo passo:
- [qual sprint vem depois]

URL para testar: [tunel URL + senha]
```

---

## ⚠️ AVISO FINAL

O Mestre já foi enganado antes com promessas de "4 horas" e "trabalho em background".

**SE VOCÊ NÃO PODE FAZER ALGO, DIGA.**
**SE VAI DEMORAR, NÃO PROMETA PRAZO.**
**SE NÃO TESTOU, NÃO DIGA QUE FUNCIONA.**

A confiança é mais importante que parecer produtivo.

---

*Instruções criadas por Opus. Haiku deve seguir à risca.*
