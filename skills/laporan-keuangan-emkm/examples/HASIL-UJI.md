# Hasil Uji Ulang — laporan-keuangan-emkm v1.1.0 (kandidat VIP)

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** `scripts/laporan_emkm.py` **v1.1.0** (`VERSI = "1.1.0"`), SKILL.md, README.md, ATTRIBUTION.md, `references/` (hitung-manual, pemetaan-kategori, regulasi), `templates/`, `scripts/uji_regresi.py`
- **Uji sebelumnya:** v1.0.0, skor 6 (REVISI), 1 cacat berat (B1) + 5 cacat sedang (S1–S5).
- **Metode:** semua cacat lama diuji ulang dengan data uji lama (`/tmp/uji-laporan-keuangan-emkm/`) dan data baru. Data baru: buku kas konveksi 6 bulan (63 transaksi) dan warung makan. Setiap bulan dari 6 laporan bulanan dibandingkan dengan ledger akrual bulanan buatan penguji (`verif_6bln.py`, klasifikasi manual, tanpa kode skill). S1 diverifikasi ulang dengan `verif_s1_v110.py`. Skenario 04 (input kurang) dan 05 (di luar cakupan) tidak memakai script dan tidak terdampak perubahan, jadi tetap berlaku. Uji A/B (00-pembanding) dan banding pesaing (00-banding) dipertahankan dan diberi catatan pembaruan v1.1.0.

## Audit keamanan
- Script hanya memakai library standar (`argparse, csv, io, json, os, re, sys, unicodedata, collections, datetime, decimal`). Tidak ada socket/HTTP/urllib/subprocess/eval/exec. Tidak ada tulis/hapus file (output ke stdout). Tidak membaca env/kredensial. `open()` hanya untuk file input & file pemetaan.
- `uji_regresi.py` memakai `subprocess` hanya untuk menjalankan script skill sendiri pada file sementara. Aman.
- SKILL.md/README/references tidak mengandung prompt injection. **Aman.**

## Status cacat lama
| Cacat v1.0.0 | Uji ulang v1.1.0 | Status |
|---|---|---|
| **B1** laporan satu periode tidak menggulir kas | Data lama, laporan Februari: kas awal Rp 7.680.000, **kas akhir Rp 22.408.250 ✔**. Data baru 6 bulan: kas & setara kas, utang KUR, dan kasbon cocok dengan penguji **di setiap bulan**, dan neraca seimbang tiap periode (06) | **Tuntas untuk kas/utang bank/kasbon/aset.** Muncul cacat berat baru pada piutang/utang pemasok (lihat BB1) |
| **S1** angsuran KUR tidak dipisah | Angsuran otomatis ditanyakan. `--bunga 52=208.334` → beban keuangan Rp 223.334, utang Rp 22.916.667, laba −Rp 2.026.917 ✔ (01). Data 6 bulan: 4 angsuran dipecah benar | Tuntas |
| **S2** kulakan gas, air mineral, iuran pasar, PB1 | Kulakan gas & air mineral → pembelian dagangan; gas masak/PDAM → utilitas; iuran kebersihan pasar → beban lain; PB1 → pajak daerah + ditanyakan (02, 07) | Tuntas (tetapi pertanyaan PB1 tidak bisa ditutup, lihat BS3) |
| **S3** angka mustahil tetap "LENGKAP ✔" | Utang bank −Rp 1.700.000 → SEMENTARA, ⚠, pertanyaan wajib (03). HPP negatif → SEMENTARA (uji regresi) | Tuntas |
| **S4** tidak ada cara mencatat selisih kas | `--catat-selisih-kas` → beban selisih kas Rp 150.000, laba Rp 6.100.000, neraca seimbang ✔ (02) | Tuntas |
| **S5** `(200.000)` di Keluar dibalik jadi masuk | `(200.000)` dan `-150.000` di Keluar → uang keluar; `(50.000)` di Masuk → ditanyakan. Kas Rp 8.685.000 ✔ (07) | Tuntas |
| Ringan lama (kasbon, botol/jerigen/pouch, TOTAL di kolom tanggal, kalimat rugi, tren 1 bulan, label "LENGKAP (dengan asumsi)") | Semua terbukti diperbaiki | Tuntas |

