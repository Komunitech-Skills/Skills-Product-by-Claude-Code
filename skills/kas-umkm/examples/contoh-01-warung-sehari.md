# Contoh 1 — Warung sehari penuh: catat, hitung laci, rekap harian

Dijalankan sungguhan dengan `scripts/kas.py` oleh pembuat skill (26/09/2026). **Semua data fiktif.**
Output dipotong seperlunya; angka tidak diubah. Agent memakai `--json`; di bawah ditampilkan isi `teks`-nya.

## Persiapan (sekali)
Pengguna: *"Bikinin buku kas warung saya. Uang laci awal bulan 500 ribu, rekening BRI 3 juta, QRIS masuk ke BRI.
Saya mau dibatasi ambil pribadi 1,5 juta sebulan."*

```
$ kas.py init --nama-usaha "Warung Bu Sri (fiktif)" --kas-awal 500rb --mulai 01/09/2026 --batas-prive 1,5jt --ya
TERSIMPAN. Buku kas siap.
Buku kas baru: ~/KomunitechData/kas/kas.db
Nama usaha: Warung Bu Sri (fiktif) | Zona: WIB | Mulai: 01/09/2026
Akun awal: Laci kas (tunai), saldo awal Rp 500.000 per 01/09/2026
Batas prive bulanan: Rp 1.500.000
Cadangan otomatis: ~/KomunitechData/kas/backup-kas

$ kas.py akun tambah --nama BRI --jenis bank --saldo-awal 3jt --tanggal-awal 01/09/2026 --terima-qris --ya
TERSIMPAN.
Akun baru: BRI [bri] (rekening bank, penampung QRIS), saldo awal Rp 3.000.000 per 01/09/2026.
```
(Keduanya sudah dipratinjau dan disetujui pengguna sebelum `--ya`.)

Catatan 1–25 September (61 baris: jualan tunai & QRIS, kulakan, gaji mingguan, sewa, token listrik, prive) diimpor dari
CSV buku kas lama dengan `impor`, lalu `pindah --dari laci --ke BRI --jumlah 5jt --tanggal 15/09/2026`.
Saldo sebelum hari ini: Laci kas Rp 2.310.000, BRI Rp 11.240.000.

## Laporan akhir hari
Pengguna: *"Hari ini jualan tunai 780rb, QRIS 240rb. Keluar: gas elpiji 25rb, es batu 20rb, ambil 200rb buat jajan
anak."*

