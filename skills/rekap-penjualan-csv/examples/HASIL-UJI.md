# Hasil Uji – rekap-penjualan-csv (UJI ULANG v1.1.0)

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Jenis uji:** **uji ulang versi 1.1.0** setelah revisi dari uji pertama (v1.0.0, skor 5/10, REVISI). Hasil uji pertama digantikan oleh dokumen ini. Cacat lama dan statusnya dicatat di bagian "Status cacat uji pertama".
- **Versi yang diuji:** SKILL.md, README.md, ATTRIBUTION.md, `scripts/rekap.py` (v1.1.0 menurut `catalog.csv`)
- **Metode:**
  1. Kelima skenario lama (contoh 01–05) dijalankan ulang dengan script baru. Angka contoh 01–03 diverifikasi ulang dengan script Python terpisah milik penguji (`/tmp/uji-rekap-penjualan-csv/v110/verif-ulang.py`, parser sendiri). Hasilnya **cocok 100%** dan identik dengan v1.0.0.
  2. Ke-14 file data rusak/tepi dari uji pertama dijalankan ulang, ditambah 6 uji tepi baru.
  3. Dua skenario baru: **06** (ekspor gaya Shopee + kolom status) dan **07** (CSV ANSI dari Excel + format rupiah campur + tanggal teks). Keduanya diverifikasi independen (`verif6.py`, `verif7.py`).
  4. Uji A/B S1 tanpa skill (`00-pembanding-tanpa-skill.md`).
  Semua data uji ada di `/tmp/uji-rekap-penjualan-csv/` (lama) dan `/tmp/uji-rekap-penjualan-csv/v110/` (baru).

## Audit keamanan
`rekap.py` v1.1.0 hanya memakai library standar (argparse, csv, io, json, re, sys, collections, datetime). File hanya dibaca, tidak ditulis. Tidak ada akses jaringan, `subprocess`/`eval`/`exec`, maupun pembacaan variabel lingkungan atau kredensial. SKILL.md: "Jangan mengirim isi file pengguna ke layanan eksternal". Tidak ada prompt injection. **Aman.**

## Status cacat uji pertama (v1.0.0)
| Kode lama | Cacat | Status v1.1.0 | Bukti |
|---|---|---|---|
| B1 (berat) | `Rp. 25000` terbaca 0,25 | ✅ **Diperbaiki** | `e-rptitik.csv` → 25.000 / 150.000 / 1.250.000. Contoh 07 cocok 100%. |
| S1 | `Rp 15.000,-` dibuang | ✅ Diperbaiki | `e-strip.csv` → 15.000 / 30.000 / 10.000 |
| S2 | CSV ANSI/cp1252 gagal dibaca | ✅ Diperbaiki (+ peringatan encoding) | `e-cp1252.csv` → "Café Latte" terbaca. Contoh 07 (`½`). |
| S3 | Rata-rata hanya per hari berjualan | ✅ Diperbaiki (kalender + hari berjualan) | `e-bolong.csv` → kalender Rp 20.000, berjualan Rp 100.000 |
| S4 | Status batal/retur ikut terhitung | ⚠️ **Sebagian**: fitur `--kolom-status` ada, tapi daftar kata bawaan tidak lengkap | Contoh 06 → **cacat berat baru B1** |
| S5 | Tidak ada bagian "di luar cakupan" | ✅ Diperbaiki ("Kapan TIDAK digunakan") | Contoh 05 diperbarui |
| S6 | Tanggal teks & format AS | ✅ Diperbaiki (+ deteksi urutan dan peringatan ambigu) | `e-tglteks.csv` terbaca, `e-us.csv` → mdy otomatis, `e-semi2.csv` → peringatan ambigu |
| R1 | Tidak ada langkah bila kolom wajib hilang | ❌ Belum | Contoh 04 |
| R2 | Aturan angka turunan belum jelas | ❌ Belum | Contoh 01, 06, 07 |
| R3 | Nomor baris yang dilewati tidak dilaporkan | ❌ Belum | Contoh 03 |
| R4 | Sel Qty kosong → baris dibuang | ❌ Belum (tidak diputuskan) | `e-kosongsel.csv` |
| R5 | Nilai negatif mengurangi omzet tanpa keterangan | ❌ Belum | uji tepi `n-edge.csv` |
| R6 | `CARA-INSTAL.md`/`LISENSI.txt` tidak ada di folder | ❌ Belum (urusan build) | — |

