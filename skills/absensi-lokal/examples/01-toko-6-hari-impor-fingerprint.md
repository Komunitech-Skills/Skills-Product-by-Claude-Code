# 01 — Toko 6 karyawan (pola 6 hari), impor log mesin fingerprint → rekap Agustus + lembur

**Skenario:** normal. Toko fiktif "Toko Maju Jaya", 6 karyawan, kerja Senin–Sabtu (Senin–Jumat 08.00–16.00 istirahat 1 jam, Sabtu 08.00–13.00 = hari kerja terpendek), libur Minggu dan 17 Agustus. Pemilik baru mulai memakai alat ini dan mengirim file ekspor mesin fingerprint (format log per tap, gaya ZKTeco) untuk bulan Agustus 2026.

Isi file uji (`log-agustus.csv`, 304 baris, dibuat penguji): tap ganda (Andi 03/08, dua kali C/In berjarak 49 detik), lupa tap pulang (Sari 12/08), tap istirahat `Break Out/Break In` (Budi 06/08), tap pulang dobel 2 menit (Rudi 10/08), Dewi tidak tap 20–21/08, Joko pulang 19.10 pada 25/08 **tanpa** perintah lembur, dan 1 tap dari ID 9 "Teknisi" yang tidak terdaftar. Semua nama fiktif.

```
No.,AC-No.,Nama,Waktu,Status
1,4,Dewi,01/08/2026 07:52:41,C/In
...
15,1,Andi,03/08/2026 07:57:46,C/In
16,1,Andi,03/08/2026 07:58:35,C/In
...
```

## Input pengguna (persis)

> Pak, ini file dari mesin absen toko bulan Agustus. Tolong direkap ya. Karyawan 6 orang, masuk Senin–Sabtu, jam 8 sampai jam 4, Sabtu sampai jam 1. Tanggal 17 libur. Telat lebih dari 5 menit baru dihitung. Lembur yang saya suruh: Andi tgl 5 dua jam, Joko Minggu tgl 9 delapan jam (stok opname), Sari Sabtu tgl 15 satu setengah jam, Rudi tgl 17 lima jam antar barang. Hitungkan uang lemburnya juga. Gaji: Andi 3,5jt + tunjangan 300rb, Sari 3,4jt + 300rb, Budi 3,3jt, Dewi 4jt + 500rb, Joko 3,3jt + 200rb, Rudi 3jt + tunjangan tetap 300rb + uang jalan rata-rata 1,5jt. ID di mesin 1 sampai 6 urut nama tadi.

## Output (mengikuti SKILL.md)

**Langkah agent (ringkas):** `info` → database belum ada → karena pengguna sudah memberi data lengkap, agent cukup mengonfirmasi lokasi penyimpanan → `init` → `init --ya` → `shift tambah --kode TOKO --masuk 08.00 --pulang 16.00 --istirahat 60 --pulang-hari-pendek 13.00` → `karyawan impor karyawan.csv` (6 baris, pola 6, hari pendek Sabtu, id mesin 1–6, Rudi dengan tunjangan tidak tetap 1.500.000) → `atur --toleransi 5` → `libur tambah --tanggal 2026-08-17` → semuanya dipratinjau lalu disimpan setelah pengguna membalas "ya".

**Pesan 1 — pratinjau impor (sebelum disimpan):**

```
Saya akan memasukkan data mesin absen (belum disimpan):
- File: log-agustus.csv (format log per tap)
- Pemetaan kolom: id <- 'AC-No.', nama <- 'Nama', waktu <- 'Waktu', status <- 'Status'
- Cara baca tanggal: Sabtu 1 Agustus 2026 jam 07.52 (masuk) | Sabtu 1 Agustus 2026 jam 07.55 (masuk) ...
  (format HARI/BULAN/TAHUN, pasti karena ada tanggal di atas 12)
- Tap baru: 301 | sudah ada: 0 | Rentang 01/08/2026 s.d. 31/08/2026
- Per karyawan: Andi 51, Budi 50, Dewi 46, Joko 52, Rudi 53, Sari 49
- Diabaikan: tap istirahat (keluar/kembali istirahat) 2
Catatan: 1 baris dari ID 9 / nama "Teknisi" tidak terdaftar, tidak diimpor. Kalau itu karyawan,
sebutkan namanya; nanti file yang sama bisa diimpor ulang tanpa dobel.
Simpan? Balas "ya".
```

