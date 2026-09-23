# Hasil Uji — broadcast-wa v1.0.1 (uji ulang)

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** v1.0.1 (commit `431955c`) — SKILL.md, README.md, ATTRIBUTION.md, `references/aturan-pdp-wa.md`,
  `scripts/siapkan_broadcast.py`, `scripts/uji_regresi.py`. Uji sebelumnya (v1.0.0) skor 6 karena cacat berat B1 & B2.
- **Metode:** skenario 01–05 diperiksa ulang terhadap SKILL.md v1.0.1 (S1 dijalankan ulang dengan script), uji A/B (00),
  **uji banding pesaing (00-banding-pesaing, baru)**, dan **uji data tepi baru (06)**: file kontak "nakal" 55 baris rancangan
  penguji, dilabeli harapan per baris *sebelum* script dijalankan, lalu dicocokkan dengan python terpisah. Semua kerja di
  `/tmp/uji-broadcast-wa-v101/`, data fiktif (0812-0000-xxxx).

## Audit keamanan
- `siapkan_broadcast.py` hanya mengimpor `argparse, csv, json, re, sys, datetime, urllib.parse.quote`. Tidak ada socket/HTTP,
  subprocess, `eval/exec`, penghapusan file, atau pembacaan kredensial. `quote` hanya menyusun teks link wa.me. **Tidak ada
  pengiriman pesan dan tidak ada akses jaringan.** Satu-satunya tulisan file adalah `--output`.
- `uji_regresi.py` hanya menjalankan script lokal lewat `subprocess` di folder sementara — wajar untuk uji.
- SKILL.md/README/references: tidak ada prompt injection; penolakan database beli, WA mod, dan penghapusan opt-out tetap ada;
  larangan memakai `--saya-pastikan-semua-setuju` untuk nomor tanpa izin sudah ditambahkan (langkah 4).

## Status cacat v1.0.0
| Cacat lama | Status v1.0.1 | Bukti |
|---|---|---|
| B1 — Berhenti "STOP"/"x"/tanggal lolos | **Beres** | 06: STOP, stop, x, 2026-09-01, ya, Unsub, Berhenti, ✓ → semua dilewati |
| B2 — baris dobel menimpa berhenti/tolak | **Beres** | 06: dobel sesudah (baris 16) **dan sebelum** baris berhenti (baris 17), dobel dari baris "tidak setuju" (20), beda format +62/812/0062 → semua dilewati |
| S1 — jadwal tidak menghindari salat Jumat | **Beres** | 6 kasus jadwal, 120 kontak: 0 pesan di Jumat 11.30–13.00; `--kirim-saat-jumatan` mematikan sesuai opsi |
| R1 — "promo non-stop" lolos cek opt-out | **Beres** (lihat cacat baru S-1) | "promo non-stop", "STOP! Jangan lewatkan" → ditolak |
| R2 — kontradiksi placeholder vs daftar siaran | **Beres** | SKILL.md langkah 2 |
| R3 — flag persetujuan tanpa pagar | **Beres** | SKILL.md langkah 4 |
| R4 — awalan 0062 ditolak | **Beres** | `0062812-0000-0103`, `0062 812 0000 0136` → 62812… |
| R5 — nama hanya sapaan → "Kak Bu" | **Beres** | "Bu" → "Halo Bu,", "Mas." → "Mas,", nama kosong → "Halo Kak," |
| R6 — CARA-INSTAL.md / LISENSI.txt | Bukan cacat skill | Dibuat oleh `scripts/build.py` saat pengemasan |

`python3 scripts/uji_regresi.py` → **6/6 OK**.

## Verifikasi angka & data (independen)
- **File nakal 55 baris** (06): label penguji KIRIM = 26 nomor; script 26 nomor unik, **identik**. Salah kirim = **0**,
  terlewat = **0**; 3 baris ambigu ("ya (lisan)", Berhenti "masih aktif", "N/A") dibuang (arah aman). Rincian dilewati
  10 + 3 + 6 + 2 + 1 + 5 + 2 = 29 = 55 − 26 ✔. Link wa.me terdekode = kolom pesan; tidak ada placeholder tersisa.
- **Data S1 lama 40 baris** dijalankan ulang: 25 siap kirim, rincian & jadwal sama dengan v1.0.0 (contoh 01 tetap valid).
- Normalisasi: 08…, +62 spasi/strip, 0062, 62 rapat, 8xx (nol hilang), `+62 (0)812`, `+62 0812`, apostrof Excel → benar;
  telepon rumah, `8.12E+11`, nomor pendek, kosong, dua nomor dalam satu sel → dilewati sebagai tidak valid ✔.
