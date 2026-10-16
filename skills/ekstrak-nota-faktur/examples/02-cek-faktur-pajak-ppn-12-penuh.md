# 02 — Cek 2 faktur pajak supplier: PPN 12% penuh + faktur lama 2024

## Skenario
S2 — permintaan normal. Admin keuangan CV kopi meminta dua faktur pajak dari supplier kemasan dicek. Faktur September 2026 memungut PPN 12% × DPP penuh untuk barang biasa, padahal seharusnya 12% × 11/12 (efektif 11%). Faktur lama Desember 2024 memakai format e-Faktur 16 digit dan tarif 11%. Semua identitas fiktif.

## Input pengguna
> Mbak/Mas, tolong cek 2 faktur pajak dari PT Kemas Jaya ini. PPN-nya udah bener belum? Yang satu faktur bulan ini, satunya faktur lama Desember 2024 yang baru ketemu di laci. [2 PDF terlampir]

Isi dokumen (transkripsi):
```
[F1] FAKTUR PAJAK — Kode dan Nomor Seri: 04.00.26.00007654321     15 September 2026
 Pengusaha Kena Pajak: PT Kemas Jaya Fiktif, NPWP 0011112222333444, NITKU 0011112222333444000000
 Pembeli: CV Kopi Nusantara Fiktif, NPWP 0099998888777666
 1 Kardus box 20x20x10   3.000 pcs x 2.750    8.250.000
 2 Lakban cokelat 2 inch   200 roll x 12.500  2.500.000
 Harga Jual 10.750.000 · DPP 10.750.000 · DPP Nilai Lain 9.854.167
 PPN = 1.290.000 · Jumlah 12.040.000 · Terbilang: Dua belas juta empat puluh ribu rupiah

[F2] FAKTUR PAJAK — Kode dan Nomor Seri: 010.000-24.12345678     18/12/2024
 PKP: PT Kemas Jaya Fiktif, NPWP 01.111.222.2-333.444 · Pembeli: CV Kopi Nusantara Fiktif, NPWP 09.999.888.8-777.666
 Standing pouch 250 g  5.000 pcs x 1.000 = 5.000.000 · DPP 5.000.000 · PPN 550.000 · Jumlah 5.550.000
```

## Output
> **Disegarkan ke v1.0.5 (2026-10-16):** dijalankan ulang dengan `scripts/cek_nota.py --hari-ini 2026-09-23` dari data hasil baca yang sama. Yang berubah dibanding uji 2026-09-23: (1) **F2 kini berstatus COCOK** — NPWP 15 digit pada dokumen bertanggal sebelum 2025 hanya diberi info "wajar", bukan peringatan; (2) **PPN Seharusnya Rp 1.182.500 dan Total Seharusnya Rp 11.932.500 untuk F1 kini dihitung script** (kolom CSV tersendiri), bukan dihitung agent; (3) kolom CSV hitungan memakai judul "… Hitung Ulang"/"… Seharusnya". Angka PPN, selisih, dan rekap tidak berubah. Tampilan di bawah untuk Claude Code/Cursor; versi kanal chat ada di bagian berikutnya.


**Hasil baca & cek 2 dokumen**

| # | Tanggal | Penjual | Jenis | Total | Status |
|---|---|---|---|---|---|
| F1 | 15-09-2026 | PT Kemas Jaya Fiktif | Faktur pajak | Rp 12.040.000 | ⚠️ Perlu dicek |
| F2 | 18-12-2024 | PT Kemas Jaya Fiktif | Faktur pajak | Rp 5.550.000 | ✅ Cocok |

