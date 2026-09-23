# Hasil Uji — broadcast-wa

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** SKILL.md, README.md, ATTRIBUTION.md, `references/aturan-pdp-wa.md`, `scripts/siapkan_broadcast.py`
- **Metode:** 5 skenario (01–05) + uji A/B (00), berperan sebagai agent yang memuat SKILL.md. Script dijalankan sungguhan di
  `/tmp/uji-broadcast-wa/` dengan data fiktif (nomor 0812-0000-xxxx), lalu hasilnya dicek dengan python terpisah.

## Audit keamanan
- `siapkan_broadcast.py` hanya memakai `argparse, csv, json, re, sys, datetime, urllib.parse.quote`. `quote` hanya untuk
  menyusun teks link wa.me; **tidak ada pengiriman pesan, tidak ada socket/HTTP, tidak ada subprocess**, tidak membaca
  kredensial, tidak menghapus file. Satu-satunya tulisan file adalah `--output`.
- SKILL.md/README/references: tidak ada prompt injection; ada penolakan eksplisit untuk database beli & WA mod.
- Catatan: output berisi data pribadi; SKILL.md sudah meminta agent tidak menempel daftar nomor di chat. **Aman secara teknis**,
  tetapi ada 2 celah pada filter persetujuan/berhenti (lihat cacat berat).

## Verifikasi angka & data (independen)
- S1 (40 baris fiktif): script 25 siap kirim; hitung ulang dengan python terpisah → 25, dan daftar nomor **identik**.
- Normalisasi nomor (dibandingkan dengan fungsi independen): `0812-0000-0001`, `+62 812 0000 0002`, `6281200000003`,
  `81200000004` (nol hilang di Excel), `(0812) 0000-0012`, `+62 (0)812-0000-0014` → semua `62812…` ✔. `021-…` (telepon rumah),
  `123`, `0812000`, `8.12E+11` (format ilmiah Excel) → ditolak sebagai tidak valid ✔. `0062812…` ditolak (seharusnya bisa diterima; ringan).
- Persetujuan: `ya`, `Ya`, `YA ` (spasi), `setuju`, `1` lolos; `tidak`, kosong → dilewati ✔.
- Jadwal: batch 20, jeda 60 dtk, jeda batch 30 mnt, maks 100/hari, jendela 09:00–20:00 → dicek manual (10:00→10:19, 10:50; 100/100/50 per hari; 19:59 & 20:00 hari ini, sisanya besok 09:00) ✔.
- Data rusak: file kosong, tanpa kolom persetujuan, variasi tanpa teks berhenti, placeholder tak dikenal (`{kecamatan}`),
  file bukan UTF-8, pemisah `;` → semua ditangani dengan pesan `ERROR:` yang jelas / terbaca benar ✔.
- **Temuan salah (cacat berat):** kolom `Berhenti` berisi `STOP` atau tanggal → kontak **tetap** masuk daftar kirim;
  nomor yang punya baris `Berhenti = ya` tetap dikirimi bila ada baris duplikat tanpa tanda berhenti (lihat B1, B2).

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 9 | Kata kunci Indonesia & Inggris lengkap, batas dengan balas-chat-cs/tagih-piutang jelas. |
| Kemudahan awam | 8 | Cukup satu kalimat; ringkasan & cara pakai link wa.me jelas. Pengguna tetap perlu CSV UTF-8. |
| Kualitas output | 9 | Variasi natural, personal, opt-out selalu ada, jadwal masuk akal. A/B: jelas lebih baik. |
| Akurasi (angka/fakta) | 7 | Hitungan & normalisasi benar; tetapi 2 celah filter berhenti membuat daftar kirim bisa salah. |
| Penanganan input kurang | 9 | Tanya sekali, 5 poin, ada jalan cepat (S4); langsung kerja bila info wajib lengkap (S3). |
| Penanganan di luar cakupan | 9 | Menolak database beli, WA mod, dan penghapusan opt-out dengan sopan + alternatif sah (S5). |
| Keamanan | 6 | Tidak ada akses jaringan/pengiriman. Namun janji inti "membuang yang minta berhenti" bisa gagal → risiko UU PDP. |

## SKOR AKHIR: 6 / 10 → **REVISI**

Kualitas teks dan alurnya sangat baik, dan uji A/B menunjukkan nilai tambah yang jelas. Tetapi fungsi yang paling
dijual ("hanya kontak yang setuju, membuang yang minta berhenti") bisa gagal pada format data yang sangat umum
(kolom Berhenti diisi "STOP"/tanggal, atau pelanggan tercatat dua kali). Mengirim promo ke orang yang sudah minta berhenti
adalah pelanggaran yang dirasakan pembeli langsung → cacat berat, skor dibatasi ≤ 6. Perbaikannya kecil.

