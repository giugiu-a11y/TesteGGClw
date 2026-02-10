#!/bin/bash
set -euo pipefail

STATE_FILE="/tmp/openclaw_health_state.json"
LOG_FILE="/tmp/openclaw_health.log"
COOLDOWN_SEC=3600
MEMORY_COOLDOWN_SEC=$((6 * 3600))

now_ts() { date -u +%s; }

read_state() {
  if [ -f "$STATE_FILE" ]; then
    python3 - <<'PY' "$STATE_FILE"
import json,sys
try:
    with open(sys.argv[1]) as f:
        data=json.load(f)
    print(int(data.get("last_alert", 0)))
except Exception:
    print(0)
PY
  else
    echo 0
  fi
}

read_memory_state() {
  if [ -f "$STATE_FILE" ]; then
    python3 - <<'PY' "$STATE_FILE"
import json,sys
try:
    with open(sys.argv[1]) as f:
        data=json.load(f)
    print(int(data.get("last_memory_disable", 0)))
except Exception:
    print(0)
PY
  else
    echo 0
  fi
}

write_state() {
  local ts="$1"
  python3 - <<'PY' "$STATE_FILE" "$ts"
import json,sys
try:
    with open(sys.argv[1]) as f:
        data=json.load(f)
except Exception:
    data={}
data["last_alert"]=int(sys.argv[2])
with open(sys.argv[1],"w") as f:
    json.dump(data, f)
PY
}

get_bot_token() {
  python3 - <<'PY'
import json
try:
    with open("/home/ubuntu/.openclaw/openclaw.json") as f:
        data=json.load(f)
    print(data.get("channels", {}).get("telegram", {}).get("botToken", "") or "")
except Exception:
    print("")
PY
}

memory_slot() {
  python3 - <<'PY'
import json
try:
    with open("/home/ubuntu/.openclaw/openclaw.json") as f:
        data=json.load(f)
    print((data.get("plugins") or {}).get("slots", {}).get("memory", "") or "")
except Exception:
    print("")
PY
}

disable_memory() {
  python3 - <<'PY'
import json
path="/home/ubuntu/.openclaw/openclaw.json"
try:
    with open(path) as f:
        data=json.load(f)
    data.setdefault("plugins", {}).setdefault("slots", {})["memory"]="none"
    with open(path,"w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    print("memory_disabled")
except Exception as e:
    print("memory_disable_failed")
PY
}

write_memory_state() {
  local ts="$1"
  python3 - <<'PY' "$STATE_FILE" "$ts"
import json,sys
try:
    with open(sys.argv[1]) as f:
        data=json.load(f)
except Exception:
    data={}
data["last_memory_disable"]=int(sys.argv[2])
with open(sys.argv[1],"w") as f:
    json.dump(data, f)
PY
}

send_alert() {
  local msg="$1"
  local token chat_id url
  token="$(get_bot_token)"
  chat_id="881840168"
  if [ -z "$token" ]; then
    echo "missing token" >> "$LOG_FILE"
    return
  fi
  if [[ "$chat_id" == -100* ]]; then
    echo "refusing to send to group id" >> "$LOG_FILE"
    return
  fi
  url="https://api.telegram.org/bot${token}/sendMessage"
  curl -sS -X POST -d "chat_id=${chat_id}" -d "text=${msg}" -d "disable_web_page_preview=true" "$url" >> "$LOG_FILE" 2>&1 || true
}

last_alert="$(read_state)"
last_memory_disable="$(read_memory_state)"
now="$(now_ts)"
if [ $((now - last_alert)) -lt "$COOLDOWN_SEC" ]; then
  exit 0
fi

if ! pgrep -f "openclaw-gateway" >/dev/null 2>&1; then
  send_alert "⚠️ ALERTA OPENCLAW: openclaw-gateway não está rodando."
  write_state "$now"
  exit 0
fi

# Detect loops/fallbacks in recent logs; disable memory to reduce cost/recursion
if [ $((now - last_memory_disable)) -gt "$MEMORY_COOLDOWN_SEC" ]; then
  if command -v openclaw >/dev/null 2>&1; then
    LOGS="$(OPENCLAW_DISABLE_PRESENCE=1 openclaw logs --plain --limit 200 2>/dev/null || true)"
    if echo "$LOGS" | rg -i "fallback|backoff|loop|rate limit|too many requests|retrying" >/dev/null 2>&1; then
      if [ "$(memory_slot)" != "none" ]; then
        if [ "$(disable_memory)" = "memory_disabled" ]; then
          systemctl --user restart openclaw-gateway.service >/dev/null 2>&1 || true
          send_alert "⚠️ ALERTA OPENCLAW: memory desativada após sinais de loop/fallback."
          write_memory_state "$now"
          write_state "$now"
          exit 0
        fi
      fi
    fi
  fi
fi

exit 0
