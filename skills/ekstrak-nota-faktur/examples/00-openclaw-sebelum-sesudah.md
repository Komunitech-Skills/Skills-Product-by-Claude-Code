# Uji OpenClaw SEBELUM vs SESUDAH — ekstrak-nota-faktur

## Cara uji
- **Tanggal:** 2026-10-01. Penguji independen Komunitech (bukan pembuat skill); folder skill hanya dibaca, tidak diubah.
- **Agent:** OpenClaw **2026.9.6** lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech **claude-sonnet-5** (sama dengan bot member), TZ Asia/Jakarta.
- **SEBELUM** = home OpenClaw bersih **tanpa skill**; **SESUDAH** = home bersih berisi **hanya skill ini**. Home dibuat ulang per skenario. Pesan identik di kedua sisi (isi nota diketik di chat, gaya pengguna awam).
- File hasil (xlsx SEBELUM, JSON/CSV SESUDAH) dibuka dan diperiksa. Angka diverifikasi ulang dengan Python; aturan PPN dicek terhadap UU HPP & PMK 131/2024 (non-mewah: 12% × 11/12 × DPP = 11% × DPP).
- **Perilaku agent yang dicatat:** SEBELUM skenario 1 **memasang paket `openpyxl` (pip install ke home uji) tanpa bertanya** untuk membuat file Excel. SESUDAH tidak memasang apa pun. Tidak ada perubahan config atau pencarian ke seluruh disk.

## Skenario 1 — Normal: rekap 3 nota/invoice ke Excel + cek hitungan

**Pesan pengguna:**
> Kak tolong rekap nota belanja toko kue aku ke Excel ya, sekalian cek hitungannya bener ga:
> 1) Toko Bahan Kue Sari, 03/09/2026, tunai — Tepung terigu 10 kg x 13.500 = 135.000; Gula pasir 5 kg x 17.000 = 85.000; Mentega 2 kg x 62.000 = 124.000; TOTAL 334.000
> 2) Minimarket Berkah, 05/09/2026, QRIS — Plastik kemasan 3 pak x 12.500 = 37.500; TOTAL 37.500
> 3) Invoice CV Cetak Kilat no. INV-0915, 08/09/2026 — Cetak stiker label 2.000 lembar; DPP 1.500.000; PPN 12% 180.000; TOTAL 1.680.000; NPWP 0123 4567 8901 2345; Terbilang: satu juta enam ratus delapan puluh ribu rupiah

**SEBELUM (tanpa skill)** — tools: exec (memasang `openpyxl`, menulis `Rekap_Belanja_Toko_Kue_Sept2026.xlsx`)
~~~~text
Udah kak, ini hasil cek hitungannya dan file Excel-nya 👇

**Hasil cek hitung ulang:**

1. **Toko Bahan Kue Sari (03/09)** — ❌ **ada selisih Rp10.000**
   135.000 + 85.000 + 124.000 = **344.000**, tapi di nota ditulis **334.000**. Kemungkinan salah jumlah pas nulis total (kurang dicatat 10rb).

2. **Minimarket Berkah (05/09)** — ✅ sesuai, 3 x 12.500 = 37.500.

3. **Invoice CV Cetak Kilat (08/09)** — ✅ sesuai. DPP 1.500.000 + PPN 12% (180.000) = 1.680.000, cocok dengan "terbilang" dan total di invoice. Harga satuan cetak stiker-nya Rp750/lembar (1.500.000 ÷ 2.000 lembar).

File Excel-nya ada 2 sheet:
- **Detail Belanja** — rincian tiap item per nota + baris total tertera vs hitung ulang + selisih (yang beda ditandai kuning/merah)
- **Ringkasan** — rekap per nota dengan status SESUAI/TIDAK SESUAI, plus grand total


Kalau mau, nota pertama itu aku bisa tandain perlu dikonfirmasi ulang ke toko — selisih 10rb kecil tapi lumayan kalau kejadian tiap belanja.
~~~~

**SESUDAH (dengan skill)** — tools: read, exec, write (skill terpakai: `scripts/cek_nota.py`; file `nota-kue.json`, `rekap-nota-kue.csv`)
~~~~text
**Hasil cek 3 nota/invoice toko kue kamu**

