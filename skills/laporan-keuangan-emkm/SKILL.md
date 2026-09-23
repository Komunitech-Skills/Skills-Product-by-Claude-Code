---
name: laporan-keuangan-emkm
description: Menyusun laporan keuangan UMKM sesuai SAK EMKM (Laporan Laba Rugi, Laporan Posisi Keuangan/neraca, Catatan atas Laporan Keuangan) dari buku kas atau daftar transaksi CSV/tabel tempel, lengkap dengan cek neraca seimbang, pemisahan prive, dan ringkasan bahasa awam. Gunakan saat pengguna minta laporan keuangan, laba rugi, neraca, "untung berapa bulan ini", laporan untuk pengajuan KUR/bank dari catatan kas (financial statements, profit and loss, balance sheet for small business). Bukan untuk rekap omzet produk (pakai rekap-penjualan-csv) atau hitung pajak (pph-final-umkm).
---

# Laporan Keuangan SAK EMKM dari Buku Kas

## Tujuan
Mengubah catatan uang masuk-keluar sehari-hari menjadi laporan keuangan standar SAK EMKM yang rapi, seimbang, dan dijelaskan dengan bahasa awam, sehingga pemilik tahu untung/ruginya dan punya dokumen untuk bank, investor, atau arsip usaha.

## Kapan digunakan
- Pengguna mengirim buku kas / catatan transaksi (CSV, tempelan tabel dari Excel/WA/Notes) dan minta laporan keuangan, laba rugi, neraca, atau "untung berapa".
- Pengguna butuh laporan keuangan sederhana untuk pengajuan KUR/kredit, proposal, atau tutup buku bulanan/tahunan.
- Pengguna bingung memisahkan uang pribadi dan uang usaha (prive).

## Kapan TIDAK digunakan
- Hanya ingin rekap omzet/produk terlaris → pakai skill `rekap-penjualan-csv`.
- Menghitung PPh final 0,5% / PPN → pakai `pph-final-umkm` / `hitung-ppn` (skill ini hanya mencatat pajak yang sudah dibayar).
- Menghitung HPP per produk / harga jual → `hitung-hpp` / `harga-jual-marketplace`.
- Proyeksi kas ke depan ("uang cukup sampai kapan") → skill proyeksi arus kas (mis. `arus-kas-13minggu` bila tersedia). Skill ini melaporkan periode yang sudah lewat.
- Laporan untuk PT/perusahaan wajib audit, konsolidasi, atau yang memakai SAK EP/SAK Indonesia → sarankan akuntan publik/konsultan.
- Menyusun laporan pajak (SPT) → arahkan ke konsultan pajak/DJP.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Daftar transaksi: tanggal, keterangan, uang masuk, uang keluar (kolom kategori opsional) | Ya | — (minta file/tempelan) |
| Nama usaha | Tidak | `[Nama Usaha]` |
| Saldo kas awal periode | Tidak* | Baris "saldo awal" di file; jika tidak ada Rp 0 |
| Stok/persediaan awal & akhir (hasil hitung stok) | Tidak* | Stok akhir = stok awal (HPP = total pembelian) |
| Piutang awal & akhir (pelanggan belum bayar) | Tidak | Rp 0 / tidak ada penjualan tempo baru |
| Utang ke pemasok awal & akhir, utang bank/pinjaman awal | Tidak | Rp 0 |
| Nilai aset tetap awal (peralatan, kendaraan) + umur manfaat | Tidak | Rp 0, penyusutan tidak dihitung |
| Modal awal | Tidak | Dihitung dari aset awal − utang awal |
| Saldo kas nyata di akhir periode (uang di laci + rekening) | Tidak | Tidak dicek |

\*Sangat memengaruhi hasil. Jika belum ada, **tanyakan sekali** dalam satu pesan (maks 5 pertanyaan bernomor), contoh:
1. Berapa uang kas + saldo rekening usaha di awal periode?
2. Berapa nilai stok barang/bahan di awal dan di akhir periode (kira-kira)?
3. Adakah pelanggan yang belum bayar atau utang ke pemasok/bank? Berapa?
4. Punya peralatan/kendaraan usaha? Nilai kira-kira dan dipakai berapa tahun lagi?
5. Nama usaha untuk judul laporan?

Jika pengguna ingin cepat ("langsung saja"), jalankan dengan default dan tampilkan bagian **Asumsi** dari output script.

