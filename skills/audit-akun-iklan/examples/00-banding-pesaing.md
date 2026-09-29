# Banding pesaing (penguji independen, Akun B)

> 2026-09-26. Pesaing **hanya dibaca untuk dinilai**, tidak disalin, script pesaing tidak dijalankan.
> Skenario: normal 1 (skincare TikTok Ads + TikTok Shop). Penilaian skenario pesaing = simulasi
> berdasarkan isi skill/referensinya.

## Kandidat yang dicari
Kata kunci: "ads audit skill", "ad account audit claude", "PPC audit skill", "Shopee ads audit",
"TikTok Shop GMV Max audit" (GitHub search, web). Tidak ditemukan skill publik untuk Shopee Ads /
TikTok Shop / pasar Indonesia.

| Pesaing | Sumber | Lisensi | Sinyal |
|---|---|---|---|
| **claude-ads** (AgriciDaniel) — sumber kurasi | github.com/AgriciDaniel/claude-ads, commit `ac21644` (2026-09-11) | MIT | ±9,6 rb bintang, ±1,4 rb fork, dibuat Feb 2026, 124 commit |
| claude-ads fork (Hainrixz / tododeia) | github.com/Hainrixz/claude-ads | MIT | 91 bintang; fokus Meta/Google/TikTok, ±161 cek, nilai huruf A–F |
| google-ads-skills (itallstartedwithaidea) | github.com/itallstartedwithaidea/google-ads-skills | Apache-2.0 | 38 bintang; Google saja; sudah deprecated, pindah repo |

## Penilaian skenario 1 (1–5 per aspek)
| Aspek | audit-akun-iklan (kita) | claude-ads asli | fork Hainrixz |
|---|---|---|---|
| Bisa dipakai awam tanpa setup | **5** – Python standar, tanpa API | 2 – installer, Python 3.10+, dependensi (requests, Playwright, dll.), run manifest/JSON bundle | 2 – serupa, OAuth opsional |
| Cakupan TikTok Shop GMV Max | **4** – 11 cek TS + ROI impas incl. afiliasi | 2 – hanya label "GMV Max for Shop campaigns" (tanpa kriteria) | 2 |
| Shopee / Tokopedia / klik-ke-WA | **5** | 0 | 0 |
| Kriteria lulus/gagal konkret | **4** – tiap cek punya kriteria + bukti + perbaikan | 2 – sengaja tanpa ambang ("do not use fixed thresholds"), agent harus cari sumber resmi saat jalan | 3 – ambang lebih banyak, bahasa Inggris |
| Ketelitian terhadap fakta usang | 3 – nama menu diberi tanggal & "bisa berubah"; beberapa saran usang (lokasi Meta) | **5** – desain source-grounded, klaim wajib bertanggal | 3 |
| Pelacakan web (CAPI, dedup, EMQ, verifikasi domain) | 2 – tidak ada cek CAPI/dedup | **5** – M02–M08 khusus | 4 |
| Ruang lingkup platform | 3 – 5 platform | **5** – 12 platform | 4 |
| Bahasa Indonesia, Rupiah, contoh lokal | **5** | 0 | 0 |
| Metode skor deterministik & cakupan bukti | 5 (diadaptasi + status `sebagian`, prioritas, rencana 7 hari) | 5 | 4 (nilai huruf) |
| **Total (maks 45)** | **36** | 26 | 22 |

## Kesimpulan
Untuk pembeli target (UMKM/agensi kecil Indonesia, awam, tanpa API) skill kita **menang jelas**.
claude-ads unggul di dua hal yang layak dipelajari (ditulis ulang dengan cara sendiri, bukan disalin):
1. **Pelacakan server-side**: cek Conversions API / deduplikasi event / kualitas pencocokan untuk
   penjual yang beriklan ke website (Shopify/WooCommerce sudah punya integrasi CAPI satu klik).
2. **Disiplin kesegaran fakta**: setiap klaim menu/fitur platform diberi tanggal sumber resmi;
   contoh temuan kita — pilihan lokasi "tinggal di" Meta sudah dihapus; Performance Max kini punya
   kata kunci negatif & laporan istilah penelusuran (2025).
