#!/bin/bash
# batch-generator-v2.sh
# Generate 35 posts for next week via OpenClaw sessions_spawn (RELIABLE)
# Usage: bash scripts/batch-generator-v2.sh

set -e
cd "$(dirname "$0")/.."

LOG_FILE="logs/batch-generation.log"
PERSONA_FILE="config/persona.txt"
DATA_FILE="data/posts_current.json"
ARCHIVE_FILE="data/archive/posts_$(date -d '+7 days' +%Y-%m-%d).json"

{
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🚀 Starting batch generation v2..."
  
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
  
  # Generate 35 posts via OpenClaw (sub-agent session - RELIABLE)
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🧠 Calling Claude via OpenClaw..."
  
  OUTPUT=$(openclaw sessions_spawn \
    --model haiku \
    --timeout 120 \
    --task "Gera 35 tweets para a próxima semana ($NEXT_WEEK a $WEEK_END), 5 por dia, horários 09:00, 12:00, 15:00, 18:00, 21:00 BRT.

Persona Jesus Sincero:
- Tom: Reflexivo, profundo, existencial
- Perspectiva: TERCEIRA PESSOA (NUNCA 'eu')
- Temas: Mudança pessoal, autenticidade, relacionamentos, espiritualidade, paradoxos
- Max 280 chars por tweet

Proibido:
- Bolsas, intercâmbio, educação formal
- Primeira pessoa
- Negatividade pura

Exemplos bons:
- 'Metade das orações são pra mudar os outros. Outra metade pra não ter que mudar.'
- 'Quer paz, mas não quer silêncio. Qual você escolhe?'
- 'Tanta correria pra ter o quê? Paz não está em coisas, mas em quem você é.'

OUTPUT: JSON válido APENAS:
{\"week\": \"$NEXT_WEEK to $WEEK_END\", \"generated_at\": \"$(date -Iseconds)\", \"posts\": [{\"date\": \"2026-02-09\", \"time\": \"09:00\", \"text\": \"...\"}]}" 2>&1)
  
  # Extract JSON from output
  JSON_OUTPUT=$(echo "$OUTPUT" | grep -o '{.*"posts".*}' | head -1)
  
  if [ -z "$JSON_OUTPUT" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ No JSON found in output"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Output: $OUTPUT" >> "$LOG_FILE"
    exit 1
  fi
  
  # Validate JSON
  if ! echo "$JSON_OUTPUT" | jq . >/dev/null 2>&1; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Invalid JSON output"
    echo "$JSON_OUTPUT" >> "$LOG_FILE"
    exit 1
  fi
  
  # Save current posts to archive
  if [ -f "$DATA_FILE" ]; then
    mkdir -p data/archive
    cp "$DATA_FILE" "$ARCHIVE_FILE"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📦 Archived previous posts: $ARCHIVE_FILE"
  fi
  
  # Save new posts
  echo "$JSON_OUTPUT" | jq . > "$DATA_FILE"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Generated posts: $DATA_FILE"
  
  # Verify file
  POST_COUNT=$(jq '.posts | length' "$DATA_FILE" 2>/dev/null || echo "0")
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📊 Posts count: $POST_COUNT"
  
  if [ "$POST_COUNT" != "35" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  Expected 35 posts, got $POST_COUNT"
  else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Perfect! 35 posts ready"
  fi
  
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🎉 Batch generation complete!"
  
} | tee -a "$LOG_FILE"