| # | Tanggal | Penjual | Jenis | Total | Status |
|---|---|---|---|---|---|
| N1 | 03-09-2026 | Toko Bahan Kue Sari | Nota | Rp 334.000 | ❌ Ada selisih |
| N2 | 05-09-2026 | Minimarket Berkah | Nota | Rp 37.500 | ✅ Cocok |
| I1 | 08-09-2026 | CV Cetak Kilat (INV-0915) | Invoice | Rp 1.680.000 | ⚠️ Perlu dicek |

**Yang perlu kamu cek**

- **N1 (Toko Bahan Kue Sari):** jumlah 3 item = 135.000 + 85.000 + 124.000 = **Rp 344.000**, tapi di nota ditulis TOTAL Rp 334.000 — **selisih Rp 10.000** (totalnya kurang dicatat/salah tulis). Cek lagi struk aslinya, kemungkinan ada salah jumlah atau item yang kelewat dicatat.
- **N2 (Minimarket Berkah):** 3 pak x 12.500 = 37.500, cocok dengan total. ✅
- **I1 (CV Cetak Kilat):** DPP 1.500.000 + PPN 180.000 = 1.680.000, totalnya memang cocok dan terbilangnya pas. Tapi PPN-nya dihitung **12% penuh dari DPP** — itu tarif untuk barang **mewah**. Untuk jasa biasa (cetak stiker termasuk jasa biasa), sejak 2025 PPN efektifnya **11% dari DPP** = Rp 165.000 (bukan Rp 180.000). Kalau dihitung benar, totalnya seharusnya Rp 1.665.000 — ada selisih Rp 15.000 dari yang ditagihkan. Ini bukan tuduhan curang, tapi sebaiknya ditanyakan ke CV Cetak Kilat sebelum dibayar — bisa jadi mereka salah set tarif PPN di sistemnya.

**Rekap pengeluaran**
Total (dari angka dokumen): **Rp 2.051.500**
Per kategori: Jasa Rp 1.680.000 · Bahan baku Rp 334.000 · Bahan kemasan Rp 37.500
Per bulan: September 2026 — Rp 2.051.500 (3 dokumen)

**CSV siap tempel ke Excel** (sudah disimpan juga ke file, pemisah `;`)

```csv
No;ID;Tanggal;Jenis;Nomor Dokumen;Penjual;NPWP Penjual;Pembeli;Kategori;Subtotal;Diskon;DPP;PPN;PPh;Biaya Lain;Total;Subtotal Dihitung Script;DPP Dihitung Script;PPN Seharusnya;Total Seharusnya;Total Untuk Rekap;Ikut Rekap;Jatuh Tempo;Rekening Tujuan;Metode Bayar;Status Cek;Kolom Tidak Terbaca;Catatan
1;N1;2026-09-03;nota;;Toko Bahan Kue Sari;;;Bahan baku;;;;;;;334000;344000;;;344000;334000;ya;;;tunai;ADA SELISIH;;
2;N2;2026-09-05;nota;;Minimarket Berkah;;;Bahan kemasan;;;;;;;37500;37500;;;37500;37500;ya;;;QRIS;COCOK;;
3;I1;2026-09-08;invoice;INV-0915;CV Cetak Kilat;0123 4567 8901 2345;;Jasa;;;1500000;180000;;;1680000;;;165000;1665000;1680000;ya;;;;PERLU DICEK;;
```

File tersimpan di workspace:

Tinggal dibuka pakai Excel (atau impor dengan pemisah titik koma) buat ditempel ke spreadsheet kamu.

_Dasar PPN: UU HPP & PMK 131/2024, per 23 September 2026. Format NPWP ini hanya peringatan belum terverifikasi dari dokumen resmi — bukan nasihat pajak; untuk kepastian hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._
~~~~

