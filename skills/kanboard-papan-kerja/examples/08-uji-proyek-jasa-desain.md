# Skenario 08 — Papan proyek jasa desain, zona WITA (normal, uji independen)

**Penguji:** agent penguji independen (Claude Code, bukan pembuat), 2026-09-30 ±19:55–21:00 WIB. **Kanboard v1.2.54 asli** di-clone sendiri oleh penguji (tag git resmi `v1.2.54`, commit `9ce6a5e`), dijalankan `APP_VERSION=v1.2.54 php -S 127.0.0.1:8090` (PHP 8.4.19 + SQLite), database BARU milik penguji. Akun uji buatan penguji: `sari` (Manajer), `dimas` (Pengguna), `rina` (Pengguna). Token pribadi dibuat acak oleh penguji dan ditulis ke kolom `api_access_token` (setara tombol "Generate token baru"), disimpan di file kunci izin 600 dan dipakai lewat `KANBOARD_KUNCI_FILE` — token tidak pernah tampil. Server tiruan pembuat **tidak** dipakai. Data fiktif. `kanboard.py` = `python3 scripts/kanboard.py`; `(kode keluar N)` ditambahkan pembungkus uji.

**Zona server: Asia/Jakarta**, pengguna di Makassar/Bali memakai `--tz WITA`. Akun AI: `sari` (Manajer). Kartu #24 dimundurkan `date_moved` 8 hari, #25 1 hari. Penutupan kartu #21 dan penonaktifan papan dilakukan penguji lewat token aplikasi (meniru tindakan manusia di layar Kanboard) untuk menguji bahwa kartu tertutup/papan nonaktif tidak dihitung.

## Permintaan pengguna
> "Saya pakai WITA. Buatkan papan proyek untuk studio desain saya, masukkan proyek klien ini, dan kasih tahu mana yang jatuh tempo hari ini dan yang nyangkut lebih dari seminggu."

