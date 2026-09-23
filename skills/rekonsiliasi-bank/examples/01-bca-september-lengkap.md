# 01 — Rekonsiliasi BCA September (pembayaran gabungan, terpecah, potong biaya, PEND)

**Skenario:** S1 — permintaan normal. Pemilik toko kue punya ekspor mutasi BCA (baris info rekening di atas, tanggal `'02/09` tanpa tahun, kolom CR/DB tanpa judul, baris PEND, ringkasan saldo di bawah) dan daftar invoice (format "Rp 1.500.000", ada penjualan tunai dan invoice batal). Semua nama & nomor fiktif.

**Input pengguna (persis):**
> Ini mutasi BCA bulan September (mutasi-bca-sept.csv) sama daftar invoice toko (penjualan-sept.csv). Tolong dicocokin ya, mana yang udah masuk mana yang belum. Kok saldo bank sama catatan saya beda hampir 2 juta?

<details><summary>Data uji (fiktif)</summary>

`mutasi-bca-sept.csv` (dipotong): baris 1–4 `No. rekening : 8880001234`, `Nama : TOKO KUE CONTOH FIKTIF`, `Periode : 01/09/2026 - 30/09/2026`, `Kode Mata Uang : Rp`; judul `Tanggal Transaksi,Keterangan,Cabang,Jumlah,,Saldo`; 15 transaksi (12 CR, 3 DB) + 1 baris `PEND` (Joko Rp 450.000) + 4 baris ringkasan saldo.

`penjualan-sept.csv`: 13 baris `Tanggal,No Invoice,Pelanggan,Total,Metode,Status` (1 tunai, 1 batal).
</details>

## Output (mengikuti SKILL.md)

> 🔒 Data rekening hanya dibaca di komputer ini. Jangan tempel PIN/OTP/password di chat; hapus data sensitif sebelum membagikan hasil.

Langkah 2 (`deteksi`) → konfirmasi ke pengguna:

> Saya membaca mutasi (**mirip format BCA**, tebakan): tanggal = "Tanggal Transaksi", keterangan = "Keterangan", nominal = "Jumlah", penanda masuk/keluar = kolom ke-5 tanpa judul (CR/DB). Tanggal tanpa tahun → saya pakai **2026** dari baris "Periode". Catatan: tanggal = "Tanggal", nominal = "Total", invoice = "No Invoice", pelanggan = "Pelanggan", status = "Status", metode = "Metode". Sudah benar?

Pengguna: "iya bener". Langkah 4 (`cocokkan ... --output-csv hasil-rekonsiliasi.csv`) → `cek_rumus_seimbang = true`.

## Rekonsiliasi BCA — 1–30 September 2026
Total catatan: **Rp 14.600.000** · Total uang masuk bank: **Rp 12.655.846** · Selisih: **Rp 1.944.154**

| Kelompok | Jumlah | Nilai catatan | Nilai bank |
|---|---:|---:|---:|
| ✅ Cocok | 3 | Rp 2.400.000 | Rp 2.400.000 |
| 🟡 Cocok parsial (perlu dicek) | 4 | Rp 8.600.000 | Rp 8.600.000 |
| ❌ Ada di catatan, tidak ada di bank | 3 | Rp 3.600.000 | — |
| ❓ Ada di bank, tidak ada di catatan | 4 | — | Rp 1.655.846 |

### Penjelasan selisih Rp 1.944.154
+ Rp 3.600.000 invoice belum terlihat masuk bank
− Rp 1.655.846 uang masuk yang belum dicatat
+ Rp 0 beda nominal pada cocok parsial
= **Rp 1.944.154 (seimbang ✔)**

### ❌ Belum ada di bank → tindakan
| Tgl | Invoice | Pelanggan | Nominal | Saran |
|---|---|---|---:|---|
| 18/09 | INV-107 | Hendra Wijaya | Rp 3.000.000 | ⚠ Lihat catatan agent di bawah: ada transfer HENDRA WIJAYA Rp 1.000.000 tgl 20/09 yang oleh script dipasangkan ke invoice lain |
| 23/09 | INV-113 | Bu Tini | Rp 150.000 | Minta bukti transfer; bisa jadi transfer Rp 150.000 dari "ANDIKA PRATAMA" 23/09 sebenarnya untuk Bu Tini |
| 25/09 | INV-108 | Joko Susilo | Rp 450.000 | Ada transaksi **PEND** (tertunda) Rp 450.000 a.n. JOKO SUSILO — kemungkinan baru masuk setelah diproses bank; cek mutasi Oktober |

### ❓ Belum ada di catatan → tindakan
| Tgl | Keterangan (disamarkan) | Nominal | Kemungkinan |
|---|---|---:|---|
| 12/09 | SETORAN TUNAI ****5678 | Rp 350.000 | Setoran tunai: dari penjualan tunai atau dana pribadi? Catat sesuai asalnya |
| 15/09 | BI-FAST CR ... DEWI LESTARI ****6543 | Rp 993.500 | ⚠ Nama DEWI LESTARI — kemungkinan besar pembayaran INV-106 (Rp 1.000.000) terpotong biaya Rp 6.500 |
| 24/09 | TRSF E-BANKING CR ... SURYA ABADI | Rp 300.000 | Tanyakan: pesanan yang lupa dicatat? |
| 30/09 | BUNGA | Rp 12.346 | Bunga bank → catat sebagai pendapatan bunga, bukan penjualan |

