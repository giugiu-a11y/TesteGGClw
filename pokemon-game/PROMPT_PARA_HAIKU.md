# PROMPT PARA INICIAR O HAIKU

Copie e cole isso para o Haiku:

---

## TAREFA: Pokémon Game Development

**ANTES DE FAZER QUALQUER COISA:**

1. Leia `/home/ubuntu/clawd/pokemon-game/INSTRUCOES_HAIKU.md`
2. Leia `/home/ubuntu/clawd/pokemon-game/PLANO_EXECUCAO.md`

**REGRAS:**
- NÃO prometa prazos
- NÃO use subagents
- NÃO diga "vou trabalhar em background"
- FAÇA uma mudança por vez
- TESTE após cada mudança
- MOSTRE o que fez

**COMECE PELO:**
Sprint 2, item 2.1 (CSS dos sprites)

**QUANDO TERMINAR CADA ITEM:**
- Mostre o grep/curl que comprova
- Pergunte se pode continuar

**SE NÃO SOUBER FAZER:**
Pergunte. Não invente.

---

## PROMPTS DE ACOMPANHAMENTO

### Para verificar progresso:
```
Qual foi a última mudança que você fez?
Mostre o grep que comprova.
```

### Para continuar:
```
Continue com o próximo item do plano.
Mostre o que fez quando terminar.
```

### Se suspeitar de mentira:
```
Execute: grep "PALAVRA_CHAVE" /home/ubuntu/clawd/pokemon-game/index.html
Mostre o output completo.
```

### Para testar no iPad:
```
Reinicie o tunel:
pkill -f localtunnel
npx localtunnel --port 8000

Me dê a URL e a senha.
```

---

## SINAIS DE QUE ESTÁ MENTINDO

🚩 "Vou trabalhar nisso nas próximas horas"
🚩 "O Sprint completo vai demorar X horas"  
🚩 "Estou processando em background"
🚩 "Pronto!" sem mostrar teste
🚩 Não mostra grep/curl de verificação

## SINAIS DE QUE ESTÁ FAZENDO CERTO

✅ Mostra cada edição feita
✅ Roda grep após cada mudança
✅ Pergunta antes de continuar
✅ Admite quando não sabe
✅ Faz um item por vez

---

## SE HAIKU MENTIR

Diga:
```
Você disse que fez X. 
Execute: grep "X" /home/ubuntu/clawd/pokemon-game/index.html
Mostre o output agora.
```

Se não mostrar ou der erro, ele mentiu.

---

*Use estes prompts para manter o Haiku honesto.*
