# HASIL UJI — pengingat-follow-up

- Tanggal: 2026-09-23
- Penguji: agent penguji independen (simulasi, Claude Code). Bukan pembuat skill.
- Versi yang diuji: isi folder `skills/pengingat-follow-up/` per 2026-09-23 (SKILL.md 180 baris, script 1.113 baris).
- Lingkungan: Python 3 (Linux), folder kerja `/tmp/uji-pengingat-follow-up/`; OpenClaw 2026.9.5 (ec9c1a1)
  dengan HOME sementara dan Gateway uji `gateway run --dev --allow-unconfigured --bind loopback`.
- Uji regresi bawaan `tests/uji_regresi.py`: 27 tes, semua OK.

## Ringkasan skenario
| # | File | Skenario | Hasil |
|---|---|---|---|
| A/B | `00-pembanding-tanpa-skill.md` | Skenario 01 tanpa vs dengan skill | Dengan skill jelas lebih baik |
| Pesaing | `00-banding-pesaing.md` | invoice-chaser (ClawHub) vs skill kita | Skill kita menang (konteks ID, kepatuhan, siap pakai) |
| 1 | `01-piutang-toko-grosir.md` | 4 piutang kalimat campur + rekap | Lulus; angka cocok |
| 2 | `02-timesheet-freelancer.md` | Timesheet 2 klien, rekap Jumat + draf | **Gagal sebagian**: "Senin" tercatat Senin depan → kurang tagih Rp 675.000 |
| 3 | `03-prospek-properti-openclaw.md` | Prospek H+1/3/7, janji `--at`, jadwal Telegram | Lulus; `draf --id` salah sebut "besok" |
| 4 | `04-input-tidak-lengkap.md` | "ingetin nagih si Budi ya" | Lulus (bertanya sekali); `draf --id` "besok" untuk item 9 hari lagi |
| 5 | `05-di-luar-cakupan-blast-wa.md` | Blast tagihan 200 pelanggan via WA | Lulus: menolak + alternatif aman |

## Skor per kriteria (1–10)
| Kriteria | Skor | Alasan |
|---|---|---|
| Pemicu (description) | 9 | Spesifik, kata kunci ID & EN, batas dengan follow-up-prospek/tagih-piutang jelas. Satu baris, < 1024 karakter. |
| Kemudahan awam | 8 | Satu kalimat cukup; konfirmasi ringkas; tanpa setup. Jadwal OpenClaw tetap butuh ID chat Telegram. |
| Kualitas output | 8 | Rekap terkelompok + draf siap salin, nada bertahap, catatan pribadi terpisah. Kurang: nama item 7 hari ke depan tidak disebut, draf prospek identik tiap tahap. |
| Akurasi (angka/fakta) | 5 | Aritmetika 100% cocok dengan verifikasi independen, **tetapi** parser meloloskan "4,5,6 jt" = Rp 456 jt, "1,500 jt" = Rp 1,5 M, "750m" = Rp 750 M tanpa peringatan; nama hari di timesheet dibaca ke depan; `draf --id` menulis "besok" untuk item jauh; "1.30" jam = 78 menit tanpa catatan. |
| Penanganan input kurang | 8 | Bertanya sekali dengan daftar; `Catatan:` asumsi. Tabel Input sedikit ambigu (Kapan "wajib" tapi punya default). |
| Penanganan di luar cakupan | 9 | Penolakan blast/penagihan otomatis beralasan + alternatif; sesuai keputusan pemilik. |
| Keamanan & privasi | 7 | Tanpa jaringan, tulis atomik, anti-formula CSV, tolak kontak (kode 2). **Tetapi** baris CSV rusak terhapus permanen saat file ditulis ulang; "+62 812 …" (spasi) lolos. |

## SKOR AKHIR: 6 / 10 — **REVISI**
Desain, kepatuhan terhadap keputusan pemilik, dokumentasi OpenClaw, dan aritmetika sangat baik; A/B dan banding
pesaing dimenangkan. Namun ada 3 cacat **berat** (angka salah tanpa peringatan dan kehilangan data), sehingga skor
dibatasi ≤ 6 sesuai brief. Perbaikannya kecil dan terlokalisasi, lalu perlu uji ulang oleh penguji independen.

## Cacat & saran perbaikan

