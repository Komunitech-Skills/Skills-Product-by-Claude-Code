# 02 — "Bikinin dong" rekonsiliasi Mandiri (debet/kredit terpisah, QRIS, kolom ganda) — uji ulang v1.1.0

**Skenario:** S2, permintaan singkat/malas.
- File mutasi bergaya Mandiri: kolom `Debit`/`Credit` terpisah, tanggal `01/08/26`, angka `1.250.000,00`, dan dua kolom bernama "Description" (jadi `Description` + `Description_2`).
- Catatan invoice memakai pemisah titik koma dan satu nominal ditulis `"1.750.000,50"`.
- Semua data fiktif.

**Input pengguna (persis):**
> bikinin dong rekonsiliasi mutasi mandiri agustus ama invoice, filenya mutasi-mandiri-agustus.csv sama invoice-agustus.csv. cepet aja gak usah nanya2

## Output (mengikuti SKILL.md, script v1.1.0)

> 🔒 Data rekening hanya dibaca di komputer ini; jangan tempel PIN/OTP. Hapus data sensitif sebelum membagikan hasil.

Karena Anda minta cepat, saya langsung memakai tebakan kolom (**asumsi**):
- Mutasi **mirip Mandiri**: tanggal = "Date", keterangan = "Description" + "Description_2" (keterangannya terbagi di dua kolom), uang masuk = "Credit", uang keluar = "Debit".
- Catatan: tanggal = "Tanggal", nominal = "Grand Total", invoice = "No", pelanggan = "Nama Pelanggan".

Kalau ada yang keliru, bilang saja, saya ulang.

## Rekonsiliasi Mandiri — 1–31 Agustus 2026
Total catatan: **Rp 10.460.001** · Total uang masuk bank: **Rp 8.705.773** · Selisih: **Rp 1.754.228**

| Kelompok | Jumlah | Nilai catatan | Nilai bank |
|---|---:|---:|---:|
| ✅ Cocok | 3 | Rp 6.750.000 | Rp 6.750.000 |
| 🟡 Cocok parsial (perlu dicek) | 3 | Rp 1.960.000 | Rp 1.947.650 |
| ❌ Ada di catatan, tidak ada di bank | 1 | Rp 1.750.001 | — |
| ❓ Ada di bank, tidak ada di catatan | 1 | — | Rp 8.123 |

### Penjelasan selisih Rp 1.754.228
+ Rp 1.750.001 invoice belum terlihat masuk bank
− Rp 8.123 uang masuk yang belum dicatat
+ Rp 12.350 beda nominal pada cocok parsial
= **Rp 1.754.228** (angka seimbang; tetap cek pasangan 🟡)

### ❌ Belum ada di bank → tindakan
| Tgl | Invoice | Pelanggan | Nominal | Saran |
|---|---|---|---:|---|
| 28/08 | 209 | Pak Harun | Rp 1.750.001 | Cek bukti transfer / tagih (`tagih-piutang`). Nominal di catatan ada ",50", mungkin salah ketik |

### ❓ Belum ada di catatan → tindakan
| Tgl | Keterangan | Nominal | Kemungkinan |
|---|---|---:|---|
| 31/08 | BUNGA JASA GIRO | Rp 8.123 | Bunga bank → catat sebagai pendapatan bunga |

### 🟡 Cocok parsial → cek satu per satu
| Catatan | Bank | Selisih | Alasan |
|---|---|---:|---|
| 208 Penjualan QRIS 13 Agt Rp 1.000.000 | 14/08 QRIS SETTLEMENT Rp 987.650 | Rp 12.350 | Dipotong biaya merchant QRIS (MDR). Cocokkan dengan laporan penarikan dana QRIS |
| 207 Fajar Nugroho 12/08 Rp 480.000 | 03/08 FAJAR NUGROHO ****0123 Rp 480.000 | Rp 0 | Nama sama, uang masuk 9 hari **sebelum** tanggal invoice (DP/bayar di muka?) |
| 202 Yulia 03/08 Rp 480.000 | 20/08 YULIA Rp 480.000 | Rp 0 | Nama sama, bank +17 hari (telat bayar) |

✅ Cocok (nama ada di berita transfer): 201 Toko Bunga Melati, 205 Lina (no. invoice ada di berita), 206 CV Makmur Sentosa.
Dilewati: 1 transaksi uang keluar (biaya administrasi Rp 12.500), karena yang dicocokkan hanya uang masuk.

Catatan: nomor rekening di keterangan disamarkan. Hapus file mutasi & hasil dari folder bersama setelah selesai.

## Catatan penguji (v1.1.0)

**Perbaikan terbukti:**
- Fajar ↔ transfer FAJAR dan Yulia ↔ transfer YULIA sekarang benar. Di v1.0.0 keduanya tertukar dan salah satunya ✅ COCOK.
- Kolom ganda sekarang menjadi `Description_2`, sehingga "BUNGA JASA GIRO" dikenali sebagai bunga.
- Alasan QRIS kini menyebut biaya merchant.
- "Toko Bunga Melati" tidak salah dikenali sebagai bunga bank.

**Angka diverifikasi independen:**
- Kunci jawaban 8/8 pasangan terpenuhi.
- Hitungan: 1.750.001 − 8.123 + 12.350 = 1.754.228 ✔.

**⚠ Tersisa:** `deteksi` hanya menyarankan "Description" sebagai keterangan, walaupun daftar `kolom_tersedia` memuat `Description_2`. Bila agent hanya memakai saran itu (tanpa kolom ke-2), hasilnya jadi buruk karena nama pengirim tidak terbaca:
- 4 pasangan "COCOK" dengan catatan "nama tidak terlihat"
- QRIS masuk "tidak ada di catatan"
- rincian +2,75 jt / −0,996 jt / +0

Di sini agent memakai dua kolom karena SKILL.md menyebut `Description_2`.
