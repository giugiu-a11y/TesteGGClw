# 🎮 Pokémon Adventures Game - Estrutura Revisada & Etapas Finais

## 📁 PASTA RAIZ

```
/home/ubuntu/clawd/pokemon-game/
```

---

## 🎯 REFOCUS: HISTÓRIA ACIMA DE TUDO

**Seu ponto é crítico**: Foco deve ser **NARRATIVA DO MANGÁ**, não gamification.

> Isso muda tudo para melhor.
> Menos sistemas, mais storytelling.
> Mais "interactive visual novel com gameplay", menos "RPG mecânico".

---

## 🚨 PRIMEIRA QUESTÃO: PIKACHU SEGUE?

**No Mangá Adventures (Red Arc):**
- Pikachu NÃO segue visualmente atrás
- Viaja dentro de Poké Ball (como qualquer outro Pokémon)
- Apenas "aparece" quando chamado ou em batalha
- Relacionamento é textual (diálogos, reações)

**Sugestão Minha:**
```
❌ NÃO adicionar "Pikachu seguidor visual"
   (Isso é Yellow, não Adventures)

✅ Pikachu aparece em momentos chave:
   - Primeiro encontro (wild, selvagem)
   - Diálogos emocionais
   - Batalhas
   - Cenas importantes do mangá
```

**Você concorda ou quer algo diferente?**

---

## 📊 ETAPAS REVISADAS (NARRATIVA FIRST)

### **Fase 0: Setup & Game Loop (DIA 1 | 3-4h)**

```
✅ HTML base com Canvas
✅ Game loop 60fps
✅ Input handler (teclado + touch)
✅ Simple scene/state manager
✅ localStorage setup

Resultado: Framework pronto para história
```

**Arquivo**: `index.html` (esqueleto vazio)

---

### **Fase 1: Cena 1 - Laboratório de Oak (DIA 2 | 6-8h)**

**O que é:**
> Você entra em Pallet Town.
> Vai direto pro lab de Oak.
> Cinemática com diálogos e choices.
> Recebe Pokédex e Poliwag.
> Blue rouba Eevee.
> Oak dá Pikachu especial.

**Assets necessários:**
```
- Tileset Pallet Town (simples, 100x100 px)
- Portraits: Oak, Blue, você
- Pikachu sprite (quando aparece)
- Poliwag sprite
```

**Resultado:**
```
Você está em pallet Town
Você fala com Oak → Diálogo cinematográfico
Você recebe Poliwag
Blue aparece → Cinemática
Você recebe Pikachu
Fim da cena 1 → localStorage salva
```

**Tamanho**: ~80KB

---

### **Fase 2: Cena 2 - Encontro Selvagem (DIA 3 | 5-6h)**

**O que é:**
> Route 1.
> Rattata selvagem ataca.
> Poliwag vence (ou você escolhe ataque).
> Pikachu aparece (vê Poliwag ganhar).
> Você captura Rattata (ou não).
> Diálogo: "Pokémon sentem dor real"

**Mecânica Mínima:**
```
Batalha SIMPLIFICADA (não é RPG completo):
- Você escolhe: [Poliwag] [Bag] [Run]
- Poliwag ataca automaticamente
- Damage é texto (não animação)
- Você pode capturar com Poké Ball
- Simples, não é sistema complexo
```

**Assets:**
```
- Tileset Route 1 (grama, caminho)
- Rattata sprite (overworld + battle)
- Battle background simples
```

**Resultado:**
```
Você vê como funciona batalha
Pikachu "reconhece" Poliwag como forte
Story progride
```

**Tamanho**: +60KB

---

### **Fase 3: Cena 3 até Viridian (DIAS 4-5 | 8-10h)**

**O que é:**
> Explorar Viridian (pequena).
> Encontrar Green disfarçada (teaser).
> Ir a Pewter City.
> Diálogos com Brock (story-focused, não "gym battle tutorial").

**Sem necessidade de:**
```
❌ Gym puzzle completo
❌ Múltiplas batalhas
❌ Sistema de levels profundo
```

**Com necessidade de:**
```
✅ Diálogos que contam história
✅ Green aparição (mistério)
✅ Opções de choice que afetam narrativa
✅ Descrições do mundo
```

**Assets:**
```
- Tileset Viridian (casas, árvores)
- Tileset Pewter City
- Green portrait (disfarçada)
- Brock portrait
- Fundo batalla (genérico)
```

**Resultado:**
```
3 cidades exploradas
Personagens introduzidos
Primeira trama secundária (Green)
```

**Tamanho**: +100KB

---

### **Fase 4: Mt. Moon (DIAS 6-7 | 8-10h)**

