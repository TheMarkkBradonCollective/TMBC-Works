#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BASE="http://127.0.0.1:8765/TMBC-Works"
fail=0

while IFS=, read -r num name slug url email phone; do
  [[ "$num" == "lead_number" ]] && continue
  path="$ROOT/$slug/index.html"
  if [[ ! -f "$path" ]]; then
    echo "MISSING: $slug"
    fail=1
    continue
  fi
  if ! grep -q 'name="robots" content="noindex"' "$path"; then
    echo "NO NOINDEX: $slug"
    fail=1
  fi
  if ! grep -q 'TMBC Works' "$path"; then
    echo "NO BANNER: $slug"
    fail=1
  fi
  code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/$slug/" || echo "000")
  if [[ "$code" != "200" ]]; then
    echo "HTTP $code: $slug"
    fail=1
  fi
done < "$ROOT/previews.csv"

if [[ "$fail" -eq 0 ]]; then
  echo "All checks passed."
else
  exit 1
fi
