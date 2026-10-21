# Hasil Uji – rekap-penjualan-csv (UJI ULANG v1.2.0)

> **Catatan versi 1.2.6 (2026-10-17, ditulis pembuat skill, bukan hasil penguji independen):** contoh `01`–`08` di
> folder ini adalah keluaran versi lama (format chat sebelum 1.2.6: judul `##`, tabel, dua jenis rata-rata). Versi
> 1.2.6 mengganti balasan chat dengan `rekap_chat` (teks biasa, satu rata-rata, terlaris menurut omzet dan jumlah)
> dan saran yang wajib bersandar pada `fakta_produk`, setelah uji bot Telegram 17 Okt 2026 (tanpa skill 8,0 →
> dengan skill 6,5, BELUM). Perubahan itu baru diperiksa lewat 27 tes regresi `scripts/uji_regresi.py` (data fiktif
> yang angka agregatnya sama dengan uji 17 Okt, plus kasus file tanpa kolom jumlah). Uji ulang skenario di
> OpenClaw/bot Telegram (dengan pra-cek `uji-tg.sh`) belum dijalankan; hasil di bawah tetap untuk versi 1.2.0.

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** v1.2.0 (menurut `catalog.csv`): SKILL.md, README.md, ATTRIBUTION.md, `scripts/rekap.py`
- **Jenis uji:** uji ulang kedua. Riwayat: v1.0.0 → 5/10 REVISI; v1.1.0 → 6/10 REVISI (cacat berat B1: status "Pengembalian Barang/Dana" dan "Belum Bayar" dihitung sebagai omzet). Dokumen ini menggantikan hasil v1.1.0.
- **Metode:**
  1. Data uji lama di `/tmp/uji-rekap-penjualan-csv/` dan `…/v110/` dijalankan ulang dengan v1.2.0: contoh 01, 02, 03, 06, 07, 14 file tepi lama, dan 6 file tepi v1.1.0.
  2. Data uji baru di `…/v120/`: `t-status.csv` (14 variasi status), `t-angka.csv` (angka ambigu), `t-nama.csv` (nama beda ketik), `catatan-warkop.csv` (contoh 08).
  3. Semua angka contoh 06 dan 08 diverifikasi dengan python terpisah milik penguji (parser & filter sendiri).
  4. Uji A/B (`00-pembanding-tanpa-skill.md`) tetap berlaku dan diberi catatan v1.2.0. **Banding pesaing baru** (`00-banding-pesaing.md`) karena sebelumnya belum ada.

## Audit keamanan
`rekap.py` v1.2.0 hanya memakai library standar (argparse, csv, io, json, re, sys, collections, datetime). File hanya dibaca, tidak ditulis. Tidak ada akses jaringan, `subprocess`/`eval`/`exec`, maupun pembacaan variabel lingkungan atau kredensial. SKILL.md: "Jangan mengirim isi file pengguna ke layanan eksternal". Tidak ada prompt injection. **Aman.**

## Status cacat uji sebelumnya (v1.1.0)
| Kode | Cacat | Status v1.2.0 | Bukti |
|---|---|---|---|
| **B1 (berat)** | "Pengembalian Barang/Dana" & "Belum Bayar" dihitung omzet | ✅ **Diperbaiki** | `s6-shopee-agustus.csv` → **Rp 9.006.000**, 73 baris (sebelumnya Rp 9.051.000 / 74). `t-status.csv`: Pengembalian, Dikembalikan, Belum Bayar/belum bayar, Menunggu Pembayaran, Dibatalkan Sistem, Unpaid → dibuang |
| B1 saran 2 | Tidak ada daftar status yang ikut dihitung | ✅ Diperbaiki | JSON `status_dihitung` (mis. `{"Selesai": 60, "Sedang Dikirim": 13}`). SKILL.md mewajibkan agent menampilkannya |
| S1 | Angka ambigu dihitung diam-diam | ✅ Diperbaiki | `15.000.00`, `15000.500`, `1.5E+06`, `1.5e6`, `15.00.000`, `1,50,000` → dilewati ("harga/total tidak valid atau meragukan"). SKILL.md menyuruh agent menyebut jumlahnya dan menyarankan perbaikan |
| S2 | "Kopi" vs "kopi " jadi 2 produk | ✅ Diperbaiki | `t-nama.csv`: Kopi/kopi /KOPI → 1 produk (4 cup, Rp 60.000). Dilaporkan di `nama_produk_digabung`. Spasi ganda (`Kopi  Susu`) juga dinormalisasi |
| R1 | Langkah bila kolom total & harga tidak ada | ❌ Belum | Contoh 04 |
| R2 | Aturan angka turunan | ❌ Belum | Contoh 01, 06, 08 |
| R3 | Nomor baris dilewati tidak dilaporkan | ❌ Belum | Contoh 03, 08 |
| R4 | Sel Qty kosong → baris dibuang (SKILL.md: "default 1") | ❌ Belum | `e-kosongsel.csv` → "Tidak ada baris valid" |
| R5 | Negatif / `(15.000)` tidak dilaporkan | ❌ Belum | `n-edge.csv`: `(15.000)` → **+15.000** |
| R6 | Hari terbaik/terendah seri tidak disebut | ❌ Belum | Contoh 08 (Es Teh = Indomie seri di produk; hari tidak seri) |
| R7 | Baris judul sebelum header, nama kolom peka huruf | ❌ Belum | `n-preamble.csv` → "Kolom tidak ditemukan" (error jelas) |
| R8 | Omzet marketplace = bruto, tidak diatur | ❌ Belum | Contoh 06 (disebut atas inisiatif agent) |
| R9 | Fallback bila skill tujuan tidak terpasang | ❌ Belum | Contoh 05 |
| R10 | `CARA-INSTAL.md` / `LISENSI.txt` tidak ada di folder | ❌ Belum (urusan build) | README baris 26, ATTRIBUTION baris 6 |