- File rusak (kosong, hanya judul, bukan UTF-8, pemisah `;`, judul kolom tak dikenal) → pesan `ERROR:` jelas ✔.

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 9 | Kata kunci Indonesia & Inggris lengkap, batas dengan balas-chat-cs/tagih-piutang jelas. |
| Kemudahan awam | 8 | Satu kalimat cukup; ringkasan jelas. Format stop.txt tidak dijelaskan ke pengguna (lihat B3). |
| Kualitas output | 8 | Variasi natural & personal; minus: sapaan bercampur ("Bu …" + "Kamu menerima …"), nama bergelar jadi "Bu HJ." / "Kak Dr.". |
| Akurasi (angka/fakta) | 8 | Filter kolom persetujuan/berhenti kini tepat 26/26 pada data nakal; tetapi daftar berhenti bercatatan dibaca salah tanpa peringatan. |
| Penanganan input kurang | 9 | Tanya sekali, 5 poin, ada jalan cepat (04); langsung kerja bila info wajib lengkap (03). |
| Penanganan di luar cakupan | 9 | Menolak database beli, WA mod, hapus opt-out dengan sopan + alternatif sah (05); flag kini berpagar. |
| Keamanan | 7 | Tanpa jaringan/pengiriman. Sisa risiko PDP: kontak di stop.txt bisa tetap dikirimi (B3); cek opt-out bisa salah lolos (S-1). |

## SKOR AKHIR: 6 / 10 → **REVISI** (hampir lulus)

Perbaikan v1.0.1 berhasil dan terbukti pada data rancangan penguji: B1, B2, jadwal Jumat, 0062, dan nama-hanya-sapaan
semuanya benar; daftar kirim akhir identik dengan hitungan independen. Namun ditemukan **satu jalur baru dengan akibat yang
sama seperti B2**: `--daftar-berhenti` membuang diam-diam baris yang berisi catatan, sehingga pelanggan yang sudah minta
berhenti tetap masuk daftar kirim — dan ringkasan tidak memberi tanda apa pun. Karena "yang minta berhenti tidak dikirimi lagi"
adalah janji inti produk, cacat ini tetap berat dan skor dibatasi ≤ 6. Perbaikannya kecil (±15 baris); setelah B3 dan S-1
diperbaiki, skill ini layak ≥ 8. Uji A/B dan uji banding pesaing: skill **jelas lebih baik** / **menang keseluruhan**.

## Daftar cacat & saran perbaikan

### Berat
- **B3 — Baris daftar berhenti yang berisi catatan diabaikan diam-diam** (`siapkan_broadcast.py` baris 215–219: seluruh
  potongan baris dilempar ke `rapikan_nomor`, yang menggabungkan *semua* digit). Terbukti: `0812-0000-0120 tgl 12/09` dan
  `Galih 0812 0000 0139 (minta stop 2026-09-01)` → digit tanggal ikut tergabung → dianggap tidak valid → Putri & Galih
  **tetap dikirimi**. Dua nomor dalam satu baris dipisah spasi juga hilang. Tidak ada peringatan, dan ringkasan tidak menyebut
  berapa nomor terbaca dari daftar berhenti.
  *Saran:* (1) cari kandidat nomor per baris dengan regex, mis. `re.findall(r"(?:\+?62|0062|0)?\s*\(?0?\)?\s*8[\d\s\-.()]{7,16}\d", baris)`,
  normalisasi masing-masing; (2) catat baris yang tidak menghasilkan nomor valid dan masukkan ke `peringatan`
  ("2 baris di stop.txt tidak terbaca: baris 1, 2 — periksa manual"); (3) tambahkan `"daftar_berhenti_terbaca": n` ke
  `ringkasan` (baris 353); (4) SKILL.md langkah 4: jelaskan format stop.txt (satu nomor per baris, boleh ada nama/tanggal)
  dan minta agent melaporkan jumlah nomor berhenti yang terbaca; (5) tambah kasus ini ke `uji_regresi.py`.

