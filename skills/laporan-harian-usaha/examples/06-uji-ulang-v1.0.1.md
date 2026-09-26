# Skenario 06 — Uji ulang v1.0.1 (setelah revisi)

**Penguji:** agent penguji independen (simulasi, Claude Code). Bukan pembuat skill dan bukan yang merevisinya. Tanggal 2026-09-24. Semua nama & data fiktif.

## Lingkungan
- Skill + 4 alat (kasir-lokal, buku-stok, absensi-lokal, pengingat-follow-up) **disalin** ke `<uji2>/skills/` (scratchpad). Tidak ada yang dipasang di `.claude/skills` repo; `~/KomunitechData` asli tidak ada dan tidak disentuh.
- Setiap data uji punya HOME palsu, `KOMUNITECH_DATA=<akar>/data`, folder kerja `<akar>/kerja`, `TZ=Asia/Jakarta` (dan `UTC` untuk uji zona). Variabel `KOMUNITECH_*_DB` dibuang.
- Data dibuat dengan **script resmi** tiap alat: kafe 4 alat ("Kedai Kopi Senja", sama dengan skenario 01–02: 18 nota 8–24 Sep, void N-260924-0006, retur 1 es teh, selisih kas −12.000; 6 karyawan; 5 pengingat) dan toko online hanya buku-stok (skenario 03). Script pembuat data = milik penguji v1.0.0 (bukan pembuat skill), path diarahkan ke salinan baru.
- Kasus tambahan dibuat di **salinan** folder kafe (`s1a`, `s1b`, `s1d`, `s1e`, `s1g`, `r1e`, `r1s`, `r3`, `r4`, `r4b`, `priv`), jadi data kafe/toko asli uji tetap utuh.
- Hitung ulang independen: `hitung_ulang.py` (query SQLite `mode=ro` + `Fraction`), tidak mengimpor kode `laporan.py` kecuali untuk memanggil fungsi yang diuji (`persen`, `cek_impor_kasir_ke_stok`).

## 1. Verifikasi klaim perbaikan

### S1 (sedang) — impor kasir ke buku-stok per nomor nota → **TERBUKTI**
Nota 24/9: 7 nota jual, 1 di-void (N-260924-0006) → 6 nota sah.

| Kasus | Cara membuat (script resmi) | Acuan independen | Hasil laporan | Cocok |
|---|---|---|---|---|
| Impor nol | tidak ada impor tgl 24 | 6 dari 6 | `6 dari 6 nota kasir tanggal 2026-09-24 belum diimpor ke buku-stok` | ✅ |
| Impor **sebagian** (repro 04-G) | `kasir.py ekspor --format buku-stok --tanggal 2026-09-24` → sisakan baris N-260924-0001 → `stok.py impor-pesanan … --ya` | 5 dari 6 | `5 dari 6 nota kasir tanggal 2026-09-24 belum diimpor …` | ✅ (v1.0.0: diam) |
| Impor penuh | file ekspor utuh (termasuk baris void "Dibatalkan") → `impor-pesanan --ya` | 0 | tidak ada butir "diimpor" | ✅ |
| Nota void | N-260924-0006 berstatus Dibatalkan → buku-stok tidak membuat baris `pesanan` | tidak dihitung | tidak dihitung "belum diimpor" (6, bukan 7) | ✅ |
| Nota **retur penuh** | `kasir.py retur --nota N-260924-0003 --item "1 matcha latte" --item "1 air mineral"` | nota tetap sah (diekspor "Selesai") | sebelum impor: 6 dari 6; setelah impor penuh: tidak ada butir | ✅ konsisten dengan ekspor kasir |
| Void **setelah** impor (nota 23/9 di-void 24/9) | impor 23/9 sudah ada → `kasir.py void --nota N-260923-0002` | — | laporan 23/9: tidak ada butir apa pun | ⚠️ lihat N3 |
| Mingguan 14–20/9 | tidak pernah diimpor | 6 nota di 5 tanggal | `6 dari 6 nota kasir tanggal 2026-09-14, …, 2026-09-20 belum diimpor` | ✅ |

