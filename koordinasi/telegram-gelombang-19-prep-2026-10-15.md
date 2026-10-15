# Gelombang Telegram 19 — persiapan (BELUM dikirim)

Tugas **C34** (keputusan otomatis **87**). Bot uji pertama `@KTclaude1_bot`, grup uji internal Komunitech.

## Status

| Item | Nilai |
|---|---|
| Skill | `surat-penawaran-harga`, `presentasi-instan`, `positioning-persona-usaha`, `cv-lamaran-ats`, `audit-akun-iklan` |
| Topik | **1534–1543** — `alat-uji/pilot/topik-g19.json` (dibuat 2026-10-15 ~06:32 UTC) |
| Pesan | `alat-uji/pilot/msgs-g19.json` (10 pesan; teks dari `examples/01-*.md`, data fiktif) |
| Skill di home bot | Disalin dari repo `/workspace/skills/` 2026-10-15 UTC; backup VM: `$HOME/komunitech-uji/backup-skills-g19-*` |
| Config topik TANPA | `patch-topik.py` → topik 1534, 1536, 1538, 1540, 1542 = `skills: []` — **gateway belum di-restart** (router HTTP 530) |
| Pra-cek `uji-tg.sh` | **Belum** — jalankan sebelum kirim bila router hidup |

## Checklist sebelum kirim (setelah router ≠ 530)

1. Smoke `openclaw agent --local -m "balas satu kata: OK"` → HTTP 200.
2. **Restart gateway** (`gw-cek.sh`) agar patch topik G19 aktif.
3. Pra-cek `uji-tg.sh` tiap skill (gagal → catat, ganti calon).
4. Kirim berurutan `kirim-urut2.py` + `msgs-g19.json`; kumpulkan jawaban; nilai TANPA→DENGAN.
5. Tulis `telegram-gelombang-19-<tanggal>.md`; lapor topik 242.

## Urutan gelombang C24

G18 masih terhenti (pesan 2–10 `msgs-g18.json` belum terkirim). Setelah router hidup: **G18 dulu** → lalu kirim G19 (prep ini).