### Sedang
- **S-1 — Cek teks berhenti bisa salah lolos oleh frasa promosi umum** (baris 43–45, cabang
  `tidak\s+(?:ingin|mau)\s+(?:menerima|dapat)` dan `\buntuk\s+berhenti\b`). Terbukti LOLOS tanpa cara berhenti:
  "Siapa yang tidak mau dapat diskon 50%?", "Kalau tidak ingin menerima kabar diskon, sayang banget lho", "untuk berhenti
  pusing mikir lauk". *Saran:* wajibkan instruksi tindakan: `(balas|ketik|kirim|reply)\s+["'“‘]?(stop|berhenti|unreg)`;
  cabang "tidak ingin menerima" hanya sah bila dalam kalimat yang sama ada `balas|ketik|kirim` + kata kunci. Tambah 3 kasus
  di atas ke `uji_regresi.py`.
- **S-2 — Gelar dianggap nama** (`pecah_nama`, baris 111–121). "IBU HJ. AMINAH" → "Bu HJ.", "dr. Andi" → "Kak Dr.",
  "H. Rahmat" → "Kak H.", "Pak H. Ahmad" → "Pak H.", "Ir./Drs./Prof./Sdr." sama. Gelar H./Hj. sangat umum di data pelanggan
  Indonesia; pesan "Selamat gajian, Bu HJ.!" terkirim ke pelanggan nyata. *Saran:* setelah sapaan, lewati token gelar
  `{h, hj, haji, hajjah, dr, drs, dra, ir, prof, sdr, sdri, st, se}` (tanpa titik, huruf kecil) selama masih ada kata
  berikutnya; bila sapaan belum ada dan gelar "hj"/"hajjah" → sapaan "Bu", "h"/"haji" → "Pak". Aturan kapital ≤ 3 huruf
  (baris 119) sebaiknya hanya untuk token tanpa huruf vokal/singkatan dikenal ("NUR" kini jadi "Kak NUR").

### Ringan
- **R-1 — Sapaan bercampur** di contoh SKILL.md baris 118 dan `references/aturan-pdp-wa.md` baris 58: "Kamu menerima pesan
  ini …" setelah menyapa "Bu/Pak {nama}". *Saran:* "Pesan ini dikirim karena {sapaan} bersedia menerima info dari <toko>.
  Balas STOP untuk berhenti."
- **R-2 — Nilai tidak baku dilaporkan dengan alasan umum.** "ya (lisan)" masuk "belum/tidak setuju"; Berhenti "masih aktif"
  dan "N/A" masuk "minta berhenti". Arahnya aman, tetapi pengguna tidak tahu harus merapikan sel mana. *Saran:* pisahkan alasan
  "nilai persetujuan/berhenti tidak dikenal: '<nilai>'" di `dilewati`, dan tambahkan "aktif"-varian ("masih aktif", "n/a",
  "na") ke `BUKAN_BERHENTI` (baris 47) hanya bila pembuat yakin — atau cukup laporkan.
- **R-3 — Belum ada konfirmasi jumlah penerima** sebelum pengguna mulai mengirim (ide dari pesaing ChatDaddy). *Saran:*
  SKILL.md langkah 4: "sebutkan jumlah siap kirim & baris yang perlu dicek, minta pengguna mengonfirmasi sebelum mulai".

## Uji A/B
`00-pembanding-tanpa-skill.md` (diperbarui): tanpa skill → 1 pesan generik tanpa opt-out, klaim karangan, saran impor semua
nomor. Dengan skill → 3 variasi personal + opt-out + filter persetujuan (25/40, dijalankan ulang di v1.0.1) + jadwal + wa.me.
**Skill jelas memberi nilai tambah.**

## Uji banding pesaing
`00-banding-pesaing.md` (baru): dibandingkan dengan ChatDaddy `send-broadcast` (alat operasional, tanpa opt-out, butuh akun)
dan `bahasa-marketing` dari alvinindra/bahasa-skills (copy Indonesia sangat baik, tetapi tanpa izin/opt-out/daftar kirim/jadwal).
Skor keseluruhan 3 / 6 / **8** → **skill kita menang**. Tidak ditemukan skill publik lain yang khusus broadcast WA berbahasa
Indonesia. Ide yang layak diadopsi: satu sapaan per pesan, hook baris pertama, konfirmasi jumlah penerima, segmentasi kolom.

## Contoh yang diperbarui
- `01` — catatan penguji: hasil uji ulang v1.0.1 (sama 25/40), Jumat otomatis, catatan sapaan bercampur & B3.
- `02`, `05` — catatan penguji: kekurangan lama sudah diperbaiki di v1.0.1. Output tetap valid.
- `00-pembanding-tanpa-skill.md` — baris jadwal & kesimpulan disesuaikan v1.0.1.
- `00-banding-pesaing.md`, `06-uji-kontak-nakal-v101.md` — baru. `03`, `04` tidak terdampak.
