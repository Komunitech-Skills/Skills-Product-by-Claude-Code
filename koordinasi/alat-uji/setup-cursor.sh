#!/usr/bin/env bash
# setup-cursor.sh — bangun lingkungan uji OpenClaw untuk agent Cursor Cloud (atau sesi baru mana pun).
# Dipanggil dari .cursor/environment.json ("install"). Idempoten: aman dijalankan berulang.
# Rahasia HANYA dari environment variable (Cursor: Settings → Cloud Agents → environment secrets):
#   bot_token       = token bot penguji Telegram (opsional; tanpa ini gateway tidak dijalankan)
#   Ninerouter_key  = kunci router model (wajib untuk uji sebelum/sesudah)
# Skrip ini tidak pernah mencetak nilai keduanya.
set -euo pipefail

REPO="${REPO:-$(cd "$(dirname "$0")/../.." && pwd)}"
BASE="${BASE:-$HOME/komunitech-uji}"          # tempat instalasi; di Cursor VM: /workspace/../komunitech-uji atau $HOME
OC_VERSI="${OC_VERSI:-2026.9.8}"
NODE_VERSI="${NODE_VERSI:-v24.21.0}"
ALAT="$REPO/koordinasi/alat-uji"

mkdir -p "$BASE"
echo "[setup] REPO=$REPO BASE=$BASE openclaw@$OC_VERSI node $NODE_VERSI"

# 1. Node portabel (tidak mengganggu Node sistem)
NODE_DIR="$BASE/node-$NODE_VERSI-linux-x64"
if [ ! -x "$NODE_DIR/bin/node" ]; then
  echo "[setup] unduh Node $NODE_VERSI"
  curl -fsSL "https://nodejs.org/dist/$NODE_VERSI/node-$NODE_VERSI-linux-x64.tar.xz" -o "$BASE/node.tar.xz"
  tar -xJf "$BASE/node.tar.xz" -C "$BASE" && rm -f "$BASE/node.tar.xz"
fi
export PATH="$NODE_DIR/bin:$PATH"

# 2. Dua instalasi OpenClaw terpisah (keputusan pemilik 2026-10-03):
#    openclaw-prod = gateway bot uji; /tmp/uji-openclaw = dipakai scripts/uji_openclaw.sh (uji muat), jangan dicampur.
for D in "$BASE/openclaw-prod"; do
  if [ ! -x "$D/node_modules/.bin/openclaw" ]; then
    echo "[setup] npm install openclaw@$OC_VERSI → $D"
    mkdir -p "$D" && ( cd "$D" && npm init -y >/dev/null 2>&1 && npm install "openclaw@$OC_VERSI" --no-audit --no-fund --silent )
  fi
done

# 3. HOME OpenClaw bot uji dari config tanpa rahasia
R="$BASE/openclaw-real"; H="$R/home/.openclaw"
mkdir -p "$H/skills" "$H/workspace" "$R/homes"
[ -f "$H/openclaw.json" ] || cp "$ALAT/config-bot-uji/openclaw.json" "$H/openclaw.json"
for f in AGENTS.md SOUL.md IDENTITY.md; do [ -f "$H/workspace/$f" ] || cp "$ALAT/config-bot-uji/workspace/$f" "$H/workspace/"; done

# 4. Pembungkus dengan path yang benar (ditulis ulang setiap run)
cat > "$R/oc.sh" <<EOF
#!/usr/bin/env bash
# env bersih; hanya kunci router yang diteruskan (sebagai NINEROUTER_UJI_KEY)
exec env -i HOME=$R/home PATH=$NODE_DIR/bin:/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 TZ=Asia/Jakarta \\
  HTTPS_PROXY="\${HTTPS_PROXY:-}" HTTP_PROXY="\${HTTP_PROXY:-}" NO_PROXY="\${NO_PROXY:-}" \\
  NODE_EXTRA_CA_CERTS="\${NODE_EXTRA_CA_CERTS:-}" SSL_CERT_FILE="\${SSL_CERT_FILE:-}" \\
  NINEROUTER_UJI_KEY="\${Ninerouter_key:-}" \\
  $BASE/openclaw-prod/node_modules/.bin/openclaw "\$@"
EOF
cat > "$R/oc-tg.sh" <<EOF
#!/usr/bin/env bash
# sama dengan oc.sh + token bot (untuk gateway / konteks Telegram)
exec env -i HOME=$R/home PATH=$NODE_DIR/bin:/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 TZ=Asia/Jakarta \\
  HTTPS_PROXY="\${HTTPS_PROXY:-}" HTTP_PROXY="\${HTTP_PROXY:-}" NO_PROXY="\${NO_PROXY:-}" \\
  NODE_EXTRA_CA_CERTS="\${NODE_EXTRA_CA_CERTS:-}" SSL_CERT_FILE="\${SSL_CERT_FILE:-}" \\
  TELEGRAM_BOT_TOKEN="\${bot_token:-}" NINEROUTER_UJI_KEY="\${Ninerouter_key:-}" \\
  $BASE/openclaw-prod/node_modules/.bin/openclaw "\$@"
EOF
chmod +x "$R/oc.sh" "$R/oc-tg.sh"

# 5. Salin alat uji lalu tulis ulang path absolut lama → path baru
for f in gw-cek.sh mk-home.sh uji.sh uji-tg.sh run-uji.sh run-uji-tg.sh; do
  sed -e "s#/tmp/claude-0/-home-user-Skills/d777d314-a309-56aa-81f9-6ad58561dd1c/scratchpad/openclaw-real#$R#g" \
      -e "s#/tmp/claude-0/-home-user-Skills/d777d314-a309-56aa-81f9-6ad58561dd1c/scratchpad/openclaw-prod#$BASE/openclaw-prod#g" \
      -e "s#/home/user/Skills#$REPO#g" \
      -e 's#pkill -TERM -f openclaw-gateway#for p in $(pgrep -f "^openclaw-gateway$"); do kill -TERM "$p"; done#g' \
      "$ALAT/$f" > "$R/$f"
  chmod +x "$R/$f"
done
mkdir -p "$R/pilot" && cp "$ALAT"/brief/*.md "$R/" 2>/dev/null || true
for f in "$ALAT"/pilot/*; do
  sed -e "s#/tmp/claude-0/-home-user-Skills/d777d314-a309-56aa-81f9-6ad58561dd1c/scratchpad/openclaw-real#$R#g" "$f" > "$R/pilot/$(basename "$f")"
done

# 6. Cek
"$R/oc.sh" --version >/dev/null && echo "[setup] openclaw OK: $("$R/oc.sh" --version 2>/dev/null | head -1)"
[ -n "${Ninerouter_key:-}" ] && echo "[setup] Ninerouter_key: ADA" || echo "[setup] Ninerouter_key: KOSONG (uji sebelum/sesudah tidak bisa jalan)"
[ -n "${bot_token:-}" ] && echo "[setup] bot_token: ADA (gateway: bash $R/gw-cek.sh)" || echo "[setup] bot_token: KOSONG (gateway tidak dijalankan)"
echo "[setup] selesai. Alat uji: $R  (mk-home.sh, uji.sh, uji-tg.sh, gw-cek.sh, pilot/)"
