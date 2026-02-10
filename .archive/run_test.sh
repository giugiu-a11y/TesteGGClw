#!/bin/bash
set -euo pipefail

python3 /home/ubuntu/clawd/scripts/briefings/fetch_trends_virais.py
python3 /home/ubuntu/clawd/scripts/briefings/fetch_noticias.py
python3 /home/ubuntu/clawd/scripts/briefings/fetch_mercado.py

python3 /home/ubuntu/clawd/scripts/briefings/build_prompt_virais.py
python3 /home/ubuntu/clawd/scripts/briefings/build_prompt_noticias.py
python3 /home/ubuntu/clawd/scripts/briefings/build_prompt_mercado.py

echo "OK. Prompts gerados em /tmp/briefing-*.prompt.txt"