**Pesan 2 — pratinjau lembur disetujui (dari `lembur --file lembur-agustus.csv`):**

```
Saya akan mencatat lembur yang DISETUJUI (belum disimpan):
- Andi, Rabu 05/08: 2 jam, hari kerja (Pasal 31 ayat (1)) = 3,5 jam setara ≈ Rp 76.879
- Joko, Minggu 09/08: 8 jam, hari istirahat pola 6 hari (Pasal 31 ayat (2) huruf a:
  7 jam x 2 + 1 jam x 3) = 17 jam setara ≈ Rp 343.931
- Sari, Sabtu 15/08: 1,5 jam, hari kerja = 2,5 jam setara ≈ Rp 53.468
- Rudi, Senin 17/08 (libur resmi, bukan hari kerja terpendek): 5 jam x 2 = 10 jam setara ≈ Rp 208.092
  (dasar upah Rudi = 75% x seluruh upah Rp 4.800.000 = Rp 3.600.000, karena gaji pokok +
  tunjangan tetap < 75% — PP 35/2021 Pasal 32 ayat (4))
Catatan: lembur 8 jam Joko ≥ 4 jam → perusahaan wajib memberi makan-minum min. 1.400 kkal (Pasal 29).
Simpan? Balas "ya".
```

**Pesan 3 — rekap (teks script apa adanya) + pertanyaan:**

```
REKAP ABSENSI AGUSTUS 2026 - Toko Maju Jaya (fiktif)
Periode 01/08/2026-31/08/2026 | toleransi terlambat 5 menit
Libur resmi: 17/08/2026 Hari Kemerdekaan RI

1. Andi (T01) - Kasir
   Hadir 25 dari 25 hari kerja
   Terlambat 2x (12 menit) | Pulang cepat 0x (0 menit)
   Jam kerja 169 jam 17 menit
   Lembur disetujui: hari kerja 2 jam, hari libur 0 jam (setara 3,5 jam) -> Rp 76.879

2. Sari (T02) - Kasir
   Hadir 25 dari 25 hari kerja
   Terlambat 0x (0 menit) | Pulang cepat 0x (0 menit)
   Jam kerja 161 jam 55 menit (+1 hari data tidak lengkap, belum dihitung)
   Lembur disetujui: hari kerja 1,5 jam, hari libur 0 jam (setara 2,5 jam) -> Rp 53.468

3. Budi (T03) - Gudang
   Hadir 25 dari 25 hari kerja
   Terlambat 5x (1 jam 29 menit) | Pulang cepat 0x (0 menit)
   Jam kerja 165 jam 51 menit

4. Dewi (T04) - Admin
   Hadir 23 dari 25 hari kerja | Tanpa keterangan 2
   Terlambat 1x (6 menit) | Pulang cepat 1x (30 menit)
   Jam kerja 152 jam 41 menit

5. Joko (T05) - Gudang
   Hadir 25 dari 25 hari kerja | masuk di hari libur 1
   Terlambat 2x (12 menit) | Pulang cepat 0x (0 menit)
   Jam kerja 178 jam 35 menit
   Lembur disetujui: hari kerja 0 jam, hari libur 8 jam (setara 17 jam) -> Rp 343.931

6. Rudi (T06) - Sopir
   Hadir 25 dari 25 hari kerja | masuk di hari libur 1
   Terlambat 2x (12 menit) | Pulang cepat 0x (0 menit)
   Jam kerja 172 jam 22 menit
   Lembur disetujui: hari kerja 0 jam, hari libur 5 jam (setara 10 jam) -> Rp 208.092

Total upah lembur: Rp 682.370

PERLU DICEK (1):
- Sari 12/08/2026: hanya ada jam masuk (07.55); jam pulang tidak tercatat

Hari kerja tanpa absen & tanpa keterangan (mohon dikonfirmasi: izin/sakit/cuti/alpa?):
- Dewi: 20/08, 21/08

Upah lembur: PP 35/2021 Pasal 31-32 (upah sejam = 1/173 x upah sebulan), hanya dari lembur yang
disetujui, dibulatkan ke rupiah terdekat. Alat bantu hitung, bukan nasihat hukum; kasus khusus
tanyakan ke Disnaker/konsultan.
```