## Daftar cacat & saran perbaikan

### Berat
- **B1 — Kolom Berhenti hanya dikenali bila isinya "ya/1/setuju…"** (`siapkan_broadcast.py` baris 227:
  `if k_berhenti and (b.get(k_berhenti) or "").strip().lower() in YA`). Isi "STOP", "berhenti", "x", "unsub", atau tanggal
  berhenti (format yang disarankan banyak orang) **lolos** dan dikirimi promo. Terbukti: kontak "Sari" (Berhenti = STOP) dan
  "Tono" (Berhenti = 2026-09-01) masuk `out.csv`.
  *Saran:* anggap berhenti bila sel **tidak kosong** dan bukan salah satu dari `{"tidak","no","n","0","-","false"}`:
  `nilai = (...).strip().lower(); if k_berhenti and nilai and nilai not in {"tidak","no","n","0","-","false"}:`.
  Samakan juga penjelasan di `references/aturan-pdp-wa.md` §1 (kolom Berhenti).
- **B2 — Tanda berhenti/tidak setuju bisa "tertimpa" baris duplikat** (baris 222–247). Nomor yang dilewati karena berhenti
  tidak dimasukkan ke himpunan penolakan; baris berikutnya dengan nomor sama tanpa tanda berhenti tetap lolos. Terbukti:
  "Hadi" baris 15 (Berhenti = ya) dilewati, "Hadi Dup" baris 16 (nomor sama) **dikirimi**.
  *Saran:* lakukan pre-pass sebelum loop utama: kumpulkan semua nomor dengan tanda berhenti (dan sebaiknya juga yang
  `Persetujuan = tidak`) ke set `berhenti`; lalu di loop utama tolak nomor yang ada di set itu. Tambahkan alasan
  "nomor ini pernah minta berhenti di baris lain".

### Sedang
- **S1 — Jadwal tidak menghindari jam salat Jumat** (`geser_ke_jendela`, baris 260–266), padahal
  `references/aturan-pdp-wa.md` §4 menyarankan menghindari ±11.30–13.00 Jumat. Uji: 100 kontak mulai Jumat 10.00 →
  sebagian pesan terjadwal 11.30–13.00.
  *Saran:* tambah opsi `--hindari-jumatan` (default aktif) yang menggeser waktu di jendela itu ke 13.00; atau minimal
  tambahkan di SKILL.md langkah 4: "Jika jadwal jatuh Jumat 11.30–13.00, laporkan ke pengguna / geser `--mulai`".

### Ringan
- **R1 — Cek teks berhenti terlalu longgar** (baris 43, `POLA_OPTOUT`): kata "non-stop" ("promo non-stop") dianggap sudah
  ada opt-out. *Saran:* wajibkan pola kalimat, mis. `balas\s+(stop|berhenti)|tidak (ingin|mau) (menerima|dapat)`.
- **R2 — SKILL.md langkah 2 mewajibkan `{sapaan} {nama}` di setiap variasi**, bertentangan dengan catatan daftar siaran di
  bagian Format output (S2). *Saran:* tulis "wajib `{sapaan} {nama}`, kecuali versi untuk daftar siaran".
- **R3 — `--saya-pastikan-semua-setuju` tanpa pagar di SKILL.md.** *Saran:* tambahkan "Jangan pakai flag ini jika pengguna
  menyebut nomor berasal dari database beli, grup, atau sumber tanpa izin."
- **R4 — Awalan `0062…` ditolak** (`rapikan_nomor`, baris 92–102). *Saran:* tangani `d.startswith("00")` → buang "00".
- **R5 — Nama hanya berisi sapaan** ("Bu") menghasilkan "Kak Bu". *Saran:* bila hanya satu kata dan itu sapaan, pakai sapaan itu dan nama kosong.
- **R6 — README merujuk `CARA-INSTAL.md` dan ATTRIBUTION merujuk `LISENSI.txt`** yang tidak ada di folder skill; pastikan ikut paket rilis.

## Uji A/B
Lihat `00-pembanding-tanpa-skill.md`. Tanpa skill: 1 pesan generik tanpa opt-out, klaim "stok terbatas" karangan, dan
saran mengimpor **semua** nomor ke daftar siaran. Dengan skill: 3 variasi personal + opt-out + filter persetujuan
(25/40) + jadwal + link wa.me. **Skill jelas memberi nilai tambah** — skor tidak dibatasi oleh A/B, tetapi oleh B1–B2.
