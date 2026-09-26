# Uji ulang v1.1.1 — penguji independen lintas akun (Akun B), 2026-09-26

- **Peran:** penguji independen (Akun B, simulasi agent Claude Code). Bukan pembuat v1.1.1 (Akun A) dan tidak
  mengubah kode, `SKILL.md`, `references/`, `tests/`, atau `catalog.csv`.
- **Lingkungan:** Linux, Python 3.11, `TZ=Asia/Jakarta`. Skill + `kasir-lokal`, `buku-stok`, `absensi-lokal`,
  `crm-wa`, `pengingat-follow-up` disalin ke scratchpad (`diff -rq` vs repo: identik). v1.1.0 pembanding diambil
  dari `git show 560836d~1:.../laporan.py` (VERSI 1.1.0) dan dijalankan berdampingan di folder skills yang sama.
- **Data rekaan sendiri (berbeda dari data pembuat):** "Kedai Senja Rekaan" — 3 nota 24/9 (sudah diekspor+diimpor ke
  buku-stok), 4 nota 25/9 (1 di-void), 2 shift (PAGI 07.00, SIANG 14.00) dengan 4 karyawan (Wulan, Tono = PAGI;
  Yusuf, Mira = SIANG), 6 kontak CRM (terlambat, deal lama, deal baru, batal, lead baru). Semua nama/nomor fiktif.
  Data dibuat dengan script resmi tiap alat, bukan menulis tabel dengan tangan.

## Ringkasan
| Temuan | Status v1.1.1 (uji Akun B) | Bukti ringkas |
|---|---|---|
| N1 alarm sebelum jam masuk | **Tertutup** (acuan shift paling awal) | 06.55: tanpa alarm (v1.1.0: alarm 3 nama); 07.00/07.30: alarm muncul |
| N2 cek dilewati tampil | **Tertutup** | rename `pesanan.no_pesanan` → teks memuat catatan 1× (v1.1.0: diam) |
| N3 void setelah impor | **Tertutup**, dengan 1 batas baru (N3b) | 2 nota 24/9 di-void 25/9 → butir dengan 2 nomor; langkah perbaikan terbukti mengembalikan stok |
| N4 status PROSPEK di referensi | **Tertutup** | `references/openclaw-jadwal.md` baris status kini ✅ + rujukan HASIL-UJI |
| N5 titik ganda `--samarkan` | **Tertutup** | "T., Y., M. Tanyakan" (v1.1.0: "M.. Tanyakan") |
| N-baru `--samarkan` ke crm rekap | **Tertutup** | wrapper `crm.py` mencatat argv: `--samarkan` hanya saat diminta, harian & 2 panggilan mingguan |
| Order perlu konfirmasi | **Tertutup** | 2 deal jatuh tempo → butir "2 order (deal)…"; jadwal besok → tanpa butir |
| Angka tidak berubah | **Terbukti** | 10 kasus × 7 bagian JSON v1.1.0 = v1.1.1; omzet & PROSPEK = hitung mandiri SQLite |

## Rincian per temuan

### N1 — alarm sebelum jam masuk
Wulan (PAGI) tap 06.50 pada 25/9, lainnya belum.
| `--sekarang` | v1.1.0 PERLU PERHATIAN | v1.1.1 PERLU PERHATIAN |
|---|---|---|
| 06.55 | "Belum absen tanpa keterangan (3): Tono, Yusuf, Mira…" | (tidak ada butir kehadiran) |
| 07.00 | alarm 3 nama | alarm 3 nama (toleransi telat absensi default 0 menit → konsisten) |
| 07.30 / 13.59 | alarm 3 nama | alarm 3 nama, **termasuk Yusuf & Mira (shift SIANG 14.00)** |
| 14.30 | alarm 3 nama | alarm 3 nama (benar) |

Bagian KEHADIRAN "Belum absen (3)" tetap tampil di semua jam (benar). Tanpa tap sama sekali 06.30 → "Belum waktunya
absen (jadwal mulai 07.00)" tetap. Alarm shift siang antara 07.00–13.59 adalah **batas yang sudah diungkap pembuat**
("N1 per-shift"), bukan cacat baru; tetap dicatat karena usaha dengan dua shift akan melihatnya di laporan siang.