## Log lengkap
```
$ buat-papan --jenis proyek-jasa --nama "Proyek Studio Desain Kirana" --ya
PAPAN DIBUAT: Proyek Studio Desain Kirana (id 3)
Template: proyek-jasa - Proyek Jasa (konsultan, agensi, kontraktor, freelancer)
Kolom:
  1. Prospek/Brief
  2. Penawaran
  3. Dikerjakan
  4. Revisi Klien
  5. Tagihan
  6. Selesai
Buka: http://127.0.0.1:8090/?controller=BoardViewController&action=show&project_id=3
(kode keluar 0)
$ tambah-kartu --judul "Logo Kopi Senja - 3 opsi" --kolom "Dikerjakan" --tenggat "Jumat jam 12:00" --tz WITA --ke rina --ya
GAGAL: Anggota 'rina' tidak ditemukan di papan ini. Yang bisa ditugaskan: Sari Wulandari.
SARAN: Tambahkan orang itu sebagai anggota papan di Kanboard (ikon roda > Izin), atau buat kartu tanpa --ke.
(kode keluar 2)
$ tambah-kartu --judul "Feed IG Klinik Gigi Ceria (9 post)" --kolom "Dikerjakan" --tenggat "akhir bulan" --tz WITA  --ya
KARTU DIBUAT: #20
Jatuh tempo: Rabu, 30 September 2026 jam 17:00 WITA
PERINGATAN: jatuh tempo ini SUDAH LEWAT - kartu langsung tercatat terlambat. Benar?
(kode keluar 0)
$ tambah-kartu --judul "Kemasan keripik Maicih KW" --kolom "Dikerjakan" --tenggat "5 hari lagi jam 09:00" --tz WITA  --ya
KARTU DIBUAT: #21
Jatuh tempo: Senin, 5 Oktober 2026 jam 09:00 WITA
(kode keluar 0)
$ tambah-kartu --judul "Company profile CV Bangun" --kolom "Dikerjakan" --tenggat "hari ini jam 20:00" --tz WITA  --ya
KARTU DIBUAT: #22
Jatuh tempo: Rabu, 30 September 2026 jam 20:00 WITA
PERINGATAN: jatuh tempo ini SUDAH LEWAT - kartu langsung tercatat terlambat. Benar?
(kode keluar 0)
$ tambah-kartu --judul "Banner ruko Pak Hendra" --kolom "Dikerjakan" --tenggat "25 Oktober 2026" --tz WITA  --ya
KARTU DIBUAT: #23
Jatuh tempo: Minggu, 25 Oktober 2026 jam 17:00 WITA
(kode keluar 0)
$ tambah-kartu --judul "Revisi menu Warung Bu Tini" --kolom "Revisi Klien" --tenggat "Jumat depan jam 10:00" --tz WITA  --ya
KARTU DIBUAT: #24
Jatuh tempo: Jumat, 9 Oktober 2026 jam 10:00 WITA
(kode keluar 0)
$ tambah-kartu --judul "Invoice brosur Apotek Sehat" --kolom "Tagihan" --tenggat "hari ini jam 23:59" --tz WITA  --ya
KARTU DIBUAT: #25
Jatuh tempo: Rabu, 30 September 2026 jam 23:59 WITA
(kode keluar 0)
$ tambah-kartu --judul "Undangan nikah Dewi-Arif" --kolom "Selesai" --tenggat "hari ini jam 22:00" --tz WITA  --ya
KARTU DIBUAT: #26
Jatuh tempo: Rabu, 30 September 2026 jam 22:00 WITA
(kode keluar 0)
$ --ke orang bukan anggota
GAGAL: Anggota 'Dimas' tidak ditemukan di papan ini. Yang bisa ditugaskan: Sari Wulandari.
SARAN: Tambahkan orang itu sebagai anggota papan di Kanboard (ikon roda > Izin), atau buat kartu tanpa --ke.
(kode keluar 2)
$ --ke ambigu "a"
PRATINJAU KARTU BARU
Papan: Proyek Studio Desain Kirana (id 3)
Kolom: Prospek/Brief
Judul: Tes PIC
PIC: Sari Wulandari
Belum disimpan. Simpan ke Kanboard? (ya/tidak)
(kode keluar 0)
$ papan ambigu "Pro"
GAGAL: Nama papan 'Pro' cocok lebih dari satu: Produksi Konveksi Mekar Jaya (id 1); Proyek Studio Desain Kirana (id 3). Sebutkan id-nya.
(kode keluar 7)
$ kolom Kirana
KOLOM PAPAN: Proyek Studio Desain Kirana (id 3)
1. Prospek/Brief (id 13): 0 kartu
2. Penawaran (id 14): 0 kartu
3. Dikerjakan (id 15): 4 kartu / batas 4
4. Revisi Klien (id 16): 1 kartu
5. Tagihan (id 17): 1 kartu
6. Selesai (id 18): 1 kartu
(kode keluar 0)
$ hari-ini --papan Kirana --tz WITA
KARTU JATUH TEMPO HARI INI (Rabu, 30 September 2026)
Papan: Proyek Studio Desain Kirana
Jumlah: 4
Kartu tanpa tanggal jatuh tempo tidak muncul di sini. Kartu jatuh tempo hari ini yang jamnya sudah lewat muncul di sini MAUPUN di 'terlambat' - jangan dijumlahkan sebagai kartu unik.
- #20 Feed IG Klinik Gigi Ceria (9 post) (jatuh tempo 30 Sep 2026 17:00; papan: Proyek Studio Desain Kirana; kolom: Dikerjakan)
- #22 Company profile CV Bangun (jatuh tempo 30 Sep 2026 20:00; papan: Proyek Studio Desain Kirana; kolom: Dikerjakan)
- #26 Undangan nikah Dewi-Arif (jatuh tempo 30 Sep 2026 22:00; papan: Proyek Studio Desain Kirana; kolom: Selesai)
- #25 Invoice brosur Apotek Sehat (jatuh tempo 30 Sep 2026 23:59; papan: Proyek Studio Desain Kirana; kolom: Tagihan)
(kode keluar 0)
$ macet --papan Kirana --hari 7
KARTU MACET (tidak pindah kolom >= 7 hari)
Papan: Proyek Studio Desain Kirana
Jumlah: 1
Kartu di kolom TERAKHIR papan (mis. Selesai/Tayang/Diterima) dianggap beres dan tidak dihitung terlambat/macet.
- #24 Revisi menu Warung Bu Tini (diam 8 hari; jatuh tempo 9 Okt 2026 10:00; papan: Proyek Studio Desain Kirana; kolom: Revisi Klien)
(kode keluar 0)
$ (admin menambah Rina sebagai anggota papan di Kanboard) lalu ulangi:
$ tambah-kartu --judul "Logo Kopi Senja - 3 opsi" --kolom Dikerjakan --tenggat "Jumat jam 12:00" --tz WITA --ke rina --ya
KARTU DIBUAT: #27
Papan: Proyek Studio Desain Kirana (id 3)
Kolom: Dikerjakan
Judul: Logo Kopi Senja - 3 opsi
Jatuh tempo: Jumat, 2 Oktober 2026 jam 12:00 WITA
PIC: Rina Penjahit
(kode keluar 0)
$ kolom --papan Kirana (Dikerjakan kini 5 > batas 4)
KOLOM PAPAN: Proyek Studio Desain Kirana (id 3)
1. Prospek/Brief (id 13): 0 kartu
2. Penawaran (id 14): 0 kartu
3. Dikerjakan (id 15): 5 kartu / batas 4 - MELEBIHI BATAS
4. Revisi Klien (id 16): 1 kartu
5. Tagihan (id 17): 1 kartu
6. Selesai (id 18): 1 kartu
(kode keluar 0)
$ (di layar Kanboard: kartu #21 DITUTUP; papan 1 tetap aktif) -> laporan --papan 3 --tz WITA
LAPORAN PAPAN KERJA - Rabu, 30 September 2026 20:59 WITA
Papan: Proyek Studio Desain Kirana | kartu terbuka: 7
Terlambat 2 | Jatuh tempo hari ini 4 | Macet >= 3 hari 1

TERLAMBAT (2)
- #20 Feed IG Klinik Gigi Ceria (9 post) (jatuh tempo 30 Sep 2026 17:00; papan: Proyek Studio Desain Kirana; kolom: Dikerjakan)
- #22 Company profile CV Bangun (jatuh tempo 30 Sep 2026 20:00; papan: Proyek Studio Desain Kirana; kolom: Dikerjakan)

HARI INI (4)
- #20 Feed IG Klinik Gigi Ceria (9 post) (jatuh tempo 30 Sep 2026 17:00; papan: Proyek Studio Desain Kirana; kolom: Dikerjakan)
- #22 Company profile CV Bangun (jatuh tempo 30 Sep 2026 20:00; papan: Proyek Studio Desain Kirana; kolom: Dikerjakan)
- #26 Undangan nikah Dewi-Arif (jatuh tempo 30 Sep 2026 22:00; papan: Proyek Studio Desain Kirana; kolom: Selesai)
- #25 Invoice brosur Apotek Sehat (jatuh tempo 30 Sep 2026 23:59; papan: Proyek Studio Desain Kirana; kolom: Tagihan)

MACET >= 3 HARI (1)
- #24 Revisi menu Warung Bu Tini (diam 8 hari; papan: Proyek Studio Desain Kirana; kolom: Revisi Klien)
(kode keluar 0)
$ (papan Kirana DINONAKTIFKAN di Kanboard) -> laporan tanpa --papan (hitungan hanya papan aktif)
LAPORAN PAPAN KERJA - Rabu, 30 September 2026 19:59 WIB
Papan: semua papan aktif | kartu terbuka: 13
Terlambat 3 | Jatuh tempo hari ini 3 | Macet >= 3 hari 4
DAFTAR PAPAN KANBOARD
- Produksi Konveksi Mekar Jaya (id 1)
(kode keluar 0)
```

