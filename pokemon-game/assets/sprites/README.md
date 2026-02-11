# Sprites (Plugavel)

Este projeto aceita override completo de sprites (personagens + pokemons) por JSON.

## Arquivos locais

- `assets/sprites/user.sprites.json` (ativo quando `?sprites=external`)
- `assets/sprites/user.sprites.example.json` (modelo)

## Formato

```json
{
  "sprites": {
    "red": "https://...png",
    "pikachuBattle": "https://...png"
  }
}
```

Voce pode colocar:
- apenas as chaves que quer trocar (override parcial), ou
- todas as chaves para controle total.

## Como ativar

1. Override local:
- `?sprites=external`

2. Override remoto:
- `?sprites=remote&spritesJson=https://.../user.sprites.json`

3. Com tiles ao mesmo tempo:
- `?tileset=external&sprites=external`
- `?tileset=remote&tilesetPng=...&tilesetJson=...&sprites=remote&spritesJson=...`

## Chaves suportadas

`red`, `blue`, `brock`, `oak`, `mom`, `girl`, `green`, `pikachuOW`, `pikachuBattle`, `pikachuBack`, `rattata`, `pidgey`, `staryu`, `poliwhirl`, `poliwhirlBack`, `poliwrath`, `poliwrathBack`, `bulbasaur`, `bulbasaurBack`, `ivysaur`, `venusaur`, `snorlax`, `gyarados`, `charmander`, `charmeleon`, `charizard`, `squirtle`, `wartortle`, `mew`, `kangaskhan`, `nidoking`, `koffing`, `ekans`, `arbok`, `geodude`, `onix`, `generalTiles`, `buildingTiles`

