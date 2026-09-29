---
name: arus-kas-13minggu
description: Membuat proyeksi arus kas 13 minggu (cash flow forecast mingguan) untuk UMKM dari saldo awal, rencana penerimaan (penjualan tunai, pelunasan piutang) dan pengeluaran (bahan, gaji, sewa, cicilan, pajak), lalu menandai minggu kas negatif/di bawah batas aman, menyimulasikan 3–5 opsi tindakan konkret, dan menghasilkan CSV siap buka di Excel. Gunakan saat pengguna tanya "uang saya cukup sampai kapan", minta proyeksi/rencana kas, cash flow 3 bulan ke depan, 13-week cash flow, cash runway, atau khawatir kas minus. Bukan untuk laporan laba rugi/neraca atau rekap penjualan masa lalu.
---

# Proyeksi Arus Kas 13 Minggu

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Menjawab pertanyaan pemilik usaha: **"Minggu ke berapa uang saya akan kurang, berapa kurangnya, dan apa yang bisa saya lakukan sekarang?"** Hasilnya tabel saldo per minggu, tanda bahaya, opsi tindakan beserta angka dampaknya, dan file CSV untuk Excel.

## Kapan digunakan
- "Tolong buatkan proyeksi kas 3 bulan ke depan", "cash flow mingguan", "13-week cash flow".
- Pengguna khawatir tidak bisa bayar gaji/THR/supplier/cicilan di minggu tertentu.
- Mau cek dampak keputusan: beli alat, buka cabang, ambil pesanan besar dengan termin.

## Kapan TIDAK digunakan
- Laporan laba rugi / neraca dari transaksi yang sudah terjadi → skill `laporan-keuangan-emkm`.
- Rekap omzet/produk terlaris dari data penjualan lalu → `rekap-penjualan-csv`.
- Menagih pelanggan (menulis pesan tagihan) → `tagih-piutang` (boleh ditawarkan setelah opsi "percepat tagihan").
- Simulasi cicilan pinjaman/KUR → `pengajuan-kur`. Mencocokkan mutasi bank → `rekonsiliasi-bank`.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Saldo kas + bank hari ini | Ya | — (tanyakan) |
| Perkiraan penjualan tunai per minggu | Ya | — (tanyakan; boleh rata-rata) |
| Piutang yang akan dibayar pelanggan (siapa, berapa, kapan) | Tidak | Tidak ada piutang |
| Pengeluaran rutin: bahan/supplier, gaji (tanggal gajian), sewa, cicilan, pajak, listrik/operasional | Ya | — (tanyakan) |
| Pengeluaran sekali: renovasi, alat, THR, iklan besar | Tidak | Tidak ada |
| Batas aman (saldo minimum yang diinginkan) | Tidak | Rata-rata pengeluaran 1 minggu (sebutkan sebagai asumsi) |
| Tanggal mulai minggu 1 | Tidak | Senin terdekat berikutnya dari hari ini |

Bisa diterima dalam bentuk: tabel/CSV/Excel yang disimpan sebagai CSV, daftar tempel, atau jawaban tanya-jawab.
Jika info wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor), contoh:
1. Berapa total uang di kas + rekening hari ini?
2. Kira-kira penjualan tunai/transfer langsung per minggu berapa?
3. Ada tagihan pelanggan yang akan dibayar? (nama, nominal, perkiraan tanggal)
4. Pengeluaran rutin: belanja bahan per minggu, gaji (tanggal berapa, total), sewa, cicilan, pajak, lain-lain?
5. Ada pengeluaran besar sekali saja dalam 3 bulan ke depan (THR, renovasi, alat)?

