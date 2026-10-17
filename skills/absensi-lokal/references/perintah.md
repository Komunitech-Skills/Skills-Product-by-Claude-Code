# Daftar perintah `scripts/absensi.py`

Format umum: `python3 scripts/absensi.py <perintah> [opsi] [--db PATH] [--json]` (Windows: `python`/`py`).
Perintah bertanda **(tulis)** hanya pratinjau sampai ditambah `--ya` setelah pengguna setuju.

| Perintah | Kegunaan | Opsi penting |
|---|---|---|
| `init` (tulis) | Buat database + shift `REG` 08.00–17.00 | — |
| `info` | Lokasi database, jumlah karyawan/tap, shift, pengaturan | — |
| `backup` | Salinan bertanggal ke `backup-absensi/` | — |
| `atur` (tulis) | Pengaturan | `--toleransi <menit>` (kelonggaran telat, default 0), `--jeda-duplikat <menit>` (default 5), `--nama-usaha` |
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
| `rekap-cepat <file>` | Rekap langsung dari file mesin absen (dihitung di memori; tidak ada yang dibuat atau disimpan). Bila buku absensi sudah ada dan berisi karyawan, isinya dipakai (hanya dibaca) | `--daftar "Andi=1; Sari=2"` (nama=nomor ID di mesin; kosong = dibaca dari isi file), `--hari-kerja 5|6`, `--masuk`, `--pulang`, `--istirahat`, `--pulang-hari-pendek`, `--toleransi`, `--libur 2026-09-14,...`, `--bulan` atau `--dari/--sampai` (kosong = dibaca dari isi file), `--kolom-*`, `--format-tanggal`, `--csv`, `--csv-harian` |
| `harian` | Laporan satu hari | `--tanggal` (default hari ini), `--karyawan` |

## `rekap-cepat` (balasan pertama untuk file mesin + permintaan rekap)
- **Buku belum ada** (atau belum berisi karyawan aktif): satu jadwal kerja (bawaan 08.00–17.00, istirahat 60 menit, 5 hari kerja, kelonggaran telat 0 menit, tanpa tanggal merah) yang bisa diubah lewat opsi; karyawan dari `--daftar` atau dari kolom ID/Nama di file. Pola 6 hari: jam pulang Sabtu lewat `--pulang-hari-pendek` (tanpa itu Sabtu dihitung hari biasa dan ditandai anggapan). Shift malam, beberapa jadwal, lembur, dan upah → pakai alur buku absensi (`init`, `karyawan`, `impor-absen`, `rekap`).
- **Buku sudah ada** (`dari_buku: true`): buku disalin ke memori (hanya dibaca, ukuran dan waktu ubah file tidak berubah) dan dipakai apa adanya: karyawan, jadwal kerja, kelonggaran telat, libur, izin/sakit/cuti, dan lembur disetujui; hasilnya sama dengan `rekap` dari buku untuk periode itu. Hanya `--toleransi` dan `--libur` yang menimpa/menambah (untuk rekap ini saja). Jam/hari kerja yang berbeda dari jadwal tersimpan tidak dipakai dan dicatat di `catatan_file`. `--daftar` yang tidak cocok dengan karyawan di buku dicatat sebagai "belum ada di buku absensi". Orang di file yang tidak dikenal dilaporkan dan ditanyakan. File yang catatannya sudah ada semua di buku diberi catatan "sudah ada", tanpa pertanyaan.
- Periode dibaca dari isi file: satu bulan penuh → rekap bulan itu; sebagian bulan atau lintas bulan (≤ 62 hari) → dari tanggal pertama sampai terakhir di file; > 62 hari → bulan terakhir. `--bulan` atau `--dari/--sampai` menimpa. Bila yang dihitung tidak mencakup seluruh isi file, `catatan_file` memuat "File berisi catatan dari ... sampai ..., tetapi yang saya hitung hanya ...".
- Field JSON: `pesan` (daftar pesan siap kirim: pembuka + `teks` + pertanyaan, dipecah per ≤ 3.800 karakter di batas antar-karyawan; kirim berurutan), `balasan` (versi utuh sebelum dipecah), `teks` (rekap + "Yang saya pakai untuk menghitung" + catatan file + tanggal kosong untuk semua karyawan), `pertanyaan` (maks. 3: Sabtu pulang lebih awal? / libur bersama? / orang tak dikenal (buku sudah ada) / hari tanpa catatan = izin, sakit, cuti, alpa? atau jam pulang yang kosong / penutup: tawaran menyimpan (buku belum ada) atau memasukkan file ke buku (buku sudah ada dan ada catatan baru)), `asumsi` (hanya yang memakai nilai bawaan), `pengaturan_dipakai`, `dari_buku`, `karyawan_terdeteksi` + `daftar_siap_pakai` (untuk `karyawan tambah --id-mesin` bila pengguna setuju menyimpan), `tanggal_kosong_semua`, `catatan_file`, `dibaca` (`catatan`, `sudah_ada`, `dari`, `sampai`), `tersimpan: false`.
- Kode karyawan internal (A01, ...) tidak muncul di teks (juga di `rekap` biasa, kecuali ada nama kembar).
- `rekap` dan `harian` juga mengembalikan `teks` dan `pesan` di JSON.

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
| `pulang_lewat_jadwal`, `masuk_libur_tanpa_lembur` | info | Pulang > 60 menit lewat jadwal / masuk di hari libur **tanpa** lembur disetujui — tidak dihitung lembur |
| `pengingat_makan_pasal_29` | info | Lembur ≥ 4 jam: makan-minum ≥ 1.400 kkal (Pasal 29) |

