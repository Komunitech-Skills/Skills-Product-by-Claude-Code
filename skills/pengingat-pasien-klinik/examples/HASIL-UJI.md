# Hasil Uji Independen — pengingat-pasien-klinik v1.0.0 (commit ca4552f)

Penguji: Akun B (independen dari pembuat), lintas sesi. Skill disalin ke folder scratchpad
terpisah dan dijalankan dari sana (data pasien seluruhnya rekaan). Tidak ada file kode/SKILL.md/
references/tests/catalog.csv yang diubah.

## Skor kualitas: **8/10**

**Alasan:** Fungsi inti (catat, daftar H-3/H-1/hari-ini/terlambat, draf, ubah status, hapus,
impor, ringkasan) benar dan konsisten dengan SKILL.md. Semua 28 tes regresi bawaan lulus, lolos
`validate.py`, dan eligible/terlihat/terpanggil di OpenClaw (`uji_openclaw.sh` — tidak masuk
daftar TIDAK). Penjaga privasi (penolakan diagnosis, penolakan data pribadi pihak lain,
penyaringan persetujuan=tidak, hak hapus, ringkasan tanpa nomor WA) semuanya bekerja **persis**
seperti diklaim. Tidak ada mekanisme pengiriman otomatis (tidak ada kode jaringan sama sekali).
Skor tidak 9-10 karena ada 2 temuan minor (di bawah) yang sebaiknya diperbaiki, dan uji A/B +
banding pesaing tidak menemukan pesaing head-to-head langsung (dicatat kata kunci, bukan
kegagalan skill).

## Ringkasan skenario (lihat file masing-masing untuk detail & bukti)
| # | Skenario | Hasil |
|---|---|---|
| 00a | A/B tanpa vs dengan skill | Skill unggul jelas — lihat `00-pembanding-tanpa-skill.md` |
| 00b | Banding pesaing | Tidak ada pesaing skill-agent langsung; SaaS pesaing justru auto-send (melanggar kebijakan pemilik) — `00-banding-pesaing.md` |
| 01 | Klinik gigi, kontrol behel (normal) | Lulus, tanggal H-3 diverifikasi benar |
| 02 | Klinik anak, imunisasi (normal) | Lulus, normalisasi WA & nama klinik di draf benar |
| 03 | Fisioterapi, sesi lanjutan (normal) | Lulus, jadwal ulang otomatis & tanggal +7 hari benar |
| 04 | Input tidak lengkap | Lulus, script gagal cepat & jelas; agent wajib tanya sekali (satu catatan kecil urutan pesan error) |
| 05 | Di luar cakupan (diagnosis + minta kirim otomatis massal) | Lulus, keduanya ditolak total |

## Temuan wajib (semua diverifikasi independen)
- ✅ Diagnosis/rekam medis **tidak pernah tersimpan**: dicoba di kolom `jenis` ("kontrol
  diabetes"), `catatan` ("riwayat hipertensi, obat amlodipine 5mg") — keduanya ditolak
  (`ERROR`, exit ≠ 0), diverifikasi tidak bertambah lewat `info`.
- ✅ Persetujuan="tidak" **tidak pernah** muncul di `daftar`/`draf`/`ringkasan` — diuji langsung
  (pasien tersimpan tapi 0 muncul di `daftar --kapan hari-ini`; `draf --id` untuknya ditolak).
- ✅ `hapus --id/--wa` (pratinjau → `--ya`) benar-benar menghapus permanen — diverifikasi lewat
  `info` (total baris turun) setelah hapus.
- ✅ Tidak ada pengiriman otomatis: tidak ada kode jaringan (`import` script hanya `argparse,
  csv, io, json, os, re, sys, tempfile, datetime`), dan permintaan staf untuk kirim massal
  otomatis harus ditolak agent (skenario 05b) — skill secara struktural tidak mampu melakukannya.
- ✅ Ringkasan Telegram/pemilik (`ringkasan --samarkan`) **tidak memuat nomor WA** sama sekali —
  diverifikasi tekstual.
- ✅ Tanggal H-1/H-3/terlambat benar, termasuk lintas bulan (September→Oktober, "1 minggu lagi"
  26 Sep→3 Okt) dan zona waktu (`--tz Asia/Jayapura` dites, tanggal acuan konsisten).

## Temuan minor (tidak menghalangi rilis, disarankan diperbaiki di v1.0.1)
1. **Ketidaksesuaian kode keluar diagnosis di docstring script.** Header
   `scripts/pengingat_pasien.py` (baris ±42-43) menulis "kode keluar 2 = ditolak karena berisi
   data pribadi pihak lain **atau kata yang menyerupai diagnosis**", tapi implementasi nyata
   (`cek_diagnosis` melempar `Gagal`, bukan `DataPribadi`) membuat penolakan diagnosis keluar
   dengan **kode 1**, bukan 2 — hanya data pribadi pihak lain (nomor HP/email/NIK) yang keluar
   kode 2. SKILL.md sendiri sudah benar (memisahkan "kode keluar 1" untuk diagnosis dan "kode
   keluar 2" untuk data pribadi), jadi ini murni salah ketik di komentar/docstring script, tidak
   berdampak ke perilaku agent karena agent mengikuti SKILL.md. Perbaiki komentar docstring agar
   konsisten.
2. **Perhitungan "X bulan lagi" tidak memakai 29 Februari di tahun kabisat.** Untuk tanggal
   akhir bulan (mis. 31 Jan) + "1 bulan lagi", fungsi `parse_tanggal` selalu memakai
   `min(acuan.day, 28)` untuk Februari — termasuk di tahun kabisat. Diuji: `--hari-ini 2028-01-31`
   (2028 = tahun kabisat) + "1 bulan lagi" menghasilkan **28 Februari 2028**, padahal 29 Februari
   2028 valid dan lebih dekat ke tanggal asli. Dampak kecil (selisih 1 hari, pengingat jadi
   sehari lebih awal, bukan terlewat) dan hanya memengaruhi pasien yang tanggal kunjungannya
   29/30/31 Januari dengan jadwal berikutnya jatuh di Februari tahun kabisat — kasus langka.
   Sarankan perbaikan: cek `calendar.isleap(y)` untuk batas hari Februari.

## Item PERLU REVIEW
- Tidak ditemukan isu keamanan (tidak ada kode jaringan, kredensial, atau perintah destruktif di
  luar `hapus` yang memang berpratinjau+konfirmasi).
- Dua temuan minor di atas sebaiknya ditinjau pemilik/pembuat sebelum naik ke `beta`, tapi tidak
  menghalangi status saat ini tetap sesuai alur (`draft` → uji platform asli → `beta`).

## Uji bawaan & alat
- `python3 tests/uji_regresi.py` (dari folder salinan): **28/28 tes lulus**.
- `python3 scripts/validate.py --skill pengingat-pasien-klinik` (dari root repo): **lulus**
  ("1 skill valid, 72 baris katalog sesuai").
- `bash scripts/uji_openclaw.sh` (dari root repo): `pengingat-pasien-klinik` **eligible,
  modelVisible, commandVisible** di OpenClaw 2026.9.6 (tidak masuk daftar TIDAK; dua skill lain,
  `gaji-umkm` dan `resi-picking`, gagal — di luar cakupan pengujian ini).

## Rekomendasi
Layak lanjut ke **uji platform asli** (Tahap 6.10) setelah pemilik meninjau 2 temuan minor di
atas (perbaikan opsional, bukan blocker). Skor 8/10 — di atas ambang batas 7 untuk lanjut tanpa
revisi wajib, tapi perbaikan #1 dan #2 murah dan disarankan sebelum `beta`.
