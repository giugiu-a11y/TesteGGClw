# Manga Audit Report (2026-02-11)

Escopo auditado: arco **Red/Green/Blue** de Pokemon Adventures vs implementacao atual em `story/season1.ptbr.json`.

## Metodo

Referencias externas usadas:
- Lista oficial de rounds do arco RGB (40 capitulos):  
  `https://bulbapedia.bulbagarden.net/wiki/List_of_Red/Green/Blue_rounds`
- Resumo do arco RGB (eventos importantes):  
  `https://bulbapedia.bulbagarden.net/wiki/Red%2C_Green%2C_and_Blue_chapter_%28Adventures%29`
- Detalhe de Volume 1 (eventos, party changes, gym battles):  
  `https://m.bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Special_volume_1`

Metrica aplicada:
1. **Cobertura estrita de capitulos (40)**: capitulo conta como coberto apenas quando o tema central aparece explicitamente em beat/cena.
2. **Cobertura de eventos-chave do arco** (6 itens da pagina RGB).
3. **Cobertura de itens estruturais do Vol.1**:
   - Additions de party (5 itens)
   - Gym battles listadas no Vol.1 (4 itens)

## Resultado objetivo

- Beats de historia no jogo: **39** (`ch1...ch27` + extensoes).
- Linhas de dialogo no script: **230**.

### 1) Cobertura estrita de capitulos RGB (40)
- Cobertos de forma explicita: **13/40 = 32.5%**
- Parcial/indireto: **10/40 = 25.0%**
- Nao coberto explicito: **17/40 = 42.5%**

Capitulos cobertos explicitamente (exemplos):
- 1 (Mew), 2 (Bulbasaur), 4 (Pikachu), 5 (Onix), 8 (Starmie), 11 (Electabuzz/Surge), 14 (Arbok), 21 (Nidoking), 27 (Kadabra/Saffron), 34-35 (Mewtwo), 40 (Charizard/Champion).

### 2) Eventos-chave do arco RGB (Bulbapedia)
- Cobertura: **6/6 = 100%**
  - Red encontra Blue
  - Oak entrega Pokedex
  - Bill ajuda com Storage
  - Red encontra Green
  - Trio derrota Team Rocket
  - Red derrota Blue e vira Champion

### 3) Estrutural Vol.1
- Party additions (Vol.1): **2/5 = 40%**  
  (Saur e Pika cobertos; Nidorino/Fearow/Snorlax ausentes explicitamente)
- Gym battles (Vol.1): **3/4 = 75%**  
  (Brock, Misty, Surge cobertos; Koga ausente no recorte atual)

## Veredito de fidelidade (auditoria quantitativa)

Pelo criterio estrito de contagem por capitulo/elemento canônico, a build atual **nao bate 75%**.

Estimativa consolidada (proxy ponderado: capitulos estritos + eventos-chave + estrutura Vol.1):
- **53.5%** de fidelidade quantitativa.

## Conclusao

- O jogo esta forte em fluxo narrativo adaptado e eventos macro.
- Em auditoria quantitativa “contando no manga”, ainda falta cobertura de varios capitulos especificos (principalmente os nao explicitados por beat tematico).
- Portanto, **nao e correto afirmar 75% garantido por contagem estrita neste estado**.

