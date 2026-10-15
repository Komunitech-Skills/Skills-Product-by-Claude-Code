# Gelombang Telegram 22 — persiapan (BELUM dikirim)

Tugas **C34** (keputusan otomatis **87**). Bot uji pertama `@KTclaude1_bot`, grup uji internal Komunitech.

## Status

| Item | Nilai |
|---|---|
| Skill | `copy-landing-page`, `analisis-rasio-keuangan-usaha`, `tagih-piutang`, `tender-checklist`, `follow-up-prospek` |
| Topik | **1567–1576** — `alat-uji/pilot/topik-g22.json` (dibuat 2026-10-15 ~08:08 UTC) |
| Pesan | `alat-uji/pilot/msgs-g22.json` (10 pesan; teks dari `examples/01-*.md`, data fiktif) |
| Skill di home bot | Disalin dari repo `/workspace/skills/` 2026-10-15 UTC (G18–G22, 25 folder); backup VM: `$HOME/komunitech-uji/backup-skills-g22-*` |
| Config topik TANPA | `patch-topik.py` → topik 1567, 1569, 1571, 1573, 1575 = `skills: []` — **gateway belum di-restart** (router HTTP 530) |
| Pra-cek `uji-tg.sh` | **Belum** — jalankan sebelum kirim bila router hidup |

## Checklist sebelum kirim (setelah router ≠ 530)

1. Smoke `openclaw agent --local -m "balas satu kata: OK"` → HTTP 200.
2. **Restart gateway** (`gw-cek.sh`) agar patch topik G18–G22 aktif.
3. Selesaikan **G18** (pesan 2–10 `msgs-g18.json`) bila belum.
4. Pra-cek `uji-tg.sh` tiap skill (gagal → catat, ganti calon).
5. Kirim berurutan `kirim-urut2.py` + `msgs-g22.json`; kumpulkan jawaban; nilai TANPA→DENGAN.
6. Tulis `telegram-gelombang-22-<tanggal>.md`; lapor topik 242.

## Urutan gelombang C24

G18 terhenti → G19 prep siap → G20 prep siap → G21 prep siap → **G22 prep siap** → G23 belum.
