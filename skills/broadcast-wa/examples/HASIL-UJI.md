# Hasil Uji — broadcast-wa v1.0.2 (uji ulang ke-2)

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** v1.0.2 (commit `9df48c8`) — SKILL.md, README.md, ATTRIBUTION.md, `references/aturan-pdp-wa.md`,
  `scripts/siapkan_broadcast.py`, `scripts/uji_regresi.py`.
- **Riwayat:** v1.0.0 skor 6 (B1, B2) → v1.0.1 skor 6 (B1/B2 beres, B3 baru: daftar berhenti bercatatan dibuang diam-diam)
  → v1.0.2 (uji ini).
- **Metode:** data v1.0.1 dijalankan ulang (`/tmp/uji-broadcast-wa-v101/`: file kontak nakal 55 baris, stop.txt, stop bercatatan,
  data S1 40 baris, 120 kontak untuk jadwal Jumat) + data baru rancangan penguji (`/tmp/uji-broadcast-wa-v102/`): stop.txt
  24 baris bercatatan untuk 26 nomor sasaran, 19 teks berhenti (9 palsu, 10 sah), 29 nama bergelar/berkombinasi. Harapan
  ditulis sebelum script dijalankan; daftar kirim dicocokkan dengan python terpisah. Skenario 01–05, A/B (00) dan banding
  pesaing (00) diperiksa ulang terhadap SKILL.md v1.0.2.

## Audit keamanan
- Impor script tetap `argparse, csv, json, re, sys, datetime, urllib.parse.quote`. Tidak ada socket/HTTP, subprocess, `eval/exec`,
  penghapusan file, atau pembacaan kredensial. **Tidak ada pengiriman pesan dan tidak ada akses jaringan.**
- SKILL.md v1.0.2: tambahan format stop.txt, status PERIKSA DULU, laporan sel tidak baku, dan konfirmasi jumlah penerima
  sebelum kirim. Tidak ada prompt injection; pagar database beli/WA mod/opt-out tetap ada.

## Status cacat v1.0.1
| Cacat v1.0.1 | Status v1.0.2 | Bukti |
|---|---|---|
| B3 — daftar berhenti bercatatan dibuang diam-diam | **Sebagian** | stop bercatatan v1.0.1 (4 baris) kini 4/4 dikecualikan; data baru 17/24 baris benar, 2 ditandai PERIKSA DULU, **5 salah baca tanpa peringatan** (lihat B3′) |
| S-1 — opt-out salah lolos ("tidak mau dapat diskon", "untuk berhenti pusing") | **Beres** | 6/6 frasa palsu lama & baru ditolak; sisa hanya kalimat yang sengaja menyesatkan (R-2) |
| S-2 — gelar jadi nama ("Bu HJ.", "Kak Dr.") | **Beres** (mode default) | 22/29 variasi benar termasuk gelar bertumpuk; sisa: tanpa spasi, Ny./Tn./Muh. (R-3) |
| R-1 — sapaan bercampur "Kamu menerima …" | **Beres** | SKILL.md & references diganti "Pesan ini dikirim karena {sapaan} …"; contoh 01–03 disesuaikan |
| R-2 — nilai tidak baku dilaporkan umum | **Beres** | "ya (lisan)", "masih aktif", "N/A" kini dilaporkan per nilai & baris |
| R-3 — tanpa konfirmasi jumlah penerima | **Beres** | SKILL.md langkah 4 "Siap kirim ke N kontak?" |

`python3 scripts/uji_regresi.py` → **11/11 OK**.

## Verifikasi angka & data (independen)
- **File kontak nakal 55 baris:** label penguji KIRIM = 26; script v1.0.2 = 26 nomor unik, **identik** (sama dengan v1.0.1).
  Salah kirim 0, terlewat 0. Rincian dilewati 8 + 3 + 5 + 1 + 2 + 1 + 5 + 2 + 1 + 1 = 29 = 55 − 26 ✔.
