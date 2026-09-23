# Daftar perintah `scripts/absensi.py`

Format umum: `python3 scripts/absensi.py <perintah> [opsi] [--db PATH] [--json]` (Windows: `python`/`py`).
Perintah bertanda **(tulis)** hanya pratinjau sampai ditambah `--ya` setelah pengguna setuju.

| Perintah | Kegunaan | Opsi penting |
|---|---|---|
| `init` (tulis) | Buat database + shift `REG` 08.00–17.00 | — |
| `info` | Lokasi database, jumlah karyawan/tap, shift, pengaturan | — |
| `backup` | Salinan bertanggal ke `backup-absensi/` | — |
| `atur` (tulis) | Pengaturan | `--toleransi <menit>` (default 0), `--jeda-duplikat <menit>` (default 5), `--nama-usaha` |
| `shift tambah` (tulis) | Tambah/ubah shift | `--kode`, `--masuk`, `--pulang` (≤ masuk = lewat tengah malam), `--istirahat <menit>` (default 60), `--pulang-hari-pendek` (pola 6 hari; `-` hapus) |
| `shift daftar` | Lihat shift | — |
| `karyawan tambah` (tulis) | Daftarkan karyawan | `--kode`, `--nama`, `--jabatan`, `--shift`, `--hari-kerja 5|6`, `--libur-mingguan sabtu,minggu`, `--hari-pendek sabtu|-`, `--id-mesin`, `--gaji-pokok`, `--tunjangan-tetap`, `--tunjangan-tidak-tetap`, `--upah-harian`, `--tanpa-lembur ya|tidak`, `--mulai` (default tgl 1 bulan ini) |
| `karyawan ubah` (tulis) | Ubah data (opsi sama) | `--kode` (atau nama), `--nonaktif`, `--aktifkan` |
| `karyawan daftar` | Lihat karyawan | — |
| `karyawan impor <file>` (tulis) | Banyak karyawan dari CSV/XLSX | kolom seperti `templates/karyawan.csv`; satu baris rusak → tidak ada yang disimpan |
| `libur tambah` (tulis) | Hari libur resmi | `--tanggal` + `--nama`, atau `--file` (kolom tanggal;nama) |
| `libur hapus` / `libur daftar` | — | `--tanggal` / `--tahun` |
| `catat` (tulis) | Masuk/pulang manual | `--karyawan`, `--masuk`, `--pulang` (`sekarang` boleh), `--tanggal`, `--lewat-tengah-malam`, `--ganti` |
| `keterangan` (tulis) | izin/sakit/cuti/alpa/dinas | `--karyawan`, `--jenis`, `--tanggal`, `--sampai`, `--catatan` |
| `lembur` (tulis) | Lembur **disetujui** | `--karyawan`, `--tanggal` (tanggal mulai shift), `--jam` (2, 1,5, 1:30), `--catatan` (siapa menyetujui), `--ganti`, atau `--file` (kolom tanggal;kode;jam;disetujui_oleh) |
| `hapus` (tulis) | Hapus data satu tanggal | `--karyawan`, `--tanggal`, `--jenis tap|keterangan|lembur|semua` (default tap) |
| `impor-absen <file>` (tulis) | File mesin fingerprint | `--kolom-id/-nama/-waktu/-tanggal/-jam/-status/-masuk/-pulang "Nama Kolom"` (`-` = abaikan), `--format-tanggal dmy|mdy`, `--dari`, `--sampai` |
| `rekap` | Rekap per karyawan | `--bulan 2026-09|lalu`, atau `--dari/--sampai` (maks 62 hari), `--karyawan`, `--pola 5|6`, `--csv`, `--csv-harian`, `--csv-gaji`, `--gabung <file-gaji.csv>` |
| `harian` | Laporan satu hari | `--tanggal` (default hari ini), `--karyawan` |

