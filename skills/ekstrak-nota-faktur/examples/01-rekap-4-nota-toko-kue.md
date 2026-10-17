# 01 — Rekap 4 nota belanja toko kue ke Excel

## Skenario
S1 — permintaan normal. Pemilik usaha kue rumahan mengirim 4 foto: struk minimarket (harga sudah termasuk PPN), nota tulisan tangan toko bahan kue (totalnya salah jumlah), invoice servis AC ber-PPN, dan kuitansi sewa tenda Rp 7,5 juta. Semua nama dan nomor fiktif.

## Input pengguna
> Tolong masukin 4 nota ini ke Excel ya, sekalian dicek angkanya bener nggak. [4 foto terlampir]

Isi foto (transkripsi yang dibaca agent):
```
[Foto 1] MINIMARKET SUMBER REJEKI FIKTIF        03-09-2026  TRX-0903-0045
  GULA PASIR 1KG      2 x 18.500     37.000
  TEPUNG TERIGU 1KG   3 x 14.200     42.600
  MARGARIN 200G       4 x  9.900     39.600
  TOTAL                             119.200
  QRIS                              119.200
  DPP 107.387   PPN 11.813

[Foto 2] Nota tulisan tangan — Toko Bahan Kue Aneka Fiktif, No. 0172, Tgl 5/9/2026
  Coklat blok 1 kg   5 x 62.000 = 310.000
  Keju cheddar 2 kg  2 x 98.000 = 196.000
  Mentega 1 kg       3 x 71.500 = 214.500
  Jumlah Rp 730.500   (Lunas, tunai)

[Foto 3] INVOICE INV/SJT/2026/0911 — CV Sejuk Teknik Fiktif, NPWP 0001234567890000, 10/09/2026
  Kepada: Dapur Kue Bu Rina (fiktif)
  Servis AC split  4 unit x 150.000   600.000
  Isi freon R32    2 unit x 350.000   700.000
  Subtotal / DPP                    1.300.000
  DPP Nilai Lain (11/12)            1.191.667
  PPN 12%                             143.000
  TOTAL                             1.443.000
  Terbilang: Satu juta empat ratus empat puluh tiga ribu rupiah   Transfer BCA

[Foto 4] KUITANSI No. 017/KW/IX/26 — Sudah terima dari Bu Rina, uang sejumlah
  "Tujuh juta lima ratus ribu rupiah", untuk sewa tenda & kursi acara 12 September 2026.
  Rp 7.500.000,-   Persewaan Tenda Pak Budi (fiktif)   (tidak terlihat meterai)
```

## Output
> **Disegarkan ke v1.0.5 (2026-10-16):** CSV di bawah adalah keluaran ulang `scripts/cek_nota.py --hari-ini 2026-09-23 --format csv --pemisah ";"` dari data hasil baca yang sama. Sejak v1.0.4/1.0.5 kolom angka dokumen dipisah dari kolom hitungan (**Subtotal Hitung Ulang**, **DPP Hitung Ulang**, **PPN Seharusnya**, **Total Seharusnya**, **Total Untuk Rekap**, dst.), dan judul lama "… Dihitung Script" tidak dipakai lagi. Status, selisih, dan rekap tidak berubah. Tampilan di bawah ini untuk Claude Code/Cursor; versi kanal chat (Telegram/WhatsApp, tanpa tabel Markdown) ada di bagian berikutnya.


**Hasil baca & cek 4 dokumen**

| # | Tanggal | Penjual | Jenis | Total | Status |
|---|---|---|---|---|---|
| N1 | 03-09-2026 | Minimarket Sumber Rejeki Fiktif | Struk | Rp 119.200 | ✅ Cocok |
| N2 | 05-09-2026 | Toko Bahan Kue Aneka Fiktif | Nota | Rp 730.500 | ❌ Ada selisih |
| I1 | 10-09-2026 | CV Sejuk Teknik Fiktif | Invoice | Rp 1.443.000 | ✅ Cocok |
| K1 | 12-09-2026 | Persewaan Tenda Pak Budi (fiktif) | Kuitansi | Rp 7.500.000 | ✅ Cocok (cek meterai) |

**Yang perlu Anda cek**
- **N2 (Toko Bahan Kue Aneka): total di nota Rp 730.500, padahal jumlah 3 barangnya Rp 720.500. Anda kemungkinan kelebihan bayar Rp 10.000.** Cek nota aslinya. Kalau memang salah jumlah, minta pengembalian atau potongan di belanja berikutnya.
- **K1 (sewa tenda Rp 7.500.000):** kuitansi di atas Rp 5.000.000 wajib bermeterai Rp 10.000 (UU 10/2020). Di foto meterainya tidak terlihat. Pastikan ada, atau minta penjual melengkapinya.
- N1: harga sudah termasuk PPN. DPP Rp 107.387 + PPN Rp 11.813 = Rp 119.200, sesuai tarif efektif 11% (12% × 11/12).
- I1: PPN Rp 143.000 benar (12% × DPP nilai lain Rp 1.191.667 = efektif 11% × Rp 1.300.000). Total dan terbilang cocok. NPWP penjual 16 digit.

