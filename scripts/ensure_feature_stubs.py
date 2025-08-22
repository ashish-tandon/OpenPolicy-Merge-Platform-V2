#!/usr/bin/env python3
import os,re,sys
ROOT="."
FEATURES=os.path.join(ROOT,"docs","plan","features","FEATURE_MAPPING_UNIFIED.md")
if not os.path.exists(FEATURES):
  os.makedirs(os.path.dirname(FEATURES),exist_ok=True)
  open(FEATURES,"w",encoding="utf-8").write("# Feature Mapping (Unified)\n")
txt=open(FEATURES,"r",encoding="utf-8").read()
parts=re.split(r'(?m)^##\s+',txt)
if len(parts)==1: # no features yet; create a starter block to be enhanced later
  txt += "\n## Placeholder Feature\n\n### Fields\n- Execution Checklist IDs:\n- ID:\n- Name:\n- Priority (P0–P4):\n- Data Entities (tables/indices):\n- API Endpoints (with methods):\n- UI Views/Components:\n- Tests Required (unit/int/e2e/contract):\n- Dependencies & Flags:\n"
  open(FEATURES,"w",encoding="utf-8").write(txt); print("Seeded feature map.")
  sys.exit(0)
hdr,blocks=parts[0],parts[1:]
fields=["Execution Checklist IDs:","ID:","Name:","Priority (P0–P4):","Data Entities (tables/indices):","API Endpoints (with methods):","UI Views/Components:","Tests Required (unit/int/e2e/contract):","Dependencies & Flags:"]
changed=False; out=[hdr]
for b in blocks:
  missing=[f for f in fields if f not in b]
  if missing:
    if "### Fields" not in b: b+="\n\n### Fields\n"
    for f in missing: b+=f"\n- {f}\n"
    b+="\n"; changed=True
  out.append(b)
new="## ".join(out)
if changed: open(FEATURES,"w",encoding="utf-8").write(new)
print("Feature stubs ensured/enhanced.")
