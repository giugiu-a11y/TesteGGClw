# 🎨 Assets Inventory - Pokémon Game

**Total:** 138 arquivos PNG | **Tamanho:** 8.5MB | **Data:** 2026-02-11

## Organização por Categoria

### 🏠 Houses (Casas) - 9 arquivos
Variações de casas, telhados, portas e estruturas externas.

| Asset ID | Descrição | Tamanho |
|----------|-----------|---------|
| 3849 | Construções gerais | 40KB |
| 3850 | Telhados variados | 374KB |
| 3851 | Portas | 16KB |
| 3852-3859 | Tipos de casas variadas | 184KB |

**Uso:** Mapas de cidades, casas principais, estruturas habitacionais

---

### ⚔️ Battles (Batalhas) - 5 arquivos
Backgrounds e arenas de batalha.

| Asset ID | Descrição | Tamanho |
|----------|-----------|---------|
| 3860-3862 | Battle backgrounds | 309KB |
| 3871 | Arena de batalha | 263KB |
| 3872 | Background batalha | 120KB |

**Uso:** Telas de batalha, transições, efeitos visuais

---

### 🛣️ Routes (Rotas) - 5 arquivos
Terrenos variados, água, grama, caminhos.

| Asset ID | Descrição | Tamanho |
|----------|-----------|---------|
| 3863 | Terreno ao ar livre | 107KB |
| 3864 | Variações de grama | 111KB |
| 3865 | Tiles de água | 18KB |
| 3866-3869 | Terrenos variados | 291KB |

**Uso:** Mapas de rotas, terrenos externos, paisagens

---

### 🏙️ Cities (Cidades) - 4 arquivos
Mapas de cidades prontos.

| Asset ID | Descrição | Tamanho |
|----------|-----------|---------|
| 3873 | Pallet Town | 30KB |
| 3874 | Viridian City | 8KB |
| 3875 | Pewter City | 41KB |
| 3876-3879 | Outras cidades | 166KB |

**Uso:** Mapas pré-prontos de cidades, layout de ruas

---

### 👤 Characters (Personagens) - 35 arquivos
Sprites de personagens e movimento do protagonista.

| Asset ID | Descrição | Tamanho |
|----------|-----------|---------|
| 3880 | Protagonista masculino | 22KB |
| 3881 | Protagonista feminino | 15KB |
| 3882 | NPCs variados | 1.1MB |
| 3936-3950 | Walk cycles (movimento) | 293KB |
| 3951-3970 | Mais NPCs e variações | 460KB |

**Uso:** Personagens jogáveis, NPCs, diálogos, movimentação

---

### 🎮 Pokémon (Criaturas) - 35 arquivos
Sprites de Pokémons em diferentes estados.

| Asset ID | Descrição | Tamanho |
|----------|-----------|---------|
| 3900 | Frente | 8KB |
| 3901 | Costas | 5KB |
| 3902 | Ícones | 114KB |
| 3903-3920 | Sprites variados (frente) | 660KB |
| 3921-3935 | Sprites variados (costas) | 510KB |

**Uso:** Pokédex, battle sprites, overworld encounters

---

### 🎬 Animated (Animações) - 8 arquivos
Tiles animados e efeitos.

| Asset ID | Descrição | Tamanho |
|----------|-----------|---------|
| 3971-3978 | Tiles animados (água, flores) | 196KB |

**Uso:** Água animada, flores que tremem, efeitos visuais

---

### 🔧 Objects (Objetos) - 10 arquivos
Estruturas, objetos e itens.

| Asset ID | Descrição | Tamanho |
|----------|-----------|---------|
| 3991-4000 | Estruturas e objetos | 310KB |

**Uso:** Móveis, itens, decoração de ambientes

---

## Tileset Geral (Base)

**Asset 3870 - General Tileset** (159KB)
- GRASS, GRASS_ALT, TALL_GRASS, FLOWER
- PATH, PATH_ALT, WATER, TREE
- FENCE, SIGN, ROOF variants
- WALL, DOOR, WINDOW, WARP
- FLOOR_IN, WALL_IN, TABLE, SHELF

---

## Como Usar

1. **Para tiles:** Use os JSON mappings em `user.tileset.json` ou crie novos
2. **Para sprites:** Referencie os asset IDs nos componentes React
3. **Para rotas pré-prontas:** Use os mapas de cidades como base

## Próximos Passos

- [ ] Testar renderização em jogo
- [ ] Ajustar tile indices conforme necessário
- [ ] Criar JSON mappings adicionais para builds específicas
- [ ] Otimizar carregamento (lazy loading, atlas merging)