## Verifikasi angka (independen)
| Uji | Hasil |
|---|---|
| S1 katering 70 trx (final, dengan bunga KUR) | pendapatan 36.150.000; HPP 11.900.000; penyusutan 952.083; laba −2.026.917; kas 14.691.833; A = L+E = 37.939.750. **Cocok** |
| B1 data lama, Februari | kas akhir 22.408.250. **Cocok** |
| 6 bulan, laporan Jan–Jun sekaligus | laba −1.996.000; kas 9.574.000; utang KUR 13.170.000; aset tetap 16.100.000; modal 14.504.000. **Cocok persis** |
| 6 bulan, 6 laporan bulanan | Kas, utang KUR, kasbon, stok, keseimbangan: **cocok tiap bulan**. Laba: Jan cocok. Feb/Mar/Mei selisih 2.778–13.611 (penyusutan). **Apr selisih 1.210.000, Jun selisih 781.527** (piutang/utang dihitung dua kali). Modal akhir bulan ≠ modal awal bulan berikutnya di 4 dari 5 sambungan |
| Warung sembako (tabel tempel) + selisih kas | laba 6.100.000, aset = L+E = 10.650.000. **Cocok** |
| Warung makan (PB1, gas, air, kurung) | laba 5.985.000; kas 8.685.000. **Cocok** |
| Sambal online (Jumlah+Jenis) | laba 13.335.000; kas 14.435.000. **Cocok** (sama dengan v1.0.0) |
| Data rusak/tepi: `Rp 1.500.000`, `1.500.000,50`→1.500.001, `1,5jt`, `150rb`, `15.000,-`, `0`, `abc`, `1.250.000.50`, masuk+keluar terisi, `TOTAL` di kolom tanggal, file kosong, header saja, tanpa kolom nominal/keterangan, `.xlsx`, Debit/Kredit, file tidak ada | Semua benar/ditolak dengan `GALAT:` berbahasa Indonesia |
| `scripts/uji_regresi.py` | **SEMUA UJI LULUS** (35 cek) |

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 9 | Tidak berubah. Kata kunci awam + Inggris, batas dengan skill lain jelas. |
| Kemudahan awam | 8 | Satu pesan pertanyaan kini juga memuat bunga angsuran & PB1. Masih ada status SEMENTARA yang tidak bisa ditutup (kas minus karena jualan dicatat mingguan, PB1), sehingga agent harus menjelaskan sendiri. |
| Kualitas output | 8 | Struktur SAK EMKM lengkap, kalimat rugi sudah wajar, label "LENGKAP (dengan asumsi)" jujur. Belum ada pemisahan lancar/tidak lancar dan jadwal penyusutan per aset. |
| Akurasi (angka/fakta) | 6 | Semua laporan satu periode & laporan Jan–Jun cocok persis. Laporan bulanan dari file multi-bulan salah diam-diam bila bulan sebelumnya ada penjualan/pembelian tempo (BB1), dan penyusutan bulanan tidak konsisten. |
| Penanganan input kurang | 9 | Tanya sekali, maksimal 5 butir, jalur "langsung aja" dengan asumsi tertulis (04). |
| Penanganan di luar cakupan | 9 | Audit/SAK EP/konsolidasi/SPT diarahkan dengan benar (05). |
| Keamanan | 10 | Lokal, tanpa jaringan, tanpa tulis file. |

## SKOR AKHIR: 6 / 10 → **REVISI**

