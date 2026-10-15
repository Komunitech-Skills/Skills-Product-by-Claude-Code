# Gelombang Telegram 20 — persiapan (BELUM dikirim)

Tugas **C34** (keputusan otomatis **87**). Bot uji pertama `@KTclaude1_bot`, grup uji internal Komunitech.

## Status

| Item | Nilai |
|---|---|
| Skill | `balas-chat-cs`, `foto-produk-brief`, `sop-writer`, `laporan-insiden-usaha`, `surat-resmi` |
| Topik | **1545–1554** — `alat-uji/pilot/topik-g20.json` (dibuat 2026-10-15 ~07:02 UTC) |
| Pesan | `alat-uji/pilot/msgs-g20.json` (10 pesan; teks dari `examples/01-*.md`, data fiktif) |
| Skill di home bot | Disalin dari repo `/workspace/skills/` 2026-10-15 UTC (G19+G20, 10 folder); backup VM: `$HOME/komunitech-uji/backup-skills-g20-*` |
| Config topik TANPA | `patch-topik.py` → topik 1545, 1547, 1549, 1551, 1553 = `skills: []` — **gateway belum di-restart** (router HTTP 530) |
| Pra-cek `uji-tg.sh` | **Belum** — jalankan sebelum kirim bila router hidup |

## Checklist sebelum kirim (setelah router ≠ 530)

1. Smoke `openclaw agent --local -m "balas satu kata: OK"` → HTTP 200.
2. **Restart gateway** (`gw-cek.sh`) agar patch topik G18–G20 aktif.
3. Selesaikan **G18** (pesan 2–10 `msgs-g18.json`) bila belum.
4. Pra-cek `uji-tg.sh` tiap skill (gagal → catat, ganti calon).
5. Kirim berurutan `kirim-urut2.py` + `msgs-g20.json`; kumpulkan jawaban; nilai TANPA→DENGAN.
6. Tulis `telegram-gelombang-20-<tanggal>.md`; lapor topik 242.

## Urutan gelombang C24

G18 terhenti → G19 prep siap → **G20 prep siap** → G21–G23 belum.
