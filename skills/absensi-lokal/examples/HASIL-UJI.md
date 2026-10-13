# HASIL UJI — absensi-lokal v1.0.0

- **Tanggal:** 2026-09-23 (selesai 24/09 dini hari)
- **Penguji:** agent penguji independen (simulasi, Claude Code) — bukan pembuat skill; hanya membaca folder `skills/absensi-lokal/`, `pedoman kurasi Komunitech`, dan brief uji.
- **Lingkungan:** Linux, Python 3.11, semua database uji di `/tmp/uji-absensi-lokal/` (lewat `--db` / `KOMUNITECH_ABSENSI_DB`), tidak menyentuh `~/KomunitechData`.
- **Regresi bawaan:** `tests/uji_regresi.py` → 29 tes OK.

## Ringkasan skenario

| # | Skenario | Hasil | Angka diverifikasi independen |
|---|---|---|---|
| 01 | Toko 6 karyawan pola 6 hari, impor log fingerprint (tap ganda, lupa tap pulang, tap istirahat, ID asing), lembur hari kerja / Minggu / Sabtu hari pendek / 17 Agustus, aturan 75% | Lulus | Ya — `verif_a.py` (semua kolom rekap & rupiah cocok, total Rp 682.370) |
| 02 | Pabrik pola 5 hari, shift malam 22.00–06.00 lintas bulan, format per hari, upah harian ×21, >4 jam/hari, >18 jam/minggu, jam `2:15`, CSV ke slip-gaji-bpjs | Lulus | Ya — `verif_b.py` + dijalankan ke `payroll.py` slip-gaji-bpjs: lembur sama persis |
| 03 | Klinik, catat lewat chat, jam 25.10 ditolak, laporan harian Telegram, `--gabung` file gaji | Lulus | Ya (manual) + CLI OpenClaw 2026.9.5 asli untuk sintaks |
| 04 | "hitung lembur Budi bulan ini" | Lulus (dengan catatan) | Ya (manual) |
| 05 | GPS diam-diam & potong gaji otomatis | Lulus sebagian (GPS diatur skill; potong gaji tidak diatur skill) | — |
| A/B | Skenario 01 tanpa skill | Skill jelas lebih baik (tanpa skill kurang bayar Rp 17.341, hari Minggu dihitung hadir, lupa tap hilang) | Ya |
| Pesaing | attendance-sheet (ClawHub), Frappe HR, siwajah | Skill kita menang telak untuk konteks Indonesia | — |

## Verifikasi hukum independen (PP 35/2021, teks salinan JDIH Kemnaker)
Penguji membaca sendiri Pasal 21, 22, 23–25, 26, 27, 28, 29, 30, 31 ayat (1)–(3), 32, 33 dan Penjelasan Pasal 26 ayat (2). **Semua cocok** dengan `references/dasar-hukum-lembur.md` dan konstanta/logika script:
- Pasal 31(1) 1,5×/2×; 31(2)a 7×2, 1×3, 3×4 (maks 11 jam); 31(2)b 5×2, 1×3, 3×4 (maks 9) hanya untuk **libur resmi** di hari kerja terpendek pola 6; 31(3) 8×2, 1×3, 3×4 (maks 12) — `TANGGA_LIBUR` & `jenis_hari` benar.
- Pasal 32(2) 1/173; 32(3) 100% pokok+tetap; 32(4) 75% bila ada tunjangan tidak tetap dan pokok+tetap < 75% — benar. Pasal 33(1) ×25/×21 — benar. Pasal 26(2) batas tidak berlaku di hari istirahat/libur — benar (hanya hari kerja dicek).
- Tabel jam setara di references dicek ulang baris demi baris: benar.
- Tidak ditemukan perbedaan. Catatan kecil: Pasal 34 (lembur "dengan sebutan lain" yang sama/lebih baik tetap berlaku) tidak disebut; sudah tercakup kalimat "PP/PK/PKB yang lebih baik ikuti itu".

## Verifikasi angka (script penguji, tidak mengimpor kode skill)
- `edge.py`: 207 kasus `lembur` pratinjau (9 jenis hari × 23 nilai jam: 0,25 … 12,5, termasuk `1:45`) — jam setara & rupiah **0 beda** dengan rumus manual (Fraction); batas tangga (11,5 jam pola 6, 9,5 jam "6p", >12 jam) ditolak dengan benar.
- Pembulatan setengah ke atas: 0,5 × 3.460.173 ÷ 173 = 10.000,5 → Rp 10.001 ✓. Total dibulatkan sekali per karyawan (sesuai standar library: nominal non-PPN ke rupiah terdekat).
- Tahun kabisat: `29/02/2028` diterima, `29/02/2027` ditolak; shift malam 29/02 21.55 → 01/03 08.10 = 9 jam 15 menit, tidak dobel di rekap Maret; 31/12/2027 22.00 → 01/01/2028 06.00 = 7 jam ✓.
- Pulang dini hari tanpa `--tanggal` pada shift malam otomatis ke shift kemarin ✓.