- **Data S1 40 baris** (dengan Variasi 2 yang diperbarui): 25 siap kirim, status SIAP, nomor identik dengan v1.0.1.
- **Jadwal Jumat:** 120 kontak, jeda 3 menit, mulai Jumat 10.00 → 10.57 lalu 13.00; 0 pesan di 11.30–13.00 ✔.
- **Daftar berhenti bercatatan (24 baris, 26 nomor):** 19 nomor dikecualikan benar; 7 nomor yang sudah minta berhenti **tetap
  ada di daftar kirim** — 2 dengan status PERIKSA DULU, **5 tanpa peringatan apa pun** (status akan SIAP begitu 2 baris
  bertanda dirapikan). Rincian per baris: `07-uji-daftar-berhenti-gelar-v102.md`.

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 9 | Tetap tepat; batas dengan balas-chat-cs/tagih-piutang jelas. |
| Kemudahan awam | 9 | Status SIAP/PERIKSA DULU, sel tidak baku disebut per baris, konfirmasi jumlah penerima. |
| Kualitas output | 9 | Satu sapaan per pesan, gelar dirapikan, variasi natural. |
| Akurasi (angka/fakta) | 7 | Filter kolom & duplikat tepat 26/26; pembacaan stop.txt masih salah pada catatan angka di belakang nomor. |
| Penanganan input kurang | 9 | Tanya sekali (04), default + asumsi (03). |
| Penanganan di luar cakupan | 9 | Penolakan database beli/WA mod/hapus opt-out tetap baik (05). |
| Keamanan | 7 | Tanpa jaringan/pengiriman. Sisa risiko UU PDP: sebagian kontak di stop.txt tetap terkirimi tanpa tanda (B3′). |

## SKOR AKHIR: 6 / 10 → **REVISI** (satu perbaikan kecil lagi)

v1.0.2 memperbaiki hampir semua temuan: opt-out palsu ditolak, gelar rapi, sapaan konsisten, sel tidak baku dilaporkan,
ada konfirmasi sebelum kirim, dan format catatan paling umum di stop.txt kini terbaca. Namun janji inti "yang minta berhenti
tidak dikirimi lagi" masih bisa gagal **tanpa tanda apa pun** bila admin menulis tanggal atau hitungan tepat di belakang
nomor ("0812 0000 0221 25 September", "0812-0000-0203 (2)") — pola yang sangat wajar. Selama kegagalan senyap ini ada,
cacat tetap berat dan skor dibatasi ≤ 6. Semua kriteria lain sudah ≥ 7; setelah B3′ ditutup, skill ini layak **8–9**.
A/B: skill jelas lebih baik. Banding pesaing: skill kita menang (3 / 6 / **8**).

## Daftar cacat & saran perbaikan

### Berat
- **B3′ — Angka kecil di belakang nomor ikut tergabung ke nomor** (`cari_nomor_di_teks`, baris 124–146: grup angka
  berspasi terus ditambahkan ke `buf` selama grup berikutnya tidak diawali 08/62). Terbukti: `0812 0000 0201 12 Sept 2026`
  → `628120000020112`; `0812-0000-0202 - 3x minta` → `62812000002023`; `0812-0000-0203 (2)` → `62812000002032`;
  `0812 0000 0221 25 September` → `628120000022125`; `0812 0000 0224 - 17 Agustus` → `628120000022417`. Hasil 14–15 digit
  masih lolos `rapikan_nomor`, jadi tidak masuk `daftar_berhenti_tidak_terbaca`, status tetap SIAP, dan kontak tetap dikirimi.
  *Saran (pilih minimal dua):*
  1. Berhenti menambah grup bila `buf` sudah menjadi nomor valid ≥ 12 digit mentah (08xx-xxxx-xxxx) dan grup berikutnya
     ≤ 4 digit, atau bila di antaranya ada `(`, ` - `, atau `x`; pisahkan `(` dari himpunan karakter run di regex baris ~129.
  2. **Jaring pengaman:** setiap nomor dari stop.txt yang **tidak cocok dengan kontak mana pun** di file kontak → masukkan ke
     `daftar_berhenti_tidak_terbaca` (status PERIKSA DULU, "nomor berhenti tidak ditemukan di file kontak — periksa").
     Ini menangkap semua salah baca, apa pun polanya.
  3. Kecualikan juga kontak yang nomornya (format 08…, 8…, 62…) muncul sebagai **substring digit** dari baris stop mana pun.
  Tambahkan 5 baris di atas ke `uji_regresi.py`.

