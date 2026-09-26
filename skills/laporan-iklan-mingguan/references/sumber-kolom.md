# Sumber nama kolom ekspor iklan per platform

Dicatat sesuai Tahap 2 `CLAUDE.md`: nama kolom yang dipakai `scripts/laporan_iklan.py` untuk
mendeteksi platform & metrik **harus** berasal dari dokumentasi resmi atau contoh ekspor nyata,
bukan tebakan. Semua sumber di bawah diakses **25 September 2026**.

Nama kolom ekspor bisa berubah sewaktu-waktu (platform iklan sering mengubah UI). Skill ini tidak
bergantung mutlak pada nama persis: bila deteksi otomatis gagal, pengguna/agent bisa memberi nama
kolom manual lewat `--kolom-biaya`, `--kolom-tayangan`, `--kolom-klik`, `--kolom-hasil`,
`--kolom-nilai-hasil` (lihat SKILL.md).

## Status verifikasi (v1.0.1, 26 September 2026)

| Platform | Nama kolom | Bentuk ekspor (baris judul, baris total, sel kosong) | Status |
|---|---|---|---|
| Meta Ads | Ringkasan pencarian halaman resmi + 2 sumber pihak ketiga | Sel `Results` kosong untuk iklan tanpa hasil: dari pengalaman penguji, **belum dicocokkan dengan ekspor asli** | **BELUM TERVERIFIKASI dari ekspor asli (PERLU REVIEW)** |
| Meta Ads (UI Bahasa Indonesia) | `Jumlah yang dibelanjakan`, `Klik tautan`, `Hasil`, `Impresi` ditambahkan sebagai sinonim | Tebakan terjemahan, belum dilihat di ekspor asli | **BELUM TERVERIFIKASI (PERLU REVIEW)** |
| TikTok Ads Manager | Halaman resmi hanya menyebut CPM/CPC/CTR/CVR; `Clicks (destination)`, `Total onsite value`, `Currency` dari sumber pihak ketiga | Belum dilihat di ekspor asli | **Sebagian terverifikasi** |
| Shopee Ads | Definisi metrik dari Pusat Edukasi Penjual (resmi) | Baris info toko di atas tabel & baris Total: dari pengalaman penguji | **Nama metrik resmi; bentuk file belum diverifikasi** |
| TikTok Shop Ads | Halaman bantuan resmi (Bahasa Indonesia) | Belum dilihat di ekspor asli | **Nama metrik resmi; bentuk file belum diverifikasi** |
| Google Ads | Google Ads Help (resmi), termasuk `Results`/`Results value` | Baris judul "Campaign report" + periode, `Campaign status`, `Avg. cost`, `Total: Account/Search/...`, `Currency code`, CSV UTF-16 bertab: dari pengetahuan penguji, **belum dicocokkan dengan unduhan asli** | **Nama kolom resmi; bentuk file belum diverifikasi** |

Karena belum semua terverifikasi dari file asli, script v1.0.1 **tidak bergantung** pada satu
bentuk saja: pencarian baris header dalam 15 baris pertama, baris total dikenali dari teks di
kolom mana pun dan dari angka (= jumlah baris lain), sel kosong dihitung 0 dengan catatan, dan
setiap laporan mencetak "Kolom dibaca: ..." agar kesalahan pemetaan langsung terlihat.
**Rekomendasi untuk pemilik:** sediakan satu ekspor asli per platform (angka boleh disamarkan)
untuk dijadikan tes regresi sebelum status `rilis`.

## Meta Ads Manager (Facebook/Instagram)

Kolom ekspor umum (preset "Performance" / kolom yang bisa ditambah manual): `Campaign name`,
`Ad set name`, `Ad name`, `Amount spent` (dengan label mata uang, mis. `Amount spent (IDR)`),
`Impressions`, `Reach`, `Frequency`, `Link clicks`, `CPC (cost per link click)`,
`CPM (cost per 1,000 impressions)`, `CTR (link click-through rate)`, `Results`,
`Cost per results`, `Purchases`, `Purchase conversion value`,
`Website purchase ROAS (return on ad spend)`.

