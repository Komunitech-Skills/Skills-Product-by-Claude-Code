---
name: rekap-penjualan-csv
description: Menganalisis file penjualan CSV (ekspor kasir, Shopee, Tokopedia, atau spreadsheet) lalu membuat rekap omzet, omzet per status pesanan (selesai, dikirim, batal), produk terlaris, tren harian, dan ringkasan siap tempel untuk grup tim dalam bahasa Indonesia. Gunakan saat pengguna mengirim data penjualan atau minta laporan/rekap penjualan (sales report, sales summary, analisis omzet, ringkasan buat grup tim).
---

# Rekap Penjualan dari CSV

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

Mengubah data penjualan mentah menjadi ringkasan yang mudah dipahami pemilik usaha.

## Kapan TIDAK digunakan
- Laporan laba rugi / neraca dari buku kas → pakai skill `laporan-keuangan-emkm`.
- Menghitung pajak (PPh Final 0,5%) → pakai skill `pph-final-umkm`.
- Prediksi/forecast penjualan masa depan → jelaskan bahwa skill ini hanya merekap data yang sudah terjadi.
- File Excel `.xlsx` → minta pengguna menyimpannya sebagai CSV dulu (Excel: *File → Save As → CSV*).

## Alur kerja

1. **Cek kolom file.** Lihat beberapa baris pertama CSV. Tentukan kolom untuk:
   - tanggal (wajib)
   - nama produk (wajib)
   - jumlah/qty (opsional, default 1)
   - total harga baris (wajib; jika tidak ada, gunakan harga satuan × qty)
2. **Jalankan script analisis** `scripts/rekap.py`. Script ada di subfolder `scripts/` di folder yang sama
   dengan SKILL.md ini (folder skill); gunakan path lengkapnya dan jangan mencarinya ke seluruh disk (`find /`). Di Windows, ganti `python3` dengan `python` atau `py`:
   ```bash
   python3 <folder-skill-ini>/scripts/rekap.py <file.csv> \
     --kolom-tanggal "Tanggal" --kolom-produk "Produk" \
     --kolom-qty "Qty" --kolom-total "Total"
   ```
   - Jika tidak ada kolom total tapi ada harga satuan, pakai `--kolom-harga "Harga"` sebagai ganti `--kolom-total`.
   - Jika ada kolom status pesanan (ekspor Shopee/Tokopedia), **selalu** tambahkan `--kolom-status "Status Pesanan"`
     agar pesanan batal/retur/refund tidak dihitung sebagai omzet.
   - Jika ada kolom nomor pesanan (mis. `No. Pesanan` di Shopee), tambahkan `--kolom-pesanan "No. Pesanan"` agar
     jumlah transaksi per hari dihitung per pesanan unik, bukan per baris produk.
   - Delimiter (`,` `;` tab), encoding Excel Windows, format angka (`Rp 15.000`, `Rp. 25000`, `15.000,-`, `15.000,50`),
     dan tanggal (`01/09/2026`, `2026-09-01 10:00`, `1 Sep 2026`, `1 Agustus 2026`) dideteksi otomatis.
   - Jika output berisi `peringatan` tentang urutan tanggal ambigu, tanyakan ke pengguna apakah formatnya
     hari/bulan (Indonesia) atau bulan/hari (AS); jika AS, jalankan ulang dengan `--urutan-tanggal mdy`.
   - Jika Python tidak tersedia, hitung manual langkah demi langkah dan beri tahu pengguna bahwa hasil belum diverifikasi script.
3. **Tulis rekap** berdasarkan output JSON script, dengan format di bawah.
4. **Beri 2–3 insight** yang bisa langsung ditindaklanjuti, berdasarkan angka.
5. **Ringkasan untuk grup tim** (bila diminta, mis. "kirim ke grup admin/packing"): salin apa adanya isi
   `ringkasan_siap_tempel` dari script sebagai **draf**; pemilik yang menempel/mengirim sendiri (jangan mengirim
   atau menjadwalkan kirim otomatis). Boleh dipersingkat dengan membuang kalimat, tetapi **jangan mengubah angka,
   tanggal, atau menambah angka baru**.

## Format output

```
## Rekap Penjualan <tanggal awal> – <tanggal akhir>

**Total omzet:** Rp X  _(dari N pesanan; satuan sesuai `satuan_pesanan`)_
**Jumlah transaksi (baris):** N
**Rata-rata omzet per hari (kalender):** Rp Y  _(hari berjualan: Rp Z)_

### Status pesanan (bila ada kolom status; dari `per_status`)
| Status | Pesanan | Nilai | Keterangan |
|---|---|---|---|
| Selesai | ... | Rp ... | masuk omzet |
| Sedang Dikirim | ... | Rp ... | masuk omzet, belum final |
| Dibatalkan | ... | Rp ... | tidak masuk omzet; tanggal: dari `dibuang_per_tanggal` |

### 5 Produk Terlaris (omzet)
| # | Produk | Qty | Omzet | % |
|---|---|---|---|---|

### Tren harian
Hari omzet tertinggi: <tanggal> (Rp ...). Hari omzet terendah: <tanggal> (Rp ...).
Hari transaksi terbanyak: <tanggal> (<jumlah> pesanan/baris transaksi).

### Insight
1. ...
2. ...

### Ringkasan siap tempel untuk grup tim (draf, Anda yang kirim)
<isi ringkasan_siap_tempel apa adanya>
```

