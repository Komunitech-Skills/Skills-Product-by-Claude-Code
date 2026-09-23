# Hasil Uji — laporan-keuangan-emkm (kandidat VIP)

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** SKILL.md, README.md, ATTRIBUTION.md, `references/` (hitung-manual, pemetaan-kategori, regulasi), `templates/` (buku-kas-template.csv, pemetaan-kustom.contoh.json), `scripts/laporan_emkm.py` v1.0.0
- **Metode:** 5 skenario (01–05) + uji A/B (00-pembanding) + uji banding pesaing (00-banding). Script dijalankan sungguhan di `/tmp/uji-laporan-keuangan-emkm/`. Buku kas uji dibuat realistis: katering 3 bulan dengan 70 transaksi, prive, KUR (pencairan + angsuran), pembelian kompor & freezer, PPh final, piutang/utang, dan 3 transaksi ambigu. Semua angka diverifikasi ulang dengan python terpisah (`verif_s1.py`, klasifikasi manual per baris tanpa memakai kode skill).

## Audit keamanan
- `laporan_emkm.py` hanya memakai library standar (`argparse, csv, io, json, os, re, sys, unicodedata, collections, datetime, decimal`). **Tidak ada** socket/HTTP/urllib/subprocess/eval/exec, tidak menghapus/menulis file (output hanya ke stdout), tidak membaca variabel lingkungan atau kredensial. Hanya membaca file input dan file pemetaan yang disebut pengguna.
- SKILL.md/README/references: tidak ada prompt injection. Ada instruksi "Data pengguna diproses lokal; jangan mengirimnya ke layanan lain".
- **Aman.**

## Verifikasi angka (independen)
| Uji | Hasil |
|---|---|
| S1 katering 70 trx: pendapatan, HPP, penyusutan, laba, kas, neraca | Semua cocok dengan hitungan penguji (laba −Rp 2.118.583; aset = L+E = Rp 37.639.750) ✔ |
| S2 warung (tabel tempel): laba, selisih kas | Laba Rp 6.250.000 ✔; selisih −Rp 150.000 dilaporkan, tidak dipaksa ✔ (pos HPP/beban salah klasifikasi, lihat S2) |
| S3 format Jumlah+Jenis | Laba Rp 13.335.000, kas Rp 14.435.000 ✔ |
| Penyusutan (aset baru mulai bulan berikutnya) | 12 jt/48×3 + 1,45 jt/48×2 + 6,8 jt/48×1 = Rp 952.083 ✔ |
| Format nominal: `Rp 1.500.000`, `1.500.000,50` (→ 1.500.001, pembulatan 0,5 ke atas), `1,5jt`, `150rb`, `15.000,-`, `0` (dilewati), `abc` & `1.250.000.50` (dilaporkan rusak), masuk+keluar terisi (dilaporkan) | ✔ |
| Tanggal `5 Januari 2026`, `2026-01-13`, `06-01-2026`, `02/13/2026` (diperingatkan format Amerika) | ✔ |
| File kosong, header saja, tanpa kolom nominal, tanpa kolom keterangan, `.xlsx`, file tidak ada, kolom Debit/Kredit | Semua keluar dengan `GALAT: …` berbahasa Indonesia yang jelas ✔ |
| Modal awal tidak cocok; stok akhir terlalu besar (HPP negatif) | Dilaporkan TIDAK SEIMBANG + penyebab; HPP negatif diperingatkan ✔ |
| **Laporan satu bulan dari buku kas multi-bulan (`--periode-awal 2026-02-01 --periode-akhir 2026-02-28`)** | **SALAH**: kas awal tetap Rp 8.500.000 (baris saldo awal 1 Jan), padahal seharusnya Rp 7.680.000 (setelah transaksi Januari). Kas akhir tertulis Rp 23.228.250, seharusnya Rp 22.408.250 (selisih Rp 820.000), dan neraca tetap berlabel "✔ seimbang" (lihat B1) |
| Nilai dalam kurung di kolom Keluar `(200.000)` | Dibalik menjadi **uang masuk** Rp 200.000 (lihat S5) |

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 9 | Kata kunci awam ("untung berapa", KUR, neraca) + Inggris, batas dengan rekap-penjualan/pph/hpp jelas. |
| Kemudahan awam | 8 | Cukup kirim file/tempel tabel; pertanyaan maks 5; ringkasan awam bagus. Istilah `--tetapkan` tersembunyi dari pengguna. |
| Kualitas output | 8 | Struktur SAK EMKM lengkap (LR, LPK, CaLK 10 butir), tren, asumsi, "Perlu dicek", disclaimer. Ringkasan untuk kondisi rugi terbaca janggal. |
| Akurasi (angka/fakta) | 5 | Aritmetika & neraca benar di semua uji normal (terverifikasi), tetapi filter periode menghasilkan kas/modal salah secara diam-diam; bunga di angsuran KUR hilang; beberapa klasifikasi kata kunci keliru. |
| Penanganan input kurang | 9 | Tanya sekali, 5 poin, template ditawarkan, ada jalur "langsung aja" dengan asumsi tertulis. |
| Penanganan di luar cakupan | 9 | Audit/SAK EP/konsolidasi/SPT ditolak dan diarahkan ke KAP/konsultan; tetap memberi bantuan yang aman. |
| Keamanan | 10 | Lokal, tanpa jaringan, tanpa tulis file. |

