# Pokémon Adventures: Plano de Desenvolvimento Realista

## 🎯 Objetivo Final
Um jogo Pokémon **100% navegador** (single HTML file) rodando no iPad Safari.
- Fiel ao mangá Pokémon Adventures (diálogos, narrativa)
- Estilo gráfico Yellow (pixel art, cores vibrantes 2026)
- Responsivo touch + 60fps
- **Tamanho alvo: <5MB** (para load instantâneo)

---

## 📊 Arquitetura & Tamanho de Arquivo

### Breakdown de Espaço:

```
index.html (arquivo único) ~4-5MB
├── HTML estrutura         ~5KB
├── CSS inline            ~30KB
├── JavaScript            ~150KB
├── Base64 assets (OTIMIZADO)  ~4.8MB
│   ├── Sprites comprimidos   ~2.5MB
│   ├── Tileset              ~1.2MB
│   ├── Portraits NPCs/Bosses ~800KB
│   └── Animações (spritesheet) ~500KB
└── JSON dados (story/maps)   ~20KB
```

### Estratégia de Compressão:

1. **Sprites**: Usar **TinyPNG** ou **ImageMagick** para reduzir cores a 256 sem perder qualidade (Gen-1 tinha paleta limitada)
2. **Tilesets**: Um único spritesheet 256x256 com padrão repetido
3. **Base64**: Comprimir com **gzip** antes de encodar (JavaScript descomprime)
4. **Minificação**: UglifyJS + CSS minifier
5. **Lazy loading**: Carregar assets em fases (splash → overworld → primeira batalha)

---

## 🏗️ Fases de Desenvolvimento

### **Fase 0: Setup & Prototipagem (2-3 dias)**
**Custo AWS: ~$0** (tudo local)

- [ ] Fork repo local para `/home/ubuntu/clawd/pokemon-game/`
- [ ] Estrutura HTML + CSS + JS básica
- [ ] Canvas renderizado (60fps loop)
- [ ] D-pad virtual + botões táteis funcionando
- [ ] Teste no iPad via `http://localhost:8080`

**Entrega**: Arquivo HTML rodando, sem gráficos ainda

---

### **Fase 1: Mapa & Movimento (3-5 dias)**
**Custo AWS: ~$0** (desenvolvimento local)

**Objetivo**: Rodar no iPad, explorar Pallet Town + Route 1

**Assets necessários** (você ripa de spriters-resource):

```bash
# Sprites do personagem (Red/Yellow)
# - Idle (4 direções)
# - Walk (4 direções, 2 frames cada)
# - Total: 4 sprites ~3KB cada

# Pikachu seguidor
# - Idle, walk, happy, sad (amizade)
# - Total: 4 sprites ~2KB cada

# Tileset Kanto (Pallet Town)
# - Grama, flores, casas, água
# - Spritesheet 256x256 com repetição
# - ~200KB (depois otimizado para ~30KB)

# Map data (JSON)
# Pallet Town: 32x32 tiles
# Colisões, warps, eventos
# ~5KB
```

**Código core**:
```javascript
// Game loop
requestAnimationFrame(gameLoop)

// Renderização
canvas.drawImage(tilesetImage, srcX, srcY, 16, 16, ...)

// Movimento
if (keys.ArrowUp) player.y -= speed

// Colisões
if (isWalkable(nextX, nextY)) player.x = nextX

// Pikachu follow AI
pikachuX += (playerX - pikachuX) * 0.15  // smooth follow
```

**Entrega**: Explorar mapa, Pikachu seguindo, save em `localStorage`

---

### **Fase 2: Diálogos & Narrativa (3-4 dias)**
**Custo AWS: ~$0** (local)

**Objetivo**: Primeira sequência do mangá (Oak, Pokédex, starter)

**Assets necessários**:
```bash
# Portraits NPCs (Prof. Oak, Blue, etc.)
# - 96x96 png
# - 1-2 frames para expressões
# - ~5KB cada NPC

# Texto estruturado (JSON)
{
  "chapter1": {
    "scene_oak_lab": [
      {
        "speaker": "Oak",
        "portrait": "oak_neutral",
        "text": "Olá, jovem! Bem-vindo ao mundo Pokémon!",
        "choices": ["Obrigado", "..."]
      }
    ]
  }
}
```

**Código core**:
```javascript
// Dialog system
class DialogBox {
  display(speaker, text, portraitKey) {
    // Renderiza caixa + portrait + texto
    // Animação: fade in / typewriter effect
  }
}

// State machine
gameState = 'DIALOG' → show dialog → wait input → next scene
```

**Entrega**: Cinemática inicial com Oak, obter Pokédex e Poliwag

---

