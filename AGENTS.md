# AGENTS.md — aturan untuk agent selain Claude Code (Cursor Cloud, Codex, dll.)

**Sumber kebenaran aturan kerja repo ini adalah `CLAUDE.md`.** Baca seluruhnya di awal setiap sesi dan patuhi seperti instruksi pemilik: misi, prinsip "instan tapi powerful & reliable", platform target, struktur repo, Tahap 1–8, aturan lisensi, audit keamanan, standar format SKILL.md (frontmatter hanya `name` + `description`), standar pembulatan, dan semua "Keputusan pemilik" bertanggal. File ini hanya menambahkan hal yang khusus untuk agent non-Claude.

## Cursor Cloud Agent

**Urutan baca:** (1) `AGENTS.md` → (2) [`.cursor/CLOUD.md`](.cursor/CLOUD.md) → (3) `CLAUDE.md` saat mengerjakan skill. Detail bootstrap VM, branch `cursor/*-8b42`, OpenClaw di `$HOME/komunitech-uji`, rahasia, Telegram, dan checklist commit ada di **CLOUD.md** — jangan duplikasi panjang di sini.

## Peranmu: "Akun C"
- Pembagian kerja ada di `koordinasi/papan-tugas.md` (bagian "Pembagian jalur", "SERAH TERIMA Akun B → Akun A", dan "Aturan untuk Akun C"). Ambil hanya tugas yang ditandai untukmu atau yang diminta pemilik di prompt. Jangan menyentuh folder `skills/<nama>` di luar tugasmu.
- Satu tugas = satu branch `cursor/<nama>-8b42` dari base `claude/claude-code-cli-differences-btizz5`. Jangan merge sendiri. Commit mengikuti pola `skill: <nama> (<status>)`, `uji: <nama> vX.Y.Z <skor>/10`, `riset: ...`, `docs: ...`.
- Selesaikan dan **commit + push sebelum run berakhir** (wajib setelah uji/testing): VM Cursor ulang dari snapshot, semua yang tidak di-commit hilang. **Jangan buat PR** otomatis — PR hanya bila pemilik secara eksplisit meminta (detail: `.cursor/CLOUD.md`).
- Tulis laporan sesi di `reports/YYYY-MM-DD-akun-c.md` (format di CLAUDE.md bagian 6).

## Pembuat ≠ penguji
Satu sesi agent tidak boleh membuat sekaligus menguji skill yang sama. Pembuat menulis SKILL.md/script/tes/README dan menaikkan status ke `uji`; penguji (sesi/agent lain) menulis `examples/00-openclaw-sebelum-sesudah.md`, `01–04`, `HASIL-UJI.md`, skor, dan verdik. Tulis ulang bersih (sumber domain publik/proprietary): sesi yang membaca sumber hanya menulis daftar ide ke `research/sources/`; sesi lain yang tidak membaca sumber menulis skill-nya. Brief standar: `koordinasi/alat-uji/brief/`.

## Lingkungan uji OpenClaw
`.cursor/environment.json` menjalankan `koordinasi/alat-uji/setup-cursor.sh` saat run dimulai: OpenClaw terpasang di `$HOME/komunitech-uji/openclaw-prod`, alat uji di `$HOME/komunitech-uji/openclaw-real/` (`mk-home.sh`, `uji.sh`, `uji-tg.sh`, `gw-cek.sh`, `pilot/tg.py`). Cara pakai dan acuan LULUS (sesudah ≥ 8 **dan** selisih ≥ 1,5) ada di `koordinasi/alat-uji/README.md` dan `brief/tester-umum.md`. `scripts/uji_openclaw.sh` memakai instalasi terpisah `/tmp/uji-openclaw`; jangan arahkan ke `openclaw-prod`. Bot produksi (VPS pemilik) tidak pernah dipakai untuk uji.

## Rahasia
`Ninerouter_key` (router model) dan `bot_token` (bot penguji Telegram) hanya ada sebagai environment variable. Jangan pernah mencetak, menyalin ke file, menaruh di commit/PR/log, atau menanyakannya ke pemilik. Jika ada token tertempel di chat, jangan ulangi satu karakter pun. Satu token bot hanya boleh dipakai satu gateway; nyalakan gateway hanya lewat `gw-cek.sh`, matikan hanya per PID (`pgrep -f "^openclaw-gateway$"`), tidak pernah `pkill -f`.

## Telegram
Laporan hasil uji dan hal yang butuh keputusan pemilik dikirim ke grup uji topik "Ringkasan uji" (`chat_id -1004407409583`, `message_thread_id 242`) lewat `pilot/tg.py`, diawali `@nikioktarian`, format di CLAUDE.md (keputusan 2026-10-03). Nomor keputusan dilanjutkan dari yang terakhir di `koordinasi/`/`reports/`. Gelombang tampilan: hanya setelah pemilik setuju, maks 10 pesan, berurutan dengan jeda, tanpa balas-otomatis, topik baru, pra-cek `uji-tg.sh` wajib, restart gateway setelah mengubah `channels.*`.

## Sebelum setiap commit
`python3 scripts/validate.py` harus lolos; tes regresi skill lolos; tidak ada `dist/`, data pribadi member/pembeli, atau identitas model di commit/PR; `rm -rf` hanya dengan `"${VAR:?}"`.
