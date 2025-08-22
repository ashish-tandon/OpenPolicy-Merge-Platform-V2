#!/usr/bin/env python3
import os, re, sys

ROOT = os.environ.get("ROOT", ".")
FEATURES = os.path.join(ROOT, "docs", "plan", "features", "FEATURE_MAPPING_UNIFIED.md")

if not os.path.exists(FEATURES):
    print(f"Missing {FEATURES}")
    sys.exit(1)

with open(FEATURES, "r", encoding="utf-8") as f:
    text = f.read()

parts = re.split(r'(?m)^##\s+', text)
hdr, blocks = parts[0], parts[1:]
missing = []

for blk in blocks:
    # title is the first line of the block
    title = blk.splitlines()[0].strip() if blk.strip() else "(untitled)"
    if "Execution Checklist IDs:" not in blk:
        missing.append(title)

if missing:
    print("❌ Missing 'Execution Checklist IDs' in feature blocks:")
    for t in missing:
        print(f" - {t}")
    sys.exit(2)

print("✅ All feature blocks contain 'Execution Checklist IDs'.")