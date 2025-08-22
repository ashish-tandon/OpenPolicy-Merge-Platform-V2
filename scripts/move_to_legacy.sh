#!/usr/bin/env bash
set -euo pipefail

ALLOWED=(
  "./docs/validation"
  "./docs/plan"
  "./docs/reviews"
  "./docs/bugs"
  "./artifacts"
  "./scripts"
  "./.gitattributes"
  "./README.md"
  "./package.json"
  "./docker-compose.yml"
  "./.github"
)

is_allowed() {
  local path="$1"
  for a in "${ALLOWED[@]}"; do
    [[ "$path" == "$a"* ]] && return 0
  done
  return 1
}

mkdir -p legacy
git ls-files -z | while IFS= read -r -d '' f; do
  if ! is_allowed "$f"; then
    mkdir -p "legacy/$(dirname "$f")"
    git mv "$f" "legacy/$f"
  fi
done

# Also move untracked files (excluding gitignored)
git ls-files -o --exclude-standard -z | while IFS= read -r -d '' f; do
  if ! is_allowed "$f"; then
    mkdir -p "legacy/$(dirname "$f")"
    mkdir -p "$(dirname "legacy/$f")"
    mv "$f" "legacy/$f"
    git add "legacy/$f"
  fi
done