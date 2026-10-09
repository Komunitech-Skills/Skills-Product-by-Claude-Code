#!/usr/bin/env bash
# mk-home.sh NAMA [skill...]  -> buat HOME OpenClaw terpisah berisi hanya skill yang disebut (tanpa skill = "sebelum")
set -e
R=/tmp/claude-0/-home-user-Skills/d777d314-a309-56aa-81f9-6ad58561dd1c/scratchpad/openclaw-real
SRC=$R/home/.openclaw; N=$1; shift
H=$R/homes/$N/.openclaw
rm -rf "$R/homes/$N"; mkdir -p "$H/skills" "$H/workspace"
python3 - "$SRC/openclaw.json" "$H/openclaw.json" <<'PY'
import json,sys
c=json.load(open(sys.argv[1])); c.pop('channels',None); c.pop('gateway',None)
c.setdefault('commands',{}).pop('ownerAllowFrom',None)
json.dump(c,open(sys.argv[2],'w'),indent=1)
PY
for f in AGENTS.md SOUL.md IDENTITY.md; do [ -f "$SRC/workspace/$f" ] && cp "$SRC/workspace/$f" "$H/workspace/"; done
for s in "$@"; do cp -r /home/user/Skills/skills/$s "$H/skills/"; done
find "$H/skills" -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
echo "home $N: $(ls $H/skills | wc -l) skill"