**Struktur tabel berbeda (harus dilewati, bukan crash)** — fungsi `cek_impor_kasir_ke_stok` dipanggil langsung pada DB rakitan:

| Kasus | Hasil |
|---|---|
| `nota` tanpa kolom `ref_nota_id` / kolom `waktu` diganti nama / tabel `nota` tidak ada | `None` + catatan "struktur tabel nota kasir berubah" ✅ |
| `pesanan` tanpa `no_pesanan` / tabel `pesanan` tidak ada / file stok bukan SQLite | `None` + catatan "struktur tabel pesanan berubah" ✅ |
| Ujung ke ujung: `pesanan.no_pesanan` di-rename di DB buku-stok | exit 0, laporan lengkap, butir impor tidak muncul; `catatan` JSON berisi alasan ✅ — **tetapi teks laporan tidak menyebut cek dilewati** (N2) |

Tidak ada crash di semua kasus.

### R1 — tidak absen tanpa keterangan masuk PERLU PERHATIAN → **TERBUKTI** (dengan efek samping N1)
- 24/9 21.30: `5. Belum absen tanpa keterangan (1): Tari. Tanyakan & catat izin/alpa.` ✅
- Tanggal lampau 10/9: `Tidak absen & tanpa keterangan (1): Tari.` ✅
- `--samarkan`: `T.` (0 nama asli di teks + JSON) ✅; kosmetik: tertulis `T.. Tanyakan` (titik ganda).
- Keterbatasan shift bertahap yang diakui **terbukti ada**: shift SORE 14.00 (Rudi), laporan 10.00 → `Belum absen tanpa keterangan (1): Rudi`.

### R2 — sebelum jam masuk paling awal → **TERBUKTI untuk kasus "belum ada yang tap"**
| `--sekarang` (25/9) | PERLU PERHATIAN |
|---|---|
| 00.30, 07.30, 07.59 | `Belum waktunya absen (jadwal mulai 08.00).` ✅ |
| 08.00, 08.30 | `Belum ada satu pun data absen hari itu…` (benar: jadwal sudah mulai) ✅ |
| 07.50, **satu karyawan sudah tap 07.45** | `Belum absen tanpa keterangan (5): Lala, Yoga, Nisa, Fajar, Tari. Tanyakan & catat izin/alpa.` ❌ alarm palsu (N1) |

### R3 — pesan zona waktu → **TERBUKTI**
- Kasir `atur --zona WITA` (info: `Asia/Makassar`), laporan `--tz` default → `Toko diatur zona Asia/Makassar (WITA) tapi laporan memakai --tz Asia/Jakarta (WIB)… pakai --tz Asia/Makassar` ✅. Dengan `--tz Asia/Makassar` / `WITA` → peringatan hilang ✅.
- Komputer `TZ=UTC` + absensi → `Jam komputer ini bukan Asia/Jakarta (selisih 7 jam). absensi-lokal mencatat jam tap menurut jam komputer…` (tidak lagi menyebut kasir) ✅. Tanpa absensi (`--tanpa absensi`) → tidak muncul ✅.

### R4 — pesan error memakai path asli → **TERBUKTI**
- absensi 0 byte: `File <akar>/data/absensi/absensi.db tidak bisa dibaca…` ✅; kasir 0 byte & stok 0 byte: path asli ✅. Kasir/stok berisi sampah: "file bukan database atau rusak… Pulihkan dari folder backup" ✅. 0 teks `laporan-usaha-` di output; 0 folder sementara tersisa. File rusak tetap 0 byte/tidak berubah.

### R5 — penerima tambahan → **SEBAGIAN**
SKILL.md (baris 21, 68, 122, 129) jelas: pemilik bersama/pengelola yang **ditunjuk eksplisit**, chat pribadi, tanpa grup/broadcast. Tetapi `references/openclaw-jadwal.md` §0 (yang wajib diikuti di Langkah C) masih: "`--to` selalu ID chat **pemilik**", WhatsApp "(2) laporan hanya ke pemilik sendiri", dan "tidak ke … karyawan" (padahal pengelola bisa karyawan). Tidak ada contoh cara membuat jadwal kedua untuk penerima lain (N4).

