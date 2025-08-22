#!/usr/bin/env python3
import os,re,glob,json,shutil,sys
ROOT="."
APPLY=os.environ.get("APPLY","0")=="1"
LEGACY="legacy"
os.makedirs(LEGACY,exist_ok=True)
# 1) Collect references from key docs (SoT, feature map, validation index)
candidates=[]
for p in ["docs/plan/OPENPOLICY_V2_SOURCE_OF_TRUTH.md",
          "docs/plan/features/FEATURE_MAPPING_UNIFIED.md",
          "docs/validation/MASTER_DOCUMENT_INDEX.md",
          "docs/validation/INDEX.md"]:
  if os.path.exists(p): candidates.append(p)
refs=set()
for p in candidates:
  txt=open(p,"r",encoding="utf-8",errors="ignore").read()
  for m in re.findall(r'[\w/\.-]+\.(?:md|csv|yml|yaml|json|sql|py|sh)',txt):
    if os.path.exists(m): refs.add(os.path.normpath(m))
# 2) Walk repo and classify
keep_roots=("docs","artifacts",".github","scripts","Makefile","docker-compose.yml","README.md")
all_files=[f for f in glob.glob("**/*",recursive=True) if os.path.isfile(f) and not f.startswith(".git/")]
core=set()
for k in keep_roots:
  if os.path.isdir(k):
    core.update([f for f in all_files if f.startswith(k.rstrip("/")+"/")])
  elif os.path.isfile(k):
    core.add(k)
# referenced = refs ∪ core
referenced=set(refs)|set(core)
legacy_candidates=[f for f in all_files if f not in referenced and not f.startswith(LEGACY+"/")]
manifest={"dry_run": not APPLY, "moved":[], "kept_core":sorted(list(core)), "kept_referenced":sorted(list(referenced- set(core))), "legacy_candidates":sorted(legacy_candidates)}
# 3) Apply moves preserving structure
if APPLY:
  for f in legacy_candidates:
    dest=os.path.join(LEGACY,f)
    os.makedirs(os.path.dirname(dest),exist_ok=True)
    shutil.move(f,dest)
    manifest["moved"].append({"from":f,"to":dest})
open("reports/organizer_manifest.json","w",encoding="utf-8").write(json.dumps(manifest,indent=2))
print(f"Organizer manifest written: reports/organizer_manifest.json (APPLY={APPLY})")