## Uji data rusak / tepi (v1.2.0)
| Input | Hasil script | Seharusnya | Status |
|---|---|---|---|
| File kosong / hanya header / file tidak ada | error jelas | error jelas | ✅ |
| `Rp. 25000`, `Rp.1250000`, `Rp15.000`, `IDR 7500`, `"Rp 1.250.000,00"`, `"Rp 15.000,-"` | benar | benar | ✅ (regresi) |
| `"1.500.000,50"`, `"15,000.50"`, `"12,500"`, `"2,5"` | 1.500.000,5 / 15.000,5 / 12.500 / 2,5 | benar | ✅ |
| cp1252 (`Café`, `½`), pemisah `;`/tab, koma di nama produk | benar | benar | ✅ (regresi) |
| Tanggal teks, format AS otomatis, peringatan urutan ambigu | benar | benar | ✅ (regresi) |
| **`15.000.00` / `15000.500` / `1.5E+06` / `1.5e6`** | **dilewati + dihitung di `alasan_dilewati`** | dilewati | ✅ |
| `15.00.000` / `1,50,000` (grup tidak baku) | dilewati | dilewati | ✅ |
| **Status `Pengembalian Barang/Dana`, `Dikembalikan`, `Belum Bayar`, `belum bayar`, `Menunggu Pembayaran`, `Unpaid`, `Dibatalkan Sistem`** | dibuang, tercatat di `dibuang_karena_status` | dibuang | ✅ |
| Status `Selesai`, `Pesanan Selesai`, `Pesanan Diterima`, `Sedang Dikirim`, `Dikomplain`, kosong | dihitung, tercatat di `status_dihitung` (kosong → `(kosong)`) | dihitung + ditampilkan | ✅ |
| Status `Pengembalian Ditolak` (retur ditolak = penjualan tetap sah) | **dibuang** (cocok substring "pengembalian") | idealnya dihitung | ⚠️ ringan (terlihat di `dibuang_karena_status`, agent wajib menampilkannya) |
| `--abaikan-status "batal"` | **mengganti** seluruh daftar bawaan (retur/belum bayar tidak lagi dibuang) | perlu disebut | ⚠️ ringan |
| `Kopi` / `kopi ` / `KOPI` | 1 produk + `nama_produk_digabung` | digabung + dilaporkan | ✅ |
| `Es Teh` / `Es  Teh` (hanya beda spasi) | digabung, tidak dilaporkan | wajar (tampilan sama) | ✅ |
| `(15.000)` | +15.000 | −15.000 atau dilewati | ⚠️ ringan (R5) |
| `-15.000`, qty `-1` | mengurangi omzet tanpa laporan | dilaporkan | ⚠️ ringan (R5) |
| Sel Qty kosong | dilewati | keputusan terdokumentasi | ⚠️ ringan (R4) |