## Pengenalan kolom file mesin (otomatis, bisa ditimpa `--kolom-*`)
- **ID**: `ID`, `No. ID`, `User ID`, `PIN`, `AC-No.`, `Enroll ID`, `Emp No.`, `ID Karyawan`, `Kode` …
- **Nama**: `Nama`, `Name`, `Nama Karyawan` … (dipakai bila ID tidak cocok; nama kembar ditolak)
- **Waktu gabungan**: `Waktu`, `Tanggal/Waktu`, `DateTime`, `Check Time`, `Timestamp` …; atau **Tanggal** + **Jam** terpisah (`Date` + `Time`).
- **Status** (opsional): `C/In`, `Check In`, `Masuk`, `0` = masuk; `C/Out`, `Check Out`, `Pulang`, `Keluar`, `1` = pulang; `Break Out/In`, `2`, `3` = istirahat (diabaikan); `OT In/Out`, `4`, `5` = tap biasa. Status lain → tap biasa + peringatan.
- **Format per hari**: `Tanggal` + `Scan Masuk`/`Masuk`/`Clock In` + `Scan Pulang`/`Pulang`/`Clock Out`. Kolom `Scan Masuk` diutamakan di atas `Jam Masuk` (pada banyak laporan mesin, `Jam Masuk` = jadwal, bukan jam asli).
- Tanggal: `03/09/2026`, `03-09-2026`, `2026-09-03`, `3 Sep 2026`, `Kamis, 03/09/2026 08:12:33`, angka seri Excel. Jam: `08.12`, `8:12:33`, `08.12.33`, `8:12 PM`.
- Encoding: UTF-8, UTF-16 (umum di ekspor mesin), Windows-1252. Pemisah `,` `;` tab `|`.

## Status harian di rekap
`hadir`, `hadir di hari libur`, `izin`, `sakit`, `cuti`, `alpa`, `dinas`, `tanpa keterangan` (hari kerja tanpa tap & tanpa keterangan — ditanyakan ke pemilik), `belum absen` (hari ini, sebelum jadwal pulang), `libur`.

## Jenis masalah (`masalah[].jenis`)
| Jenis | Tingkat | Arti |
|---|---|---|
| `pulang_sebelum_masuk` | salah | Jam pulang ≤ jam masuk; jam kerja tidak dihitung |
| `durasi_tidak_wajar` | salah | Masuk–pulang > 18 jam |
| `tap_tidak_lengkap` | salah | Hanya masuk atau hanya pulang |
| `lembur_saat_tidak_hadir` | salah | Lembur di hari izin/sakit/cuti/alpa → tidak dihitung |
| `lembur_libur_melebihi_aturan` | salah | Di atas tangga Pasal 31 → tidak dihitung |
| `tap_di_luar_shift` | cek | Tap jauh dari jadwal (> 4 jam sebelum masuk / > 8 jam setelah pulang) |
| `masuk_ganda` / `pulang_ganda` | cek | Lebih dari satu tap masuk/pulang berjauhan |
| `keterangan_dan_tap` | cek | Ada izin/sakit tetapi juga ada tap |
| `lembur_tanpa_absen` / `lembur_lebih_dari_absen` | cek | Lembur disetujui tidak sesuai jam absen (tetap dihitung) |
| `lembur_lebih_4_jam` / `lembur_lebih_18_jam_seminggu` | cek | Melebihi Pasal 26 (tetap dihitung) |
| `tap_ganda`, `golongan_jabatan_tertentu`, `upah_belum_diisi`, `lembur_masa_depan` | info | Informasi |

## CSV untuk `slip-gaji-bpjs`
- Tanpa `--gabung`: kolom `nama;jabatan;ptkp;gaji_pokok;tunjangan_tetap;tunjangan_tidak_tetap;lembur_hari_kerja;lembur_hari_libur;kode_absensi;hari_hadir;hari_alpa;terlambat_menit`. `ptkp` & gaji dikosongkan (wajib diisi dulu).
- Dengan `--gabung file-gaji.csv`: kolom `lembur_hari_kerja` (mis. `2+1,5`) dan `lembur_hari_libur` (mis. `8+6p`, `p` = libur resmi di hari kerja terpendek) diisi ke file gaji yang sudah ada, dicocokkan lewat nama (atau kode di kolom `nik`). Baris yang sudah berisi `lembur_rp` tidak diisi jam (mencegah dobel).
- `slip-gaji-bpjs` memakai satu `--hari-kerja` per jalan → ekspor terpisah per pola (`--pola 5` / `--pola 6`).