Pertanyaan agent (satu pesan):
1. Sari 12/08 pulang jam berapa (lupa tap)?
2. Dewi 20–21/08 tidak absen: izin, sakit, cuti, atau alpa?
3. Info: Joko 25/08 pulang 19.10 tetapi tidak ada di daftar lembur yang Bapak setujui, jadi **tidak** dihitung lembur (PP 35/2021 Pasal 28: lembur harus ada perintah + persetujuan). Kalau memang Bapak suruh lembur, sebutkan jamnya.

**Pengguna:** "Sari pulang jam 4 lewat 5. Dewi sakit, ada surat dokter. Joko itu nunggu jemputan, bukan lembur."

→ `keterangan --karyawan Dewi --jenis sakit --tanggal 2026-08-20 --sampai 2026-08-21 --catatan "surat dokter"` dan `catat --karyawan Sari --tanggal 2026-08-12 --pulang 16.05` (pratinjau → "ya" → `--ya`) → rekap ulang + `--csv rekap-agustus.csv --csv-harian rincian-agustus.csv`:

```
2. Sari (T02) - Kasir
   Hadir 25 dari 25 hari kerja
   Terlambat 0x (0 menit) | Pulang cepat 0x (0 menit)
   Jam kerja 169 jam 4 menit
   ...
4. Dewi (T04) - Admin
   Hadir 23 dari 25 hari kerja | Sakit 2
   ...
Total upah lembur: Rp 682.370
File: rekap-agustus.csv, rincian-agustus.csv
```

Cuplikan `rincian-agustus.csv` (pemisah `;`, bisa dibuka Excel):
```
kode;nama;tanggal;hari;jenis_hari;status;jadwal_masuk;jadwal_pulang;masuk;pulang;terlambat_menit;pulang_cepat_menit;jam_kerja;lembur_disetujui_jam
T01;Andi;03/08/2026;Senin;kerja;hadir;08.00;16.00;07.57;16.07;;;7:09;
T04;Dewi;28/08/2026;Jumat;kerja;hadir;08.00;16.00;07.54;15.30;;30;6:35;
T05;Joko;09/08/2026;Minggu;istirahat;hadir di hari libur;08.00;16.00;07.58;17.05;;;8:06;8
T05;Joko;25/08/2026;Selasa;kerja;hadir;08.00;16.00;07.53;19.10;;;10:17;
T06;Rudi;17/08/2026;Senin;libur-resmi;hadir di hari libur;08.00;16.00;08.00;14.05;;;5:04;5
```

## Catatan penguji
- **Semua angka cocok** dengan hitungan independen penguji (`/tmp/uji-absensi-lokal/a/verif_a.py`, membaca CSV mentah tanpa mengimpor kode skill): hadir, hari terjadwal (25 = 31 − 5 Minggu − 17 Agustus), terlambat kali/menit, pulang cepat, menit kerja (termasuk Sabtu tanpa potongan istirahat), hari tidak lengkap, daftar tanpa keterangan, dan rupiah lembur per karyawan. Contoh: Rudi 10 × 3.600.000 ÷ 173 = 208.092,49 → Rp 208.092; total Rp 682.370.
- Impor ulang file yang sama: `Tap baru: 0 | sudah ada sebelumnya: 301` — tidak dobel.
- Bagus: tap ganda & tap istirahat dibuang, ID asing dilaporkan (tidak ditebak), lembur tanpa perintah (Joko 25/08) tidak dihitung, aturan 75% Pasal 32 ayat (4) diterapkan otomatis.
- Kurang: (1) teks rekap tidak menyebut dasar upah 75% Rudi — hanya ada di JSON (`dasar_upah_keterangan`), agent harus menambahkannya sendiri; (2) pengingat Pasal 29 (makan ≥ 1.400 kkal) di atas ditulis agent dari SKILL.md, script tidak mengeluarkannya; (3) Joko 25/08 pulang 3 jam lewat jadwal tanpa lembur disetujui tidak muncul sebagai info sama sekali — aplikasi absensi berbayar biasanya menandai "kelebihan jam tanpa SPL"; (4) label karyawan saat impor tidak menampilkan tunjangan tidak tetap Rudi.
