# Skenario 04 — Input tidak lengkap / buruk

**Penguji:** agent independen, 2026-09-24. Semua pada salinan data skenario 01 di folder sementara.

## A. Percakapan: data di lokasi lain
> "Laporan usaha hari ini." — kasir ternyata disimpan di flashdisk `E:\toko\kasir.db`.

Simulasi agent yang hanya membaca SKILL.md: menjalankan script tanpa bertanya (Input: "Tidak perlu bertanya apa pun untuk laporan pertama"), mendapati "PENJUALAN — Belum ada data (kasir-lokal belum dipakai di komputer ini)", lalu mengikuti Langkah A.2: *"Bagian penjualan kosong: kasir-lokal tidak ditemukan di lokasi biasanya. Apakah data kasir Anda disimpan di tempat lain? Sebutkan lokasinya, nanti saya pakai opsi --kasir-db."* Tidak mengarang angka. ✅ (Uji tanpa alat sama sekali: semua bagian "Belum ada data", PERLU PERHATIAN menyebut opsi `--kasir-db/--stok-db/--absensi-db/--pengingat`, kode keluar 0.)

## B. Argumen salah (kode keluar 2, pesan jelas)
| Perintah | Hasil |
|---|---|
| `--tanggal 2026-09-30` | `ERROR: tanggal 2026-09-30 belum terjadi (hari ini 2026-09-24).` rc=2 ✅ |
| `--tanggal besok` | `ERROR: tanggal 'besok' tidak dikenali. Pakai hari-ini, kemarin, 2026-09-24, atau 24/09/2026.` rc=2 ✅ |
| `--tanggal 31/02/2026 --json` | `{"ok": false, "error": "tanggal '31/02/2026' tidak ada di kalender."}` rc=2 ✅ |
| `--periode mingguan --tanggal 2026-10-05` | `ERROR: minggu itu belum dimulai.` rc=2 ✅ |
| `--tz ngawur` | pesan menyarankan WIB/WITA/WIT, rc=2 ✅ |
| `--tanpa gaji` | `--tanpa hanya menerima: kasir, stok, absensi, pengingat (bukan gaji)` rc=2 ✅ |
| `--tz Asia/Tokyo` | **diterima** (label "Asia/Tokyo"). Tidak berbahaya, tetapi di luar cakupan Indonesia (catatan rendah). |

## C. Database rusak / bukan SQLite / 0 byte
`kasir.db` diganti teks + 5 KB acak; `absensi.db` dikosongkan (0 byte). Kode keluar 0:
```
PENJUALAN
Belum ada data: kasir-lokal tidak terbaca (lihat Perlu Perhatian).
...
KEHADIRAN
Belum ada data: absensi-lokal tidak terbaca (lihat Perlu Perhatian).
...
PERLU PERHATIAN
...
3. kasir-lokal tidak terbaca: file bukan database atau rusak (file is not a database). Pulihkan dari folder backup alatnya.
4. absensi-lokal tidak terbaca: File /tmp/laporan-usaha-dsjcnue6/absensi.db tidak bisa dibaca sebagai database absensi-lokal (no such table: meta). Jangan hapus atau timpa file ini; hubungi pembuat/penjual skill atau pulihkan dari folder backup-absensi.
```
- Stok & tagihan tetap dilaporkan ✅. Penjualan **tidak** jatuh ke omzet buku-stok saat kasir rusak (benar, menghindari angka campur) ✅. Hash file rusak sebelum = sesudah ✅.
- ⚠️ Butir 4 menyebut **path salinan sementara** (`/tmp/laporan-usaha-…/absensi.db`, sudah dihapus), bukan file asli `…/data/absensi/absensi.db`. Pengguna awam bisa bingung (cacat R4).

## D. Skill alat tidak terpasang
Folder skills tanpa `absensi-lokal` (data absensi ada):
`6. absensi-lokal tidak terbaca: data ada, tetapi script absensi.py tidak ditemukan. Pasang skill absensi-lokal di folder skills yang sama, atau beri --absensi-script PATH.` Bagian lain normal ✅.

## E. Database terkunci
Proses lain memegang `BEGIN EXCLUSIVE` pada `kasir.db` selama 8 detik; laporan dengan `--timeout 2`:
```
PENJUALAN
Belum ada data: kasir-lokal tidak terbaca (lihat Perlu Perhatian).
...
4. kasir-lokal tidak terbaca: database sedang dipakai program lain lebih dari 2 detik (mis. transaksi sedang disimpan). Data aman; jalankan laporan lagi sebentar lagi.
```
Selesai dalam **2,3 detik** (tidak menggantung); alat lain tetap dilaporkan ✅.

## F. Daftar pengingat berisi baris rusak / nomor HP
- Tambah baris `6,piutang,Pak Anto,30-02-2026,abc,...` (tanggal & nominal rusak) dan baris sah #7: laporan menghitung #7 (lewat 4 hari, total tertunggak 5.450.000 = 4.950.000 + 500.000 ✅) dan menambah `7. 1 baris di daftar pengingat rusak & dilewati. Ketik 'rekap pengingat' untuk rinciannya.` ✅
- Baris dengan nama `Bu Maya 081234567890`: ditampilkan sebagai `#8 piutang Rp 500.000, lewat 4 hari`; grep `0812` di teks & JSON → 0 ✅.

## G. Waktu ganjil
- Laporan "hari ini" jam **00.30** (`--sekarang 2026-09-25T00:30+07:00`) memunculkan `Belum ada satu pun data absen hari itu. File mesin absen mungkin belum diimpor.` — alarm palsu karena shift belum mulai (cacat R2). Hal yang sama terjadi bila pemilik bertanya jam 07.30 sebelum jam masuk 08.00.
- Impor kasir ke buku-stok **sebagian** (hanya N-260924-0001 dari 7 nota, seperti ekspor siang hari): peringatan "belum diimpor" **hilang** padahal 6 nota belum memotong stok (cacat S1). Reproduksi:
  ```bash
  kasir.py ekspor --format buku-stok --tanggal 2026-09-24 --csv j24.csv
  (baris judul + baris N-260924-0001 saja) > j24-pagi.csv
  stok.py impor-pesanan j24-pagi.csv --platform lainnya --ya
  laporan.py --sekarang 2026-09-24T21:30+07:00   # PERLU PERHATIAN tidak lagi menyebut "belum diimpor"
  ```
- Sesi kasir dibuka 21.40 dan belum ditutup → `Kasir belum ditutup (dibuka 2026-09-24 21:40)...` ✅.

**Hasil: LULUS** untuk penanganan error (tidak crash, tidak menggantung, tidak menulis file asli, pesan jelas), dengan 3 temuan (S1, R2, R4).