## Verifikasi angka (independen)
| File uji | Total omzet | Baris valid | Top-5 & % | Rata-rata | Terbaik/terendah | Hasil |
|---|---|---|---|---|---|---|
| 01 kasir kopi | Rp 5.084.000 | 127 | cocok | cocok | cocok | ✅ identik v1.1.0 |
| 02 toko online `;` `68.500,00` | Rp 13.899.100 | 88 | cocok | cocok | cocok | ✅ identik |
| 03 kue kering (3 rusak) | Rp 4.220.000 | 27 (+3) | cocok | cocok | cocok | ✅ identik |
| **06 Shopee + status** | **Rp 9.006.000** | **73** | Topi 25 pcs, 12,5% | 290.516,13 / 333.555,56 | 6/8 Rp 1.054.000 / 24/8 Rp 55.000 | ✅ **cocok 100%** |
| 07 ANSI + `Rp.`/`,-` | Rp 2.538.500 | 26 | cocok | cocok | cocok | ✅ identik |
| **08 warkop (baru)** | Rp 202.000 | 13 (+3 ambigu) | cocok | 67.333,33 | 21/9 Rp 77.000 / 23/9 Rp 55.000 | ✅ cocok 100% |
| `n-status.csv` (v1.1.0) | Rp 320.000 (110.000 + 165.000 + 45.000) | 3 | — | — | — | ✅ (pada v1.1.0, Pengembalian Rp 129.000 dan Belum Bayar Rp 258.000 ikut terhitung) |

## Ringkasan skenario
| # | Skenario | Hasil |
|---|---|---|
| 00 | A/B tanpa skill | Tetap berlaku. Skill jelas lebih baik (parser rupiah, status, insight). |
| 00 | **Banding pesaing (baru)** | `coffeefuelbump/csv-data-summarizer-claude-skill` (MIT). S1: angka sama, tapi laporan generik dan kolom "Tanggal" tidak dikenali. Pada data Indonesia nyata pesaing salah 100× (`35.000,00`), tidak menyaring status, dan gagal membaca CSV ANSI. **Skill kita menang (9 vs 5).** |
| 01 | Kasir kopi 2 minggu | Baik. Identik. |
| 02 | Toko online `;` + harga satuan | Baik. Identik. |
| 03 | "rekapin dong" + baris rusak | Baik. Nomor baris masih belum dilaporkan. |
| 04 | File tanpa kolom harga | Agent bertanya dengan benar. SKILL.md belum mengatur langkahnya (R1). |
| 05 | Laba rugi + pajak | Diarahkan ke skill terkait dengan benar. |
| 06 | Shopee + status | **Diperbaiki & dijalankan ulang:** Rp 9.006.000, status dihitung/dibuang ditampilkan. Banner peringatan dihapus. |
| 07 | Excel ANSI + format rupiah campur | Baik. Identik. |
| 08 | **Baru:** warkop, angka meragukan + nama beda ketik | Angka ambigu dilewati dan dijelaskan, nama digabung dan dilaporkan. |

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 8 | Jelas: CSV penjualan, kasir/Shopee/Tokopedia, rekap/omzet, bilingual. |
| Kemudahan awam | 8 | Satu kalimat cukup. File ANSI Excel terbaca. Tetap butuh Python dan CSV (bukan .xlsx). |
| Kualitas output | 9 | Format rapi, status dihitung/dibuang transparan, angka meragukan dijelaskan dengan cara memperbaiki, insight berbasis angka. |
| Akurasi (angka/fakta) | 9 | Semua file uji cocok verifikasi independen. Filter status lengkap untuk istilah Indonesia. Tidak ada lagi tebakan diam-diam untuk format ambigu. Sisa: `(15.000)` dibaca positif, dan "Pengembalian Ditolak" ikut dibuang (terlihat). |
| Penanganan input kurang | 6 | Error kolom hilang/file kosong jelas. SKILL.md belum mengatur langkah bila kolom total & harga tidak ada (R1). Qty kosong vs "default 1" belum konsisten (R4). |
| Penanganan di luar cakupan | 8 | "Kapan TIDAK digunakan" lengkap. Belum ada fallback bila skill tujuan tidak terpasang. |
| Keamanan | 9 | Lokal, library standar, jujur soal data. |

## SKOR AKHIR: **8 / 10** → **LULUS**

Cacat berat B1 dan kedua cacat sedang dari v1.1.0 sudah diperbaiki dan terbukti dengan data uji yang sama. Ekspor Shopee kini menghasilkan tepat Rp 9.006.000. Status yang dihitung dan dibuang terlihat oleh pengguna, sehingga salah golongan bisa dikoreksi. Angka berformat meragukan dilewati dan dilaporkan, bukan ditebak. Nama produk beda ketik digabung dan dilaporkan. Tidak ada regresi pada 5 contoh lama dan 20 file tepi. Uji A/B dan banding pesaing sama-sama dimenangkan skill ini dengan jelas. Skor belum 9 karena beberapa celah ringan yang sudah lama (terutama R1, R3, R4) belum ditutup, dan ada dua celah ringan baru pada filter status.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
- Tidak ada.

