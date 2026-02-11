# COORDINATION (2 IAs)

## Fonte de Verdade
- Estado atual: `STATUS.md`
- Proximos passos: `NEXT.md`
- Historia: `story/season1.ptbr.json`

## Ownership por Area
- IA A (engine): input, dialog, batalha, warp, save/load.
- IA B (content/visual): mapas, tileset mapping, story beats/dialogos.
- Se uma IA mexer na area da outra, registrar no commit e atualizar `STATUS.md`.

## Regras Anti-Retrabalho
1. Nao duplicar gatilho de historia em dois lugares.
   - Regra: gatilhos ficam em `onMapEnter()` + beats JSON.
2. Nao editar `index.html` inteiro de uma vez.
   - Fazer patches pequenos por bloco (mapa, input, batalha, story).
3. Sempre testar sintaxe antes de commit:
   - `node --check` no script extraido de `index.html`
   - `python3 -m json.tool` nos JSON alterados
4. Nao commitar lixo de ambiente (`sessions/**`, `__pycache__`, venv).

## Contrato de Qualidade
- iPad first: toque precisa avancar dialogo e batalha.
- Manga first: jogador so confirma; sistema executa a acao.
- Visual: estilo consistente (nao parecer prototipo cru).