## Verifikasi independen (19:59 WIB = 20:59 WITA)
- Tenggat WITA → server Jakarta: "Jumat jam 12:00 WITA" → 2 Okt 11:00 WIB (dicek DB) ✔; "hari ini jam 20:00 WITA" langsung diberi PERINGATAN sudah lewat ✔ (saat itu 20:5x WITA).
- Hari ini (WITA 30 Sep): #20 17:00, #22 20:00, #26 22:00, #25 23:59 → 4 ✔. Terlambat: #20, #22 → 2 ✔ (#26 di Selesai, #25 belum). Macet ≥7: #24 (8 hari) ✔. Kartu tertutup #21 tidak dihitung (terbuka 7) ✔. Papan nonaktif hilang dari `daftar-papan` & laporan "semua papan aktif" ✔.
- `kolom`: 5 kartu di "Dikerjakan" batas 4 → "MELEBIHI BATAS" ✔.
- Nama papan ambigu `"Pro"` → kode 7 + minta id ✔. `--ke rina` sebelum Rina jadi anggota → kode 2 + daftar yang bisa ditugaskan + saran ✔; setelah ditambah admin → PIC tercatat ✔.

## Temuan dari skenario ini
- **Rendah:** `hari-ini` dan bagian "HARI INI" di `laporan` ikut memuat kartu di **kolom terakhir** (#26 "Undangan nikah Dewi-Arif" di Selesai), padahal di bagian lain kolom terakhir dianggap beres. Tidak salah hitung, tapi tidak konsisten dan bisa membuat pemilik mengejar pekerjaan yang sudah beres.
- **Rendah:** `--ke "a"` (satu huruf) cocok sebagian ke satu-satunya anggota "Sari Wulandari" tanpa penegasan; pratinjau menampilkan PIC sehingga masih tertangkap.
- `"Jumat depan"` dari Rabu 30 Sep → Jumat 9 Okt (minggu kalender berikutnya), sesuai dokumentasi SKILL.md.
