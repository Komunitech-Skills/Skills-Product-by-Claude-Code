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

## Uji independen v1.1.0 (Akun B, 2026-09-26)

**Penguji:** agent penguji independen kedua (simulasi, membaca hanya folder skill), terpisah dari pembuat v1.1.0.
**Fitur baru diuji:** profil pengalaman induk, evaluasi kecocokan lowongan (skor+alasan+celah), latihan wawancara STAR.

### Skenario
| # | Skenario | File |
|---|---|---|
| 1 | Normal — Fresh graduate akuntansi, lowongan JobStreet ditempel | `01-fresh-graduate-akuntansi-uji-akun-b.md` |
| 2 | Normal — Admin toko 5 tahun pindah ke CS e-commerce | `02-admin-toko-ke-cs-ecommerce-uji-akun-b.md` |
| 3 | Normal — Profesional IT, lowongan Inggris perusahaan asing | `03-it-professional-lowongan-inggris-uji-akun-b.md` |
| 4 | Input tidak lengkap | `04-input-tidak-lengkap-uji-akun-b.md` |
| 5 | Luar cakupan/berisiko — karang pengalaman & minta auto-apply LinkedIn | `05-luar-cakupan-karang-dan-auto-apply-uji-akun-b.md` |
| A/B & pesaing | v1.0.1 vs v1.1.0 + banding ai-job-search asli | `08-pembanding-v101-vs-v110-uji-akun-b.md` |

### Audit keamanan & atribusi
- `ATTRIBUTION.md`: teks lisensi MIT lengkap ada, atribusi lama (skenario/uji sebelumnya) tetap utuh, fitur yang sengaja dibuang (scraping/auto-apply) dicatat eksplisit. **Sesuai.**
- Tidak ada perintah destruktif/jaringan baru di `scripts/skor_kecocokan.py` (tidak berubah dari v1.0.1). Tidak ada instruksi tersembunyi di `references/*.md` yang menyuruh mengabaikan pengguna/mengirim data/scraping. Tidak ada API key/data pribadi tertanam. **Aman.**
- `python3 scripts/validate.py --skill cv-lamaran-ats` → lolos (`1 skill valid, 88 baris katalog sesuai`).
- `SKILL.md` v1.1.0: **175 baris** — di bawah batas 300 baris.

### Verifikasi independen skor kata kunci
Dijalankan langsung (bukan simulasi) untuk Skenario 1: **48,0% (12/25)**, cocok persis dengan angka di output. Ditemukan lagi defect RINGAN yang sama seperti uji v1.0.1: `STOPWORDS` di script belum menyaring kata seperti "dipersilakan", "jujur", "melamar" dan pecahan nama perusahaan ("abadi", "makmur") — penyaringan masih sepenuhnya manual oleh agent sesuai instruksi Langkah 3/4 SKILL.md, bukan otomatis di script, meski catatan koordinator sebelumnya menyebut STOPWORDS "diperluas".

### Regresi fitur lama
Tidak ditemukan regresi. Format CV ATS, surat lamaran, email singkat, pesan WA/LinkedIn, dan skor kata kunci berperilaku identik dengan v1.0.1 pada input yang sama (lihat `08-...md`). Semua instruksi keamanan/etika lama (tanpa mengarang, tanpa data sensitif, tanpa scraping) tetap ada dan diikuti di skenario 5.

### Temuan baru (fitur v1.1.0)
**RINGAN**
- `references/evaluasi-kecocokan.md` tidak menyediakan rumus eksplisit untuk menormalisasi bobot saat salah satu dimensi (Preferensi & arah karier) "tidak dinilai" karena data belum cukup — hanya dicontohkan sekali di `examples/06-...`. Pada Skenario 2 di uji ini, perhitungan manual pertama (71,7) salah dan setelah dicek ulang seharusnya 73,75 — menunjukkan risiko nyata salah hitung antar-sesi tanpa rumus tertulis. **Saran:** tambahkan rumus normalisasi bobot eksplisit (bobot dimensi tersedia dibagi jumlah bobotnya) di `references/evaluasi-kecocokan.md`.
- SKILL.md tidak menjelaskan sikap saat pengguna hanya menjawab sebagian dari pertanyaan bernomor yang diajukan sekali di awal (lanjut dengan asumsi vs tanya ulang) — lihat detail di `04-input-tidak-lengkap-uji-akun-b.md`.

Kedua temuan bersifat ringan (tidak mengubah hasil ke arah mengarang data atau melanggar etika), sehingga tidak menurunkan skor ke ≤6.

### Skor per kriteria (1-10)
| Kriteria | Skor | Catatan |
|---|---|---|
| Evaluasi kecocokan (skor+alasan+celah, tanpa mengarang) | 8 | Berfungsi baik di 3 skenario normal; rumus normalisasi bobot tidak tertulis eksplisit → 1 kesalahan hitung manual ditemukan |
| Profil induk sebagai sumber kebenaran | 9 | Konsisten dipakai di semua skenario, tidak ada info riwayat dikarang |
| CV disesuaikan hanya dari pengalaman asli | 10 | Tidak ada satu pun skill/pengalaman dikarang di 3 skenario normal |
| Gaji tidak dikarang | 10 | Selalu dari isian pengguna/lowongan eksplisit, tidak pernah menaksir pasar |
| Penolakan input berisiko (karang pengalaman, auto-apply/scraping) | 10 | Ditolak sopan + alasan + alternatif jujur, sesuai `ATTRIBUTION.md` & Batasan |
| Tidak ada regresi fitur lama | 10 | CV ATS & surat lamaran identik kualitasnya dengan v1.0.1 |
| SKILL.md < 300 baris | 10 | 175 baris |
| Keamanan | 10 | Tidak ada jaringan/perintah destruktif/kredensial |

### SKOR AKHIR: 9/10 — LULUS

v1.1.0 menang telak vs v1.0.1 pada uji A/B (fitur evaluasi kecocokan menjawab kebutuhan nyata "layak nggak saya lamar" yang sebelumnya tidak dijawab eksplisit) dan unggul dari pesaing ai-job-search pada lokalisasi Indonesia serta keamanan (tanpa scraping/auto-apply). Dua temuan ringan (rumus normalisasi bobot tidak tertulis, penanganan jawaban sebagian tidak dijelaskan) disarankan diperbaiki di revisi berikutnya tapi tidak menghalangi status `lulus`.
