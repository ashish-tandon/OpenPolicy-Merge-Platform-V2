#!/usr/bin/env python3
import re, sys, os, glob, json
from collections import defaultdict

ROOT = os.environ.get("ROOT", ".")
VAL = os.path.join(ROOT, "docs", "validation")
PLAN = os.path.join(ROOT, "docs", "plan")
API_SPEC = os.path.join(VAL, "API_DESIGN_SPECIFICATION.md")
DB_ART_DIR = os.path.join(ROOT, "artifacts", "db", "pass1")
UI_ART_DIR = os.path.join(ROOT, "artifacts", "ui", "pass1")
OUT_MD = os.path.join(PLAN, "lineage", "DATA_LINEAGE_AUTO.md")
OUT_JSON = os.path.join(PLAN, "lineage", "DATA_LINEAGE_AUTO.json")

os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)

table_pat = re.compile(r'\b(table|schema|relation)\s*[:\- ]\s*`?([a-zA-Z0-9_\.]+)`?', re.I)
col_pat   = re.compile(r'\b(column|field)\s*[:\- ]\s*`?([a-zA-Z0-9_]+)`?', re.I)
endpoint_pat = re.compile(r'^\s*(GET|POST|PUT|PATCH|DELETE)\s+(/[a-zA-Z0-9_\-/{}/\.]+)', re.I)
route_pat = re.compile(r'\b(Route|Path)\s*[:\- ]\s*`?(/[a-zA-Z0-9_\-/{}/\.]+)`?', re.I)
screen_pat = re.compile(r'\b(Screen|View)\s*[:\- ]\s*`?([A-Za-z0-9_/.\-]+)`?', re.I)
comp_pat   = re.compile(r'\b(Component)\s*[:\- ]\s*`?([A-Za-z0-9_/.\-]+)`?', re.I)

tables_by_file = defaultdict(set)
columns_by_file = defaultdict(set)
endpoints = []
ui_routes, ui_screens, ui_components = set(), set(), set()

# DB
for p in glob.glob(os.path.join(DB_ART_DIR, "*.md")):
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if (m := table_pat.search(line)): tables_by_file[p].add(m.group(2))
            if (c := col_pat.search(line)):   columns_by_file[p].add(c.group(2))

# API
if os.path.exists(API_SPEC):
    with open(API_SPEC, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if (m := endpoint_pat.match(line)):
                endpoints.append({"method": m.group(1).upper(), "path": m.group(2)})

# UI
for p in glob.glob(os.path.join(UI_ART_DIR, "*.md")):
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            for m in route_pat.finditer(line):  ui_routes.add(m.group(2))
            for m in screen_pat.finditer(line): ui_screens.add(m.group(2))
            for m in comp_pat.finditer(line):   ui_components.add(m.group(2))

def path_tokens(path):
    return [seg.split("{")[0] for seg in path.strip("/").split("/") if seg]

def token_match(path, name):
    toks = path_tokens(path)
    return any(tok and tok in name for tok in toks)

# Build JSON structure
data = {
    "db": [
        {
            "file": os.path.relpath(fp, ROOT),
            "tables": sorted(list(tables_by_file[fp])),
            "columns": sorted(list(columns_by_file[fp])),
        }
        for fp in sorted(tables_by_file.keys())
    ],
    "api": endpoints,
    "ui": {
        "routes": sorted(list(ui_routes)),
        "screens": sorted(list(ui_screens)),
        "components": sorted(list(ui_components)),
    },
    "mappings": []  # endpoint -> db candidates -> ui candidates
}

# Suggested E2E mappings
for ep in endpoints:
    method, path = ep["method"], ep["path"]
    db_candidates = []
    for fpath in sorted(tables_by_file.keys()):
        for t in sorted(tables_by_file[fpath]):
            if token_match(path, t):
                db_candidates.append({"table": t, "source": os.path.relpath(fpath, ROOT)})
    ui_cand = {
        "routes": [r for r in ui_routes if token_match(path, r)],
        "screens": [s for s in ui_screens if token_match(path, s)],
        "components": [c for c in ui_components if token_match(path, c)],
    }
    data["mappings"].append({
        "endpoint": {"method": method, "path": path},
        "db_candidates": db_candidates,
        "ui_candidates": ui_cand
    })

# Write JSON
with open(OUT_JSON, "w", encoding="utf-8") as jf:
    json.dump(data, jf, indent=2, ensure_ascii=False)

# Write MD (summary)
with open(OUT_MD, "w", encoding="utf-8") as w:
    w.write("# Data Lineage (Auto-Generated)\n\n")
    w.write("Auto-generated from DB artifacts, API spec, and UI artifacts. See the JSON for structured data.\n\n")
    w.write(f"- JSON: `{os.path.relpath(OUT_JSON, ROOT)}`\n\n")
    w.write("## API Endpoints\n")
    for ep in endpoints:
        w.write(f"- `{ep['method']} {ep['path']}`\n")
    w.write("\n## Suggested End-to-End Route Pairs (summary)\n")
    for m in data["mappings"]:
        w.write(f"### `{m['endpoint']['method']} {m['endpoint']['path']}`\n")
        if m["db_candidates"]:
            w.write("- **DB candidates:**\n")
            for d in m["db_candidates"]:
                w.write(f"  - `{d['table']}` (from {d['source']})\n")
        else:
            w.write("- **DB candidates:** _none detected_\n")
        w.write("- **UI routes:** " + (", ".join(m["ui_candidates"]["routes"]) or "_none_") + "\n")
        w.write("- **UI screens:** " + (", ".join(m["ui_candidates"]["screens"]) or "_none_") + "\n")
        w.write("- **UI components:** " + (", ".join(m["ui_candidates"]["components"]) or "_none_") + "\n\n")

print(f"Wrote {OUT_MD} and {OUT_JSON}")