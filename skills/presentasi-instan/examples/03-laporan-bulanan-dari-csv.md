# Contoh 03 — Laporan bulanan ke owner dari file CSV (permintaan singkat)

## Skenario
S3, permintaan normal tapi singkat/malas. Admin toko catering & frozen food mengirim file ekspor penjualan Agustus (`penjualan-agustus-2026.csv`, 138 baris, kolom `Tanggal,Produk,Kategori,Qty,Harga Satuan,Total`, nominal berformat `Rp 175.000`) dan menyebut target.

## Input pengguna
```
bikinin dong slide laporan bulanan agustus buat owner dari file penjualan-agustus-2026.csv ini, target kita 45 juta
```

## Output
File nyata: [`laporan-agustus-2026.html`](laporan-agustus-2026.html) (8 slide, palet "Putih Minimalis", font Verdana/Tahoma). Data sumber: [`penjualan-agustus-2026.csv`](penjualan-agustus-2026.csv) (fiktif).

Langkah agent: sesuai bagian "Integrasi dengan skill lain", angka dihitung dengan skill `rekap-penjualan-csv` (`scripts/rekap.py --kolom-tanggal Tanggal --kolom-produk Produk --kolom-qty Qty --kolom-total Total --top 7`), lalu dimasukkan ke template `laporan-bulanan.md`.

Susunan slide:
1. Sampul — Laporan Bulanan · Penjualan Agustus 2026 · `[isi nama usaha]`
2. Ringkasan — omzet **Rp 41.190.000** = **91,5%** dari target Rp 45.000.000; kurang **Rp 3.810.000**; catering 77,8%; minggu kedua paling ramai Rp 11.229.000
3. Capaian vs target — 3 kartu + rata-rata Rp 1.328.710/hari (138 transaksi, 31 hari)
4. Rincian per produk — tabel 7 produk + total (qty 1.175, Rp 41.190.000, 100%) — lihat `ss-01-laporan-slide4-laptop.png`
5. Kategori & minggu — Catering Rp 32.039.000 (77,8%), Frozen Rp 9.151.000 (22,2%); per minggu Rp 8.804.000 / Rp 11.229.000 / Rp 8.483.000 / Rp 8.143.000 / Rp 4.531.000 (29–31 Agustus, 3 hari)
6. Kendala — frozen hanya 22,2%; hari terendah 4 Agustus Rp 204.000, terbaik 14 Agustus Rp 3.135.000; `[isi dari tim]`
7. Rencana September — 3 baris `[isi rencana + penanggung jawab]`
8. Penutup — "Agustus: 91,5% dari target"

Balasan ke pengguna:
```
Presentasi Laporan Penjualan Agustus 2026 sudah jadi: laporan-agustus-2026.html (8 slide)

Cara pakai:
- Buka file-nya dua kali klik — bisa di laptop maupun HP, tanpa internet.
- Navigasi: panah kiri/kanan, geser jari, atau tombol ‹ ›.
- Cetak jadi PDF: Ctrl+P / Cmd+P → Simpan sebagai PDF → Lanskap.

Asumsi yang dipakai: palet "Putih Minimalis"; semua 138 baris terbaca, tidak ada status batal/retur di file; "minggu" = tanggal 1–7, 8–14, dst.
Bagian yang masih perlu Anda lengkapi: nama usaha, penyebab kendala dari tim, 3 rencana September + penanggung jawab.
Hasil cek otomatis: LULUS, tanpa peringatan.
```

## Catatan penguji
- **Angka diverifikasi independen** dengan script Python terpisah (tanpa `rekap.py`): total 41.190.000 ✔, tiap baris Qty×Harga = Total ✔, 7 produk & persentase ✔, kategori ✔, 5 kelompok minggu berjumlah 41.190.000 ✔, hari terbaik/terendah ✔, 91,5% & selisih 3.810.000 ✔.
- **Bagus:** tidak mengarang kendala/rencana; tabel 8 baris tetap muat (tanpa luber) pada 28px.
- **Kurang:** SKILL.md tidak punya langkah eksplisit "jika pengguna memberi CSV, jalankan dulu `rekap-penjualan-csv`" — hanya bagian integrasi opsional. Font "Verdana/Tahoma" tidak ada di Linux/Android; tampil dengan font cadangan (aman, tapi klaim "terpasang bawaan di … Linux" di `aturan-desain.md` #4 tidak akurat).
- **Cacat kerangka:** PDF A4 lanskap memotong kolom "Porsi" seluruhnya (lihat `ss-02-cacat-pdf-a4-lanskap-kolom-terpotong.png`).
