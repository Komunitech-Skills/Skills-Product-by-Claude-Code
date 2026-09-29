# Uji 02 (normal) — Distributor fiktif, 30 hari, telat kirim naik pelan

> Data fiktif penguji: `examples/uji-distributor-30hari.csv` (31 Agu – 29 Sep 2026). Kolom:
> pengiriman, telat_kirim, retur, keluhan, catatan. Telat kirim stabil 4–9 lalu naik ±2/hari
> sejak 20 Sep (catatan 20 Sep: "2 armada masuk bengkel; ganti ke ekspedisi pihak ketiga").
> TARGET: telat_kirim maks 15, keluhan maks 3.

## Input pengguna
"Tolong cek log pengiriman 30 hari ini, ada masalah yang mulai muncul? Nama usaha CV Lancar Kirim."

## Perintah
```bash
python3 scripts/peringatan_dini.py examples/uji-distributor-30hari.csv --format json
python3 scripts/peringatan_dini.py examples/uji-distributor-30hari.csv --nama-usaha "CV Lancar Kirim (fiktif)"
```
Cek JSON: `pengiriman` ditebak `dua` → agent sebaiknya bertanya/menjalankan ulang dengan
`--arah pengiriman=turun` (hasil sama pada data ini, pengiriman normal).

## Output siap kirim (29 Sep)
```
🚨 PERINGATAN DINI OPERASIONAL
CV Lancar Kirim (fiktif) — Sel, 29 Sep 2026
Data 31 Agu–29 Sep (30 hari tercatat)
Ringkas: 1 🔴 · 0 🟠 · 0 🟡 · 3 normal

🔴 Telat kirim: 23 hari ini (kemarin 23)
   melewati target maks 15 (+53%); 5 dari 7 hari terakhir tidak capai target; 2,7σ di atas rata-rata 28 hari sebelumnya (9,04) -- lewat batas waspada 2σ; 7 hari tercatat berturut-turut di atas rata-rata -- pola bergeser, bukan kebetulan sehari.
✅ Normal: Pengiriman, Retur, Keluhan

❓ Cek hari ini (cari akar masalah, bukan cari kambing hitam):
Telat kirim:
 • Kurir/armada: ada kendaraan rusak, kurir kurang, atau ganti ekspedisi?
 • Pesanan menumpuk di jam tertentu? Jam potong (cut-off) masih dipatuhi?
 • Barang siap tepat waktu dari produksi/gudang, atau sudah telat sejak packing?
5 kenapa: Kenapa Telat kirim naik? → karena … → kenapa itu terjadi? → … (ulang sampai ketemu hal yang bisa diperbaiki).
Kalau sudah ada kerugian/komplain pelanggan: susun laporan insiden (skill laporan-insiden-usaha).

Catatan: ini peringatan statistik (tanda untuk dicek), bukan kepastian masalah atau ramalan pasti.
```

## Uji "dini": laporan bila dijalankan tanggal 22 Sep (angka telat baru 9, masih jauh di bawah target 15)
```
🚨 PERINGATAN DINI OPERASIONAL
CV Lancar Kirim (fiktif) — Sel, 22 Sep 2026
Data 31 Agu–22 Sep (23 hari tercatat)
Ringkas: 0 🔴 · 1 🟠 · 0 🟡 · 3 normal

🟠 Telat kirim: 9 hari ini (kemarin 8)
   42% di atas rata-rata hari Selasa 3 minggu terakhir (6,33); naik 3 hari berturut-turut.
✅ Normal: Pengiriman, Retur, Keluhan

❓ Cek hari ini (cari akar masalah, bukan cari kambing hitam):
Telat kirim:
 • Kurir/armada: ada kendaraan rusak, kurir kurang, atau ganti ekspedisi?
 • Pesanan menumpuk di jam tertentu? Jam potong (cut-off) masih dipatuhi?
 • Barang siap tepat waktu dari produksi/gudang, atau sudah telat sejak packing?
5 kenapa: Kenapa Telat kirim naik? → karena … → kenapa itu terjadi? → … (ulang sampai ketemu hal yang bisa diperbaiki).
Kalau sudah ada kerugian/komplain pelanggan: susun laporan insiden (skill laporan-insiden-usaha).

Catatan: ini peringatan statistik (tanda untuk dicek), bukan kepastian masalah atau ramalan pasti.
```
Deret level telat kirim per tanggal (`--tanggal`): 19–21 Sep ✅ · **22 Sep 🟠** · 23 Sep 🔴 (3,4σ +
proyeksi ±2 hari lewat target) · 24 Sep 🟠 · 25–29 Sep 🔴 (lewat target 15 mulai 25 Sep).
Peringatan muncul **3 hari sebelum** target dilanggar.

## Tambahan analisis agent
Telat kirim naik sejak Senin 21 Sep, sehari setelah catatan "2 armada masuk bengkel; ganti ke
ekspedisi pihak ketiga" (20 Sep) — layak dicek lebih dulu, tapi belum tentu penyebab tunggal.
Keluhan belum naik; kalau pelanggan mulai komplain, susun laporan insiden.