## Aturan & batasan

- Pertanyaan "hari paling rame/ramai" dijawab dari **dua sisi**: omzet (`hari_terbaik`) **dan** jumlah transaksi
  (`hari_transaksi_terbanyak`, sebut satuannya: pesanan unik atau baris). Bila tanggalnya berbeda, jelaskan bedanya.

- Semua angka rupiah ditulis dengan pemisah ribuan titik: `Rp 1.250.000`.
- **Semua angka wajib dari keluaran script.** Jangan menjumlah, mengurangi, mengira ("~Rp440rb"), atau
  menyimpulkan sendiri angka yang tidak ada di JSON — termasuk nilai per status, jumlah pesanan per pelanggan,
  dan hari/tanggal pembatalan. Nilai per status ambil dari `per_status`; tanggal pesanan batal/retur ambil dari
  `dibuang_per_tanggal` (itu tanggal pesanan dibuat, bukan tanggal dibatalkan — sebut begitu). Insight yang
  butuh angka di luar JSON: jangan ditulis, atau jalankan ulang script dengan opsi yang sesuai.
- Pesanan berstatus belum final (`per_status[..].final = false`, mis. "Sedang Dikirim") sudah masuk omzet;
  sebutkan nilainya persis dari `per_status` dan bahwa angka itu bisa turun bila ada batal/retur.
- Jika script melaporkan baris yang dilewati (`baris_dilewati` > 0) atau `dibuang_karena_status`, sebutkan jumlah dan alasannya.
- Sampaikan setiap isi `peringatan` dari script kepada pengguna.
- Jika memakai `--kolom-status`, tampilkan ke pengguna status yang **dihitung** (`status_dihitung`) dan yang **dibuang**
  (`dibuang_karena_status`), agar pengguna bisa mengoreksi bila ada status yang salah golongan
  (mis. jalankan ulang dengan `--abaikan-status` berisi daftar sendiri).
- Jika `nama_produk_digabung` tidak kosong, sebutkan penggabungannya (mis. "Kopi" dan "kopi " dihitung sebagai satu produk).
- Angka dengan format meragukan (mis. `15.000.00`, `15000.500`, notasi ilmiah `1.5E+06` dari Excel) sengaja **dilewati**,
  bukan ditebak; sebutkan jumlahnya dan sarankan pengguna memperbaiki format kolom di Excel.
- Insight harus berdasarkan data; hindari saran generik seperti "tingkatkan pemasaran".
- Jangan mengirim isi file pengguna ke layanan eksternal.

## Privasi data pembeli (wajib)

Ekspor marketplace sering memuat nama penerima, nomor telepon, dan alamat. Script tidak membaca kolom itu.

- **Teks untuk grup tim/karyawan = angka agregat saja.** Tanpa nama, nomor HP, alamat, atau nomor pesanan
  pembeli. Pakai `ringkasan_siap_tempel` (sudah agregat). Bila tim packing butuh daftar pesanan, arahkan ke
  halaman pesanan di Seller Center, bukan disalin ke grup.
- **Permintaan "daftar pelanggan buat promo" / "kirim promo ke semua pembeli"** dari file ekspor:
  - Data pembeli marketplace diberikan untuk **memenuhi pesanan** (kirim barang), bukan untuk promosi di luar
    platform. Anggap **default: pembeli marketplace BELUM memberi izin** dihubungi untuk promo (UU PDP No. 27/2022;
    kebijakan platform juga umumnya melarang memakai data pembeli di luar platform).
  - Jangan membuat file nama + nomor HP untuk promo dari ekspor marketplace. Daftar promo hanya berisi pelanggan
    yang **sudah menyatakan setuju (opt-in)**, mis. pernah chat langsung dan bilang mau dikabari promo, mengisi
    formulir, atau bergabung sendiri ke saluran toko. Catat persetujuannya (kapan & lewat apa) — skill `crm-wa`
    punya kolom untuk itu.
  - Untuk pembeli marketplace yang belum opt-in, tawarkan jalur di dalam platform: voucher toko, fitur
    promo resmi marketplace yang berbasis pengikut/opt-in (dipakai manual oleh penjual), atau ajakan "ikuti toko" di kemasan/kartu ucapan.
  - **Tanpa broadcast/blast** lewat alat apa pun (termasuk OpenClaw, WhatsApp Business, dan fitur chat broadcast di dalam marketplace seperti Shopee Chat Broadcast, yang berisiko melanggar kebijakan platform) ke kontak yang
    belum opt-in. Ke pelanggan yang sudah opt-in: siapkan draf pesan, pemilik kirim **satu per satu**.
  - Jangan menyimpan atau meneruskan nomor/nama pembeli ke tempat lain (memori, grup, file baru) tanpa diminta
    jelas oleh pemilik, dan sebutkan lokasi file bila memang dibuat.
