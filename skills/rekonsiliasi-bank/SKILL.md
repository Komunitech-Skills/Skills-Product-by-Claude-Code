---
name: rekonsiliasi-bank
description: Mencocokkan mutasi rekening (CSV ekspor internet banking BCA, Mandiri, BRI, BNI, atau bank lain) dengan catatan penjualan/invoice UMKM — cocok persis (nominal + tanggal ± toleransi hari), cocok parsial (beda tanggal, terpotong biaya transfer, satu transfer untuk beberapa invoice, invoice dicicil), tidak ada di bank, tidak ada di catatan — plus penjelasan selisih yang seimbang. Gunakan saat pengguna minta rekonsiliasi bank, cocokkan mutasi/rekening koran dengan penjualan, cek transfer pelanggan sudah masuk, bank reconciliation. Bukan untuk rekap omzet atau laba rugi.
---

# Rekonsiliasi Bank vs Catatan Penjualan

## Tujuan
Menjawab: **"Transfer mana yang sudah masuk, mana yang belum, dan kenapa saldo bank tidak sama dengan catatan saya?"** Hasilnya laporan 4 kelompok + penjelasan selisih yang angkanya seimbang, dan (opsional) CSV untuk Excel.

## Kapan digunakan
- "Tolong cocokkan mutasi BCA bulan ini dengan daftar invoice saya."
- "Pelanggan bilang sudah transfer, kok di catatan belum lunas?"
- Tutup buku bulanan: memastikan penjualan transfer benar-benar masuk rekening.
- Mencocokkan pembayaran ke supplier (uang keluar) dengan catatan pembelian → `--arah keluar`.

## Kapan TIDAK digunakan
- Rekap omzet/produk terlaris → `rekap-penjualan-csv`. Laporan laba rugi/neraca → `laporan-keuangan-emkm`.
- Menagih pelanggan yang belum bayar → `tagih-piutang` (tawarkan setelah laporan).
- File hanya PDF/foto mutasi → minta unduh ulang dalam CSV/Excel dari internet banking, atau salin tabelnya ke spreadsheet dan simpan sebagai CSV. Jangan mengetik ulang ratusan baris secara manual tanpa memberi tahu risikonya.
- Mutasi rekening orang lain yang tidak berhak diakses pengguna → tolak dengan sopan.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| File mutasi rekening (CSV; Excel disimpan sebagai CSV) | Ya | — (minta) |
| File catatan penjualan/invoice (CSV/tabel tempel): tanggal & nominal | Ya | — (minta) |
| Kolom no. invoice & nama pelanggan di catatan | Tidak | Tanpa (pencocokan hanya nominal+tanggal, lebih lemah) |
| Toleransi hari cocok persis | Tidak | 3 hari |
| Jendela hari cocok parsial | Tidak | 14 hari |
| Toleransi beda nominal (biaya transfer/admin) | Tidak | Rp 10.000 atau 1% (mana yang lebih besar), dilaporkan sebagai PARSIAL |
| Arah | Tidak | Uang masuk vs penjualan |

Jika catatan berupa tabel tempel di chat, simpan dulu sebagai CSV di folder kerja pengguna. Jika info kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor).

