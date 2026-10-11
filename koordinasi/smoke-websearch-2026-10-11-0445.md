# Smoke `web_search` — VM Cursor 2026-10-11 ~04:45 UTC

Run otomasi Akun C (`cursor/iterasi-otomatis-akun-c-0445`). Tindak lanjut run 03:45: plugin DDG gagal di OpenClaw 2026.9.x (API plugin ≥2026.10.1).

## Lingkungan

- OpenClaw prod dinaikkan ke **2026.10.1** (`npm install openclaw@2026.10.1` di `$BASE/openclaw-prod`).
- Plugin **@openclaw/duckduckgo-plugin@2026.10.1** terpasang ke `$HOME/.openclaw/extensions/duckduckgo` (via `openclaw plugins install`).
- `mk-home.sh` menyalin folder `extensions/` ke HOME uji (wajib agar `web_search` hidup di `run-uji.sh`).
- Config: `tools.web.search.provider=duckduckgo`, `plugins.entries.duckduckgo.enabled=true` (repo: `koordinasi/alat-uji/config-bot-uji/openclaw.json`).

## Hasil satu giliran

- Perintah: cari 3 toko kue Bandung + nomor telepon; wajib `web_search`.
- **Tools terpanggil:** `tool_search`, **`web_search`**, `tool_call` (bukan hanya `web_fetch`).
- Provider log: duckduckgo.
- Output tersimpan VM: `$SCRATCHPAD/openclaw-real/hasil/smoke-ws-s1.txt` (337 karakter; 2 nomor telepon + 1 tanpa nomor di cuplikan).

## Catatan

- Peringatan plugin "record-missing" saat load dari HOME hasil `cp -a extensions` — aman untuk uji; instal resmi via `plugins install` di HOME prod sudah dilakukan.
- Default `OC_VERSI` di `setup-cursor.sh` diperbarui ke **2026.10.1** agar VM baru langsung memenuhi syarat plugin.

## Verdik smoke

**LOLOS** — `web_search` hidup; uji penuh `cari-prospek-web` v1.0.2 tetap mengacu commit `9d97e53b` (6,7→8,2 LULUS).