**Rekap pengeluaran**
Total: **Rp 9.792.700** · PPN tercantum: Rp 154.813 (bukan dari faktur pajak, jadi belum bisa dikreditkan)

| Kategori | Dokumen | Total |
|---|---|---|
| Sewa | 1 | Rp 7.500.000 |
| Perbaikan & perawatan | 1 | Rp 1.443.000 |
| Bahan baku | 2 | Rp 849.700 |

| Penjual | Dokumen | Total |
|---|---|---|
| Persewaan Tenda Pak Budi (fiktif) | 1 | Rp 7.500.000 |
| CV Sejuk Teknik Fiktif | 1 | Rp 1.443.000 |
| Toko Bahan Kue Aneka Fiktif | 1 | Rp 730.500 |
| Minimarket Sumber Rejeki Fiktif | 1 | Rp 119.200 |

Per bulan: September 2026, 4 dokumen, Rp 9.792.700.
Total N2 direkap sesuai yang tertulis dan dibayar (Rp 730.500). Kalau selisih Rp 10.000 dikembalikan, kurangi totalnya.
Kategori ditebak dari isi dokumen. Beri tahu saya kalau Anda memakai kategori lain.

**CSV (siap tempel ke Excel, pemisah ;)**
```csv
No;ID;Tanggal;Jenis;Nomor Dokumen;Penjual;NPWP Penjual;Pembeli;Kategori;Subtotal;Diskon;DPP;PPN;PPh;Biaya Lain;Total;Subtotal Hitung Ulang;DPP Hitung Ulang;PPN Seharusnya;Total Seharusnya;Total Untuk Rekap;Ikut Rekap;Jatuh Tempo;Rekening Tujuan;Metode Bayar;Status Cek;Kolom Tidak Terbaca;Catatan
1;N1;2026-09-03;struk;TRX-0903-0045;Minimarket Sumber Rejeki Fiktif;;;Bahan baku;;;107387;11813;;;119200;119200;;11813;119200;119200;ya;;;QRIS;COCOK;;
2;N2;2026-09-05;nota;"=""0172""";Toko Bahan Kue Aneka Fiktif;;;Bahan baku;;;;;;;730500;720500;;;720500;730500;ya;;;tunai;ADA SELISIH;;Nota tulisan tangan
3;I1;2026-09-10;invoice;INV/SJT/2026/0911;CV Sejuk Teknik Fiktif;"=""0001234567890000""";Dapur Kue Bu Rina (fiktif);Perbaikan & perawatan;1300000;;1300000;143000;;;1443000;;;143000;1443000;1443000;ya;;;transfer BCA;COCOK;;
4;K1;2026-09-12;kuitansi;017/KW/IX/26;Persewaan Tenda Pak Budi (fiktif);;;Sewa;;;;;;;7500000;;;;;7500000;ya;;;tunai;COCOK;;Untuk sewa tenda & kursi acara 12 September 2026, meterai tidak terlihat
```
Cara pakai: simpan sebagai `rekap-nota.csv` lalu buka di Excel. File yang sama juga sudah saya simpan sebagai `rekap-nota.csv` (UTF-8 BOM). Kolom Subtotal/DPP/PPN/Total berisi angka yang tertulis di dokumen saja; hasil hitung ulang ada di kolom terpisah. Contoh: N2 tidak menulis subtotal, jadi kolom **Subtotal** kosong dan **Subtotal Hitung Ulang** = 720500 (jumlah 3 barang); **Total Seharusnya** 720500 vs **Total** 730500 menunjukkan selisih Rp 10.000.

_Dasar PPN: UU HPP & PMK 131/2024, per 23 September 2026. Format NPWP/NITKU/nomor faktur: belum terverifikasi dari dokumen resmi, hanya peringatan. Alat bantu cek, bukan nasihat pajak; untuk kepastian hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._

## Versi kanal chat (Telegram/WhatsApp) — ditambahkan 2026-10-16 (v1.0.5)
Di kanal chat tabel Markdown tidak dipakai. Isi dan angka sama dengan di atas (keluaran script yang sama), hanya bentuknya. *Disusun ulang dari keluaran di atas mengikuti aturan kanal chat v1.0.5; bukan hasil uji baru.*

