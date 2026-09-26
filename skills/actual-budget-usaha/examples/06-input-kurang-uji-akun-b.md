# Skenario 6 (input tidak lengkap) — uji Akun B

**Pengguna:** "Tolong masukin mutasi ke Actual dong, sama kasih tau sisa anggaran."
(Tanpa file, tanpa nama bank/akun, lokasi budget tidak diketahui.)

## Perilaku yang diharapkan SKILL.md & yang diuji
- `cari` di komputer tanpa folder `Documents/Actual` → kode 3: "Tidak ada budget Actual di: ...; Cek lokasi di Actual:
  Settings → 'Actual's data directory' ... Versi web/server menyimpan data di browser/server" ✔
- `cari --folder data` menemukan 2 budget; `ringkasan --db data` → kode 2 "Folder berisi lebih dari satu budget.
  Pilih salah satu" + daftar ✔
- Mutasi BCA tanpa tahun → kode 2 minta `--tahun` ✔; file `.xlsx` → minta simpan sebagai CSV ✔; `.pdf` → minta CSV ✔;
  file kosong → "kosong" ✔; file tidak ada → kode 3 ✔; `--bulan Agustusan` / `2026-13` → kode 2 dengan contoh ✔

## Draf balasan agent (satu pesan, pertanyaan singkat)
> Siap. Supaya sekali jalan, saya perlu:
> 1. File mutasi **CSV** dari internet banking (bukan PDF; kalau Excel, "Simpan Sebagai" CSV). Bank apa?
> 2. Nama akun tujuannya di Actual (mis. "BCA Usaha").
> 3. Bulan & tahun mutasi (BCA tidak mencantumkan tahun).
> 4. Budget Actual Anda tidak ketemu di folder Documents/Actual. Buka Actual → Settings → "Actual's data
>    directory", lalu kirim lokasinya. (Kalau Actual Anda dibuka lewat browser, ringkasan otomatis butuh file Export.)
> Kalau mau cepat: kirim file-nya saja, saya anggap tahun 2026 dan saya sebutkan asumsinya.

**Hasil: LULUS** — semua kasus kurang/rusak berhenti dengan pesan bahasa Indonesia yang bisa ditindaklanjuti,
tanpa menebak angka.