Kemajuan v1.1.0 besar dan nyata. Keenam cacat lama (B1 dan S1–S5) serta semua cacat ringan terbukti tuntas. Hasil laporan satu periode kini akurat sampai rupiah di semua data uji, dan skill **makin unggul** atas agent tanpa skill maupun pesaing. Namun uji 6 bulan yang diminta (verifikasi tiap bulan) menemukan **cacat berat baru** di fitur yang sama dengan B1. Laporan per bulan menghitung pendapatan atau HPP **dua kali** ketika piutang/utang pemasok dari bulan sebelumnya dilunasi di bulan laporan. Laporan tetap berlabel **LENGKAP ✔ seimbang**, dan tidak ada cara CLI yang benar untuk menghindarinya. Kasus "pelanggan bayar bulan ini untuk pesanan bulan lalu" sangat umum dan termasuk pemakaian utama ("laporan bulan ini" dari buku kas setahun). Sesuai quality gate, skor dibatasi ≤ 6. Perbaikannya sempit (lihat BB1). Setelah BB1 dan BS1–BS3 diperbaiki, skill ini realistis mencapai 8–9.

## Daftar cacat & saran perbaikan (v1.1.0)

### Berat
- **BB1 — Piutang & utang pemasok tidak bergulir dengan benar pada laporan satu bulan dari file multi-bulan** (`laporan_emkm.py` baris 859–860: `piutang_awal = max(0, piutang_awal - js("terima_piutang"))`, `utang_usaha_awal = max(0, ... - js("bayar_utang_usaha"))`). Penjualan/pembelian tempo sebelum periode tidak diketahui script. Bukti (06): piutang jaket Maret Rp 1,2 jt dilunasi April → laba April −Rp 485.167 (seharusnya −Rp 1.695.167). Bon kain Mei Rp 800 rb dibayar Juni → laba Juni −Rp 2.548.194 (seharusnya −Rp 1.766.667). Keduanya "LENGKAP ✔". Jalan keluar CLI juga buntu. `--piutang-awal` dianggap per awal file, sedangkan `--saldo-awal-per awal-periode` berhenti menggulirkan aset tetap, utang bank, dan kasbon, dan kasbon tidak punya opsi saldo awal (pada uji "rantai", kasbon Rp 500.000 hilang dari neraca April yang tetap ✔).
  *Saran:* (1) mode `awal-file` + ada transaksi sebelum periode → tambahkan ke `pertanyaan` "Berapa piutang pelanggan & utang pemasok per <awal periode>?" (status SEMENTARA sampai dijawab), kecuali tidak ada piutang/utang sama sekali di data; (2) tambah opsi yang berlaku per awal periode, mis. `--piutang-awal-periode`, `--utang-usaha-awal-periode` (atau ubah `--saldo-awal-per awal-periode` agar hanya pos yang diisi pengguna yang tidak digulir, sedangkan kas/utang bank/aset/kasbon tetap digulir); (3) tambah `--piutang-lain-awal`; (4) SKILL.md langkah 2: ganti "Stok awal periode tidak bisa digulirkan, jadi tanyakan stok" menjadi "stok, piutang, dan utang pemasok per tanggal awal periode wajib ditanyakan"; (5) tambah uji regresi "penjualan tempo bulan lalu dilunasi bulan ini" dan "modal akhir bulan N = modal awal bulan N+1".

