# 01 — Rekonsiliasi BCA September (pembayaran gabungan, terpecah, potong biaya, PEND) — uji ulang v1.1.0

**Skenario:** S1, permintaan normal. Pemilik toko kue punya ekspor mutasi BCA dan daftar invoice.
- Ciri file BCA: ada baris info rekening di atas, tanggal `'02/09` tanpa tahun, kolom CR/DB tanpa judul, satu baris PEND, dan ringkasan saldo di bawah.
- Ciri daftar invoice: format "Rp 1.500.000", ada penjualan tunai dan invoice batal.
- Semua nama dan nomor fiktif.

**Input pengguna (persis):**
> Ini mutasi BCA bulan September (mutasi-bca-sept.csv) sama daftar invoice toko (penjualan-sept.csv). Tolong dicocokin ya, mana yang udah masuk mana yang belum. Kok saldo bank sama catatan saya beda hampir 2 juta?

<details><summary>Data uji (fiktif)</summary>

`mutasi-bca-sept.csv` (dipotong):
- baris 1–4: `No. rekening : 8880001234`, `Nama : TOKO KUE CONTOH FIKTIF`, `Periode : 01/09/2026 - 30/09/2026`, `Kode Mata Uang : Rp`
- judul kolom: `Tanggal Transaksi,Keterangan,Cabang,Jumlah,,Saldo`
- 15 transaksi (12 CR, 3 DB), 1 baris `PEND` (Joko Rp 450.000), dan 4 baris ringkasan saldo

`penjualan-sept.csv`: 13 baris dengan kolom `Tanggal,No Invoice,Pelanggan,Total,Metode,Status`. Di dalamnya ada 1 penjualan tunai dan 1 invoice batal.
</details>

## Output (mengikuti SKILL.md, script v1.1.0)

> 🔒 Data rekening hanya dibaca di komputer ini. Jangan tempel PIN/OTP/password di chat; hapus data sensitif sebelum membagikan hasil.

Konfirmasi kolom (hasil `deteksi`):
> Saya membaca mutasi (**mirip format BCA**, tebakan):
> - tanggal = "Tanggal Transaksi"
> - keterangan = "Keterangan"
> - nominal = "Jumlah"
> - penanda masuk/keluar = kolom ke-5 tanpa judul (CR/DB)
>
> Tanggalnya tanpa tahun, jadi saya pakai **2026** dari baris "Periode".
>
> Catatan: tanggal = "Tanggal", nominal = "Total", invoice = "No Invoice", pelanggan = "Pelanggan", status = "Status", metode = "Metode".
>
> Sudah benar?

Pengguna: "iya bener". Hasil `cocokkan`: `cek_rumus_seimbang = true`.

## Rekonsiliasi BCA — 1–30 September 2026
Total catatan: **Rp 14.600.000** · Total uang masuk bank: **Rp 12.655.846** · Selisih: **Rp 1.944.154**

| Kelompok | Jumlah | Nilai catatan | Nilai bank |
|---|---:|---:|---:|
| ✅ Cocok | 3 | Rp 2.400.000 | Rp 2.400.000 |
| 🟡 Cocok parsial (perlu dicek) | 5 | Rp 11.600.000 | Rp 9.593.500 |
| ❌ Ada di catatan, tidak ada di bank | 2 | Rp 600.000 | — |
| ❓ Ada di bank, tidak ada di catatan | 3 | — | Rp 662.346 |

*Dari 3 yang "cocok", 1 (INV-113) nama pengirimnya berbeda. Pasangan ini saya tandai "perlu dicek" di bawah.*

### Penjelasan selisih Rp 1.944.154
+ Rp 600.000 invoice belum terlihat masuk bank
− Rp 662.346 uang masuk yang belum dicatat
+ Rp 2.006.500 beda nominal pada cocok parsial
= **Rp 1.944.154** (angka seimbang, tetapi tetap cek pasangan bertanda 🟡. Seimbang tidak berarti semua pasangan benar.)

### ❌ Belum ada di bank → tindakan
| Tgl | Invoice | Pelanggan | Nominal | Saran |
|---|---|---|---:|---|
| 22/09 | INV-112 | Andi Saputra | Rp 150.000 | Minta bukti transfer / tagih (`tagih-piutang`) |
| 25/09 | INV-108 | Joko Susilo | Rp 450.000 | Ada transaksi **PEND** (tertunda) Rp 450.000 a.n. JOKO SUSILO. Kemungkinan masuk setelah diproses bank; cek mutasi Oktober sebelum menagih |

