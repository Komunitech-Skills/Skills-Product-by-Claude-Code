# Membaca penawaran pemasok: istilah yang sering menjebak

> Ringkasan untuk alat bantu perbandingan, bukan nasihat pajak atau hukum. Status aturan pajak per 2026-09-23 (sama dengan acuan hitung PPN di library Komunitech). Aturan bisa berubah; cek sumber resmi (pajak.go.id, Kring Pajak 1500200) sebelum keputusan besar.

## 1. Termin bayar (syarat pembayaran)
| Istilah di penawaran | Artinya | Cara mengisi |
|---|---|---|
| COD, tunai, cash, bayar saat barang datang | Bayar penuh saat barang diterima | DP 0%, tempo 0 |
| Bayar di muka, transfer dulu, CBD (*cash before delivery*), lunas di depan | Bayar penuh sebelum barang dikirim | DP 100% |
| DP 30%/50%, pelunasan saat kirim/terima | Uang muka saat pesan, sisanya saat barang tiba | DP 30/50, tempo 0 |
| Tempo 14/30 hari, TOP 30, Net 30, H+30 | Bayar sekian hari setelah barang/faktur diterima | DP 0, tempo 14/30 |
| DP 50% sisa tempo 30 hari | Gabungan | DP 50, tempo 30 |
| Konsinyasi / titip jual | Bayar setelah barang laku | Di luar hitungan; jelaskan terpisah |

Cara menilai: makin lama Anda boleh menahan uang, makin ringan untuk kas. **DP ke pemasok baru adalah risiko** (barang belum terbukti datang); untuk pemasok baru sarankan DP kecil, rekening atas nama usaha (bukan pribadi), dan bukti penawaran tertulis. "Diskon tunai 2% atau tempo 30 hari" setara biaya modal sekitar 2% per bulan; bila usaha Anda meminjam modal di bawah itu, tempo biasanya lebih untung (opsi bunga modal di hitungan menilainya dalam rupiah).

## 2. PPN: pemasok PKP vs non-PKP
- Hanya **Pengusaha Kena Pajak (PKP)** yang memungut PPN dan menerbitkan faktur pajak. Pemasok **non-PKP** (umumnya usaha kecil yang belum dikukuhkan PKP) tidak memungut PPN; harganya adalah harga akhir.
- Tarif: PPN 12% × DPP nilai lain 11/12 × harga untuk barang/jasa **non-mewah** (PMK 131/2024, berlaku 1 Januari 2025) → efektif **11% dari harga sebelum PPN**. Barang mewah (PPnBM) 12% penuh, dan beberapa barang/jasa punya besaran tertentu sendiri: di luar hitungan skill ini.
- **Jebakan utama:** penawaran PKP sering ditulis "harga belum termasuk PPN". Rp4.200 dari pemasok PKP = Rp4.662 setelah PPN, sehingga bisa lebih mahal dari pemasok non-PKP Rp4.500. Selalu tanya "sudah/belum termasuk PPN?".
- **Bila usaha Anda sendiri PKP**, PPN dari pemasok PKP umumnya bisa dikreditkan sebagai Pajak Masukan, sehingga biaya sebenarnya adalah harga sebelum PPN. Uang yang keluar di awal tetap termasuk PPN. Syarat ringkas (UU PPN Pasal 9; **PERLU REVIEW konsultan pajak**): usaha Anda PKP; faktur pajak sah atas nama dan NPWP usaha Anda; pembelian berhubungan langsung dengan kegiatan usaha yang terutang PPN (bukan untuk penyerahan yang dibebaskan PPN); dikreditkan dalam batas waktu yang diatur. Bila syarat tidak terpenuhi, PPN menjadi biaya. Hasil hitungan menuliskan asumsi ini terbuka.
- Pemasok non-PKP yang menagih "PPN" → minta klarifikasi dan rincian; jangan dibayar sebagai PPN tanpa faktur pajak.
- **Kamus kolom `ppn`** (sama di template, SKILL.md, dan hitungan): `termasuk` = PKP, harga sudah termasuk PPN · `belum` = PKP, harga belum termasuk PPN (+11%) · `non-pkp` = tanpa PPN · `bebas` = barang dibebaskan PPN · `?`/kosong = belum jelas → `[isian]`. Kata "belum" tidak pernah berarti data kosong.
- Ongkir/biaya lain yang ditagih pemasok PKP di faktur yang sama **diasumsikan** ikut kena PPN (Harga Jual dalam UU PPN mencakup biaya yang diminta penjual karena penyerahan barang). Ongkir yang Anda bayar langsung ke ekspedisi tidak ikut PPN pemasok. Pengecualian yang mungkin: ongkir yang hanya diteruskan sebagai penggantian biaya ekspedisi dengan dokumen atas nama pembeli. Asumsi ini ditulis terbuka di hasil beserta besarnya ("PPN atas ongkir Rp…"). **PERLU REVIEW konsultan pajak.**
- **Barang kebutuhan pokok yang dibebaskan PPN:** menurut PP 49/2022, beberapa bahan pokok (mis. beras, gabah, jagung, kedelai, garam, daging, telur, susu segar, buah, sayur, ubi, bumbu, gula konsumsi) dibebaskan PPN. Untuk barang seperti ini jangan menulis "potensi PPN": isi `--barang "gula pasir"` (dikenali sebagai kemungkinan bahan pokok) atau `--bebas-ppn ya` / kolom `ppn` = `bebas`. Daftar pastinya dan syaratnya ikuti aturan resmi. **PERLU REVIEW konsultan pajak.**
- Pembulatan di hitungan: PPN dari DPP persis, dibulatkan ke bawah sekali; harga termasuk PPN dipecah dengan DPP rupiah bulat terbesar. Belum dicocokkan dengan Coretax; bila faktur berbeda, ikuti faktur.

