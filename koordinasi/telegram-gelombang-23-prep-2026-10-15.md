# Gelombang Telegram 23 — persiapan (BELUM dikirim)

Tugas **C34** (keputusan otomatis **87**). Bot uji pertama `@KTclaude1_bot`, grup uji internal Komunitech.

## Status

| Item | Nilai |
|---|---|
| Skill | `dasbor-lokal`, `audit-seo-toko-online`, `analisis-excel` (6 pesan) |
| Topik | **1578–1583** — `alat-uji/pilot/topik-g23.json` (dibuat 2026-10-15 ~08:32 UTC) |
| Pesan | `alat-uji/pilot/msgs-g23.json` (6 pesan; teks awam, data fiktif) |
| Skill di home bot | Disalin dari repo `/workspace/skills/` 2026-10-15 UTC (G18–G23, 28 folder); backup VM: `$HOME/komunitech-uji/backup-skills-g23-202610150832` |
| Config topik TANPA | `patch-topik.py` → topik 1578, 1580, 1582 = `skills: []` (+ patch ulang G19–G22) — **gateway belum di-restart** (router HTTP 530) |
| Pra-cek `uji-tg.sh` | **Belum** — jalankan sebelum kirim bila router hidup |

## Checklist sebelum kirim (setelah router ≠ 530)

1. Smoke `openclaw agent --local -m "balas satu kata: OK"` → HTTP 200.
2. **Restart gateway** (`gw-cek.sh`) agar patch topik G18–G23 aktif.
3. Selesaikan **G18** (pesan 2–10 `msgs-g18.json`) bila belum.
4. Pra-cek `uji-tg.sh` tiap skill (gagal → catat, ganti calon).
5. Kirim berurutan `kirim-urut2.py` + `msgs-g23.json`; kumpulkan jawaban; nilai TANPA→DENGAN.
6. Tulis `telegram-gelombang-23-<tanggal>.md`; lapor topik 242.

## Urutan gelombang C24

G18 terhenti → G19–G22 prep siap → **G23 prep siap** (C34 selesai untuk persiapan gelombang).