**O que é (Narrativa Crítica):**
> Entrada de Team Rocket.
> Encontro com Rocket Grunt.
> Mt. Moon como "tutorial" de conflito.
> Pikachu provavelmente não quer lutar Team Rocket.
> Você aprende que "Pokémon sofrem mesmo".

**Story Beats:**
```
1. Você entra em Mt. Moon
2. Vê Rocket recolhendo fósseis
3. Rocket avança sobre você
4. Batalha obrigatória (Rocket Grunt)
5. Você ganha (com ajuda de Poliwag/Pikachu)
6. Fuga de Team Rocket
7. Encontra fóssil (Dome OU Helix)
8. Pikachu está ferido/assustado
9. Você cura no Pokémon Center
```

**Mecânica:**
```
Batalha contra Rocket (similar fase 2)
Diálogos emocionais
Choice: [Lutar] [Fugir]
```

**Assets:**
```
- Tileset Mt. Moon (caverna)
- Rocket Grunt sprite
- Poké Center interior
```

**Tamanho**: +80KB

---

### **Fase 5: Cerulean até Saffron (DIAS 8-10 | 12-15h)**

**O que é:**
> Misty (traiçoeira, conforme mangá).
> Lt. Surge (story-relevant).
> Celadon (team rocket hideout - CORE NARRATIVE).
> Encontro com Giovanni.
> Silph Scope (busca importante no mangá).

**Story Beats (Highlights):**
```
- Misty: Você a vence ou ela te ajuda? (choice)
- Lt. Surge: Pokémon sofrem (theme recorrente)
- Celadon: Team Rocket base (narrativa densa)
- Giovanni: First real antagonist
- Silph Scope: Descobre mistério
```

**Mecânica Mínima:**
```
- 3-4 batalhas contra gym leaders (simples)
- Diálogos pesados
- Choices que afetam relacionamento com personagens
```

**Assets:**
```
- Tilesets (Cerulean, Vermilion, Celadon, Saffron)
- Misty, Lt.Surge, Giovanni portraits
- Team Rocket grunts
```

**Tamanho**: +150KB

---

### **Fase 6: Final (Dias 11-12 | 6-8h)**

**O que é:**
> Cinnabar + Viridian (Giovanni gym).
> Indigo Plateau.
> Elite Four + Champion Blue.
> Red vs Blue (final).
> Pikachu evolui? (Raichu via amizade? → SEM ISSO!)
> Red vence.

**Nota sobre "Pikachu não evolui":**
```
No mangá Adventures, Red's Pikachu NÃO evolui para Raichu.
Ele permanece Pikachu (diferente de Yellow).
Isso é important para fidelidade.

Sua Poliwag SIM pode evoluir (Poliwrath).
```

**Assets:**
```
- Tilesets finais (volcano, cave, plateau)
- Elite Four + Blue portraits
- Boss battles (visual, não complexo)
```

**Tamanho**: +100KB

---

### **Fase 7: Post-Game (Optional | DIAS 13-15)**

**O que é:**
> Yellow Arc integration (OPCIONAL).
> Red petrificado → Yellow a salva?
> Ou simple ending.

**Você decide:**
```
A) Parar no final de Red (simples, completo)
B) Adicionar coda Yellow (mais complexo)
```

---

## 📐 RESUMO DE FASES

| Fase | Conteúdo | Dias | Size |
|------|----------|------|------|
| **0** | Framework | 1 | ~20KB |
| **1** | Oak + Pallet | 2 | +80KB |
| **2** | Batalha 1 + Route 1 | 3 | +60KB |
| **3** | Viridian-Pewter | 4-5 | +100KB |
| **4** | Mt. Moon + Team Rocket | 6-7 | +80KB |
| **5** | Gyms + Celadon + Saffron | 8-10 | +150KB |
| **6** | Final + Champion | 11-12 | +100KB |
| **7** | Yellow arc (opt) | 13-15 | +200KB |
| | | | |
| **TOTAL** (Phases 0-6) | Mangá Red completo | 12 dias | ~590KB |
| **TOTAL** (com Yellow) | Red + Yellow | 15 dias | ~790KB |

---

## 📁 ESTRUTURA DE PASTA FINAL

