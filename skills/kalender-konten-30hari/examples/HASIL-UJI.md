# Hasil Uji — kalender-konten-30hari

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** SKILL.md, README.md, ATTRIBUTION.md, `references/momen-dan-pilar.md`, `scripts/buat_kalender.py`
- **Metode:** 5 skenario (01–05) + uji A/B (00), berperan sebagai agent yang memuat SKILL.md. Script dijalankan sungguhan di
  `/tmp/uji-kalender-konten-30hari/` (kerangka `--format json` → diisi agent → `--isi` ke md/csv). Nama hari diverifikasi dengan **rumus Zeller**
  (implementasi terpisah, tanpa `datetime`).

## Audit keamanan
- Script hanya memakai `argparse, csv, io, json, sys, datetime`. Tidak ada akses jaringan, subprocess, penghapusan file, atau pembacaan kredensial.
  Menulis file hanya ke `--output`.
- SKILL.md/references: tidak ada prompt injection. **Aman.**

## Verifikasi tanggal & fakta (independen)
- Nama hari: 7 rentang diuji (Okt 2026, Nov 2026, 28 Sep–27 Okt 2026, 15 Sep–14 Okt 2026, 15 Des 2026–13 Jan 2027 lintas tahun, 1–31 Okt 2026,
  15 Feb–5 Mar 2028 dengan 29 Feb) → **0 salah** dari 211 baris.
- Hari peringatan (30 Sep, 1 Okt, 10 Nov) **tidak pernah** mendapat pilar promo, termasuk saat bertabrakan dengan gajian (1 Okt, 30 Sep dengan
  `--gajian 30`) dan dengan momen pengguna bertipe promo (10 Nov) ✔.
- Tanggal momen tetap dicek: Hari Batik 2 Okt, Hari Santri 22 Okt, Sumpah Pemuda 28 Okt, Hari Pahlawan 10 Nov, Hari Guru 25 Nov, Hari Ibu 22 Des,
  Hari Anak 23 Jul, Hardiknas 2 Mei, Hari Pelanggan Nasional 4 Sep ✔. Perkiraan Imlek 2027 (±6 Feb), awal Ramadan 1448 H (±8 Feb 2027), Idulfitri
  (±10 Mar 2027) masuk akal dan sudah diberi label "BELUM TERVERIFIKASI / cek SKB 3 Menteri" ✔.
- Default "bulan depan" dari `--hari-ini 2026-09-23` → 1 Okt 2026; dari 2026-12-23 → 1 Jan 2027 ✔.
- Data rusak: tanggal 30 Feb, `--hari 5`, pilar duplikat/tunggal, JSON rusak/kosong, `--momen` tanpa nama, pemisah `|` → semua ditolak dengan `ERROR:` jelas.
  `--isi` membetulkan nama hari yang salah ("Senin" → "Kamis" untuk 1 Okt 2026) ✔. CSV `;` dengan BOM, sel berisi `,;"` di-quote benar ✔.

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 9 | Kalender/jadwal/content plan, Indonesia & Inggris, batas dengan caption jelas. |
| Kemudahan awam | 8 | Satu kalimat cukup; tabel & CSV siap spreadsheet. Tabel 11 kolom agak lebar dibaca di HP. |
| Kualitas output | 8 | Ide spesifik per hari, hook ≤ 10 kata, momen lokal, kapasitas produksi dihormati. A/B: jelas lebih baik. |
| Akurasi (angka/fakta) | 9 | Tanggal & hari 100% benar; momen tetap benar; tanggal bergerak tidak ditebak. |
| Penanganan input kurang | 9 | S4 tanya sekali + default; S3 langsung kerja dengan asumsi. |
| Penanganan di luar cakupan | 9 | S5 jujur soal analitik & posting otomatis, menawarkan fungsi inti. |
| Keamanan | 10 | Tidak ada risiko teknis. |

## SKOR AKHIR: 8 / 10 → **LULUS**

