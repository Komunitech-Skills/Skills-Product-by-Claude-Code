# Uji 06 — Uji ulang independen v1.0.1 (Tahap 6 butir 7)

> Penguji ke-2, **bukan** pembuat/perevisi/penguji sebelumnya. 2026-09-25. Skill disalin ke scratchpad
> (`uji2-ax/analisis-excel/`) dan dijalankan dari salinan. Linux, Python 3.11, tanpa openpyxl/pandas.
> Platform: `claude-code (simulasi agent)`. Kunci jawaban dihitung dari data sumber generator,
> **tanpa membaca kode script** (kode baru dibaca sesudahnya, hanya untuk mendiagnosis temuan N1).

- Tes bawaan `python3 tests/uji_regresi.py` → **37 tes OK** (sebelumnya 26).
- SKILL.md **170 baris** (< 300).
- Fixture lama: `examples/buat_fixture_uji.py`. Fixture baru: `examples/buat_fixture_uji_ulang.py`
  (deterministik, seed 7250926; kunci di `kunci-ulang.json`, dicek dua kali generate → identik).

## 1. Verifikasi perbaikan P1/P2 dari uji pertama

| # lama | Perbaikan yang diklaim | Hasil uji ulang |
|---|---|---|
| 1 (P1) | `--sheet semua` / `--sheet "Q1,Q2,Q3"` | ✔ Skenario 01: gabung Q1+Q2+Q3 (499 baris), sheet tersembunyi `Master Barang` dilewati + dicatat, TOTAL tiap sheet dibuang (Q1:151, Q2:175, Q3:185), peringatan per sheet berawalan `Sheet 'Q2':`, nomor baris `Q3:79`. Koperasi: TW3 (urutan kolom beda, judul huruf kecil, kolom tambahan) & TW4 (tanpa Keterangan, tanggal teks) digabung + peringatan; penutup `Jumlah`/`Total`/`Subtotal`/`TOTAL TW4` semuanya dibuang. Sheet tersembunyi bisa dipilih eksplisit (`TW1,Arsip 2025`) + ditandai. Sheet kosong / judul saja / beda struktur → dilewati + alasan. Nama sheet berkoma `Jan, Feb` terpilih utuh; `1,5` (nomor) bisa. **Tetapi lihat N2** (sheet ringkasan di depan). |
| 2 (P1) | CSV kutip tak tertutup → GAGAL | ✔ `kutip-rusak.csv` (lama) → GAGAL baris 2; `kutip-tengah.csv` (kutip rusak di baris 7 dari 12) → GAGAL "baris 7 s.d. 12", kode 2; `kutip-di-akhir.csv` → GAGAL baris 4; `kutip-tertutup-jauh.csv` (kutip ditutup 3 baris kemudian) → GAGAL "baris 3 s.d. 5". Sel alamat multi-baris yang **hanya satu barisnya berisi koma** → terbaca + peringatan. **Tetapi lihat N1** (alamat sah berisi koma di ≥ 2 baris ditolak). |
| 3 (P2) | Kolom "Nilai terisi" | ✔ Muncul di pivot/top bila ada sel kosong (Pipa & Sanitasi 50/48; Gol C 13/12; Kelas 4A 22/20) + peringatan nomor baris. |
| 4 (P2) | Penyamaran data pribadi | ✔ NIK `3201•••••••••503`, HP `0812•••••235`, email `a•••@contoh.id`, rekening `1234•••764`; pengelompokan tetap pakai nilai lengkap; `--tampilkan-pribadi` → nilai lengkap + peringatan tegas. `top --grup Nama --nilai "Gaji Pokok"` → peringatan "data SENSITIF … per Nama". (Catatan N5/N6.) |
| 5 (P2) | "4 A"/"4A" digabung | ✔ `4A ← '4 A' / '4A' / '4a'` dst., dilaporkan; juga `Gol A ← 'GolA'/'gol a'/'GOL  A'`, `Jakarta Selatan ← 'JAKARTA SELATAN'/'JakartaSelatan'` (+ spasi ganda). |
| 6 (P2) | Peringatan duplikat di semua perintah | ✔ profil, ringkas, pivot, tren, top, banding (banding menghitung duplikat di dalam subset periode — "2 baris" untuk Jul–Agu). Duplikat lintas sheet diberi nomor `TW2:9 = TW2:8`. |
| 7 (P3) | Label banding dua sheet | ✔ `--sheet TW2 --file-b <sama> --sheet-b TW3` → kolom "TW2" vs "TW3". |
| 10/11 (P3) | Urutan bulan / catatan persen negatif | ✔ Juli–Agustus–September; catatan "% dari total tidak ditampilkan karena ada nilai negatif". |