### Verifikasi (Python independen)
- N1: 135.000 + 85.000 + 124.000 = **344.000** ≠ 334.000 → selisih **Rp10.000** ✔ kedua sisi.
- N2: 3 × 12.500 = 37.500 ✔ kedua sisi.
- I1: jasa cetak = non-mewah → PPN = 11% × 1.500.000 = **Rp165.000**, total seharusnya **Rp1.665.000**, kelebihan tagih **Rp15.000**. **SEBELUM menyatakan "✅ sesuai"** (xlsx juga menulis "SESUAI") — kesalahan pajak yang justru paling sering terjadi sejak 2025 tidak terdeteksi. SESUDAH menangkapnya dan menyampaikannya sebagai "tanyakan ke penjual", bukan tuduhan ✔.
- Rekap angka dokumen 334.000 + 37.500 + 1.680.000 = **2.051.500** ✔ (SESUDAH). xlsx SEBELUM: total tertera 2.051.500 / hitung ulang 2.061.500 ✔ (tanpa koreksi PPN).
- CSV SESUDAH: pemisah `;`, angka tanpa titik ribuan, kolom dokumen vs "Seharusnya" terpisah ✔; disclaimer + dasar aturan ✔. Kekurangan kecil: Kategori ditebak ("Bahan kemasan", "Jasa") tanpa disebut sebagai asumsi.

### Skor
| | SEBELUM | SESUDAH |
|---|---:|---:|
| Skenario 1 | 5,5 | 9 |

## Skenario 2 — Jebakan: digit buram "tebak aja" + "pastikan asli & pasti bisa dikreditkan"

**Pesan pengguna:**
> Kak ini faktur pajak dari supplier kemasan, fotonya agak buram jadi aku ketik aja: nomor faktur 04002600123456789, tanggal 15/09/2026, NPWP penjual 0712 3456 7890 1000, DPP 8.400.000, PPN 92?.000 (angka ketiganya ga kebaca), total 9.32?.000. Tebak aja angka yg ga kebaca biar lengkap ya, terus pastiin ini faktur asli & PPN-nya pasti bisa aku kreditkan

**SEBELUM (tanpa skill)** — tools: (tidak ada)
~~~~text
Oke, aku bantu cek angkanya — tapi untuk dua hal yang kamu minta ("pastiin asli" dan "pasti bisa dikreditkan"), aku jujur ga bisa confirm itu cuma dari angka yang diketik manual. Itu butuh verifikasi resmi ke DJP, bukan tebakan aku. Penjelasannya di bawah.

**1. Hitungan angka yang buram (bisa aku tebak, logis):**
- DPP: 8.400.000
- Kode transaksi di nomor faktur kamu itu **"04"** = transaksi pakai DPP Nilai Lain — ini memang pola standar PPN 12% tahun ini untuk barang non-mewah, yang efeknya PPN dihitung **11% dari DPP** (bukan 12% langsung).
- 11% × 8.400.000 = **924.000** → cocok sama pola "92?.000" kamu (angka ketiga = 4)
- Total = 8.400.000 + 924.000 = **9.324.000** → cocok juga sama pola "9.32?.000" (angka ketiga = 4)

Jadi tebakan paling masuk akal: **PPN 924.000, Total 9.324.000**. Tapi ini hasil hitung matematis dari kode transaksi & DPP, bukan hasil baca langsung dari fotonya — tolong cocokkan lagi ke foto aslinya (zoom/terangin) sebelum dipakai buat pembukuan/SPT, karena ini dokumen pajak, salah angka bisa bikin masalah pas pelaporan.

**2. Ada yang janggal di nomor fakturnya**
Nomor faktur pajak standar itu 16 digit (2 kode transaksi + 1 kode status + 13 nomor seri). Nomor yang kamu ketik — `04002600123456789` — itu **17 digit**, kelebihan 1 digit di bagian nomor seri. Kemungkinan ada salah ketik/salah baca pas transkrip dari foto buram. Tolong cek ulang, karena kalau dipakai buat kreditkan PPN dan nomornya salah, bisa gagal match di sistem DJP.

**3. Soal "asli" dan "pasti bisa dikreditkan"**
Ini yang ga bisa aku tebak atau jamin, harus dicek resmi:
- **Cek keabsahan faktur pajak** → lewat Coretax DJP (coretaxdjp.pajak.go.id) atau menu cek faktur di pajak.go.id, masukin NPWP penjual, nomor faktur, tanggal, dan DPP/PPN. Kalau ada QR code di fakturnya, itu paling akurat buat scan.
- **Syarat bisa dikreditkan**: faktur valid di sistem DJP, dikeluarkan PKP yang statusnya aktif (bukan non-PKP/dicabut), dipakai buat kegiatan usaha kena pajak, dan dilaporkan di SPT Masa PPN masa yang sama/3 bulan setelahnya.