### Ringan
- **R11 (baru) – Pencocokan status berbasis substring membuang status "ditolak".** `Pengembalian Ditolak`, `Pembatalan Ditolak`, dan `Retur Ditolak` adalah penjualan sah tapi dibuang (loop `if any(k in st.lower() for k in abaikan)`). Dampaknya kecil karena status ini tampil di `dibuang_karena_status`. *Saran:* sebelum mencocokkan daftar buang, cek daftar pengecualian (`"ditolak"`, `"dibatalkan permintaan"`) dan masukkan ke `status_dihitung` dengan peringatan "status ragu, periksa".
- **R12 (baru) – `--abaikan-status` mengganti seluruh daftar bawaan, dan teks help-nya kedaluwarsa.** Help di `main()` masih menulis default lama (tanpa pengembalian/belum bayar). SKILL.md menyarankan "jalankan ulang dengan `--abaikan-status` berisi daftar sendiri" tanpa menyebut bahwa daftar bawaan hilang. *Saran:* perbarui help (atau bangkitkan dari `STATUS_BATAL_DEFAULT`), tambahkan opsi `--tambah-abaikan-status` / `--hitung-status` yang menambah/mengecualikan tanpa menghapus bawaan, dan beri satu kalimat di SKILL.md.
- **R1 – Langkah bila kolom total & harga tidak ada** belum diatur (SKILL.md *Alur kerja* langkah 1). *Saran:* "Jika tidak ada kolom total maupun harga, jangan menebak; tanyakan sekali harga per produk atau minta file lain." Opsi `--harga-produk "A=15000,B=12000"`.
- **R2 – "Semua angka harus berasal dari output script"** bertentangan dengan angka turunan yang wajar (%, jumlah dua produk). *Saran:* "Angka turunan boleh asal dihitung dari JSON script."
- **R3 – Baris yang dilewati tidak disebut nomor/isinya.** Pada contoh 08 agent harus membuka file sendiri untuk menjelaskan baris mana yang harus diperbaiki. *Saran:* `contoh_baris_dilewati: [{"baris": 9, "alasan": "...", "nilai": "15.000.00"}]`, maksimal 10.
- **R4 – Qty kosong → baris dibuang**, padahal tabel SKILL.md menyebut qty "default 1". *Saran:* putuskan satu aturan dan tuliskan di SKILL.md.
- **R5 – `(15.000)` terbaca +15.000; nilai negatif tidak dilaporkan.** *Saran:* `(x)` → −x, plus `jumlah_baris_negatif` dan totalnya di JSON.
- **R6 – Nilai seri (hari/produk) tidak ditandai.** *Saran:* kembalikan daftar tanggal bila nilainya sama.
- **R7 – Baris judul sebelum header dan nama kolom peka huruf.** *Saran:* `--lewati-baris N` atau deteksi header otomatis; pencocokan nama kolom tanpa peka huruf.
- **R8 – Omzet marketplace adalah bruto.** *Saran:* satu aturan di *Aturan & batasan*: sebutkan bahwa omzet belum dikurangi voucher, ongkir, dan biaya platform.
- **R9 – Pengarahan ke `laporan-keuangan-emkm`/`pph-final-umkm` tanpa fallback.** *Saran:* "Jika skill tersebut tidak ada, jelaskan singkat dan sarankan konsultan/kanal resmi."
- **R10 – `CARA-INSTAL.md` (README baris 26) dan `LISENSI.txt` (ATTRIBUTION baris 6)** tidak ada di folder skill. Pastikan ikut paket rilis.
- **Ide dari pesaing (bukan cacat):** grafik tren harian/omzet per produk opsional (lihat `00-banding-pesaing.md`).

## Catatan untuk contoh
- Contoh 01–05 dan 07 dipertahankan dan diberi catatan "Uji ulang v1.2.0" (angka identik).
- Contoh 06 **dijalankan ulang**: banner peringatan dihapus, angka diperbarui ke Rp 9.006.000, dan status dihitung/dibuang ditampilkan. Siap dipakai sebagai materi pembeli.
- Contoh 08 (baru) memperlihatkan angka meragukan yang dilewati dan nama produk yang digabung.
