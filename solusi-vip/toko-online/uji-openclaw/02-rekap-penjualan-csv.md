# Uji OpenClaw — Toko Online · Rekap penjualan sebulan dari CSV ekspor Shopee

Tanggal uji: 2026-10-01 (Asia/Jakarta) · Penguji independen · Skill yang diharapkan: `rekap-penjualan-csv`

OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`) yang sama dengan bot. SEBELUM = home `kosong-toko-online` (tanpa skill). SESUDAH = home `sol-toko-online` (paket skill solusi terpasang). Pesan identik.

**File uji (fiktif, sama persis di kedua workspace):** `penjualan-september.csv`, 72 baris gaya ekspor Shopee
(kolom `No. Pesanan, Status Pesanan, Waktu Pesanan Dibuat, Nama Produk, Harga Satuan, Jumlah, Total Harga Produk`,
angka format `Rp 59.000`), 5 produk hijab, status campuran: 66 Selesai, 4 Batal, 2 Pengembalian Dana. Tidak ada nama/nomor pembeli.

## Pesan member

> td aku udh taro file penjualan-september.csv di folder kerja (export dr shopee). tolong rekapin dong omzet sebulan brp, produk paling laku apa, sama hari paling rame kapan

## Balasan SEBELUM (tanpa skill) — utuh

_Alat yang dipakai agent: `exec, process, ls, read` · model jawaban: `claude-sonnet-5` · durasi 64 detik_

> Udah beres rekapnya, data diambil dari transaksi berstatus **Selesai** aja (4 batal & 2 refund dikecualikan, total 66 order valid).
>
> **📊 Omzet September: Rp 3.038.000**
>
> **🏆 Produk paling laku (by qty terjual):**
> 1. Pashmina Ceruty Babydoll — 30 pcs (Rp 1.350.000) ← kontributor omzet terbesar juga
> 2. Ciput Antem 3in1 — 21 pcs (Rp 252.000)
> 3. Bergo Instan Jersey — 19 pcs (Rp 665.000)
> 4. Inner Ninja Rajut — 16 pcs (Rp 240.000)
> 5. Hijab Voal Motif Premium — 9 pcs (Rp 531.000)
>
> **📅 Hari paling rame:**
> - By omzet tertinggi: **30 Sept** (Rp 285.000, 3 transaksi)
> - By jumlah order terbanyak: **1 & 5 Sept** sama-sama 5 transaksi (5 Sept omzetnya lebih gede, Rp 211.000)
>
> Jadi Pashmina Ceruty Babydoll itu best seller-nya — laris manis dan omzetnya paling gede. Mau aku breakdown per minggu juga atau bikinin rekap dalam bentuk tabel/excel biar gampang dilaporin?

## Balasan SESUDAH (dengan paket skill) — utuh

_Alat yang dipakai agent: `ls, read, exec, process` · model jawaban: `claude-sonnet-5` · durasi 56 detik_

> Udah aku rekap pakai data **penjualan-september.csv** (66 transaksi "Selesai", 1–30 Sep 2026). 4 pesanan Batal dan 2 Pengembalian Dana otomatis dikeluarkan dari omzet.
>
> ## Rekap Penjualan 1–30 September 2026
>
> **Total omzet:** Rp 3.038.000
> **Jumlah transaksi (baris):** 66
> **Rata-rata omzet per hari (kalender):** Rp 101.267 _(hari berjualan: Rp 108.500, dari 28 hari ada penjualan dari 30 hari)_
>
> ### 5 Produk Terlaris (omzet)
> | # | Produk | Qty | Omzet | % |
> |---|---|---|---|---|
> | 1 | Pashmina Ceruty Babydoll | 30 | Rp 1.350.000 | 44,4% |
> | 2 | Bergo Instan Jersey | 19 | Rp 665.000 | 21,9% |
> | 3 | Hijab Voal Motif Premium | 9 | Rp 531.000 | 17,5% |
> | 4 | Ciput Antem 3in1 | 21 | Rp 252.000 | 8,3% |
> | 5 | Inner Ninja Rajut | 16 | Rp 240.000 | 7,9% |
>
> ### Tren harian
> Hari terbaik: **30 September** (Rp 285.000). Hari terendah: **4 September** (Rp 12.000) — sama dengan 14 & 18 Sep (masing-masing juga Rp 12.000, kemungkinan hari sepi/tanggal tua).
>
> ### Insight
> 1. **Pashmina Ceruty Babydoll** adalah tulang punggung omzet — hampir separuh (44,4%) dari total bulan ini. Kalau produk ini kehabisan stok, omzet bakal langsung anjlok, jadi pastikan stoknya selalu aman.
> 2. Hari-hari sepi (Rp 12.000) justru jatuh di 4, 14, dan 18 September — semuanya bukan weekend dan bukan tanggal gajian/awal bulan. Pola ini layak dicek lagi bulan depan buat lihat apakah memang pola mingguan tertentu.
> 3. Akhir bulan (30 Sep) jadi hari terbaik — kemungkinan efek gajian/tanggal muda bulan berikutnya. Bisa dicoba dorong promo di H-1/H-2 akhir bulan untuk manfaatkan momentum ini.
>
> Ada 2 pesanan Pengembalian Dana dan 4 Batal yang sengaja tidak dihitung — kalau mau aku masukkan juga ke analisis (misal buat lihat produk mana yang sering diretur), tinggal bilang.

## Verifikasi angka & fakta (independen)

Dihitung ulang dengan Python (`csv` + `collections`, independen dari script skill):

| Hal | Hitung ulang | SEBELUM | SESUDAH |
|---|---|---|---|
| Omzet status Selesai | Rp 3.038.000 (66 baris) | ✅ | ✅ |
| Dibuang | 4 Batal (Rp 101.000) + 2 Pengembalian Dana (Rp 160.000) | ✅ disebut | ✅ disebut |
| Omzet per produk | Pashmina 30 pcs Rp 1.350.000 · Bergo 19 Rp 665.000 · Voal 9 Rp 531.000 · Ciput 21 Rp 252.000 · Inner 16 Rp 240.000 | ✅ (urut qty) | ✅ (urut omzet) |
| % kontribusi | 44,4% / 21,9% / 17,5% / 8,3% / 7,9% | — | ✅ |
| Rata-rata per hari | Rp 101.267 (30 hari) · Rp 108.500 (28 hari berjualan) | — | ✅ |
| Hari omzet tertinggi | 30 Sep Rp 285.000 (3 transaksi) | ✅ | ✅ |
| Hari order terbanyak | 1 & 5 Sep (5 transaksi); 5 Sep Rp 211.000 | ✅ | tidak dijawab |
| Hari terendah | 4, 14, 18 Sep (Rp 12.000) — Jumat, Senin, Jumat | — | ✅ ("bukan weekend" benar) |

Tidak ada kesalahan angka di kedua sisi. SESUDAH menyebut "30 Sep kemungkinan efek gajian" — dugaan, sudah diberi kata "kemungkinan".

## Nilai

| | SEBELUM | SESUDAH |
|---|---|---|
| Skor (1–10) | 7.5 | 8.5 |

- **SEBELUM 7,5/10** — model dasarnya sudah kuat di tugas ini: angka benar, otomatis membuang Batal/Refund, menjawab "hari paling rame" dari dua sisi (omzet & jumlah order). Kurang: tanpa persentase kontribusi, rata-rata harian, atau insight tindakan.
- **SESUDAH 8,5/10** — skill terpakai (`read` + `exec` script `rekap.py`). Format rekap konsisten, % kontribusi, rata-rata per hari kalender vs hari berjualan, 3 insight berbasis data (ketergantungan 44% pada 1 produk → jaga stok). Kurang: pertanyaan "hari paling rame" hanya dijawab dari sisi omzet, bukan jumlah pesanan.
- **Jujur:** selisih nilai di skenario ini kecil; beda utamanya kelengkapan & konsistensi format, bukan ketepatan.

Kriteria: ketepatan, langsung siap pakai, kepatuhan aturan Indonesia, keamanan/privasi, kejelasan untuk awam.
