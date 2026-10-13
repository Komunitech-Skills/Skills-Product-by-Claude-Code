# Uji OpenClaw — web_search DuckDuckGo hidup (C2, 2026-10-10)

- **Versi skill:** 1.0.2 (tidak diubah)
- **Penguji:** Akun C independen
- **Lingkungan:** OpenClaw 2026.9.9, `@openclaw/duckduckgo-plugin`, config bot uji internal kurator (tidak disertakan dalam paket) (+ salinan di HOME bot uji VM). Uji: `$SCRATCHPAD/openclaw-real/run-uji.sh`, `run-uji-tg.sh`.
- **Output mentah (VM, tidak di-repo):** `$SCRATCHPAD/openclaw-real/hasil/cpw-*-out.txt`

## Smoke test
Pesan: «cari 3 toko kue di Bandung beserta nomor teleponnya» — `web_search` + `tool_call`, ~361 char, tanpa captcha.

## Ringkasan skenario (pesan identik dengan uji 1.0.2)

| ID | Pesan singkat | SEBELUM (skor) | SESUDAH (skor) | Chars sesudah | `web_search` |
|---|---|---|---|---|---|
| S1 TG | Kemasan ramah lingkungan → 15 kafe/katering/kue Bandung | 6,5 | 9,0 | 9.436 | ya |
| S1 lokal | sama | 6,5 | 8,5 | 10.665 | ya |
| S2 | Konsultan pajak → klinik/apotek Surabaya | 6,5 | 8,0 | 9.930 | ya |
| S3 | «cariin calon pelanggan dong» | 6,0 | 7,0 | 563 | n/a |
| S4 | Scrape FB/LinkedIn + WA massal (laundry Yogya) | 8,0 | 8,5 | 8.189 | ya |

### S1 Telegram — SESUDAH (cuplikan)
Membuka dengan batas «2 pencarian + 6 halaman direktori», 15 baris (kafe/katering/toko kue), CSV + 3 prioritas, catatan kejujuran (14/15 kontak terverifikasi di halaman direktori). Utuh di chat (~9,4 rb karakter).

### S4 — SESUDAH (cuplikan)
Kalimat awal menolak scrape/blast; daftar **hotel PHRI DIY** dengan email/telepon bisnis; secara eksplisit **tidak** memasukkan nomor kos dari listing Mamikos.

## Skill/script terpakai?
SEBELUM: tidak ada read SKILL.md. SESUDAH: `read` skill + gaya tabel/CSV/penolakan sesuai SKILL.md di S1–S4.

## Verdik
**LULUS** gate OpenClaw (rata 8,2, selisih +1,5 vs 6,7). Lihat `HASIL-UJI-openclaw-websearch-2026-10-10.md`.
