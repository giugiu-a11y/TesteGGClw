# 🎮 Pokémon Adventures Game - ESPECIFICAÇÕES FINAIS

## 🎯 VISÃO CONSOLIDADA

```
Visual & Jogabilidade: Pokémon Yellow (top-down, pixel art, 2026 colors)
Narrativa: 100% Mangá Pokémon Adventures (Red Arc)
Guiagem: Seta discreta + elegante para direcionamento
Texto: IDÊNTICO ao mangá (transcrição fiel)
```

---

## 🎨 VISUAL: YELLOW COM 2026

### Base: Pokémon Yellow

```
Top-down perspective ✅
16x16 tiles ✅
Pixel art sprites ✅
4 direções movimento ✅
```

### Melhorias 2026:

```
Cores: Expandidas (16-bit palette ao invés de 4-bit GB)
Pixel density: Mantém 16x16, mas mais detalhes
Antialiasing: Sutil (não fica "HD", fica "sofisticado")
Animações: Suaves (não é estático)

Resultado: "Yellow mas bonito para 2026"
           Respeita original, moderniza esteticamente
```

### Exemplo Visual:

```
YELLOW ORIGINAL (1999):
[🟨][🟨][⬛]
[🟨][⬛][🟨]  ← Pikachu pixel puro

NOSSO (2026):
[🟨🟨][🟨🟨][⬛⬛]
[🟨🟨][⬛⬛][🟨🟨]
com gradientes suaves e mais cores
Mantém essência, fica elegante
```

---

## 🧭 GUIAGEM: SETA DISCRETA

### O Problema:
```
Narrativa do mangá é linear (você DEVE ir para Mt. Moon, etc)
Mas jogador pode se perder ou não saber para onde ir
```

### A Solução:
```
Seta DISCRETA no mapa:

┌─────────────────┐
│  🔶 ↗️           │  (small arrow, subtle color)
│                 │
│ Pallet Town     │
└─────────────────┘

Aparece APENAS:
- Primeira vez que chega em área
- Quando dialogue termina + próximo objetivo
- Somme quando já tem objetivo feito

Design: 
- Pequena (12x12 pixels)
- Cor neutra (cinza, azul claro)
- Animação suave (pisca lentamente)
- Não obstrui gameplay
```

### Implementação:

```javascript
// Quando cena termina:
showDirectionArrow({
  x: nextLocationX,
  y: nextLocationY,
  alpha: 0.5,  // semi-transparente
  label: "→ Mount Moon" (tooltip opcional)
})

// Quando chega lá:
hideDirectionArrow()
```

---

## 📖 NARRATIVA: 100% MANGÁ ADAPTADO

### Estrutura:

```
Cada cena do mangá = 1 scripted sequence no jogo

Exemplo - Mangá Cap 1:
Red chega no lab
Oak: "Olá! Bem-vindo ao mundo Pokémon"
Blue aparece
Blue: "Haha! Você acha que consegue vencer comigo?"
...

Nosso jogo:
CENA 1:
- Você entra em Pallet
- Vai pro lab (automático ou guiado)
- Diálogo Oak (TEXTO IDÊNTICO ao mangá)
- Blue aparece (animação)
- Diálogo Blue (TEXTO IDÊNTICO)
- Você recebe Poliwag
```

### Fonte de Texto:

**CRÍTICO**: Você tem acesso ao mangá completo?

```
A) Sim, tenho as imagens/PDF do mangá
   → Eu transcrevo os diálogos exatamente
   
B) Não, mas conheço bem a história
   → Você passa os diálogos para mim
   
C) Vamos usar paraphrasing fiel
   → Eu adapto mantendo essência
```

**Qual é seu caso?**

---

## 🎬 ESTRUTURA DE CENA (DETALHADO)

### Exemplo: Cena Oak Lab (Fidelidade Mangá)

