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

---

## Uji independen Akun B (2026-09-26)

Penguji: Akun B (independen dari pembuat, sesi terpisah dari uji sebelumnya di atas). Skill
dijalankan dari lokasinya di repo (kode tidak diubah); data pasien dibuat di scratchpad
`/tmp/.../scratchpad/u22/` (seluruhnya fiktif), tidak disimpan di repo. Tidak ada file
kode/SKILL.md/README/catalog.csv yang diubah. `python3 tests/uji_regresi.py`: **28/28 lulus**.
`python3 scripts/validate.py --skill pengingat-pasien-klinik` (dari root repo): **lulus**
("1 skill valid, 80 baris katalog sesuai"). `scripts/uji_openclaw.sh` **tidak dijalankan**
(di luar tugas sesi ini per instruksi).

### Skor kualitas: **7/10**

**Alasan:** Fungsi inti (catat, daftar H-3/H-1/hari-ini/terlambat, ubah status, hapus, impor,
ringkasan, draf) tetap benar dan konsisten dengan SKILL.md; semua tanggal yang diverifikasi
manual (termasuk batas bulan, batas tahun, dan tahun kabisat) cocok kecuali satu bug lama yang
direproduksi ulang. Tidak ada kode jaringan/kredensial — audit keamanan bersih. Skor **turun dari
8/10 (uji sebelumnya) menjadi 7/10** karena ditemukan **1 temuan baru tingkat TINGGI**: kata
kunci diagnosis (`campak`, `rabies`, `dbd`, dll.) di `KATA_DIAGNOSIS` memblokir jenis kunjungan
yang sebetulnya sah dan eksplisit disebut sebagai skenario inti skill sendiri ("imunisasi
campak" untuk klinik anak, "vaksin rabies" untuk klinik hewan) — ini bukan cuma soal gaya bahasa,
tapi memblokir kasus pakai yang dijanjikan SKILL.md. Ditambah 1 temuan tingkat sedang-tinggi
(blocklist diagnosis punya celah lebar untuk penyakit umum di luar ~40 kata) dan reproduksi ulang
1 bug tanggal tahun kabisat yang sudah tercatat sebelumnya (masih belum diperbaiki di kode saat
ini). Skor masih di atas ambang 7 sehingga secara teknis lolos, tapi TIDAK disarankan naik ke
`beta` sebelum temuan tingkat tinggi diperbaiki, karena berisiko membuat staf klinik anak/hewan
gagal mencatat pengingat yang justru paling umum mereka butuhkan.

### Ringkasan skenario baru yang dijalankan
| # | Skenario | Hasil |
|---|---|---|
| 00a | A/B tanpa vs dengan skill (ulang, independen) | Skill tetap unggul jelas — `00-pembanding-tanpa-skill-uji-akun-b.md` |
| 00b | Banding pesaing (pencarian ulang, independen) | Tidak ada pesaing terbukti; 1 kandidat baru ditemukan tapi tidak bisa diverifikasi (403) — `00-banding-pesaing-uji-akun-b.md` |
| 01 | Klinik gigi, kontrol behel (normal) | Lulus, tanggal & H-3 diverifikasi manual cocok |
| 02 | Klinik anak, imunisasi (normal) | **Gagal tanpa workaround** — "imunisasi campak"/"vaksin campak" ditolak sebagai diagnosis; lulus setelah diganti "imunisasi rutin" |
| 03 | Fisioterapi, sesi lanjutan (normal) | Lulus untuk pengelompokan H-1/H-3/hari-ini/terlambat; bug tahun kabisat direproduksi ulang di "N bulan lagi" |
| 04 | Input tidak lengkap | Lulus, field wajib (tanggal, persetujuan) tidak bisa dilewati, tidak ada asumsi diam-diam |
| 05 | Di luar cakupan (diagnosis + kirim otomatis/broadcast) | Kirim otomatis/broadcast: lulus total (struktural, tidak ada kode jaringan). Diagnosis: lulus untuk kata di blocklist, TAPI "batu ginjal" dan penyakit umum lain di luar daftar **lolos tersimpan** |

### Temuan (tingkat tinggi/sedang/rendah)

**Tingkat TINGGI**
1. **Blocklist diagnosis memblokir jenis kunjungan sah yang jadi skenario inti skill.**
   `KATA_DIAGNOSIS` di `scripts/pengingat_pasien.py` memuat `campak`, `rabies`, `dbd`, `tbc`,
   `tuberkulosis`, `malaria`, `campak`, `difteri`, `kusta` — semuanya juga nama **vaksin/imunisasi
   rutin** yang sangat umum disebut apa adanya oleh staf klinik anak dan klinik hewan (dua target
   pengguna yang disebut eksplisit di SKILL.md). Akibatnya `"vaksin rabies"` (jenis kunjungan
   paling umum di klinik hewan Indonesia) dan `"imunisasi campak"` (imunisasi dasar anak) **selalu
   ditolak**, padahal keduanya bukan pengungkapan diagnosis pasien — nama vaksin bukan rahasia
   medis dengan sensitivitas yang sama dengan diagnosis penyakit yang diderita. Bukti & langkah
   reproduksi lengkap: `examples/02-klinik-anak-imunisasi-uji-akun-b.md`.
   **Saran perbaikan:** keluarkan nama vaksin umum dari `KATA_DIAGNOSIS`, atau beri pengecualian
   ketika kata itu langsung didahului "vaksin"/"imunisasi" (`\b(vaksin|imunisasi)\s+campak\b`),
   sambil tetap menolak pola seperti "riwayat campak"/"kena campak"/"positif rabies".

**Tingkat SEDANG**
2. **Blocklist diagnosis punya celah lebar untuk penyakit umum di luar ~40 kata terdaftar.**
   Diuji: `batu ginjal, asma, maag, usus buntu, katarak, glaukoma, varises, wasir, amandel,
   sinusitis, vertigo, anemia, leukemia, gerd, polip` — semuanya **lolos tersimpan** tanpa
   penolakan (tidak ada di `KATA_DIAGNOSIS`). Komentar kode sudah jujur menyebut daftar ini bukan
   daftar medis lengkap, jadi ini bukan klaim yang menyesatkan, tapi celahnya lebih lebar dari
   kesan "jaring pengaman" — mencakup istilah penyakit sehari-hari, bukan cuma istilah medis
   jarang. Mitigasi utama harus tetap dari kepatuhan agent ke instruksi SKILL.md (checklist
   "jangan simpan diagnosis"), bukan mengandalkan validasi teknis script semata. Bukti:
   `examples/05-di-luar-cakupan-uji-akun-b.md`.
3. **Bug tahun kabisat pada "N bulan lagi" direproduksi ulang (sudah tercatat di uji sebelumnya,
   belum diperbaiki).** `parse_tanggal()` memakai `min(acuan.day, 28) if bln == 2` tanpa mengecek
   `calendar.isleap`, sehingga penjadwalan ulang dari tanggal 29-31 Januari (atau bulan panjang
   lain) ke Februari di tahun kabisat mendarat di 28 Februari, bukan 29 Februari yang valid.
   Dampak kecil (maju 1 hari, bukan terlewat) tapi tetap salah hitung. Bukti:
   `examples/03-fisioterapi-uji-akun-b.md`.

**Tingkat RENDAH**
4. Tidak ditemukan celah keamanan baru (tidak ada kode jaringan/kredensial/subprocess shell;
   audit ulang kode sumber `scripts/pengingat_pasien.py` baris demi baris mengonfirmasi ini).
5. Penanganan data rusak (CSV kosong, file tidak ada, kolom hilang/lebih, tanggal format salah,
   nomor WA aneh — termasuk notasi ilmiah Excel, encoding cp1252 dengan BOM dan karakter
   non-ASCII) **semuanya ditangani dengan baik**: pesan error jelas, baris rusak tidak
   menghentikan program, file cp1252 dibaca lalu ditulis ulang sebagai UTF-8 saat ada perubahan.
   Tidak ada temuan baru di area ini.

### Rekomendasi
Perbaiki temuan tingkat TINGGI (#1) sebelum naik status ke `beta`, karena ini memblokir skenario
inti yang dijanjikan SKILL.md sendiri untuk 2 dari target pasar utamanya (klinik anak, klinik
hewan). Temuan #2 dan #3 bisa disertakan dalam perbaikan yang sama sebelum `beta`. Skor 7/10 —
di ambang batas revisi (Tahap 6.7: "di bawah 7 → revisi"); disarankan tetap direvisi meski pas di
angka 7, mengingat dampaknya langsung ke dua segmen pengguna yang disebut eksplisit di SKILL.md.

## Revisi v1.0.1 (2026-09-27) — perbaikan temuan Akun B

Perbaikan oleh agent pembuat (H8), untuk ketiga temuan di atas:
1. **TINGGI (#1)** — `KATA_JUGA_VAKSIN` + `POLA_PEMICU_VAKSIN` ditambahkan di
   `scripts/pengingat_pasien.py`: nama penyakit yang juga nama vaksin (campak, rabies, difteri,
   dll) diizinkan bila berdekatan dengan kata "vaksin/imunisasi/vaksinasi/booster/suntik" dan
   TIDAK ada kata bernada diagnosis (`KATA_PENANDA_DIAGNOSIS`: riwayat, positif, didiagnosis,
   menderita, kena, sakit, dll) di kalimat yang sama. "imunisasi campak", "vaksin rabies", "vaksin
   MR", "imunisasi difteri (DPT)" kini diterima; "riwayat campak", "positif rabies", "didiagnosis
   difteri" tetap ditolak.
2. **SEDANG (#2)** — `KATA_DIAGNOSIS` diperluas (batu ginjal, asma, maag, usus buntu, katarak,
   glaukoma, varises, wasir, amandel, sinusitis, vertigo, anemia, leukemia, polip, migrain,
   bronkitis, pneumonia, infeksi saluran kemih, hernia, tifoid, disentri, gondok, tiroid, lupus,
   rematik, asam urat, dan vaksin-preventable disease umum lain). Tetap bukan daftar medis
   lengkap (jaring pengaman, bukan validasi klinis) — kepatuhan agent ke checklist SKILL.md tetap
   mitigasi utama. Pesan penolakan kini menyarankan jenis kunjungan netral ("kontrol lanjutan").
3. **SEDANG (#3)** — bug tahun kabisat pada "N bulan lagi" diperbaiki: kode tidak lagi
   hard-code `min(hari, 28)` untuk Februari, cukup coba tanggal asli lalu turun satu-satu bila
   bulan tujuan lebih pendek (`_coba_tanggal` sudah tahu kabisat lewat `datetime.date`).
   29 Jan 2028 + 1 bulan sekarang -> 29 Feb 2028 (2028 kabisat), bukan 28 Feb.

6 tes regresi baru ditambahkan (28 tes lama tidak diubah, semua tetap lulus tanpa modifikasi):
`test_bulan_lagi_tahun_kabisat`, `test_nama_vaksin_lolos_berkonteks_vaksin`,
`test_nama_vaksin_tetap_ditolak_bila_bernada_diagnosis`,
`test_diagnosis_umum_diluar_daftar_lama_ditolak`, `test_jenis_imunisasi_campak_diterima`,
`test_jenis_vaksin_rabies_diterima`. `python3 tests/uji_regresi.py`: **34/34 lulus**.
`python3 scripts/validate.py --skill pengingat-pasien-klinik`: **lulus** ("1 skill valid, 80 baris
katalog sesuai"). `scripts/uji_openclaw.sh` tidak dijalankan (di luar tugas sesi ini).
Skor kualitas belum dinilai ulang oleh penguji independen — perlu uji independen baru sebelum naik
status ke `beta`, sesuai Tahap 6.7 SKILL Factory.