## Data rusak
| Input | Hasil |
|---|---|
| CSV kosong / hanya biner / `.xls` / `.xlsx` palsu | Pesan jelas, exit 1 ✓ |
| UTF-16 dengan BOM | Terbaca ✓ |
| UTF-16 **tanpa** BOM | Ditolak sebagai "berisi data biner" (pesan menyesatkan) ✗ ringan |
| Kolom waktu hilang | Pesan + saran `--kolom-*` ✓ |
| Tanggal campur d/m & m/d | Ditolak "format tidak konsisten" ✓; semua ≤ 12 → dibaca d/m + peringatan ✓ |
| Jam 25:61, 31/02 | Baris rusak dilaporkan, baris lain tetap ✓ |
| Karyawan tak dikenal / ID kosong | Dilaporkan, tidak diimpor ✓ |
| Impor ulang file sama | `Tap baru: 0 | sudah ada 301` ✓ |
| Tap masa depan | Tidak diimpor + peringatan ✓ |
| File hanya judul kolom | `ok: true`, 0 tap, peringatan urutan tanggal yang tidak relevan ✗ ringan |
| DB tidak ada / folder tidak ada / file bukan DB | Pesan jelas ✓ |
| **DB terkunci** proses lain | Setelah 5 detik: "File r.db **bukan database absensi-lokal (atau rusak)**" ✗ sedang |
| Tujuan `--csv` tidak bisa ditulis (folder, path tak ada; di Windows: file sedang dibuka Excel) | **Traceback Python**, exit 0 ✗ sedang; `init --ya --db` ke folder tak bisa dibuat juga traceback |

## Keamanan & privasi
- Tidak ada `socket/urllib/http/subprocess/eval/exec`; hanya `sqlite3`, file lokal, dan `unlink` backup sementara miliknya sendiri. Tidak ada kredensial/token. Tidak ada prompt injection di SKILL.md/references.
- Tulis selalu pratinjau → `--ya`; backup otomatis sebelum impor/hapus. ID mesin 16 digit (mirip NIK) ditolak. Tidak ada kolom NIK/rekening/alamat/HP di skema. Catatan: `--gabung` menyalin utuh file gaji pengguna (bisa berisi kolom `nik`) ke CSV keluaran — wajar, tapi tidak disimpan di DB.
- Jadwal OpenClaw hanya `harian`/`rekap` (baca). Telegram default, WhatsApp hanya nomor terpisah + persetujuan tertulis — sesuai keputusan pemilik.

## Skor per kriteria

| Kriteria | Skor | Alasan |
|---|---|---|
| Pemicu (description) | 9 | Spesifik, ID+EN, menyebut kapan pakai & lempar ke slip-gaji-bpjs |
| Kemudahan awam | 8 | Satu kalimat cukup; pratinjau berbahasa sederhana; setup awal 5 pertanyaan sekali |
| Kualitas output | 8 | Rekap siap tempel, CSV Excel, ekspor slip-gaji kompatibel; kurang grid Excel & info "pulang lewat jadwal tanpa SPL" |
| Akurasi (angka/fakta) | 9 | 0 selisih pada semua verifikasi independen; pasal cocok; minus peringatan 18 jam/minggu lintas bulan |
| Penanganan input kurang | 8 | Bertanya sekali; tetapi rekap tanpa data sama sekali menyarankan konfirmasi alpa 20 hari |
| Penanganan di luar cakupan | 7 | GPS/aplikasi HP diatur; denda/potong gaji telat tidak diatur di SKILL.md |
| Keamanan | 9 | Lokal, tanpa jaringan, konfirmasi, backup, penolakan NIK |

## SKOR AKHIR: **8 / 10 — LULUS**
Tidak ada cacat berat: semua angka uang & jam benar, dasar hukum cocok dengan teks resmi, impor tidak dobel, data ganjil dilaporkan. Skor tidak 9 karena beberapa jalur error masih crash/menyesatkan dan dua celah kepatuhan/UX di bawah.

## Daftar cacat & saran perbaikan

**BERAT:** tidak ada.