Tidak ada cacat berat: tanggal/hari selalu benar dan hari peringatan tidak pernah dipromosikan pada kerangka dari script. Kelemahan utamanya
ada di langkah ekspor `--isi` yang tidak lagi menjaga aturan hari peringatan, dan rotasi pilar yang masih menaruh promo di tanggal tua.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
- **S1 — Mode `--isi` tidak memeriksa ulang promo di hari peringatan** (`baca_isi`, baris 169–197). JSON yang diedit agent dengan
  `Pilar: "Menu & Promo"` dan ide "Diskon 50% semua menu" pada 2026-10-01 diekspor tanpa peringatan apa pun (hanya muncul peringatan porsi promo).
  Padahal SKILL.md langkah 4 menyebut `--isi` sebagai tahap "memeriksa". *Saran:* di `baca_isi`, hitung ulang `momen_hari()` per tanggal; bila ada
  tipe `peringatan` dan pilar mengandung "promo/jual" **atau** ide mengandung kata "diskon/promo/sale/gratis", cetak `PERINGATAN: baris N (tanggal)
  adalah hari peringatan — hindari promo`. Sekalian isi ulang kolom `Momen` bila kosong.
- **S2 — Promo pengguna yang jatuh di hari peringatan dibuang diam-diam** (`susun`, baris 144: `paksa_promo[i] and not larang_promo[i]`). Uji:
  `--momen "2026-11-10:Diskon 10.11:promo"` → baris 10 Nov menjadi "Testimoni" tanpa pemberitahuan; pengguna mengira promonya terjadwal.
  *Saran:* tambahkan ke `ringkasan["peringatan"]`: "Momen promo '<nama>' pada <tanggal> bertepatan dengan <hari peringatan>; tidak dijadwalkan sebagai promo — geser tanggalnya."
- **S3 — Rotasi pilar menaruh promo di tanggal tua** (`susun`, baris 148–155). Contoh: 21 Okt, 21 Nov, 21 & 23 Des 2026 mendapat pilar promo, padahal
  `references/momen-dan-pilar.md` §2 menulis tanggal tua "bukan hard-selling". *Saran:* perlakukan momen "Tanggal tua" seperti `dekat_promo` (lewati kandidat pilar promo).

### Ringan
- **R1 — Default 30 hari vs nama bulan.** "Kalender Oktober" dengan default berhenti di 30 Okt (tanggal 31 hilang). *Saran:* tabel Input SKILL.md:
  "Jika pengguna menyebut nama bulan, pakai jumlah hari bulan itu (`--hari 31`)", atau default script = sisa hari bulan kalender.
- **R2 — Tanggal kembar dipaksa promo untuk semua usaha** (baris 118–124). Laundry/warung lokal jarang ikut kampanye marketplace; agent harus menetralkan
  sendiri. *Saran:* opsi `--tanpa-tanggal-kembar` atau tipe "tema" untuk usaha non-marketplace.
- **R3 — Pilar non-promo yang bernuansa jualan (Ulasan/Testimoni) tetap bisa jatuh di hari peringatan.** Script hanya mencegah pilar promo. *Saran:* di
  hari peringatan, pilih pilar edukasi/proses bila ada, dan tulis catatan di kolom Momen (sudah ada) — cukup ditambah di SKILL.md langkah 3.
- **R4 — Kolom Format "Video pendek + Story/Status"** tetap menyebut Status walau platform tanpa WA Status. *Saran:* sesuaikan `format_untuk()` dengan daftar platform.
- **R5 — Kapasitas produksi harus diatur manual di JSON.** *Saran:* opsi `--video-per-minggu N` yang menandai hari lain "Story/Status saja".
- **R6 — README merujuk `CARA-INSTAL.md`, ATTRIBUTION merujuk `LISENSI.txt`** yang tidak ada di folder skill; pastikan ikut paket rilis.

## Uji A/B
Lihat `00-pembanding-tanpa-skill.md`. Tanpa skill: hanya ±16 dari 30 hari terisi ("pola serupa…"), **countdown promo di Hari Pahlawan**, dan 3 promo
karangan. Dengan skill: 30/30 hari, tanggal terverifikasi, tanpa promo di hari peringatan, tanpa promo karangan, plus CSV. **Skill jelas memberi nilai tambah.**