## Langkah kerja
1. **Siapkan data.** Jika pengguna menempel tabel di chat, simpan persis apa adanya ke file sementara (mis. `buku-kas.csv` atau `.md` untuk tabel `|`). Jangan mengetik ulang/mengubah angka. File Excel (.xlsx) → minta pengguna simpan sebagai CSV.
2. **Jalankan script** (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/laporan_emkm.py buku-kas.csv \
     --nama-usaha "Dapur Bu Sri" --kas-awal "Rp 3.000.000" \
     --persediaan-awal 0 --persediaan-akhir "Rp 200.000" --umur-aset-tahun 4
   ```
   Opsi penting (semua nominal boleh format Indonesia: `Rp 1.500.000`, `1,5jt`, `150rb`):
   - Saldo: `--kas-awal --piutang-awal --piutang-akhir --persediaan-awal --persediaan-akhir --aset-tetap-awal --utang-usaha-awal --utang-usaha-akhir --utang-bank-awal --modal-awal --kas-akhir-aktual`
   - Penyusutan: `--umur-aset-tahun 4` (garis lurus) **atau** `--penyusutan "Rp 150.000"`.
   - Periode: `--periode-awal 2026-02-01 --periode-akhir 2026-02-28`; tren: `--rekap bulan|kuartal|tahun`.
     **Laporan satu bulan dari file multi-bulan:** saldo awal yang diberikan (atau baris "saldo awal" di file) dianggap per **awal data file**, lalu script **menggulirkan** kas, piutang, utang, kasbon, aset tetap, dan modal dengan transaksi sebelum periode. Jika pengguna memberi saldo per tanggal awal periode, tambahkan `--saldo-awal-per awal-periode`. Stok awal periode tidak bisa digulirkan, jadi tanyakan stok per tanggal awal periode.
   - Angsuran pinjaman: `--bunga <baris>=<nominal bunga>` memecah angsuran menjadi pokok (mengurangi utang) + bunga (beban keuangan); `--bunga <baris>=0` = pokok saja.
   - Selisih kas yang sudah dikonfirmasi pemilik: `--kas-akhir-aktual "Rp ..." --catat-selisih-kas` (dicatat sebagai beban/pendapatan selisih kas).
   - Kolom tidak terdeteksi: `--kolom-tanggal "Tgl" --kolom-masuk "Debet"` dst. Kolom Debit/Kredit wajib ditegaskan (artinya bisa terbalik antara buku kas dan mutasi bank).
   - `--format json` untuk angka mentah; default `teks` (Markdown siap tempel).
3. **Baca bagian "Perlu dicek".** Gabungkan **transaksi belum terklasifikasi** dan **"Pertanyaan untuk pemilik"** (angsuran tanpa rincian bunga, PB1/PBJT, angka mustahil seperti utang/HPP negatif atau kas minus) menjadi **satu pesan** bernomor. Beri pilihan jawaban yang masuk akal. Setelah dijawab, jalankan ulang dengan `--tetapkan <baris>=<kode>`, `--bunga <baris>=<nominal>`, saldo awal yang diperbaiki, atau file `--pemetaan` (lihat `templates/pemetaan-kustom.contoh.json`). Daftar kode: `--daftar-kategori`. Selama status SEMENTARA, jangan sajikan laporan sebagai final.
4. **Cek neraca.** Jika TIDAK SEIMBANG, jelaskan selisih dan penyebab yang dilaporkan script; jangan "memaksa" angka agar seimbang. Jika selisihnya berasal dari kas nyata vs buku dan pemilik mengonfirmasi (mis. uang hilang/kembalian), tawarkan menjalankan ulang dengan `--catat-selisih-kas`. Tanda ⚠ di cek keseimbangan berarti ada angka mustahil; selesaikan dulu pertanyaannya.
5. **Sajikan hasil** memakai format output di bawah. Semua angka HARUS dari output script. Lengkapi placeholder `[Lengkapi: ...]` di Catatan jika pengguna sudah memberi infonya.
6. Periksa checklist sebelum mengirim.

### Aturan klasifikasi penting (dijalankan script, jelaskan bila ditanya)
- **Prive** (ambil pribadi, belanja rumah tangga, SPP anak, "gaji pemilik") bukan beban: mengurangi modal, tidak mengurangi laba.
- **Setoran modal, pinjaman diterima, cicilan pokok, bayar utang pemasok, terima piutang, beli aset tetap, pindah dana antar rekening** bukan pendapatan/beban: hanya mengubah pos neraca.
- **Bunga pinjaman & biaya bank** = beban keuangan; **PPh** = beban pajak penghasilan (dipisah sesuai SAK EMKM). "PPN" sengaja tidak diklasifikasi otomatis (tanyakan). **Angsuran/cicilan** selalu ditanyakan porsi bunganya kecuali ada baris bunga di bulan yang sama. **PB1/PBJT** (pajak restoran/hotel) dicatat sebagai pajak daerah dan ditanyakan apakah dipungut dari pembeli.
- **Kasbon karyawan** = piutang lain-lain (aset), bukan beban; pelunasan/potong kasbon mengurangi piutang itu.
- Aturan lengkap & kata kunci: `references/pemetaan-kategori.md`.

### Fallback jika Python tidak bisa dijalankan
Beri tahu pengguna bahwa hasil dihitung manual (belum diverifikasi script), lalu ikuti `references/hitung-manual.md`. Rumus inti:
- Pendapatan bersih = penjualan tunai + (piutang akhir − piutang awal + penerimaan piutang) − retur
- HPP = persediaan awal + pembelian (tunai + tempo) − persediaan akhir
- Laba bersih = pendapatan bersih − HPP − beban usaha (termasuk penyusutan) + pendapatan lain − beban keuangan − beban PPh
- Kas akhir = kas awal + total uang masuk − total uang keluar
- Modal akhir = modal awal + setoran modal + laba bersih − prive
- Cek: kas + piutang + persediaan + aset tetap (nilai buku) = utang usaha + utang bank + modal akhir
- Pembulatan: setiap nominal dibulatkan ke rupiah terdekat (0,5 ke atas) sebelum dijumlahkan.

## Format output
```
# Laporan Keuangan <Nama Usaha>
Periode <tgl> s.d. <tgl> · mengacu SAK EMKM · status: LENGKAP/SEMENTARA

## Ringkasan untuk pemilik        ← 3–6 kalimat awam: untung/rugi, margin, pengeluaran terbesar, prive, kas akhir
## 1. Laporan Laba Rugi           ← tabel
## 2. Laporan Posisi Keuangan     ← tabel + baris cek keseimbangan (✔/✘ + selisih)
## 3. Catatan atas Laporan Keuangan (ringkas)
## Tren per periode               ← jika > 1 bulan
## Perlu dicek                    ← transaksi tak terklasifikasi, baris rusak, peringatan
## Asumsi yang dipakai
Disclaimer: bukan laporan audit, bukan nasihat pajak.
```
Tambahkan di akhir 2–3 **saran tindakan** berbasis angka (mis. "biaya gaji 60% dari total biaya; ...") dan tawarkan: versi PDF/Word, laporan per bulan, atau menjalankan ulang setelah pengguna menjawab pertanyaan.

## Contoh
**Input pengguna:** "Tolong buatkan laporan keuangan Jan–Mar dari buku kas ini, kas awal 3 juta, stok akhir sekitar 200 ribu, oven baru dipakai 4 tahun" + file `normal.csv` (20 transaksi).

**Output (dipotong):**
```
Usaha kamu UNTUNG Rp 2.185.417 selama 1 Januari 2026 s.d. 31 Maret 2026. Dari penjualan bersih
Rp 11.000.000, yang tersisa jadi laba sekitar 19,9% ... Pengeluaran terbesar: beban gaji & upah
sebesar Rp 5.400.000 (59,9% dari total biaya). ...
| Beban pokok penjualan | (Rp 1.350.000) |
| **LABA (RUGI) BERSIH** | **Rp 2.185.417** |
✔ Cek keseimbangan: Aset = Liabilitas + Ekuitas (Rp 5.185.417). Neraca seimbang.
```

**Input tidak lengkap:** "bikin neraca dong" tanpa data → minta daftar transaksi + ajukan pertanyaan saldo awal (daftar bernomor di atas), sekaligus tawarkan `templates/buku-kas-template.csv`.

## Checklist sebelum mengirim hasil
- [ ] Semua angka berasal dari output script (atau hitungan manual yang ditandai jelas).
- [ ] Format rupiah `Rp 1.250.000`; pengurang dalam kurung.
- [ ] Prive tidak tercatat sebagai beban; setoran modal/pinjaman tidak tercatat sebagai pendapatan.
- [ ] Status SEMENTARA dijelaskan + transaksi tak terklasifikasi dan "Pertanyaan untuk pemilik" ditanyakan (bukan ditebak diam-diam).
- [ ] Laporan per bulan dari file multi-bulan: asumsi penggulungan saldo awal ditampilkan, stok awal per tanggal awal periode ditanyakan.
- [ ] Hasil cek keseimbangan ditampilkan; jika selisih, penyebab dijelaskan.
- [ ] Asumsi dan disclaimer "bukan laporan audit" tercantum.

## Batasan & penanganan error
- Uji regresi script: `python3 <folder-skill-ini>/scripts/uji_regresi.py` (harus "SEMUA UJI LULUS").
- Script keluar dengan kode ≠ 0 dan pesan `GALAT: ...` berbahasa Indonesia untuk file kosong, tidak ditemukan, Excel/PDF, biner, judul kolom tidak dikenal, atau tidak ada baris valid → sampaikan pesan itu dan langkah perbaikannya.
- Baris dengan tanggal/nominal tak terbaca tidak dihitung dan dilaporkan nomornya; baris "TOTAL"/"saldo akhir" dilewati; baris "saldo awal" dipakai sebagai kas awal. Nominal dalam kurung/minus di kolom Keluar dibaca sebagai uang keluar; di kolom Masuk dijadikan baris bermasalah untuk ditanyakan.
- Dasar akrual didekati dari buku kas + saldo awal/akhir yang diberikan pengguna; akurasi bergantung pada angka stok, piutang, dan utang tersebut.
- Tidak menghitung pajak terutang, tidak menilai kelayakan kredit, tidak menggantikan akuntan. Dasar aturan & tanggal berlaku: `references/regulasi.md`.
- Data pengguna diproses lokal; jangan mengirimnya ke layanan lain.