> **Hasil baca & cek 4 dokumen**
> N1 · 03-09-2026 · Minimarket Sumber Rejeki Fiktif · Struk · Rp 119.200 · ✅ Cocok
> N2 · 05-09-2026 · Toko Bahan Kue Aneka Fiktif · Nota · Rp 730.500 · ❌ Ada selisih
> I1 · 10-09-2026 · CV Sejuk Teknik Fiktif · Invoice · Rp 1.443.000 · ✅ Cocok
> K1 · 12-09-2026 · Persewaan Tenda Pak Budi (fiktif) · Kuitansi · Rp 7.500.000 · ✅ Cocok (cek meterai)
>
> **Yang perlu Anda cek** (sama dengan daftar di atas)
>
> **Rekap pengeluaran:** total Rp 9.792.700 · PPN tercantum Rp 154.813 (bukan dari faktur pajak) · Sewa Rp 7.500.000 (1) · Perbaikan & perawatan Rp 1.443.000 (1) · Bahan baku Rp 849.700 (2) · September 2026: 4 dokumen
>
> 📎 rekap-nota.csv (dilampirkan sebagai dokumen; buka di Excel)

Bila CSV juga ditampilkan di chat: `--pemisah tab`, kolom yang kosong di semua baris dibuang utuh (Diskon, PPh, Biaya Lain, DPP Hitung Ulang, Jatuh Tempo, Rekening Tujuan, Kolom Tidak Terbaca), isi sel tidak diubah:
```
No	ID	Tanggal	Jenis	Nomor Dokumen	Penjual	NPWP Penjual	Pembeli	Kategori	Subtotal	DPP	PPN	Total	Subtotal Hitung Ulang	PPN Seharusnya	Total Seharusnya	Total Untuk Rekap	Ikut Rekap	Metode Bayar	Status Cek	Catatan
1	N1	2026-09-03	struk	TRX-0903-0045	Minimarket Sumber Rejeki Fiktif			Bahan baku		107387	11813	119200	119200	11813	119200	119200	ya	QRIS	COCOK	
2	N2	2026-09-05	nota	"=""0172"""	Toko Bahan Kue Aneka Fiktif			Bahan baku				730500	720500		720500	730500	ya	tunai	ADA SELISIH	Nota tulisan tangan
3	I1	2026-09-10	invoice	INV/SJT/2026/0911	CV Sejuk Teknik Fiktif	"=""0001234567890000"""	Dapur Kue Bu Rina (fiktif)	Perbaikan & perawatan	1300000	1300000	143000	1443000		143000	1443000	1443000	ya	transfer BCA	COCOK	
4	K1	2026-09-12	kuitansi	017/KW/IX/26	Persewaan Tenda Pak Budi (fiktif)			Sewa				7500000				7500000	ya	tunai	COCOK	Untuk sewa tenda & kursi acara 12 September 2026, meterai tidak terlihat
```
Bila kanal tidak bisa melampirkan berkas: jalur/folder kerja tidak disebut, cukup tawarkan "balas 'kirim file'".

## Catatan penguji
- Script: `cek_nota.py nota.json` (teks) dan `--format csv --pemisah ";" --output rekap-nota.csv`. Status, selisih, dan rekap diambil apa adanya.
- **Verifikasi independen** (`/tmp/uji-ekstrak-nota-faktur/verif/verif.py`, tanpa mengimpor script):
  - item N2 = 310.000 + 196.000 + 214.500 = 720.500, jadi selisih Rp 10.000 benar
  - struk: 119.200 × 100/111 = 107.387,39 → DPP 107.387, PPN 11.813 benar
  - I1: 1.300.000 × 11% = 143.000 dan 1.300.000 × 11/12 = 1.191.666,67 (tertulis 1.191.667, dalam toleransi) benar
  - rekap 119.200 + 730.500 + 1.443.000 + 7.500.000 = 9.792.700 dan PPN 11.813 + 143.000 = 154.813 benar
  - terbilang I1 dan K1 benar
- Bagus: pengingat meterai, pemisahan "PPN tercantum" vs "PPN dari faktur pajak", NPWP/nomor ber-nol di depan dibungkus `="…"`.
- *(Catatan 2026-10-16: temuan di bawah sudah diperbaiki sejak v1.0.4 — Subtotal N1/N2 kini kosong dan hasil jumlah ada di kolom "Subtotal Hitung Ulang"; CSV di atas sudah disegarkan. Penilaian penguji tetap penilaian uji 2026-09-23.)*
- **Kurang (ringan):** kolom **Subtotal** di CSV untuk N2 berisi 720500 hasil jumlah script, padahal di dokumen tidak ada subtotal (`subtotal: null`). Tidak ada penanda di CSV/JSON, sehingga bertentangan dengan aturan `references/skema-data.md` bagian 1 ("angka hasil hitungan hanya boleh muncul sebagai 'dihitung script'"). Agent di sini menambahkan catatan manual.