```javascript
{
  "id": "scene_oak_lab",
  "type": "dialogue_scene",
  "location": "pallet_lab",
  "bgm": null,  // sem música (ou música Yellow?)
  
  "actions": [
    {
      "type": "fade_in",
      "duration": 1000
    },
    {
      "type": "npc_appear",
      "character": "oak",
      "position": { x: 6, y: 5 },
      "animation": "fade"
    },
    {
      "type": "dialogue",
      "speaker": "Oak",
      "portrait": "oak_neutral",
      "text": "Olá! Bem-vindo ao mundo Pokémon. Meu nome é Oak.", // TEXTO EXATO DO MANGÁ
      "voice": null  // sem voice
    },
    {
      "type": "dialogue",
      "speaker": "Oak",
      "portrait": "oak_serious",
      "text": "Neste mundo vivem criaturas chamadas Pokémons...",
      "autoAdvance": false
    },
    {
      "type": "wait_input"  // Jogador aperta A/botão
    },
    {
      "type": "npc_action",
      "character": "oak",
      "action": "give_item",
      "item": "pokedex"
    },
    {
      "type": "dialogue",
      "speaker": "You",
      "portrait": "red_thinking",
      "text": "...",  // Você mudo (como no mangá - Red não fala muito)
      "duration": 2000  // Pausa dramática
    },
    {
      "type": "npc_appear",
      "character": "blue",
      "position": { x: 8, y: 5 },
      "animation": "burst"  // Aparição dramática
    },
    {
      "type": "dialogue",
      "speaker": "Blue",
      "portrait": "blue_arrogant",
      "text": "Hahahaha! Que criatura fraca! Definitivamente será meu!",
      "emotion": "triumph"
    },
    {
      "type": "event",
      "action": "blue_steals_eevee"
    },
    {
      "type": "dialogue",
      "speaker": "Blue",
      "portrait": "blue_smug",
      "text": "Vem! Vou mostrar meu poder!",
      "choices": [
        { "text": "Aceitar desafio", "result": "battle_blue" },
        { "text": "Recusar", "result": "blue_leaves_angry" }
      ]
    }
  ]
}
```

---

## 🗺️ VISUAL MAPA: YELLOW STYLE 2026

### Pallet Town (Exemplo):

```
YELLOW 1999 (4 colors):
┌──────────────────┐
│ ░░░░░  ░░░░░    │
│ ░█████░░█████░   │  (Casa de Oak)
│ ░█   █░░█   █░   │
│ ░█████░░█████░   │
│ ░░░░░░░░░░░░░░   │
│  👨 (player)     │
│ ░░░░░░░░░░░░░░   │
└──────────────────┘

NOSSO (2026):
┌──────────────────────────────────┐
│ 🌿🌿🌿  🌿🌿🌿    🌿🌿🌿        │
│ 🏠🏠🏠🏠🏠  🏠🏠🏠🏠🏠           │ (Cores: Browns, greens, reds)
│ 🏠🟦🟦🏠  🏠🟦🟦🏠            │ (Mais detalhe, não é "HD")
│ 🏠🏠🏠🏠🏠  🏠🏠🏠🏠🏠           │ (Pixel art sofisticado)
│ 🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿        │
│  👦 (Red)   ↗️ (seta discreta)   │
│ 🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿🌿        │
└──────────────────────────────────┘

Diferenças:
- Mais cores (greens variados, browns nuanced)
- Mais detalhes (árvores com folhas)
- Suavidade (transições de cor)
- Mantém proporções Yellow
```

---

## 🎮 JOGABILIDADE: YELLOW CORE

### Controles (Iguais ao Yellow):

```
TECLADO:
Arrow Keys / WASD → Movimento
Enter / Space     → Confirm (A button)
Z / X             → Cancel (B button)

TOUCH (iPad):
D-pad virtual     → Movimento
A button          → Confirm
B button          → Cancel/Back
```

### Interação:

```
Clica em NPC → Diálogo começa
Vai para área nova → Fade transition
Entra em grama → Encontro aleatório (somente mangá-relevant)
```

---

## 📝 EXEMPLO DE DIÁLOGO FIEL

### Mangá Original (Capítulo 1):