## 3. Franco vs loco (istilah pengiriman lokal)
| Istilah | Artinya | Dampak ke biaya |
|---|---|---|
| **Franco [gudang/toko pembeli]**, gratis ongkir, harga sampai tempat | Harga sudah termasuk kirim sampai alamat Anda | Ongkir 0 (sudah di harga) |
| **Loco [gudang penjual]**, ex-gudang, ambil sendiri | Harga di gudang pemasok; ambil sendiri atau ongkir Anda tanggung | Tambahkan biaya ambil/ekspedisi Anda |
| Franco ekspedisi / sampai agen | Pemasok mengantar ke ekspedisi pilihan; ongkir ekspedisi Anda bayar | Ongkir ekspedisi dibayar terpisah (tanpa PPN pemasok) |
| Ongkir "menyesuaikan", "tergantung berat" | Belum ada angka | Tulis `[isian: ongkir]`; jangan menebak |

Istilah ekspor-impor internasional (EXW, FOB, CIF, DDP) mirip konsepnya, tetapi skill ini tidak menghitung bea masuk, PPN impor, PPh impor, atau kurs; minta angka itu dari pengguna/forwarder.

## 4. MOQ, kelipatan, harga grosir
- **MOQ** (*minimum order quantity*): jumlah minimal sekali pesan. Bila kebutuhan di bawah MOQ, Anda harus beli lebih → **modal tertahan** di stok sisa dan risiko rusak/kedaluwarsa/model berganti.
- **Kelipatan/isi dus:** pesan harus per dus (mis. isi 24); 130 pcs berarti beli 144.
- **Harga grosir bertingkat:** umumnya harga tingkat berlaku untuk seluruh jumlah (beli 100 → semua Rp11.000). Akibatnya kadang **beli sedikit lebih banyak justru lebih murah total** (95 × Rp12.000 = Rp1.140.000 > 100 × Rp11.000 = Rp1.100.000). Bila pemasok memakai harga berjenjang per bagian (100 pertama harga A, sisanya harga B), tulis di catatan dan sesuaikan.
- **Minimal belanja Rp** (mis. minimal Rp1 juta): diperlakukan seperti MOQ dalam rupiah.

## 5. Kualitas, sampel, dan rekam jejak
- **Harga sampel vs produksi:** sampel bisa dibuat lebih rapi atau dari bahan berbeda. Minta pernyataan tertulis bahwa barang produksi sama dengan sampel (bahan, ukuran, warna, ketebalan), simpan sampelnya sebagai acuan.
- "Harga bisa berubah sewaktu-waktu" → minta **masa berlaku harga** tertulis.
- Garansi/retur: minta tertulis (berapa hari, siapa tanggung ongkir retur, diganti barang atau uang).
- Nilai kualitas 1-5 diisi pengguna dari hal nyata: hasil sampel, pengalaman pesanan sebelumnya (tepat waktu, cacat), lama berlangganan, ulasan yang dilihat sendiri. Tanpa dasar → 3 (netral).

## 6. Risiko ketergantungan satu pemasok
Satu pemasok untuk barang penting = bila mereka telat, stok habis, atau naik harga, usaha Anda ikut berhenti. Pilihan yang wajar untuk UMKM: pemasok utama + satu cadangan yang pernah dicoba (pesanan kecil), atau membagi pesanan (mis. 70/30) bila tambahan biayanya kecil. Hitungan "bagi pesanan" menunjukkan berapa tambahan biayanya.
