#!/bin/bash
# batch-generator.sh
# Generate 35 posts for next week (1 Claude call, zero IA posting)
# Usage: bash scripts/batch-generator.sh

set -e

cd "$(dirname "$0")/.."

LOG_FILE="logs/batch-generation.log"
PERSONA_FILE="config/persona.txt"
DATA_FILE="data/posts_current.json"
ARCHIVE_FILE="data/archive/posts_$(date -d '+7 days' +%Y-%m-%d).json"

{
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🚀 Starting batch generation..."
  
  # Verify persona file exists
  if [ ! -f "$PERSONA_FILE" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Persona file not found: $PERSONA_FILE"
    exit 1
  fi
  
  # Read persona
  PERSONA=$(cat "$PERSONA_FILE")
  NEXT_WEEK=$(date -d '+7 days' +%Y-%m-%d)
  WEEK_END=$(date -d '+14 days' +%Y-%m-%d)
  
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📝 Persona loaded"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📅 Generating posts for: $NEXT_WEEK to $WEEK_END"
  
  # Generate 35 posts via Claude (1 call)
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🧠 Calling Claude (batch generation)..."
  
  OUTPUT=$(clawdbot agent --local --session-id "jesus-batch-$(date +%s)" --thinking low << 'PROMPT_EOF'
PERSONA:
Tom: Reflexivo, profundo, existencial
Linguagem: Simples, direta, acessível (evitar palavras complexas)
Perspectiva: Terceira pessoa (NUNCA "eu")
Temas: Mudança pessoal, autenticidade, relacionamentos, espiritualidade, paradoxos da vida
Comprimento: 280 chars max
Estilo: Provocação + reflexão + espiritualidade (sem religião forçada)

TEMAS PROIBIDOS:
❌ Bolsas de estudo
❌ Intercâmbio
❌ Educação formal
❌ Trabalho remoto como tema principal
❌ Primeira pessoa ("Eu...")
❌ Negatividade pura (sem esperança)

EXEMPLOS BOM:
✅ "Metade das orações são pra mudar os outros. Outra metade pra não ter que mudar. Jesus sorri dessa contradição humana."
✅ "Quer que eu mude sua vida, mas não quer largar o sofá. Parceria é via dupla."
✅ "Tanta correria pra ter... o quê? Paz não está em coisas, mas em quem você é."

---

TAREFA:
Gera 35 tweets para a próxima semana (5 por dia, 7 dias):
- Horários: 09:00, 12:00, 15:00, 18:00, 21:00 BRT
- Temas variados (mudança, autenticidade, relacionamentos, paradoxos)
- Respeta persona rigorosamente
- Cada tweet tem max 280 chars

OUTPUT FORMAT (JSON válido):
```json
{
  "week": "2026-02-06 to 2026-02-12",
  "generated_at": "2026-02-05T02:00:00Z",
  "posts": [
    {"date": "2026-02-06", "time": "09:00", "text": "..."},
    {"date": "2026-02-06", "time": "12:00", "text": "..."},
    ...
  ]
}
```

APENAS JSON, nada de explicação ou prefixo.
PROMPT_EOF
  )
  
  # Validate JSON
  if ! echo "$OUTPUT" | jq . >/dev/null 2>&1; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Invalid JSON output from Claude"
    echo "$OUTPUT" >> "$LOG_FILE"
    exit 1
  fi
  
  # Save current posts to archive
  if [ -f "$DATA_FILE" ]; then
    cp "$DATA_FILE" "$ARCHIVE_FILE"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📦 Archived previous posts: $ARCHIVE_FILE"
  fi
  
  # Save new posts
  echo "$OUTPUT" | jq . > "$DATA_FILE"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Generated 35 posts: $DATA_FILE"
  
  # Verify file
  POST_COUNT=$(jq '.posts | length' "$DATA_FILE")
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📊 Posts count: $POST_COUNT"
  
  if [ "$POST_COUNT" != "35" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  Expected 35 posts, got $POST_COUNT"
  fi
  
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🎉 Batch generation complete!"
  
} | tee -a "$LOG_FILE"
