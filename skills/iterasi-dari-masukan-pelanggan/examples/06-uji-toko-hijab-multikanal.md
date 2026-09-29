# Uji 06 (normal 1) - Toko hijab online: Shopee + WA + Instagram
Penguji independen, 2026-09-29. Data fiktif buatan penguji (nama/nomor fiktif), gaya asli pembeli: slang, typo, emoji.
Data lengkap disimpan penguji di scratchpad (`uji-iterasi/s06/`); ringkasan di bawah.

## Data
- `shopee.csv` (20 ulasan) dengan judul kolom ala ekspor marketplace: `No. Pesanan,Nama Pembeli,Ulasan Pembeli,Rating,Waktu Ulasan`.
  Dua pembeli berbeda menulis teks yang sama persis: "Barang sesuai pesanan".
- `chat-wa.txt` (ekspor Android, 14 baris: 1 pesan sistem, 1 media, 3 pesan admin, 9 pesan pelanggan; ada nomor HP sebagai nama pengirim,
  no. pesanan, resi, alamat "Jl. Melati No 5").
- `ig.txt` (5 komentar, 1 berisi @akun).

## Jalan 1 - perintah persis seperti SKILL.md langkah 3
```
python3 scripts/olah_masukan.py chat-wa.txt=WhatsApp shopee.csv=Shopee ig.txt=Instagram --staf "Admin Hijabku" --simpan-anonim anonim.csv
```
Hasil: exit 0, **tetapi salah total untuk kanal Shopee**:
```
Kanal: Shopee 14, WhatsApp 9, Instagram 5
Tidak dihitung: pesan sistem/media 2, pesan staf 3, terlalu pendek 20, duplikat 6
Perlu dibaca agent ... - "12/09/2026" - "13/09/2026" - "14/09/2026"
```
Penyebab (dibaca dari kode `pilih_kolom`): kolom `Ulasan Pembeli` **dibuang** karena mengandung kata "pembeli" (daftar `KOLOM_NAMA`),
sedangkan `Waktu Ulasan` (mengandung "ulasan") dan `No. Pesanan` (mengandung "pesan") **dipilih sebagai kolom teks**. Jadi 14 "masukan"
Shopee adalah tanggal; ke-20 ulasan asli tidak terbaca sama sekali, dan tidak ada peringatan. Agent yang teliti bisa curiga dari
kutipan "12/09/2026" di "Perlu dibaca agent", tetapi tabel isu teratas sudah terlanjur tampil meyakinkan (4 isu, semua "Pantau").
**Temuan KRITIS.**

## Jalan 2 - kolom dipaksa (`--kolom-teks "Ulasan Pembeli" --kolom-tanggal "Waktu Ulasan"`)
Total 33 masukan (Shopee 19, WA 9, IG 5); "duplikat 1" = ulasan "Barang sesuai pesanan" dari pembeli ke-2 **dibuang** padahal orang berbeda.

| # | Tema | Keluhan | Skor | Prioritas |
|---|---|---|---|---|
| 1 | Kualitas produk | 5 | 20 | Segera |
| 2 | Pengiriman | 4 | 12 | Segera |
| 3 | Porsi / ukuran | 2 | 6 | Pantau |
| 4-6 | Kemasan, Layanan, Harga | 1 | 3/3/2 | Pantau |

## Jalan 3 - agent membuat `tema.json` sesuai langkah 4 (warna, jahitan/bahan, stok/restock, layanan)
Hasil: Kualitas 5 (20), Jahitan/bahan 4 (16), Warna 4 (16), Pengiriman 4 (12), Kemasan 2, Ukuran 2, Harga 1.

## Label manual penguji vs script (bawaan, jalan 2) - 34 masukan asli
Pasangan (masukan, tema) yang benar-benar keluhan menurut penguji = 21.

| Tema | Label manual | Script benar | Script salah | Terlewat |
|---|---|---|---|---|
| Kualitas (termasuk warna tidak sesuai foto/pudar) | 9 | 5 | 0 | 4 (WA warna beda, WA jahitan lepas -> dianggap PUJIAN, pudar, IG "teman beli beda jauh" -> PUJIAN) |
| Pengiriman lama | 3 | 2 | 2 (restock "nunggu lama", "dikirim salah warna") | 1 ("blm dtg udh seminggu" = netral) |
| Ukuran | 2 | 2 | 0 | 0 |
| Kemasan | 2 | 1 | 0 | 1 ("plastik tipis, sobek pas nyampe" -> PUJIAN) |
| Layanan (chat tidak dibalas) | 1 | 0 | 1 (komplain warna -> layanan) | 1 ("ga dibales" tidak dikenali) |
| Harga | 2 | 1 | 0 | 1 ("harga naik terus" = netral) |
| Stok/restock | 1 | 0 | 0 | 1 |
| Ketepatan pesanan (salah warna dikirim) | 1 | 0 | 0 | 1 |
| **Total** | **21** | **11** | **3** | **10** |

Presisi keluhan 11/14 = 79%, recall 11/21 = 52%. Urutan #1 (kualitas) benar. Penyebab salah yang berulang:
- kata **"pas"** ada di daftar positif, padahal di bahasa sehari-hari "pas" sering berarti "ketika" ("lepas pas baru dipake", "sobek pas nyampe");
  keluhan jadi pujian.
- **"sesuai foto"** diperlakukan positif walau kalimatnya pertanyaan/keluhan ("warnanya sesuai foto ga? ... beda jauh").
- **"paket"** masuk tema Varian/menu ("paket sy blm dtg" -> varian_menu).
- Kata dengan akhiran/slang tidak terbaca: "dibales", "cepet", "restock", "dateng".
- Setelah tema.json: "chat ga dibales" dengan "dibales" sebagai kata negatif menjadi **positif** (negasi membalik keluhan).
- `tema.json` dengan `id` sama (mis. `layanan`) **mengganti** seluruh kata bawaan, tidak menambah; tidak dijelaskan di template.
- Nama pengirim "Kak Yanti" membuat kata "kak" di seluruh chat berubah menjadi "[nama]" (aman, tapi kutipan jadi aneh).

## Verifikasi angka independen
`verifikasi.py` (ditulis penguji, membaca CSV anonim + JSON): total, per kanal, sentimen, per bulan, jumlah masukan per tema,
skor = keluhan x dampak, persen, aturan prioritas, urutan -> **semua cocok** (jalan 3, n=33; juga data contoh pembuat n=51).
Aritmetika script benar; masalahnya ada pada pembacaan kolom dan klasifikasi.

## Privasi
Nama pengirim, nomor HP (juga sebagai nama pengirim), no. pesanan, resi, alamat "Jl. ...", @akun: tersamarkan. Tidak ada nama di laporan.

## Nilai skenario: 5/10 (alur verifikasi menolong, tetapi ekspor marketplace umum gagal diam-diam).
