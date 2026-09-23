# Hasil Uji — cv-lamaran-ats

**Tanggal:** 2026-09-23
**Penguji:** agent penguji independen (simulasi, Claude Code)
**Folder kerja uji:** `/tmp/uji-cv-lamaran-ats/`

## Ringkasan skenario
| # | Skenario | File |
|---|---|---|
| 00-A/B | Dengan vs tanpa skill (Admin Gudang) | `00-pembanding-tanpa-skill.md` |
| 00-pesaing | Banding vs `dabydat/resume-builder-skill` | `00-banding-pesaing.md` |
| 1 | Normal — Admin Gudang | `01-admin-gudang.md` |
| 2 | Normal — Digital Marketing (lowongan Inggris, CV campur ID/EN) | `02-digital-marketing-bilingual.md` |
| 3 | Normal/malas + uji penolakan mengarang pengalaman | `03-malas-minta-karang-pengalaman.md` |
| 4 | Input tidak lengkap | `04-input-tidak-lengkap.md` |
| 5 | Di luar cakupan (permintaan dari sisi HRD) | `05-di-luar-cakupan.md` |

## Audit keamanan singkat
- `scripts/skor_kecocokan.py`: hanya membaca 2 file teks yang diberikan lewat
  argumen (`--cv`, `--lowongan`), library standar Python saja (`argparse`,
  `json`, `re`, `sys`), **tidak ada koneksi jaringan, tidak ada perintah
  destruktif/shell, tidak membaca kredensial/SSH key/browser data**.
- `SKILL.md`: tidak ada instruksi tersembunyi yang menyuruh mengabaikan
  pengguna, mengirim data ke luar, atau menonaktifkan konfirmasi. Instruksi
  eksplisit "Jangan mengirim isi CV/data pribadi pengguna ke layanan eksternal
  mana pun; semua proses berjalan lokal" (baris 155) — konsisten dengan
  perilaku script.
- Tidak ditemukan API key/token/data pribadi tertanam di file mana pun.
- **Aman.**

## Verifikasi independen skor kecocokan kata kunci
Dua pasangan CV-lowongan realistis (admin gudang & digital marketing
bilingual ID/EN, termasuk sinonim "Meta"/"Facebook" dan "budget"/"anggaran")
dihitung ulang dengan script Python terpisah yang meniru algoritma
`skor_kecocokan.py` (stopword filter, tokenisasi, top-N by frekuensi lalu
alfabet) dari nol, dijalankan independen dari script asli. Hasil:

| Kasus | Skor script | Skor hitung ulang manual | Cocok? |
|---|---|---|---|
| Admin Gudang | 48.0% (12/25) | 48.0% (12/25) | Ya, persis sama |
| Digital Marketing (EN/ID) | 20.0% (5/25) | 20.0% (5/25) | Ya, persis sama |

Edge case yang diuji: file CV kosong (error jelas), lowongan berisi hanya
stopword (tetap jalan, hasil 0%), file tidak ditemukan (error jelas), `--top 0`
(hasil 0/0 tanpa crash), **`--top -5` (defect, lihat di bawah)**.

## Skor per kriteria (1–10)
| Kriteria | Skor | Catatan |
|---|---|---|
| Pemicu (description tepat) | 9 | Jelas, spesifik, ada kata kunci ID & EN, membedakan dari `lowongan-kerja` |
| Kemudahan awam | 9 | Bisa dipicu satu kalimat; pertanyaan dibatasi & bernomor saat kurang info; nada santai untuk permintaan "malas" |
| Kualitas output | 8 | CV/surat/email/pesan WA lengkap, siap tempel; ringkasan profil & poin pengalaman relevan |
| Akurasi (angka/fakta) | 7 | Skor kata kunci akurat & terverifikasi, tapi daftar "kata kunci hilang" mentah dari script mengandung banyak kata non-keyword (noise) — lihat cacat sedang |
| Penanganan input kurang | 9 | Bertanya sekali, bernomor, maksimal 5 pertanyaan, sesuai SKILL.md |
| Penanganan di luar cakupan | 9 | Menolak & mengarahkan ke `lowongan-kerja` dengan tepat |
| Keamanan | 10 | Tidak ada panggilan jaringan/perintah destruktif/pembacaan kredensial |

## SKOR AKHIR: 8/10 — LULUS

Pertimbangan menyeluruh: fungsi inti (tailoring CV tanpa mengarang, format ATS
satu kolom, etika data sensitif, skor kata kunci) berjalan benar dan teruji di
semua skenario, termasuk uji khusus penolakan permintaan "tambahin aja
pengalaman 3 tahun biar lolos" (skenario 3) yang lulus dengan baik. Cacat yang
ditemukan bersifat sedang/ringan (kualitas daftar kata kunci mentah dari
script, bukan kesalahan angka), sehingga tidak menurunkan skor ke ≤6.

