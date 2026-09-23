# 03 — Cocokkan pembayaran supplier di mutasi BRI (arah keluar)

**Skenario:** S3 — permintaan normal, variasi arah uang keluar. Ekspor bergaya BRI (`TGL_TRAN, DESK_TRAN, MUTASI_DEBET, MUTASI_KREDIT, SALDO_AKHIR_MUTASI`, tanggal+jam, info rekening di atas) vs daftar pembelian. Semua fiktif.

**Input pengguna (persis):**
> Mbak/Mas, saya admin keuangan CV. Tolong cocokin pembayaran ke supplier di mutasi BRI Oktober (mutasi-bri-okt-keluar.csv) sama catatan pembelian (pembelian-okt.csv). Mau tau faktur mana yang belum kebayar.

## Output (mengikuti SKILL.md)

> 🔒 Data rekening hanya dibaca di komputer ini; jangan tempel PIN/OTP. Hapus data sensitif sebelum membagikan hasil.

Konfirmasi kolom:
> Mutasi (**mirip BRI**, tebakan): tanggal = "TGL_TRAN", keterangan = "DESK_TRAN", uang keluar = "MUTASI_DEBET", uang masuk = "MUTASI_KREDIT" (kolom saldo tidak dipakai). Catatan pembelian: tanggal = "Tanggal", nominal = "Jumlah", faktur = "No Faktur", dan nama supplier = "Supplier" (kolom ini tidak terdeteksi otomatis — saya pakai). Saya cocokkan **uang keluar** (`--arah keluar`). Benar?

Pengguna: "betul".

## Rekonsiliasi BRI (uang keluar vs pembelian) — Oktober 2026
Total catatan pembelian: **Rp 20.565.000** · Total uang keluar bank: **Rp 20.214.000** · Selisih: **Rp 351.000**

| Kelompok | Jumlah | Nilai catatan | Nilai bank |
|---|---:|---:|---:|
| ✅ Cocok | 2 | Rp 5.715.000 | Rp 5.715.000 |
| 🟡 Cocok parsial (perlu dicek) | 2 | Rp 13.500.000 | Rp 13.493.500 |
| ❌ Ada di catatan, tidak ada di bank | 1 | Rp 1.350.000 | — |
| ❓ Ada di bank, tidak ada di catatan | 2 | — | Rp 1.005.500 |

### Penjelasan selisih Rp 351.000
+ Rp 1.350.000 faktur belum terlihat dibayar dari rekening ini
− Rp 1.005.500 uang keluar yang belum dicatat
+ Rp 6.500 beda nominal pada cocok parsial
= **Rp 351.000 (seimbang ✔)**

### ❌ Faktur belum terlihat dibayar → tindakan
| Tgl | Faktur | Supplier | Nominal | Saran |
|---|---|---|---:|---|
| 27/10 | PB-05 | UD Telur Segar | Rp 1.350.000 | Belum dibayar, dibayar tunai, atau dari rekening lain? Cek ke supplier |

### ❓ Uang keluar belum dicatat → tindakan
| Tgl | Keterangan | Nominal | Kemungkinan |
|---|---|---:|---|
| 28/10 | NBMB TRF KE BU SITI (PRIBADI) | Rp 1.000.000 | Tampaknya dana pribadi → catat sebagai prive/pengambilan pemilik, pisahkan dari biaya usaha |
| 31/10 | BIAYA ADMIN BULANAN | Rp 5.500 | Biaya bank → catat sebagai biaya administrasi bank |

### 🟡 Cocok parsial → cek satu per satu
| Catatan | Bank | Selisih | Alasan |
|---|---|---:|---|
| PB-03 CV Kemasan Jaya Rp 5.500.000 | 09/10 + 16/10 @ Rp 2.750.000 | Rp 0 | Dibayar 2 kali (termin) |
| PB-04 PT Gula Manis Rp 8.000.000 | 20/10 Rp 7.993.500 | Rp 6.500 | Dibayar kurang Rp 6.500 — cek apakah ada potongan/diskon atau kekurangan bayar ke supplier |

✅ Cocok: PB-01 UD Sumber Pangan (02/10, nama ada di berita), PB-02 PLN (BRIVA, +1 hari).
Dilewati: 1 baris "SALDO AWAL" (nominal kosong); 1 transaksi uang masuk diabaikan (arah = keluar).

Catatan: nomor rekening di keterangan disamarkan (`****9991`). Hapus file mutasi & hasil setelah selesai.

## Catatan penguji
- ✅ Mode `--arah keluar` bekerja; termin 2× dan beda tipis terdeteksi; totals diverifikasi manual: pembelian 4.500.000+1.215.000+5.500.000+8.000.000+1.350.000 = 20.565.000; debet 4.500.000+1.215.000+2.750.000×2+7.993.500+1.000.000+5.500 = 20.214.000; 1.350.000 − 1.005.500 + 6.500 = 351.000 ✔. Angka format `"4.500.000,00"` terbaca benar.
- ⚠ Teks alasan script tetap berorientasi penjualan pada arah keluar ("bukan penjualan", "pemasukan lain", "potongan biaya transfer ... bank lebih kecil") — agent harus menerjemahkan manual. Perbaiki: alasan bergantung `--arah`.
- ⚠ `deteksi` memetakan "nominal" ke `SALDO_AKHIR_MUTASI` (salah, meski tak dipakai karena debet/kredit terpisah) dan tidak mengenali "Supplier" sebagai kolom nama (tambah "supplier", "vendor", "pemasok" ke `KATA_CATAT["nama"]`).
