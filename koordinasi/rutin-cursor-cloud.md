# Rutin Cursor Cloud (Akun C)

Ringkasan eksekusi per run otomasi/cron. Detail penuh: `AGENTS.md`, `.cursor/CLOUD.md`, `CLAUDE.md`, prompt di `koordinasi/rutin.md` (bagian Akun C).

## Urutan wajib

1. `git fetch origin` — base `claude/claude-code-cli-differences-btizz5`
2. Baca `papan-tugas.md` (Akun C, SERAH TERIMA, Permintaan antar-akun) + `automation-progress-akun-c.md`
3. Branch `cursor/<tugas>-8b42` (satu tugas = satu branch)
4. Secret: `Ninerouter_key`, `bot_token`, `tester_bot_token` (jangan cetak)
5. Uji: `$HOME/komunitech-uji/openclaw-real/` — `mk-home.sh`, `run-uji.sh` / `run-uji-tg.sh` bila `unshare` gagal
6. Sebelum commit: `python3 scripts/validate.py`
7. Setelah uji: **push segera** → perbarui log di `automation-progress-akun-c.md` → Telegram 242
8. Laporan: `reports/YYYY-MM-DD-akun-c.md`

## Pembuat ≠ penguji

Satu run hanya (A) skill/catalog **atau** (B) `examples/` + skor — tidak keduanya untuk skill yang sama.
