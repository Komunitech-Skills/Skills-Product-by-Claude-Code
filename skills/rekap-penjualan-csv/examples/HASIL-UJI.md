# Hasil Uji – rekap-penjualan-csv

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** SKILL.md, README.md, ATTRIBUTION.md, `scripts/rekap.py` di folder ini
- **Metode:** 5 skenario dijalankan dengan berperan sebagai agent yang memuat SKILL.md, dan script dijalankan sungguhan di `/tmp/uji-rekap-penjualan-csv/`. Hasil 3 file normal diverifikasi ulang dengan script Python terpisah yang ditulis penguji (parser sendiri, tidak memakai `parse_angka`). Ditambah 14 uji data rusak/tepi.

## Audit keamanan
`rekap.py` hanya memakai library standar (argparse, csv, json, re, datetime). Tidak ada akses jaringan, tidak ada penulisan/penghapusan file, tidak ada pembacaan kredensial atau variabel lingkungan, dan tidak ada `eval`/`exec`/`subprocess`. SKILL.md dan README tidak memuat prompt injection. FAQ README jujur menyebut bahwa isi data tetap dibaca oleh AI agent. **Aman.**

## Verifikasi angka (independen)
| File uji | Total omzet | Baris valid | Top-5 & % | Hari terbaik/terendah | Hasil |
|---|---|---|---|---|---|
| 01 kasir kopi (`,`, `Rp 18.000`) | Rp 5.084.000 | 127 | cocok | cocok | ✅ |
| 02 toko online (`;`, `68.500,00`, harga×qty) | Rp 13.899.100 | 88 | cocok | cocok | ✅ |
| 03 kue kering (3 baris rusak) | Rp 4.220.000 | 27 (+3 dilewati) | cocok | cocok | ✅ |

## Uji data rusak / tepi
| Input | Hasil script | Seharusnya | Status |
|---|---|---|---|
| File kosong (0 byte) | error "File kosong" | error jelas | ✅ |
| Hanya header | error "File kosong" | error jelas | ✅ |
| Qty 0 & total 0 | dihitung Rp 0, tidak error | OK | ✅ |
| `"Rp 1.500.000"` | 1.500.000 | 1.500.000 | ✅ |
| `"1.500.000,50"` | 1.500.000,50 | 1.500.000,50 | ✅ |
| `;` + `15.000,50` | 15.000,50 | 15.000,50 | ✅ |
| Nama produk berisi koma pada file `;` | terbaca benar | – | ✅ |
| Kolom Qty tidak ada di file | error "Kolom tidak ditemukan" + daftar kolom | error jelas | ✅ |
| **`Rp. 25000`, `Rp. 150000`, `Rp.1250000`** | **0,25 / 0,15 / 0,125 (total Rp 0,53!)** | 25.000 / 150.000 / 1.250.000 | ❌ **SALAH DIAM-DIAM** |
| `"Rp 15.000,-"`, `"30.000,-"` | baris dilewati ("harga/total tidak valid") | 15.000 / 30.000 | ❌ (dilaporkan, tapi omzet kurang) |
| Encoding Windows-1252/ANSI (mis. `Café`) | error "Gagal membaca file: 'utf-8' codec…" | terbaca | ❌ |
| Tanggal `1 Sep 2026`, `01 September 2026`, `2026/09/01 10:00` | dilewati semua | terbaca | ⚠️ (dilaporkan) |
| Tanggal format AS `9/5/2026` | dibaca 9 Mei (tanpa peringatan); `9/23/2026` dilewati | peringatan format ambigu | ⚠️ |
| Periode 10 hari, hanya 2 hari ada penjualan | "rata-rata per hari" Rp 100.000 (÷2 hari) | ÷10 hari kalender = Rp 20.000, atau label diperjelas | ⚠️ menyesatkan |
| Sel Qty kosong | baris dilewati ("qty tidak valid") | bisa default 1 atau dilewati | ⚠️ perlu keputusan |

## Ringkasan skenario
| # | Skenario | Hasil |
|---|---|---|
| 01 | Ekspor kasir kopi 2 minggu | Baik. Angka cocok, insight konkret. |
| 02 | Toko online `;` + harga satuan | Baik. Angka cocok. Filter status batal belum ada. |
| 03 | "rekapin dong" + 3 baris rusak | Baik. Baris dilewati dilaporkan dengan benar. |
| 04 | File tanpa kolom harga | Agent bertanya sekali, tapi alurnya tidak diatur di SKILL.md. |
| 05 | Minta laba rugi + pajak | Diarahkan dengan benar, tapi SKILL.md tidak punya aturan di luar cakupan. |

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 8 | Jelas: CSV penjualan, rekap, omzet, bilingual. |
| Kemudahan awam | 7 | Satu kalimat sudah cukup. Tapi butuh Python, dan CSV ANSI dari Excel Windows gagal dibaca. |
| Kualitas output | 8 | Format rapi, insight berbasis angka, baris rusak dilaporkan. |
| Akurasi (angka/fakta) | 4 | Happy path 100% akurat, tetapi `Rp. 25000` menghasilkan angka salah **tanpa peringatan**, dan `Rp 15.000,-` dibuang. |
| Penanganan input kurang | 6 | Error kolom hilang dan file kosong jelas. SKILL.md tidak mengatur langkah bila kolom wajib tidak ada. |
| Penanganan di luar cakupan | 4 | Tidak ada instruksi (laba, pajak, prediksi, .xlsx langsung). |
| Keamanan | 9 | Lokal, library standar, jujur soal data. |

## SKOR AKHIR: 5 / 10 → **REVISI**