## SKOR AKHIR: 6 / 10 → **REVISI**

Skill ini **jelas lebih baik** daripada agent tanpa skill (A/B lulus) dan **menang** melawan satu-satunya pesaing Indonesia yang ditemukan. Alur tanya-bukan-tebak dan skrip deterministiknya sudah setara produk VIP. Namun ada **satu cacat berat**: fitur periode yang diiklankan di SKILL.md menghasilkan neraca dengan kas dan modal salah, tetapi tetap berlabel "seimbang". Kasusnya sangat umum ("laporan bulan ini" dari buku kas setahun). Sesuai aturan quality gate, skor dibatasi ≤ 6. Setelah B1 dan beberapa cacat sedang diperbaiki, skill ini realistis mencapai 8–9.

## Daftar cacat & saran perbaikan

### Berat
- **B1 — `--periode-awal` tidak menggulirkan saldo kas awal** (`laporan_emkm.py` baris 730 `trx = [t for t in trx_semua if p_awal <= ...]` dan baris 770–777 penentuan `kas_awal`). Transaksi sebelum periode dibuang, tetapi kas awal tetap diambil dari baris "saldo awal" di awal file. Neraca menjadi salah sebesar arus kas bersih sebelum periode, dan cek keseimbangan tetap ✔ karena modal awal dihitung dari kas awal yang sama-sama salah. Bukti: laporan Februari dari buku kas Jan–Mar, kas akhir Rp 23.228.250 (seharusnya Rp 22.408.250).
  *Saran:* bila `--kas-awal` tidak diisi dan ada transaksi dengan tanggal < `p_awal`, hitung `kas_awal = saldo_awal_baris (atau 0) + Σ(masuk − keluar)` transaksi sebelum `p_awal` (koreksi `transfer_internal` sama seperti baris 931–932), dan tambahkan asumsi "Kas awal periode = saldo awal file + arus kas sebelum <tanggal>". Tambahkan juga peringatan bahwa piutang/stok/utang/aset awal harus per tanggal `p_awal`, bukan per awal file. Di SKILL.md langkah 2, beri catatan untuk laporan per bulan dari file multi-bulan.