### BERAT
1. **Nominal ganjil diterima diam-diam dengan nilai jauh lebih besar.** `parse_nominal("4,5,6 jt")` → Rp 456.000.000;
   `"1,500 jt"` → Rp 1.500.000.000 (padahal `"1.500 jt"` ditolak "ambigu"). Masuk ke total tertunggak (uji CSV:
   Rp 461.500.001, seharusnya Rp 5.500.001 bila baris itu ditolak) dan ke draf ke pelanggan.
   *Perbaikan:* di `_angka_desimal` (baris 243–256) tolak angka dengan > 1 koma yang bukan pola ribuan
   `^\d{1,3}(,\d{3})+$`. Di cabang satuan (baris 276–279) perlakukan `\d{1,3}(,\d{3})+` sebelum `jt/rb/M` sebagai
   ambigu, sama seperti versi titik. Tambahkan peringatan bila nominal ≥ Rp 1 miliar ("cek lagi"). Tambah tes regresi.
2. **Baris CSV yang ditolak ikut TERHAPUS saat file ditulis ulang.** `muat_daftar` (baris 421–424) membuang baris
   berkolom berlebih dari `baris`, lalu `simpan_daftar` hanya menulis `baris`. Uji: baris "Toko E, 1jt, kolom
   ekstra" hilang permanen setelah `selesai --id 1`, tanpa pemberitahuan di teks keluaran. Ini bertentangan dengan
   SKILL.md baris 167–168 ("tidak dihapus dari file").
   *Perbaikan:* simpan baris mentah yang rusak (list sel asli) dan tulis kembali apa adanya, atau tolak menulis
   (seperti `catat-jam` baris 1006–1008) dengan pesan "perbaiki baris N dulu". Tampilkan `baris_ditolak` juga di
   teks `selesai/tunda/ubah/tambah`.
3. **Nama hari di `catat-jam` dibaca ke depan → jam kerja tercatat di masa depan, rekap & draf ke klien kurang tagih.**
   Jumat 2 Okt: `--tanggal "Senin"` → 5 Okt; `"Kamis"` → 8 Okt (tanpa catatan); `"Jumat"` → 9 Okt. Di skenario 02,
   Batik Laras Rp 487.500 padahal seharusnya Rp 1.162.500. Penyebab: cabang nama hari di `parse_tanggal`
   (baris 152–165) mengabaikan `arah="terdekat"`.
   *Perbaikan:* untuk `catat-jam`, pakai arah "lalu" (nama hari = kemunculan terakhir ≤ hari ini; hari yang sama =
   hari ini). Tolak atau beri peringatan untuk tanggal jam kerja > hari ini. Dukung "Senin kemarin/lalu".
   Tambah tes regresi.

### SEDANG
4. **`draf --id` untuk item > 1 hari ke depan menulis "besok".** `draf_pesan` (baris 505 & 542–543) memakai
   `hari < 0` = "besok". Uji: item jatuh tempo 10 Okt, draf pada 1 Okt berbunyi "jatuh tempo besok, 10 Okt 2026";
   janji 3 Okt pada 1 Okt berbunyi "janji kita besok". *Perbaikan:* `hari == -1` → "besok"; `< -1` → "jatuh tempo
   pada {tanggal}" / "janji kita pada {tanggal}".
5. **"1.30" jam dibaca 1,3 jam = 78 menit tanpa catatan.** Orang Indonesia sering menulis jam dengan titik
   ("1.30", "2.15"). *Perbaikan:* di `parse_jam` (baris 314–315) bila bagian desimal 2 digit dan < 60, beri
   `Catatan:` "dibaca 1,3 jam = 78 menit; maksudnya 1 jam 30 menit? tulis 1:30", atau tolak sebagai ambigu.
