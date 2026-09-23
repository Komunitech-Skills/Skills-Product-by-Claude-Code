# 02 — "Bikinin dong" rekonsiliasi Mandiri (debet/kredit terpisah, QRIS, angka format Indonesia)

**Skenario:** S2 — permintaan singkat/malas. Ekspor bergaya Mandiri (kolom `Debit`/`Credit` terpisah, tanggal `01/08/26`, angka `1.250.000,00`, dua kolom bernama sama "Description"), catatan invoice pakai titik koma dan satu nominal `"1.750.000,50"`. Semua fiktif.

**Input pengguna (persis):**
> bikinin dong rekonsiliasi mutasi mandiri agustus ama invoice, filenya mutasi-mandiri-agustus.csv sama invoice-agustus.csv. cepet aja gak usah nanya2

## Output (mengikuti SKILL.md)

> 🔒 Data rekening hanya dibaca di komputer ini; jangan tempel PIN/OTP. Hapus data sensitif sebelum membagikan hasil.

Karena Anda minta cepat, saya langsung pakai tebakan kolom (**asumsi**): mutasi **mirip Mandiri** — tanggal = "Date", keterangan = "Description", uang masuk = "Credit", uang keluar = "Debit". Catatan — tanggal = "Tanggal", nominal = "Grand Total", invoice = "No", pelanggan = "Nama Pelanggan". Kalau ada yang keliru, bilang saja, saya ulang.

## Rekonsiliasi Mandiri — 1–31 Agustus 2026
Total catatan: **Rp 10.460.001** · Total uang masuk bank: **Rp 8.705.773** · Selisih: **Rp 1.754.228**

| Kelompok | Jumlah | Nilai catatan | Nilai bank |
|---|---:|---:|---:|
| ✅ Cocok | 4 | Rp 7.230.000 | Rp 7.230.000 |
| 🟡 Cocok parsial (perlu dicek) | 2 | Rp 1.480.000 | Rp 1.467.650 |
| ❌ Ada di catatan, tidak ada di bank | 1 | Rp 1.750.001 | — |
| ❓ Ada di bank, tidak ada di catatan | 1 | — | Rp 8.123 |

### Penjelasan selisih Rp 1.754.228
+ Rp 1.750.001 invoice belum terlihat masuk bank
− Rp 8.123 uang masuk yang belum dicatat
+ Rp 12.350 beda nominal pada cocok parsial
= **Rp 1.754.228 (seimbang ✔)**

### ❌ Belum ada di bank → tindakan
| Tgl | Invoice | Pelanggan | Nominal | Saran |
|---|---|---|---:|---|
| 28/08 | 209 | Pak Harun | Rp 1.750.001 | Cek bukti transfer / tagih (`tagih-piutang`). Nominal di catatan ada ",50" — mungkin salah ketik |

### ❓ Belum ada di catatan → tindakan
| Tgl | Keterangan (disamarkan) | Nominal | Kemungkinan |
|---|---|---:|---|
| 31/08 | (kosong) | Rp 8.123 | Tanggal akhir bulan & nominal kecil — kemungkinan bunga jasa giro; catat sebagai pendapatan bunga |

### 🟡 Cocok parsial → cek satu per satu
| Catatan | Bank | Selisih | Alasan |
|---|---|---:|---|
| 208 Penjualan QRIS 13 Agt Rp 1.000.000 | 14/08 QRIS SETTLEMENT Rp 987.650 | Rp 12.350 | Settlement QRIS sudah dipotong biaya (MDR). Cocokkan dengan laporan penarikan dana QRIS, bukan per transaksi |
| 207 Fajar Nugroho 12/08 Rp 480.000 | 20/08 YULIA Rp 480.000 | Rp 0 | Nominal sama, +8 hari. ⚠ Nama pengirim YULIA, bukan Fajar — cek ulang |

✅ Cocok: 201 Toko Bunga Melati, 202 Yulia (⚠ uangnya dari FAJAR NUGROHO ****0123 tgl 03/08 — kemungkinan tertukar dengan baris 207 di atas), 205 Lina (no. invoice ada di berita transfer), 206 CV Makmur Sentosa.

Dilewati: 1 transaksi uang keluar (biaya administrasi Rp 12.500) diabaikan karena arah = uang masuk.

Catatan: nomor rekening di keterangan disamarkan. Hapus file mutasi & hasil dari folder bersama setelah selesai.

## Catatan penguji
- ✅ Menghormati "gak usah nanya2": memakai tebakan dan menyebutnya sebagai asumsi (sesuai langkah 3).
- ✅ Angka diverifikasi manual: catatan 1.250.000+480.000+2.000.000+3.500.000+480.000+1.000.000+1.750.001 = 10.460.001; kredit bank 1.250.000+480.000+2.000.000+3.500.000+987.650+480.000+8.123 = 8.705.773; 1.750.001 − 8.123 + 12.350 = 1.754.228 ✔. `"1.750.000,50"` dibulatkan ke Rp 1.750.001 (sesuai aturan pembulatan script).
- ❌ **Salah pasang lagi (COCOK yang yakin):** transfer FAJAR NUGROHO 03/08 dipasangkan ✅ COCOK ke invoice **Yulia** (tanggal sama, tanpa cek nama), lalu transfer YULIA 20/08 dipasangkan ke invoice Fajar. Script tidak menurunkan status ketika nama di keterangan jelas milik pelanggan lain.
- ⚠ Kolom "Description" ganda: script hanya menyimpan kolom kedua, sehingga "BUNGA JASA GIRO" hilang dan baris bunga tidak dikenali sebagai bunga (keterangan kosong). Tebakan "bunga" di atas dari agent, bukan script.
- ⚠ Alasan PARSIAL QRIS dari script berbunyi "kemungkinan baru bayar sebagian" — kurang tepat untuk settlement QRIS (biaya MDR); agent perlu menerjemahkan.