## 2. File uji BARU + kunci jawaban independen

### A. `Koperasi Maju Bersama 2026.xlsx` (6 sheet, string inline, sheet `Ringkasan` berstruktur beda di urutan PERTAMA)
Perintah: `--sheet "TW1,TW2,TW3,TW4"` (karena `semua` gagal, N2).

| Uji | Kunci (generator) | Script | Cocok |
|---|---|---|---|
| Jumlah per sheet TW1/TW2/TW3/TW4 | 86.720.000 / 80.620.000 / 90.470.000 / 74.825.000 | sama | ✔ |
| Baris per sheet | 43 / 46 (termasuk 1 duplikat) / 41 / 42 | sama | ✔ |
| Gabungan | 332.635.000 | Rp 332.635.000 | ✔ |
| Pivot Akun × Jenis | Penjualan Toko 133.420.000; Jasa Pinjaman 73.125.000; Rapat Anggota 55.765.000; Gaji 36.000.000; Listrik & Air 16.505.000; Provisi 10.570.000; ATK 7.250.000; Beban 115.520.000 / Pendapatan 217.115.000 | sama | ✔ |
| Tren 12 bulan | 25.685.000 … Des 23.965.000 (12 nilai) | 12 nilai sama; % Feb +12,1%, Jun +58,9% dicek manual | ✔ |
| Top-3 beban (`--filter Jenis=Beban`) | Rapat Anggota 55.765.000 (48,3%), Gaji 36.000.000, Listrik 16.505.000 | sama | ✔ |
| Banding pendapatan Q2 vs Q3 | 51.530.000 → 65.395.000 = +26,9% | sama | ✔ |
| `--dari 2026-01 --sampai 2026-09` per Jenis | Pendapatan 171.645.000 / Beban 86.165.000 | sama | ✔ |
| 3 nilai teks "Rp x.xxx.xxx" di TW2, tanggal teks di TW4 | terbaca | terbaca | ✔ |
| Sheet tersembunyi `Arsip 2025` | tidak ikut di `semua` | dicatat, tidak ikut | ✔ |

### B. `pesanan-marketplace-sep.csv` (60 pesanan, 15 alamat 3 baris berisi koma & `""kutip""`, emoji di produk)
- File asli (CSV **sah**; `csv.reader` Python: 61 rekaman × 9 kolom) → **GAGAL: "CSV kemungkinan rusak: baris 5 s.d. 7 …"** → temuan **N1**.
- Varian `-v2` (koma hanya di baris pertama alamat) → terbaca, lalu:

| Uji | Kunci | Script | Cocok |
|---|---|---|---|
| Total | 5.627.000 | Rp 5.627.000 | ✔ |
| Pivot Kota (varian digabung) | Kab. Bogor 2.054.000 (18) · Medan 1.302.000 (13) · Bandung 1.099.000 (12) · Jaksel 877.000 (10) · Surabaya 295.000 (7) | sama | ✔ |
| Top produk (emoji utuh) | Hijab 🌸 2.470.000 · Tumbler ☕ 1.157.000 · Kaos 👕 1.080.000 · Sandal 🩴 575.000 · Masker 😷 345.000 | sama, emoji tampil benar | ✔ |
| Tren per minggu (ISO 36–40) | 325.000 · 1.821.000 · 847.000 · 1.014.000 · 1.620.000 | sama (label "Minggu 31 Agu 2026" dst.) | ✔ |
| Banding 1–15 vs 16–30 Sep | 2.171.000 → 3.456.000 (+59,2%) | sama | ✔ |
| Outlier Rp 325.000 | MP-0020 = rekaman ke-21 | "baris 21" (nomor rekaman/Excel) | ✔ (lihat N3: peringatan multi-baris memakai nomor baris fisik) |

### C. `anggota-koperasi.csv` (`;`, BOM, angka `1.250.000`, NIK/HP/email/rekening, 2 duplikat, 1 kosong)

| Uji | Kunci | Script | Cocok |
|---|---|---|---|
| Deteksi tipe | NIK/HP/Rekening/No = kode; Email teks pribadi | sama; contoh disembunyikan | ✔ |
| Pivot Golongan (dengan duplikat) | Gol B 28.100.000 (19) · Gol C 18.400.000 (13, terisi 12) · Gol A 16.850.000 (10) | sama | ✔ |
| Jumlah/rata-rata Simpanan Wajib | 63.350.000 / 41 = 1.545.121,95 | sama | ✔ |
| Top-3 NIK | …503 4.700.000 (Anggota 04 ×2 duplikat) · …643 2.600.000 · …356 2.400.000 | sama, tersamar | ✔ |
| `--tampilkan-pribadi` | NIK lengkap 3201139996280503 dst. | sama + peringatan | ✔ |
| Duplikat | 2 (baris 42 = baris 5) | sama, di semua subperintah | ✔ |

