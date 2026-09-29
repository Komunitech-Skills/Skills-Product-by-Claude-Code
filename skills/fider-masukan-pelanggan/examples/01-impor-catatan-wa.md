# 01 - Impor catatan WA menjadi usulan (dijalankan pada Fider v0.38.0 asli, 2026-09-29)

**Permintaan:** "Ini catatan WA minggu ini, jadikan usulan di Fider."

Berkas `catatan.txt` (data fiktif):
```
- Pelanggan minta bisa bayar pakai QRIS (Bu Rina 081234567890)
- Tolong ada notifikasi WA kalau pesanan sudah dikirim, minta 3 orang

Ongkir ke luar Jawa sering salah hitung. Kontak: budi@contoh.id

Tambah pembayaran QRIS
```

**Langkah 1 - pratinjau** (`impor catatan.txt --sumber "WhatsApp pelanggan"`): agent menampilkan 4 butir; 3 ditandai BUAT, 1 ("Tambah pembayaran QRIS") ditandai LEWATI karena sama dengan pos #1 yang sudah ada; nomor HP dan email tertulis `[nomor disembunyikan]` / `[email disembunyikan]`. Diakhiri "PRATINJAU - BELUM ADA YANG DITULIS". Belum ada yang tertulis di Fider.

**Langkah 2 - pemilik menjawab "ya"** → `impor catatan.txt --sumber "WhatsApp pelanggan" --ya --hapus-suara-saya`:
```
SELESAI: 3 pos dibuat, 1 dilewati (kemungkinan duplikat).
- #3 Pelanggan minta bisa bayar pakai QRIS (Bu Rina [nomor disembunyikan])
- #4 Tolong ada notifikasi WA kalau pesanan sudah dikirim, minta 3 orang
- #5 Ongkir ke luar Jawa sering salah hitung. Kontak: [email disembunyikan]
```
**Catatan pembuat:** nama "Bu Rina" tidak disamarkan otomatis (hanya nomor HP/email); agent seharusnya menyarankan membuang nama dari judul sebelum "ya". #3 kemudian digabung ke #1 (lihat 02).