### 🟡 Cocok parsial → cek satu per satu
| Catatan | Bank | Selisih | Alasan |
|---|---|---:|---|
| INV-111 Rina Marlina 01/09 Rp 600.000 | 11/09 RINA MARLINA Rp 600.000 | Rp 0 | Nominal sama, bank +10 hari (telat bayar?) |
| INV-103 + INV-104 CV Andalas Jaya Rp 1.200.000 + Rp 800.000 | 10/09 CV ANDALAS JAYA Rp 2.000.000 | Rp 0 | 1 transfer untuk 2 invoice |
| INV-105 PT Sumber Rejeki Rp 5.000.000 | 12/09 + 19/09 @ Rp 2.500.000 | Rp 0 | Dibayar 2 kali (termin) |
| INV-106 Dewi Lestari 14/09 Rp 1.000.000 | 20/09 **HENDRA WIJAYA** Rp 1.000.000 | Rp 0 | Script: nominal sama, +6 hari. ⚠ **Nama berbeda — hampir pasti salah pasang** |

**Catatan agent (hasil membaca nama, bukan dari script):** pasangan yang lebih masuk akal adalah INV-106 Dewi ↔ Rp 993.500 (potong biaya Rp 6.500) dan INV-107 Hendra ↔ Rp 1.000.000 (baru bayar 1 dari 3 juta, sisa Rp 2.000.000 perlu ditagih). Dengan pasangan itu penjelasan selisih menjadi +Rp 600.000 − Rp 662.346 + Rp 2.006.500 = Rp 1.944.154. Mohon konfirmasi sebelum mengubah catatan.

Dilewati: 1 baris PEND + 4 baris ringkasan saldo (tanggal tak terbaca); 3 transaksi uang keluar (DB) diabaikan; dari catatan dibuang 1 penjualan **Tunai** (INV-109) dan 1 **Batal** (INV-110).
⚠ Tanggal bank tanpa tahun dianggap 2026 (dari baris Periode).

File `hasil-rekonsiliasi.csv` (pemisah `;`, bisa dibuka di Excel) sudah dibuat.
Ingin saya bantu buat pesan penagihan untuk INV-107/INV-108/INV-113 dengan skill `tagih-piutang`?

Catatan: nomor rekening di keterangan disamarkan. Hapus file mutasi & `hasil-rekonsiliasi.csv` dari folder bersama setelah selesai.

## Catatan penguji
- ✅ Parsing BCA sempurna: baris info rekening dilewati, tahun diambil dari "Periode", kolom CR/DB tanpa judul terdeteksi (`kolom_5`), PEND & ringkasan saldo dilewati, `"12,345.67"` → Rp 12.346, "Rp 1.500.000" terbaca, tunai/batal dibuang.
- ✅ Diverifikasi independen (python terpisah, `verif_bca.py`): total catatan Rp 14.600.000, total CR bank Rp 12.655.846, selisih Rp 1.944.154 — **cocok**. Gabungan (Andalas) dan terpecah (Sumber Rejeki) terdeteksi benar. Nomor ≥ 8 digit disamarkan (`****5678`, `****6543`).
- ❌ **CACAT: salah pasang.** Tahap 2a (nominal sama, beda tanggal ≤ 14 hari) berjalan *sebelum* tahap 2d (potong biaya) dan 2e (nama cocok), dan tidak memeriksa nama. Akibatnya INV-106 Dewi dipasangkan ke transfer HENDRA WIJAYA, transfer Dewi Rp 993.500 jadi "tidak ada di catatan", dan INV-107 Hendra jadi "belum dibayar sama sekali" (padahal sudah bayar Rp 1 jt). Penjelasan selisih versi script (+3,6 jt − 1,66 jt + 0) **berbeda** dari yang benar (+0,6 jt − 0,66 jt + 2,0 jt). Rumus tetap "seimbang ✔" karena seimbang secara konstruksi, sehingga tanda ✔ memberi rasa aman palsu.
- ❌ **CACAT: kecocokan nama palsu.** INV-112 "Andi Saputra" dinyatakan ✅ COCOK dengan alasan "nama ada di keterangan bank" padahal pengirimnya "ANDIKA PRATAMA" (`andi` adalah substring `andika`).
- ⚠ Catatan agent di atas hanya muncul karena penguji membaca nama; SKILL.md tidak menyuruh agent memeriksa kejanggalan nama pada PARSIAL/COCOK, jadi agent lain kemungkinan meneruskan hasil yang salah.
- ⚠ Baris PEND tidak dilaporkan terpisah (digabung dengan "baris ringkasan saldo atau PEND": 5), padahal checklist meminta PEND disampaikan.