- Sumber: Meta Business Help Center, "Customize Columns in Ads Manager"
  (https://www.facebook.com/business/help/1452248935049010) dan "Columns in the Import/Export
  Template in Ads Manager" (https://www.facebook.com/business/help/1471948569691450) — daftar
  metrik dikonfirmasi lewat ringkasan pencarian (halaman penuh memerlukan JavaScript/login), serta
  dicocokkan dengan ringkasan pihak ketiga yang mengutip nama kolom yang sama: Metricool Help
  Center (https://help.metricool.com/meta-ads-metrics-ahrw9) dan clariBI
  (https://claribi.com/knowledge-base/how-to-export-csv-data-from-meta-ads-manager-and-import-it-into-claribi/).
- Catatan: kolom biaya/CPC/CPM biasanya diberi akhiran `(IDR)` mengikuti mata uang akun iklan —
  dipakai skill ini untuk deteksi mata uang (lihat "Mata uang" di bawah).

## TikTok Ads Manager (iklan global, `ads.tiktok.com`)

Kolom umum: `Campaign name`, `Cost`, `Impressions`, `Clicks (destination)`, `CPC (destination)`,
`CPM`, `CTR (destination)`, `Conversion`, `Cost per conversion`, `Total onsite value`,
`Complete Payment ROAS`.

- Sumber: TikTok Ads Manager Help Center, "Create and Manage Reports"
  (https://ads.tiktok.com/help/article/create-manage-reports) — daftar dimensi/metrik laporan
  kustom; dicocokkan dengan ringkasan Coinis "Export TikTok Ads Report: Step-by-Step Guide"
  (https://coinis.com/how-to/export-tiktok-ads-report) dan Improvado "TikTok Ads Dashboard Guide"
  (https://improvado.io/blog/tiktok-ads-dashboard) yang mengutip kolom dasbor default (Campaign
  Name, Status, Budget, Spend, Impressions, Clicks, CTR, CPC, Conversions, CPA, Cost per Result,
  ROAS).

## Shopee Ads (Iklan Shopee, Seller Center Indonesia)

Kolom Bahasa Indonesia: `Dilihat` (tayangan), `Klik`, `Konversi (Langsung)`,
`Rasio Konversi (Langsung)`, `Biaya`, `Biaya per Konversi (Langsung)`,
`Omzet Penjualan (Langsung)`, `ACOS (Langsung)`.

- Sumber: Pusat Edukasi Penjual Shopee, "Mengevaluasi Performa Iklan Shopee"
  (https://seller.shopee.co.id/edu/article/17525) dan "Memantau Performa Iklan" / Iklanku Indonesia
  (https://iklan.shopee.co.id/learn/faq/53/8, https://iklan.shopee.co.id/learn/faq/555/8) — definisi
  Dilihat, Klik, Konversi Langsung, Rasio Konversi, dan contoh perhitungan ACOS (Biaya Iklan ÷ Omzet
  Iklan Langsung × 100%) dikutip langsung dari halaman ini.
- Nama kolom saat "Download Data" bisa memakai variasi Inggris (`Impression`, `Click`,
  `Direct Conversion`, `Direct GMV`, `ACOS`) tergantung bahasa akun; keduanya dicakup oleh daftar
  substring deteksi (Bahasa Indonesia & Inggris).

## TikTok Shop Ads (dulunya Tokopedia Ads, setelah merger Tokopedia–TikTok)

Kolom umum (kampanye Product/GMV Max & Shop Ads): `Biaya`/`Cost`, `Biaya bersih`, `Impresi`,
`Klik`, `Pesanan`/`Orders`, `GMV`/`Pendapatan Kotor`/`Gross Revenue`, `ROAS`,
`Cost per Purchase`.

- Sumber: TikTok Ads Manager Help Center (Bahasa Indonesia), "Tentang Metrik Iklan di Seller
  Center" (https://ads.tiktok.com/help/article/about-ads-metrics-in-seller-center?lang=id) dan
  "Cara Melihat Laporan Kampanye Product GMV Max"
  (https://ads.tiktok.com/help/article/how-to-see-reporting-for-your-product-gmv-max-campaign?lang=id)
  — definisi Biaya, Impresi, Klik, CPM, CPC, Cost per Purchase, ROAS, dan GMV ("jumlah yang
  dibayar pembeli, dikurangi pajak penjualan, ditambah diskon produk") dikutip langsung.
- Tokopedia Seller University juga menautkan pelaporan "Tokopedia Product Shopping Ads" ke
  TikTok Ads Manager yang sama (https://ads.tiktok.com/resources/help/article/how-to-view-reporting-for-tokopedia-product-shopping-ads?lang=id),
  jadi ekspor Tokopedia Ads memakai kolom yang sama dengan TikTok Shop Ads.

## Google Ads

Kolom tabel statistik (nama yang sering disingkat di UI, tetap sama di ekspor CSV): `Campaign`,
`Cost`, `Impr.` (Impressions), `Clicks`, `CTR`, `Avg. CPC`, `Avg. CPM`, `Conversions`,
`Cost / conv.`, `Conv. value`, dan kolom baru `Results` / `Results value` (dikenali sebagai hasil
& nilai hasil sejak v1.0.1). Kolom yang **sengaja tidak dipakai** walau mengandung kata kunci:
`Campaign status`/`Campaign type` (bukan nama), `Avg. cost`/`Cost / conv.`/`Budget` (bukan biaya
total), `Search impr. share` (bukan tayangan), `Conv. value / cost` (bukan nilai).

- Sumber: Google Ads Help, "About columns in your statistics table"
  (https://support.google.com/google-ads/answer/2454071) — daftar nama kolom persis termasuk
  singkatan `Impr.`/`Avg. CPC`/`Avg. CPM`; Google Ads API docs, "Reports in the Google Ads UI" &
  pemetaan kolom konversi (https://developers.google.com/google-ads/api/docs/conversions/ui-mapping)
  mengonfirmasi `Cost / conv.` = `metrics.cost_per_conversion` dan `Conv. value` =
  `metrics.conversions_value`; definisi "Cost / conv." dan "Value / conv." dari Google Ads Help,
  "Understand your conversion tracking data" (https://support.google.com/google-ads/answer/6270625).

## Mata uang

Mata uang akun iklan bisa muncul di tiga tempat, dan v1.0.1 memeriksa ketiganya:
1. Label di judul kolom biaya/nilai, mis. `Amount spent (IDR)`, `Amount spent (USD)` (Meta).
2. Kolom terpisah `Currency` (TikTok, sumber pihak ketiga) / `Currency code` (Google Ads, dari
   pengetahuan penguji) / `Mata uang`. **Belum diverifikasi dari ekspor asli.**
3. Simbol/kode di sel angka: `Rp`, `$`, `US$`, `S$`, `RM`, `€`, `£`, `¥`, atau kode `USD`/`SGD`/...
Bila salah satunya bukan IDR, script **berhenti** dan meminta `--kurs` atau `--mata-uang IDR`
(lihat SKILL.md). File yang mencampur dua mata uang selalu ditolak.

## Keterbatasan yang jujur disebutkan

- Nama kolom bisa berbeda sedikit menurut bahasa akun/browser pengguna (mis. Google Ads berbahasa
  Indonesia memakai "Kampanye", "Biaya", "Tayangan", "RKT" alih-alih nama Inggris di atas). Skill
  ini mencakup sinonim Indonesia untuk kolom umum (biaya, tayangan, klik, konversi) tetapi **tidak**
  menjamin mencakup semua variasi bahasa UI Google Ads; gunakan `--kolom-*` bila deteksi gagal.
- Halaman Meta Business Help Center penuh memerlukan JavaScript sehingga tidak bisa diambil apa
  adanya oleh alat riset otomatis; nama kolom Meta di atas dikonfirmasi silang lewat ringkasan
  pencarian resmi + dua sumber pihak ketiga yang mengutip kolom yang sama, bukan dibaca langsung
  dari halaman aslinya. Tandai **PERLU REVIEW** bila pemilik ingin verifikasi manual sebelum rilis.