## Uji data rusak / tepi (v1.1.0)
| Input | Hasil script | Seharusnya | Status |
|---|---|---|---|
| File kosong / hanya header | error "File kosong atau hanya berisi judul kolom" | error jelas | ✅ |
| File tidak ada | error "Gagal membaca file" | error jelas | ✅ |
| Qty 0 & total 0 | dihitung Rp 0 | OK | ✅ |
| `"Rp 1.500.000"`, `"1.500.000,50"`, `15.000,50` (`;`) | benar | benar | ✅ |
| `Rp. 25000`, `Rp.1250000`, `Rp15.000`, `IDR 7500`, `"Rp 1.250.000,00"` | benar | benar | ✅ |
| `"Rp 15.000,-"`, `"30.000,-"` | benar | benar | ✅ |
| cp1252 (`Café`, `½`) | terbaca + peringatan encoding | terbaca | ✅ |
| `1 Sep 2026`, `01 September 2026`, `2026/09/01 10:00`, `14 Sept 2026` | terbaca | terbaca | ✅ |
| `9/5/2026` + `9/23/2026` | mdy otomatis (5 & 23 Sept) | benar | ✅ |
| Semua tanggal ≤ 12 (`01/09`, `02/09`) | dmy + peringatan ambigu | peringatan | ✅ |
| Tanggal campur dmy & mdy dalam satu file | 1 baris dilewati ("tanggal tidak terbaca") | dilaporkan | ✅ |
| Nama produk berisi koma pada file `;`; pemisah tab | benar | benar | ✅ |
| Kolom tidak ada / beda huruf besar-kecil (`tanggal` vs `Tanggal`) | error + daftar kolom tersedia | error jelas (idealnya tidak peka huruf) | ✅ / ⚠️ ringan |
| Baris judul sebelum header ("Laporan Penjualan…") | error "Kolom tidak ditemukan", kolom_tersedia = judul | idealnya opsi lewati baris | ⚠️ ringan |
| **Status `Pengembalian Barang/Dana`** | **dihitung sebagai omzet** | dibuang (retur) | ❌ **BERAT** |
| **Status `Belum Bayar`** | **dihitung sebagai omzet** | dibuang atau dilaporkan | ❌ (bagian B1) |
| `Kopi` dan `kopi ` (beda huruf/spasi) | 2 produk terpisah | digabung | ⚠️ sedang |
| `15000.500` | **15.000.500** | ambigu → lewati/peringatan | ❌ sedang (diam-diam) |
| `15.000.00` (salah ketik `15.000,00`) | **1.500.000** | ambigu → lewati/peringatan | ❌ sedang (diam-diam) |
| `1.5E+06` (notasi ilmiah Excel) | **1.506** | 1.500.000 atau lewati | ❌ sedang (diam-diam) |
| `(15.000)` (gaya akuntansi negatif) | +15.000 | −15.000 atau lewati | ⚠️ ringan |
| `-15.000` / qty `-1` | mengurangi omzet / qty negatif, tanpa laporan | dilaporkan terpisah | ⚠️ ringan (R5 lama) |
| Sel Qty kosong | baris dilewati ("qty tidak valid") | keputusan terdokumentasi | ⚠️ ringan (R4 lama) |
| Hari terendah seri (2 hari sama) | hanya 1 dilaporkan | sebut seri | ⚠️ ringan |

## Verifikasi angka (independen)
| File uji | Total omzet | Baris valid | Top-5 & % | Rata-rata | Terbaik/terendah | Hasil |
|---|---|---|---|---|---|---|
| 01 kasir kopi | Rp 5.084.000 | 127 | cocok | cocok | cocok | ✅ |
| 02 toko online `;` `68.500,00` | Rp 13.899.100 | 88 | cocok | cocok | cocok | ✅ |
| 03 kue kering (3 rusak) | Rp 4.220.000 | 27 (+3) | cocok | cocok | cocok | ✅ |
| 06 gaya Shopee + status | Rp 9.051.000 (script) vs **Rp 9.006.000 (seharusnya)** | 74 vs **73** | Topi 12,9% vs **12,5%** | — | terendah 7/8 vs **24/8** | ❌ (aritmetika cocok, filter status kurang) |
| 07 ANSI + `Rp.`/`,-` + tanggal teks | Rp 2.538.500 | 26 | cocok | cocok | cocok | ✅ |