**Yang perlu Anda cek**
- **F1: PPN ditulis Rp 1.290.000, yaitu 12% × DPP penuh Rp 10.750.000.** Tarif 12% penuh hanya untuk barang mewah. Untuk kardus dan lakban (barang biasa), aturan sejak 2025 adalah 12% × DPP nilai lain (11/12 × DPP), jadi **PPN seharusnya Rp 1.182.500** (efektif 11%).
  - Kelebihan PPN: **Rp 107.500**. Total seharusnya (hitung ulang): **Rp 11.932.500** (di faktur tertulis Rp 12.040.000).
  - Faktur ini sudah mencantumkan DPP nilai lain Rp 9.854.167, tetapi PPN-nya tidak dihitung dari angka itu (12% × Rp 9.854.167 ≈ Rp 1.182.500).
  - Saran: **tanyakan ke PT Kemas Jaya sebelum membayar.** Contoh kalimat: *"Mohon dicek faktur 04.00.26.00007654321. PPN tertulis Rp 1.290.000, sedangkan 12% × DPP nilai lain Rp 9.854.167 = Rp 1.182.500. Apakah bisa diterbitkan faktur pengganti?"* Ini bisa saja salah ketik atau salah hitung, bukan berarti fakturnya palsu.
- **F2 (Desember 2024): PPN Rp 550.000 = 11% × Rp 5.000.000, benar** untuk faktur bertanggal sebelum 2025. Nomor seri 16 digit memang format e-Faktur sebelum Coretax. NPWP penjual dan pembeli 15 digit (format lama) **wajar untuk faktur tahun 2024** dan tidak perlu tindakan.
- F1 lainnya cocok: jumlah item = DPP, NPWP 16 digit, NITKU 22 digit sesuai NPWP, nomor seri 17 digit (kode transaksi 04 = DPP nilai lain, status 00 = normal), terbilang sesuai jumlah tertulis.

**Rekap pengeluaran**
Total tertulis: Rp 17.590.000 · PPN dari faktur pajak: Rp 1.840.000
(Bila F1 dikoreksi penjual: total menjadi Rp 17.482.500 dan PPN Rp 1.732.500.)

| Bulan | Dokumen | Total |
|---|---|---|
| 2024-12 | 1 | Rp 5.550.000 |
| 2026-09 | 1 | Rp 12.040.000 |

