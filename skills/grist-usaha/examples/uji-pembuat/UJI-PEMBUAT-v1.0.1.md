# Catatan pembuat — grist-usaha v1.0.0 → v1.0.1 (revisi atas temuan Akun B)

Catatan AGENT PEMBUAT (bukan penguji independen), menindaklanjuti `examples/HASIL-UJI.md` dan
`examples/03-rekap-operasional-csv.md`. Kedua file tester tersebut TIDAK diubah.

## Temuan #1 (TINGGI) — overclaim "Rp 1,25jt" — DIPERBAIKI
Dikonfirmasi ulang: `_bersihkan_angka("Rp 1,25jt")` v1.0.0 memang mengembalikan `None`. Sesuai
instruksi kerja, dipilih opsi **(a) tambah dukungan parsing singkatan** (bukan menghapus klaim di
README), karena klaimnya sesuai kebutuhan nyata UMKM dan lebih bernilai untuk dipenuhi.

Implementasi (lihat `references/singkatan-besaran.md` untuk rincian & alasan lengkap):
- `_bersihkan_angka` sekarang memakai `Decimal` (bukan float) untuk perkalian singkatan, dan
  mengembalikan **tuple** `(nilai, alasan)` — bukan skalar tunggal seperti v1.0.0. Ini perubahan
  signature yang disengaja supaya kasus "sudah mirip angka+singkatan tapi ambigu/tidak valid" bisa
  dibedakan dari "memang bukan angka sama sekali" (dipakai untuk temuan #2 di bawah). Semua
  pemanggil di `scripts/grist.py` (2 titik di `cmd_bersihkan_csv`) dan di
  `tests/uji_regresi.py` (helper `cek()`) sudah disesuaikan.
- Sufiks didukung: `ribu`/`rb`/`k` (×1.000), `juta`/`jt` (×1.000.000), `miliar` (×1.000.000.000).
- **Keputusan ambiguitas `m`/`M`** (sesuai instruksi kerja untuk berhati-hati): huruf **besar**
  tunggal `M` diterima sebagai miliar (konvensi umum bisnis Indonesia); huruf **kecil** tunggal
  `m` **sengaja ditolak** (`None` + alasan eksplisit "ambigu, bisa disangka satuan lain seperti
  meter") karena `m` adalah simbol SI resmi untuk meter dan berisiko salah tebak. Kata penuh
  `miliar`/`Miliar` tetap diterima (tidak ambigu, case-insensitive). Rinciannya di
  `references/singkatan-besaran.md`.
- Koma & titik desimal ditangani benar sesuai keempat kasus di instruksi kerja: `1,25jt` =
  `1.25jt` = 1.250.000; `1.250.000` (tanpa singkatan, jalur lama tidak diubah) = 1.250.000;
  `1.5jt` = 1.500.000. Angka dengan koma DAN titik sekaligus sebelum singkatan (mis.
  `1.250,5jt`) ditolak sebagai ambigu, bukan ditebak.
- README/SKILL.md **tidak perlu diubah isinya** (klaim "Rp 1,25jt dirapikan otomatis" sekarang
  BENAR) — hanya ditambah rincian singkatan yang didukung + rujukan ke
  `references/singkatan-besaran.md` di SKILL.md bagian D.

## Temuan #2 (SEDANG) — kolom batal tanpa menyebut baris — DIPERBAIKI (opsi "nama baris" dipilih)
Instruksi kerja memberi 2 opsi: minta konfirmasi pengguna sebelum convert sisanya, ATAU
"keep existing behaviour but name the rows". Dipilih opsi **kedua** (lebih sederhana, tidak butuh
alur konfirmasi interaktif tambahan, tetap aman): perilaku all-or-nothing per kolom **dipertahankan
persis seperti v1.0.0**, tapi `cmd_bersihkan_csv` sekarang melacak, per kolom, sel mana yang gagal
(`kolom_gagal[i]`: nomor baris file + nilai asli + alasan bila ada) DAN apakah kolom itu pernah
punya sel yang berhasil jadi angka (`kolom_ada_sukses[i]`). Kolom yang batal Numeric PADAHAL
sebagian selnya sukses → tampilkan peringatan eksplisit (baris, nilai, s.d. 5 contoh + jumlah
sisanya) di layar DAN di `--json` (`kolom_gagal_sebagian`). Kolom yang memang teks murni (tidak
pernah ada sel sukses, mis. "Nama Barang") **tidak** dilaporkan sebagai "gagal" — itu bukan
kegagalan.

## Verifikasi terhadap fixture tester
Dijalankan ulang CSV persis di `examples/03-rekap-operasional-csv.md` (6 baris, termasuk baris
rusak "tiga puluh ribu"/"belum diisi"): kolom `HargaSatuan` & `TotalPenjualan` tetap Text (perilaku
lama dipertahankan, sesuai ekspektasi tester), TAPI sekarang peringatan menyebut "baris 6: 'tiga
puluh ribu'" dan "baris 6: 'belum diisi'" secara eksplisit — menjawab langsung rekomendasi tester
"sebutkan baris pertama yang gagal parse per kolom".

## Pengujian
- `tests/uji_regresi.py`: 50 → **66 test** (+16: 11 kasus singkatan besaran termasuk
  `Rp 1,25jt` PERSIS klaim README, ambiguitas `m` kecil, koma+titik ambigu, negatif, bukan-
  singkatan tetap `None`/`None`; + 3 test CLI `bersihkan-csv` untuk laporan baris gagal & kolom
  teks murni tidak salah dilaporkan & singkatan lewat CLI ujung-ke-ujung). Semua 66 lulus.
- `python3 scripts/validate.py --skill grist-usaha` ✅.
- `bash scripts/uji_openclaw.sh` ✅ eligible untuk grist-usaha.

## Belum diperbaiki / masih terbuka (di luar cakupan revisi ini, sesuai instruksi kerja)
- Temuan RENDAH #3 (kolom rumus tidak dibuat otomatis lewat REST API) — sudah didokumentasikan
  jujur, bukan bug, tidak diubah.
- Belum ada uji terhadap Grist sungguhan (Docker/Desktop) — masih tercatat sebagai keterbatasan
  di README.md, tidak berubah di v1.0.1.
- Status tetap `uji` (belum dinaikkan ke `lulus`) — menunggu penguji independen (Akun B) menguji
  ulang v1.0.1 sesuai Tahap 6 alur kerja.