## Ringkasan skenario
| # | Skenario | Hasil |
|---|---|---|
| 00 | A/B: S1 tanpa skill | Angka sama pada data rapi. Dengan skill lebih baik: insight tajam, nama hari, rata-rata jelas. Keandalan parser terbukti (cara umum salah 100× pada file 02). |
| 01 | Kasir kopi 2 minggu | Baik. Identik dengan v1.0.0, format rata-rata baru. |
| 02 | Toko online `;` + harga satuan | Baik. Identik. |
| 03 | "rekapin dong" + baris rusak | Baik. Identik. Nomor baris masih belum dilaporkan. |
| 04 | File tanpa kolom harga | Agent bertanya dengan benar, tapi SKILL.md masih belum mengatur langkah ini. |
| 05 | Laba rugi + pajak | Baik. Kini diatur di SKILL.md dan diarahkan ke skill terkait. |
| 06 | **Baru:** ekspor gaya Shopee + status | **Cacat berat:** "Pengembalian Barang/Dana" dihitung sebagai omzet tanpa peringatan. |
| 07 | **Baru:** Excel ANSI + format rupiah campur | Sangat baik. Semua cacat utama v1.0.0 terbukti diperbaiki. |

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 8 | Jelas: CSV penjualan, kasir/Shopee/Tokopedia, rekap/omzet, bilingual. |
| Kemudahan awam | 8 | Satu kalimat cukup. ANSI dari Excel kini terbaca. Tetap butuh Python dan CSV (bukan .xlsx). |
| Kualitas output | 8 | Format rapi, rata-rata kalender vs hari berjualan, peringatan disampaikan, insight berbasis angka. |
| Akurasi (angka/fakta) | 5 | Format rupiah Indonesia kini akurat (cacat v1.0.0 beres). Tapi retur berstatus "Pengembalian" dan "Belum Bayar" tetap dihitung **tanpa peringatan**, dan beberapa format angka ambigu dihitung diam-diam. |
| Penanganan input kurang | 6 | Error kolom hilang/file kosong jelas. SKILL.md belum mengatur langkah bila kolom wajib tidak ada (R1 lama). |
| Penanganan di luar cakupan | 8 | Bagian "Kapan TIDAK digunakan" lengkap (laba rugi, pajak, prediksi, .xlsx). |
| Keamanan | 9 | Lokal, library standar, jujur soal data. |

## SKOR AKHIR: 6 / 10 → **REVISI**

Revisi v1.1.0 berhasil memperbaiki cacat berat dan hampir semua cacat sedang dari uji pertama. `Rp. 25000`, `15.000,-`, CSV ANSI, tanggal teks/AS, rata-rata kalender, dan bagian "di luar cakupan" kini benar, dan terverifikasi independen (contoh 07). Namun fitur baru yang paling penting untuk pengguna marketplace, yaitu **filter status**, punya celah yang membuat **omzet salah tanpa peringatan**: istilah Indonesia "Pengembalian"/"Dikembalikan" dan "Belum Bayar" tidak disaring, dan script tidak menunjukkan status apa saja yang ikut dihitung. Sesuai brief, angka salah tanpa peringatan adalah cacat berat, sehingga skor dibatasi ≤ 6. Perbaikannya kecil dan terarah (lihat B1). Setelah B1 dan S1–S2 diperbaiki, skill ini diperkirakan layak **LULUS (≥ 8)**.

## Daftar cacat & saran perbaikan

### Berat
- **B1 – Retur berstatus "Pengembalian…" dan pesanan "Belum Bayar" ikut dihitung sebagai omzet tanpa peringatan** (`scripts/rekap.py`: `STATUS_BATAL_DEFAULT` dan loop `if a.kolom_status:`; SKILL.md langkah 2 butir "Jika ada kolom status…").
  Bukti: contoh 06, omzet Rp 9.051.000 padahal seharusnya Rp 9.006.000. Hari terendah salah (7/8 vs 24/8), dan % Topi Baseball salah. Pada uji `n-status.csv`, "Belum Bayar" (Rp 258.000) ikut dihitung.
  *Saran perbaikan:*
  1. Tambahkan ke default: `"pengembalian", "dikembalikan", "belum bayar", "menunggu pembayaran", "tidak dibayar", "expired", "kedaluwarsa"`. Pertimbangkan pencocokan per kata (bukan substring) agar tidak salah buang.
  2. Tambahkan ke JSON: `"status_dihitung": {"Selesai": 60, "Sedang Dikirim": 13, ...}` (status unik yang **ikut** dihitung beserta jumlah baris).
  3. SKILL.md langkah 3: "Selalu tampilkan ke pengguna daftar status yang dihitung dan yang dibuang. Jika ada status yang maknanya ragu (mis. 'Pengembalian', 'Dikomplain', 'Belum Bayar'), tanyakan atau jalankan ulang dengan `--abaikan-status`."
  4. Tambahkan kasus uji: `Pengembalian Barang/Dana`, `Dikembalikan`, `Belum Bayar`, `Pesanan Selesai`, `Dibatalkan Sistem`.

