# Telegram group test setup — operator notes (2026-09-29)

Gateway: OpenClaw 2026.9.6, HOME=openclaw-real/home, started detached:
`cd openclaw-real && nohup ./oc-tg.sh gateway run --ambient-channels --bind loopback > gw3.log 2>&1 &`

## What changed
1. **Skills installed**: all 109 skills in catalog.csv that have a SKILL.md (all statuses except ditolak/arsip)
   copied from /home/user/Skills/skills/ to home/.openclaw/skills/ (previously only 10).
   Not installed: listmonk-newsletter, fider-masukan-pelanggan (no SKILL.md, not in catalog).
   Backup of the old dir: openclaw-real/skills-backup-before-all/
2. **Config** (home/.openclaw/openclaw.json; backup: openclaw-real/openclaw.json.before-group-open):
   - `channels.telegram.groups["-1004407409583"]`: removed `allowFrom:["1538336036"]`,
     added `groupPolicy:"open"` (all members), `requireMention:true` (for everyone, incl. owner:
     OpenClaw has no per-sender requireMention setting). Top-level `groupPolicy` stays `allowlist`,
     so other groups remain blocked. DM/owner settings unchanged.
   - `skills.limits.maxSkillsPromptChars: 110000` (default 18000 would drop descriptions of 109 skills).
3. **Topics**: 89 new forum topics "🧪 <skill>" with an intro message each (tg-topics.json updated;
   backup tg-topics.before-all.json). Script: openclaw-real/topics3.py, log: topics3.log.
   Announcement posted in General.
4. **Sandbox: NOT enabled** (owner decision: group = trusted team). Tools run on the host.

## Risk (accepted by owner)
Any group member who mentions the bot can make the agent run exec/read/write on this host with the
gateway's env (it contains the Telegram bot token and router key) and read files outside the workspace.
If the group gets untrusted members, enable the sandbox or deny tools (below).

## Enable sandbox later (ready: image openclaw-sandbox:bookworm-slim exists, has python3 3.11)
Add to openclaw.json, then restart the gateway:
```json
"agents": { "defaults": { "sandbox": { "mode": "non-main", "scope": "session", "workspaceAccess": "none" } } }
```
(Docker defaults: network none, read-only root, capDrop ALL; skills are mirrored read-only into the sandbox.)
Check with `./oc.sh sandbox explain`. Alternative without Docker: group tools deny
`channels.telegram.groups["-1004407409583"].tools.deny = ["group:runtime","group:fs","group:automation"]`.

## Revert
```bash
R=openclaw-real
cp -p $R/openclaw.json.before-group-open $R/home/.openclaw/openclaw.json   # owner-only, requireMention false
rm -rf $R/home/.openclaw/skills && cp -a $R/skills-backup-before-all $R/home/.openclaw/skills
pkill -TERM -f openclaw-gateway; cd $R && nohup ./oc-tg.sh gateway run --ambient-channels --bind loopback > gw3.log 2>&1 &
```
Topics can be deleted with Bot API deleteForumTopic (IDs in tg-topics.json; old map in tg-topics.before-all.json).

## Instalasi OpenClaw produksi terpisah (2026-10-03)
- Gateway bot Telegram produksi kini jalan dari `$S/openclaw-prod/` (node_modules + node-v24.21.0, OpenClaw 2026.9.8 fc23bc8, disalin `cp -a` dari /tmp/uji-openclaw).
- Dipakai oleh: `openclaw-real/oc.sh`, `oc-tg.sh` (dan karena itu `gw-cek.sh`, `run.sh`). Cadangan versi lama: `*.bak-20261003`.
- `/tmp/uji-openclaw` tetap milik alat uji (`scripts/uji_openclaw.sh`, `uji.sh`, `mk-home.sh`). Sebab dipisah: npm install versi baru di sana memicu gateway restart (SIGUSR2 installation_replaced) lalu gagal karena modul hilang.
- JANGAN pakai openclaw-prod untuk uji / jangan arahkan skrip uji ke sana.
- Upgrade sengaja: backup dulu (`cp -a openclaw-prod openclaw-prod.bak-TGL`), lalu
  `PATH=$S/openclaw-prod/node-v24.21.0-linux-x64/bin:$PATH npm install --prefix $S/openclaw-prod openclaw@<versi> --no-audit --no-fund`;
  gateway akan restart sendiri (installation_replaced) — bila tidak pulih, kill PID gateway (`pgrep -x openclaw-gateway`, jangan pkill -f) lalu `bash openclaw-real/gw-cek.sh`, cek log "polling ingress started".
- Uji keterpisahan 2026-10-03: uji_openclaw.sh diganti ke 2026.9.7 lalu kembali 2026.9.8 → gateway PID sama, tidak ada installation_replaced di log.

## 2026-10-06 — Pelajaran gelombang 11
Setelah ubah `channels.telegram.*` (topik/skills per topik) di openclaw.json, hot reload membuat semua balasan ditolak ("PlatformMessageNotDispatchedError: The reply channel changed"). Solusi: hentikan gateway dengan PID tepat (`pgrep -f "^openclaw-gateway$"` → `kill -TERM <pid>`), lalu `gw-cek.sh` untuk menyalakan ulang. Lakukan SEBELUM mengirim gelombang.

## 2026-10-10 — Gateway bot uji pindah ke agent Cursor Cloud (keputusan pemilik)
- Pemilik memilih memakai bot penguji LAMA (@KTclaude1_bot) di VM Cursor. Gateway di sesi Akun B dipastikan MATI (tidak ada proses `openclaw-gateway`; proses terakhir mati sendiri setelah kontainer idle, log terakhir gw-20261006-1227.log) dan routine Akun B dijeda sehingga `gw-cek.sh` tidak menyalakannya lagi.
- Aturan: hanya SATU gateway per token bot. Selama Cursor memegang `bot_token`, sesi Akun A/B tidak boleh menjalankan `gw-cek.sh`/`oc-tg.sh gateway run`. Bila pekerjaan dikembalikan ke Claude Code, hapus dulu secret `bot_token` di Cursor.
- Di Cursor: `bash $HOME/komunitech-uji/openclaw-real/gw-cek.sh` menyalakan gateway tiap run (VM ulang dari snapshot, gateway tidak bertahan antar run).
