# HASIL UJI — laporan-harian-usaha 1.0.0

- **Tanggal:** 2026-09-23 (dijalankan dengan jam sistem 24 Sep 2026)
- **Penguji:** agent penguji independen (simulasi, Claude Code). Bukan pembuat skill.
- **Lingkungan:** Linux, Python 3.11, zona komputer UTC (juga diuji `TZ=Asia/Jakarta` dan `TZ=Asia/Makassar`), OpenClaw 2026.9.5 (CLI asli, HOME sementara, Gateway lokal `--dev --bind loopback`).
- **Data uji:** dibangun sendiri di `/tmp/uji-lhu/` dengan menjalankan script **asli** keempat alat. Kafe fiktif, 7–24 Sep 2026: 155 nota jual, 4 void, 3 retur, mode PBJT 10%, 17 kali tutup kasir (3 dengan selisih), 2 nota lewat tengah malam, 1 hari tanpa penjualan. Buku-stok mengimpor ekspor kasir kecuali 2 hari, 4 SKU minus, 1 barang rusak. 5 karyawan, 2 shift, pola 6 hari: terlambat, izin, sakit, alpa, masuk hari libur, lembur disetujui, pulang lewat jadwal tanpa persetujuan, pulang lewat tengah malam. DAFTAR.csv 8 baris dengan nama, HP, dan NIK fiktif, serta nominal "1.250.000". Script uji: `bangun.py`, `verif.py`, `uji_ro.py` (berkas kerja, di luar repo).
- Uji regresi bawaan `tests/uji_regresi.py`: **31/31 OK**. `scripts/validate.py`: lolos.

## Ringkasan skenario
| # | Skenario | Hasil |
|---|---|---|
| 00 | A/B tanpa skill vs dengan skill | Dengan skill **jauh lebih baik**: tanpa skill omzet salah +34% (PBJT, void, retur), NIK dan HP pelanggan bocor |
| 00 | Banding pesaing (ClawHub daily-report, oc-daily-business-report, Datasette, Metabase) | Tidak ada skill sebanding. Skill kita **menang** untuk UMKM awam. Dashboard unggul hanya di eksplorasi/grafik |
| 01 | Harian lengkap 4 alat | ✅ 21/21 angka cocok dengan hitungan independen dan output resmi alat |
| 02 | Mingguan Senin + `--samarkan` | ⚠️ Penjualan 19/19 cocok. **Kehadiran "hadir 30 dari 30" salah** (seharusnya 29 + 1 masuk hari libur) |
| 03 | Hanya kasir terpasang / DB terkunci / DB rusak | ✅ Dilewati dengan pesan jelas, tidak menggantung (10,2 detik), tanpa angka karangan |
| 04 | Input tidak lengkap (tanpa alat) | ✅ Script benar. ⚠️ SKILL.md tidak mengatur kasus semua-kosong (kerangka kosong bisa terkirim tiap malam) |
| 05 | Di luar cakupan (WA broadcast, ubah omzet) | ✅ Ditolak + alternatif sesuai keputusan pemilik |

## Verifikasi angka (independen)
- `verif.py` menghitung dari **tabel mentah** (SQL read-only ke `nota`, `bayar`, `nota_item`, `sesi`, `produk`, dan CSV pengingat) tanpa memakai kode `laporan.py`. Yang dicek: omzet bersih, uang diterima, nota jual/void/retur, nilai retur+void, rata-rata per nota, per metode, top-5 (kode, netto, qty), omzet dan % pembanding, selisih tutup kasir, daftar stok bermasalah (SKU, status, stok, kebutuhan restock), id tagihan terlambat/hari ini/besok, piutang terlambat, total tertunggak.
- Dijalankan untuk harian 15, 18, 21, 23, dan 24/9, mingguan 14–20/9, dan minggu berjalan 21–24/9: **0 selisih**. Satu "selisih" adalah format string verifikator ('28' vs '28.0'), nilainya sama.
- Dibandingkan juga dengan output resmi `kasir.py rekap`, `absensi.py harian/rekap`, `stok.py laporan ringkas`, dan `cek_jatuh_tempo.py rekap`: sama, **kecuali** (a) rata-rata per nota (definisi beda, lihat S2) dan (b) hadir mingguan (lihat B1).
- Persen: 16,5% (+39.100/237.500), −19,7%, +28,0% dicek manual. Pembanding Rp 0 → "naik dari Rp 0 (persen tidak dihitung)" ✔.
- Stok dicek ulang dari saldo awal + masuk − penjualan terimpor − rusak ✔.
- Kehadiran harian (24/9 dan 15/9) cocok dengan tap mentah: terlambat 18 menit (07.18 vs 07.00, toleransi 0), pulang 21.40 = 1 jam 40 menit lewat jadwal 20.00, lembur 1,5 jam ✔.
- Buku-stok sebagai sumber penjualan (tanpa kasir): omzet tercatat 243.500 dan 285.400 cocok dengan `mutasi` jual-mp ✔.
- **Tengah malam & zona waktu:** nota 23.50 masuk 23/9 dan 00.10 masuk 24/9 ✔. `--sekarang 2026-09-24T00:30+07:00` dan `2026-09-23T17:30Z` → tanggal 24/9 ✔. `23:59+07:00` → 23/9 ✔. `TZ=Asia/Makassar` + `--tz Asia/Makassar` 00.30 WITA → 24/9, label "WITA" ✔. Tanpa `--tz` di komputer WITA 00.30 → laporan 23/9 dengan peringatan (lihat S3).