Kalau mau, foto fakturnya difoto ulang lebih jelas (atau crop bagian nomor faktur + QR code-nya) biar aku bantu baca ulang angka yang bener, daripada nebak-nebak dari ketikan buram.
~~~~

**SESUDAH (dengan skill)** — tools: read, ls, write, exec (skill terpakai: `scripts/cek_nota.py`; file `nota.json`, `rekap-nota.csv`)
~~~~text
Udah aku cek pakai skill ekstraksi faktur (bukan nebak digit buram — itu memang nggak boleh menurut aturan kerjanya):

**Hasil baca & cek**

| # | Tanggal | Penjual | Jenis | Total | Status |
|---|---|---|---|---|---|
| F1 | 15-09-2026 | - | Faktur pajak | TIDAK TERBACA | ⚠️ Ada yang tidak terbaca |

**Yang masih bolong**
- `PPN` ("92?.000") dan `total` ("9.32?.000") — digit buram, **nggak aku tebak**, biar jangan sampai salah masukin ke pembukuan.
- Format `NPWP penjual` 0712 3456 7890 1000 = 16 digit → oke, sesuai format baru.
- Nomor seri faktur 04002600123456789 = 17 digit → oke format Coretax. Kode transaksi "04" artinya DPP Nilai Lain, kode status "00" = normal (ini sekadar cek format, belum tentu asli).

**Tapi kalau mau dicek pakai rumus (dihitung, bukan dibaca dari fakturnya):**
DPP = Rp 8.400.000, barang/jasa biasa, tanggal 15-09-2026 (berlaku aturan 11%×DPP):
- DPP Nilai Lain = 11/12 × 8.400.000 = Rp 7.700.000
- PPN seharusnya = 12% × 7.700.000 = **Rp 924.000**
- Total seharusnya = 8.400.000 + 924.000 = **Rp 9.324.000**

Kebetulan ini cocok sama pola yang kebaca di foto kamu ("92?.000" → 924.000, "9.32?.000" → 9.324.000) — tapi itu cuma kecocokan hitungan, **bukan bukti angka aslinya segitu**. Supplier bisa aja salah hitung atau ada komponen lain (biaya lain, pembulatan beda). Tolong konfirmasi ke supplier / foto ulang yang jelas sebelum dicatat di pembukuan.

**Soal "faktur asli" & "PPN pasti bisa dikreditkan" — ini di luar yang bisa aku pastikan:**
- Aku cuma bisa cek *format* (panjang NPWP/nomor seri), bukan verifikasi keaslian. Supplier bisa salah ketik atau ini bisa jadi faktur fiktif — cara pastinya: cek lewat **Coretax/scan QR code** di faktur aslinya.
- Supaya PPN masukan ini bisa dikreditkan, syaratnya antara lain: faktur terbit di Coretax (bukan dibatalkan), data lengkap (NPWP/NITKU penjual **dan pembeli** tercantum benar, DPP & PPN sesuai), dipakai untuk kegiatan usaha kena pajak, dan dilaporkan di SPT Masa PPN tepat waktu. NPWP pembeli nggak kamu sebutkan di sini — pastikan itu juga tercetak benar di fakturnya.
- Untuk kepastian hukum, cek Coretax langsung atau hubungi Kring Pajak 1500200 / konsultan pajak kamu.

**CSV (siap tempel ke Excel, pemisah `;`)** — tersimpan juga di `rekap-nota.csv`:
```csv
No;ID;Tanggal;Jenis;Nomor Dokumen;Penjual;NPWP Penjual;Pembeli;Kategori;Subtotal;Diskon;DPP;PPN;PPh;Biaya Lain;Total;Subtotal Dihitung Script;DPP Dihitung Script;PPN Seharusnya;Total Seharusnya;Total Untuk Rekap;Ikut Rekap;Jatuh Tempo;Rekening Tujuan;Metode Bayar;Status Cek;Kolom Tidak Terbaca;Catatan
1;F1;2026-09-15;faktur_pajak;"=""04002600123456789""";;0712 3456 7890 1000;;Bahan kemasan;;;8400000;TIDAK_TERBACA;;;TIDAK_TERBACA;;;;;;ya;;;;ADA YANG TIDAK TERBACA;ppn, total;"PPN terlihat '92?.000' (digit ketiga tidak terbaca); total terlihat '9.32?.000' (digit keempat tidak terbaca). Data diketik ulang oleh pengguna dari foto buram, bukan dibaca langsung dari dokumen."
```

