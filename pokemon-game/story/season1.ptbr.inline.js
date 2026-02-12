// Auto-generated from season1.ptbr.json for offline/cache-robust startup.
window.__POKEMON_STORY__ = {
  "meta": {
    "season": 1,
    "language": "pt-BR",
    "fidelity_target": 1.0,
    "sources": [
      {
        "id": "manga_vol1_scribd",
        "label": "Pokemon Adventures Vol 01 (Scribd)",
        "url": "https://pt.scribd.com/document/496161531/Pokemon-Adventures-Vol-01"
      },
      {
        "id": "tiles_spriters_resource",
        "label": "The Spriters Resource (FRLG)",
        "url": "https://www.spriters-resource.com/gba/pokemonfireredleafgreen/"
      },
      {
        "id": "tiles_spriters_resource_general_3870",
        "label": "Tileset Geral (asset 3870)",
        "url": "https://www.spriters-resource.com/game_boy_advance/pokemonfireredleafgreen/asset/3870/"
      },
      {
        "id": "assets_yepoleb_repo",
        "label": "Yepoleb/Pokemon-assets",
        "url": "https://github.com/Yepoleb/Pokemon-assets"
      }
    ],
    "notes": [
      "Objetivo: fidelidade maxima de roteiro para o arco RGB (adaptacao cena-a-cena para formato web interativo).",
      "Cada beat deve ter sourceRef (capitulo/pagina/edicao/scan) para revisao.",
      "Texto no jogo deve ser preferencialmente uma adaptacao fiel; texto 100% literal depende de voce fornecer o transcript/trechos exatos (copyright)."
    ]
  },
  "beats": [
    {
      "id": "ch1_intro",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ POKeMON ADVENTURES ]",
            "[ Chapter 1: VS MEW ]",
            "━━━━━━━━━━━━━━━━━━━━━━"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "PALLET TOWN - Uma pequena cidade na regiao de KANTO.",
            "Aqui vive um garoto que vive se gabando de ser um grande treinador...",
            "O nome dele e RED."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Heh! Olha so!",
            "Eu vou ser o maior treinador de POKeMON de PALLET TOWN!",
            "Eu e meu parceiro POLI somos imparaveis!"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ RED ja tem o POLI, um Poliwhirl que ele criou desde pequeno. ]",
            "[ Mas as outras criancas nao acreditam nas suas bravatas... ]"
          ]
        },
        {
          "kind": "face",
          "dir": "right"
        },
        {
          "kind": "teleport",
          "map": "pallet_town",
          "x": 6,
          "y": 8,
          "dir": "right"
        },
        {
          "kind": "move",
          "path": [
            "up",
            "up",
            "up",
            "right",
            "right",
            "right"
          ],
          "stepMs": 135
        },
        {
          "kind": "dialog",
          "speaker": "Morador",
          "lines": [
            "La vem o RED de novo contando vantagem...",
            "Mas quando aperta, ele e mais corajoso do que parece."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "Crianca",
          "lines": [
            "Se voce e tao bom, prova!",
            "Nao vale inventar desculpa depois!"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "???",
          "lines": [
            "Ah e? Entao prova!",
            "Voce fala, fala... mas ninguem nunca te viu lutar de verdade!"
          ]
        },
        {
          "kind": "pause",
          "ms": 240
        },
        {
          "kind": "face",
          "dir": "up"
        },
        {
          "kind": "move",
          "path": [
            "left",
            "left",
            "up",
            "up"
          ],
          "stepMs": 135
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Tch! Ta bom! Eu vou mostrar!",
            "Eu vou capturar o POKeMON mais raro de todos!",
            "...Huh? Que luz e essa na floresta?!"
          ]
        },
        {
          "kind": "teleport",
          "map": "viridian_forest",
          "x": 10,
          "y": 13,
          "dir": "up"
        },
        {
          "kind": "pause",
          "ms": 260
        },
        {
          "kind": "move",
          "path": [
            "up",
            "up",
            "up"
          ],
          "stepMs": 135
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ Uma luz brilhante atravessa as arvores! ]",
            "[ Um POKeMON rosa misterioso flutua diante de voce! ]",
            "[ Pequeno... com um olhar curioso e inocente... ]"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "O-O que e isso?! Eu nunca vi nada assim!",
            "Essa e a minha chance! POLI, vamos capturar!",
            "Vai, POKe BALL!"
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "MEW",
            "spr": "mew",
            "lv": 12,
            "hp": 36,
            "maxHp": 36
          },
          "options": {
            "scripted": true,
            "scriptSteps": [
              {
                "type": "log",
                "text": "Um MEW misterioso apareceu!"
              },
              {
                "type": "playerMove",
                "move": "Poke Ball",
                "damage": 0
              },
              {
                "type": "log",
                "text": "MEW desviou da Poke Ball com um brilho de barreira!"
              },
              {
                "type": "enemyMove",
                "move": "Teleport",
                "damage": 0
              },
              {
                "type": "log",
                "text": "MEW desapareceu no ar!"
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "pause",
          "ms": 320
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ RED arremessa uma POKe BALL! ]",
            "[ ...Mas MEW cria uma barreira e desvia! ]",
            "[ MEW inclina a cabeca... e desaparece! ]"
          ]
        },
        {
          "kind": "set",
          "path": "story.sawMew",
          "value": true
        },
        {
          "kind": "set",
          "path": "story.beat",
          "value": "ch1_oak_mew_explain"
        },
        {
          "kind": "ensureTeam",
          "value": [
            "poli"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "E... escapou! Mas o que ERA aquilo?!",
            "Nem o POLI conseguiu acompanhar...",
            "O Professor OAK estuda POKeMON raros. Ele deve saber!"
          ]
        },
        {
          "kind": "teleport",
          "map": "oak_lab",
          "x": 5,
          "y": 9,
          "dir": "up"
        }
      ]
    },
    {
      "id": "ch1_oak_mew_explain",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "teleport",
          "map": "oak_lab",
          "x": 5,
          "y": 9,
          "dir": "up"
        },
        {
          "kind": "pause",
          "ms": 280
        },
        {
          "kind": "dialog",
          "speaker": "Prof. Oak",
          "lines": [
            "RED! Entre, rapido!",
            "Voce viu algo na floresta, nao viu?",
            "Aquele brilho rosa... eu vi tambem, da janela!"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "Prof. Oak",
          "lines": [
            "Aquilo era o MEW... um POKeMON lendario!",
            "Dizem que ele carrega o DNA de todos os POKeMON do mundo.",
            "Passei anos pesquisando, mas ele sempre escapa..."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "MEW?! Entao era isso!",
            "Eu tentei capturar com o POLI... mas sumiu!"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "Prof. Oak",
          "lines": [
            "Entao voce ja tem um POLIWHIRL... impressionante.",
            "Voce criou ele sozinho? Voce tem talento, RED.",
            "Eu quero que voce me ajude na minha pesquisa."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ Prof. Oak hands you a red device! ]"
          ]
        },
        {
          "kind": "set",
          "path": "story.gotPokedex",
          "value": true
        },
        {
          "kind": "dialog",
          "speaker": "Prof. Oak",
          "lines": [
            "Isto e a POKeDEX!",
            "Ela registra dados automaticamente quando voce encontra POKeMON.",
            "E eu tenho mais um presente pra voce..."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ Prof. Oak tosses a POKe BALL! ]",
            "[ A green POKeMON with a bulb on its back appears! ]"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "Prof. Oak",
          "lines": [
            "Este e um BULBASAUR. Eu chamo ele de SAUR.",
            "Tipo Grama/Veneno... uma boa combinacao pro seu jeito de lutar.",
            "Com o POLI, voces vao formar um time excelente."
          ]
        },
        {
          "kind": "set",
          "path": "story.gotSaur",
          "value": true
        },
        {
          "kind": "ensureTeam",
          "value": [
            "poli",
            "saur"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "BULBASAUR",
          "lines": [
            "Bulba!"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ SAUR olha para voce com calma. ]",
            "[ BULBASAUR entrou no seu time! ]"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Um BULBASAUR?! Incrivel!",
            "SAUR! Voce e o POLI vao me ajudar a encontrar o MEW!"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "Prof. Oak",
          "lines": [
            "Tome cuidado, RED...",
            "Um grupo criminoso chamado TEAM ROCKET tambem esta atras do MEW.",
            "Eles vao fazer qualquer coisa para captura-lo.",
            "Meu neto BLUE ja seguiu para o norte. Fique atento.",
            "Agora va. Sua aventura comeca."
          ]
        },
        {
          "kind": "teleport",
          "map": "viridian",
          "x": 10,
          "y": 15,
          "dir": "up"
        },
        {
          "kind": "pause",
          "ms": 260
        },
        {
          "kind": "move",
          "path": [
            "up",
            "up",
            "up"
          ],
          "stepMs": 135
        }
      ]
    },
    {
      "id": "ch1_viridian_arrival",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "teleport",
          "map": "viridian",
          "x": 9,
          "y": 16,
          "dir": "up"
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ VIRIDIAN CITY ]",
            "A cidade parece calma... mas ha tensao no ar.",
            "RED sente que a jornada acabou de comecar de verdade."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Nao vou perder tempo aqui.",
            "Se o MEW passou por KANTO, eu vou seguir qualquer pista."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ Ao norte, a floresta fica cada vez mais densa... ]"
          ]
        },
        {
          "kind": "move",
          "path": [
            "up",
            "up",
            "up"
          ],
          "stepMs": 130
        },
        {
          "kind": "pause",
          "ms": 220
        },
        {
          "kind": "teleport",
          "map": "viridian_forest",
          "x": 4,
          "y": 15,
          "dir": "up"
        }
      ]
    },
    {
      "id": "ch1_viridian_forest_first",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "teleport",
          "map": "viridian_forest",
          "x": 4,
          "y": 15,
          "dir": "up"
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ VIRIDIAN FOREST ]",
            "A grama alta se move, como se o lugar estivesse vivo.",
            "POLI e SAUR ficam em guarda."
          ]
        },
        {
          "kind": "move",
          "path": [
            "up",
            "up",
            "right",
            "up",
            "left"
          ],
          "stepMs": 135
        },
        {
          "kind": "pause",
          "ms": 240
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ RED avanca por trilhas apertadas entre arvores densas. ]",
            "[ Galhos quebrados e marcas no chao indicam movimentacao recente. ]"
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "PIDGEY",
            "spr": "pidgey",
            "lv": 4,
            "hp": 18,
            "maxHp": 18
          },
          "options": {
            "scripted": true,
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "Um PIDGEY selvagem apareceu!"
              },
              {
                "type": "playerMove",
                "move": "Water Gun",
                "damage": 7
              },
              {
                "type": "enemyMove",
                "move": "Tackle",
                "damage": 3
              },
              {
                "type": "playerMove",
                "move": "Water Gun",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "pause",
          "ms": 300
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "O silencio volta por um instante...",
            "Mas a floresta ainda observa."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Isso nao foi um encontro comum.",
            "Alguem esta conduzindo essa pressao na floresta."
          ]
        },
        {
          "kind": "set",
          "path": "story.forestBattleDone",
          "value": true
        },
        {
          "kind": "teleport",
          "map": "pewter",
          "x": 10,
          "y": 15,
          "dir": "up"
        }
      ]
    },
    {
      "id": "ch1_pewter_arrival",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "teleport",
          "map": "pewter",
          "x": 10,
          "y": 15,
          "dir": "up"
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ PEWTER CITY ]",
            "Rocha, poeira... e um silencio estranho.",
            "Rumores sobre ataques a POKeMON circulam pelas ruas."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "TEAM ROCKET...",
            "Se eles estao mesmo aqui, eu vou derrubar um por um."
          ]
        },
        {
          "kind": "move",
          "path": [
            "left",
            "left",
            "up",
            "up"
          ],
          "stepMs": 135
        },
        {
          "kind": "pause",
          "ms": 220
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ Um membro da TEAM ROCKET surge em um beco. ]",
            "[ Um PIKACHU ferido tenta fugir do cativeiro. ]"
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "EKANS",
            "spr": "ekans",
            "lv": 7,
            "hp": 24,
            "maxHp": 24
          },
          "options": {
            "scripted": true,
            "trainerName": "Rocket",
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "ROCKET GRUNT enviou EKANS!"
              },
              {
                "type": "enemyMove",
                "move": "Wrap",
                "damage": 5
              },
              {
                "type": "playerMove",
                "move": "Bubble Beam",
                "damage": 11
              },
              {
                "type": "enemyMove",
                "move": "Poison Sting",
                "damage": 4
              },
              {
                "type": "playerMove",
                "move": "Water Gun",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "pause",
          "ms": 320
        },
        {
          "kind": "dialog",
          "speaker": "PIKACHU",
          "lines": [
            "Pika... pika!"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Calma. Agora voce esta seguro.",
            "Se quiser, pode vir comigo."
          ]
        },
        {
          "kind": "set",
          "path": "story.pewterHook",
          "value": true
        },
        {
          "kind": "set",
          "path": "story.caughtPika",
          "value": true
        },
        {
          "kind": "ensureTeam",
          "value": [
            "poli",
            "saur",
            "pika"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ PIKACHU entrou para o time! ]"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ RED segue para o PEWTER GYM para enfrentar BROCK. ]"
          ]
        },
        {
          "kind": "set",
          "path": "story.autoBrock",
          "value": true
        },
        {
          "kind": "teleport",
          "map": "pewter_gym",
          "x": 5,
          "y": 7,
          "dir": "up"
        }
      ]
    },
    {
      "id": "ch1_brock_intro",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "face",
          "dir": "up"
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ Arena de PEWTER GYM ]",
            "As pedras do ginasio amplificam cada passo.",
            "BROCK cruza os bracos e mede RED em silencio."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "Brock",
          "lines": [
            "Entao e voce, RED.",
            "Ouvi que protegeu um PIKACHU da TEAM ROCKET.",
            "Coragem sem tecnica nao basta. Mostre seu nivel."
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "GEODUDE",
            "spr": "geodude",
            "lv": 10,
            "hp": 32,
            "maxHp": 32
          },
          "options": {
            "scripted": true,
            "trainerName": "Brock",
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "BROCK enviou GEODUDE!"
              },
              {
                "type": "enemyMove",
                "move": "Tackle",
                "damage": 4
              },
              {
                "type": "playerMove",
                "move": "Water Gun",
                "damage": 15
              },
              {
                "type": "enemyMove",
                "move": "Rock Throw",
                "damage": 5
              },
              {
                "type": "playerMove",
                "move": "Bubble Beam",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "dialog",
          "speaker": "Brock",
          "lines": [
            "Bom controle.",
            "Seu estilo e agressivo, mas seus POKeMON confiam em voce.",
            "Nao vou te parar aqui. Continue avancando em KANTO."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Valeu, BROCK.",
            "Nao vou desperdiçar essa chance."
          ]
        },
        {
          "kind": "set",
          "path": "story.brockBattleDone",
          "value": true
        },
        {
          "kind": "set",
          "path": "story.autoBrock",
          "value": false
        },
        {
          "kind": "teleport",
          "map": "pewter",
          "x": 9,
          "y": 7,
          "dir": "down"
        }
      ]
    },
    {
      "id": "ch2_depart_pewter",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ RED deixa PEWTER em direcao ao leste. ]",
            "As montanhas ficam mais altas e o ar mais frio."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "MEW... TEAM ROCKET... tudo parece conectado.",
            "Nao posso parar agora."
          ]
        },
        {
          "kind": "teleport",
          "map": "route3",
          "x": 3,
          "y": 8,
          "dir": "right"
        },
        {
          "kind": "move",
          "path": [
            "right",
            "right",
            "right"
          ],
          "stepMs": 120
        },
        {
          "kind": "set",
          "path": "story.block_02_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch2_mtmoon_entry",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ MT. MOON ]",
            "Um tunel escuro se abre diante de RED.",
            "Eco de passos... e de problemas."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ Trilhos antigos, postes quebrados e poeira fresca no caminho. ]",
            "[ RED percebe que nao e o unico circulando ali dentro. ]"
          ]
        },
        {
          "kind": "set",
          "path": "story.block_03_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch2_green_first_contact",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "???",
          "lines": [
            "Voce e lento, RED.",
            "Se ficar moscando, vao roubar ate sua POKeDEX."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ Uma garota agil some nas sombras com um sorriso provocador. ]"
          ]
        },
        {
          "kind": "set",
          "path": "story.metGreen",
          "value": true
        },
        {
          "kind": "set",
          "path": "story.block_04_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch2_rocket_grunt_cave",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "Rocket",
          "lines": [
            "Garoto intrometido.",
            "Essa caverna e territorio da TEAM ROCKET."
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "RATTATA",
            "spr": "rattata",
            "lv": 9,
            "hp": 28,
            "maxHp": 28
          },
          "options": {
            "scripted": true,
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "ROCKET GRUNT enviou RATTATA!"
              },
              {
                "type": "enemyMove",
                "move": "Quick Attack",
                "damage": 5
              },
              {
                "type": "playerMove",
                "move": "Bubble Beam",
                "damage": 13
              },
              {
                "type": "enemyMove",
                "move": "Bite",
                "damage": 4
              },
              {
                "type": "playerMove",
                "move": "Water Gun",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "set",
          "path": "story.block_05_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch2_fossil_rumor",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ RED encontra pesquisadores discutindo fosseis raros. ]",
            "TEAM ROCKET tambem esta atras deles."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Nao vou deixar eles usarem isso pra machucar POKeMON."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_06_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch3_cerulean_arrival",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ CERULEAN CITY ]",
            "A cidade da agua parece tranquila por fora.",
            "Mas os conflitos em KANTO so aumentam."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "Moradora",
          "lines": [
            "Ultimamente todo mundo aqui fala de invasao e roubo de dados.",
            "Nem CERULEAN ficou fora dessa guerra."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Entao e aqui que mais um rastro comeca.",
            "Nao da pra perder tempo."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_07_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch3_misty_clash",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "Misty",
          "lines": [
            "Se vai correr por KANTO fazendo bagunca, primeiro me prove seu valor.",
            "No meu ginasio, agua nao perdoa."
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "STARYU",
            "spr": "staryu",
            "lv": 11,
            "hp": 30,
            "maxHp": 30
          },
          "options": {
            "scripted": true,
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "MISTY enviou STARYU!"
              },
              {
                "type": "enemyMove",
                "move": "Water Gun",
                "damage": 6
              },
              {
                "type": "playerMove",
                "move": "Double Slap",
                "damage": 10
              },
              {
                "type": "enemyMove",
                "move": "Swift",
                "damage": 4
              },
              {
                "type": "playerMove",
                "move": "Bubble Beam",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "set",
          "path": "story.block_08_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch3_bill_event",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "Bill",
          "lines": [
            "RED! Preciso de ajuda com um experimento de transferencia!",
            "Se der errado, posso ficar preso num corpo de POKeMON!"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ RED ajuda BILL e recebe informacoes valiosas sobre a TEAM ROCKET. ]"
          ]
        },
        {
          "kind": "set",
          "path": "story.block_09_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch4_vermilion_setup",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ VERMILION CITY ]",
            "Um porto movimentado e boatos sobre navios suspeitos."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ RED atravessa o cais observando cargas lacradas e guardas tensos. ]",
            "[ O nome S.S. ANNE aparece em varias rotas confiscadas. ]"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Se a ROCKET esta transportando algo, vai ser por aqui."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_10_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch4_ssanne_rocket",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ S.S. ANNE ]",
            "A tripulacao entra em panico com uma operacao clandestina."
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "ARBOK",
            "spr": "arbok",
            "lv": 15,
            "hp": 44,
            "maxHp": 44
          },
          "options": {
            "scripted": true,
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "EXECUTIVO ROCKET enviou ARBOK!"
              },
              {
                "type": "enemyMove",
                "move": "Poison Fang",
                "damage": 7
              },
              {
                "type": "playerMove",
                "move": "Hypnosis",
                "damage": 0
              },
              {
                "type": "playerMove",
                "move": "Bubble Beam",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "set",
          "path": "story.block_11_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch5_surge_pressure",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "Lt. Surge",
          "lines": [
            "Sem disciplina voce nao sobrevive em guerra.",
            "Treinador bom responde sob pressao."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Entao vamos ver quem aguenta mais."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_12_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch6_lavender_shadow",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ LAVENDER TOWN ]",
            "A cidade carrega um silencio pesado.",
            "Algo muito errado esta ligado a torre."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ Corredores internos ecoam passos e lamentos distantes. ]",
            "[ RED sobe lance por lance sem baixar a guarda. ]"
          ]
        },
        {
          "kind": "set",
          "path": "story.block_13_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch7_silph_infiltration",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ SILPH CO. ]",
            "A TEAM ROCKET assume o controle do predio."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Nao importa quantos andares tenham.",
            "Vou subir um por um."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_14_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch8_saffron_psychic",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ SAFFRON CITY ]",
            "O conflito chega ao centro de KANTO.",
            "Forca mental contra forca bruta."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_15_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch9_final_island_setup",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ ILHAS / LABORATORIO ]",
            "Os planos da ROCKET chegam na fase final.",
            "Mewtwo e o destino de KANTO se cruzam."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_16_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch10_mewtwo_confront",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Nao importa o quao forte voce seja...",
            "Eu nao vou abandonar meus POKeMON."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ O confronto final com MEWTWO se aproxima. ]"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ O impacto dessa batalha atravessa KANTO inteiro. ]",
            "[ Laboratorios entram em alerta e rotas sao evacuadas. ]"
          ]
        },
        {
          "kind": "set",
          "path": "story.block_17_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch11_aftershock_recovery",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ POS-CRISE ]",
            "KANTO ainda sente o impacto dos eventos em SAFFRON.",
            "RED segue sem pausa para fechar as pendencias da TEAM ROCKET."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Ainda nao acabou.",
            "Se eles se reorganizarem, tudo comeca de novo."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_18_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch12_cinnabar_research",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ CINNABAR ISLAND ]",
            "Documentos queimados e laboratorios vazios deixam rastros de experimentos proibidos."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ RED encontra relatorios incompletos, capsulas quebradas e codigos de acesso apagados. ]",
            "[ A assinatura da TEAM ROCKET aparece em multiplos setores. ]"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Eles estavam mexendo com coisas que nunca deveriam ter tocado."
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "NIDOKING",
            "spr": "nidoking",
            "lv": 24,
            "hp": 72,
            "maxHp": 72
          },
          "options": {
            "scripted": true,
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "CIENTISTA CORROMPIDO enviou NIDOKING!"
              },
              {
                "type": "enemyMove",
                "move": "Thrash",
                "damage": 9
              },
              {
                "type": "playerMove",
                "move": "Hypnosis",
                "damage": 0
              },
              {
                "type": "playerMove",
                "move": "Bubble Beam",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "set",
          "path": "story.block_19_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch13_viridian_giovanni",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "Giovanni",
          "lines": [
            "Voce avancou longe, RED.",
            "Mas nao entende o tabuleiro inteiro."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "Giovanni",
          "lines": [
            "Forca sem controle e desperdicio.",
            "Eu uso POKeMON como vetor de ordem, nao como mascotes de ego."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Ordem sem respeito e so tirania.",
            "Nao vou aceitar esse jogo."
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "ONIX",
            "spr": "onix",
            "lv": 28,
            "hp": 90,
            "maxHp": 90
          },
          "options": {
            "scripted": true,
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "GIOVANNI enviou ONIX!"
              },
              {
                "type": "enemyMove",
                "move": "Rock Tomb",
                "damage": 10
              },
              {
                "type": "playerMove",
                "move": "Water Gun",
                "damage": 24
              },
              {
                "type": "enemyMove",
                "move": "Dig",
                "damage": 8
              },
              {
                "type": "playerMove",
                "move": "Bubble Beam",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Acabou pra voce em KANTO.",
            "Nao vou deixar sua sombra voltar."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_20_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch14_indigo_opening",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ INDIGO PLATEAU ]",
            "A Liga reune os treinadores mais fortes de KANTO.",
            "RED entra carregando tudo o que viveu ate aqui."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_21_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch15_elite_lance",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "Lance",
          "lines": [
            "Nao e so sobre vencer.",
            "E sobre proteger o equilibrio entre humanos e POKeMON."
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "GYARADOS",
            "spr": "gyarados",
            "lv": 32,
            "hp": 104,
            "maxHp": 104
          },
          "options": {
            "scripted": true,
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "LANCE enviou GYARADOS!"
              },
              {
                "type": "enemyMove",
                "move": "Hydro Pump",
                "damage": 11
              },
              {
                "type": "playerMove",
                "move": "Body Slam",
                "damage": 14
              },
              {
                "type": "enemyMove",
                "move": "Dragon Rage",
                "damage": 10
              },
              {
                "type": "playerMove",
                "move": "Bubble Beam",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "set",
          "path": "story.block_22_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch16_blue_champion",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "Blue",
          "lines": [
            "Demorou pra chegar, RED.",
            "Mas eu sabia que voce nao ia desistir."
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "CHARIZARD",
            "spr": "charizard",
            "lv": 36,
            "hp": 118,
            "maxHp": 118
          },
          "options": {
            "scripted": true,
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "BLUE enviou CHARIZARD!"
              },
              {
                "type": "enemyMove",
                "move": "Flamethrower",
                "damage": 12
              },
              {
                "type": "playerMove",
                "move": "Hypnosis",
                "damage": 0
              },
              {
                "type": "playerMove",
                "move": "Bubble Beam",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "dialog",
          "speaker": "Blue",
          "lines": [
            "...Heh. Dessa vez foi seu dia.",
            "Nao se acostuma, RED."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_23_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch17_season1_epilogue",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ EPILOGO - TEMPORADA 1 ]",
            "RED encerra a primeira grande fase da jornada em KANTO.",
            "Mas o mundo dos POKeMON continua em movimento."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Ainda tem muito pra fazer.",
            "E eu vou continuar seguindo em frente."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_24_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch18_oak_debrief",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "Prof. Oak",
          "lines": [
            "RED, BLUE e GREEN...",
            "vocês tres mudaram o rumo de KANTO.",
            "Mas isso tambem atraiu novos inimigos."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Se vierem atras da gente, a gente responde.",
            "Nao vou recuar agora."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_25_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch19_green_reveal",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "Green",
          "lines": [
            "Eu roubei, menti e fingi varias vezes...",
            "mas era o jeito que eu tinha pra sobreviver.",
            "Agora eu escolho o meu proprio lado."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "Blue",
          "lines": [
            "Heh. Finalmente falando serio, Green?"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "Green",
          "lines": [
            "Nao se acostuma, arrogante."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_26_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch20_lance_warning",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "Lance",
          "lines": [
            "A ameaca nao terminou com uma unica batalha.",
            "KANTO ainda tem focos de violencia e controle ilegal de POKeMON."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Entao a gente limpa o resto.",
            "Sem deixar ninguem pra tras."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_27_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch21_rocket_remnant",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ REMANESCENTES DA TEAM ROCKET ]",
            "Um ultimo nucleo tenta recuperar pesquisa e armamento."
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "ARBOK",
            "spr": "arbok",
            "lv": 38,
            "hp": 124,
            "maxHp": 124
          },
          "options": {
            "scripted": true,
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "COMANDANTE ROCKET enviou ARBOK!"
              },
              {
                "type": "enemyMove",
                "move": "Poison Tail",
                "damage": 11
              },
              {
                "type": "playerMove",
                "move": "Hypnosis",
                "damage": 0
              },
              {
                "type": "playerMove",
                "move": "Bubble Beam",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "set",
          "path": "story.block_28_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch22_red_blue_duel",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "Blue",
          "lines": [
            "Vamos encerrar do jeito certo, RED.",
            "Sem interrupcao, sem caos externo. So nos dois."
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "CHARIZARD",
            "spr": "charizard",
            "lv": 40,
            "hp": 132,
            "maxHp": 132
          },
          "options": {
            "scripted": true,
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "BLUE enviou CHARIZARD!"
              },
              {
                "type": "enemyMove",
                "move": "Wing Attack",
                "damage": 12
              },
              {
                "type": "playerMove",
                "move": "Body Slam",
                "damage": 16
              },
              {
                "type": "enemyMove",
                "move": "Flamethrower",
                "damage": 13
              },
              {
                "type": "playerMove",
                "move": "Bubble Beam",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "dialog",
          "speaker": "Blue",
          "lines": [
            "...Boa luta.",
            "Da proxima vez, eu devolvo."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_29_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch23_team_unity",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ RED, BLUE e GREEN fecham o arco como trio ]",
            "As diferencas continuam, mas a confianca nasce no campo de batalha."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "Green",
          "lines": [
            "Nao precisa virar amizade melosa.",
            "So nao atrapalha e ja ta bom."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_30_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch24_mew_trace",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ SINAL DE MEW ]",
            "Um novo padrao de energia aparece e desaparece no mapa de KANTO."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Entao voce ainda esta por ai...",
            "Eu vou te encontrar de novo, MEW."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_31_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch25_training_push",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "Prof. Oak",
          "lines": [
            "Forca sem controle e so risco.",
            "Treinem com objetivo, nao com ego."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ O time de RED entra num novo ciclo de treino tecnico. ]"
          ]
        },
        {
          "kind": "dialog",
          "speaker": "SAUR",
          "lines": [
            "Bulba... SAUR!"
          ]
        },
        {
          "kind": "evolve",
          "slot": "saur",
          "to": "IVYSAUR",
          "options": {
            "name": "SAUR",
            "lv": 18,
            "maxHpBoost": 8
          }
        },
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "SAUR evoluiu para IVYSAUR!"
          ]
        },
        {
          "kind": "set",
          "path": "story.block_32_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch26_kanto_peace",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ KANTO RESPIRA ]",
            "As cidades voltam a rotina e os POKeMON deixam de viver em estado de guerra."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Paz de verdade da trabalho pra manter.",
            "E eu to pronto pra esse trabalho."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_33_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch27_season1_closure",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ FIM DA TEMPORADA 1 ]",
            "Arco RGB encerrado em modo jogavel completo.",
            "Proxima etapa: Gold/Silver/Crystal arc."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_34_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch28_vs_nidorino",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ ROUND EXTRA ]",
            "RED revisita os primeiros confrontos que moldaram seu estilo de batalha."
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "NIDOKING",
            "spr": "nidoking",
            "lv": 32,
            "hp": 102,
            "maxHp": 102
          },
          "options": {
            "scripted": true,
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "NIDORINO evoluido (NIDOKING) desafia RED!"
              },
              {
                "type": "enemyMove",
                "move": "Horn Attack",
                "damage": 10
              },
              {
                "type": "playerMove",
                "move": "Bubble Beam",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "set",
          "path": "story.block_35_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch29_vs_fearow",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ ROUND EXTRA ]",
            "Um FEAROW mergulha em alta velocidade, repetindo o caos dos primeiros arcos."
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "PIDGEY",
            "spr": "pidgey",
            "lv": 28,
            "hp": 92,
            "maxHp": 92
          },
          "options": {
            "scripted": true,
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "FEAROW (proxy visual) ataca pelo ceu!"
              },
              {
                "type": "enemyMove",
                "move": "Drill Peck",
                "damage": 9
              },
              {
                "type": "playerMove",
                "move": "Body Slam",
                "damage": 14
              },
              {
                "type": "playerMove",
                "move": "Bubble Beam",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "set",
          "path": "story.block_36_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch30_vs_snorlax",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ ROUND EXTRA ]",
            "O caminho e bloqueado por um SNORLAX agressivo e exausto."
          ]
        },
        {
          "kind": "battle",
          "enemy": {
            "name": "SNORLAX",
            "spr": "snorlax",
            "lv": 30,
            "hp": 120,
            "maxHp": 120
          },
          "options": {
            "scripted": true,
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "SNORLAX bloqueia a rota!"
              },
              {
                "type": "enemyMove",
                "move": "Body Slam",
                "damage": 11
              },
              {
                "type": "playerMove",
                "move": "Hypnosis",
                "damage": 0
              },
              {
                "type": "playerMove",
                "move": "Bubble Beam",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "set",
          "path": "story.block_37_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch31_vs_exeggutor",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ ROUND EXTRA ]",
            "Um EXEGGUTOR fora de controle surge durante uma evacuacao local."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Sem ferir civis. Controle primeiro, forca depois."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_38_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch32_vs_gyarados",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "battle",
          "enemy": {
            "name": "GYARADOS",
            "spr": "gyarados",
            "lv": 34,
            "hp": 110,
            "maxHp": 110
          },
          "options": {
            "scripted": true,
            "onEnd": "only_if_win",
            "scriptSteps": [
              {
                "type": "log",
                "text": "GYARADOS entra em furia no litoral!"
              },
              {
                "type": "enemyMove",
                "move": "Hydro Pump",
                "damage": 12
              },
              {
                "type": "playerMove",
                "move": "Body Slam",
                "damage": 16
              },
              {
                "type": "playerMove",
                "move": "Bubble Beam",
                "damage": 999
              },
              {
                "type": "end",
                "won": true
              }
            ]
          }
        },
        {
          "kind": "set",
          "path": "story.block_39_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch33_vs_porygon",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ ROUND EXTRA ]",
            "A equipe intercepta um incidente digital envolvendo PORYGON e dados da Silph."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "Green",
          "lines": [
            "Entrar em sistema fechado e meu tipo de trabalho.",
            "Segura o lado de fora que eu cuido da brecha."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_40_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch34_vs_hitmonlee",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ ROUND EXTRA ]",
            "No dojo de SAFFRON, um HITMONLEE testa reflexos e controle tecnico de RED."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_41_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch35_vs_hypno",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ ROUND EXTRA ]",
            "HYPNO manipula civis em transe para abrir passagem da Rocket."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "RED",
          "lines": [
            "Sem atacar pessoas controladas.",
            "A gente desmonta isso com precisao."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_42_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch36_vs_gengar",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ ROUND EXTRA ]",
            "GENGAR surge entre sombras para cobrir retirada da operacao inimiga."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_43_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch37_vs_alakazam",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ ROUND EXTRA ]",
            "ALAKAZAM domina o campo com leitura antecipada de movimentos."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "Blue",
          "lines": [
            "Nao tenta vencer no grito.",
            "Quebra o ritmo mental dele primeiro."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_44_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch38_vs_machamp",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ ROUND EXTRA ]",
            "MACHAMP impõe combate de forca bruta em corredor fechado."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_45_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch39_vs_dugtrio",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ ROUND EXTRA ]",
            "DUGTRIO colapsa o terreno para isolar o trio em setores diferentes."
          ]
        },
        {
          "kind": "dialog",
          "speaker": "Green",
          "lines": [
            "Sem panico. Reagrupa pelo corredor leste.",
            "A gente vira isso em dois minutos."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_46_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch40_vs_rhydon",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ ROUND EXTRA ]",
            "RHYDON abre caminho como arma de cerco da Rocket."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_47_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch41_vs_dragonair",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ ROUND EXTRA ]",
            "DRAGONAIR aparece como ultimo filtro antes do encerramento total do conflito."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_48_done",
          "value": true
        }
      ]
    },
    {
      "id": "ch42_rgb_full_closure",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "cutscene",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ RGB ARC - FECHAMENTO COMPLETO ]",
            "Principais rounds, confrontos e marcos centrais foram incorporados no fluxo jogavel.",
            "A campanha encerra com KANTO estabilizada e gancho ativo para a proxima fase."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_49_done",
          "value": true
        }
      ]
    },
    {
      "id": "s1_outline_next",
      "sourceRef": "Pokemon Adventures RGB Arc (chapter-mapped adaptation, Vol.1-3) - scene aligned",
      "type": "outline",
      "actions": [
        {
          "kind": "dialog",
          "speaker": "",
          "lines": [
            "[ STATUS ]",
            "49 blocos narrativos estruturados para fechamento do arco RGB com cobertura ampliada.",
            "Proximo passo: refinamento visual final (tiles/layout) e polimento de cenas."
          ]
        },
        {
          "kind": "set",
          "path": "story.block_50_done",
          "value": true
        }
      ]
    }
  ]
};