### Kosmetik
- Minus ganda: `Retur 1 | void 1 (Rp 30.000)` dan `Ada 1 void & 1 retur (Rp 30.000)` ✅
- Label pajak: `Per metode bayar (termasuk pajak/service, omzet di atas belum termasuk):` hanya muncul bila uang diterima ≠ omzet ✅
- `--tz Asia/Tokyo | UTC | Europe/London` → exit 2 + pesan (JSON `ok:false`) ✅; `asia/pontianak` diterima ✅; `--tz ""` = default WIB (wajar).
- K1 (`--samarkan` bentrok nama berawalan sama) — belum diperbaiki, sesuai pernyataan.

## 2. Regresi (skenario 01–03 diulang, dihitung ulang independen)

| Skenario | Angka | Laporan | Acuan independen | Cocok |
|---|---|---|---|---|
| 01 harian 24/9 | Omzet / uang diterima | 346.400 / 381.040 | 346.400 / 381.040 | ✅ |
| | Nota sah, rata-rata | 6 (+1 void), 57.733 | 6, 346.400/6 = 57.733,3 → 57.733 | ✅ |
| | vs 23/9, vs 17/9 | 96.000 naik 260,8%; 77.000 naik 349,9% | 260,83…→260,8; 349,87…→349,9 | ✅ |
| | Per metode | Tunai 203.100, QRIS 125.140, Transfer 52.800 | tunai = bayar − kembalian (279.000 − 75.900) | ✅ |
| | Terlaris 5 | KSA 5/100.000 … RTB 3/44.800 | sama | ✅ |
| | Retur+void Rp | 30.000 | 20.000 + 10.000 | ✅ |
| | Stok & restock | RTB −5 MINUS 13, TEH 0 HABIS 10, MCH 4 MENIPIS 2 | sama | ✅ |
| | Kehadiran | hadir 3/6, Lala 17 mnt, Yoga 5 mnt, Nisa sakit, Fajar alpa, Tari, Yoga pulang 19.40 +2j40m | sama (dari data yang dimasukkan) | ✅ |
| | Tagihan | #1 lewat 6 hari; #2, #5 hari ini; #3 besok; tertunggak 4.950.000 | sama | ✅ |
| 02 mingguan 14–20/9 | Omzet, diterima, nota, rata-rata | 372.500 / 409.750 / 6 / 62.083 | sama | ✅ |
| | vs 7–13/9 | 189.000 naik 97,1% | 97,09…→97,1 | ✅ |
| | Kehadiran | 35/36, telat 3× 72 mnt, izin 1, lembur 2 jam | 25+7+40 = 72 | ✅ |
| | Jadwal Senin 07.00 | periode sama 14–20/9, angka penjualan identik | — | ✅ |
| 02b minggu berjalan 21–24/9 | Omzet, nota, rata-rata, pembanding | 442.400 / 8 / 55.300 / vs 14–17/9 192.000 naik 130,4% | sama | ✅ |
| 03 toko (buku-stok saja) 23/9 | Omzet | 390.000 (135.000 offline + 255.000 Shopee; batal & rusak tidak dihitung) | sama | ✅ |
| | Pembanding | 79.000 naik 393,7%; 198.000 naik 97,0% | sama | ✅ |
| | Stok | MASKER-3 HABIS 10, KB-NV-XL MENIPIS 3, KB-HT-L 8/8 MENIPIS | sama | ✅ |

