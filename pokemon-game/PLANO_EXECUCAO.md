# 🎮 POKÉMON ADVENTURES - PLANO DE EXECUÇÃO COMPLETO

**Objetivo:** Jogo fiel ao mangá Pokémon Adventures + jogabilidade estilo Pokémon Yellow (2026, colorido)
**Arquivo principal:** `/home/ubuntu/clawd/pokemon-game/index.html`
**URL de teste:** `https://stupid-teams-report.loca.lt` (ou reiniciar localtunnel)
**Status atual:** Sprint 1 funcional (esqueleto básico)

---

## 📋 ÍNDICE

1. [Sprint 2: Visual Upgrade](#sprint-2-visual-upgrade)
2. [Sprint 3: Sistema de Batalha](#sprint-3-sistema-de-batalha)
3. [Sprint 4: Narrativa Expandida](#sprint-4-narrativa-expandida)
4. [Sprint 5: Polish Final](#sprint-5-polish-final)

---

## SPRINT 2: VISUAL UPGRADE

### 2.1 Substituir Emojis por Sprites CSS

**Onde:** Dentro do `<style>` tag, adicionar após `.dialog-text`:

```css
/* ==================== SPRITES ==================== */

.sprite {
    image-rendering: pixelated;
    image-rendering: crisp-edges;
}

/* Player sprite */
.player-sprite {
    width: 32px;
    height: 32px;
    background: linear-gradient(
        to bottom,
        #FFD700 0%, #FFD700 25%,      /* Cabelo amarelo */
        #FFCCAA 25%, #FFCCAA 45%,     /* Rosto */
        #FF0000 45%, #FF0000 70%,     /* Camisa vermelha */
        #3366FF 70%, #3366FF 100%     /* Calça azul */
    );
    border-radius: 50% 50% 0 0;
    position: relative;
}

/* Pikachu sprite (segue o jogador) */
.pikachu-sprite {
    width: 24px;
    height: 24px;
    background: #FFD700;
    border-radius: 50%;
    position: relative;
}
.pikachu-sprite::before {
    content: '';
    position: absolute;
    top: -8px;
    left: 2px;
    width: 8px;
    height: 12px;
    background: #FFD700;
    border-radius: 50% 50% 0 0;
    transform: rotate(-15deg);
}
.pikachu-sprite::after {
    content: '';
    position: absolute;
    top: -8px;
    right: 2px;
    width: 8px;
    height: 12px;
    background: #FFD700;
    border-radius: 50% 50% 0 0;
    transform: rotate(15deg);
}

/* Portrait boxes melhorados */
.portrait-oak {
    background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
    border: 3px solid #FFD700;
}

.portrait-blue {
    background: linear-gradient(135deg, #4169E1 0%, #1E90FF 100%);
    border: 3px solid #FF6347;
}

.portrait-pikachu {
    background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
    border: 3px solid #FF0000;
}

/* Tiles melhorados */
.tile-grass {
    background: linear-gradient(45deg, #228B22 25%, #32CD32 50%, #228B22 75%);
}

.tile-building {
    background: linear-gradient(to bottom, #8B4513 0%, #A0522D 50%, #8B4513 100%);
    border: 2px solid #5D3A1A;
}

.tile-water {
    background: linear-gradient(45deg, #1E90FF 25%, #00BFFF 50%, #1E90FF 75%);
    animation: water-flow 2s ease-in-out infinite;
}

@keyframes water-flow {
    0%, 100% { background-position: 0 0; }
    50% { background-position: 10px 10px; }
}
```

### 2.2 Melhorar Renderização do Mapa

**Onde:** Substituir função `drawMap()` no JavaScript:

```javascript
function drawMap() {
    const scene = scenes[gameState.currentScene];
    const mapKey = scene.map || 'pallet_town';
    const map = maps[mapKey] || maps['pallet_town'];
    const tileSize = Math.floor(canvas.width / 24); // Responsive tile size

    for (let y = 0; y < map.length; y++) {
        for (let x = 0; x < map[y].length; x++) {
            const char = map[y][x];
            const px = x * tileSize;
            const py = y * tileSize + 60; // Offset for UI

            if (char === '#') {
                // Building tile with gradient
                const gradient = ctx.createLinearGradient(px, py, px, py + tileSize);
                gradient.addColorStop(0, '#8B4513');
                gradient.addColorStop(0.5, '#A0522D');
                gradient.addColorStop(1, '#8B4513');
                ctx.fillStyle = gradient;
                ctx.fillRect(px, py, tileSize, tileSize);
                ctx.strokeStyle = '#5D3A1A';
                ctx.lineWidth = 2;
                ctx.strokeRect(px, py, tileSize, tileSize);
            } else if (char === '.') {
                // Grass tile with pattern
                ctx.fillStyle = '#228B22';
                ctx.fillRect(px, py, tileSize, tileSize);
                // Add grass detail
                ctx.fillStyle = '#32CD32';
                ctx.fillRect(px + 2, py + 2, 4, 4);
                ctx.fillRect(px + tileSize - 6, py + tileSize - 6, 4, 4);
            } else if (char === '~') {
                // Water tile
                const gradient = ctx.createLinearGradient(px, py, px + tileSize, py + tileSize);
                gradient.addColorStop(0, '#1E90FF');
                gradient.addColorStop(0.5, '#00BFFF');
                gradient.addColorStop(1, '#1E90FF');
                ctx.fillStyle = gradient;
                ctx.fillRect(px, py, tileSize, tileSize);
            } else if (char === 'T') {
                // Tree
                ctx.fillStyle = '#228B22';
                ctx.fillRect(px, py, tileSize, tileSize);
                ctx.fillStyle = '#006400';
                ctx.beginPath();
                ctx.arc(px + tileSize/2, py + tileSize/3, tileSize/3, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#8B4513';
                ctx.fillRect(px + tileSize/2 - 3, py + tileSize/2, 6, tileSize/2);
            } else {
                // Default grass
                ctx.fillStyle = '#2d5016';
                ctx.fillRect(px, py, tileSize, tileSize);
            }
        }
    }
}
```

### 2.3 Melhorar Renderização do Player

**Onde:** Substituir função `drawPlayer()`:

```javascript
function drawPlayer() {
    const tileSize = Math.floor(canvas.width / 24);
    const px = gameState.playerX * tileSize;
    const py = gameState.playerY * tileSize + 60;

    // Sombra
    ctx.fillStyle = 'rgba(0,0,0,0.3)';
    ctx.beginPath();
    ctx.ellipse(px + tileSize/2, py + tileSize - 2, tileSize/3, tileSize/6, 0, 0, Math.PI * 2);
    ctx.fill();

    // Corpo (Red - protagonista)
    // Calça azul
    ctx.fillStyle = '#3366FF';
    ctx.fillRect(px + 4, py + tileSize/2 + 4, tileSize - 8, tileSize/2 - 6);
    
    // Camisa vermelha
    ctx.fillStyle = '#FF0000';
    ctx.fillRect(px + 2, py + tileSize/4, tileSize - 4, tileSize/3);
    
    // Cabeça
    ctx.fillStyle = '#FFCCAA';
    ctx.beginPath();
    ctx.arc(px + tileSize/2, py + tileSize/4, tileSize/4, 0, Math.PI * 2);
    ctx.fill();
    
    // Cabelo preto
    ctx.fillStyle = '#1a1a1a';
    ctx.beginPath();
    ctx.arc(px + tileSize/2, py + tileSize/5, tileSize/4, Math.PI, Math.PI * 2);
    ctx.fill();
    
    // Boné vermelho
    ctx.fillStyle = '#FF0000';
    ctx.fillRect(px + tileSize/4, py + 2, tileSize/2, tileSize/6);
    ctx.fillRect(px + tileSize/2 - 2, py, tileSize/3, tileSize/8);

    // Desenhar Pikachu seguindo (se tiver)
    if (gameState.hasPikachu) {
        drawPikachu(px - tileSize, py + 4);
    }
}

function drawPikachu(x, y) {
    const size = 20;
    
    // Corpo amarelo
    ctx.fillStyle = '#FFD700';
    ctx.beginPath();
    ctx.ellipse(x + size/2, y + size/2, size/2, size/2.5, 0, 0, Math.PI * 2);
    ctx.fill();
    
    // Orelhas
    ctx.beginPath();
    ctx.moveTo(x + 4, y + 4);
    ctx.lineTo(x + 2, y - 8);
    ctx.lineTo(x + 10, y + 2);
    ctx.fillStyle = '#FFD700';
    ctx.fill();
    
    ctx.beginPath();
    ctx.moveTo(x + size - 4, y + 4);
    ctx.lineTo(x + size - 2, y - 8);
    ctx.lineTo(x + size - 10, y + 2);
    ctx.fill();
    
    // Pontas pretas das orelhas
    ctx.fillStyle = '#1a1a1a';
    ctx.beginPath();
    ctx.moveTo(x + 2, y - 8);
    ctx.lineTo(x + 4, y - 4);
    ctx.lineTo(x + 6, y - 6);
    ctx.fill();
    
    ctx.beginPath();
    ctx.moveTo(x + size - 2, y - 8);
    ctx.lineTo(x + size - 4, y - 4);
    ctx.lineTo(x + size - 6, y - 6);
    ctx.fill();
    
    // Bochechas vermelhas
    ctx.fillStyle = '#FF6347';
    ctx.beginPath();
    ctx.arc(x + 4, y + size/2, 3, 0, Math.PI * 2);
    ctx.arc(x + size - 4, y + size/2, 3, 0, Math.PI * 2);
    ctx.fill();
    
    // Olhos
    ctx.fillStyle = '#1a1a1a';
    ctx.beginPath();
    ctx.arc(x + size/3, y + size/3, 2, 0, Math.PI * 2);
    ctx.arc(x + size*2/3, y + size/3, 2, 0, Math.PI * 2);
    ctx.fill();
}
```

### 2.4 Adicionar Estado do Pikachu

**Onde:** No objeto `gameState`, adicionar:

```javascript
const gameState = {
    currentScene: 'scene_oak_lab',
    playerX: 12,
    playerY: 3,
    dialogIndex: 0,
    isDialogActive: false,
    hasPikachu: false,  // ADICIONAR ESTA LINHA
    mapTiles: [],
    save: () => localStorage.setItem('pokemonGameState', JSON.stringify(gameState))
};
```

### 2.5 Ativar Pikachu após recebê-lo

**Onde:** Na cena 'scene_pikachu', no diálogo especial, adicionar lógica:

Modificar a função `showDialog()` para verificar texto especial:

```javascript
function showDialog(speaker, portrait, text, duration = null) {
    const dialogBox = document.getElementById('dialogBox');
    document.getElementById('dialogSpeaker').textContent = speaker;
    document.getElementById('dialogPortrait').textContent = portrait;
    document.getElementById('dialogText').textContent = text;
    dialogBox.classList.add('visible');
    gameState.isDialogActive = true;

    // Verificar eventos especiais
    if (text.includes('[Você recebe PIKACHU]')) {
        gameState.hasPikachu = true;
        gameState.save();
    }

    if (duration) {
        setTimeout(() => {
            dialogBox.classList.remove('visible');
            gameState.isDialogActive = false;
            gameState.dialogIndex++;
        }, duration);
    }
}
```

### 2.6 Melhorar Caixa de Diálogo

**Onde:** Substituir estilos do `.dialog-box`:

```css
.dialog-box {
    position: fixed;
    bottom: 100px;
    left: 10px;
    right: 10px;
    background: linear-gradient(180deg, #1a1a2e 0%, #0d0d1a 100%);
    border: 4px solid #FFD700;
    border-radius: 15px;
    padding: 15px;
    color: white;
    font-size: 16px;
    max-height: 180px;
    overflow-y: auto;
    z-index: 999;
    display: none;
    font-family: 'Courier New', monospace;
    line-height: 1.8;
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.3), inset 0 0 30px rgba(0,0,0,0.5);
}

.dialog-box.visible {
    display: block;
    animation: dialogAppear 0.3s ease-out;
}

@keyframes dialogAppear {
    from { 
        transform: translateY(50px) scale(0.9); 
        opacity: 0; 
    }
    to { 
        transform: translateY(0) scale(1); 
        opacity: 1; 
    }
}

.dialog-portrait {
    float: left;
    width: 64px;
    height: 64px;
    margin-right: 15px;
    background: linear-gradient(135deg, #2a2a4a 0%, #1a1a2e 100%);
    border: 3px solid #FFD700;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
}

.dialog-speaker {
    font-weight: bold;
    color: #FFD700;
    font-size: 18px;
    margin-bottom: 8px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

.dialog-text {
    font-size: 14px;
    color: #FFFFFF;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}
```

---

## SPRINT 3: SISTEMA DE BATALHA

### 3.1 Adicionar HTML do Battle Overlay

**Onde:** Após o `<div id="dialogBox">`, adicionar:

```html
<div id="battleOverlay" class="battle-overlay">
    <div class="battle-scene">
        <div class="opponent-side">
            <div class="pokemon-name" id="opponentName">Rattata</div>
            <div class="hp-bar-container">
                <div class="hp-bar" id="opponentHp"></div>
            </div>
            <div class="pokemon-sprite opponent" id="opponentSprite"></div>
        </div>
        <div class="player-side">
            <div class="pokemon-sprite player" id="playerPokemonSprite"></div>
            <div class="pokemon-name" id="playerPokemonName">Pikachu</div>
            <div class="hp-bar-container">
                <div class="hp-bar" id="playerPokemonHp"></div>
            </div>
        </div>
    </div>
    <div class="battle-menu" id="battleMenu">
        <div class="battle-text" id="battleText">O que Pikachu deve fazer?</div>
        <div class="battle-options">
            <button class="battle-btn" data-action="fight">⚔️ LUTAR</button>
            <button class="battle-btn" data-action="bag">🎒 BOLSA</button>
            <button class="battle-btn" data-action="pokemon">🔄 POKÉMON</button>
            <button class="battle-btn" data-action="run">🏃 FUGIR</button>
        </div>
    </div>
    <div class="attack-menu hidden" id="attackMenu">
        <button class="attack-btn" data-move="thundershock">⚡ Thunder Shock</button>
        <button class="attack-btn" data-move="quickattack">💨 Quick Attack</button>
        <button class="attack-btn" data-move="growl">📢 Growl</button>
        <button class="attack-btn" data-move="tailwhip">🔄 Tail Whip</button>
        <button class="back-btn" data-action="back">← Voltar</button>
    </div>
</div>
```

### 3.2 Adicionar CSS do Battle System

**Onde:** No `<style>`, adicionar:

```css
/* ==================== BATTLE SYSTEM ==================== */

.battle-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(180deg, #87CEEB 0%, #98FB98 60%, #228B22 100%);
    z-index: 2000;
    flex-direction: column;
}

.battle-overlay.active {
    display: flex;
}

.battle-scene {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    padding: 20px;
}

.opponent-side {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    padding-right: 20px;
}

.player-side {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding-left: 20px;
}

.pokemon-sprite {
    width: 96px;
    height: 96px;
    image-rendering: pixelated;
}

.pokemon-sprite.opponent {
    /* Rattata sprite via CSS */
    background: #9370DB;
    border-radius: 50% 50% 40% 40%;
    position: relative;
}
.pokemon-sprite.opponent::before {
    content: '';
    position: absolute;
    top: 10px;
    left: 15px;
    width: 20px;
    height: 30px;
    background: #9370DB;
    border-radius: 50% 50% 0 0;
    transform: rotate(-20deg);
}
.pokemon-sprite.opponent::after {
    content: '';
    position: absolute;
    top: 10px;
    right: 15px;
    width: 20px;
    height: 30px;
    background: #9370DB;
    border-radius: 50% 50% 0 0;
    transform: rotate(20deg);
}

.pokemon-sprite.player {
    /* Pikachu sprite via CSS */
    background: #FFD700;
    border-radius: 50%;
    position: relative;
}

.pokemon-name {
    font-family: 'Courier New', monospace;
    font-weight: bold;
    font-size: 18px;
    color: #1a1a1a;
    text-shadow: 1px 1px 0 white;
    margin: 5px 0;
}

.hp-bar-container {
    width: 150px;
    height: 12px;
    background: #333;
    border: 2px solid #FFD700;
    border-radius: 6px;
    overflow: hidden;
}

.hp-bar {
    height: 100%;
    background: linear-gradient(90deg, #00FF00 0%, #32CD32 100%);
    width: 100%;
    transition: width 0.5s ease-out;
}

.hp-bar.low {
    background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%);
}

.hp-bar.critical {
    background: linear-gradient(90deg, #FF0000 0%, #FF6347 100%);
    animation: hp-pulse 0.5s ease-in-out infinite;
}

@keyframes hp-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.battle-menu {
    background: linear-gradient(180deg, #1a1a2e 0%, #0d0d1a 100%);
    border-top: 4px solid #FFD700;
    padding: 15px;
    min-height: 180px;
}

.battle-text {
    color: white;
    font-family: 'Courier New', monospace;
    font-size: 16px;
    margin-bottom: 15px;
    min-height: 40px;
}

.battle-options {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}

.battle-btn, .attack-btn {
    padding: 15px;
    font-size: 16px;
    font-family: 'Courier New', monospace;
    font-weight: bold;
    background: linear-gradient(180deg, #4a4a6a 0%, #2a2a4a 100%);
    border: 3px solid #FFD700;
    border-radius: 10px;
    color: white;
    cursor: pointer;
    transition: all 0.2s;
}

.battle-btn:active, .attack-btn:active {
    transform: scale(0.95);
    background: linear-gradient(180deg, #6a6a8a 0%, #4a4a6a 100%);
}

.attack-menu {
    background: linear-gradient(180deg, #1a1a2e 0%, #0d0d1a 100%);
    border-top: 4px solid #FFD700;
    padding: 15px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.attack-menu.hidden {
    display: none;
}

.back-btn {
    background: linear-gradient(180deg, #8B0000 0%, #4a0000 100%);
    border-color: #FF6347;
}
```

### 3.3 Adicionar JavaScript do Battle System

**Onde:** Antes do `// Start game`, adicionar:

```javascript
// ==================== BATTLE SYSTEM ====================

const battleState = {
    active: false,
    turn: 'player',
    playerPokemon: {
        name: 'Pikachu',
        hp: 35,
        maxHp: 35,
        attack: 55,
        defense: 40,
        speed: 90,
        moves: [
            { name: 'Thunder Shock', power: 40, type: 'electric' },
            { name: 'Quick Attack', power: 40, type: 'normal', priority: true },
            { name: 'Growl', power: 0, type: 'normal', effect: 'lower_attack' },
            { name: 'Tail Whip', power: 0, type: 'normal', effect: 'lower_defense' }
        ]
    },
    opponent: null,
    textQueue: [],
    animating: false
};

const wildPokemon = {
    rattata: {
        name: 'Rattata',
        hp: 30,
        maxHp: 30,
        attack: 56,
        defense: 35,
        speed: 72,
        moves: [
            { name: 'Tackle', power: 40, type: 'normal' },
            { name: 'Tail Whip', power: 0, type: 'normal', effect: 'lower_defense' }
        ],
        catchRate: 255,
        expYield: 51
    },
    pidgey: {
        name: 'Pidgey',
        hp: 40,
        maxHp: 40,
        attack: 45,
        defense: 40,
        speed: 56,
        moves: [
            { name: 'Tackle', power: 40, type: 'normal' },
            { name: 'Sand Attack', power: 0, type: 'ground', effect: 'lower_accuracy' }
        ],
        catchRate: 255,
        expYield: 50
    }
};

function startBattle(pokemonKey) {
    battleState.active = true;
    battleState.opponent = JSON.parse(JSON.stringify(wildPokemon[pokemonKey]));
    battleState.turn = 'player';
    
    document.getElementById('battleOverlay').classList.add('active');
    document.getElementById('opponentName').textContent = battleState.opponent.name;
    updateHpBars();
    
    showBattleText(`Um ${battleState.opponent.name} selvagem apareceu!`);
}

function endBattle(victory) {
    battleState.active = false;
    document.getElementById('battleOverlay').classList.remove('active');
    
    if (victory) {
        const exp = battleState.opponent.expYield;
        showDialog('Sistema', '🎮', `Pikachu ganhou ${exp} pontos de experiência!`, 2000);
    }
}

function showBattleText(text, callback) {
    const textEl = document.getElementById('battleText');
    textEl.textContent = text;
    
    if (callback) {
        setTimeout(callback, 1500);
    }
}

function updateHpBars() {
    const playerHpPercent = (battleState.playerPokemon.hp / battleState.playerPokemon.maxHp) * 100;
    const opponentHpPercent = (battleState.opponent.hp / battleState.opponent.maxHp) * 100;
    
    const playerBar = document.getElementById('playerPokemonHp');
    const opponentBar = document.getElementById('opponentHp');
    
    playerBar.style.width = playerHpPercent + '%';
    opponentBar.style.width = opponentHpPercent + '%';
    
    // Update colors based on HP
    [playerBar, opponentBar].forEach((bar, i) => {
        const percent = i === 0 ? playerHpPercent : opponentHpPercent;
        bar.classList.remove('low', 'critical');
        if (percent <= 20) bar.classList.add('critical');
        else if (percent <= 50) bar.classList.add('low');
    });
}

function playerAttack(moveIndex) {
    if (battleState.animating) return;
    battleState.animating = true;
    
    const move = battleState.playerPokemon.moves[moveIndex];
    const damage = calculateDamage(battleState.playerPokemon, battleState.opponent, move);
    
    showBattleText(`Pikachu usou ${move.name}!`, () => {
        battleState.opponent.hp = Math.max(0, battleState.opponent.hp - damage);
        updateHpBars();
        
        if (damage > 0) {
            showBattleText(`Causou ${damage} de dano!`, () => {
                if (battleState.opponent.hp <= 0) {
                    showBattleText(`${battleState.opponent.name} desmaiou!`, () => {
                        endBattle(true);
                    });
                } else {
                    battleState.animating = false;
                    opponentTurn();
                }
            });
        } else {
            showBattleText(`${move.name} teve efeito!`, () => {
                battleState.animating = false;
                opponentTurn();
            });
        }
    });
}

function opponentTurn() {
    const opponent = battleState.opponent;
    const move = opponent.moves[Math.floor(Math.random() * opponent.moves.length)];
    const damage = calculateDamage(opponent, battleState.playerPokemon, move);
    
    showBattleText(`${opponent.name} usou ${move.name}!`, () => {
        battleState.playerPokemon.hp = Math.max(0, battleState.playerPokemon.hp - damage);
        updateHpBars();
        
        if (damage > 0) {
            showBattleText(`Causou ${damage} de dano!`, () => {
                if (battleState.playerPokemon.hp <= 0) {
                    showBattleText(`Pikachu desmaiou!`, () => {
                        endBattle(false);
                    });
                } else {
                    battleState.animating = false;
                    showBattleText('O que Pikachu deve fazer?');
                }
            });
        } else {
            battleState.animating = false;
            showBattleText('O que Pikachu deve fazer?');
        }
    });
}

function calculateDamage(attacker, defender, move) {
    if (move.power === 0) return 0;
    
    const baseDamage = ((2 * 5 / 5 + 2) * move.power * (attacker.attack / defender.defense)) / 50 + 2;
    const randomFactor = (Math.random() * 0.15) + 0.85;
    return Math.floor(baseDamage * randomFactor);
}

function tryToRun() {
    const escapeChance = (battleState.playerPokemon.speed / battleState.opponent.speed) * 0.5;
    
    if (Math.random() < escapeChance || Math.random() < 0.3) {
        showBattleText('Conseguiu fugir!', () => {
            endBattle(false);
        });
    } else {
        showBattleText('Não conseguiu fugir!', () => {
            opponentTurn();
        });
    }
}

// Event listeners para battle
document.querySelectorAll('.battle-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const action = btn.dataset.action;
        if (action === 'fight') {
            document.getElementById('battleMenu').style.display = 'none';
            document.getElementById('attackMenu').classList.remove('hidden');
        } else if (action === 'run') {
            tryToRun();
        }
    });
});

document.querySelectorAll('.attack-btn').forEach((btn, index) => {
    btn.addEventListener('click', () => {
        playerAttack(index);
        document.getElementById('attackMenu').classList.add('hidden');
        document.getElementById('battleMenu').style.display = 'block';
    });
});

document.querySelector('.back-btn').addEventListener('click', () => {
    document.getElementById('attackMenu').classList.add('hidden');
    document.getElementById('battleMenu').style.display = 'block';
});
```

### 3.4 Adicionar Trigger de Batalha em Route 1

**Onde:** Na função `update()`, após o código de warp zones, adicionar:

```javascript
// Random encounter em Route 1
if (gameState.currentScene === 'route1' && !battleState.active) {
    if (Math.random() < 0.02) { // 2% chance por frame de movimento
        const pokemon = Math.random() < 0.7 ? 'rattata' : 'pidgey';
        startBattle(pokemon);
    }
}
```

---

## SPRINT 4: NARRATIVA EXPANDIDA

### 4.1 Novos Mapas (Route 1 expandida, Viridian Forest)

**Onde:** No objeto `maps`, substituir/adicionar:

```javascript
const maps = {
    'pallet_town': [
        '........................',
        '.##########......########.',
        '.#........#......#......#.',
        '.#..PROF..#......#..MOM.#.',
        '.##########......########.',
        '............🌸............',
        '....🌸.......🌸....🌸.....',
        '.........................',
        '..........EXIT..........'
    ],
    'route1': [
        'TTTTTT......TTTTTTTTTTTT',
        'T....T......T..........T',
        'T....~~~~~~.T....🌿🌿..T',
        '....~~~~~~..........🌿..',
        '....~~~~~~....🌿🌿......',
        '~~~~~~......🌿🌿🌿🌿....',
        '..........🌿🌿....🌿🌿..',
        'T....🌿🌿........🌿....T',
        'TTTT................TTTT'
    ],
    'viridian_forest': [
        'TTTTTTTTTTTTTTTTTTTTTTTT',
        'T..🌿..T....T..🌿🌿....T',
        'T.🌿🌿.T....T.🌿🌿🌿...T',
        'T......T....T..........T',
        'T..TTTTTTTTTTTTTTTT....T',
        'T..T................T..T',
        'T..T..🌿🌿🌿🌿🌿🌿..T..T',
        'T.....🌿🌿🌿🌿🌿🌿.....T',
        'TTTTTTTTTT....TTTTTTTTTT'
    ],
    'viridian': [
        '........###########......',
        '......##...........##....',
        '....##...POKEMON....##...',
        '....##...CENTER.....##...',
        '..##.......##.........##.',
        '.#.........##..MART....#.',
        '#..........##..........#',
        '#......................#',
        '########################'
    ],
    'pewter': [
        '########################',
        '#........GYM...........#',
        '#.......#####..........#',
        '#.......#####..MUSEUM..#',
        '#....................###',
        '#....POKEMON.....##....#',
        '#....CENTER......##....#',
        '#....................###',
        '########################'
    ]
};
```

### 4.2 Diálogos Expandidos (Fidelidade ao Mangá)

**Onde:** No objeto `scenes`, expandir diálogos:

```javascript
const scenes = {
    'scene_oak_lab': {
        bg: '#2d5016',
        title: 'Laboratório do Prof. Oak',
        map: 'pallet_town',
        startPos: {x: 12, y: 4},
        dialogues: [
            { speaker: 'Oak', portrait: '🧙', text: 'Ah, você deve ser Red! Eu estava te esperando.' },
            { speaker: 'Oak', portrait: '🧙', text: 'Meu nome é Professor Oak. Estudo Pokémons há mais de 40 anos.' },
            { speaker: 'Oak', portrait: '🧙', text: 'Este mundo é habitado por criaturas chamadas Pokémon.' },
            { speaker: 'Oak', portrait: '🧙', text: 'Alguns os usam para batalhas. Outros, como companheiros.' },
            { speaker: 'Oak', portrait: '🧙', text: 'Mas há algo que você precisa entender, Red...' },
            { speaker: 'Oak', portrait: '🧙', text: 'Pokémons não são ferramentas. Eles sentem dor. Eles têm sonhos.' },
            { speaker: 'You', portrait: '👦', text: '...', duration: 600 },
            { speaker: 'Oak', portrait: '🧙', text: 'Vim te oferecer uma missão: completar esta Pokédex.' },
            { speaker: 'Oak', portrait: '🧙', text: 'Mas mais importante... entender o que significa ser um treinador.' },
            { speaker: '???', portrait: '👱', text: 'Hah! Que piada.' },
            { speaker: 'Blue', portrait: '👱', text: 'Vovô, você vai dar uma Pokédex pra esse moleque?' , next: 'scene_oak_lab_part2' }
        ]
    },
    'scene_oak_lab_part2': {
        bg: '#2d5016',
        title: 'Laboratório do Prof. Oak',
        map: 'pallet_town',
        startPos: {x: 12, y: 4},
        dialogues: [
            { speaker: 'Blue', portrait: '👱', text: 'Eu sou Blue! O melhor treinador de Pallet Town!' },
            { speaker: 'Blue', portrait: '👱', text: 'Vovô, me dê logo meu Pokémon. Não tenho tempo pra perder.' },
            { speaker: 'Oak', portrait: '🧙', text: 'Blue... paciência é uma virtude.' },
            { speaker: 'Blue', portrait: '👱', text: 'Tsc. Tanto faz.' },
            { speaker: 'Blue', portrait: '👱', text: '*Blue pega um Pokéball da mesa*' },
            { speaker: 'Blue', portrait: '👱', text: 'Este Eevee será meu. O mais raro de todos.' },
            { speaker: 'Oak', portrait: '🧙', text: 'Blue! Esse Pokémon não é para--' },
            { speaker: 'Blue', portrait: '👱', text: 'Nos vemos por aí, Red. Se você sobreviver.' },
            { speaker: 'Blue', portrait: '👱', text: '*Blue sai rindo*', duration: 800 },
            { speaker: 'Oak', portrait: '🧙', text: '...' },
            { speaker: 'Oak', portrait: '🧙', text: 'Red, venha comigo. Tenho algo especial para você.', next: 'scene_pikachu' }
        ]
    },
    'scene_pikachu': {
        bg: '#3a3a2e',
        title: 'Sala dos Fundos',
        map: 'pallet_town',
        startPos: {x: 12, y: 4},
        dialogues: [
            { speaker: 'Oak', portrait: '🧙', text: 'Este Pikachu... ele é diferente.' },
            { speaker: 'Oak', portrait: '🧙', text: 'Encontrei-o ferido na Viridian Forest há algumas semanas.' },
            { speaker: 'Oak', portrait: '🧙', text: 'Ele não confia em humanos. Foi maltratado antes.' },
            { speaker: 'Pikachu', portrait: '⚡', text: 'Pika... pikaaa...', duration: 500 },
            { speaker: 'Oak', portrait: '🧙', text: 'Veja... ele está com medo.' },
            { speaker: 'You', portrait: '👦', text: '*Red se ajoelha e estende a mão*', duration: 800 },
            { speaker: 'Pikachu', portrait: '⚡', text: '...Pika?', duration: 400 },
            { speaker: 'Oak', portrait: '🧙', text: 'Impressionante... ele não ataca você.' },
            { speaker: 'Oak', portrait: '🧙', text: 'Red, cuide bem dele. Ele precisa de alguém como você.' },
            { speaker: 'Oak', portrait: '🧙', text: '[Você recebe PIKACHU]', special: true, duration: 800 },
            { speaker: 'Pikachu', portrait: '⚡', text: 'Pika... pikachu!', duration: 500 },
            { speaker: 'Oak', portrait: '🧙', text: 'Agora vá. Sua jornada começa na Route 1.', next: 'route1' }
        ]
    },
    'route1': {
        bg: '#3d6b1f',
        title: 'Route 1',
        map: 'route1',
        startPos: {x: 12, y: 7},
        dialogues: [
            { speaker: 'Narrator', portrait: '📖', text: 'Route 1 - O primeiro passo de uma longa jornada.', duration: 1500 },
            { speaker: 'Narrator', portrait: '📖', text: 'Pokémons selvagens habitam a grama alta. Tenha cuidado.', duration: 1500 }
        ]
    },
    'viridian': {
        bg: '#2d5016',
        title: 'Viridian City',
        map: 'viridian',
        startPos: {x: 12, y: 7},
        dialogues: [
            { speaker: 'Narrator', portrait: '📖', text: 'Viridian City - A cidade eternamente verde.', duration: 1500 }
        ]
    }
};
```

---

## SPRINT 5: POLISH FINAL

### 5.1 Adicionar Efeitos Sonoros (Base64 inline)

**Onde:** No início do `<script>`, adicionar:

```javascript
// ==================== AUDIO SYSTEM ====================

const AudioManager = {
    context: null,
    sounds: {},
    
    init() {
        this.context = new (window.AudioContext || window.webkitAudioContext)();
    },
    
    // Gerar beep simples para efeitos
    playBeep(frequency = 440, duration = 0.1, type = 'square') {
        if (!this.context) this.init();
        
        const oscillator = this.context.createOscillator();
        const gainNode = this.context.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.context.destination);
        
        oscillator.frequency.value = frequency;
        oscillator.type = type;
        
        gainNode.gain.setValueAtTime(0.3, this.context.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.context.currentTime + duration);
        
        oscillator.start(this.context.currentTime);
        oscillator.stop(this.context.currentTime + duration);
    },
    
    // Sons específicos
    dialogAdvance() { this.playBeep(880, 0.05); },
    menuSelect() { this.playBeep(660, 0.08); },
    battleStart() { 
        this.playBeep(440, 0.1);
        setTimeout(() => this.playBeep(550, 0.1), 100);
        setTimeout(() => this.playBeep(660, 0.15), 200);
    },
    attack() { this.playBeep(220, 0.15, 'sawtooth'); },
    damage() { this.playBeep(110, 0.2, 'sawtooth'); },
    levelUp() {
        [440, 550, 660, 880].forEach((f, i) => {
            setTimeout(() => this.playBeep(f, 0.15), i * 100);
        });
    }
};

// Inicializar audio no primeiro toque
document.addEventListener('touchstart', () => AudioManager.init(), { once: true });
document.addEventListener('click', () => AudioManager.init(), { once: true });
```

### 5.2 Integrar Sons nos Eventos

**Onde:** Modificar funções existentes:

```javascript
// Em showDialog(), adicionar no início:
AudioManager.dialogAdvance();

// Em playerAttack(), após showBattleText do ataque:
AudioManager.attack();

// Em opponentTurn(), após causar dano:
AudioManager.damage();

// Em startBattle():
AudioManager.battleStart();

// Em grantExp() (se level up):
AudioManager.levelUp();
```

### 5.3 Adicionar Transições Suaves

**Onde:** No CSS, adicionar:

```css
/* Transições de cena */
.scene-transition {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #000;
    z-index: 3000;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease-in-out;
}

.scene-transition.active {
    opacity: 1;
    pointer-events: all;
}
```

**No HTML, adicionar após gameContainer:**
```html
<div class="scene-transition" id="sceneTransition"></div>
```

**No JS, criar função:**
```javascript
function transitionToScene(newScene, callback) {
    const transition = document.getElementById('sceneTransition');
    transition.classList.add('active');
    
    setTimeout(() => {
        if (callback) callback();
        setTimeout(() => {
            transition.classList.remove('active');
        }, 300);
    }, 300);
}
```

---

## ✅ CHECKLIST DE EXECUÇÃO

### Para o Haiku executar em ordem:

1. [ ] **Backup primeiro:** `cp index.html index.html.backup`
2. [ ] **Sprint 2.1-2.6:** Visual upgrade (CSS + JS de renderização)
3. [ ] **Testar:** Verificar se mapa e player renderizam bonitos
4. [ ] **Sprint 3.1-3.4:** Battle system (HTML + CSS + JS)
5. [ ] **Testar:** Andar em Route 1 e ver se batalha inicia
6. [ ] **Sprint 4.1-4.2:** Narrativa expandida (mapas + diálogos)
7. [ ] **Testar:** Verificar diálogos novos
8. [ ] **Sprint 5.1-5.3:** Polish (áudio + transições)
9. [ ] **Testar final:** Jogo completo

### Comandos úteis:

```bash
# Reiniciar servidor
cd /home/ubuntu/clawd/pokemon-game
pkill -f "http.server" && python3 -m http.server 8000 --bind 0.0.0.0 &

# Criar tunel público
npx localtunnel --port 8000

# Ver senha do tunel
curl https://loca.lt/mytunnelpassword
```

---

## 📝 NOTAS IMPORTANTES

1. **Não apagar código existente** - Sempre adicionar/modificar
2. **Testar após cada sprint** - Não acumular mudanças
3. **Fazer backup antes de edições grandes**
4. **Se algo quebrar, reverter:** `git checkout HEAD index.html`

---

*Plano criado por Opus em 2026-02-10. Pronto para execução por Haiku.*