### Sedang
- **S1 — Angsuran KUR/pinjaman tidak dipisah pokok & bunga.** "Angsuran KUR BRI ke-1 Rp 2.291.667" seluruhnya mengurangi utang (kategori `bayar_pinjaman`). Beban bunga ±Rp 208.334 hilang, sehingga laba terlalu tinggi dan utang terlalu rendah. *Saran:* SKILL.md › "Kasus yang sengaja ditanyakan" (dan `references/pemetaan-kategori.md` bagian yang sama): wajib tanyakan rincian pokok/bunga setiap ada `bayar_pinjaman` tanpa baris bunga pada bulan yang sama. Di script: tambahkan peringatan otomatis + opsi `--bunga BARIS=NOMINAL` yang memecah satu baris menjadi pokok + beban keuangan.
- **S2 — Urutan aturan kata kunci menimbulkan salah klasifikasi umum** (`ATURAN_BAWAAN`, baris 71–161): "Kulakan gas melon" → utilitas (seharusnya pembelian barang dagangan); "Beli air mineral gelas" → utilitas; "Iuran kebersihan pasar" → pembelian bahan (kata `pasar`); "Bayar pajak restoran PB1" → **PPh** (seharusnya pajak daerah, dan bila dipungut dari pembeli bukan beban). *Saran:* tambahkan aturan prioritas tinggi untuk kata kerja pembelian (`kulakan`, `kulak`, `restock`, `stok`, `untuk dijual`) sebelum `beban_utilitas`; pindahkan kata spesifik `beban_lain` (`iuran`, `keamanan`, `kebersihan`, `sampah`) sebelum `pembelian_bahan`; tambahkan `pajak restoran`, `pb1`, `pbjt`, `pajak hotel` ke `beban_pajak_lain` dan masukkan "PB1/PBJT" ke daftar yang ditanyakan (seperti PPN).
- **S3 — Status "LENGKAP" dan "✔ seimbang" walau ada kondisi mustahil** (baris 1033). Utang bank negatif (−Rp 1.700.000 di S3), HPP negatif, atau piutang/utang negatif hanya masuk "Peringatan". Laporan ini bisa terkirim ke bank. *Saran:* status SEMENTARA bila `utang_bank_akhir < 0`, `hpp < 0`, `persediaan/piutang/utang < 0`, atau `kas_min < 0`, dan tampilkan kondisi itu di daftar pertanyaan "Perlu dicek".
- **S4 — Tidak ada cara resmi mencatat selisih kas.** Dengan `--kas-akhir-aktual`, selisih kecil (S2: Rp 150.000) membuat neraca selamanya TIDAK SEIMBANG. SKILL.md langkah 4 hanya melarang "memaksa" angka. *Saran:* opsi `--catat-selisih-kas` (setelah pengguna mengonfirmasi) yang membukukan selisih sebagai "Selisih kas (kurang/lebih)" di beban/pendapatan lain-lain. Tambahkan juga satu kalimat di SKILL.md langkah 4 agar agent menawarkannya.
- **S5 — Nominal dalam kurung/negatif di kolom Keluar dibalik menjadi uang masuk** (baris 638–641). `(200.000)` di kolom Keluar untuk "Beli tepung" dibaca sebagai pemasukan Rp 200.000, sehingga kas meleset Rp 400.000. Di buku kas, tanda kurung sering berarti "keluar". *Saran:* di mode Masuk/Keluar, nilai negatif/kurung pada kolom Keluar diperlakukan sebagai keluar (abs), atau dimasukkan ke `bermasalah` agar ditanyakan, bukan dibalik diam-diam.

### Ringan
- Tidak ada kategori piutang lain-lain/kasbon karyawan/uang muka. Kasbon yang akan dipotong gaji terpaksa dibebankan. Tambahkan `piutang_lain` (keluar → aset; masuk → pelunasan).
- Kata kunci kurang: `botol`, `jerigen`, `pouch` (kemasan); `belanja dapur rumah`, `arisan` (sebaiknya ditanyakan, dan sudah ditanyakan).
- Baris total dengan teks "TOTAL" di kolom tanggal dilaporkan sebagai "tanggal tidak terbaca" alih-alih dilewati (baris 614–616 hanya memeriksa kolom keterangan).
- Ringkasan awam saat rugi: "yang tersisa jadi laba sekitar -5,9% … labanya sekitar -Rp 5.861". Ganti dengan kalimat "setiap Rp 100.000 penjualan, usaha rugi sekitar Rp 5.861" (`ringkasan_awam`, baris 1103–1108).
- "Tren per periode" tetap tampil untuk 1 bulan (SKILL.md: "jika > 1 bulan"), baris 1227.
- Label "LENGKAP" saat stok akhir/penyusutan memakai default bisa menyesatkan untuk bank. Pertimbangkan "LENGKAP (dengan asumsi)".
- README menyebut `CARA-INSTAL.md` yang tidak ada di folder skill. Pastikan ikut dalam paket.
- Pembanding pesaing: pertimbangkan pemisahan aset/liabilitas lancar vs tidak lancar dan jadwal penyusutan per aset di CaLK (lihat `00-banding-pesaing.md`).

## Ringkasan uji tambahan
- **A/B (00-pembanding-tanpa-skill.md):** skill **jelas lebih baik**. Transaksi ambigu ditanyakan, bukan ditebak (tanpa skill, zakat pribadi masuk beban). Penyusutan tepat per tanggal beli. Ada CaLK, disclaimer, dan hasil yang bisa diulang. Tanpa skill hanya unggul di perlakuan kasbon.
- **Pesaing (00-banding-pesaing.md):** `adamriofc/laporan-keuangan-psak` (MIT) hanya kerangka ±25 baris tanpa script, aturan prive, atau disclaimer. Skill kita **menang** di semua kriteria.