## Langkah kerja
1. **Susun CSV rencana** di folder kerja pengguna (mis. `rencana-kas.csv`), satu baris per pos, pemisah `;`:
   ```
   minggu;jenis;kategori;nominal;keterangan;kritis
   semua;masuk;Penjualan tunai;12.000.000;;
   3;masuk;Pelunasan piutang;8.500.000;CV Maju;
   semua;keluar;Bahan baku (supplier);7.000.000;;ya
   tgl:25;keluar;Gaji karyawan;18.000.000;6 orang;ya
   tgl:1;keluar;Sewa ruko;6.500.000;;ya
   5;keluar;Renovasi etalase;9.000.000;;tidak
   ```
   - Kolom `minggu`: `3` / `minggu 3` / `minggu ke-3` | `1-13` | `2,6,10` | `semua` | `setiap 2` | `setiap 4 mulai 2` | `tgl:25` (minggu yang memuat tanggal 25 tiap bulan; tanggal 29–31 otomatis jadi akhir bulan di bulan pendek; tanggal yang jatuh sebelum minggu 1 tidak dihitung).
   - `jenis`: `masuk`/`keluar` (jika kosong ditebak dari nama kategori).
   - `kritis`: `ya` (wajib dibayar tepat waktu) / `tidak` (bisa ditunda). Kosong → ditebak dari kata kunci. **Gaji, upah, THR, bonus karyawan, cicilan, angsuran, leasing, kredit, pajak, BPJS selalu kritis** (walau diisi `tidak`) dan tidak pernah ikut simulasi "tunda". Pos yang ditebak tidak kritis dilaporkan di `peringatan` → konfirmasi ke pengguna. Pembayaran bahan/stok ikut simulasi "termin supplier" walau kolom `kritis` kosong, karena termin adalah negosiasi, bukan menunda sepihak.
   - Beri kata **"piutang/pelunasan/tagihan"** pada penerimaan dari pelanggan, dan **"bahan/supplier/stok"** pada pembayaran pemasok, agar simulasi opsi mengenalinya.
   - Template kosong: `templates/rencana-kas.csv`.
