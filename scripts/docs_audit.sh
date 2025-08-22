#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-.}"
VAL="$ROOT/docs/validation"
PLAN="$ROOT/docs/plan"
SOT="$PLAN/OPENPOLICY_V2_SOURCE_OF_TRUTH.md"
UPDATED="$VAL/UPDATED_MASTER_EXECUTION_CHECKLIST.md"
FEATURES="$PLAN/features/FEATURE_MAPPING_UNIFIED.md"
LINEAGE="$PLAN/lineage/DATA_LINEAGE_MAP.md"
STRICT="${STRICT:-}"

fail() { echo "❌ $*"; [ -n "$STRICT" ] && exit 1 || true; }

echo "== Docs Audit =="
echo "Repo root: $ROOT"

# 1) Inventory
VAL_COUNT=$(find "$VAL" -type f \( -name '*.md' -o -name '*.csv' \) 2>/dev/null | wc -l | xargs || echo 0)
echo "Validation docs: $VAL_COUNT"

# 2) Presence checks
[ -f "$SOT" ] || fail "Missing SoT: $SOT"
[ -f "$UPDATED" ] || { echo "Warning: Missing updated checklist: $UPDATED"; }
[ -f "$FEATURES" ] || fail "Missing feature map: $FEATURES"
[ -f "$LINEAGE" ] || fail "Missing lineage map: $LINEAGE"

# 3) MERGE_NOTE flags
MERGE_NOTES=$(grep -R --line-number "MERGE_NOTE" "$ROOT" 2>/dev/null || true)
if [ -n "$MERGE_NOTES" ]; then
  echo "⚠ Found MERGE_NOTE markers:"
  echo "$MERGE_NOTES"
  [ -n "$STRICT" ] && fail "Unresolved MERGE_NOTE markers found"
fi

# 4) Cross-link sanity: Feature IDs ↔ Checklist IDs
if [ -f "$UPDATED" ] && [ -f "$FEATURES" ]; then
  MISSING_LINKS=0
  
  # Extract candidate checklist IDs from checklist (e.g., "1", "15.2", etc.)
  CHECKLIST_IDS=$(awk '
  /^#+[[:space:]]*Task/ {next}
  {
    while (match($0, /\b[0-9]+(\.[0-9]+)?\b/)) {
      print substr($0, RSTART, RLENGTH)
      $0 = substr($0, RSTART+RLENGTH)
    }
  }' "$UPDATED" | sort -u)
  
  # For each feature block, verify it references at least one checklist ID present above
  echo "Scanning feature-to-checklist references…"
  awk -v ids="$(printf "%s" "$CHECKLIST_IDS")" '
  BEGIN {
    split(ids, a, "\n");
    for (i in a) if (length(a[i])) seen[a[i]]=1
  }
  BEGINFILE { inblock=0; block=""; title="" }
  # Delimit blocks by headings
  /^##[[:space:]]/ {
    if (length(block)) {
      # Validate previous block
      found=0
      for (id in seen) {
        if (block ~ ("\\b" id "\\b")) { found=1; break }
      }
      if (!found) {
        printf("⚠ Feature block missing checklist ID link: %s\n", title);
        missing++
      }
    }
    inblock=1
    title=$0
    block=""
    next
  }
  { if (inblock) block = block "\n" $0 }
  END {
    if (length(block)) {
      found=0
      for (id in seen) { if (block ~ ("\\b" id "\\b")) { found=1; break } }
      if (!found) { printf("⚠ Feature block missing checklist ID link: %s\n", title); missing++ }
    }
    if (missing>0) { exit 42 }
  }' "$FEATURES" || { MISSING_LINKS=1; }
  
  if [ "$MISSING_LINKS" -eq 1 ]; then
    [ -n "$STRICT" ] && fail "Missing feature↔checklist links"
  fi
fi

# 5) Size growth sanity (optional, uses git if available)
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Checking doc deletions vs HEAD…"
  if git diff --numstat HEAD -- docs/ | awk '{if ($3 ~ /\.md$|\.csv$/ && $1==0 && $2>0) c++} END{exit c>0}'; then
    echo "✅ No line deletions detected in docs/* vs HEAD"
  else
    fail "Detected line deletions in docs/* vs HEAD"
  fi
fi

# 6) SoT index coverage: SoT must link to ≥95% of validation + artifact files
if [ -f "$SOT" ]; then
  SOT_CONTENT=$(cat "$SOT")
  list_targets() {
    find "$VAL" -type f \( -name '*.md' -o -name '*.csv' \) 2>/dev/null || true
    find "$ROOT/artifacts" -type f -name '*.md' 2>/dev/null || true
  }
  TOTAL=0
  HIT=0
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    TOTAL=$((TOTAL+1))
    rel=$(python3 - <<PY
import os, sys
print(os.path.relpath("$f","$ROOT"))
PY
)
    # consider it "linked" if its relpath or basename appears in SoT
    base=$(basename "$rel")
    if grep -Fq "$rel" <<<"$SOT_CONTENT" || grep -Fq "$base" <<<"$SOT_CONTENT"; then
      HIT=$((HIT+1))
    fi
  done < <(list_targets)
  
  if [ "$TOTAL" -gt 0 ]; then
    pct=$(python3 - <<PY
t=$TOTAL; h=$HIT
print(f"{(h*100.0)/t:.2f}")
PY
)
    echo "SoT index coverage: $HIT/$TOTAL (${pct}%)"
    # Enforce ≥95%
    python3 - <<PY
pct=float("$pct")
import sys
strict = "${STRICT}"
if pct < 95.0 and strict:
    print("Coverage below 95% with STRICT=1")
    sys.exit(1)
PY
  fi
fi

echo "✅ Docs audit complete."