## Hanya-baca (checksum sha256 + ukuran + mtime seluruh folder data, termasuk file -journal/-wal/-shm yang baru muncul)
| Kondisi | File berubah |
|---|---|
| Normal | tidak ada |
| **Skema lama** (stok tanpa `mutasi.dibatalkan`, kasir tanpa 5 kolom nota v1.1). Alat melakukan migrasi `ALTER TABLE` | tidak ada (migrasi hanya terjadi di salinan) |
| Sisa `absensi.db-journal` | tidak ada |
| DB terkunci (EXCLUSIVE) | tidak ada |
| stok.db sampah / kasir.db terpotong | tidak ada |
| kasir.db mode **WAL** dengan -wal belum di-checkpoint | `kasir.db` dan `-wal` sama. **`-shm` berubah** (indeks memori bersama SQLite, bukan data) |

## Privasi
Teks dan JSON (dengan dan tanpa `--samarkan`) dicari nama pelanggan, "0812/0813", NIK, "INV-", perihal, alasan izin, dan nama penyetuju lembur: **tidak ada**. `--samarkan` mengubah semua nama karyawan menjadi inisial, termasuk di JSON ✔.

## OpenClaw (CLI asli 2026.9.5)
- `skills install <folder> --global` untuk 5 skill → `skills check --json`: `laporan-harian-usaha` ada di `eligible`, `modelVisible`, `commandVisible` ✔.
- Perintah §2 referensi dijalankan persis (path hasil `expanduser`, `--command-cwd` workspace, `--command-env KOMUNITECH_DATA=…`): diterima. `schedule {cron "0 21 * * *", tz Asia/Jakarta}` → nextRun 14.00 UTC = 21.00 WIB ✔. Mingguan `0 7 * * 1` (+`--samarkan`) → Senin 00.00 UTC = 07.00 WIB ✔. Pilihan 2 (agent, `--session isolated --tools exec,read`) diterima ✔ (isi jawaban tidak diuji, butuh API key).
- `automations run <id> --wait` → `status: ok`, exit 0, `run.summary` = teks laporan **lengkap** (2.462 karakter; `diagnostics.summary` dipotong 2.000, hanya diagnostik). Pengingat ditemukan lewat `--command-cwd`. `deliveryStatus: not-delivered`, "Telegram bot token missing" (tanpa token asli) ✔ sesuai referensi.
- `runs --id`, `disable`, `enable`, `pairing approve [channel] <code>`, `channels login --channel`: sintaks sesuai `--help` ✔.
- Kanal sesuai keputusan pemilik: Telegram default, WA hanya nomor terpisah + persetujuan risiko tertulis, tanpa broadcast/grup ✔.
- Catatan: Gateway yang berjalan di UTC (VPS) memicu butir peringatan zona **setiap malam** (lihat S3).

## Skor
| Kriteria | Skor | Alasan |
|---|---|---|
| Pemicu (description) | 9 | Spesifik, kata kunci ID/EN, menyebut kapan pakai skill alat. 586 karakter |
| Kemudahan awam | 8 | Satu kalimat → satu perintah, teks rapi. Minus: butir peringatan zona muncul di VPS UTC, pesan "data absen ganjil" generik |
| Kualitas output | 8 | Satu pesan lengkap + "Perlu perhatian" yang benar-benar berguna (kurang kas, belum impor, lembur) |
| Akurasi | **6** | Semua angka penjualan/stok/tagihan/harian benar, **tetapi hadir mingguan salah** bila ada yang masuk hari libur. Rata-rata/nota beda dengan rekap resmi kasir |
| Penanganan input kurang | 7 | Script aman. SKILL.md belum mengatur "semua alat kosong" dan jadwal yang mengirim kerangka kosong |
| Penanganan di luar cakupan | 9 | Broadcast ditolak tegas sesuai keputusan pemilik. "Ubah angka" tercakup oleh aturan jangan ubah angka |
| Keamanan | 9 | Hanya-baca terbukti (termasuk migrasi skema), tanpa jaringan, privasi pelanggan terjaga. Minus kecil: -shm pada DB WAL |

### SKOR AKHIR: **6/10 → REVISI**
Kualitas keseluruhan tinggi dan hampir semua angka terbukti benar. Namun ada **satu angka salah** (kehadiran mingguan) yang membuat pemilik mengira kehadiran 100% padahal ada karyawan sakit. Sesuai brief, angka salah = cacat berat, jadi skor maksimal 6. Perbaikannya kecil (satu baris). Setelah B1, S1–S3 diperbaiki dan diuji ulang, perkiraan skor ≥ 8.

