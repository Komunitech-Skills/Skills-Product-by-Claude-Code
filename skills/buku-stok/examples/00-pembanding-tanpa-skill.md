# 00 — Uji A/B: tanpa skill vs dengan skill buku-stok (skenario S1)

**Input pengguna (sama persis):**
> Ini file pesanan Shopee hari ini (shopee-hari1.csv), potong stoknya dan buatkan daftar ambil barang ya

File: ekspor bergaya Shopee, 35 kolom, 7 pesanan (status campuran), 1 baris kembar, 1 nomor pesanan rusak `2.60923E+17`.

## A. Tanpa skill (agent umum, tanpa membaca skill apa pun)

Simulasi jujur perilaku agent umum: membaca CSV dengan Python ad-hoc, mengelompokkan per SKU, dan menjawab.

```
Saya sudah membaca file pesanan Shopee Anda. Ringkasan barang yang perlu diambil:

| SKU        | Produk                         | Jumlah |
|------------|--------------------------------|--------|
| KAOS-PT-M  | Kaos Polos Cotton 30s Putih,M  | 6      |
| KAOS-HT-M  | Kaos Polos Cotton 30s Hitam,M  | 3      |
| TOTE-NAT   | Tote Bag Kanvas Natural        | 1      |

(Saya hanya menghitung pesanan berstatus "Perlu Dikirim".)

Untuk memotong stok, saya perlu tahu stok Anda saat ini. Silakan kirim daftar stok
terbaru (misalnya file Excel), nanti saya kurangi dengan jumlah di atas.
Tips: simpan stok di Google Sheets dan kurangi manual setiap hari.
```

Masalah pada jawaban A (diperiksa terhadap isi file):
- Baris kembar persis dihitung dua kali → KAOS-PT-M 6 (seharusnya 3).
- Baris nomor pesanan rusak ikut dihitung sebagai pesanan → KAOS-HT-M 3 (seharusnya 2), tanpa peringatan agar diekspor ulang.
- Pesanan "Selesai"/"Dikirim" tidak memotong stok sama sekali → stok akan selisih.
- Stok tidak bisa dipotong: tidak ada catatan stok, HPP, atau riwayat; besok pengguna harus mengirim ulang stok dan tidak ada perlindungan terhadap impor file yang sama dua kali atau pesanan yang batal setelah diproses.
- Tidak ada urutan tempel resi per kurir, tidak ada lokasi rak, tidak ada backup.

## B. Dengan skill buku-stok
(lengkap di `01-impor-shopee-dan-picking.md`)
```
Pesanan baru yang memotong stok: 4 | Tidak dihitung: 1 batal, 1 pengembalian, 1 belum bayar
Stok yang akan berkurang: KAOS-PT-M -3 (30->27), KAOS-HT-M -2 (24->22), KAOS-HT-L -2 (18->16),
TOTE-NAT -1 (40->39), MUG-KRM -1 (12->11)
Catatan: 1 baris kembar dihitung sekali; 1 nomor pesanan rusak (dibuka di Excel) tidak diproses.
Simpan? -> ya -> tersimpan + backup
DAFTAR AMBIL: Rak A1 KAOS-HT-M x2 | Rak A2 KAOS-PT-M x3 | Rak B1 TOTE-NAT x1
URUTAN RESI: 1. 2609230002CD J&T JX0000000022 | 2. 2609230001AB SPX SPXID0000000011
```

## Penilaian
| Kriteria | Tanpa skill | Dengan skill |
|---|---|---|
| Angka benar | Tidak (2 dari 3 baris picking salah) | Ya, diverifikasi manual |
| Stok benar-benar terpotong & tersimpan | Tidak | Ya (SQLite lokal + backup otomatis) |
| Anti impor ganda / batal setelah impor | Tidak ada | Ada, teruji |
| Picking per rak + urutan resi | Sebagian (tanpa rak/resi) | Lengkap, siap cetak/CSV |
| Konfirmasi sebelum menyimpan | — | Ya (pratinjau → "ya") |

**Kesimpulan:** hasil dengan skill jelas lebih baik — bukan sekadar format, tetapi angka yang benar dan catatan stok yang bertahan antarhari. Bahan "sebelum/sesudah" README sudah sesuai.