## Daftar cacat

**SEDANG**
- Stopword list `scripts/skor_kecocokan.py` (baris 25–42) belum menyaring kata
  umum Indonesia seperti "mampu", "bawah", "bekerja", "berkala", "menjadi",
  "nilai", "mengoperasikan", "menguasai", "memahami", "melakukan", "menjaga",
  "sederajat" — kata-kata ini muncul di daftar mentah "kata kunci hilang" dan
  bisa membuat agent yang kurang berhati-hati menyuruh pengguna menambahkan
  kata seperti "mampu"/"bawah" ke CV, yang terlihat aneh. Contoh nyata di
  Skenario 1: dari 13 kata "hilang", 5 di antaranya adalah noise ("mampu",
  "bawah", "bekerja", "berkala", "makmur" — bagian nama perusahaan).
  **Saran perbaikan:** perluas `STOPWORDS` dengan kata kerja bantu/umum di
  atas; pertimbangkan menambah filter kata yang hanya muncul sebagai bagian
  nama perusahaan (heuristik: token yang muncul persis di baris pertama/nama
  perusahaan lowongan bisa dikecualikan). Juga tambahkan satu kalimat di
  Langkah 3 SKILL.md yang secara eksplisit menyuruh agent menyaring kata tidak
  relevan sebelum menampilkan daftar ke pengguna (sekarang implisit, tergantung
  kehati-hatian agent).

**RINGAN**
- SKILL.md Langkah 4 belum mencontohkan penanganan sinonim ID/EN atau sinonim
  istilah (mis. "anggaran"=budget, "Meta"=Facebook, "Google Ads"≈"iklan
  Google") — penanganan yang baik pada Skenario 2 adalah inisiatif agent,
  bukan instruksi tertulis, sehingga konsistensinya antar sesi tidak terjamin.
  **Saran:** tambahkan satu kalimat contoh di Langkah 4, mis. "termasuk
  menyamakan istilah sinonim ID/EN (Meta=Facebook, anggaran=budget) untuk
  pengalaman yang sama, tanpa menganggapnya pengalaman baru."
- Bagian "Menjalankan skor kecocokan" tidak menjelaskan langkah kalau CV lama
  pengguna berbentuk file PDF/Word (bukan teks) — SKILL.md hanya bilang
  "simpan isi CV ke file teks" tanpa arahan cara mengekstrak teks dari
  PDF/Word untuk pengguna awam yang cuma punya file tersebut.
  **Saran:** tambahkan catatan di baris ~66-69 SKILL.md: "Kalau CV lama
  pengguna berupa file PDF/Word, minta pengguna salin-tempel isinya sebagai
  teks biasa — skill ini tidak mengonversi file."
- `scripts/skor_kecocokan.py` argumen `--top` tidak divalidasi harus positif:
  `--top -5` diterima tanpa error dan diam-diam mengubah makna slicing Python
  (`[:-5]` = "kecualikan 5 kata terakhir" alih-alih error) sehingga hasil
  hitungan total kata kunci berubah drastis (55 vs 25) tanpa peringatan.
  Risiko rendah karena SKILL.md hanya mencontohkan nilai positif, tapi kalau
  pengguna/agent salah ketik minus, hasil salah tanpa pesan error.
  **Saran:** di `main()` (baris ~104), tambahkan validasi `if a.top < 1:
  keluar_error("--top harus bilangan positif")`.

## Verifikasi independen script: **YA** (dua pasangan CV-lowongan realistis,
kedua kasus verified manual matching persis; ditambah 5 edge case: file
kosong, file tidak ada, lowongan hanya stopword, `--top 0`, `--top -5`).

## Catatan koordinator — v1.0.1 (setelah uji, skor 8 LULUS)
Cacat sedang/ringan dari penguji diperbaiki langsung dan dicek ulang dengan script:
- cv-lamaran-ats: STOPWORDS diperluas (kata umum ID + "pt/cv/tbk"), SKILL.md langkah 3 wajib menyaring kata non-keahlian sebelum ditampilkan, langkah 4 menangani sinonim ID/EN, langkah 1 menangani CV PDF/Word; `--top` ≤ 0 kini ditolak dengan pesan jelas.
- riset-calon-pelanggan: `--bobot` negatif kini ditolak (exit 1, pesan jelas); bobot default tetap sama (skor contoh tidak berubah).