### N2 — cek dilewati tampil di teks
- `ALTER TABLE pesanan RENAME COLUMN no_pesanan TO no_psn` di salinan stok.db → v1.1.1 butir 6 "Cek impor kasir ke
  buku-stok dilewati: struktur tabel pesanan berubah." (1×, tidak duplikat walau cek impor dan cek void sama-sama
  melewati). v1.1.0: `catatan` terisi tapi teks diam.
- Kasus buatan sendiri: rename `pesanan.dibatalkan` → `stok.py` sendiri gagal, laporan menampilkan "buku-stok tidak
  terbaca: …no such column: dibatalkan" (sama di kedua versi, tidak crash).

### N3 — nota di-void setelah diimpor
Kasus sendiri: N-260924-0002 & -0003 (sudah diimpor 24/9) di-void 25/9 17.00/17.05; N-260925-0004 di-void 16.02
**sebelum** impor, lalu ekspor+impor 25/9.
- v1.1.1 laporan 25/9: "2 nota kasir di-void setelah diimpor ke buku-stok, stoknya belum dikembalikan (N-260924-0002,
  N-260924-0003). Ekspor ulang tanggal nota itu…". N-260925-0004 tidak disebut (benar: tidak pernah memotong stok —
  KSGA 40 − 3 − 5 = 32). v1.1.0: tidak ada butir.
- Langkah yang disarankan dijalankan: ekspor 24/9 + `impor-pesanan --ya` → `dibatalkan` 0→1, stok KH 11→13, ETM 24→28,
  AM600 23→24 (tepat qty nota yang di-void) → butir hilang. **Terbukti benar.**
- Mingguan berjalan (21–26/9) juga memuat butir. Omzet 25/9 = Rp 123.000 (175.000 − 24.000 − 28.000), cocok hitung mandiri.
- **N3b (Rendah, baru):** butir hanya muncul di laporan **tanggal void**. Laporan harian 26/9 (stok masih salah bila
  langkah belum dijalankan) sudah diam. Jadwal harian 21.00 akan menangkapnya sekali; bila pemilik melewatkan pesan itu,
  pengingat berikutnya baru di laporan mingguan Senin. `SKILL.md` Cara kerja §3 tidak menyebut batas "hanya di periode
  void". Saran: periksa void dalam jendela beberapa hari ke belakang, atau sebut batasnya di SKILL.md.
- Catatan N6 (terbuka, keputusan desain): pada kasus ini baris "Nota: 1 (+3 dibatalkan) | rata-rata Rp 123.000"
  lebih mencolok karena 2 void berasal dari nota kemarin, sementara 3 nota 25/9 sah. Tetap angka resmi kasir-lokal.

### N4 — referensi OpenClaw
Baris status di `references/openclaw-jadwal.md` kini "✅ Bagian PROSPEK… diuji ulang oleh penguji independen 25
September 2026 (OpenClaw 2026.9.6…)" dan merujuk HASIL-UJI. Sesuai isi HASIL-UJI bagian Uji v1.1.0. §0 aturan
penerima selaras dengan SKILL.md. Tidak ada klaim platform baru (Telegram sampai & Windows tetap ⚠️).

### N5 — `--samarkan`
07.30, `--samarkan`: v1.1.1 "Belum absen tanpa keterangan (3): T., Y., M. Tanyakan & catat izin/alpa." v1.1.0: "M..".
Tanpa `--samarkan`: "…Mira. Tanyakan" (titik tunggal).

### N-baru — `--samarkan` diteruskan ke `crm.py rekap`
`--crm-script` diarahkan ke wrapper yang mencatat argv lalu menjalankan `crm.py` asli:
```
v1.1.0 tanpa/dengan --samarkan : rekap --db … --dari 2026-09-25 --sampai 2026-09-25 --hari-ini 2026-09-25 --json
v1.1.1 tanpa --samarkan        : rekap --db … --json
v1.1.1 dengan --samarkan       : rekap --db … --json --samarkan
v1.1.1 mingguan --samarkan     : 2 panggilan (21–27/9 & 14–20/9), keduanya --samarkan
```
JSON `prospek` identik di 4 varian (lama/baru × dengan/tanpa samarkan). Privasi: teks+JSON `--samarkan` tidak memuat
nama/nomor karyawan maupun prospek (grep 11 nama & awalan nomor; satu kecocokan "9000" ternyata angka omzet 90000).

