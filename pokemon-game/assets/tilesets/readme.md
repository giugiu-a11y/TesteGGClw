# Tilesets (Plugavel)

Este projeto suporta 2 modos:

1. **Procedural (default)**: tiles gerados no codigo (seguro, sem dependencias externas).
2. **Externo (plugavel)**: voce coloca um PNG + um JSON de mapeamento aqui, e ativa via querystring.

## Como usar tileset externo

1. Coloque:
- `assets/tilesets/user.png`
- `assets/tilesets/user.tileset.json`

2. Abra o jogo com:
- `?tileset=external`

## Pack CC0 (OpenGameArt) incluido

Este repo ja inclui um pack CC0 em:
- `assets/tilesets/punyworld.png`
- `assets/tilesets/punyworld.tileset.json`
- `assets/tilesets/user.png` + `assets/tilesets/user.tileset.json` (preconfigurados e completos com o mesmo mapeamento do `punyworld`)

Ative com:
- `?tileset=external`

## Formato do JSON

O arquivo `user.tileset.json` deve ter:
- `tileSize`: 16
- `atlasCols`: numero de colunas no atlas
- `map`: um objeto que mapeia `tileKey` -> `{ "ax": <col>, "ay": <row> }`

Exemplo de `tileKey`:
- `"GRASS"`, `"PATH"`, `"WATER"`, `"TALL_GRASS"`, `"TREE"`
- `"FENCE"`, `"SIGN"`, `"FLOWER"`, `"WARP"`
- `"FLOOR_IN"`, `"WALL_IN"`, `"TABLE"`, `"SHELF"`

## Com sprites juntos (pokemon/personagens)

O jogo tambem aceita override de sprites por JSON:
- `assets/sprites/user.sprites.json`
- ativar com `?sprites=external`

Exemplo completo:
- `?tileset=external&sprites=external&reset=1`