```
/home/ubuntu/clawd/pokemon-game/
│
├── 📄 index.html (ARQUIVO ÚNICO FINAL)
│
├── 📁 src/ (desenvolvimento)
│   ├── main.js (game loop)
│   ├── scene-manager.js (cenas/diálogos)
│   ├── battle-simple.js (batalha mínima)
│   ├── input.js (controles)
│   ├── renderer.js (canvas drawing)
│   └── state.js (save/load localStorage)
│
├── 📁 assets/ (resources RAW)
│   ├── sprites/
│   │   ├── player-red.png (4 direções)
│   │   ├── pikachu.png
│   │   ├── poliwag.png
│   │   ├── rattata.png
│   │   ├── gym-leaders.png (sprites)
│   │   └── ...
│   │
│   ├── tilesets/
│   │   ├── pallet.png
│   │   ├── route1.png
│   │   ├── viridian.png
│   │   ├── pewter.png
│   │   ├── mtmoon.png
│   │   ├── cerulean.png
│   │   ├── vermilion.png
│   │   ├── celadon.png
│   │   ├── saffron.png
│   │   ├── cinnabar.png
│   │   ├── viridian-gym.png
│   │   └── indigo-plateau.png
│   │
│   ├── portraits/
│   │   ├── oak.png
│   │   ├── blue.png
│   │   ├── green.png
│   │   ├── misty.png
│   │   ├── brock.png
│   │   ├── surge.png
│   │   ├── erika.png
│   │   ├── koga.png
│   │   ├── blaine.png
│   │   ├── giovanni.png
│   │   ├── elite-four.png
│   │   └── ...
│   │
│   └── data/
│       ├── story.json (diálogos + scenes)
│       ├── maps.json (mapa layout)
│       ├── npcs.json (personagens)
│       └── pokemon-data.json (Pokémon stats)
│
├── 📁 build/ (output final)
│   └── index.html (GERADO - arquivo único pronto)
│
├── 📁 tools/
│   ├── build.sh (gera arquivo final)
│   ├── compress-assets.sh (PNG → Base64)
│   └── dev-server.sh (roda localhost)
│
└── 📄 README.md (instruções)
```

---

## 🔧 WORKFLOW DIÁRIO

```bash
# 1. Editar código
vim /home/ubuntu/clawd/pokemon-game/src/scene-manager.js

# 2. Testar localmente
cd /home/ubuntu/clawd/pokemon-game/
python3 -m http.server 8080
# Abrir iPad → http://seu-ip:8080

# 3. Editar assets (imagens)
# Você salva em assets/sprites/, assets/tilesets/, etc

# 4. Quando pronto, buildar
./tools/build.sh
# Gera → build/index.html (~600KB, pronto para jogar)

# 5. Deploy
git push
# GitHub Actions auto-publica em:
# https://seu-usuario.github.io/pokemon-game/
```

---

## 📝 STORY.JSON EXEMPLO

```json
{
  "scenes": [
    {
      "id": "scene_oak_lab",
      "location": "pallet_town",
      "description": "Laboratório do Professor Oak",
      "dialogues": [
        {
          "speaker": "Oak",
          "portrait": "oak_neutral",
          "text": "Olá! Bem-vindo ao mundo Pokémon. Meu nome é Oak.",
          "choices": null
        },
        {
          "speaker": "Oak",
          "portrait": "oak_happy",
          "text": "Existem criaturas neste mundo chamadas Pokémons. Você pode capturá-las e treiná-las.",
          "choices": null
        },
        {
          "speaker": "You",
          "portrait": "red_neutral",
          "text": "...",
          "choices": null
        },
        {
          "speaker": "Oak",
          "portrait": "oak_serious",
          "text": "Aqui. Esta é sua Pokédex. E este é seu Pokémon parceiro.",
          "choices": null,
          "action": "give_poliwag"
        }
      ]
    },
    {
      "id": "scene_blue_steals",
      "location": "pallet_town_outside",
      "dialogues": [
        {
          "speaker": "Blue",
          "portrait": "blue_arrogant",
          "text": "Hahahaha! Você pensa que pode vencer comigo? Fácil!",
          "choices": null
        }
      ],
      "action": "blue_steals_eevee"
    }
  ]
}
```

---

## 🎬 O QUE NÃO VAI TER

```
❌ Amizade sistema complexo
❌ EV/IV sistema
❌ Shiny Pokémons
❌ Múltiplas gerações (só Gen 1)
❌ Pokéwalker
❌ Pikachu seguidor visual
❌ Mini-games
❌ Breeding
❌ Competitivo online
```

---

## ✅ O QUE VAI TER

```
✅ Narrativa mangá completa (Red arc)
✅ Diálogos fiéis
✅ Personagens com personality
✅ Batalhas que contam história
✅ Choices que afetam narrativa
✅ Pokémons que "sofrem"
✅ Visual bonito (colorido, 2026)
✅ Leve & rápido (iPad 4G)
✅ Save/Load (localStorage)
✅ Tudo em 1 arquivo HTML
```

---

## 🚀 PRÓXIMO PASSO

**Você concorda com esta estrutura?**

```
[ ✅ PERFEITO! Começa agora Sprint 0 ]
[ 🤔 Quer ajustar algo? ]
```

Se concordar, em **2 horas você tem:**
- Pasta criada e estruturada
- Game loop rodando
- Primeiro diálogo testável
- Pronto para iTunes no iPad

Bora? 🎮