- **Rumus persen:** `persen()` vs acuan `Fraction` (0,05 menjauhi nol): 30.011 kasus (acak termasuk minus + tepi ±0,05) → **0 beda**.
- **Hanya baca:** 12 file data asli uji (DB, backup, DAFTAR.csv) sha256 sebelum = sesudah setelah ±20 kali jalan pada data itu (termasuk DB terkunci). 0 folder `laporan-usaha-*` tersisa.
- **DB terkunci** (`BEGIN EXCLUSIVE`, `--timeout 1`): selesai 1,3 detik, exit 0, kasir "sedang dipakai program lain", alat lain tetap dilaporkan.
- **Privasi:** teks + JSON harian/mingguan (juga data berisi nomor HP di nama & perihal via `--simpan-kontak`) → 0 nama pelanggan, 0 perihal, 0 nomor HP, 0 nama penyetuju lembur, 0 catatan sakit. Tagihan tampil sebagai `#6 piutang Rp 250.000, lewat 4 hari`.
- **Tengah malam WIB:** komputer `TZ=UTC`, `--sekarang 2026-09-24T17:30Z` → laporan **Jumat 25 September**, "Dibuat 2026-09-25 00:30 WIB"; `--tanggal kemarin` → 24/9. Tanpa `--sekarang` di komputer UTC → tanggal WIB benar. `--tanggal 2026-09-25` pada 24/9 → exit 2.
- `tests/uji_regresi.py` → **39 tes OK** (26 detik). `scripts/validate.py` → 53 skill valid. `scripts/uji_openclaw.sh` → OpenClaw 2026.9.6, semua skill terbaca & siap.

**Tidak ada regresi angka.** Satu regresi perilaku kecil (N1) muncul dari perubahan R1.

## 3. Cacat tersisa / temuan baru

| ID | Keparahan | Lokasi | Temuan & reproduksi |
|---|---|---|---|
| N1 | Rendah | `scripts/laporan.py:762-774` | Pengecualian "belum waktunya" hanya berlaku bila **belum ada seorang pun** yang tap. Satu karyawan datang lebih awal → sisanya ditulis `Belum absen tanpa keterangan (5): … Tanyakan & catat izin/alpa.` sebelum jam masuk. Repro: salinan kafe → `absensi.py catat --karyawan Dimas --tanggal 2026-09-25 --masuk 07.45 --ya` → `laporan.py --sekarang 2026-09-25T07:50+07:00`. Di v1.0.0 butir ini tidak muncul sama sekali (akibat perubahan R1). Dampak: laporan pagi/ad-hoc (jadwal 21.00 tidak terpengaruh); saran "catat alpa" bisa menyesatkan. Saran: jangan masukkan ke PERLU PERHATIAN bila `hari_ini` dan jam < jadwal masuk paling awal. |
| N2 | Rendah | `laporan.py:372, 443, 456, 710`; `teks_laporan` | Bila cek impor / selisih kas **dilewati** karena struktur tabel berubah, alasannya hanya ada di `catatan` JSON; teks yang dikirim ke Telegram diam (pemilik mengira tidak ada masalah). SKILL.md menyebut "dilewati dengan catatan". Repro: rename `pesanan.no_pesanan` di salinan stok.db → teks tanpa butir impor dan tanpa catatan. |
| N3 | Rendah | `cek_impor_kasir_ke_stok` | Nota yang di-void **setelah** diimpor (stok di buku-stok masih terpotong sampai ekspor-impor ulang) tidak terdeteksi. Repro: salinan kafe (23/9 sudah diimpor) → `kasir.py void --nota N-260923-0002 --waktu "2026-09-24 20:30" --ya` → laporan 23/9 & 24/9 tanpa butir "impor ulang". Di luar klaim S1; alat kasir sendiri memberi catatan saat void. |
| N4 | Rendah | `references/openclaw-jadwal.md:14-16` | Tidak selaras dengan R5 di SKILL.md (lihat di atas). |
| N5 | Kosmetik | `laporan.py:773` + `inisial()` | `--samarkan`: `T.. Tanyakan` (titik ganda). |
| N6 | Kosmetik (lama) | aturan rata-rata | Void lintas hari (nota 23/9 di-void 24/9): laporan 24/9 menulis `Nota: 5 (+2 dibatalkan)` & rata-rata 64.480, sementara butir impor menyebut "6 dari 6 nota". Sesuai rumus tertulis (nota jual − nota void pada periode), tetapi dua angka nota di satu laporan bisa membingungkan. |
| K1 | Kosmetik (diketahui) | `inisial()` | `--samarkan` bentrok untuk nama berawalan sama. |

Tidak ada cacat tinggi atau sedang. Tidak ada angka salah, tidak ada penulisan ke data asli, tidak ada kebocoran data pelanggan.