## Langkah kerja
1. **Ingatkan privasi (1 kalimat)** sebelum mulai: data rekening hanya dibaca di komputer ini; jangan tempel nomor rekening/PIN/OTP; hapus data sensitif sebelum membagikan hasil.
2. **Deteksi kolom** (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/rekonsiliasi.py deteksi --bank mutasi.csv --catatan penjualan.csv
   ```
   Script menebak baris judul (melewati baris info rekening di atas tabel), kolom tanggal/keterangan/nominal, kolom penanda CR/DB, dan format bank (tebakan).
3. **Konfirmasi ke pengguna** dalam satu pesan singkat, contoh:
   > Saya membaca mutasi (mirip format BCA): tanggal = "Tanggal Transaksi", keterangan = "Keterangan", nominal = "Jumlah", penanda masuk/keluar = kolom ke-5 (CR/DB). Catatan: tanggal = "Tanggal", nominal = "Total", invoice = "No Invoice", pelanggan = "Pelanggan". Sudah benar?

   Jika pengguna ingin cepat, lanjutkan dengan tebakan dan sebutkan sebagai asumsi. Detail format per bank: `references/format-bank.md`.
4. **Cocokkan**:
   ```bash
   python3 <folder-skill-ini>/scripts/rekonsiliasi.py cocokkan --bank mutasi.csv --catatan penjualan.csv \
     --bank-tanggal "Tanggal Transaksi" --bank-keterangan "Keterangan" --bank-nominal "Jumlah" --bank-dk kolom_5 \
     --catat-tanggal "Tanggal" --catat-nominal "Total" --catat-ref "No Invoice" --catat-nama "Pelanggan" \
     --catat-status "Status" --catat-metode "Metode" --output-csv hasil-rekonsiliasi.csv
   ```
   - Bank dengan kolom debet & kredit terpisah: `--bank-kredit "Kredit" --bank-debet "Debet"` (ganti `--bank-nominal/--bank-dk`).
   - Nominal tunggal tanpa CR/DB, uang keluar bertanda minus: `--bank-tanpa-penanda negatif-keluar`.
   - Tanggal bank tanpa tahun (mis. `'02/09`): tahun diambil dari baris "Periode" di atas file; bila tidak ada, tambah `--tahun 2026`.
   - `--catat-metode` + default `--abaikan-metode tunai,cash` membuang penjualan tunai (tidak lewat bank). `--catat-status` membuang batal/refund.
   - Atur toleransi: `--toleransi-hari 3 --maks-hari-parsial 14 --toleransi-selisih 10000 --toleransi-persen 1`. Periode: `--dari 2026-09-01 --sampai 2026-09-30`.
   - `--format teks` untuk ringkasan cepat; default JSON.
5. **Tulis laporan** (format di bawah). Semua angka dari output script. Pastikan `cek_rumus_seimbang` = true; jika false, laporkan sebagai kesalahan dan jangan menyimpulkan.
6. **Beri tindak lanjut konkret** per kelompok (lihat bagian Format). Tawarkan `tagih-piutang` untuk invoice yang belum dibayar.
7. Tutup dengan pengingat privasi & hapus file hasil bila sudah tidak diperlukan.

**Fallback tanpa Python** (beri tahu pengguna bahwa hasil dicocokkan manual dan bisa terlewat): urutkan kedua daftar per tanggal; untuk tiap catatan cari transaksi bank uang masuk dengan nominal sama dan tanggal ±3 hari → COCOK; sisanya cek nominal sama beda tanggal ≤14 hari, beda nominal ≤ Rp 10.000/1%, atau jumlah 2–3 transaksi yang sama dengan satu nominal → PARSIAL; sisanya masuk "tidak ada di bank"/"tidak ada di catatan". Selisih = total catatan − total bank = (tidak ada di bank) − (tidak ada di catatan) + (selisih parsial).

## Format output
```
## Rekonsiliasi <nama bank, bila diketahui> — <periode>
Total catatan: Rp … · Total uang masuk bank: Rp … · Selisih: Rp …

| Kelompok | Jumlah | Nilai catatan | Nilai bank |
|---|---:|---:|---:|
| ✅ Cocok | … | Rp … | Rp … |
| 🟡 Cocok parsial (perlu dicek) | … | Rp … | Rp … |
| ❌ Ada di catatan, tidak ada di bank | … | Rp … | — |
| ❓ Ada di bank, tidak ada di catatan | … | — | Rp … |

### Penjelasan selisih Rp …
+ Rp … invoice belum terlihat masuk bank
− Rp … uang masuk yang belum dicatat
+ Rp … beda nominal pada cocok parsial
= Rp … (seimbang ✔)

### ❌ Belum ada di bank → tindakan
| Tgl | Invoice | Pelanggan | Nominal | Saran |
### ❓ Belum ada di catatan → tindakan
| Tgl | Keterangan (disamarkan) | Nominal | Kemungkinan |
### 🟡 Cocok parsial → cek satu per satu
| Catatan | Bank | Selisih | Alasan |

Catatan: nomor rekening di keterangan disamarkan. Hapus file mutasi & hasil dari folder bersama setelah selesai.
```
Saran per kelompok: belum ada di bank → cek bukti transfer / tagih (`tagih-piutang`) / cek rekening lain; belum ada di catatan → tanyakan asal dana, catat bila penjualan, pisahkan dana pribadi; bunga/biaya bank → catat sebagai pendapatan/biaya bank; parsial beda nominal → catat biaya transfer atau tagih kekurangan.

## Contoh
**Input pengguna:** "Ini mutasi BCA September (mutasi.csv) dan daftar invoice saya (penjualan.csv). Tolong cocokkan."

**Output (ringkas):**
```
Total catatan Rp 25.700.000 · Uang masuk bank Rp 20.454.846 · Selisih Rp 5.245.154
✅ Cocok 3 · 🟡 Parsial 4 · ❌ Belum di bank 1 (Rp 1.250.000) · ❓ Belum di catatan 2 (Rp 1.011.346)
Penjelasan: + Rp 1.250.000 (INV-0010 Joko belum masuk) − Rp 1.011.346 (Hendra Rp 999.000 & bunga Rp 12.346)
            + Rp 5.006.500 (PT Sinar baru bayar Rp 5.000.000 dari Rp 10.000.000; CV Maju kurang Rp 6.500 — biaya transfer?)
            = Rp 5.245.154 ✔
Parsial lain: Andi Wijaya bayar INV-0006 + INV-0007 sekaligus Rp 3.000.000; Rina bayar INV-0008 dua kali @ Rp 1.000.000.
```

## Checklist sebelum mengirim hasil
- [ ] Pemetaan kolom sudah dikonfirmasi (atau disebut sebagai asumsi).
- [ ] Semua angka dari script; `cek_rumus_seimbang` = true.
- [ ] Setiap PARSIAL diberi label "perlu dicek" — bukan dianggap pasti benar.
- [ ] Baris yang dilewati (PEND, baris saldo, tanggal tak terbaca), catatan tunai/batal yang dibuang, dan semua `peringatan` disampaikan.
- [ ] Tidak menampilkan nomor rekening/kartu lengkap; tidak menyarankan mengirim file mutasi ke pihak lain.
- [ ] Pengingat hapus data sensitif ada di akhir.

## Batasan & penanganan error
- Format ekspor bank bisa berubah sewaktu-waktu; itu sebabnya kolom selalu dikonfirmasi. Tebakan "mirip BCA/BRI/…" hanya petunjuk.
- Pencocokan otomatis bisa keliru bila banyak transaksi bernominal sama; tambahkan kolom invoice/nama pelanggan untuk akurasi lebih baik.
- Settlement marketplace/QRIS/EDC biasanya dibayar gabungan dan sudah dipotong biaya → sering muncul sebagai PARSIAL/tidak cocok; sarankan mencocokkan dengan laporan penarikan dana (payout) marketplace, bukan per pesanan.
- Script keluar dengan kode ≠ 0 dan pesan JSON bila file Excel/PDF, kolom tidak ada, tanggal tanpa tahun, atau tidak ada baris valid — sampaikan dengan bahasa sederhana beserta cara memperbaikinya.
- Privasi: script tidak mengakses internet, tidak menyimpan apa pun selain `--output-csv` yang diminta, dan menyamarkan deret angka ≥ 8 digit (`--tampilkan-lengkap` hanya bila pengguna memintanya). Jangan pernah meminta PIN, password, OTP, atau token internet banking.
- Bukan audit; untuk sengketa dengan bank atau pelanggan, gunakan rekening koran resmi dari bank.
