# Asset Runtime Contract

Objetivo: garantir que o jogo rode igual em AWS local e GitHub Pages, sem regressão visual.

## Fontes oficiais de runtime
- Tileset base (obrigatório): `assets/tilesets/user.png` + `assets/tilesets/user.tileset.json`
- Sprites runtime: `assets/sprites/user.sprites.json`
- Map backgrounds por mapa: `assets/tilesets/mapbg.manifest.json`
- Scene/cutscene backdrops por beat: `assets/tilesets/scene_backdrop.manifest.json`

## Regras de compatibilidade
- Use caminhos relativos começando em `./assets/...` (compatível com Pages e servidor local).
- Não usar links absolutos locais (ex.: `/home/ubuntu/...`) em manifests.
- Não depender de fallback procedural para visual principal.
- Cada mapa jogável deve ter entrada em `mapbg.manifest.json`.

## Pastas de referência visual principal
- `assets/tilesets/cities/`
- `assets/tilesets/manual_environmental/`
- `assets/tilesets/characters/`
- `assets/tilesets/pokemon_sprites/`
- `assets/tilesets/trainers/`
- `assets/tilesets/battle_terrain/`

## Validação obrigatória
Execute:

```bash
cd /home/ubuntu/clawd/pokemon-game
bash ci-check.sh
```

`ci-check.sh` roda:
- validação JSON
- sintaxe JS de `index.html`
- `tools/asset_preflight.py` (consistência de manifests e referências)