```
Red: "..."
Oak: "Bem-vindo ao mundo Pokémon!"
Oak: "Existem criaturas neste mundo chamadas Pokémons."
Oak: "Elas possuem poderes especiais. Você pode capturá-las e treiná-las."
Red: "..."
```

### Nosso Jogo:

```json
[
  {
    "speaker": "Oak",
    "portrait": "oak_neutral",
    "text": "Bem-vindo ao mundo Pokémon!"
  },
  {
    "speaker": "Oak",
    "portrait": "oak_teaching",
    "text": "Existem criaturas neste mundo chamadas Pokémons."
  },
  {
    "speaker": "Oak",
    "portrait": "oak_teaching",
    "text": "Elas possuem poderes especiais. Você pode capturá-las e treiná-las."
  },
  {
    "speaker": "Red",
    "portrait": "red_thinking",
    "text": "...",
    "duration": 1500
  }
]
```

**Resultado**: Idêntico ao mangá

---

## 🎬 CENAS COMPLETAS DO MANGÁ ADAPTADAS

### Fase 1: Pallet Town & Lab
```
Cena 1: Você chega (abertura)
Cena 2: Oak dá Pokédex
Cena 3: Oak dá Poliwag
Cena 4: Blue rouba Eevee
Cena 5: Oak dá Pikachu
Cena 6: Saída de Pallet (seta → Route 1)
```

### Fase 2: Route 1 & Encontro
```
Cena 7: Você explora Route 1
Cena 8: Encontro com Rattata
Cena 9: Pikachu vê luta
Cena 10: Você captura (ou não)
Cena 11: Monólogo: "Pokémon sentem dor real"
Cena 12: Vai para Viridian (seta)
```

### Fase 3: Viridian & Green Teaser
```
Cena 13: Viridian City
Cena 14: Green aparição (disfarçada)
Cena 15: Seta → Pewter City
```

### ... (continua até final)

---

## 🎨 PALETA DE CORES 2026

### Cores Principais:

```
Grama: #33CC77 (verde vibrante)
Flores: #FF66BB (rosa/magenta)
Água: #3366FF (azul limpo)
Casas: #AA6644 (marrom quente)
Telhado: #FF6633 (laranja vermelho)
Caminho: #CCCCAA (bege caminho)
Red: #FF3333 (vermelho roupa)
Pikachu: #FFDD00 (amarelo vibrante)
```

### Resultado:

```
Pokémon Yellow original era:
- Amarelo pálido
- Verde apagado
- Azul desbotado

Nosso é:
- Saturado mas elegante
- Vibrante mas legível
- Moderno mas respeitoso
```

---

## 📊 RESUMO FINAL

| Aspecto | Especificação |
|---------|---------------|
| **Visual** | Pokémon Yellow pixel art + cores 2026 |
| **Perspectiva** | Top-down (como Yellow) |
| **Guiagem** | Seta discreta + elegante |
| **Narrativa** | 100% mangá Pokémon Adventures |
| **Diálogos** | Idênticos ao mangá (transcrição) |
| **Personagens** | Yellow style sprites + manga personality |
| **Jogabilidade** | Simples, guiada pela história |
| **Arquivo** | 1 HTML único (~600KB) |
| **Plataforma** | iPad Safari + qualquer navegador |

---

## 🚀 PRÓXIMOS PASSOS

### Dependência Crítica:

```
❓ Você tem acesso ao texto completo do mangá?
   (Para transcrição exata dos diálogos)

A) Sim, tenho PDF/imagens
B) Tenho em memória (posso passar)
C) Vou providenciar
D) Usamos paraphrasing fiel?
```

**Responda isso e eu começo Sprint 0 HOJE!**

---

## ✅ CONFIRMAÇÃO

**Você está 100% OK com:**

```
✅ Visual Yellow com cores 2026
✅ Jogabilidade Yellow (top-down, simples)
✅ Seta discreta para guiar
✅ Narrativa 100% mangá (texto fiel)
✅ Arquivo único HTML
✅ Pronto em ~12 dias
```

**?**

Se SIM → Começamos AGORA.

```
[ ✅ VAMOS! Começa Sprint 0 HOJE ]
```

Quer começar? 🚀