**SEDANG**
1. **Crash saat menulis CSV** (`tulis_csv`, baris ±487–496; juga `cmd_init` `db.parent.mkdir` baris ±1140): `IsADirectoryError`/`PermissionError`/`FileNotFoundError` keluar sebagai traceback dengan exit code 0. Di Windows ini terjadi setiap kali file rekap lama masih terbuka di Excel. Saran: bungkus `open()`/`mkdir()` dengan `except OSError as e: raise Gagal("File %s tidak bisa ditulis (sedang dibuka di Excel?/folder tidak ada). Tutup filenya atau pilih nama lain.")`, dan di `main()` tangkap `OSError` umum → JSON `ok:false`.
2. **DB terkunci dilaporkan sebagai "rusak"** (`buka()` baris ±577–581 menangkap `sqlite3.DatabaseError`, termasuk `OperationalError: database is locked`). Pengguna awam bisa mengira datanya rusak lalu menghapus/menimpa file. Saran: tangkap `sqlite3.OperationalError` dengan "locked" lebih dulu dan lempar pesan "Database sedang dipakai proses lain (mis. jadwal OpenClaw), coba lagi sebentar"; pertimbangkan `sqlite3.connect(..., timeout=15)`.
3. **Batas 18 jam/minggu (Pasal 26) terlewat untuk minggu yang terbelah akhir bulan** (`hitung_lembur` baris ±996–1031 hanya menjumlah lembur dalam periode rekap). Uji: 31/08 4 jam + 1–4/09 4 jam/hari = 20 jam di minggu ISO 36 → rekap Agustus dan September tidak memperingatkan; hanya `--dari 2026-08-31 --sampai 2026-09-06` yang memperingatkan. Terjadi hampir tiap bulan. Saran: untuk cek mingguan, ambil lembur dari Senin minggu pertama s.d. Minggu minggu terakhir yang menyentuh periode; tambahkan juga cek total minggu di pratinjau `_catat_lembur` / `lembur --file`.

**RINGAN**
4. Rekap tanpa satu pun tap di periode (contoh 04) menampilkan 20 tanggal "mohon dikonfirmasi: izin/sakit/cuti/alpa?" — tambahkan deteksi "belum ada data absen periode ini, sudah impor file mesin?" di `cmd_rekap`, dan di SKILL.md langkah D.2: jangan tanyakan alpa bila belum ada data mesin.
5. SKILL.md "Kapan TIDAK digunakan" belum mengatur **denda/potong gaji otomatis karena telat** dan pemantauan lokasi diam-diam (privasi, UU 27/2022). Tambahkan satu baris + rujukan PP 36/2021 (denda/pemotongan hanya bila diatur PK/PP/PKB, ada batas total potongan) → arahkan ke `surat-peringatan-karyawan` / `potongan_lain` di `slip-gaji-bpjs`.
6. Pengingat Pasal 29 (makan ≥ 1.400 kkal bila lembur ≥ 4 jam) diklaim di SKILL.md baris 133 tetapi tidak dikeluarkan script — tambahkan sebagai `info` di `hitung_lembur`/pratinjau lembur.
7. Dasar upah 75% (Pasal 32 ayat (4)) dan ×21/×25 (Pasal 33) hanya ada di JSON; tampilkan di teks rekap/pratinjau lembur (mis. "dasar Rp 3.600.000 = 75% × Rp 4.800.000"). Label karyawan juga tidak menampilkan tunjangan tidak tetap.
8. `--csv-gaji` tanpa `--gabung` mengosongkan `gaji_pokok/tunjangan` padahal sudah ada di database; untuk pekerja **upah harian** tidak ada catatan bahwa `gaji_pokok` di slip harus = upah harian × 21/25 agar rupiah lembur sama. Saran: isi otomatis dari DB (dan untuk upah harian isi upah sebulan konversi + catatan).
9. Tidak ada info untuk "pulang jauh lewat jadwal tanpa lembur disetujui" (Joko 25/08 pulang 19.10) — tambahkan `info`/`cek` "kelebihan jam X tanpa lembur disetujui" (tetap tidak dihitung upah).
10. UTF-16 tanpa BOM ditolak sebagai "biner" (`baca_tabel` baris ±415–420): deteksi pola byte nol berselang → decode `utf-16-le/be`. File hanya berisi judul kolom → beri pesan "tidak ada baris data" alih-alih peringatan urutan tanggal.
11. `references/openclaw-jadwal.md`: contoh cron `1-6` cocok pola 6 hari; sebutkan `1-5` untuk pola 5 hari. Catatan "Sudah ada 3 tap dari mesin di sekitar tanggal ini" pada `catat` menghitung tap hari berikutnya juga (membingungkan).

## Yang belum diuji
- Uji platform asli (OpenClaw/Codex/Claude Code/Cursor) oleh manusia; `bash scripts/uji_openclaw.sh` tidak dijalankan penguji (di luar izin tulis). Pengiriman Telegram sungguhan tidak diuji (butuh token bot).
- Windows (path, encoding konsol, Excel mengunci file) belum diuji langsung.
- File `.xlsx` asli dari mesin merek tertentu (hanya CSV & jalur error XLSX yang diuji).

`platform_teruji` yang jujur: `claude-code (simulasi agent)`.

## Catatan koordinator — v1.0.1
3 cacat SEDANG + semua cacat RINGAN diperbaiki pembuat; 38/38 tes regresi lulus (dicek ulang koordinator). Pengingat makan Pasal 29 memakai ambang teks pasal (lembur ≥ 4 jam). Status tetap lulus (perbaikan disertai tes regresi, tidak mengubah angka lembur yang sudah diverifikasi).