### D. Data rusak baru
| File / perintah | Harapan | Hasil |
|---|---|---|
| `kutip-tengah.csv` | GAGAL baris 7 | ✔ kode 2 |
| `kutip-tertutup-jauh.csv` | GAGAL | ✔ "baris 3 s.d. 5" |
| `kutip-di-akhir.csv` | GAGAL baris 4 | ✔ (kalimat "baris 4 s.d. 4", N8) |
| `alamat-sah.csv` (`"Jl. Y, No. 2⏎Kel. Z, Kec. W"`) | terbaca + peringatan | ✘ **GAGAL** (N1) |
| `semua-beda.xlsx --sheet semua` | gabung yang sama, sisanya dilewati + alasan | ✔ Satu + "Jan, Feb" = 13; Dua/Kosong/Judul Saja dilewati |
| `--sheet "Satu,TWX"` | GAGAL daftar sheet | ✔ |
| `--sheet "Satu,Jan, Feb"` | ambigu | GAGAL "Sheet 'Jan' tidak ada" (N7; `--sheet "1,5"` berhasil) |
| `--sheet Kosong` / `Judul Saja` | GAGAL awam | ✔ |
| `--sheet semua` pada CSV | diabaikan + info | ✔ "--sheet diabaikan karena file ini CSV" |

**Ketidakcocokan angka: 0** (semua angka yang berhasil dihitung cocok dengan kunci).

## 3. Ulang skenario 01 mengikuti SKILL.md v1.0.1 (multi-sheet)
**Pengguna:** *"Ini file penjualan toko saya Jan–Sep (per kuartal). Total berapa, kategori apa paling laku,
tren per bulan gimana, dan Q3 dibanding Q2 naik atau turun?"*

Langkah agent: `daftar` → melihat Q1/Q2/Q3 + Master Barang tersembunyi → pertanyaan lintas sheet →
`ringkas/pivot/tren/banding … --sheet semua` (sesuai Langkah 1). **Tidak ada penjumlahan manual** (gap P1 lama tertutup).

**Jawaban singkat:** Total penjualan Jan–Sep 2026 **Rp 233.556.000** dari 496 transaksi bernilai. Kategori
terbesar **Semen Rp 105.444.000** (juga qty terbanyak, 1.683). Q3 **turun 28,8%** dibanding Q2
(Rp 97.112.500 → Rp 69.130.500), terutama Semen −Rp 28.300.000 (−54,6%).

| Kategori | Baris | Jumlah Total | Nilai terisi |
|---|---:|---:|---:|
| Semen | 149 | Rp 105.444.000 | 149 |
| Cat | 88 | Rp 36.252.000 | 88 |
| Keramik | 60 | Rp 32.785.000 | 60 |
| Pipa & Sanitasi | 50 | Rp 25.453.000 | 48 |
| Besi | 85 | Rp 25.428.000 | 85 |
| Alat & Perkakas | 67 | Rp 8.194.000 | 66 |
| **TOTAL** | **499** | **Rp 233.556.000** | **496** |

| Periode | Baris | Jumlah Total | Perubahan |
|---|---:|---:|---:|
| Jan 2026 | 48 | Rp 23.917.000 | - |
| Feb 2026 | 44 | Rp 17.888.500 | -25,2% |
| Mar 2026 | 55 | Rp 25.507.500 | 42,6% |
| Apr 2026 | 52 | Rp 34.340.000 | 34,6% |
| Mei 2026 | 58 | Rp 30.672.500 | -10,7% |
| Jun 2026 | 61 | Rp 32.100.000 | 4,7% |
| Jul 2026 | 58 | Rp 17.476.000 | -45,6% |
| Agu 2026 | 63 | Rp 26.433.000 | 51,3% |
| Sep 2026 | 60 | Rp 25.221.500 | -4,6% |

**Temuan:** 1) Tertinggi April (Rp 34.340.000), terendah Juli (Rp 17.476.000). 2) Q3 turun 28,8%; per hari
Rp 1.067.170 → Rp 751.418 (−29,6%). 3) Pipa & Sanitasi (+41,3%) dan Cat (+17,3%) justru naik di Q3.
**Perlu dicek:** 3 sel Total berupa rumus tanpa nilai (Q2:68, Q3:79, Q3:98) tidak dihitung; baris TOTAL tiap
sheet dilewati; sel gabungan H4:H6 di tiap sheet; 6 penulisan kategori digabung (SEMEN/semen…); ada retur
negatif sehingga % dari total tidak ditampilkan; sheet tersembunyi Master Barang tidak ikut.
(Asumsi: sheet Q1+Q2+Q3, kolom Total, tanggal dari kolom Tanggal.)

