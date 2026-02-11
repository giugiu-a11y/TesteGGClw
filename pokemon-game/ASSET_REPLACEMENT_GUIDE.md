# Asset Replacement Guide (Tiles + Sprites)

Este guia deixa tudo pronto para outra IA trocar arte sem mexer em logica.

## 1) Tileset (mapa/cenario)

Arquivos:
- `assets/tilesets/user.png`
- `assets/tilesets/user.tileset.json`

Ativar:
- `?tileset=external`

Modo remoto:
- `?tileset=remote&tilesetPng=<URL_PNG>&tilesetJson=<URL_JSON>`

## 2) Sprites (personagens + pokemons)

Arquivo:
- `assets/sprites/user.sprites.json`

Ativar:
- `?sprites=external`

Obs: atualmente este modo ja e o comportamento padrao do jogo.

Modo remoto:
- `?sprites=remote&spritesJson=<URL_JSON>`

## 3) Usar ambos juntos

- Local:
  - `?tileset=external&sprites=external&reset=1`
- Remoto:
  - `?tileset=remote&tilesetPng=<URL_PNG>&tilesetJson=<URL_JSON>&sprites=remote&spritesJson=<URL_JSON>&reset=1`

## 4) Validacao obrigatoria

```bash
cd /home/ubuntu/clawd/pokemon-game
python3 -m json.tool assets/tilesets/user.tileset.json >/dev/null
python3 -m json.tool assets/sprites/user.sprites.json >/dev/null
awk 'BEGIN{p=0} /<script>/{p=1;next} /<\/script>/{p=0} p{print}' index.html > /tmp/pokemon_game_script.js
node --check /tmp/pokemon_game_script.js
```

## 5) Publicar

```bash
cd /home/ubuntu/clawd
git add pokemon-game/assets/tilesets/user.png \
        pokemon-game/assets/tilesets/user.tileset.json \
        pokemon-game/assets/sprites/user.sprites.json \
        pokemon-game/index.html \
        pokemon-game/assets/tilesets/README.md \
        pokemon-game/assets/sprites/README.md \
        pokemon-game/ASSET_REPLACEMENT_GUIDE.md
git commit -m "Asset pipeline: complete external tiles+sprites mapping"
git push origin main
```
