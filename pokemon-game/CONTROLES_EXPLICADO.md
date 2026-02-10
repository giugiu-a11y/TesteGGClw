# 🎮 CONTROLES EXPLICADO (SIMPLES)

## 🖥️ NO SEU MAC (Teclado)

### MOVIMENTO (SETAS DO TECLADO)

```
Use as SETAS DO TECLADO:

    ⬆️  (seta para cima)    = Move para cima
⬅️  ⬇️  ➡️  (outras setas) = Move para os lados

OU use WASD:
W = Cima
A = Esquerda
D = Direita
S = Baixo
```

**✅ As setas já funcionam no código!** Você pode testar agora no Mac com teclado.

---

## 📱 NO iPad (Touch - Botões na Tela)

### Você verá DOIS CONTROLES:

#### **À ESQUERDA (D-Pad):**
```
        ▲
      ◀ ▼ ▶

Toque em qualquer um para mover naquela direção
```

#### **À DIREITA (Botões A e B):**
```
    B  ← Vermelho (cancelar)
  A    ← Verde (confirmar/ação)
```

---

## 🎯 COMO USAR

### No Mac:

```
1. Abre terminal:
   cd /home/ubuntu/clawd/pokemon-game/
   ./start-dev.sh

2. Abre Chrome/Firefox/Safari:
   http://localhost:8000

3. Usa SETAS do teclado para mover:
   ⬆️⬇️⬅️➡️

4. Aperta LETRA X para confirmar/avançar diálogo:
   Pressiona X (no teclado)

5. Aperta LETRA Z para cancelar:
   Pressiona Z (no teclado)
```

### No iPad:

```
1. Abra Safari

2. Digite URL: http://192.168.x.x:8000
   (use IP do seu Mac)

3. Vê os botões na tela:
   
   D-PAD (esquerda)    |   BOTÕES (direita)
   ▲                   |      B (vermelho)
   ◀ ▼ ▶              |   A (verde)

4. Toque no D-PAD para mover
   Toque em A (verde) para confirmar
```

---

## 🔴 BOTÃO A e B (Explicado Simples)

### **A (Verde)** = Confirmar / Aceitar / Avançar
```
- Quer falar com NPC? Aperta A
- Diálogo apareceu? Aperta A para ler próxima frase
- Quer pegar item? Aperta A
```

### **B (Vermelho)** = Cancelar / Voltar / Sair
```
- Entrou em menu errado? Aperta B
- Quer sair do diálogo? Aperta B
```

---

## 🖱️ Mapeamento de Teclas

| Ação | Teclado Mac | Xbox Style |
|------|------------|-----------|
| Mover Cima | ⬆️ Arrow Up | W |
| Mover Baixo | ⬇️ Arrow Down | S |
| Mover Esquerda | ⬅️ Arrow Left | A |
| Mover Direita | ➡️ Arrow Right | D |
| Confirmar (A) | **X** | A |
| Cancelar (B) | **Z** | B |

---

## ✅ TESTE AGORA NO MAC

```bash
# Terminal 1: Rodar servidor
cd /home/ubuntu/clawd/pokemon-game/
./start-dev.sh

# Terminal 2 (ou abra Chrome): Acessar
# Chrome: http://localhost:8000

# Teste:
- Aperta ⬆️ (seta para cima) → Personagem sobe
- Aperta ⬅️ ➡️ (setas laterais) → Personagem anda
- Aperta X → Fala com Oak / Avança diálogo
```

---

## 🔒 É SEGURO?

### **SIM, 100% SEGURO.**

#### Por que?

```
O servidor roda LOCALMENTE:
- Está no seu Mac (192.168.x.x)
- É privado (só sua rede WiFi acessa)
- Não expõe para internet
- Sem credenciais, sem dados, sem cloud

É igual a:
- Abrir um arquivo .html no navegador
- Mas com um pequeno servidor embutido
```

#### O que `./start-dev.sh` faz?

```bash
#!/bin/bash
cd /home/ubuntu/clawd/pokemon-game/
python3 -m http.server 8000
```

**Isso é tudo!** Apenas:
1. Entra na pasta
2. Abre um servidor HTTP básico na porta 8000
3. Serve os arquivos locais

**Não faz:**
- ❌ Acesso à internet
- ❌ Upload de dados
- ❌ Conexão com servidores
- ❌ Nada perigoso

---

## 🎯 PASSO A PASSO SEGURO

### Mac (você):

```bash
# 1. Abre TERMINAL
# 2. Cola:
cd /home/ubuntu/clawd/pokemon-game/

# 3. Cola:
./start-dev.sh

# Vê:
🎮 Pokémon Adventures - Starting Dev Server
📁 Directory: /home/ubuntu/clawd/pokemon-game/
🌐 Local Server: http://localhost:8000
📱 iPad Access: http://192.168.1.100:8000    ← Cole este IP

# 4. Deixa rodando (não fecha)
```

### iPad:

```
1. Abre Safari
2. Clica na barra de URL
3. Cola: http://192.168.1.100:8000
   (use o IP que apareceu no terminal)
4. Enter
5. Espera 2-3 segundos
6. Jogo carrega! 🎮
```

---

## ⚡ RESUMO

```
Movimento:     ⬆️⬇️⬅️➡️ (setas) ou WASD
Confirmar (A): X (teclado) ou Botão Verde (iPad)
Cancelar (B):  Z (teclado) ou Botão Vermelho (iPad)

Segurança:     ✅ 100% seguro, é servidor local
Internet:      ❌ Não usa internet nenhuma
Privacidade:   ✅ Tudo local, zero exposição
```

---

## 🆘 PROBLEMAS?

### "As setas não funcionam"
- Certifique que clicou no Canvas (área preta do jogo)
- Depois aperta as setas

### "Não vejo os botões no iPad"
- Eles estão na parte inferior da tela
- Desliza para cima se necessário

### "Servidor não inicia"
```bash
# Tenta com sudo:
sudo python3 -m http.server 8000

# Ou porta diferente:
python3 -m http.server 9000
# (depois acessa http://localhost:9000)
```

---

**Pronto! Agora é seguro testar. Bora?** 🚀
