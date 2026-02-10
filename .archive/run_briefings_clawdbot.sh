#!/bin/bash
set -euo pipefail

# Guardrail: limit LLM runs per day to avoid runaway costs.
TODAY="$(date -u +%Y%m%d)"
COUNT_FILE="/tmp/briefing_llm_count_${TODAY}.txt"
MAX_RUNS_PER_DAY="${MAX_BRIEFING_RUNS_PER_DAY:-2}"
COUNT=0
if [ -f "$COUNT_FILE" ]; then
  COUNT="$(cat "$COUNT_FILE" 2>/dev/null || echo 0)"
fi
if [ "$COUNT" -ge "$MAX_RUNS_PER_DAY" ]; then
  echo "Guardrail: MAX_BRIEFING_RUNS_PER_DAY reached ($COUNT/$MAX_RUNS_PER_DAY). Exiting."
  exit 0
fi
echo $((COUNT+1)) > "$COUNT_FILE"

# 1) Coleta (zero-IA)
python3 /home/ubuntu/clawd/scripts/briefings/fetch_trends_virais.py
python3 /home/ubuntu/clawd/scripts/briefings/fetch_noticias.py
python3 /home/ubuntu/clawd/scripts/briefings/fetch_mercado.py

# 2) Prompts
python3 /home/ubuntu/clawd/scripts/briefings/build_prompt_virais.py
python3 /home/ubuntu/clawd/scripts/briefings/build_prompt_noticias.py
python3 /home/ubuntu/clawd/scripts/briefings/build_prompt_mercado.py

# 3) LLM (optional) -> JSON
USE_LLM="${BRIEFINGS_USE_LLM:-0}"
if [ "$USE_LLM" = "1" ]; then
  clawdbot --profile opus agent --agent main --local --thinking off --message "$(cat /tmp/briefing-virais.prompt.txt)" --json > /tmp/briefing-virais.agent.json
  clawdbot --profile opus agent --agent main --local --thinking off --message "$(cat /tmp/briefing-noticias.prompt.txt)" --json > /tmp/briefing-noticias.agent.json
  clawdbot --profile opus agent --agent main --local --thinking off --message "$(cat /tmp/briefing-mercado.prompt.txt)" --json > /tmp/briefing-mercado.agent.json
else
  : > /tmp/briefing-virais.agent.json
  : > /tmp/briefing-noticias.agent.json
  : > /tmp/briefing-mercado.agent.json
fi

# 4) Extrai texto com fallback
build_out () {
  local name="$1"
  local agent_file="/tmp/briefing-${name}.agent.json"
  local out_file="/tmp/briefing-${name}.out.txt"
  if [ ! -s "$agent_file" ] || rg -q "exception" "$agent_file"; then
    python3 /home/ubuntu/clawd/scripts/briefings/format_fallback.py "$name" > "$out_file"
    return
  fi
  if ! python3 /home/ubuntu/clawd/scripts/briefings/extract_clawdbot_text.py < "$agent_file" > "$out_file"; then
    python3 /home/ubuntu/clawd/scripts/briefings/format_fallback.py "$name" > "$out_file"
  fi
}

build_out virais
build_out noticias
build_out mercado

# 5) Envia no Assistente (somente ele)
python3 /home/ubuntu/clawd/scripts/briefings/send_telegram_assistente.py /tmp/briefing-virais.out.txt
python3 /home/ubuntu/clawd/scripts/briefings/send_telegram_assistente.py /tmp/briefing-noticias.out.txt
python3 /home/ubuntu/clawd/scripts/briefings/send_telegram_assistente.py /tmp/briefing-mercado.out.txt
