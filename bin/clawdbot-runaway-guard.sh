#!/usr/bin/env bash
set -euo pipefail

LOG="$(ls -1t /tmp/clawdbot/clawdbot-*.log 2>/dev/null | head -n 1 || true)"
[ -n "${LOG:-}" ] || exit 0
[ -f "$LOG" ] || exit 0

python3 - <<'PY'
import re, datetime, pathlib, sys

log = pathlib.Path(next(pathlib.Path("/tmp/clawdbot").glob("clawdbot-*.log"), None) or "")
# pega o mais recente com glob em python (evita depender do bash)
paths = sorted(pathlib.Path("/tmp/clawdbot").glob("clawdbot-*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
if not paths:
    sys.exit(0)
log = paths[0]

lines = log.read_text(errors="ignore").splitlines()[-4000:]
now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
cut = now - datetime.timedelta(seconds=120)

cnt = 0
for ln in lines:
    if "embedded run start:" not in ln: 
        continue
    if "messageChannel=telegram" not in ln:
        continue
    m = re.search(r'"time"\s*:\s*"([^"]+)"', ln)
    if not m:
        continue
    t = m.group(1).replace("Z", "+00:00")
    try:
        dt = datetime.datetime.fromisoformat(t)
    except Exception:
        continue
    if dt >= cut:
        cnt += 1

# 2 ou mais runs em 2 min sem você digitar = loop
sys.exit(1 if cnt >= 2 else 0)
PY
