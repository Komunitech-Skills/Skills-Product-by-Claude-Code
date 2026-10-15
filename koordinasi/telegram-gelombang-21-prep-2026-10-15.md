# Gelombang Telegram 21 — persiapan (BELUM dikirim)

Tugas **C34** (keputusan otomatis **87**). Bot uji pertama `@KTclaude1_bot`, grup uji internal Komunitech.

## Status

| Item | Nilai |
|---|---|
| Skill | `studio-video-pendek-ai`, `strategi-harga-produk`, `resi-picking`, `peringatan-dini-operasional`, `gaji-umkm` |
| Topik | **1556–1565** — `alat-uji/pilot/topik-g21.json` (dibuat 2026-10-15 ~07:33 UTC) |
| Pesan | `alat-uji/pilot/msgs-g21.json` (10 pesan; teks dari `examples/01-*.md`, data fiktif) |
| Skill di home bot | Disalin dari repo `/workspace/skills/` 2026-10-15 UTC (G18–G21, 20 folder); backup VM: `$HOME/komunitech-uji/backup-skills-g21-*` |
| Config topik TANPA | `patch-topik.py` → topik 1556, 1558, 1560, 1562, 1564 = `skills: []` — **gateway belum di-restart** (router HTTP 530) |
| Pra-cek `uji-tg.sh` | **Belum** — jalankan sebelum kirim bila router hidup |

## Checklist sebelum kirim (setelah router ≠ 530)

1. Smoke `openclaw agent --local -m "balas satu kata: OK"` → HTTP 200.
2. **Restart gateway** (`gw-cek.sh`) agar patch topik G18–G21 aktif.
3. Selesaikan **G18** (pesan 2–10 `msgs-g18.json`) bila belum.
4. Pra-cek `uji-tg.sh` tiap skill (gagal → catat, ganti calon).
5. Kirim berurutan `kirim-urut2.py` + `msgs-g21.json`; kumpulkan jawaban; nilai TANPA→DENGAN.
6. Tulis `telegram-gelombang-21-<tanggal>.md`; lapor topik 242.

## Urutan gelombang C24

G18 terhenti → G19 prep siap → G20 prep siap → **G21 prep siap** → G22–G23 belum.