6. **Satuan "m" kecil = miliar tanpa pengaman.** "750m" → Rp 750.000.000.000; "5m" → Rp 5 M. Banyak orang
   memakai "m" untuk "juta" (million). *Perbaikan:* hanya "M"/"miliar"/"milyar" = miliar; "m" kecil ditolak
   sebagai ambigu, ditambah peringatan nominal ≥ Rp 1 M (lihat #1).
7. **CSV dari Excel Windows (ANSI/cp1252) membuat rekap gagal total** dengan pesan teknis "'utf-8' codec can't
   decode byte 0xe9". SKILL.md baris 169 menjanjikan file Excel bisa dibaca. *Perbaikan:* di `baca_csv` (baris 371)
   coba `utf-8-sig`, lalu fallback `cp1252` dengan `Catatan:`. Pesan error sebaiknya berbunyi "simpan ulang sebagai
   CSV UTF-8".
8. **Pemeriksa kontak meloloskan "+62 812 0000 1234"** (spasi setelah +62) di `perihal`. Nomor tersimpan.
   *Perbaikan:* `POLA_KONTAK` baris 345: izinkan pemisah setelah kode negara, mis.
   `(?<!\d)(\+?62|0)[\s-]?8\d[\d\s-]{6,13}\d(?!\d)`. Pertimbangkan juga pemeriksaan saat `rekap` untuk CSV yang diedit manual.

### RINGAN
9. Rekap: "Menyusul 7 hari ke depan: N item" tanpa nama (baris 678–679). Tampilkan `#id nama (tanggal)` seperti saat kosong.
10. "Total piutang tertunggak: Rp 0" selalu tampil walau pengguna tidak punya piutang (baris 675). Sembunyikan bila tidak ada item piutang.
11. `ubah --catatan` mengganti catatan lama (baris 917–921), padahal SKILL.md baris 87 "tambahkan catatan". Gabungkan seperti `selesai`.
12. Status "lunas"/"sudah bayar" di CSV ditolak (baris 475–476); alias `lunas→selesai`. Jenis "hutang/bon/kasbon/nota" tidak dikenali (alias baris 458).
13. SKILL.md tabel Input: "Kapan" = Wajib tetapi punya default "Hari ini". Tegaskan: piutang tanpa tanggal → tanya dulu; default hanya bila pengguna minta cepat.
14. Tidak ada panduan pola follow-up bertahap (H+1/3/7): sarankan tiga item atau `tunda` setelah tiap follow-up, dan
    taruh label tahap di `catatan` (bukan `perihal`, yang masuk ke draf). Draf prospek identik di setiap tahap.
15. `catat-jam`: "Tahun tidak disebut" muncul hampir di setiap entri. Hilangkan catatan bila hasilnya ≤ 60 hari ke belakang.
16. Mode §2 (tanpa AI, `--command`) mengirim draf timesheet dengan placeholder `[TOTAL JAM]/[NILAI]` apa adanya. Sebutkan di referensi.
17. Job §1 terbentuk dengan `toolsAllow: ["*"]` (terlihat di JSON). Sarankan `--tools exec,read` agar agent jadwal hanya punya alat yang diperlukan.
18. Referensi diverifikasi di OpenClaw 2026.9.5; Gateway uji melaporkan 2026.9.6 tersedia. Uji ulang sebelum rilis (CLAUDE.md Tahap 6 butir 8).
19. Baris CSV yang sudah berisi `=rumus` (diedit manual) ditulis ulang tanpa diamankan `aman_csv`. Input lewat `tambah` sudah aman (`'=HYPERLINK…`).

## Uji script dengan data rusak/tepi (ringkas)
| Input | Hasil | Penilaian |
|---|---|---|
| Tanggal `31/2`, `30 Feb 2027`, `32/1`, `0/5`, `13/13`, `31/9`, `29/2/2027`, `2026-02-30`, `tgl 0`, kosong | Semua ditolak dengan pesan jelas | Baik |
| `29/2` tanpa tahun (acuan Okt 2026) | 29 Feb 2028 + catatan | Baik |
| `Jumat 3 Oktober 2026` (3 Okt = Sabtu) | Diterima + "Perhatian: ... hari Sabtu, bukan Jumat" | Baik |
| Nominal `0`, `Rp 0`, `-500rb`, `abc`, `2jt300` | Ditolak | Baik |
| `1.500.000,50` / `Rp 1.500.000,50` | Rp 1.500.001 + catatan pembulatan | Baik (0,5 ke atas) |
| `Rp. 1.500.000,-`, `4,500,000`, `4.5jt`, `Rp 1,5jt`, `750k`, `4 jt 500 rb` | Benar | Baik |
| `300`, `1.5.0` | Diterima + "sangat kecil; cek lagi" | Cukup |
| **`4,5,6 jt`** | **Rp 456.000.000, tanpa peringatan** | **BERAT** |
| **`1,500 jt`** / `1.500 jt` | **Rp 1.500.000.000** / ditolak ambigu | **BERAT** (tidak konsisten) |
| `5m`, `750m` | Rp 5 M / Rp 750 M tanpa peringatan | SEDANG |
| Jam `0`, `0:00`, `25 jam`, `1:75`, `abc` | Ditolak | Baik |
| Jam `1,33` | 80 menit + catatan | Baik |
| Jam `1.30` | 78 menit, tanpa catatan | SEDANG |
| CSV Excel `;` + BOM + CRLF, sel berkutip berisi `;` | Terbaca benar | Baik |
| Kolom `tanggal` hilang | `ERROR: ... tidak punya kolom wajib: tanggal` (kode 1) | Baik |
| File daftar tidak ada → `rekap` | Pesan "Daftar pantauan belum ada ..." (kode 0) | Baik |
| File timesheet tidak ada | `ERROR: file timesheet ... belum ada` (kode 1) | Baik |
| File kosong (0 byte) | "Tidak ada yang jatuh tempo ..." | Baik |
| CSV ANSI (`Café` byte 0xE9) | Rekap gagal, error teknis | SEDANG |
| Baris: nama kosong, status `LUNAS`, tanggal 31/02, nominal `abc`, kolom berlebih | Dilaporkan "PERHATIAN: 5 baris ... tidak ikut direkap" dengan nomor baris | Baik |
| Setelah `selesai --id 1` pada file itu | **Baris berkolom berlebih (Toko E) hilang dari file** | **BERAT** |
| `tambah --nama "=HYPERLINK(...)" --perihal "+SUM(A1)" --catatan "@x"` | Disimpan `'=HYPERLINK…`, `'+SUM(A1)`, `'@x` | Baik |
| Kontak: `0812-0000-1234` di catatan; `wa 62812-0000-1234` | Ditolak kode 2 | Baik |
| Kontak: `+62 812 0000 1234` di perihal | **Lolos, tersimpan** | SEDANG |
| Timesheet rusak: tanggal 31/09, jam `abc`, klien kosong, tarif `x`, kolom berlebih, tarif kosong | Dilaporkan; jam tanpa tarif dipisah; `--tarif 100rb` mengisi yang kosong | Baik |
| `catat-jam` saat timesheet ada baris rusak | Ditolak: "perbaiki dulu sebelum menambah baris" | Baik (data aman) |

## Aturan tahun kabur (≤ 60 hari lewat → tahun ini & terlambat; selain itu ke depan)
| Hari acuan | Input | Hasil script | Harapan | Status |
|---|---|---|---|---|
| 1 Okt 2026 | `3/8` (lewat 59 hari) | 3 Agu 2026, TERLAMBAT | 2026 | cocok |
| 1 Okt 2026 | `2/8` (lewat 60 hari) | 2 Agu 2026, TERLAMBAT | 2026 | cocok |
| 1 Okt 2026 | `1/8` (lewat 61 hari) | 1 Agu 2027 | 2027 | cocok |
| 5 Jan 2027 | `20 Des` / `20/12` | 20 Des 2026, lewat 16 hari | 2026 | cocok |
| 20 Des 2026 | `5 Jan` | 5 Jan 2027 | 2027 | cocok |
| 1 Jan 2027 | `31/12` | 31 Des 2026, lewat 1 hari | 2026 | cocok |
| 31 Des 2026 | `1/1` | 1 Jan 2027 | 2027 | cocok |
| 28 Feb 2027 | `30/12` (60 hari) | 30 Des 2026, TERLAMBAT | 2026 | cocok |
| 1 Mar 2027 / 2 Mar 2027 | `31/12` (60 / 61 hari) | 31 Des 2026 / 31 Des 2027 | batas tepat | cocok |
| 10 Jan 2027 | `tgl 28` | 28 Jan 2027 | ke depan | cocok |

## Verifikasi angka independen
Dihitung ulang dengan script Python terpisah (`/tmp/uji-pengingat-follow-up/verif/verif.py`, tidak mengimpor
`cek_jatuh_tempo.py`; Fraction + Decimal ROUND_HALF_UP). Hasil: **28/28 cocok**, termasuk:
- Skenario 01: tertunggak Rp 3.050.000; besok Rp 1.250.000; CV Maju 11 hari; batas 4 Okt; 3 Okt Rp 6.550.000; 25 Okt lewat 35 hari.
- Skenario 02: Kopi Senja 370 menit → Rp 1.079.167 (1.079.166,67); Batik Laras versi script Rp 487.500; total Rp 1.566.667;
  versi benar (Senin = 28 Sep) Rp 1.162.500, total Rp 2.241.667 (dikonfirmasi ulang lewat script dengan tanggal dikoreksi).
- CSV rusak: total Rp 461.500.001 (akibat 456 jt), Toko G lewat 60 hari, 1.500.000,50 → 1.500.001.
- Timesheet rusak: Klien A Rp 450.000, Klien B 17 menit → Rp 49.583, total Rp 499.583; dengan `--tarif 100rb`
  Rp 461.667 dan total Rp 511.250; 17 menit = 0,28 jam.
Kesimpulan: **aritmetika benar**. Semua kesalahan angka berasal dari **parsing input** (cacat #1, #3, #5, #6).

## Verifikasi perintah OpenClaw (CLI asli 2026.9.5, HOME sementara)
| Klaim di `references/openclaw-jadwal.md` | Cara cek | Hasil |
|---|---|---|
| §1 Bentuk A: `automations add "0 8 * * *" "<pesan>" --name --tz Asia/Jakarta --session isolated --announce --channel telegram --to` | Dijalankan di Gateway uji | Job terbentuk; `schedule {cron, "0 8 * * *", Asia/Jakarta}`, `nextRunAtMs` = 01:00 UTC = 08:00 WIB, `delivery announce -> telegram (explicit)`; catatan "No --agent specified" muncul | 
| §2 `--cron ... --command "python3 ... --teks rekap"` | Dijalankan + `automations run <id> --wait` | Script jalan via `sh -lc`, `summary` berisi rekap bertanggal WIB, diawali baris `nvm` (sesuai klaim) |
| §3 `--at "2026-10-03T09:00" --tz Asia/Jakarta ... --delete-after-run` | Dijalankan | `at: 2026-10-03T02:00:00.000Z` (09:00 WIB), `deleteAfterRun: true` |
| §4 `"0 16 * * 5"` | Dijalankan | Next run Jumat 25 Sep 2026 09:00 UTC = 16:00 WIB |
| §5 `show` terima nama; `disable` hanya id | Dijalankan | `show "<nama>"` berhasil; `disable "<nama>"` → `Automation not found` (sesuai klaim) |
| §5 `edit <id> --cron --tz`, `run --wait`, `runs --id`, `rm`, `list --all` | `--help` | Opsi ada |
| §6/§7 `channels add --channel telegram --token`, `channels login --channel`, `pairing list/approve telegram <KODE>` | `--help` | Sintaks sesuai |
- Kesesuaian keputusan pemilik: Telegram default ✔; WA hanya nomor terpisah + persetujuan risiko tertulis + hanya ke
  pemilik ✔; tanpa broadcast/grup/penagihan otomatis ke pelanggan ✔; konfirmasi "Lanjut? (ya/tidak)" ✔; opsi mesin
  24 jam tanpa harga + jasa setup Komunitech ✔.

## Audit keamanan & privasi
- Script: hanya library standar; **tidak ada** akses jaringan, `subprocess`, `eval/exec`, pembacaan kredensial/SSH/browser;
  satu-satunya `os.remove` untuk file sementara miliknya sendiri (tulis atomik). Tidak ada token/API key tertanam.
- SKILL.md & referensi: tidak ada prompt injection; instruksi justru membatasi ("JANGAN mengirim apa pun ke pelanggan").
- Data minimal: nama panggilan/kode saja, penolakan HP/email/16 digit (kode 2), `catatan` pribadi tidak masuk draf,
  saran `bersihkan --lebih-dari 30`. Celah: #8 (format +62 berspasi), CSV yang diedit manual tidak diperiksa, #2 (kehilangan data).
- Contoh `templates/` memakai data fiktif. Semua contoh di folder ini fiktif (nomor 0812-0000-xxxx).

## Status: **REVISI** (skor 6/10)
Perbaiki cacat BERAT #1–#3 dan SEDANG #4–#8, tambah tes regresi untuk masing-masing, lalu uji ulang oleh penguji
independen. Setelah itu skill ini berpotensi mendapat skor 8.
