# Contoh pembuat skill: pabrik roti fiktif, log 30 hari (v1.0.1)

> Contoh dari pembuat skill (bukan hasil uji independen). Usaha, angka, dan catatan **fiktif**.
> File log: `examples/log-roti-30hari.csv` (31 Agu – 29 Sep 2026, Minggu 13 Sep libur, baris
> `TARGET` berisi output min 2.000, reject maks 50, penjualan min Rp 9.000.000, keluhan maks 2,
> telat kirim maks 1, absen maks 2). Angka sengaja ditulis campur: `2.081`, `2,1rb`,
> `Rp 9.252.000`, `9,1jt`. Tanggal 7 Sep ada kejadian listrik padam (reject 95).

## Input pengguna
"Ini log harian pabrik roti saya 30 hari terakhir. Ada yang perlu saya waspadai? Pemasok tepung
biasanya kirim 2 hari setelah dipesan. Nama usaha: Roti Bu Ratna."

## Perintah
```bash
python3 scripts/peringatan_dini.py examples/log-roti-30hari.csv --nama-usaha "Roti Bu Ratna (fiktif)"
python3 scripts/peringatan_dini.py examples/log-roti-30hari.csv --format json   # untuk cek arah & kualitas data
```
Arah hasil tebakan (dari JSON): output/penjualan = `turun` (makin kecil makin buruk); reject,
keluhan, telat kirim, absen = `naik`; `stok_tepung_kg` + `pakai_tepung_kg` = pasangan stok;
metrik turunan `% reject` ditambahkan otomatis. Tidak ada yang perlu dikoreksi.

## Output siap kirim (Telegram)
```
🚨 PERINGATAN DINI OPERASIONAL
Roti Bu Ratna (fiktif) — Sel, 29 Sep 2026
Data 31 Agu–29 Sep (29 hari tercatat)
Ringkas: 2 🔴 · 1 🟠 · 1 🟡 · 4 normal

🔴 % reject: 3,08 hari ini (kemarin 2,25)
   7,0σ di atas rata-rata 27 hari sebelumnya (1,47) -- lewat batas bahaya 3σ (2 dari 3 hari terakhir); naik 3 hari berturut-turut.
🔴 Reject (pcs): 63 hari ini (kemarin 46)
   6,8σ di atas rata-rata 27 hari sebelumnya (31,15) -- lewat batas bahaya 3σ (2 dari 3 hari terakhir); melewati target maks 50 (+26%); naik 3 hari berturut-turut.
🟠 Stok tepung (kg): sisa 169 = ±3,2 hari pemakaian (rata-rata 52,29/hari) -> cukup sampai Jum, 2 Okt, mulai kurang Sab, 3 Okt; pemasok butuh 2 hari -- siapkan pesanan
🟡 Penjualan (Rp): Rp 8.644.500 hari ini (kemarin Rp 8.730.000)
   turun 3 hari berturut-turut; di bawah target min Rp 9.000.000 (-4%); 2 dari 7 hari terakhir di bawah target.
✅ Normal: Output (pcs), Keluhan, Telat kirim, Absen

❓ Cek hari ini (cari akar masalah, bukan cari kambing hitam):
% reject:
 • Material: ada bahan baku batch/pemasok baru, atau bahan disimpan terlalu lama?
 • Mesin: suhu/setting mesin (oven, mixer, sealer) berubah, baru diservis, atau sempat rusak?
 • Manusia & metode: operator baru/ganti shift? resep, SOP, atau ukuran batch berubah?
Stok tepung (kg):
 • Kapan terakhir pesan ke pemasok, dan berapa hari biasanya barang datang?
 • Pemakaian naik karena produksi/reject naik, atau ada selisih (hilang/rusak)?
 • Ada pemasok cadangan bila pemasok utama telat?
5 kenapa: Kenapa % reject naik? → karena … → kenapa itu terjadi? → … (ulang sampai ketemu hal yang bisa diperbaiki).
Kalau sudah ada kerugian/komplain pelanggan: susun laporan insiden (skill laporan-insiden-usaha).

ℹ️ Data: 1 hari kosong (Min, 13 Sep) tidak diisi tebakan; 2 angka ekstrem lama tidak dipakai di rata-rata.
Catatan: ini peringatan statistik (tanda untuk dicek), bukan kepastian masalah atau ramalan pasti.
```

## Tambahan analisis agent (di luar pesan siap kirim)
Reject naik 3 hari berturut-turut sejak 27 Sep dan melonjak 29 Sep; di kolom catatan (dibaca agent
dari JSON `catatan_hari_ini`, **tidak** dikutip di pesan Telegram kecuali `--sertakan-catatan`) ada "mulai pakai tepung merk
baru dari pemasok baru" (28 Sep) dan "oven 2 suhu tidak stabil siang" (29 Sep). Keduanya layak
dicek lebih dulu — kenaikan sudah dimulai 27 Sep, sehari sebelum tepung baru dipakai, jadi belum tentu satu
penyebab. Tepung sebaiknya dipesan hari ini atau paling lambat besok pagi: sisa ±3,2 hari, pemasok butuh 2 hari.
Mau saya bantu isi 5 kenapa untuk reject, atau jadwalkan laporan ini tiap malam jam 20.00 ke
Telegram?

## Verifikasi angka manual (independen dari script, `statistics` Python)
| Angka | Hitungan manual | Script |
|---|---|---|
| Garis dasar reject | 27 angka 31 Agu–28 Sep **tanpa** 7 Sep (95, pencilan): rata 31,148; sd sampel 4,688 | rata 31,15; σ 4,688 |
| z reject hari ini | (63 − 31,148) / 4,688 = 6,79 (≥ 4σ → 🔴 walau satu hari) | 6,8σ 🔴 |
| Rata-rata Selasa 4 minggu | 22 Sep 35, 15 Sep 26, 8 Sep 33, 1 Sep 25 → 119/4 = 29,75; 63 vs 29,75 = +112% | 29,75; 112% |
| Target reject | (63 − 50) / 50 = +26% | +26% |
| Pemakaian tepung 7 hari | 51+52+56+57+50+50+50 = 366 / 7 = 52,286 | 52,29 |
| Sisa hari stok | 169 / 52,286 = 3,23 → ditampilkan 3,2 (ke bawah); 3 hari penuh → cukup sampai Jum 2 Okt, mulai kurang Sab 3 Okt | 3,2; Jum 2 Okt / Sab 3 Okt |
| Level stok | 3,2 ≤ 2 × lead time (4) dan > 2 → 🟠 | 🟠 |
