# 00 — Uji A/B: S1 dengan skill vs tanpa skill (uji ulang v1.1.0)

**Input (sama dengan S1):**
> Ini mutasi BCA bulan September (mutasi-bca-sept.csv) sama daftar invoice toko (penjualan-sept.csv). Tolong dicocokin ya, mana yang udah masuk mana yang belum. Kok saldo bank sama catatan saya beda hampir 2 juta?

Data sama persis dengan `01-bca-september-lengkap.md` (fiktif).

## A. Tanpa skill (agent umum, membaca kedua file lalu mencocokkan sendiri)

> Saya sudah membaca mutasi rekening **8880001234** a.n. TOKO KUE CONTOH FIKTIF periode September 2026 dan daftar invoice Anda.
>
> **Sudah masuk:**
> - INV-101 Budi Santoso Rp 1.500.000 (2/9) ✓
> - INV-102 Toko Sari Roti Rp 750.000 (6/9) ✓
> - INV-103 & INV-104 CV Andalas Jaya: dibayar sekaligus Rp 2.000.000 (10/9) ✓
> - INV-105 PT Sumber Rejeki Rp 5.000.000: dibayar 2× Rp 2.500.000 (12/9 & 19/9) ✓
> - INV-106 Dewi Lestari: masuk Rp 993.500 (15/9), kurang Rp 6.500 (biaya transfer)
> - INV-111 Rina Marlina Rp 600.000 (11/9) ✓
> - INV-112 Andi Saputra Rp 150.000: ada transfer Rp 150.000 dari Andika Pratama (23/9), mungkin ini
> - INV-108 Joko Susilo Rp 450.000: ada transfer dari Joko (status pending)
>
> **Belum masuk:**
> - INV-107 Hendra Wijaya Rp 3.000.000: baru masuk Rp 1.000.000 (20/9), kurang Rp 2.000.000
> - INV-113 Bu Tini Rp 150.000
> - INV-109 Pak Rahmat Rp 250.000
>
> **Uang masuk lain:** setoran tunai Rp 350.000, Surya Abadi Rp 300.000, bunga Rp 12.345,67.
>
> **Kenapa beda?** Total invoice Anda (tanpa yang batal) Rp 14.850.000, sedangkan uang masuk di bank Rp 13.105.845,67, jadi selisihnya sekitar Rp 1,74 juta. Selisih ini terutama karena pembayaran Hendra yang belum lunas dan beberapa invoice yang belum dibayar, dikurangi uang masuk lain yang tidak ada di catatan.

## B. Dengan skill v1.1.0
Lihat `01-bca-september-lengkap.md`. Ringkasnya:
- Konfirmasi kolom.
- Pasangan yang benar:
  - **Dewi ↔ Rp 993.500** (potong biaya Rp 6.500)
  - **Hendra ↔ Rp 1 jt** (sisa Rp 2 jt ditagih)
  - Rina (telat 10 hari)
  - Andalas (gabungan)
  - Sumber Rejeki (termin)
- Rincian selisih **+Rp 600.000 − Rp 662.346 + Rp 2.006.500 = Rp 1.944.154**.
- PEND Joko dilaporkan terpisah; penjualan tunai dan invoice batal dibuang.
- INV-113 ↔ ANDIKA ditandai "perlu dicek".
- Nomor rekening disamarkan, CSV untuk Excel dibuat, dan ada tawaran `tagih-piutang`.

## Penilaian
| Aspek | Tanpa skill | Dengan skill v1.1.0 |
|---|---|---|
| Ketepatan pasangan berdasarkan nama | Baik (membaca nama) | **Setara**: semua pasangan S1 benar (11/11 menurut kunci jawaban) |
| Angka total & selisih | **Salah**: penjualan tunai & transaksi PEND ikut dihitung → "±1,74 juta" | Benar: Rp 1.944.154, dengan rincian yang benar dan terverifikasi independen |
| Penjelasan selisih | Kualitatif, tidak bisa dicek | Rinci, seimbang ke rupiah |
| Pembayaran ANDIKA 150 rb | Ditebak untuk Andi Saputra (menebak dari potongan nama) | Tidak dipasangkan ke Andi; ditandai "perlu dicek" untuk Bu Tini |
| Privasi | Nomor rekening lengkap ditampilkan | Disamarkan + pengingat hapus file |
| Skala (ratusan baris) | Makin tidak andal | Deterministik, CSV keluaran |

**Kesimpulan:** dengan v1.1.0 skill **jelas lebih baik**. Kelemahan v1.0.0 (agent tanpa skill lebih tepat soal nama) sudah tertutup di S1, dan skill tetap unggul di angka, penanganan PEND/tunai/batal, privasi, dan format. (Output "tanpa skill" adalah simulasi penguji; kesalahan tunai & PEND adalah kesalahan umum agent tanpa panduan.)