### Order (deal) perlu konfirmasi
- okA: Mbak Nisa (deal) jadwal 24/9, Bu Endah (deal) jadwal 25/9 → PROSPEK "order perlu konfirmasi 2", v1.1.1 butir 7
  "2 order (deal) sudah waktunya dikonfirmasi ke pelanggan. Ketik 'follow-up hari ini'…". v1.1.0: tanpa butir.
- okB: deal dijadwalkan 26/9 (besok) → "order perlu konfirmasi 0", tanpa butir; deal itu dihitung di "besok 1"
  (perilaku crm-wa `kelompok_followup`, sama di kedua versi).
- Angka butir = `crm.py rekap --json` langsung (`order_perlu_konfirmasi: 2`).

## Verifikasi angka independen (`verif.py` di scratchpad)
Omzet & jumlah nota/void dihitung dari `kasir.db` mentah (`mode=ro`, jumlah `total` nota per tanggal nota); PROSPEK
dari `crm.db` mentah (lead_masuk, deal jumlah/nilai, kohort lead/deal/batal, follow-up terlambat/hari ini/besok, order
perlu konfirmasi) tanpa memanggil kode `crm.py`/`laporan.py`. Bagian JSON `penjualan`, `stok`, `kehadiran`,
`tagihan`, `prospek`, `periode`, `alat` dibandingkan v1.1.0 vs v1.1.1 (tanpa stempel waktu & path salinan).

| Data | Mode | v1.1.0 = v1.1.1 | Omzet laporan = mandiri | PROSPEK |
|---|---|---|---|---|
| master | harian 25/9 | ya | 175.000 = 175.000 | cocok |
| master | harian 24/9 | ya | 140.000 = 140.000 | cocok |
| master | harian 25/9 `--samarkan` | ya | 175.000 | cocok |
| master | mingguan berjalan 21–26/9 | ya | 315.000 = 315.000 | cocok |
| master | mingguan lalu 21–27/9 (Senin 28/9) | ya | 315.000 | cocok |
| n1 | harian 06.55 | ya | 175.000 | cocok |
| n3 | harian 25/9 (void lintas hari) | ya | 123.000 = 123.000 | cocok |
| n3 | mingguan `--samarkan` | ya | 263.000 = 263.000 | cocok |
| okA | harian (2 order jatuh tempo) | ya | 175.000 | cocok |
| okB | harian `--samarkan` | ya | 175.000 | cocok |

**10/10 kasus: 0 beda** antar versi dan terhadap hitung mandiri. Hitung tangan 25/9: 5×18.000 (QRIS) + (15.000 +
2×6.000) + (2×12.000 + 2×17.000) = 175.000; tunai 85.000; rata-rata 175.000/3 = 58.333 (dibulatkan) — sama dengan teks.
Catatan penguji: rancangan awal verifier salah mendefinisikan "besok" (hanya prospek terbuka); setelah membaca
`crm.py kelompok_followup`, deal berjadwal besok ikut "besok". Ini definisi crm-wa (docstring-nya hanya menyebut
prospek & pelanggan selesai — ketidakselarasan kecil milik crm-wa, di luar cakupan skill ini).

## Keamanan & hanya-baca
sha256 seluruh `*.db` (kasir, stok, absensi, crm) sebelum vs sesudah 4 laporan (v1.1.0/v1.1.1, harian `--samarkan`
& mingguan): **sama**.

## Perintah otomatis
- `python3 tests/uji_regresi.py` (salinan scratchpad, identik dengan repo) → **Ran 53 tests … OK**.
- `python3 scripts/validate.py --skill laporan-harian-usaha` (dari `/home/user/Skills`) → "✅ 1 skill valid, 72 baris
  katalog sesuai."

## Temuan terbuka setelah uji ini
| ID | Keparahan | Ringkas |
|---|---|---|
| N3b | Rendah (baru) | Pengingat void-setelah-impor hanya di laporan tanggal void; hari berikutnya diam walau stok masih salah. Batas tidak disebut di SKILL.md |
| N1 per-shift | Rendah (diketahui) | Shift siang ikut alarm antara jam masuk shift pagi dan shift siang |
| N6 | Kosmetik (keputusan desain) | "Nota sah"/rata-rata per nota saat void lintas hari |
| K1 | Kosmetik (keputusan desain) | Inisial bentrok pada `--samarkan` |