Alur dan format bagus, dan tiga dataset normal terverifikasi akurat. Tapi ada **cacat berat**: format rupiah yang sangat umum di Indonesia, `Rp. 25000` (titik setelah "Rp" tanpa pemisah ribuan), terbaca sebagai 0,25 tanpa peringatan apa pun. Omzet bisa dilaporkan salah hingga jutaan kali lipat lebih kecil. Ini bertentangan langsung dengan janji README "Angka dihitung dengan script, bukan dikira-kira". Sesuai brief, cacat berat membatasi skor ≤ 6.

## Daftar cacat & saran perbaikan

### Berat
- **B1 – `Rp. 25000` terbaca 0,25 tanpa peringatan** (`scripts/rekap.py`, `parse_angka`, baris 39). Regex `[^\d,.\-]` membuang "Rp" tapi menyisakan titik di depan, sehingga `.25000` menjadi float 0.25.
  *Saran:* buang simbol mata uang **sebelum** regex, lalu rapikan tanda baca di tepi:
  ```python
  s = re.sub(r"(?i)(rp|idr)\.?", "", str(teks))
  s = re.sub(r"[.,]-\s*$", "", s)          # '15.000,-' -> '15.000'
  s = re.sub(r"[^\d,.\-]", "", s).strip(".,")
  ```
  Tambahkan juga pengaman: bila nilai hasil parse < 1 padahal teks aslinya berisi ≥ 4 digit, masukkan ke `baris_dilewati` dengan alasan "format angka ambigu" (jangan diam-diam dihitung). Tambahkan kasus `Rp. 25000`, `Rp.1.250.000`, `15.000,-` ke tes.

### Sedang
- **S1 – Format `Rp 15.000,-` dibuang** (baris 39–56, `parse_angka`). Format ini umum di nota Indonesia. Barisnya dilaporkan, tapi omzet jadi kurang. *Saran:* sudah tercakup oleh perbaikan B1 (buang akhiran `,-`).
- **S2 – CSV ber-encoding Windows (ANSI/cp1252) gagal dibaca** (`baca_csv`, baris 65). "CSV (Comma delimited)" dari Excel Windows sering tidak UTF-8. *Saran:* coba `utf-8-sig`, bila `UnicodeDecodeError` ulangi dengan `cp1252`, lalu `latin-1`, dan laporkan encoding yang dipakai di JSON.
- **S3 – "Rata-rata omzet per hari" hanya dibagi hari yang ada penjualan** (baris `rata_rata_omzet_per_hari`, dan label di *Format output* SKILL.md). Untuk usaha yang tidak berjualan setiap hari, angka ini terlihat lebih besar dari kenyataan. *Saran:* tambahkan `jumlah_hari_kalender` dan `rata_rata_per_hari_kalender` di JSON, lalu ubah label SKILL.md menjadi "Rata-rata omzet per hari berjualan (N hari dari M hari)".
- **S4 – Pesanan batal/retur ikut terhitung** padahal SKILL.md/README menyebut ekspor Shopee/Tokopedia. *Saran:* tambahkan opsi `--kolom-status "Status Pesanan" --abaikan-status "Batal,Dibatalkan,Pengembalian"`. Di SKILL.md langkah 1, instruksikan agent untuk memeriksa kolom status dan memakainya bila ada.
- **S5 – Tidak ada bagian "di luar cakupan"** (SKILL.md, *Aturan & batasan*). *Saran:* tambahkan: "Di luar cakupan: laporan laba rugi (butuh HPP/biaya), perhitungan pajak, prediksi penjualan, membaca .xlsx langsung. Jelaskan singkat, jangan hitung tarif pajak, tawarkan rekap omzet sebagai dasar."
- **S6 – Tanggal format teks & AS** (`FORMAT_TANGGAL`, baris 14–19). `1 Sep 2026`, `01 September 2026`, dan `2026/09/01 10:00` tidak didukung. `9/5/2026` bisa terbaca terbalik tanpa peringatan. *Saran:* tambahkan format `%Y/%m/%d %H:%M` dan nama bulan Indonesia/Inggris (Jan/Januari…Des/Desember). Deteksi urutan hari/bulan per kolom (bila ada nilai "bulan" > 12, tukar urutannya), lalu laporkan asumsi formatnya di JSON.

### Ringan
- **R1 – SKILL.md tidak mengatur langkah bila kolom wajib (tanggal/produk/total-atau-harga) tidak ada** (*Alur kerja* langkah 1). *Saran:* "Jika kolom wajib tidak ada, jangan menebak. Tanyakan sekali (mis. daftar harga per produk), atau minta file lain." Pertimbangkan opsi `--harga-produk "A=15000,B=12000"`.
- **R2 – Aturan "semua angka harus berasal dari output script"** (*Aturan & batasan*) bertentangan dengan insight yang wajar (persentase gabungan, perbandingan minggu). *Saran:* "Angka turunan (jumlah/selisih/persentase dari output script) boleh, asal dihitung dari JSON dan tidak menebak."
- **R3 – Script tidak menyebut baris mana yang dilewati.** *Saran:* tambahkan `contoh_baris_dilewati` (nomor baris + nilai mentah, maks. 10) agar pengguna bisa memperbaiki file.
- **R4 – Sel Qty kosong membuat baris dibuang**, padahal SKILL.md menyebut qty "default 1". *Saran:* putuskan dan dokumentasikan. Misalnya sel qty kosong = 1, atau tetap dilewati dengan alasan eksplisit.
- **R5 – Nilai negatif (retur) ikut mengurangi omzet tanpa keterangan.** *Saran:* laporkan `jumlah_baris_negatif` dan totalnya secara terpisah.
- **R6 – README merujuk `CARA-INSTAL.md` dan `LISENSI.txt`** yang tidak ada di folder skill. Pastikan keduanya ikut dalam paket rilis.