**CSV (siap tempel ke Excel, pemisah ;)**
```csv
No;ID;Tanggal;Jenis;Nomor Dokumen;Penjual;NPWP Penjual;Pembeli;Kategori;Subtotal;Diskon;DPP;PPN;PPh;Biaya Lain;Total;Subtotal Hitung Ulang;DPP Hitung Ulang;PPN Seharusnya;Total Seharusnya;Total Untuk Rekap;Ikut Rekap;Jatuh Tempo;Rekening Tujuan;Metode Bayar;Status Cek;Kolom Tidak Terbaca;Catatan
1;F1;2026-09-15;faktur_pajak;04.00.26.00007654321;PT Kemas Jaya Fiktif;"=""0011112222333444""";CV Kopi Nusantara Fiktif;Bahan kemasan;10750000;;10750000;1290000;;;12040000;;;1182500;11932500;12040000;ya;;;;PERLU DICEK;;
2;F2;2024-12-18;faktur_pajak;010.000-24.12345678;PT Kemas Jaya Fiktif;01.111.222.2-333.444;CV Kopi Nusantara Fiktif;Bahan kemasan;5000000;;5000000;550000;;;5550000;;;550000;5550000;5550000;ya;;;;COCOK;;
```
Kolom PPN/Total = angka tertulis di faktur; **PPN Seharusnya**/**Total Seharusnya** = hitung ulang sebagai pembanding. Total Untuk Rekap F1 tetap angka tertulis (Rp 12.040.000) sampai penjual mengoreksi.

Catatan: faktur F2 bertanggal Desember 2024. Apakah PPN masukannya masih bisa dikreditkan (ada batas waktu pengkreditan) perlu ditanyakan ke konsultan pajak atau Kring Pajak 1500200. Skill ini tidak memutuskan hal itu.

_Dasar PPN: UU HPP & PMK 131/2024, per 23 September 2026. Format NPWP/NITKU/nomor faktur: belum terverifikasi dari dokumen resmi, hanya peringatan. Alat bantu cek, bukan nasihat pajak; untuk kepastian hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._

## Versi kanal chat (Telegram/WhatsApp) — ditambahkan 2026-10-16 (v1.0.5)
Tanpa tabel Markdown; angka sama dengan keluaran script di atas:

> **Hasil baca & cek 2 dokumen**
> F1 · 15-09-2026 · PT Kemas Jaya Fiktif · Faktur pajak · Rp 12.040.000 · ⚠️ Perlu dicek
> F2 · 18-12-2024 · PT Kemas Jaya Fiktif · Faktur pajak · Rp 5.550.000 · ✅ Cocok
>
> **Yang perlu Anda cek**
> • F1: PPN ditulis Rp 1.290.000 (12% × DPP penuh). Untuk kardus & lakban seharusnya Rp 1.182.500, total seharusnya Rp 11.932.500 (lebih Rp 107.500). Tanyakan ke penjual sebelum membayar.
> • F2: PPN Rp 550.000 benar untuk tarif 2024; NPWP 15 digit wajar untuk tahun itu.
>
> **Rekap:** total tertulis Rp 17.590.000 · PPN dari faktur pajak Rp 1.840.000 · Des 2024 Rp 5.550.000 (1) · Sep 2026 Rp 12.040.000 (1)
>
> 📎 rekap-faktur.csv (dilampirkan sebagai dokumen bila diminta)

CSV di chat (`--pemisah tab`, kolom kosong di semua baris dibuang: Subtotal Hitung Ulang, DPP Hitung Ulang, Diskon, PPh, Biaya Lain, Jatuh Tempo, Rekening Tujuan, Metode Bayar, Kolom Tidak Terbaca, Catatan):
```
No	ID	Tanggal	Jenis	Nomor Dokumen	Penjual	NPWP Penjual	Pembeli	Kategori	Subtotal	DPP	PPN	Total	PPN Seharusnya	Total Seharusnya	Total Untuk Rekap	Ikut Rekap	Status Cek
1	F1	2026-09-15	faktur_pajak	04.00.26.00007654321	PT Kemas Jaya Fiktif	"=""0011112222333444"""	CV Kopi Nusantara Fiktif	Bahan kemasan	10750000	10750000	1290000	12040000	1182500	11932500	12040000	ya	PERLU DICEK
2	F2	2024-12-18	faktur_pajak	010.000-24.12345678	PT Kemas Jaya Fiktif	01.111.222.2-333.444	CV Kopi Nusantara Fiktif	Bahan kemasan	5000000	5000000	550000	5550000	550000	5550000	5550000	ya	COCOK
```

## Catatan penguji
- **Verifikasi independen PPN** (aritmetika integer, terpisah dari script): 10.750.000 × 12% × 11/12 = 10.750.000 × 11/100 = 1.182.500 (tepat, tidak ada pecahan). 12% penuh = 1.290.000. Selisih 107.500. F2: 5.000.000 × 11% = 550.000 (tarif 1 Apr 2022–31 Des 2024). DPP nilai lain 10.750.000 × 11/12 = 9.854.166,67, tertulis 9.854.167 dan cocok. Semua sesuai dengan output script.
- Bagus: peringatan 12% penuh ditulis sebagai "tanyakan ke penjual", bukan tuduhan. Tidak ada kata "palsu". Tarif mengikuti tanggal dokumen.
- *(Catatan 2026-10-16: kedua temuan "Kurang (ringan)" di bawah sudah diperbaiki di versi skill berikutnya — F2 kini COCOK dan script mengeluarkan PPN/Total Seharusnya; keluaran di atas sudah disegarkan ke v1.0.5. Penilaian penguji tetap penilaian uji 2026-09-23.)*
- **Kurang (ringan):** script memberi peringatan NPWP 15 digit **pada faktur 2024** ("minta penjual memperbarui identitas bila dokumen bertanggal 2025 ke atas"). Akibatnya status F2 menjadi "PERLU DICEK" padahal untuk tanggal itu formatnya normal. `cek_npwp` (baris 297–313) tidak menerima tanggal. Saran: teruskan `tanggal`. Bila < 2025-01-01 (atau < 1 Jul 2024), jadikan level `info`/`ok`.
- **Kurang (ringan):** script tidak menghitung "total seharusnya" saat PPN dinilai keliru. Angka Rp 11.932.500 dan Rp 107.500 dihitung agent dari angka script. SKILL.md langkah 4 meminta angka dari script apa adanya. Saran: tambahkan `ppn_seharusnya` dan `total_seharusnya` ke hasil JSON agar agent tidak perlu berhitung.
