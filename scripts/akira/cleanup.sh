#!/bin/bash
# cleanup.sh - Remove old logs and caches
# Roda automaticamente via cron

LOG_FILE="/tmp/cleanup.log"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

echo "[$TS] 🧹 Cleanup iniciado" >> "$LOG_FILE"

# 1. Remove /tmp/akira-*.json > 7 dias
DELETED_TMP=$(find /tmp/akira-*.json -mtime +7 -delete -print 2>/dev/null | wc -l)
echo "[$TS] 🗑️  Deleted /tmp/akira-*.json (>7d): $DELETED_TMP files" >> "$LOG_FILE"

# 2. Remove cron runs > 30 dias
DELETED_CRON=$(find ~/.clawdbot/cron/runs/*.jsonl -mtime +30 -delete -print 2>/dev/null | wc -l)
echo "[$TS] 🗑️  Deleted cron runs (>30d): $DELETED_CRON files" >> "$LOG_FILE"

# 3. Compress old JSONs (6h-7d) to save space
COMPRESSED=$(find /tmp/akira-*.json -mtime -7 -mtime +0.25 -exec gzip -9 {} + -print 2>/dev/null | wc -l)
echo "[$TS] 📦 Compressed JSON (6h-7d): $COMPRESSED files" >> "$LOG_FILE"

# 4. Cleanup old cleanup logs (>90 dias)
OLD_CLEANUP=$(find "$LOG_FILE" -mtime +90 -delete -print 2>/dev/null)
if [ -n "$OLD_CLEANUP" ]; then
  echo "[$TS] 🗑️  Cleanup log archived" >> "$LOG_FILE"
fi

# 5. Report disk space
DISK_USAGE=$(du -sh /home/ubuntu/clawd /tmp 2>/dev/null | tail -2)
echo "[$TS] 💾 Disk usage:" >> "$LOG_FILE"
echo "$DISK_USAGE" >> "$LOG_FILE"

echo "[$TS] ✅ Cleanup concluído" >> "$LOG_FILE"

# Print summary
echo "✅ Cleanup feito:"
echo "  - /tmp/akira-*.json (>7d): $DELETED_TMP deleted"
echo "  - Cron runs (>30d): $DELETED_CRON deleted"
echo "  - JSONs comprimidos: $COMPRESSED"
