# Uji 03 (normal) — Kafe fiktif, 21 hari, pemakaian stok bahan

> Data fiktif penguji: `examples/uji-kafe-21hari.csv` (9–29 Sep 2026). Kolom: transaksi,
> penjualan_rp (campur `Rp 5.500.000` dan `5,8jt`), stok_susu_liter + pakai_susu_liter, stok_kopi_gr
> (`8.992`) + pakai_kopi_gr, waste_porsi. Akhir pekan ramai (+60 transaksi). TARGET penjualan min
> `Rp 5.000.000`. Restok susu terakhir 26 Sep, kopi terakhir 26 Sep.

## Input pengguna
"Cek log kafe saya 3 minggu ini. Susu dikirim besok kalau pesan hari ini (1 hari), biji kopi 3 hari.
Stok cukup nggak? Nama: Kopi Senja."

## Perintah
```bash
python3 scripts/peringatan_dini.py examples/uji-kafe-21hari.csv --lead-time stok_susu_liter=1 --lead-time stok_kopi_gr=3 --format json
python3 scripts/peringatan_dini.py examples/uji-kafe-21hari.csv --lead-time stok_susu_liter=1 --lead-time stok_kopi_gr=3 --nama-usaha "Kopi Senja (fiktif)"
```
Cek JSON: arah transaksi/penjualan `turun`, waste `naik`; dua pasangan stok terdeteksi otomatis;
`5,8jt` dan `Rp 5.500.000` terbaca benar (dicocokkan dengan angka asli generator).

## Output siap kirim
```
🚨 PERINGATAN DINI OPERASIONAL
Kopi Senja (fiktif) — Sel, 29 Sep 2026
Data 9 Sep–29 Sep (21 hari tercatat)
Ringkas: 1 🔴 · 1 🟠 · 0 🟡 · 3 normal

🔴 Stok kopi (gr): sisa 3.024 = ±0,9 hari pemakaian (rata-rata 3.229,71/hari) -> perkiraan habis Sel, 29 Sep; pemasok butuh 3 hari -- pesan HARI INI
🟠 Stok susu (liter): sisa 32 = ±1,7 hari pemakaian (rata-rata 18,14/hari) -> perkiraan habis Rab, 30 Sep; pemasok butuh 1 hari -- siapkan pesanan
✅ Normal: Transaksi, Penjualan (Rp), Waste (porsi)

❓ Cek hari ini (cari akar masalah, bukan cari kambing hitam):
Stok kopi (gr):
 • Kapan terakhir pesan ke pemasok, dan berapa hari biasanya barang datang?
 • Pemakaian naik karena produksi/reject naik, atau ada selisih (hilang/rusak)?
 • Ada pemasok cadangan bila pemasok utama telat?
5 kenapa: Kenapa Stok kopi (gr) memburuk? → karena … → kenapa itu terjadi? → … (ulang sampai ketemu hal yang bisa diperbaiki).
Kalau sudah ada kerugian/komplain pelanggan: susun laporan insiden (skill laporan-insiden-usaha).

Catatan: ini peringatan statistik (tanda untuk dicek), bukan kepastian masalah atau ramalan pasti.
```

## Tambahan analisis agent
Biji kopi paling mendesak: sisa 3.024 gr ≈ 0,9 hari, sedangkan pemasok butuh 3 hari — walau dipesan
hari ini, kemungkinan ada ±2 hari tanpa stok; pertimbangkan beli darurat dari pemasok lokal.
Susu cukup ±1,7 hari dengan pengiriman 1 hari: pesan paling lambat besok pagi. Penjualan dan
transaksi normal (akhir pekan memang lebih ramai).

## Verifikasi independen
| Angka | Verifikator | Script |
|---|---|---|
| Rata pakai kopi 7 hari | 22.608/7 = 3.229,714 | 3.229,71 |
| Sisa kopi | 3.024/3.229,714 = 0,936 → 0,9 ≤ lead 3 → 🔴 | 0,9; 🔴 |
| Rata pakai susu | 127/7 = 18,143 | 18,14 |
| Sisa susu | 32/18,143 = 1,76 → 1,7; > lead 1, ≤ 2 → 🟠 | 1,7; 🟠 |
| Penjualan (garis dasar 20 angka) | rata 6.070.000, sd 871.236, z −0,31; Selasa 5.550.000 (+4,5%) | sama; ✅ |
**56 angka dibandingkan, 0 beda.**

## Temuan
- **Tanggal habis kopi ditulis "Sel, 29 Sep" = hari laporan itu sendiri**, padahal stok akhir hari
  masih 3.024 gr (habis di tengah hari Rabu 30 Sep). Rumus `tanggal + floor(sisa_hari)` = hari
  terakhir yang tertutup penuh; untuk sisa < 1 hari kalimat "perkiraan habis hari ini" membingungkan.
- Sisa 0,9 hari dengan lead 3 hari → pesan "pesan HARI INI" tidak menyebut bahwa pesanan hari ini
  pun **sudah terlambat** ±2 hari (agent menambahkannya, script tidak).

---

## Uji ulang v1.0.1 (2026-09-29, penguji independen)
Output siap kirim v1.0.1:
```
🚨 PERINGATAN DINI OPERASIONAL
Kopi Senja (fiktif) — Sel, 29 Sep 2026
Data 9 Sep–29 Sep (21 hari tercatat)
Ringkas: 1 🔴 · 1 🟠 · 0 🟡 · 3 normal

🔴 Stok kopi (gr): sisa 3.024 = ±0,9 hari pemakaian (rata-rata 3.229,71/hari) -> TIDAK cukup untuk besok -> habis besok (Rab, 30 Sep); pemasok butuh 3 hari -- pesan HARI INI; walau dipesan hari ini (datang ±Jum, 2 Okt), kemungkinan kosong ±2,1 hari
🟠 Stok susu (liter): sisa 32 = ±1,7 hari pemakaian (rata-rata 18,14/hari) -> cukup sampai Rab, 30 Sep, mulai kurang Kam, 1 Okt; pemasok butuh 1 hari -- siapkan pesanan
✅ Normal: Transaksi, Penjualan (Rp), Waste (porsi)

❓ Cek hari ini (cari akar masalah, bukan cari kambing hitam):
Stok kopi (gr):
 • Kapan terakhir pesan ke pemasok, dan berapa hari biasanya barang datang?
 • Pemakaian naik karena produksi/reject naik, atau ada selisih (hilang/rusak)?
 • Ada pemasok cadangan bila pemasok utama telat?
5 kenapa: Kenapa Stok kopi (gr) memburuk? → karena … → kenapa itu terjadi? → … (ulang sampai ketemu hal yang bisa diperbaiki).
Kalau sudah ada kerugian/komplain pelanggan: susun laporan insiden (skill laporan-insiden-usaha).

Catatan: ini peringatan statistik (tanda untuk dicek), bukan kepastian masalah atau ramalan pasti.
```
Temuan tanggal habis stok **teratasi**: kopi 0,9 hari → "TIDAK cukup untuk besok -> habis besok (Rab,
30 Sep) ... walau dipesan hari ini (datang ±Jum, 2 Okt), kemungkinan kosong ±2,1 hari" (3 − 0,936 =
2,06 → 2,1 ✓). Susu 1,76 hari → "cukup sampai Rab 30 Sep, mulai kurang Kam 1 Okt" ✓.
Verifikasi `verif2.py`: **38 angka/level, 0 beda.**
