#!/usr/bin/env python3
import re, os, sys

ROOT = os.environ.get("ROOT", ".")
FEATURES = os.path.join(ROOT, "docs", "plan", "features", "FEATURE_MAPPING_UNIFIED.md")

if not os.path.exists(FEATURES):
    print(f"Missing {FEATURES}")
    sys.exit(1)

with open(FEATURES, "r", encoding="utf-8") as f:
    text = f.read()

# Detect feature blocks starting with "## "
blocks = re.split(r'(?m)^##\s+', text)
if len(blocks) <= 1:
    print("No feature blocks found (looking for '## ' headings).")
    sys.exit(0)

header = blocks[0]
features = blocks[1:]

changed = False
new_features = []

for blk in features:
    # blk starts with the heading line content (title + body)
    # Ensure the schema fields exist; if missing, insert stubs.
    want_fields = [
        "Execution Checklist IDs:",
        "ID:",
        "Name:",
        "Priority (P0–P4):",
        "Data Entities (tables/indices):",
        "API Endpoints (with methods):",
        "UI Views/Components:",
        "Tests Required (unit/int/e2e/contract):",
        "Dependencies & Flags:",
    ]

    missing = [field for field in want_fields if field not in blk]
    if missing:
        # Append a "Fields" section if not present; otherwise append stubs at end
        if "## Fields" not in blk and "### Fields" not in blk:
            blk += "\n\n### Fields\n"
        for field in missing:
            blk += f"\n- {field} \n"
        blk += "\n"
        changed = True
    new_features.append(blk)

new_text = "## ".join([header] + new_features)

if changed:
    with open(FEATURES, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("Stubs inserted where missing.")
else:
    print("All feature blocks already contain required fields.")
