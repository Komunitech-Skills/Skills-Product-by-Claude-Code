# Catatan uji pembuat — `grist-usaha` v1.0.0 (bukan hasil uji independen)

**Tanggal:** 2026-09-26
**Penguji:** sesi ini (agent) — **bukan** penguji independen terpisah dari pembuat, karena
skill ini dibuat & diuji dalam satu sesi kerja atas permintaan pemilik untuk mempercepat batch
pertama. Ini dicatat apa adanya; CLAUDE.md Tahap 6 butir 2 ("pengujian oleh agent/sesi terpisah")
**belum dipenuhi** — perlu diulang oleh sesi/penguji independen sebelum naik ke status `uji`.

## Ringkasan 5 skenario (Tahap 6 butir 3)
| # | Skenario | Berkas | Hasil |
|---|---|---|---|
| 1 | Normal — baca ringkasan stok dari file `.grist` | `01-ringkasan-stok-dari-file-grist.md` | Sesuai harapan |
| 2 | Normal — rancang & buat tabel Pelanggan lewat REST API | `02-rancang-dan-buat-tabel-pelanggan.md` | Sesuai harapan |
| 3 | Normal — bersihkan CSV (angka Rupiah campuran format) & impor | `03-bersihkan-dan-impor-csv.md` | Sesuai harapan |
| 4 | Input tidak lengkap/ambigu (5 varian) | `04-input-tidak-lengkap.md` | Semua ditangani dengan pesan jelas, tidak menebak sembarangan |
| 5 | Di luar cakupan (5 varian) | `05-di-luar-cakupan.md` | Semua ditolak/diarahkan dengan alasan jelas |

Uji dengan **data rusak** (Tahap 6 butir 3, "bila ada script, jalankan juga dengan data rusak"):
- File `.grist` bukan SQLite sama sekali → ditolak dengan pesan jelas (`tests/uji_regresi.py`
  `test_file_rusak_bukan_sqlite`).
- File SQLite valid tapi tanpa tabel `_grist_Tables` (bukan dokumen Grist) → ditolak, menyebut
  tabel metadata yang hilang (`test_file_sqlite_tanpa_metadata_grist`).
- File `.grist` kosong (0 byte) → ditolak (`test_file_kosong`).
- CSV dengan nama kolom tidak sah untuk Grist → ditolak **sebelum** memanggil API sama sekali
  (`test_impor_csv_nama_kolom_tidak_sah_ditolak_sebelum_kirim`), supaya tidak ada percobaan
  tulis parsial.
- Kunci API salah (401 dari server) → dilaporkan apa adanya, kunci tidak pernah tercetak
  (`test_cek_kunci_salah`).
- Dokumen tidak ditemukan / nama ambigu → pesan menyebutkan daftar dokumen yang sebenarnya bisa
  diakses (`test_dokumen_tidak_ditemukan`, `TestCariDokumen`).

**Verifikasi angka independen (Tahap 6 butir 3):** rumus pembersihan angka (`_bersihkan_angka`)
diuji dengan 7 kasus format berbeda (`Rp 1.234.567,89`, `1234567.89`, `1.234.567`, `32,5`,
`1,234`, `Rp. 50.000`, dan teks bukan-angka) di `TestBersihkanAngka`, dihitung ulang manual
(bukan hanya "jalankan lalu cocokkan dengan dirinya sendiri"). Rumus `rumus_sisa_stok`/
`rumus_status_stok` di file fixture diverifikasi manual: `Gula Aren 1kg` (masuk 50, keluar 48,
batas 10) → sisa **2 < 10** → MENIPIS ✓; `Cup Kertas 12oz` (masuk 200, keluar 200) → sisa **0**
→ HABIS ✓; `Kopi Robusta 1kg` (masuk 100, keluar 40, batas 20) → sisa **60 ≥ 20** → AMAN ✓.

## Uji A/B & uji banding pesaing (Tahap 6 butir 4–5) — **BELUM dikerjakan, jujur**
Cakupan tugas untuk skill ini (draft pertama, batch 2026-09-26) tidak meminta perbandingan
"agent tanpa skill vs dengan skill" maupun uji banding pesaing (skill publik Airtable/Grist di
ClawHub/skills.sh/GitHub). Ini **PERLU DIKERJAKAN** sebelum skill naik ke status `uji`/`lulus`,
sesuai CLAUDE.md Tahap 6 butir 4–5. Rekomendasi kata kunci pencarian pesaing untuk sesi
berikutnya: "grist skill", "grist mcp", "airtable agent skill", "grist api agent".

## Kejujuran soal apa yang benar-benar diuji vs tidak
- **Diuji sungguhan, otomatis, berulang (`tests/uji_regresi.py`, 50 kasus, semua lulus):**
  fungsi pembersihan angka/nama kolom, pembacaan file `.grist` (SQLite) read-only termasuk file
  rusak, validasi alamat server (localhost vs internet vs jaringan lokal), logika pencarian
  dokumen by nama (docId ambigu/tidak ketemu), penyimpanan kunci API (izin file 600, penolakan
  menimpa), dan seluruh alur REST API (`cek`/`buat-tabel`/`impor-csv`) **terhadap server Grist
  TIRUAN** yang meniru bentuk respons resmi grist-core.
- **BELUM diuji:** terhadap `grist-core`/Grist Desktop yang sungguhan menyala (lingkungan sesi
  ini tidak bisa menjalankan Docker — dicoba, ditolak kebijakan sandbox; tidak ada GUI untuk
  aplikasi desktop). Rumus di `references/rumus-umum.md` belum dijalankan di kotak formula Grist
  sungguhan. File `.grist` fixture adalah **tiruan** yang skemanya disusun dari kode sumber resmi
  (lihat `research/sources/grist-2026-09-26.md`), bukan ekspor Grist asli.
- Lihat `docs/panduan-grist.md` bagian 0 dan `README.md` untuk keterangan yang sama ke pembeli.

## Uji muat OpenClaw
Lihat catatan hasil `bash scripts/uji_openclaw.sh` di laporan sesi (`reports/2026-09-26.md`).

## Skor kualitas: **6/10**
Alasan: fungsi inti benar & teruji otomatis (fungsi murni + SQLite read-only + REST API lewat
server tiruan), penanganan input buruk & di luar cakupan lengkap, keamanan kunci API & alamat
server sudah dipikirkan. **Skor ditahan di 6** (bukan lebih tinggi) semata karena Tahap 6 belum
lengkap secara prosedural: belum ada uji A/B, uji banding pesaing, penguji independen terpisah
dari pembuat, maupun uji terhadap Grist sungguhan/OpenClaw asli — sesuai aturan CLAUDE.md "di
bawah 7 → revisi, jangan rilis" dan "uji A/B/banding pesaing wajib, kalau tidak dikerjakan skor
maks. 6". Status katalog: **draft** (belum `uji`/`lulus`), konsisten dengan skor ini.

## Rekomendasi sebelum naik ke status `uji`
1. Uji sungguhan di Grist Desktop atau Docker `gristlabs/grist` oleh pemilik/tim (komputer
   dengan Docker/GUI berfungsi) — jalankan seluruh alur `docs/panduan-grist.md`, konfirmasi
   rumus di `references/rumus-umum.md` benar-benar jalan di kotak formula Grist.
2. Penguji independen (sesi/agent lain yang hanya membaca folder skill ini) menjalankan ulang
   5 skenario.
3. Uji A/B (tanpa skill vs dengan skill) & uji banding pesaing.
4. `bash scripts/uji_openclaw.sh` dan uji platform asli (`docs/uji-platform.md`).