Verifikasi: total, 6 kategori, 9 bulan, Q2/Q3, banding per kategori (6 baris), qty per kategori (2.941),
top-3 pelanggan Q1+Q3 (Umum 47.830.000 · PT Griya Asri 24.897.500 · Pak Darto 23.823.000, Lainnya 39.893.000)
→ **semua cocok** dengan `kunci-jawaban.json` / hitungan dari data generator. Workbook 1904 → tren identik ✔.

## 4. Temuan baru (berprioritas)
| # | Prio | Temuan | Bukti | Usulan |
|---|---|---|---|---|
| N1 | **P1** | CSV **sah** ditolak: sel teks multi-baris dalam kutip yang **≥ 2 barisnya berisi koma** (alamat Indonesia hampir selalu "Jl. …, No. …⏎Kel. …, Kec. …") → `GAGAL: CSV kemungkinan rusak`, kode 2, tanpa opsi untuk memaksa. Saran "hapus baris barunya" berat untuk awam (15 alamat). | `alamat-sah.csv`; `pesanan-marketplace-sep.csv` (dibaca normal oleh `csv.reader`, 9 kolom konsisten). Heuristik `mirip >= 2` di `baca_csv` hanya menghitung baris-dalam-sel yang memuat pemisah. | Anggap curiga hanya bila baris-dalam-sel **tampak seperti rekaman utuh** (jumlah pemisah ≥ jumlah kolom header − 1), atau bila jumlah kolom rekaman ≠ header. Tambah opsi `--izinkan-multibaris` (turunkan jadi peringatan). Tes regresi dengan alamat 2–3 baris berkoma. |
| N2 | P2 | `--sheet semua` memakai **sheet terlihat pertama** sebagai acuan struktur. Workbook dengan sheet `Ringkasan`/`Rekap`/`Cover` di depan (umum) → semua sheet detail "TIDAK digabung", hasil = 4 baris ringkasan; `pivot --nilai Jumlah` GAGAL "kolom tidak ada". Transparan (peringatan "Hanya 1 sheet…"), tapi SKILL.md tidak menyuruh agent mengulang dengan daftar sheet. | Koperasi: `--sheet semua` → "gabungan sheet Ringkasan; 4 baris". | Pilih acuan = kelompok struktur dengan sheet/baris terbanyak; SKILL.md: "bila ada peringatan 'TIDAK digabung', ulangi dengan `--sheet "TW1,TW2,…"`". |
| N3 | P3 | Peringatan sel multi-baris diulang per sel (15 butir) dan memakai nomor baris fisik (Notepad), sedangkan outlier/sel kosong memakai nomor rekaman (Excel): MP-0020 = "baris 21" vs baris fisik 29. | varian `-v2` | Ringkas jadi satu peringatan ("15 sel multi-baris, mis. baris …") dan satu sistem penomoran (sebut keduanya bila beda). |
| N4 | P3 | Judul "Jumlah Jumlah per Sheet" bila kolom nilai bernama "Jumlah". | Koperasi | Bila nama kolom = nama fungsi, tulis "Total kolom 'Jumlah'". |
| N5 | P3 | Email tersamar `a•••@contoh.id` identik untuk anggota01 & anggota04 → baris top tampak kembar. | anggota | Sertakan 1–2 karakter akhir bagian lokal (`a•••01@contoh.id`). |
| N6 | P3 | "Uang Lembur" per karyawan tidak memicu peringatan SENSITIF (Gaji Pokok memicu); kolom "Simpanan …" tidak dilabel uang (tampil tanpa Rp). | lembur, anggota | Tambah lembur/upah/tunjangan/THR/bonus ke daftar sensitif; simpanan/iuran/setoran ke kata kunci uang. |
| N7 | P3 | `--sheet "Satu,Jan, Feb"` → GAGAL "Sheet 'Jan' tidak ada" tanpa saran. | semua-beda | Pesan: "nama sheet berisi koma — pakai nomor sheet, mis. --sheet \"1,5\"". |
| N8 | P3 | Kalimat "baris 4 s.d. 4". | kutip-di-akhir | Satu baris → "di baris 4". |

Tidak ditemukan: perintah berbahaya, akses jaringan, pembacaan kredensial, prompt injection. File asli tidak diubah.