2. **Jalankan script** (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/proyeksi_kas.py rencana-kas.csv \
     --saldo-awal "Rp 20.000.000" --mulai 2026-10-05 --batas-aman "Rp 10.000.000" \
     --output-csv proyeksi-kas-13-minggu.csv
   ```
   - Tambah `--format teks` untuk melihat tabel cepat; default JSON (dipakai untuk menulis jawaban).
   - `--pemisah ,` jika Excel pengguna berbahasa Inggris (default `;` untuk Excel berbahasa Indonesia). File selalu UTF-8 dengan BOM agar huruf tidak rusak di Excel.
   - Opsi simulasi: `--geser-piutang 2`, `--geser-supplier 2`, `--geser-nonkritis 4` (minggu).
   - Horizon lain: `--jumlah-minggu N` (4–26), mis. "sampai Lebaran" atau "sampai akhir tahun" → hitung jumlah minggu dari tanggal mulai. Judul output menyesuaikan ("Proyeksi Kas N Minggu").
3. **Baca hasil**: `ringkasan` (minggu negatif, minggu di bawah batas, saldo terendah, tambahan dana dibutuhkan, `arus_kas_bersih`, `defisit_struktural`), `simulasi_opsi` (dampak tiap opsi + `rincian_digeser` + `saldo_setelah_kewajiban_tertunda` + `hanya_menunda`), `baris_dilewati`, `peringatan`.
4. **Tulis jawaban** dengan format di bawah. Angka hanya dari output script.
5. **Susun 3–5 opsi tindakan konkret** (lihat `references/opsi-tindakan.md`), urutkan dari dampak terbesar & paling mudah. Setiap opsi wajib menyebut: siapa/pos apa, nominal, dari minggu berapa ke minggu berapa, dan hasil simulasinya. Jangan beri saran generik.
   - Opsi dengan `jatuh_setelah_horizon` > 0: selalu sebut nominal yang pindah ke setelah minggu terakhir dan `saldo_setelah_kewajiban_tertunda`.
   - Opsi berlabel **`hanya_menunda: true` DILARANG ditulis sebagai solusi**. Boleh disebut hanya sebagai "menunda masalah", dengan saldo setelah kewajiban tertunda yang negatif.
   - Jika `defisit_struktural` = true, opsi geser jadwal saja tidak cukup: wajib ada minimal 1 opsi yang menambah pemasukan atau memangkas biaya rutin (dengan angka yang dijalankan ulang).
6. Jika pengguna memilih satu opsi, ubah CSV (geser minggunya) dan **jalankan ulang** untuk menunjukkan tabel "sesudah tindakan".
7. Periksa checklist sebelum mengirim.

**Fallback tanpa Python** (beri tahu pengguna bahwa hasil dihitung manual): untuk setiap minggu w,
`Saldo akhir(w) = Saldo akhir(w−1) + Total masuk(w) − Total keluar(w)`, dengan Saldo akhir(0) = saldo awal.
Status: saldo < 0 → NEGATIF; 0 ≤ saldo < batas aman → DI BAWAH BATAS; selain itu AMAN.
Tambahan dana agar tidak negatif = |saldo terendah| bila negatif. Bulatkan setiap nominal ke rupiah penuh.

## Format output
```
## Proyeksi Kas 13 Minggu (<tgl mulai> – <tgl akhir>)
Saldo awal Rp … · Batas aman Rp … (<diisi Anda / asumsi>)

| Mg | Periode | Masuk | Keluar | Saldo akhir | Status |
|---|---|---:|---:|---:|---|
| 1 | 5–11 Okt | Rp … | Rp … | Rp … | 🟢 Aman |
… (13 baris; 🟡 Di bawah batas, 🔴 NEGATIF)

### Kesimpulan
- Titik paling kritis: minggu <x> (<periode>), saldo Rp … karena <pos besar penyebabnya>.
- Minggu negatif: … · Di bawah batas aman: …
- Tambahan dana agar tidak minus: Rp … (agar di atas batas aman: Rp …)
- Arus kas <N> minggu: masuk Rp … vs keluar Rp … → <naik/turun> Rp … (rata-rata Rp …/minggu). **Bila turun: ini masalah rutin (defisit struktural), bukan hanya soal jadwal.**
- Pos rutin yang jatuh tak lama setelah minggu terakhir (dari `peringatan`), bila ada.

### Opsi tindakan (urut dari dampak terbesar)
1. **<Tindakan spesifik>** — <siapa/pos, nominal, minggu x → y>. Hasil simulasi: saldo terendah jadi Rp …, minggu negatif jadi <…>. Cara: <1 kalimat / contoh kalimat negosiasi>.
2. …
(3–5 opsi)

### File Excel
proyeksi-kas-13-minggu.csv — buka di Excel/Google Sheets.

Asumsi: … · Pembulatan: setiap nominal dibulatkan ke rupiah penuh.
Catatan: proyeksi berdasarkan perkiraan Anda; perbarui tiap minggu dengan angka aktual.
```
Jika semua minggu aman, tetap tampilkan tabel, lalu beri 2–3 saran menjaga kas (mis. dana cadangan, jadwal belanja) — jangan mengarang masalah.

## Contoh
**Input pengguna:** "Kas saya sekarang 20 juta. Jualan tunai sekitar 12 juta seminggu. Gaji 18 juta tiap tanggal 25, sewa 6,5 juta tiap tanggal 1, cicilan bank 4,25 juta tiap tanggal 10, belanja bahan 7 juta/minggu. PT Sinar mau bayar 15 juta awal Desember. Mau renovasi etalase 9 juta awal November. Aman nggak sampai akhir tahun?"

**Output (ringkas):**
```
Titik paling kritis: minggu 8 (23–29 Nov), saldo tinggal Rp 0 — gajian Rp 18.000.000 jatuh
seminggu sebelum PT Sinar membayar Rp 15.000.000 (minggu 9).
Batas aman (asumsi, rata-rata pengeluaran 1 minggu): Rp 14.326.923 → 10 dari 13 minggu di bawahnya.

Arus kas 13 minggu: masuk Rp 171.000.000 vs keluar Rp 186.250.000 → turun Rp 15.250.000
(±Rp 1.173.077/minggu). Ini defisit rutin: menggeser jadwal saja tidak cukup.

Opsi 1. Negosiasi termin bahan mundur 2 minggu → saldo terendah selama 13 minggu jadi Rp 14.000.000.
        Tetapi Rp 14.000.000 tagihan bahan pindah ke setelah minggu 13 (bukan hilang);
        setelah dibayar, saldo tinggal Rp 4.750.000.
Opsi 2. Minta PT Sinar melunasi Rp 15.000.000 di minggu 7 (bukan 9), tawarkan potongan kecil
        → minggu 8 tidak lagi habis; saldo terendah Rp 4.750.000 (minggu 13).
Opsi 3. Tunda renovasi etalase Rp 9.000.000 dari minggu 5 ke minggu 9 → saldo minggu 8 jadi Rp 9.000.000.
Gabungan ketiganya → saldo terendah Rp 18.750.000 selama 13 minggu, tetapi Rp 14.000.000 bahan tetap
        harus dibayar setelah minggu 13 → saldo riil Rp 4.750.000 (di bawah batas aman).
Opsi 4. Karena defisit rutin, tambah pemasukan atau pangkas biaya ±Rp 1.173.077/minggu
        (mis. naikkan harga/penjualan, kurangi pembelian bahan yang berlebih) — jalankan ulang untuk angkanya.
Catatan: cicilan bank Rp 4.250.000 jatuh 10 Jan 2027, 7 hari setelah minggu 13.
```

## Checklist sebelum mengirim hasil
- [ ] Semua angka berasal dari output script (atau fallback manual yang disebutkan).
- [ ] Minggu negatif & di bawah batas disebut jelas beserta penyebab utamanya (pos terbesar minggu itu).
- [ ] 3–5 opsi, masing-masing ada nominal, minggu asal → tujuan, dan hasil simulasi.
- [ ] Peringatan "jatuh setelah minggu 13" disampaikan beserta `saldo_setelah_kewajiban_tertunda` — menunda bukan menghapus kewajiban.
- [ ] Tidak ada opsi berlabel `hanya_menunda` yang ditulis sebagai solusi.
- [ ] Bila `defisit_struktural` = true: disebut di Kesimpulan (masuk vs keluar, turun Rp …) dan ada opsi tambah pemasukan/pangkas biaya rutin.
- [ ] Pos yang DITEBAK tidak kritis sudah dikonfirmasi/diberitahukan; gaji, cicilan, pajak, THR tidak pernah disarankan ditunda.
- [ ] Penempatan tanggal dijelaskan bila relevan (tgl 29–31 di bulan pendek → akhir bulan; pos bulan berikutnya yang jatuh tepat setelah minggu terakhir).
- [ ] Asumsi (batas aman default, tanggal mulai, penjualan rata) disebut.
- [ ] Baris yang dilewati & isi `peringatan` script disampaikan.
- [ ] Format Rupiah `Rp 1.250.000`; nama file CSV disebut.

## Batasan & penanganan error
- Proyeksi hanya sebaik perkiraan pengguna; sarankan skenario "penjualan turun 20%" bila usaha musiman (buat CSV kedua, jalankan ulang, bandingkan).
- Script keluar dengan kode ≠ 0 dan pesan JSON bila file tidak ada, kolom wajib hilang, saldo awal tak terbaca, atau semua baris rusak — sampaikan pesannya dengan bahasa sederhana dan minta data yang benar.
- Baris dengan nominal/minggu tak terbaca dilewati dan dilaporkan; tanyakan ke pengguna jika pos itu penting.
- Pinjaman sebagai opsi: sebut hanya sebagai pilihan terakhir dengan jumlah = tambahan dana dibutuhkan; jangan merekomendasikan pinjol ilegal; untuk simulasi cicilan arahkan ke `pengajuan-kur`.
- Bukan nasihat keuangan profesional; untuk keputusan besar (PHK, jual aset, restrukturisasi utang) sarankan diskusi dengan akuntan/konsultan.
- Data keuangan pengguna tidak dikirim ke mana pun; script berjalan lokal tanpa internet.