### **Fase 3: Sistema de Batalha Simplificado (4-5 dias)**
**Custo AWS: ~$0** (local, talvez EC2 para compilar/testar)

**Objetivo**: Batalha 1v1 básica (seu Pikachu vs Pokémon selvagem)

**Assets necessários**:
```bash
# Battle sprites (front view)
# - Seu Pikachu: normal, hurt, faint
# - Pokémon inimigo (Rattata, Pidgeotto, etc.)
# - ~8KB cada

# Animações (spritesheet)
# - Attack flash, damage recoil
# - ~20KB comprimido
```

**Mecânicas**:
- Turn-based: **Player** → **Enemy** → repeat
- 4 opções: **Fight** (ataque), **Pokémon** (switch), **Bag** (item), **Run**
- Cálculo tipo/efetividade (tabela simples)
- Leveling up pós-vitória
- Captura com Poké Ball

**Código core**:
```javascript
class Battle {
  playerPokemon = { hp: 35, level: 5, moves: ['Thunderbolt'] }
  enemyPokemon = { hp: 20, level: 3, moves: ['Tackle'] }
  
  playerAttack(moveIndex) {
    damage = calcDamage(playerPokemon, moveIndex, enemyPokemon)
    enemyPokemon.hp -= damage
    if (enemyPokemon.hp <= 0) win()
  }
}
```

**Entrega**: Encontro aleatório → batalha → vitória/derrota → voltar ao mapa

---

### **Fase 4: Mais Conteúdo (expandível)**

Após as 3 fases, você terá uma base sólida para adicionar:
- Mais cidades e maps
- Mais Pokémons e moves
- Sistema de inventário completo
- Gyms com lógica de batalha
- Progresso de story (capítulos do mangá)
- Múltiplos personagens jogáveis (Red → Yellow)

---

## 🛠️ Tech Stack & Ferramentas

### Desenvolvimento Local:
```bash
# Editor: VSCode
# Teste: Live Server (http://localhost:8080)
# Browser: Safari (iPad) via local network
# Versionamento: Git (GitHub privado recomendado)

# Otimização:
# - ImageMagick (comprimir PNGs)
# - ImageOptim (macOS) ou OptiPNG (Linux)
# - UglifyJS (minificar JS)
# - gzip (comprimir antes de Base64)
```

### Ferramentas de Asset:
```bash
# Rip de spriters-resource: chrome downloader
# Edição: Aseprite OU Piskel (gratuito)
# Composição: ImageMagick + script shell

# Script para converter PNG → Base64:
base64 < sprite.png | gzip | base64 > sprite.base64.txt
```

---

## 💰 Estratégia de Custo AWS

### **O que NÃO fazer:**
❌ Hospedagem contínua de EC2 para dev
❌ Lambda invocações constantes
❌ Armazenamento ilimitado

### **O que FAZER:**
✅ **Desenvolver LOCALMENTE** (VSCode + Live Server)
✅ **Testar no iPad via rede local** (mesmo wifi)
✅ **S3 apenas para distribuição final** (~$0.50/mês para 5MB)
✅ **CloudFront CDN (opcional)** para cache global (~$0/mês se <10GB/mês)
✅ **GitHub Pages (MELHOR)**: hospedar o arquivo `.html` gratuitamente!

### Custo Estimado Total:
- **Local dev**: $0
- **GitHub Pages hospedagem**: $0 (gratuito, domínio personalizado opcional)
- **S3 backup** (opcional): ~$1-2/mês
- **Total**: **~$0-2/mês**

---

## 📁 Estrutura de Diretórios

```
/home/ubuntu/clawd/pokemon-game/
├── index.html (arquivo único, gerado no final)
├── src/
│   ├── main.js (game loop, state machine)
│   ├── canvas-renderer.js (desenho)
│   ├── input-handler.js (controles)
│   ├── game-state.js (save/load localStorage)
│   ├── battle-system.js
│   ├── dialog-system.js
│   └── assets-loader.js (Base64 → Image objects)
├── assets/
│   ├── sprites/ (PNG originais)
│   │   ├── player-red.png
│   │   ├── pikachu-follow.png
│   │   └── ...
│   ├── tilesets/ (PNG)
│   │   └── kanto-overworld.png
│   ├── portraits/ (PNG)
│   │   ├── oak.png
│   │   ├── blue.png
│   │   └── ...
│   ├── data/ (JSON)
│   │   ├── maps.json (estrutura de mapas)
│   │   ├── story.json (diálogos + eventos)
│   │   ├── pokemon.json (stats dos Pokémons)
│   │   └── moves.json (movimentos e dano)
├── build/ (output)
│   └── index.html (gerado, pronto para rodar)
├── tools/
│   ├── build.sh (combina tudo em um HTML)
│   ├── compress-assets.sh (PNG → Base64 comprimido)
│   └── test-local.sh (sobe server e abre Safari)
└── docs/
    ├── ARCHITECTURE.md
    ├── STORY_BREAKDOWN.md
    └── GAMEPLAY_MECHANICS.md
```

