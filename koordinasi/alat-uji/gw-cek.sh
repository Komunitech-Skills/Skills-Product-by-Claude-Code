#!/usr/bin/env bash
# Folder scratchpad sesi (wajib): export SCRATCHPAD=/path/ke/scratchpad
SP=${SCRATCHPAD:?isi SCRATCHPAD dengan folder scratchpad sesi}
# Cek gateway OpenClaw; nyalakan ulang bila mati. Tidak mencetak token.
R=$SP/openclaw-real
cd "$R" || { echo "GAGAL: folder $R tidak ada (kontainer baru?)"; exit 2; }
# Gateway produksi memakai instalasi terpisah (lewat oc.sh/oc-tg.sh), bukan /tmp/uji-openclaw.
P=$SP/openclaw-prod
[ -x "$P/node_modules/.bin/openclaw" ] || { echo "GAGAL: instalasi produksi $P tidak ada"; exit 4; }
if pgrep -f "^openclaw-gateway$" >/dev/null; then echo "GATEWAY: HIDUP"; exit 0; fi
[ -n "$bot_token" ] && [ -n "$Ninerouter_key" ] || { echo "GAGAL: env bot_token/Ninerouter_key kosong"; exit 3; }
LOG=gw-$(date +%Y%m%d-%H%M).log
nohup ./oc-tg.sh gateway run --ambient-channels --bind loopback > "$LOG" 2>&1 &
for i in $(seq 1 40); do
  sleep 3
  # OpenClaw >= 2026.10 memulihkan database agent di latar belakang; tunggu 60 detik dan hanya perbaiki bila tidak pulih
  if [ "$i" -gt 20 ] && grep -q "Sessions remain unavailable" "$LOG" && ! grep -q "recovered after background inspection" "$LOG"; then
    # matikan HANYA gateway (PID persis), jangan pkill -f yang bisa mengenai proses penguji
    for p in $(pgrep -f "^openclaw-gateway$"); do kill -TERM "$p"; done; sleep 3
    cp -r home/.openclaw/agents/main/agent "home/.openclaw/agents/main/agent.bak-$(date +%Y%m%d%H%M)"
    timeout 300 ./oc.sh doctor --fix --non-interactive >/dev/null 2>&1
    LOG=gw-$(date +%Y%m%d-%H%M)-fix.log
    nohup ./oc-tg.sh gateway run --ambient-channels --bind loopback > "$LOG" 2>&1 &
  fi
  if grep -q "starting provider (@" "$LOG" && pgrep -f "^openclaw-gateway$" >/dev/null; then echo "GATEWAY: DINYALAKAN ULANG ($LOG)"; exit 0; fi
done
echo "GAGAL: gateway belum siap, lihat $R/$LOG"; exit 1