### ❓ Belum ada di catatan → tindakan
| Tgl | Keterangan (disamarkan) | Nominal | Kemungkinan |
|---|---|---:|---|
| 12/09 | SETORAN TUNAI ****5678 | Rp 350.000 | Setoran tunai: dari penjualan tunai atau dana pribadi? Catat sesuai asalnya |
| 24/09 | TRSF E-BANKING CR ... SURYA ABADI | Rp 300.000 | Tanyakan: pesanan yang lupa dicatat? |
| 30/09 | BUNGA | Rp 12.346 | Bunga bank → catat sebagai pendapatan bunga, bukan penjualan |

### 🟡 Cocok parsial → cek satu per satu
| Catatan | Bank | Selisih | Alasan |
|---|---|---:|---|
| INV-106 Dewi Lestari Rp 1.000.000 | 15/09 BI-FAST DEWI LESTARI Rp 993.500 | Rp 6.500 | Bank lebih kecil, kemungkinan terpotong biaya transfer → catat sebagai biaya transfer atau tagih kekurangan |
| INV-107 Hendra Wijaya Rp 3.000.000 | 20/09 HENDRA WIJAYA Rp 1.000.000 | Rp 2.000.000 | Baru bayar sebagian → **tagih sisa Rp 2.000.000** |
| INV-111 Rina Marlina 01/09 Rp 600.000 | 11/09 RINA MARLINA Rp 600.000 | Rp 0 | Nama & nominal sama, bank +10 hari (telat bayar) |
| INV-103 + INV-104 CV Andalas Jaya (Rp 1,2 jt + Rp 0,8 jt) | 10/09 CV ANDALAS JAYA Rp 2.000.000 | Rp 0 | 1 transfer untuk 2 invoice |
| INV-105 PT Sumber Rejeki Rp 5.000.000 | 12/09 + 19/09 @ Rp 2.500.000 | Rp 0 | Dibayar 2 kali (termin) |
| INV-113 Bu Tini 23/09 Rp 150.000 | 23/09 **ANDIKA PRATAMA** Rp 150.000 | Rp 0 | Script: cocok nominal & tanggal, "nama tidak terlihat". **Pengirim bukan Bu Tini**; tanyakan apakah Andika membayar atas nama Bu Tini |

✅ Cocok pasti: INV-101 Budi Santoso (02/09) dan INV-102 Toko Sari Roti (06/09). Nama keduanya ada di berita transfer.

Yang dilewati dan dibuang:
- 4 baris ringkasan saldo dilewati.
- 1 transaksi **tertunda (PEND)** Rp 450.000 tidak dihitung.
- 3 transaksi uang keluar diabaikan.
- Dari catatan dibuang 1 penjualan **Tunai** (INV-109) dan 1 invoice **Batal** (INV-110).

⚠ Tanggal bank tanpa tahun dianggap 2026 (dari baris Periode).

File `hasil-rekonsiliasi.csv` (pemisah `;`) sudah dibuat. Mau saya siapkan pesan penagihan untuk INV-107 (sisa Rp 2 jt) dan INV-112 dengan skill `tagih-piutang`?

Catatan: nomor rekening di keterangan disamarkan. Hapus file mutasi & `hasil-rekonsiliasi.csv` dari folder bersama setelah selesai.

## Catatan penguji (v1.1.0)

**Perbaikan terbukti:**
- Semua pasangan sekarang benar sesuai kunci jawaban data uji (`/tmp/uji-rekonsiliasi-bank/verif_v110.py`, 11/11 pasangan):
  - Dewi ↔ Rp 993.500 (potong biaya)
  - Hendra ↔ Rp 1 jt (baru bayar sebagian)
- Rincian selisih **+Rp 600.000 − Rp 662.346 + Rp 2.006.500 = Rp 1.944.154**, sama dengan hitungan independen.
- "Andi" tidak lagi dicocokkan ke "ANDIKA". Kata nama sekarang dicocokkan sebagai kata utuh.
- PEND dilaporkan terpisah (`transaksi_tertunda_pend`).

**Tersisa:**
- Pasangan INV-113 ↔ ANDIKA PRATAMA tetap berstatus **COCOK** di script, hanya dengan catatan "nama tidak terlihat — cek sekilas", dan ikut dihitung di baris ✅ ringkasan.
- SKILL.md langkah 5 sudah menyuruh agent tidak memberi ✅ pada pasangan seperti ini, sehingga agent menandainya manual. Akibatnya angka "✅ 3" di tabel tidak sama dengan jumlah pasangan yang benar-benar pasti (2).
