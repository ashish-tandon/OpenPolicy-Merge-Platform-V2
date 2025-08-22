#!/usr/bin/env python3
import os,re,glob,json
ROOT="."
VAL=os.path.join(ROOT,"docs","validation")
PLAN=os.path.join(ROOT,"docs","plan")
API=os.path.join(VAL,"API_DESIGN_SPECIFICATION.md")
DB=os.path.join(ROOT,"artifacts","db","pass1")
UI=os.path.join(ROOT,"artifacts","ui","pass1")
OUT_MD=os.path.join(PLAN,"lineage","DATA_LINEAGE_AUTO.md")
OUT_JSON=os.path.join(PLAN,"lineage","DATA_LINEAGE_AUTO.json")
os.makedirs(os.path.dirname(OUT_MD),exist_ok=True)
tp=re.compile(r'\b(table|schema|relation)\s*[:\- ]\s*`?([A-Za-z0-9_\.]+)`?',re.I)
cp=re.compile(r'\b(column|field)\s*[:\- ]\s*`?([A-Za-z0-9_]+)`?',re.I)
ep=re.compile(r'^\s*(GET|POST|PUT|PATCH|DELETE)\s+(/[A-Za-z0-9_\-/{}/\.]+)',re.I)
rp=re.compile(r'\b(Route|Path)\s*[:\- ]\s*`?(/[A-Za-z0-9_\-/{}/\.]+)`?',re.I)
sp=re.compile(r'\b(Screen|View)\s*[:\- ]\s*`?([A-Za-z0-9_/.\-]+)`?',re.I)
xp=re.compile(r'\b(Component)\s*[:\- ]\s*`?([A-Za-z0-9_/.\-]+)`?',re.I)
tbl,cols,endpoints,ui_routes,ui_screens,ui_comps={}, {}, [], set(), set(), set()
for p in glob.glob(os.path.join(DB,"*.md")):
  for ln in open(p,encoding="utf-8",errors="ignore"):
    if (m:=tp.search(ln)): tbl.setdefault(p,set()).add(m.group(2))
    if (c:=cp.search(ln)): cols.setdefault(p,set()).add(c.group(2))
if os.path.exists(API):
  for ln in open(API,encoding="utf-8",errors="ignore"):
    if (m:=ep.match(ln)): endpoints.append({"method":m.group(1).upper(),"path":m.group(2)})
for p in glob.glob(os.path.join(UI,"*.md")):
  for ln in open(p,encoding="utf-8",errors="ignore"):
    for m in rp.finditer(ln): ui_routes.add(m.group(2))
    for m in sp.finditer(ln): ui_screens.add(m.group(2))
    for m in xp.finditer(ln): ui_comps.add(m.group(2))
def toks(x): return [s.split("{")[0] for s in x.strip("/").split("/") if s]
def match(path,name): 
  P=toks(path); return any(t and t in name for t in P)
data={"db":[{"file":os.path.relpath(fp,ROOT),"tables":sorted(list(tbl.get(fp,set()))),"columns":sorted(list(cols.get(fp,set())))} for fp in sorted(tbl.keys())],
      "api":endpoints,
      "ui":{"routes":sorted(list(ui_routes)),"screens":sorted(list(ui_screens)),"components":sorted(list(ui_comps))},
      "mappings":[]}
for ep_ in endpoints:
  path=ep_["path"]
  db_c=[{"table":t,"source":os.path.relpath(fp,ROOT)} for fp in sorted(tbl.keys()) for t in sorted(list(tbl[fp])) if match(path,t)]
  ui_c={"routes":[r for r in ui_routes if match(path,r)],"screens":[s for s in ui_screens if match(path,s)],"components":[c for c in ui_comps if match(path,c)]}
  data["mappings"].append({"endpoint":ep_,"db_candidates":db_c,"ui_candidates":ui_c})
os.makedirs(os.path.dirname(OUT_JSON),exist_ok=True)
open(OUT_JSON,"w",encoding="utf-8").write(json.dumps(data,indent=2,ensure_ascii=False))
with open(OUT_MD,"w",encoding="utf-8") as w:
  w.write("# Data Lineage (Auto-Generated)\n\n")
  w.write("Source docs: validation & artifacts (existing + legacy references preserved in SoT Crosslinks Appendix).\n\n")
  w.write(f"- JSON: `{os.path.relpath(OUT_JSON,ROOT)}`\n\n## API Endpoints\n")
  for e in endpoints: w.write(f"- `{e['method']} {e['path']}`\n")
  w.write("\n## Suggested End-to-End Pairs\n")
  for m in data["mappings"]:
    w.write(f"### `{m['endpoint']['method']} {m['endpoint']['path']}`\n")
    if m["db_candidates"]:
      w.write("- **DB candidates:**\n")
      for d in m["db_candidates"]: w.write(f"  - `{d['table']}` (from {d['source']})\n")
    else: w.write("- **DB candidates:** _none detected_\n")
    w.write("- **UI routes:** " + (", ".join(m['ui_candidates']['routes']) or "_none_") + "\n")
    w.write("- **UI screens:** " + (", ".join(m['ui_candidates']['screens']) or "_none_") + "\n")
    w.write("- **UI components:** " + (", ".join(m['ui_candidates']['components']) or "_none_") + "\n\n")
print(f"Wrote {OUT_MD} and {OUT_JSON}")