### Sedang
- (tidak ada)

### Ringan
- **R-1 — Baris stop dengan nomor urut di depan** ("5. 0812-…", "1) 0812 …") hanya ditandai PERIKSA DULU; kontaknya tetap ada
  di `broadcast_siap.csv`. *Saran:* buang pola nomor urut `^\s*\d{1,3}[.)]\s+` sebelum ekstraksi, dan/atau terapkan saran B3′-3
  agar kontak itu dikecualikan sambil tetap memberi peringatan.
- **R-2 — Cek opt-out:** salah lolos pada kalimat menyesatkan ("jangan balas STOP ya", "jangan sampai kirim berhenti") dan
  "Ketik stop-motion" (`\b` sesudah "stop" cocok sebelum "-"; baris 45). Salah tolak yang aman: "Balas dengan kata STOP",
  "balas: STOP", "Balas ke nomor ini dengan STOP". *Saran:* tolak bila didahului `jangan( sampai)?`, tambah `(?![-\w])`
  sesudah kata kunci, izinkan `:` dan hingga 4 kata di antara "balas" dan STOP.
- **R-3 — Gelar sisa:** "Hj.Nurul" / "Dr.Rina" (tanpa spasi), "H.M. Yusuf", "Muh.", "Ny." / "Tn." (sebaiknya → Bu/Pak) tidak
  dikenali (`pecah_nama`, baris 148–167); dengan `--nama-lengkap` gelar belakang bertitik tetap terbawa ("S.e.", "M.si.")
  karena `_bersih` (baris 120) tidak membuang titik di tengah. *Saran:* pecah token pada titik sebelum cek gelar, normalisasi
  `re.sub(r"[.,]", "", k)`, tambah `ny→Bu`, `tn→Pak`, `muh/moh/m` (lewati), dan gelar belakang umum (`mm, msi, mpd, mt, skom, spd`).

## Uji A/B
`00-pembanding-tanpa-skill.md`: tanpa skill → 1 pesan generik tanpa opt-out, klaim karangan, saran impor semua nomor. Dengan
skill → 3 variasi personal + opt-out + filter persetujuan (25/40, dijalankan ulang di v1.0.2) + jadwal + wa.me.
**Skill jelas memberi nilai tambah.**

## Uji banding pesaing
`00-banding-pesaing.md`: ChatDaddy `send-broadcast` (alat operasional berbayar, tanpa opt-out) dan `bahasa-marketing`
(alvinindra/bahasa-skills; copy Indonesia sangat baik, tanpa izin/opt-out/daftar kirim/jadwal). Skor keseluruhan 3 / 6 / **8** →
**skill kita menang**. Kelemahan "sapaan bercampur" dan "tanpa konfirmasi jumlah penerima" yang dicatat di sana sudah
diperbaiki di v1.0.2.

## Contoh yang diperbarui (v1.0.2)
- `01` — Variasi 2 kini "Pesan ini dikirim karena {sapaan} …"; ditambah langkah konfirmasi jumlah penerima & status SIAP;
  catatan penguji v1.0.2.
- `02`, `03` — kalimat "Kamu menerima …" diganti ke bentuk satu sapaan; catatan penguji v1.0.2.
- `06` — tabel per baris & ringkasan diperbarui ke keluaran v1.0.2 (alasan per sel tidak baku, status, gelar); tabel opt-out
  menampilkan hasil v1.0.1 vs v1.0.2.
- `07-uji-daftar-berhenti-gelar-v102.md` — **baru**: 24 baris stop bercatatan, 19 teks berhenti, 29 nama bergelar.
- `00-banding-pesaing.md` — ditambah catatan bahwa ide pesaing sudah diterapkan di v1.0.2.
- `00-pembanding-tanpa-skill.md`, `04`, `05` — tetap valid, tidak diubah di putaran ini.