## Verifikasi independen
telat_kirim: garis dasar 28 angka rata 9,04 sd 5,103 → z 2,74 (script 2,7σ); 7 hari berturut di
atas rata-rata (script sama); Selasa 4 minggu rata 7,00 → +228,6%; tren 1,929/hari R² 0,952; target
5 dari 7 hari lewat → 🔴. **64 angka dibandingkan, 0 beda.**

## Catatan penguji
- Pada 29 Sep z turun jadi 2,7σ (dari 3,4σ di 28 Sep) karena hari-hari yang sudah naik ikut masuk
  garis dasar 28 hari — keterbatasan wajar, tetap 🔴 lewat target & aturan "pola bergeser".
- Alasan ke-4/ke-5 (mis. "229% di atas rata-rata Selasa") terpotong karena laporan hanya
  menampilkan 3 alasan — sesuai desain.

---

## Uji ulang v1.0.1 (2026-09-29, penguji independen)
Output siap kirim v1.0.1 (29 Sep):
```
🚨 PERINGATAN DINI OPERASIONAL
CV Lancar Kirim (fiktif) — Sel, 29 Sep 2026
Data 31 Agu–29 Sep (30 hari tercatat)
Ringkas: 1 🔴 · 0 🟠 · 0 🟡 · 3 normal

🔴 Telat kirim: 23 hari ini (kemarin 23)
   melewati target maks 15 (+53%); 5 dari 7 hari terakhir melewati target; biasanya ±9/hari (28 hari sebelumnya), hari ini 23 -- peluang kebetulan ±1 dari 320 hari (2 dari 3 hari terakhir); 7 hari tercatat berturut-turut di atas rata-rata -- pola bergeser, bukan kebetulan sehari.
✅ Normal: Pengiriman, Retur, Keluhan

❓ Cek hari ini (cari akar masalah, bukan cari kambing hitam):
Telat kirim:
 • Kurir/armada: ada kendaraan rusak, kurir kurang, atau ganti ekspedisi?
 • Pesanan menumpuk di jam tertentu? Jam potong (cut-off) masih dipatuhi?
 • Barang siap tepat waktu dari produksi/gudang, atau sudah telat sejak packing?
5 kenapa: Kenapa Telat kirim naik? → karena … → kenapa itu terjadi? → … (ulang sampai ketemu hal yang bisa diperbaiki).
Kalau sudah ada kerugian/komplain pelanggan: susun laporan insiden (skill laporan-insiden-usaha).

Catatan: ini peringatan statistik (tanda untuk dicek), bukan kepastian masalah atau ramalan pasti.
```
Bila dijalankan 22 Sep:
```
🚨 PERINGATAN DINI OPERASIONAL
CV Lancar Kirim (fiktif) — Sel, 22 Sep 2026
Data 31 Agu–22 Sep (23 hari tercatat)
Ringkas: 0 🔴 · 0 🟠 · 1 🟡 · 3 normal

🟡 Telat kirim: 9 hari ini (kemarin 8)
   naik 3 hari berturut-turut.
✅ Normal: Pengiriman, Retur, Keluhan

❓ Cek hari ini (cari akar masalah, bukan cari kambing hitam):
Telat kirim:
 • Kurir/armada: ada kendaraan rusak, kurir kurang, atau ganti ekspedisi?
 • Pesanan menumpuk di jam tertentu? Jam potong (cut-off) masih dipatuhi?
 • Barang siap tepat waktu dari produksi/gudang, atau sudah telat sejak packing?
5 kenapa: Kenapa Telat kirim naik? → karena … → kenapa itu terjadi? → … (ulang sampai ketemu hal yang bisa diperbaiki).
Kalau sudah ada kerugian/komplain pelanggan: susun laporan insiden (skill laporan-insiden-usaha).

Catatan: ini peringatan statistik (tanda untuk dicek), bukan kepastian masalah atau ramalan pasti.
```
`telat_kirim` kini model **hitungan** (λ < 20, angka bulat). `pengiriman` kini ditebak `turun` ✓.
Deret level: 21 Sep ✅ · **22 Sep 🟡** (naik 3 hari) · 23 Sep 🟡 (p 0,019, +117% vs Rabu, proyeksi ±2
hari lewat target) · 24 Sep 🟡 · 25 Sep 🟠 (lewat target) · 26–29 Sep 🔴.
Catatan penguji: 🟡 tetap muncul 3 hari sebelum target dilanggar, tetapi 🟠 baru muncul **bersamaan**
dengan pelanggaran target (v1.0.0: 🟠 pada 22 Sep). Pada 24 Sep angka 13 (≈2× biasanya) dua hari
berturut-turut hanya 🟡 karena angka 13 kemarin sudah masuk garis dasar (p hari ini 0,0249, tipis di
atas P2 0,02275) sehingga aturan "2 dari 3 hari" tidak terpenuhi. Trade-off yang disengaja (alarm palsu
turun drastis); dicatat RENDAH di HASIL-UJI.
Verifikasi `verif2.py`: **36 angka/level, 0 beda.**
