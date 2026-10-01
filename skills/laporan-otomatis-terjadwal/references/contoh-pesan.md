# Contoh laporan (hasil nyata `scripts/susun_pesan.py`)

Semua contoh di bawah adalah **hasil nyata** menjalankan `susun_pesan.py` (dijalankan ulang
setelah revisi skill) -- bukan karangan. Dipakai sebagai acuan format saat menyusun laporan baru.
Angka penjualan & stok berasal dari skenario yang diuji independen di Gateway OpenClaw lokal
(lihat `examples/01-penjualan-mingguan-telegram.md` dan `examples/02-stok-menipis-dari-buku-stok.md`).

## Penjualan mingguan

```
*Laporan Penjualan Mingguan*
Senin 14 - Minggu 20 Sep 2026
Total omzet: Rp 2.778.000
Transaksi: 62 baris penjualan
Rata-rata omzet/hari: Rp 396.857
Hari terbaik: Minggu 20/09 (Rp 524.000)
Hari terendah: Rabu 16/09 (Rp 270.000)
*Produk terlaris*
- Matcha Latte -- 39 pcs -- Rp 858.000
- Roti Bakar Coklat -- 38 pcs -- Rp 570.000
- Croissant -- 26 pcs -- Rp 520.000
⚠️ 7 transaksi berstatus Batal tidak dihitung.
⚠️ 1 baris dilewati (tanggal tidak terbaca).
```
Catatan: label "baris penjualan" karena CSV contoh tidak punya kolom nomor nota (satu pesanan
marketplace bisa berisi beberapa baris produk). Bila ada kolom nota (`--kolom-pesanan`) atau
1 baris = 1 nota, tulis "<N> nota / <Q> pcs" (mis. "57 nota / 110 pcs"); jumlah baris/nota tidak
pernah disebut "item" -- lihat `templates/RESEP-penjualan.md`.

## Stok menipis -- sumber `buku-stok` (ada 2 produk menipis)

```
*Stok Menipis*
Kamis, 24 Sep 2026, 07:00 WIB
Jumlah produk menipis: 2
*Produk menipis*
- Kaos Polos Cotton 30s - Hitam L -- sisa 8 -- ambang 10 -- habis ~20 hari
- Mug Keramik 350ml - Putih -- sisa 9 -- ambang 10 -- habis ~90 hari
Data stok dari buku-stok, transaksi terakhir dicatat 23 Sep 2026 18:08.
```

## Stok menipis -- tidak ada yang menipis (kabar baik, tetap dilaporkan)

```
*Stok Menipis*
Selasa, 23 Sep 2026, 07:00 WIB
Jumlah produk menipis: 0
Tidak ada produk menipis hari ini.
Data stok dari buku-stok, transaksi terakhir dicatat 3 jam lalu.
```
`jumlah: 0` dari `stok.py laporan menipis --json` adalah hasil VALID (bukan data kosong) --
lihat `templates/RESEP-stok-menipis.md`. Baris ini masuk `catatan` (info netral, tanpa ikon ⚠️),
bukan `peringatan`.

## Piutang jatuh tempo (contoh format, tanpa nama pelanggan)

```
*Piutang Jatuh Tempo Hari Ini*
Selasa, 23 Sep 2026
Jatuh tempo hari ini: 2 tagihan -- Rp 15.000.000
Terlambat: 1 tagihan -- Rp 12.500.000
H-1 (besok): 3 tagihan -- Rp 8.200.000
Detail per pelanggan ada di file sumber piutang Anda -- buka manual untuk menindaklanjuti (draf
pesan tagih per pelanggan dibuat lewat skill tagih-piutang, dikirim manual, bukan otomatis).
```

## Data sumber belum ada (kegagalan yang ditangani dengan jujur)

```
Laporan penjualan hari ini BELUM dibuat.

Alasan: belum ada file penjualan (pola *.csv) di folder Dokumen/Laporan-AI/masuk/penjualan.
Ekspor data penjualan dari sumbernya (kasir/marketplace/bank) sebagai CSV, taruh di folder itu,
lalu laporan akan otomatis dibuat di jadwal berikutnya.

(Pesan ini dari cek_sumber_data.py -- TIDAK ada angka omzet yang dikirim karena datanya belum
ada, bukan karena omzetnya nol.)
```

## Data mirip data pribadi terdeteksi (exit code 3 -- contoh, JANGAN dikirim begini)

Kalau baris JSON mengandung pola NIK/KTP/nomor HP/email, `susun_pesan.py` tetap mencetak pesan
apa adanya ke stdout, TAPI keluar dengan **exit code 3** dan penjelasannya HANYA ke stderr
(`PERINGATAN-PDP: ...`) -- tidak pernah ditambahkan ke isi pesan itu sendiri. Agent WAJIB berhenti
dan meninjau ulang baris yang dituding sebelum mengaktifkan jadwal (lihat `SKILL.md` Langkah
3.5). Kata seperti "unik" atau "Klinik" TIDAK memicu ini (dicocokkan dengan batas kata).