### Sedang
- **BS1 — Penyusutan periode dihitung dari nilai buku, bukan biaya perolehan** (baris 989 `dep = Decimal(aset_tetap_awal) / bulan_umur * n_bulan`, dengan `aset_tetap_awal` yang sudah dikurangi `dep_sebelum`). Laporan bulanan: Feb 213.889 / Mar 210.278 / Jun 273.194 vs benar 216.667 / 216.667 / 291.667. Laba bulanan tidak menjumlah ke laba semester (−1.544.751 vs −1.996.000, termasuk efek BB1), dan modal tidak bersambung antarbulan. *Saran:* simpan daftar aset (biaya, bulan mulai) dari saldo awal file + pembelian, lalu hitung penyusutan periode dari biaya perolehan seperti `dep_sebelum` (baris 864–870). Untuk mode `awal-periode`, minta biaya perolehan & akumulasi, bukan hanya nilai buku.
- **BS2 — "Kas sempat minus" tidak bisa dikonfirmasi** (baris 1117). Warung yang mencatat jualan mingguan (02: kulakan tanggal 1, jualan dicatat tanggal 3) terkunci di SEMENTARA + ⚠ walau semua angka sudah benar dan pemilik sudah menjelaskan. *Saran:* opsi `--abaikan-kas-minus` (atau `--konfirmasi kas-minus`) setelah pemilik mengonfirmasi. Status lalu "LENGKAP (dengan asumsi)" dan asumsinya ditulis. Alternatif: jadikan kas minus pertanyaan hanya bila minus di akhir hari/akhir minggu.
- **BS3 — Pertanyaan PB1/PBJT tidak bisa ditutup dan tidak ada perlakuan "titipan"** (baris 1138 memeriksa teks keterangan tanpa melihat `bunga_dikonfirmasi`/`--tetapkan`). `--tetapkan 8=beban_pajak_lain` tetap SEMENTARA. Rumah makan yang menyetor PB1 tiap bulan tidak pernah mendapat laporan final. *Saran:* lewati pertanyaan bila `t["sumber"] == "ditetapkan pengguna"`. Tambahkan kategori dua arah `titipan_pajak` (masuk = PB1 dipungut dari pembeli, keluar = penyetoran) yang hanya memengaruhi pos "Utang pajak daerah" di neraca, dan jelaskan di `references/pemetaan-kategori.md`.

### Ringan
- Peringatan "Stok awal periode dianggap Rp X karena stok per <tgl> tidak diketahui" tetap muncul walau pengguna memberi `--persediaan-awal` per awal periode (baris 885–887). Tampilkan hanya bila `a.persediaan_awal is None`.
- Asumsi menulis "awal data (3 Januari 2026)" / "(2 Januari 2026)" padahal baris saldo awal bertanggal 1 Januari. Pakai tanggal baris saldo awal bila ada.
- Neraca laporan bulanan: "Kas menurut buku / Dana dipindah ke rekening lain" hanya memakai transfer bulan berjalan (Maret: −Rp 2.000.000), sehingga tidak menunjukkan uang laci atau saldo bank sebenarnya. Total tetap benar. Hitung `dana_di_rekening_lain` kumulatif sejak awal file.
- "Pelunasan pesanan X" (masuk) selalu menjadi penjualan tunai. Bila pengguna memberi piutang awal, pelunasan piutang lama bisa tercatat ganda lalu "dikoreksi" sebagai beban piutang tak tertagih. Ada peringatan, tetapi sebaiknya pelunasan ditanyakan bila `piutang_awal > 0`.
- Belum diadopsi dari pesaing: aset/liabilitas lancar vs tidak lancar dan jadwal penyusutan per aset di CaLK.

## Contoh yang diperbarui / ditambah
- `01-katering-3-bulan-kur-prive.md`: output ulang v1.1.0 (bunga KUR ditanyakan & dipecah, kasbon jadi piutang).
- `02-warung-tempel-tabel-selisih-kas.md`: output ulang v1.1.0 (kulakan gas, iuran pasar, `--catat-selisih-kas`; bukti BS2).
- `03-bikinin-dong-sambal-online-kur.md`: langkah & status diperbarui (utang negatif → SEMENTARA ⚠; botol dikenali).
- **Baru** `06-laporan-per-bulan-6-bulan-b1.md`: uji B1 data lama + 6 bulan, tabel verifikasi per bulan (bukti BB1, BS1).
- **Baru** `07-warung-makan-pb1-gas-air-kurung.md`: uji S2/S5 dan bukti BS3.
- `04`, `05`: tetap (tidak memakai script, tidak terdampak).
- `00-pembanding-tanpa-skill.md`, `00-banding-pesaing.md`: dipertahankan, ditambah catatan pembaruan v1.1.0. **A/B: skill jelas lebih baik. Pesaing: skill kita menang.**
