#!/usr/bin/env bash
# Uji muat semua skill di OpenClaw sungguhan (tanpa API key model).
# Memasang Node 24 + OpenClaw ke /tmp (tidak mengubah sistem), menyalin skills/ ke
# HOME sementara, lalu menjalankan `openclaw skills check --json`.
# Yang diuji: skill terbaca, eligible, terlihat oleh model, bisa dipanggil sebagai perintah.
# Yang TIDAK diuji: perilaku agent saat menjalankan skill (butuh API key model).
#
# Pakai:  bash scripts/uji_openclaw.sh [versi-openclaw]
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
VERSI_OC="${1:-latest}"
DASAR=/tmp/uji-openclaw
mkdir -p "$DASAR"

# Node 24 (OpenClaw 2026.x butuh Node >= 24.16)
if ! ls "$DASAR"/node-v24*/bin/node >/dev/null 2>&1; then
  V=$(curl -s https://nodejs.org/dist/index.json | python3 -c \
      "import json,sys;print([r['version'] for r in json.load(sys.stdin) if r['version'].startswith('v24.')][0])")
  curl -sL "https://nodejs.org/dist/$V/node-$V-linux-x64.tar.xz" | tar xJ -C "$DASAR"
fi
export PATH="$(ls -d "$DASAR"/node-v24*/bin | head -1):$PATH"

npm install --prefix "$DASAR" "openclaw@$VERSI_OC" --no-audit --no-fund --silent >/dev/null 2>&1
OC="$DASAR/node_modules/.bin/openclaw"
echo "OpenClaw: $("$OC" --version | head -1)"

export HOME="$DASAR/home"
rm -rf "$HOME" && mkdir -p "$HOME/.openclaw/skills"
cp -r "$REPO"/skills/* "$HOME/.openclaw/skills/"
find "$HOME/.openclaw/skills" -name examples -prune -exec rm -rf {} +

cd "$DASAR"
timeout 180 "$OC" skills check --json 2>/dev/null > "$DASAR/check.json"

python3 - "$REPO" "$DASAR/check.json" <<'EOF'
import json, os, sys
repo, path = sys.argv[1], sys.argv[2]
t = open(path).read(); d = json.loads(t[t.find('{'):])
nama = lambda k: {x.get('name') if isinstance(x, dict) else x for x in d.get(k, [])}
milik = set(os.listdir(os.path.join(repo, 'skills')))
gagal = False
for k in ('eligible', 'modelVisible', 'commandVisible'):
    kurang = sorted(milik - nama(k))
    print(f"{k:15} {len(milik) - len(kurang)}/{len(milik)}" + (f"  TIDAK: {kurang}" if kurang else ""))
    gagal |= bool(kurang)
for k in ('missingRequirements', 'blocked', 'disabled', 'notInjected'):
    kena = sorted(milik & nama(k))
    if kena:
        print(f"{k:15} {kena}"); gagal = True
print("❌ Ada skill bermasalah di OpenClaw" if gagal else "✅ Semua skill terbaca & siap di OpenClaw")
sys.exit(1 if gagal else 0)
EOF
