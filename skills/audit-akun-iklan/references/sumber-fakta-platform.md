# Sumber Fakta Platform (diverifikasi untuk v1.0.1)

Fakta platform di `scripts/daftar_cek.csv` yang **bukan** patokan Komunitech, beserta sumbernya.
Tanggal akses: **2026-09-26**. Menu & kebijakan platform sering berubah; cek ulang sebelum rilis
berikutnya dan perbarui tabel ini.

| Cek | Fakta yang dipakai | Sumber resmi | Catatan verifikasi |
|---|---|---|---|
| M08 | Meta kini hanya menyasar "orang yang tinggal di atau baru-baru ini berada di" lokasi; pilihan "tinggal di" saja / "bepergian" sudah dihapus | https://www.facebook.com/business/help/365561350785642 (Use Location Targeting), https://www.facebook.com/business/help/202297959811696 (About location targeting) | Halaman resmi Meta tidak bisa dibaca otomatis (butuh render/login), dan cuplikan mesin pencari masih menampilkan teks lama. Perubahan dikonfirmasi sumber sekunder: https://searchengineland.com/new-update-to-meta-ads-location-targeting-404124 , https://www.jonloomer.com/big-change-to-meta-ads-location-targeting/ . **PERLU cek manual di Ads Manager oleh pemilik/tim** saat uji platform asli. |
| M22 | Deduplikasi pixel + Conversions API memakai `event_id` dan `event_name` yang sama, dalam 48 jam sejak event pertama | https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events/ | Dibaca langsung. Halaman ringkasan CAPI (https://www.facebook.com/business/help/AboutConversionsAPI) tidak bisa dibaca otomatis; karena itu M22 berbobot **tinggi**, bukan kritis, dan tidak diklaim "wajib". |
| T18 | TikTok menyarankan Events API bersama Pixel untuk website, dengan deduplikasi `event_id` (jendela 48 jam) | https://ads.tiktok.com/help/article/events-api , https://ads.tiktok.com/help/article/event-deduplication?lang=en | Dibaca langsung: "For website connections, we recommend having an Events API integration with your existing Pixel integration". |
| T08 | Anggaran harian ad group minimal 10x CPA rata-rata 7 hari (Maximum Delivery) atau 10x CPA bid (Target Cost per Result) | https://ads.tiktok.com/help/article/best-practices-for-bidding-strategies?lang=en | Dibaca langsung. v1.0.0 menulis "20x" — dikoreksi. Halaman Learning Phase menyebut volatilitas turun setelah ±25 hasil atau 7 hari: https://ads.tiktok.com/help/article/learning-phase?lang=en |
| G15, G16 | Performance Max mendukung kata kunci negatif tingkat kampanye dan daftar kata kunci negatif; berlaku untuk inventaris Penelusuran & Shopping; kata kunci negatif tingkat akun ikut berlaku ke PMax | https://support.google.com/google-ads/answer/15726455?hl=en , https://support.google.com/google-ads/answer/11396330?hl=en | Dibaca langsung. Batas 10.000 per kampanye disebut di https://support.google.com/google-ads/answer/16451273?hl=en (belum dibaca penuh). |
| S04 | Shopee Indonesia memakai istilah GMV Max Auto / GMV Max ROAS; disarankan tidak sering mengubah target ROAS saat fase belajar | https://iklan.shopee.co.id/learn/faq/549/1746 , https://iklan.shopee.co.id/learn/faq/57/2031 | Diambil dari laporan penguji independen (HASIL-UJI.md v1.0.0); belum dibaca ulang oleh pembuat. |
| TS11 | GMV Max punya pengecualian materi massal; TikTok memperingatkan pengecualian bisa menurunkan performa | https://ads.tiktok.com/help/article/about-bulk-creative-exclusion-filters-for-product-gmv-max?lang=en | Diambil dari laporan penguji independen; belum dibaca ulang oleh pembuat. |

Angka lain di daftar cek (frekuensi ≤ 3/6, CTR turun > 30%, jam ramai 19–22, 5 video, 4 sitelink,
selisih event ≤ 30%) adalah **patokan awal Komunitech** dan ditulis begitu di kolom `lulus_jika`.