Agent meneruskan semua baris; kategori yang tidak disebut pengguna dikosongkan:
```
$ kas.py catat --baris "masuk;780rb;penjualan;tunai;jualan tunai" --baris "masuk;240rb;penjualan;qris;jualan QRIS" \
    --baris "keluar;25rb;;tunai;gas elpiji" --baris "keluar;20rb;;tunai;es batu" --baris "keluar;200rb;;;jajan anak" --json
{
  "ok": false,
  "error": "Baris 3: Kategori untuk 'gas elpiji' (keluar Rp 25.000) belum jelas. Tanyakan ke pengguna, pilih salah satu: penjualan, modal, beli-stok, gaji, listrik-air, sewa, prive, pajak, pinjaman, lain-lain.",
  "perlu_kategori": true
}
```
Agent **tidak menebak**; bertanya satu kali: *"Gas elpiji dan es batu masuk kategori apa? Pilihan: beli stok/bahan
(untuk jualan) atau lain-lain (operasional)."* Pengguna: *"gas operasional, es batu bahan."*
```
$ kas.py catat --baris "masuk;780rb;penjualan;tunai;jualan tunai" --baris "masuk;240rb;penjualan;qris;jualan QRIS" \
    --baris "keluar;25rb;lain-lain;tunai;gas elpiji" --baris "keluar;20rb;beli-stok;tunai;es batu" --baris "keluar;200rb;;;jajan anak"
PRATINJAU (belum disimpan):
1. MASUK  Rp 780.000 | 26/09/2026 | Penjualan | Tunai -> Laci kas | jualan tunai
2. MASUK  Rp 240.000 | 26/09/2026 | Penjualan | QRIS -> BRI | jualan QRIS
3. KELUAR Rp 25.000 | 26/09/2026 | Pengeluaran lain-lain | Tunai -> Laci kas | gas elpiji
4. KELUAR Rp 20.000 | 26/09/2026 | Beli stok/bahan | Tunai -> Laci kas | es batu
5. KELUAR Rp 200.000 | 26/09/2026 | Prive (ambil pribadi) | Tunai -> Laci kas | jajan anak
Asumsi: baris 5: kategori 'prive' ditebak dari kata 'jajan'; baris 5: dibayar/diterima tunai (metode tidak disebut).
Saldo setelah dicatat: Laci kas Rp 2.845.000, BRI Rp 11.480.000
Catatan: PERINGATAN PRIVE bulan ini (s.d. 26/09/2026): Rp 1.800.000 melewati batas prive bulanan yang Anda tetapkan (Rp 1.500.000).

Simpan? Jalankan perintah yang sama + --ya setelah pengguna setuju.
```
Agent ke pengguna: *"Saya catat begini: [5 baris]. 'Jajan anak' saya masukkan ke ambil pribadi (prive), diambil dari
laci. Catatan: ambil pribadi bulan ini sudah Rp 1.800.000, lewat batas Rp 1.500.000 yang Anda tetapkan. Simpan?"*
Pengguna: *"ya"* → perintah yang sama + `--ya` (tersimpan sebagai #63–#67).

## Hitung laci
Pengguna: *"Uang di laci: seratus ribuan 22 lembar, lima puluh ribuan 10, dua puluh ribuan 5, sepuluh ribuan 2, lima
ribuan 1, dua ribuan 2."*
```
$ kas.py opname --pecahan "100rb x22, 50rb x10, 20rb x5, 10rb x2, 5rb x1, 2rb x2"
PRATINJAU (belum disimpan):
Hitung uang Laci kas, Sabtu, 26/09/2026
Menurut buku : Rp 2.845.000
Uang dihitung: Rp 2.829.000
Rincian: Rp 100.000 x22, Rp 50.000 x10, Rp 20.000 x5, Rp 10.000 x2, Rp 5.000 x1, Rp 2.000 x2
Hasil: SELISIH KURANG Rp 16.000 (ditandai).
Kemungkinan penyebab (cek dulu, jangan menuduh siapa pun): kembalian terlalu banyak; pengeluaran kecil dari laci belum dicatat (es batu, parkir, dll.); uang diambil untuk keperluan pribadi tanpa dicatat (prive); pembayaran QRIS/transfer tercatat sebagai tunai; salah hitung uang.
Buku belum disesuaikan. Jika penyebabnya ketemu, catat transaksi yang terlewat. Jika tidak ketemu dan pengguna setuju, ulangi dengan --sesuaikan agar saldo buku = uang fisik.
Pastikan semua transaksi hari ini sudah dicatat sebelum menghitung.
```
Agent menyampaikan selisih tanpa menuduh dan mengajak mengecek pengeluaran kecil. Pengguna ingat parkir 5rb dan
kerupuk 8rb belum dicatat. Sisa selisih Rp 3.000 tidak ketemu; pengguna setuju buku disesuaikan.
```
$ kas.py catat --baris "keluar;5rb;lain-lain;tunai;parkir" --baris "keluar;8rb;beli-stok;tunai;kerupuk" --ya
TERSIMPAN.
1. #68 KELUAR Rp 5.000 | 26/09/2026 | Pengeluaran lain-lain | Tunai -> Laci kas | parkir
2. #69 KELUAR Rp 8.000 | 26/09/2026 | Beli stok/bahan | Tunai -> Laci kas | kerupuk
Saldo setelah dicatat: Laci kas Rp 2.832.000

$ kas.py opname --pecahan "100rb x22, 50rb x10, 20rb x5, 10rb x2, 5rb x1, 2rb x2" --sesuaikan --ya
TERSIMPAN.
Hitung uang Laci kas, Sabtu, 26/09/2026
Menurut buku : Rp 2.832.000
Uang dihitung: Rp 2.829.000
Hasil: SELISIH KURANG Rp 3.000 (ditandai).
Buku DISESUAIKAN: dicatat keluar Rp 3.000 (kategori selisih hitung laci), saldo buku jadi Rp 2.829.000.
```

## Rekap harian (teks ini juga yang dikirim jadwal Telegram)
```
$ kas.py rekap --tanggal hari-ini
BUKU KAS Warung Bu Sri (fiktif)
Rekap harian Sabtu, 26/09/2026

UANG MASUK: Rp 1.020.000
- Penjualan: Rp 1.020.000
UANG KELUAR: Rp 261.000
- Beli stok/bahan: Rp 28.000
- Prive (ambil pribadi): Rp 200.000
- Pengeluaran lain-lain: Rp 30.000
- Selisih laci kurang: Rp 3.000

HASIL USAHA (masuk usaha - keluar usaha): Rp 959.000
  (tidak termasuk modal, pinjaman, prive, dan pindah dana; ini hitungan kas, bukan laba akuntansi)
Prive (ambil pribadi): Rp 200.000 = 20,9% dari hasil usaha
Per metode: Tunai masuk Rp 780.000 keluar Rp 261.000; QRIS masuk Rp 240.000 keluar Rp 0

SALDO per akhir 26/09/2026:
- Laci kas: Rp 2.829.000
- BRI: Rp 11.480.000
Total: Rp 14.309.000 (awal periode Rp 13.550.000, naik Rp 759.000)
Hitung Laci kas 26/09: buku Rp 2.832.000, fisik Rp 2.829.000 -> SELISIH KURANG Rp 3.000 (disesuaikan)

PERINGATAN PRIVE bulan ini (s.d. 26/09/2026): Rp 1.800.000 melewati batas prive bulanan yang Anda tetapkan (Rp 1.500.000).
```

## Cek angka manual
- Laci: 2.310.000 + 780.000 − 25.000 − 20.000 − 200.000 = 2.845.000; setelah parkir & kerupuk = 2.832.000.
- Uang fisik: 22×100.000 + 10×50.000 + 5×20.000 + 2×10.000 + 1×5.000 + 2×2.000 = 2.829.000 → kurang 3.000.
- Hasil usaha: 1.020.000 − (28.000 + 30.000 + 3.000) = 959.000. Prive 200.000 / 959.000 = 20,86% → 20,9%.
- Total saldo 2.829.000 + 11.480.000 = 14.309.000; naik 759.000 = masuk 1.020.000 − keluar 261.000.
- Prive September: 4 × 400.000 (tgl 4, 11, 18, 25) + 200.000 = 1.800.000 > batas 1.500.000.
