# Catatan pembuat — resi-picking v1.0.1 → v1.0.2 (tugas H1, Akun B)

Catatan AGENT PEMBUAT (bukan penguji independen). Tugas H1 di papan tugas internal kurator (tidak disertakan dalam paket) meminta
deteksi kolom per-kata (bukan substring), sinonim per marketplace dengan sumber dicatat, pesan saran
`--kolom-...` yang jelas saat kolom ambigu/tidak ditemukan, dan tes fixture per marketplace.

## Temuan saat mulai kerja
Sebagian besar cakupan H1 **sudah dikerjakan** di commit `00dd593` (v1.0.1, sesi Akun B sebelumnya):
pencocokan token kata utuh (`_token`/`_token_sublist`, bukan substring), sinonim
Shopee/Tokopedia/TikTok Shop/Lazada/Blibli dengan sumber & status verifikasi di
`references/sumber-kolom-marketplace.md`, pesan error yang menyebut kolom yang ada di file + flag
`--kolom-...`, dan 6 test fixture per marketplace di `tests/uji_regresi.py::UjiHeaderMarketplaceAsli`.
Bagian yang BELUM ada: penanganan eksplisit untuk kolom **ambigu** (lebih dari satu kolom di file
yang sama-sama cocok sinonim field yang sama) - sebelumnya auto-deteksi diam-diam memilih kandidat
pertama tanpa memberi tahu pengguna ada kandidat lain.

## Perubahan v1.0.2
1. **Fungsi baru `kolom_ambigu(header, sinonim, kol)`** (`scripts/resi.py`): untuk tiap field yang
   berhasil dipetakan, cek apakah ada kolom LAIN (belum dipakai field lain) yang juga cocok sinonim
   field itu (persis atau token-sublist). Kalau ada >1 kandidat, field itu ditandai ambigu.
2. **Peringatan eksplisit** di `proses()`: field ambigu yang TIDAK dipetakan manual lewat
   `--kolom-...` menghasilkan baris di `peringatan` yang menyebut semua kolom kandidat, kolom yang
   akhirnya dipakai, dan flag `--kolom-<field>` untuk membetulkan. Field baru `kolom_ambigu` di JSON
   keluaran juga memuat ini secara terstruktur (per label field manusiawi).
3. **SKILL.md** langkah 3 & catatan PERLU REVIEW diperbarui supaya agent tahu memeriksa
   `kolom_ambigu`/peringatan dan menawarkan `--kolom-...` bila ada kandidat ganda.
4. **Versi** dinaikkan ke `1.0.2` (`VERSI` di `scripts/resi.py`).

## Contoh kasus ambigu
File dengan kolom "SKU Induk" dan "Nomor SKU" sekaligus - keduanya cocok sinonim SKU. Sebelumnya:
dipetakan diam-diam ke salah satu (posisi pertama), tanpa jejak untuk pengguna. Sekarang: tetap
dipetakan (tidak gagal - lebih baik jalan dengan peringatan daripada berhenti untuk kasus yang
biasanya tidak fatal), TAPI `peringatan` & `kolom_ambigu` menyebut "SKU Induk" dan "Nomor SKU" +
kolom yang dipakai + saran `--kolom-sku "Nomor SKU"` bila salah.

## Pengujian
- `tests/uji_regresi.py`: 27 → **29 test** (+2: `UjiKolomAmbigu` - peringatan ambigu muncul saat
  dua kolom SKU mirip, dan peringatan hilang begitu dipetakan manual lewat `--kolom-sku`). Semua 29
  lulus: `python3 skills/resi-picking/tests/uji_regresi.py`.
- `python3 scripts/validate.py --skill resi-picking` ✅.
- Tidak menjalankan `bash scripts/uji_openclaw.sh` (di luar cakupan tugas H1 sesi ini, sudah lulus
  di v1.0.1 menurut `catalog.csv`).

## Belum diperbaiki / masih terbuka
- Nama kolom Shopee/Tokopedia/Lazada/Blibli tetap berstatus **best-effort** (lihat
  `references/sumber-kolom-marketplace.md`) - belum ada contoh file ekspor asli untuk dicocokkan
  satu-satu. Rekomendasi tetap sama: minta contoh file ekspor asli (data pembeli disamarkan) sebelum
  naik ke status `lulus`.
- Status `catalog.csv` (`uji`, versi `1.0.1`) sengaja TIDAK diubah di sesi ini sesuai instruksi kerja
  (catalog.csv bukan tanggung jawab agent pembuat) - perlu diperbarui manual ke `1.0.2` oleh sesi
  yang mengelola katalog.
- Temuan #2 (gabung lintas marketplace) dan #3 (baris "Total" tanpa SKU) dari `HASIL-UJI.md` v1.0.0
  masih di luar cakupan, seperti dicatat di `UJI-PEMBUAT-v1.0.1.md`.
