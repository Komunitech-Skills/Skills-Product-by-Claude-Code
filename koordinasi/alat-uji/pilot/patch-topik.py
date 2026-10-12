"""Patch openclaw.json bot uji: topik TANPA → skills: [] ; topik DENGAN → tidak dibatasi (semua skill di home).
Pakai: python3 patch-topik.py <openclaw.json> <topik-gNN.json>   (backup dibuat; gateway WAJIB restart sesudahnya)"""
import json, shutil, sys, time
cfg, top = sys.argv[1], sys.argv[2]
shutil.copy(cfg, f"{cfg}.bak-{time.strftime('%Y%m%d%H%M')}")
c = json.load(open(cfg))
t = c["channels"]["telegram"]["groups"]["-1004407409583"].setdefault("topics", {})
m = json.load(open(top))
for k, tid in m.items():
    if k.endswith("|sebelum"):
        t[str(tid)] = {"skills": []}
    else:
        t.pop(str(tid), None)
json.dump(c, open(cfg, "w"), indent=1)
print("topik TANPA dipatch:", [v for k, v in m.items() if k.endswith("|sebelum")], "| total topik di config:", len(t))
