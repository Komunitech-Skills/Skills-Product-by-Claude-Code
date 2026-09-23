# 03 — Permintaan singkat, data belum ada (tidak mengirim angka nol)

**Skenario:** S3 (normal, singkat/malas). Pengguna menyebut hampir semua info, tetapi folder datanya ternyata masih kosong.

**Input pengguna (persis):**
> bikinin dong rekap penjualan tiap pagi jam 7, filenya di Dokumen/Laporan-AI/masuk/penjualan, kirim ke telegram saya 123456789

**Perintah yang dijalankan agent:**
```bash
python3 scripts/cek_sumber_data.py --folder "Dokumen/Laporan-AI/masuk/penjualan" --pola "*.csv" --label "penjualan" --maks-umur-hari 1
# exit code 1, "siap": false, "status": "tidak_ada_file"
```

## Output
```
Saya cek dulu folder datanya sebelum membuat jadwal:

Belum ada file penjualan (pola *.csv) di folder Dokumen/Laporan-AI/masuk/penjualan.
Ekspor data penjualan dari sumbernya (kasir/marketplace/bank/aplikasi stok) sebagai CSV,
taruh di folder itu, lalu jalankan lagi. Laporan TIDAK dibuat (tidak ada angka nol palsu).

Jadi jadwalnya belum saya buat, supaya Anda tidak menerima laporan "omzet Rp 0" yang salah.
Setelah file ekspor pertama ada di folder itu, bilang "sudah", nanti saya:
1. hitung contoh laporan pertama dari file itu dan tunjukkan ke Anda,
2. buat jadwal harian 07:00 WIB ke Telegram 123456789 setelah Anda setuju.

Asumsi yang saya pakai: jadwal setiap hari 07:00 WIB (Asia/Jakarta), isi laporan =
penjualan kemarin (total omzet, jumlah transaksi, 3 produk terlaris).
```

## Catatan penguji
- Sesuai Langkah 2: proses berhenti, pesan script ditampilkan apa adanya. Tidak ada jadwal dibuat.
- Uji tepi `cek_sumber_data.py` (semua benar): folder tidak ada → `folder_tidak_ada`; file 0 byte → `file_kosong`; hanya judul → `tidak_ada_baris_data`; baris `;;;` saja → `tidak_ada_baris_data`; file 53 hari → `siap: true` + peringatan umur. Bila semua baris "Batal", `rekap.py` gagal dengan "Tidak ada baris valid" (exit 1) → juga tidak mengirim nol.
- Celah: file **lama** (mis. ekspor minggu lalu yang lupa diganti, umur 7 hari dengan `--maks-umur-hari 10` di resep mingguan) lolos tanpa peringatan → angka minggu lalu bisa terkirim ulang sebagai laporan minggu ini. Lihat HASIL-UJI.md S-4.
- Bagus: asumsi default disebutkan (jam, zona waktu, isi laporan).
