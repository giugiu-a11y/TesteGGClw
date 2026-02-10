#!/bin/bash
# test-single-post.sh
# Test: Post a single tweet manually
# Usage: bash scripts/test-single-post.sh "Your test tweet here..."

set -e

cd "$(dirname "$0")/.."

TEXT="$1"
if [ -z "$TEXT" ]; then
  echo "❌ Usage: $0 \"Your tweet text here...\""
  exit 1
fi

# Validate length
CHAR_COUNT=${#TEXT}
if [ "$CHAR_COUNT" -gt 280 ]; then
  echo "❌ Tweet too long ($CHAR_COUNT > 280 chars)"
  exit 1
fi

echo "📝 Testing tweet post..."
echo "📊 Length: $CHAR_COUNT/280 chars"
echo "🐦 Text: $TEXT"
echo ""

# Activate venv
source venv/bin/activate

# Load credentials with EXPORT (critical fix!)
set -a
source .env
set +a

# Post
python3 scripts/post_jesus.py "$TEXT"

echo ""
echo "✅ Test successful!"