## CSV untuk `slip-gaji-bpjs`
- Tanpa `--gabung`: kolom `nama;jabatan;ptkp;gaji_pokok;tunjangan_tetap;tunjangan_tidak_tetap;lembur_hari_kerja;lembur_hari_libur;kode_absensi;hari_hadir;hari_alpa;terlambat_menit`. Gaji & tunjangan diisi dari database absensi; pekerja upah harian diisi upah sebulan konversi (× 25 / × 21, Pasal 33) + catatan. `ptkp` wajib diisi dulu.
- Dengan `--gabung file-gaji.csv`: kolom `lembur_hari_kerja` (mis. `2+1,5`) dan `lembur_hari_libur` (mis. `8+6p`, `p` = libur resmi di hari kerja terpendek) diisi ke file gaji yang sudah ada, dicocokkan lewat nama (atau kode di kolom `nik`). Baris yang sudah berisi `lembur_rp` tidak diisi jam (mencegah dobel).
- `slip-gaji-bpjs` memakai satu `--hari-kerja` per jalan → ekspor terpisah per pola (`--pola 5` / `--pola 6`).

## Script terpisah: `scripts/upah_harian.py` (pekerja harian lepas, tanpa database)
`python3 scripts/upah_harian.py [--pola 6|5] [--periode LABEL] --pekerja "Nama; tarif=120rb; hari=6; setengah=1; lembur=2+1; lembur-libur=3; tarif-lembur=15rb; tambahan=20rb; potongan=200rb; pola=6" [--pekerja ...] [--file pekerja.csv] [--json]`
- Upah hadir = tarif × hari + tarif × ½ × setengah (dibulatkan ke rupiah terdekat). Lembur minimum = jam setara × (tarif × 25 atau × 21) ÷ 173, dibulatkan sekali per pekerja. `tarif-lembur` → lembur dibayar = jam × tarif pemilik (peringatan bila < minimum). Total = hadir + lembur dibayar + tambahan − potongan.
- Field JSON per pekerja: `upah_hadir`, `rumus_upah_hadir`, `lembur_jam`, `lembur_jam_setara`, `upah_sejam`, `lembur_minimum_pp35`, `lembur_dibayar`, `total_dibayar`, `total_versi_minimum_pp35`, `peringatan`; plus `total_dibayar`, `total_versi_minimum_pp35`, `teks`.
- Peringatan: lembur > 4 jam/hari atau > 18 jam/minggu (Pasal 26), potongan > upah, upah harian > Rp450.000 (PPh 21 harian mungkin terutang). Lembur libur melebihi tangga Pasal 31 → ditolak.
- Uji: `python3 tests/uji_upah_harian.py`.
