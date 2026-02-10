# 🎮 Pokémon Adventures Game

**Pokémon Adventures manga adaptation para navegador (iPad + Desktop)**

> **Status**: Sprint 0 ✅ Completo
> **Tamanho**: ~17KB (será ~600KB ao final com assets)
> **Plataforma**: iPad Safari, Chrome, Firefox
> **Linguagem**: JavaScript vanilla + HTML5 Canvas

---

## 🚀 START DEV SERVER

### No seu Mac/Linux:

```bash
cd /home/ubuntu/clawd/pokemon-game/
./start-dev.sh
```

**Saída esperada**:
```
🎮 Pokémon Adventures - Starting Dev Server
==========================================

📁 Directory: /home/ubuntu/clawd/pokemon-game/
🌐 Local Server: http://localhost:8000
📱 iPad Access: http://192.168.x.x:8000

Open your iPad Safari and go to: http://192.168.x.x:8000

Press Ctrl+C to stop
```

### No seu iPad:

1. Abra **Safari**
2. Digite na barra de URL: `http://192.168.x.x:8000`
   (substitua `x.x` pelo IP mostrado no terminal)
3. **Enter** → Jogo carrega instantaneamente

---

## 🎮 CONTROLES

### **Teclado (Desktop)**:
- ⬆️⬇️⬅️➡️ = Movimento (WASD ou Setas)
- **X** = Confirmar / Avançar diálogo
- **Z** = Cancelar

### **iPad (Touch)**:
- **D-Pad** (esquerda) = Movimento
- **Botão Verde (A)** = Confirmar
- **Botão Vermelho (B)** = Cancelar

---

## 📂 ESTRUTURA

```
pokemon-game/
├── index.html           # Jogo completo (arquivo único)
├── start-dev.sh         # Script para rodar server
├── README.md            # Este arquivo
├── FINAL_SPECS.md       # Especificações finais
├── PROJECT_STRUCTURE.md # Estrutura do projeto
│
├── src/                 # Código fonte (desenvolvimento)
│   ├── main.js         # (será separado depois)
│   ├── scenes.js
│   └── ...
│
├── assets/              # Recursos (PNG, JSON)
│   ├── sprites/        # Personagens e Pokémons
│   ├── tilesets/       # Mapas/mundos
│   ├── portraits/      # Retratos NPCs
│   └── data/           # JSON (diálogos, mapas)
│
└── build/               # Output final (HTML único)
    └── index.html       # Arquivo final de deploy
```

---

## 📋 O QUE ESTÁ FUNCIONANDO AGORA (SPRINT 0)

✅ **Game Loop** 60fps  
✅ **Canvas Rendering** básico  
✅ **Input Handler** (teclado + touch)  
✅ **D-Pad Virtual** responsivo  
✅ **Diálogos** (cena do laboratório)  
✅ **Mapa** visual de Pallet Town  
✅ **Personagem** (você)  
✅ **Seta discreta** mostrando direção  
✅ **Save/Load** localStorage  

---

## 📖 PRÓXIMAS FASES

### **Sprint 1** (Dias 2-3):
- Mais diálogos (Oak, Blue, Poliwag)
- Transições de cenas
- Mais mapas (Route 1, Viridian)

### **Sprint 2** (Dias 4-5):
- Sistema de batalha simplificado
- Encontro com Pokémon selvagem
- Captura básica

### **Sprint 3** (Dias 6-10):
- Integração de sprites reais
- Mais cidades
- Mais eventos narrativos

### **Sprint 4** (Dias 11-12):
- Polish final
- Otimização
- Deploy

---

## 🎨 CUSTOMIZAÇÕES

### Adicionar Novo Diálogo

Edite `scenes` no `index.html`:

```javascript
const scenes = {
    'scene_oak_lab': {
        dialogues: [
            { speaker: 'Oak', portrait: '🧙', text: 'Seu texto aqui' },
            // ... mais diálogos
        ]
    }
};
```

### Adicionar Nova Cena

```javascript
const scenes = {
    'scene_route1': {
        bg: '#2d5016',
        title: 'Route 1',
        dialogues: [
            { speaker: 'You', portrait: '👦', text: 'Que grama estranha...' }
        ]
    }
};
```

---

## 🐛 TROUBLESHOOTING

### "Não consigo acessar do iPad"

1. Certifique-se que Mac e iPad estão no **MESMO WiFi**
2. Pegue o IP correto:
   ```bash
   hostname -I
   ```
3. Use exatamente: `http://SEU-IP:8000`

### "Diálogos não avançam"

Clique no botão **Verde (A)** para avançar.

### "Personagem fica preso"

Mapa é pequeno (teste). Será expandido nas próximas sprints.

---

## 📊 FILE SIZE ATUAL

```
index.html: 17KB (teste)
Final target: ~600KB (com sprites/diálogos completos)
Load time: <1 segundo iPad 4G
```

---

## 🔄 WORKFLOW DIÁRIO

```bash
# 1. Editar código
vim index.html

# 2. Recarregar no iPad
# (Safari: Refresh / Swipe down)

# 3. Testar + reportar bugs

# 4. Commit
git add .
git commit -m "feat: [descrição]"
git push
```

---

## 🚀 DEPLOY FINAL

```bash
# Quando pronto:
./tools/build.sh

# Gera: build/index.html (~600KB, pronto)

# Deploy GitHub Pages:
git push origin main
# Auto-publica em: https://seu-usuario.github.io/pokemon-game/
```

---

## 📞 NOTAS

- **Desenvolvido em**: AWS EC2 (Ubuntu 22.04)
- **Testado em**: Safari iPad + Chrome Desktop
- **Compatível**: iOS 14+, Android 8+
- **Sem dependências**: Pure JavaScript, sem frameworks

---

## ✅ PRÓXIMO PASSO

```bash
# Inicia server:
./start-dev.sh

# Abra no iPad:
http://SEU-IP:8000

# Interaja:
- Use D-Pad para mover
- Aperte A (verde) para falar com Oak
- Avance os diálogos

# Reporta feedback! 🎮
```

---

**Criado**: 2026-02-10  
**Sprint**: 0 (Framework)  
**Status**: ✅ Pronto para testar
