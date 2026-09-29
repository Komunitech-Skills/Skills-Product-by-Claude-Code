# Uji 04 (input tidak lengkap) — hanya 5 hari data

> Data fiktif: `examples/uji-bengkel-5hari.csv` (25–29 Sep 2026): output_pcs 820/840/805/830/810,
> reject_pcs 12/14/17/19/24, TARGET reject maks 20.

## Input pengguna
"Saya baru mulai nyatat 5 hari. Reject kok kayaknya naik ya? Bengkel Las Sinar."

## Perilaku agent (mengikuti SKILL.md)
Data < 7 hari tetap dijalankan (tidak menolak), `data_sedikit: true` → keterbatasan ditegaskan.
```bash
python3 scripts/peringatan_dini.py examples/uji-bengkel-5hari.csv --nama-usaha "Bengkel Las Sinar (fiktif)"
```
```
🚨 PERINGATAN DINI OPERASIONAL
Bengkel Las Sinar (fiktif) — Sel, 29 Sep 2026
Data 25 Sep–29 Sep (5 hari tercatat)
Ringkas: 0 🔴 · 1 🟠 · 1 🟡 · 1 normal
⚠️ Data baru 5 hari: batas kendali (σ) butuh ≥15 hari, tren ≥5 hari, banding hari yang sama ≥15 hari. Peringatan di bawah masih terbatas.

🟠 Reject (pcs): 24 hari ini (kemarin 19)
   melewati target maks 20 (+20%); naik 4 hari berturut-turut.
🟡 % reject: 2,96 hari ini (kemarin 2,29)
   naik 4 hari berturut-turut.
✅ Normal: Output (pcs)

❓ Cek hari ini (cari akar masalah, bukan cari kambing hitam):
Reject (pcs):
 • Material: ada bahan baku batch/pemasok baru, atau bahan disimpan terlalu lama?
 • Mesin: suhu/setting mesin (oven, mixer, sealer) berubah, baru diservis, atau sempat rusak?
 • Manusia & metode: operator baru/ganti shift? resep, SOP, atau ukuran batch berubah?
5 kenapa: Kenapa Reject (pcs) naik? → karena … → kenapa itu terjadi? → … (ulang sampai ketemu hal yang bisa diperbaiki).
Kalau sudah ada kerugian/komplain pelanggan: susun laporan insiden (skill laporan-insiden-usaha).

Catatan: ini peringatan statistik (tanda untuk dicek), bukan kepastian masalah atau ramalan pasti.
```

## Tambahan agent
"Datanya baru 5 hari, jadi yang bisa dicek baru target dan naik-turun beruntun. Reject memang naik
4 hari berturut-turut (12 → 24) dan hari ini lewat target maks 20. Batas kendali (σ) baru bisa
dihitung setelah ±15 hari dan banding hari yang sama setelah 2 minggu — tetap isi lognya tiap hari,
hasilnya makin tajam. Mau saya kirimi template log kosong?"

## Verifikasi
Reject: 4 kenaikan beruntun → 🟡 aturan beruntun; (24−20)/20 = +20% ≥ 10% → 🟠 target → level 🟠 ✓.
% reject 2,96 (24/810×100) naik 4 hari → 🟡 ✓. σ, hari-sama tidak dijalankan ✓ (JSON `butuh_data`).
Tren 5 titik dihitung (slope 2,9/hari, R² 0,969) tapi proyeksi tidak dipakai karena sudah lewat
target ✓. **27 angka dibandingkan, 0 beda.**

## Penilaian
Lulus. Laporan jujur soal keterbatasan, tidak mengarang σ. Minor: baris ⚠️ menyebut "tren ≥5 hari"
padahal tren sudah jalan dengan 5 hari (daftar syarat generik, bisa membingungkan).

## Data rusak tambahan (dijalankan penguji; ringkasan, detail di HASIL-UJI.md)
File kosong / hanya judul / kolom salah → `GALAT` kode 2 dengan pesan jelas ✓. Log hari ini belum
diisi → `⬜ LOG HARIAN BELUM DIISI` (tidak dibilang aman) ✓. Tanggal `31/02/2026` / `kemarin` →
baris dilewati & dilaporkan ✓.