### Sedang
- **S1 – Format angka ambigu tetap dihitung diam-diam** (`parse_angka`). `15.000.00` → 1.500.000 (seharusnya 15.000), `15000.500` → 15.000.500, `1.5E+06` → 1.506. *Saran:* (a) tolak notasi ilmiah (`e`/`E` diikuti angka) dengan alasan "format angka ilmiah, ubah format sel di Excel ke Number". (b) Jika memakai titik sebagai pemisah ribuan, wajibkan setiap grup setelah grup pertama tepat 3 digit **dan** grup pertama 1–3 digit. `15000.500` dan `15.000.00` tidak lolos, sehingga dimasukkan ke `baris_dilewati` dengan alasan "format angka ambigu". (c) Tambahkan kasus-kasus ini ke tes.
- **S2 – Nama produk tidak dinormalisasi** (loop utama, `produk = (...).strip()`). "Kopi" dan "kopi " terhitung sebagai 2 produk, sehingga peringkat dan % produk terlaris bisa salah pada catatan ketik manual (contoh 03, 07 adalah jenis file ini). *Saran:* kelompokkan dengan kunci `" ".join(nama.split()).casefold()`, tampilkan ejaan yang paling sering, dan laporkan `produk_digabung` bila ada penggabungan.

### Ringan
- **R1 – Langkah bila kolom wajib hilang belum diatur** (SKILL.md *Alur kerja* langkah 1; masih terbuka dari v1.0.0). *Saran:* "Jika tidak ada kolom total maupun harga, jangan menebak. Tanyakan sekali harga per produk atau minta file lain." Pertimbangkan opsi `--harga-produk "A=15000,B=12000"`.
- **R2 – Aturan "semua angka harus berasal dari output script"** bertentangan dengan angka turunan yang wajar (masih terbuka). *Saran:* "Angka turunan (jumlah, selisih, persentase dari JSON) boleh, asal dihitung dari output script."
- **R3 – Nomor baris yang dilewati tidak dilaporkan** (masih terbuka). *Saran:* `contoh_baris_dilewati: [{"baris": 5, "alasan": "...", "nilai": "..."}]`, maksimal 10.
- **R4 – Sel Qty kosong membuat baris dibuang**, padahal SKILL.md menyebut qty "default 1" (masih terbuka). *Saran:* putuskan (kosong = 1, atau dilewati) dan tulis di SKILL.md.
- **R5 – Nilai negatif / gaya akuntansi `(15.000)` tidak dilaporkan terpisah** (masih terbuka). *Saran:* `jumlah_baris_negatif` + total, dan `(x)` diperlakukan sebagai −x.
- **R6 – Hari terbaik/terendah seri tidak disebut.** *Saran:* kembalikan daftar tanggal bila nilainya sama.
- **R7 – Baris judul sebelum header dan nama kolom peka huruf besar-kecil.** *Saran:* opsi `--lewati-baris N` atau deteksi otomatis baris header, dan pencocokan nama kolom tanpa peka huruf.
- **R8 – Omzet ekspor marketplace adalah omzet bruto** (sebelum ongkir/voucher/biaya platform). Tidak ada instruksi untuk menyebutkannya. *Saran:* tambahkan ke *Aturan & batasan*: "Untuk ekspor marketplace, sebutkan bahwa omzet belum dikurangi voucher, ongkir, dan biaya platform."
- **R9 – Pengarahan ke `laporan-keuangan-emkm`/`pph-final-umkm` tanpa fallback** bila skill itu tidak terpasang. *Saran:* "Jika skill tersebut tidak ada, jelaskan singkat dan sarankan konsultan/kanal resmi."
- **R10 – README merujuk `CARA-INSTAL.md`** dan ATTRIBUTION merujuk `LISENSI.txt`, dan keduanya tidak ada di folder skill. Pastikan keduanya ikut dalam paket rilis.

## Catatan untuk contoh
- Contoh 01–05 dipertahankan dan diberi catatan "Uji ulang v1.1.0" (angka identik, format rata-rata disesuaikan, dan status cacat lama diperbarui).
- Contoh 06 **sengaja memperlihatkan cacat B1** dan diberi banner peringatan. Jalankan ulang setelah perbaikan sebelum dipakai sebagai materi pembeli.
- Contoh 07 adalah contoh positif baru yang siap dipakai.