## Daftar cacat & saran
### BERAT
- **B1. Kehadiran mingguan menjumlahkan masuk hari libur ke "hadir … dari … hari terjadwal".** `scripts/laporan.py` baris 510: `hasil["hari_hadir"] += int(kr.get("hadir", 0)) + int(kr.get("hadir_di_hari_libur", 0))`. Contoh 14–20/9: "hadir 30 dari 30", padahal `absensi.py rekap` = 29 hadir terjadwal (J. sakit 1) + 1 masuk hari libur (S.). Bisa juga menghasilkan "31 dari 30". **Saran:** simpan `hadir_di_hari_libur` terpisah, lalu di baris 825 tampilkan `"hadir %d dari %d hari terjadwal (+%d masuk hari libur)"`. Tambahkan uji regresi dengan karyawan yang masuk di hari liburnya.

### SEDANG
- **S1. Kerangka kosong terkirim bila tidak ada alat terbaca.** SKILL.md langkah A.1 "Kirim `teks` apa adanya", dan jadwal Pilihan 1 (tanpa AI) akan mengirim "Belum ada data" ×4 setiap malam. **Saran:** laporan.py keluar dengan kode khusus (mis. 3), atau cetak satu kalimat pendek bila `semua alat tidak_ada/gagal`. Tambahkan di SKILL.md A.2: "Jika SEMUA bagian 'Belum ada data': jangan kirim kerangka, tanyakan sekali alat yang dipakai + lokasi datanya". Di referensi §1.5, tegaskan uji manual wajib sebelum membuat jadwal.
- **S2. "Rata-rata per nota" berbeda dengan rekap resmi kasir-lokal** (24/9: laporan Rp 34.575, `kasir.py rekap` Rp 40.508, karena kasir memakai uang diterima termasuk PBJT dan belum dikurangi retur). Ini bertentangan dengan klaim SKILL.md "angka dihitung oleh perintah laporan resmi". **Saran:** pakai `rata_rata_per_nota` dari kasir, atau beri label "rata-rata (omzet tanpa pajak)" di baris 750 dan jelaskan perbedaannya di "Aturan hitung". Hal yang sama untuk "Per metode bayar" (jumlahnya = uang diterima termasuk pajak): beri label "(uang diterima, termasuk pajak)".
- **S3. Peringatan zona waktu tidak akurat dan terus muncul.** Baris 664–669: (a) kalimat "Kasir & absensi mencatat jam komputer" salah untuk kasir-lokal 1.1.0, yang mencatat dalam zona toko (`meta.zona`); (b) di VPS UTC, yang disarankan referensi, butir ini muncul setiap malam; (c) di toko WITA tanpa `--tz`, sarannya "samakan zona komputer", padahal yang tepat adalah `--tz Asia/Makassar`. **Saran:** baca `pengaturan.zona` dari `kasir.py info` dan pakai sebagai default `--tz` bila pengguna tidak memberi. Peringatkan jam komputer hanya untuk absensi-lokal. Beri saran `--tz` bila zona komputer ≠ zona laporan.

### RINGAN
- R1. "N data absen ganjil perlu dicek (mis. tap tidak lengkap)" (baris 707–708) tidak menyebut siapa atau apa. Di uji, isinya "lembur disetujui 1,5 jam, absen hanya 40 menit". Tampilkan nama (atau inisial) + potongan `pesan` seperti bagian lembur.
- R2. Saat DB terkunci, tidak ada coba ulang. Laporan terjadwal pukul 21.00 bisa terkirim tanpa penjualan. Tambahkan satu kali coba ulang setelah ±30 detik sebelum menandai "gagal".
- R3. Alat yang datanya ada tetapi sengaja tidak dibeli/dipasang memunculkan "Pasang skill …" setiap malam. SKILL.md sebaiknya menyarankan `--tanpa stok` untuk kasus ini.
- R4. `--samarkan` hanya memakai huruf pertama, sehingga dua karyawan bisa sama-sama "B.". Pakai 2 huruf atau tambahkan kode karyawan bila bentrok.
- R5. Klaim "file asli tidak pernah ditulis": pada DB mode WAL, SQLite tetap menulis `-shm`. Alat Komunitech memakai journal biasa sehingga tidak berdampak, tetapi sebaiknya kalimatnya diperhalus atau buka dengan `immutable=1` setelah menyalin -wal.
- R6. Sumber penjualan buku-stok: hari yang belum diimpor tampil "vs kemarin Rp 0 → naik dari Rp 0". Tambahkan catatan "tanggal X belum ada impor penjualan".
- R7. SKILL.md "Kapan TIDAK digunakan" belum menyebut permintaan mengubah/menaikkan angka. Tambahkan: tolak, lalu tawarkan periode lebih panjang atau `laporan-keuangan-emkm`.
- R8. Pengiriman nyata ke Telegram belum pernah diuji (butuh bot token). Isi `platform_teruji` cukup `openclaw (CLI 2026.9.5, tanpa pengiriman); claude-code (simulasi agent)`.

## Status yang disarankan
Tetap `draft` → perbaiki B1 (wajib) dan S1–S3 → uji ulang oleh penguji independen (fokus: rekap mingguan dengan masuk hari libur, VPS UTC, toko WITA, kasus tanpa alat).