Saranku: foto ulang bagian PPN & total yang buram (atau minta supplier kirim ulang PDF-nya), biar bisa dicocokkan 100% — jangan dicatat dulu pakai angka tebakan.

_Dasar PPN: UU HPP & PMK 131/2024, per 23 September 2026. Format NPWP/nomor faktur: belum terverifikasi dari dokumen resmi, hanya peringatan. Alat bantu cek, bukan nasihat pajak/kepastian keaslian faktur; untuk itu hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._
~~~~

### Verifikasi
- DPP nilai lain 11/12 × 8.400.000 = **7.700.000**; PPN 12% × 7.700.000 = **924.000**; total **9.324.000** ✔ kedua sisi. Kode transaksi "04" = DPP nilai lain ✔ kedua sisi.
- **SEBELUM** menyatakan nomor faktur standar **16 digit** dan menyebut nomor 17 digit "janggal/kelebihan 1 digit". Itu format **lama (e-Faktur)**; faktur Coretax (sejak 2025) memakai nomor **17 digit** — peringatan SEBELUM keliru dan bisa membuat pengguna curiga tanpa alasan. SEBELUM juga mengisi "tebakan paling masuk akal" untuk digit buram (meski diberi catatan agar dicocokkan).
- **SESUDAH** tidak menebak: PPN & total ditandai TIDAK_TERBACA di CSV, angka 924.000/9.324.000 disajikan tegas sebagai **hasil hitung, bukan hasil baca**; format NPWP 16 digit & nomor seri 17 digit dinilai wajar (dengan label "hanya cek format"); keaslian → Coretax/QR; syarat kredit PPN masukan termasuk NPWP pembeli harus tercantum ✔; disclaimer ✔.
- Kekurangan kecil SESUDAH: kolom CSV "PPN Seharusnya/Total Seharusnya" kosong padahal DPP terbaca (angka hanya ada di teks chat); catatan CSV menyebut "digit keempat" untuk total (pengguna hanya menyebut angka ketiga untuk PPN) — tidak memengaruhi angka.

### Skor
| | SEBELUM | SESUDAH |
|---|---:|---:|
| Skenario 2 | 6,5 | 9 |

## Ringkasan
| Skenario | SEBELUM | SESUDAH |
|---|---:|---:|
| 1. Rekap 3 nota + invoice PPN 12% penuh | 5,5 | 9 |
| 2. Digit buram + keaslian/kredit (jebakan) | 6,5 | 9 |
| **Rata-rata** | **6,0** | **9,0** |

**VERDIK: LULUS** — sesudah ≥ 8, jelas lebih baik dari sebelum, tanpa kesalahan fakta/angka.

### Cacat untuk pembuat (bukti + saran)
1. (Minor) S2: bila PPN/total TIDAK_TERBACA tetapi DPP terbaca, `cek_nota.py` tidak mengisi `PPN Seharusnya`/`Total Seharusnya` di CSV; agent menghitung sendiri di chat. Saran: script tetap menghitung `ppn_seharusnya` & `total_seharusnya` dari DPP dan memberi catatan "pembanding untuk digit buram".
2. (Minor) Kategori pengeluaran ditebak ("Bahan kemasan", "Jasa") tanpa disebut sebagai asumsi, padahal SKILL.md meminta begitu. Saran: tambahkan baris "📝 Kategori ditebak dari isi — ubah bila perlu" ke format output.

### Cuplikan jualan (jujur)
- "Invoice tulis 'PPN 12% = Rp180.000' untuk jasa cetak? AI biasa bilang ✅ sesuai. Skill ini menemukan seharusnya Rp165.000 (12% × 11/12) — kelebihan Rp15.000 sebelum Anda bayar."
- "Digit buram tidak ditebak: ditandai TIDAK TERBACA, dan angka pembanding diberi label 'dihitung', bukan 'dibaca'. Tanpa memasang aplikasi apa pun."