---

## 🔄 Workflow de Desenvolvimento

### **Dia a dia**:

```bash
# 1. Editar assets / código
vim src/main.js
open assets/sprites/pikachu.png

# 2. Testar localmente
cd pokemon-game/
python3 -m http.server 8080
# Abrir Safari → http://localhost:8080

# 3. Testar no iPad (mesmo wifi)
# Abrir Safari no iPad → http://<seu-mac-ip>:8080

# 4. Fazer commit
git add -A
git commit -m "feat: diálogo Oak implementado"
git push

# 5. Quando pronto, buildar final
./tools/build.sh
# Gera: build/index.html (~4-5MB, pronto para Safari)
```

### **Build final**:

```bash
#!/bin/bash
# build.sh

echo "1. Comprimindo assets..."
./tools/compress-assets.sh

echo "2. Minificando JS..."
uglifyjs src/*.js -o src/bundle.min.js

echo "3. Minificando CSS..."
cleancss style.css -o style.min.css

echo "4. Gerando HTML único..."
cat > build/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
<style>
/* CSS minificado aqui -->
</style>
</head>
<body>
<canvas id="gameCanvas"></canvas>
<script>
// JS minificado aqui
// Assets Base64 aqui
const ASSETS = {
  playerRed: "data:image/png;base64,iVBORw0KG...",
  pikachu: "data:image/png;base64,iVBORw0KG...",
  tilesetKanto: "data:image/png;base64,iVBORw0KG..."
}
</script>
</body>
</html>
EOF

echo "5. Testando..."
du -h build/index.html
echo "Pronto para rodar! ✅"
```

---

## 📋 Checklist de Fases

### **Fase 0: Setup (dias 1-3)**
- [ ] Repo local estruturado
- [ ] HTML + canvas + game loop rodando
- [ ] D-pad virtual funcional
- [ ] Teste no iPad via localhost

### **Fase 1: Mapa (dias 4-8)**
- [ ] Tileset Kanto ripeado e otimizado
- [ ] Renderização de mapa
- [ ] Movimento do player
- [ ] Pikachu seguidor com IA
- [ ] Colisões implementadas
- [ ] Save/load localStorage

### **Fase 2: Narrativa (dias 9-12)**
- [ ] Portraits dos NPCs otimizados
- [ ] Dialog system implementado
- [ ] Cinemática Oak (Pokédex, starter)
- [ ] State machine de eventos

### **Fase 3: Batalha (dias 13-17)**
- [ ] Battle sprites ripeados
- [ ] Sistema de turno básico
- [ ] Cálculo de dano e tipos
- [ ] Encontro aleatório funcional
- [ ] Captura com Poké Ball

### **Fase 4: Polish (dias 18-20)**
- [ ] Otimização de performance
- [ ] Testes no iPad
- [ ] Build final
- [ ] Deploy no GitHub Pages

---

## 🚀 Timeline Realista

**Total: 20-25 dias** (trabalhando ~4-6 horas/dia)

Se você trabalhar **2 horas/dia**: ~40-50 dias
Se você trabalhar **8 horas/dia**: ~10-15 dias (possível com foco)

---

## 📝 Próximas Ações

1. **Criar repo local** com estrutura de diretórios
2. **Configurar Live Server** para testes no iPad
3. **Riper sprites** de spriters-resource (começa com player + Pikachu)
4. **Prototipar game loop** (canvas + input)
5. **Testar performance** no iPad (importante!)

---

## ⚠️ Riscos & Mitigação

| Risco | Impacto | Mitigação |
|-------|--------|----------|
| Arquivo HTML > 5MB | Não carrega no iPad | Usar gzip + otimizar assets |
| Performance ruim (fps drops) | Injogável | Profile com DevTools Safari, limitar renderings |
| Assets ripeados com copyright | Legal issue | Usar assets para prototipagem, criar originais depois |
| Tempo estimado errado | Projeto estende | Quebrar em MVPs, versão 1.0 pode ser reduzida |

---

## 📌 MVPs (Minimum Viable Product)

**MVP 1.0**: Rodar, explorar Pallet Town, dialogue inicial
**MVP 1.5**: + batalha vs 1 Pokémon, capturar, level up
**MVP 2.0**: + mais cidades, mais diálogos, salvar progresso
**MVP 3.0**: + 8 gyms, Elite Four, final do mangá

---

**Pronto para começar?**
