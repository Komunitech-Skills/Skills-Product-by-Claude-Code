# Uji ulang parsial — `web_search` hidup (C2)

- **Tanggal:** 2026-10-10
- **Penguji:** Akun C (independen)
- **Versi skill:** 1.0.2 (SKILL.md tidak diubah)
- **Perubahan lingkungan:** OpenClaw **2026.9.9**, plugin `@openclaw/duckduckgo-plugin`, `tools.web.search.provider: duckduckgo` (tanpa kunci API). Uji via `run-uji.sh` (VM Cursor, tanpa `unshare`).
- **Smoke test:** pesan "cari 3 toko kue di Bandung…" → `web_search` terpanggil, 3 nomor/entri (2 terverifikasi + 1 tanpa nomor di sumber).

## Skenario 1 lokal (kemasan ramah lingkungan → kafe/katering/toko kue Bandung)

Pesan identik dengan uji 1.0.2 (`00-openclaw-sebelum-sesudah.md`).

| Sisi | Durasi | `web_search` | Karakter | Ringkas |
|---|---|---|---|---|
| SEBELUM | ~2,3 mnt | ya | 4.254 | 15 calon, banyak rujuk situs usaha langsung (di luar aturan skill) |
| SESUDAH | ~2,4 mnt | ya | 6.988 | 8 baris terverifikasi direktori saja, jujur belum 15, CSV + prioritas |

**Skor sementara (1 skenario):** SEBELUM 6,5 / SESUDAH **8,5** — skill lebih patuh batas direktori & kejujuran baris.

## Verdik parsial (diperbarui)

**Infrastruktur C2: SELESAI.** Uji penuh 4 skenario + S1 Telegram selesai run **2026-10-10 ~18:04 UTC** → **LULUS** 6,7→8,2 (+1,5). Detail: `09-openclaw-websearch-hidup-2026-10-10.md`, `HASIL-UJI-openclaw-websearch-2026-10-10.md`.

## Output mentah (VM uji, tidak di-repo)

- `$SCRATCHPAD/openclaw-real/hasil/cpw-s1-b1-01.txt`
- `$SCRATCHPAD/openclaw-real/hasil/cpw-s1-s1-01.txt`
