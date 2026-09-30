# Uji banding pesaing (skenario normal 1 + penawaran pembukaan)

> Uji independen 2026-09-30. Skill pesaing **hanya dibaca untuk dinilai** (tidak disalin):
> - `product-name` — phuryn/pm-skills (`pm-marketing-growth/skills/product-name/SKILL.md`, branch main, dibaca 2026-09-30, MIT)
> - `offers` — coreyhaines31/marketingskills (`skills/offers/SKILL.md`, branch main, dibaca 2026-09-30, MIT)
> Keduanya juga sumber ATM skill ini (lihat `ATTRIBUTION.md`), jadi banding ini sekaligus menguji "nilai tambah besar".

**Input:** sama dengan uji 06 (kedai kopi Medan), ditambah: "Sekalian bikin promo pembukaan. Es kopi susu Rp18.000, modal Rp7.000, jual juga di GoFood (potongan 20%)."

## A. Pendekatan pesaing (dijalankan penguji mengikuti instruksi pesaing)
**product-name:** 5 nama, tiap nama berisi Name / Rationale / Brand Fit / Memorability / "Domain & Trademark Considerations". Instruksinya memprioritaskan nama yang "Available for trademark and domain registration" tetapi tidak memberi cara memeriksa; akibatnya agent cenderung menulis catatan seperti "likely available" tanpa dasar. Tidak ada skor, tidak ada pembanding dengan merek pesaing yang diberikan, tidak ada cek arti bahasa daerah, bahasa Inggris, konteks global.
Contoh keluaran: "Toba Brew — evokes Sumatran heritage…; Domain & Trademark: toba-brew.com may be taken; consider variations." (5 opsi, tanpa skor.)

**offers:** kerangka kuat — persamaan nilai 4 tuas, 6 komponen, diagnosis tuas terlemah, larangan kelangkaan palsu dan "worth $X", peringatan diskon untuk akuisisi. Tetapi: fokus jasa/kursus/SaaS dan dolar; tidak ada hitungan laba per unit, tidak memperhitungkan potongan GoFood 20%, tidak ada teks WA/marketplace, tidak ada dasar hukum Indonesia. Keluaran penguji: "Grand Opening Offer: buy 1 get 1 first week + loyalty card; guarantee: remake if not satisfied" — tanpa cek apakah beli-1-gratis-1 rugi di GoFood.

## B. Skill kita
Nama: seperti uji 06 (10 opsi ber-skor, TANDAI, "belum dicek", PDKI kelas 30/43).
Penawaran, dihitung script (penguji menjalankan):
- Beli 1 gratis 1 di GoFood setara diskon 50%: `--harga 18000 --hpp 7000 --platform 20 --diskon 50` -> harga tayang Rp9.000, potongan Rp1.800, laba **Rp200/gelas** (margin 2,2%) — hampir tanpa laba, dan script memberi catatan tentang harga normal (diskon > 50% tidak terpicu karena tepat 50%).
- Alternatif skill: harga normal + bonus kartu stempel (modal Rp300) di GoFood: laba Rp18.000 - 3.600 - 7.000 - 300 = **Rp7.100/gelas** (39,4%). Verifikasi penguji: cocok dengan script.
- Kelangkaan jujur: "Promo pembukaan 1-7 [isi: bulan], 100 gelas per hari" (bila kapasitas nyata).

Verifikasi penguji perintah pertama: 18.000 x 0,5 = 9.000; 20% = 1.800; 9.000 - 1.800 - 7.000 = **200**; 200/9.000 = 2,2%. Cocok.

## Penilaian berdampingan (1-10, penilaian penguji)
| Aspek | Pesaing (product-name + offers) | Skill kita |
|---|---|---|
| Kerangka penawaran (tuas nilai, 6 komponen) | 9 | 8 (setara, versi ringkas) |
| Penamaan: struktur & alasan | 6 | 8 |
| Menghindari nama meniru merek pesaing | 4 (tidak ada mekanisme) | 9 (TANDAI via script) |
| Kejujuran ketersediaan nama/merek | 4 (mendorong klaim "available") | 9 |
| Hitungan laba sebelum promo | 2 | 9 |
| Konteks Indonesia (bahasa, daerah, PDKI, GoFood/Shopee, UU PK, WA) | 1 | 9 |
| Teks siap tempel | 3 | 8 |
| **Rata-rata** | **4,1** | **8,6** |

**Kesimpulan:** skill kita unggul jelas. Kelebihan pesaing yang patut dipelajari (bukan disalin): `offers` punya pustaka format per jenis usaha (jasa, kursus, B2B) dan peringatan eksplisit bahwa diskon untuk menarik pembeli baru merusak persepsi harga; skill kita bisa menambahkan satu baris panduan untuk usaha **jasa** (lihat temuan uji 08).
