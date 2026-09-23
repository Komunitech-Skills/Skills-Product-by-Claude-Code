# 00 — Uji A/B: S1 dengan skill vs tanpa skill

**Input (sama dengan S1):**
> Ini mutasi BCA bulan September (mutasi-bca-sept.csv) sama daftar invoice toko (penjualan-sept.csv). Tolong dicocokin ya, mana yang udah masuk mana yang belum. Kok saldo bank sama catatan saya beda hampir 2 juta?

Data sama persis dengan `01-bca-september-lengkap.md` (fiktif).

## A. Tanpa skill (agent umum, membaca kedua file lalu mencocokkan sendiri)

> Saya sudah membaca mutasi rekening **8880001234** a.n. TOKO KUE CONTOH FIKTIF periode September 2026 dan daftar invoice Anda.
>
> **Sudah masuk:**
> - INV-101 Budi Santoso Rp 1.500.000 (2/9) ✓
> - INV-102 Toko Sari Roti Rp 750.000 (6/9) ✓
> - INV-103 & INV-104 CV Andalas Jaya — dibayar sekaligus Rp 2.000.000 (10/9) ✓
> - INV-105 PT Sumber Rejeki Rp 5.000.000 — dibayar 2× Rp 2.500.000 (12/9 & 19/9) ✓
> - INV-106 Dewi Lestari — masuk Rp 993.500 (15/9), kurang Rp 6.500 (biaya transfer)
> - INV-111 Rina Marlina Rp 600.000 (11/9) ✓
> - INV-112 Andi Saputra Rp 150.000 — ada transfer Rp 150.000 dari Andika Pratama (23/9), mungkin ini
> - INV-108 Joko Susilo Rp 450.000 — ada transfer dari Joko (status pending)
>
> **Belum masuk:**
> - INV-107 Hendra Wijaya Rp 3.000.000 — baru masuk Rp 1.000.000 (20/9), kurang Rp 2.000.000
> - INV-113 Bu Tini Rp 150.000
> - INV-109 Pak Rahmat Rp 250.000
>
> **Uang masuk lain:** setoran tunai Rp 350.000, Surya Abadi Rp 300.000, bunga Rp 12.345,67.
>
> **Kenapa beda?** Total invoice Anda (tanpa yang batal) Rp 14.850.000, sedangkan uang masuk di bank Rp 13.105.845,67, jadi selisihnya sekitar Rp 1,74 juta. Selisih ini terutama karena pembayaran Hendra yang belum lunas dan beberapa invoice yang belum dibayar, dikurangi uang masuk lain yang tidak ada di catatan.

## B. Dengan skill
Lihat `01-bca-september-lengkap.md` (ringkas): konfirmasi kolom → tabel 4 kelompok (3 cocok / 4 parsial / 3 belum di bank / 4 belum di catatan) → **penjelasan selisih Rp 1.944.154 yang seimbang** → tabel tindakan per kelompok → file CSV untuk Excel → nomor rekening disamarkan → pengingat privasi. Namun 2 pasangan salah dari script (Dewi↔transfer Hendra; Andi↔"ANDIKA") yang hanya tertangkap karena agent membaca nama.

## Penilaian
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Ketepatan pasangan (data kecil 16 baris) | Lebih baik — agent membaca nama sehingga Dewi & Hendra benar | Script salah pasang 2 kasus; perlu koreksi agent |
| Angka total & selisih | **Salah**: penjualan **tunai** INV-109 ikut dihitung, transaksi **PEND** ikut dihitung sebagai uang masuk → selisih "±1,74 juta" (benar: Rp 1.944.154) | Benar & diverifikasi independen |
| Penjelasan selisih | Kualitatif, tidak bisa dicek | Rinci, seimbang ke rupiah |
| Privasi | Nomor rekening lengkap ditampilkan | Disamarkan + pengingat hapus file |
| Skala (ratusan baris) | Makin tidak andal (baca manual) | Deterministik, CSV keluaran |
| Tindak lanjut | Umum | Per kelompok + tawaran `tagih-piutang` |

**Kesimpulan:** Skill **lebih baik secara keseluruhan** (angka total/selisih benar, PEND/tunai/batal ditangani, privasi, format siap pakai, skala). Tetapi pada data ini agent tanpa skill justru lebih tepat memasangkan pembayaran berdasarkan nama — tanda bahwa logika pencocokan script perlu memakai nama sebagai pembeda sebelum tahap "nominal sama beda tanggal". (Output "tanpa skill" adalah simulasi penguji yang berusaha realistis: kesalahan tunai & PEND adalah kesalahan umum agent tanpa panduan.)
