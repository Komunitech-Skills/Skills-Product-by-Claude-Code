# Hasil Uji — riset-calon-pelanggan

**Tanggal:** 2026-09-23
**Penguji:** agent penguji independen (simulasi, Claude Code)
**Folder kerja uji:** `/tmp/uji-riset-calon-pelanggan/`

## Ringkasan skenario
| # | Skenario | File |
|---|---|---|
| 00-A/B | Dengan vs tanpa skill (Cleaning Service Surabaya) | `00-pembanding-tanpa-skill.md` |
| 00-pesaing | Banding vs `coreyhaines31/marketingskills` (prospecting) | `00-banding-pesaing.md` |
| 1 | Normal — Cleaning Service Surabaya | `01-cleaning-service-surabaya.md` |
| 2 | Normal — Software Kasir Resto + skor dari CSV | `02-software-kasir-resto-skor-csv.md` |
| 3 | Normal/malas — Kemasan Makanan Ramah Lingkungan | `03-malas-kemasan-makanan.md` |
| 4 | Input tidak lengkap | `04-input-tidak-lengkap.md` |
| 5 | Di luar cakupan (minta scraping/beli database/blast) | `05-di-luar-cakupan-scraping.md` |

## Audit keamanan singkat
- `scripts/skor_prospek.py`: hanya membaca 1 file CSV yang diberikan lewat
  argumen, library standar Python saja (`argparse`, `csv`, `json`, `sys`,
  `io`), **tidak ada koneksi jaringan, tidak ada perintah destruktif/shell,
  tidak membaca kredensial/SSH key/browser data**.
- `SKILL.md` & `references/sumber-pencarian.md`: tidak ada instruksi
  tersembunyi yang menyuruh mengabaikan pengguna, mengirim data ke luar, atau
  menonaktifkan konfirmasi. Berulang kali menegaskan "skill ini tidak
  melakukan scraping otomatis... tidak mengakses internet" dan "jangan
  mengirim isi file/daftar prospek pengguna ke layanan eksternal mana pun" —
  konsisten dengan perilaku script.
- Tidak ditemukan API key/token/data pribadi tertanam di file mana pun.
- **Aman.**

## Verifikasi independen skor kualifikasi prospek
Data normal (5 baris) dan data kotor (9 baris, termasuk format "Rp 5", nilai
di luar 0–5, nilai negatif, nama kosong/spasi, kolom kosong, desimal koma
"4,5") dihitung ulang manual dengan rumus
`(cocok_icp×0,3 + kebutuhan×0,3 + bayar×0,2 + akses×0,2) ÷ 5 × 100` dari
SKILL.md (fallback manual) — bukan menjalankan ulang script yang sama, untuk
verifikasi independen. Hasil:

| Kasus | Skor script (contoh) | Hitung ulang manual | Cocok? |
|---|---|---|---|
| Resto Sedap Rasa (5,5,4,4) | 92.0 | 92.0 | Ya |
| Kafe Kopi Senja (4,4,3,5) | 80.0 | 80.0 | Ya |
| Bank Makmur (5,5,5,5) | 100.0 | 100.0 | Ya |
| Toko Kelontong (1,1,1,1) | 20.0 | 20.0 | Ya |
| Bengkel Jaya Motor (4,5,"4,5",3) desimal koma | 84.0 | 84.0 | Ya |

Baris rusak pada data kotor (9 baris): nama kosong, nilai "Rp 5" (bukan
angka), nilai 6 (di luar 0-5), nilai -1 (di luar 0-5), nama hanya spasi,
kolom kebutuhan kosong — **keenamnya dilewati dan dilaporkan jumlahnya**
(`baris_dilewati: 6`) sesuai spesifikasi, tidak ditebak. Delimiter titik koma
(`;`) dan tab terdeteksi otomatis dan diuji berhasil. Kolom hilang, file
kosong, dan total bobot ≠ 1.0 menghasilkan pesan error yang jelas.

## Skor per kriteria (1–10)
| Kriteria | Skor | Catatan |
|---|---|---|
| Pemicu (description tepat) | 9 | Jelas, menyebut ICP/lead generation/qualify leads, membedakan dari `follow-up-prospek` & `proposal-kerjasama` |
| Kemudahan awam | 9 | Satu kalimat cukup memicu; pertanyaan dibatasi & bernomor; nada santai untuk permintaan "malas" |
| Kualitas output | 8 | ICP, sumber pencarian, tabel, skor, pesan pembuka, catatan UU PDP — lengkap dan siap pakai |
| Akurasi (angka/fakta) | 8 | Skor terverifikasi akurat di semua kasus normal & kotor; **defect bobot negatif** (lihat di bawah) menurunkan sedikit |
| Penanganan input kurang | 9 | Bertanya sekali, bernomor, hanya 1 hal wajib (produk/jasa), sisanya opsional |
| Penanganan di luar cakupan | 10 | Menolak scraping/beli database/blast dengan tegas, jelas alasan & risiko, tetap menawarkan alternatif sah |
| Keamanan | 10 | Tidak ada panggilan jaringan/perintah destruktif/pembacaan kredensial |

## SKOR AKHIR: 8/10 — LULUS

Pertimbangan menyeluruh: fungsi inti (ICP, sumber publik & sah, skor
kualifikasi terverifikasi, pesan pembuka patuh UU PDP, penolakan tegas
terhadap scraping/beli database/blast) berjalan benar dan konsisten di semua
skenario. Cacat yang ditemukan bersifat sedang (satu defect validasi input
script) dan ringan, tidak mempengaruhi jalur penggunaan normal, sehingga tidak
menurunkan skor ke ≤6.

## Daftar cacat

**SEDANG**
- `scripts/skor_prospek.py` tidak memvalidasi bahwa tiap bobot individual
  bernilai non-negatif — hanya mengecek total bobot ≈ 1.0 (baris 83–84).
  Diuji: `--bobot=-0.5,0.5,0.5,0.5` (total tetap 1.0) **diterima tanpa
  error** dan menghasilkan skor yang salah arah — prospek dengan "cocok ICP"
  tinggi justru mendapat skor LEBIH RENDAH karena bobotnya negatif (contoh
  nyata: "Klinik Sehat Bersama" dengan cocok_icp=5 turun dari kategori Panas
  ke Hangat, sementara logikanya harusnya makin tinggi cocok_icp makin
  Panas). Risiko rendah untuk pengguna awam yang memakai bobot default, tapi
  bisa terjadi kalau pengguna/agent salah ketik tanda minus saat mengubah
  `--bobot` sesuai prioritas bisnis mereka (SKILL.md baris 70 mengizinkan
  pengubahan ini tanpa menyebut batasan harus positif).
  **Saran perbaikan:** di `main()` sekitar baris 76–84, tambahkan
  `if any(w < 0 for w in bobot_list): keluar_error({"error": "Semua bobot
  harus bernilai 0 atau lebih (tidak boleh negatif)."})` sebelum pengecekan
  total bobot.

**RINGAN**
- SKILL.md tidak menjelaskan cara menangani skor yang sama persis antar
  prospek (tie-breaking) — pada Skenario 2, dua prospek mendapat skor 80.0
  persis sama; agent perlu berimprovisasi menjelaskan perbedaan kualitatif
  (akses PIC vs kemampuan bayar) tanpa instruksi tertulis.
  **Saran:** tambahkan satu baris di bagian "Format output" atau Langkah 5,
  mis. "Jika skor sama persis, urutkan berdasarkan kemudahan akses PIC lebih
  dulu, lalu sebutkan alasan kualitatif pembeda."
- Boundary kategori (Panas ≥75) tidak bisa dicapai persis dengan kombinasi
  nilai bulat 0–5 pada bobot default (hanya bisa dicapai dengan nilai
  desimal seperti 4,5) — bukan bug (desimal memang diizinkan via input
  "0,5"→0.5), tapi SKILL.md tidak menyebutkan ini ke pengguna sehingga tim
  sales yang hanya mengisi angka bulat mungkin heran kenapa skor 74 (bukan
  75) tergolong Hangat padahal terasa "hampir Panas". Dampak sangat kecil,
  hanya observasi UX.

## Verifikasi independen script: **YA** (data normal 5 baris + data kotor 9
baris dengan format Rp, nilai di luar rentang, nilai negatif, nama
kosong/spasi, kolom kosong, desimal koma; ditambah uji delimiter titik koma,
file kosong, kolom hilang, total bobot ≠ 1.0, dan bobot bernilai negatif).

## Catatan koordinator — v1.0.1 (setelah uji, skor 8 LULUS)
Cacat sedang/ringan dari penguji diperbaiki langsung dan dicek ulang dengan script:
- cv-lamaran-ats: STOPWORDS diperluas (kata umum ID + "pt/cv/tbk"), SKILL.md langkah 3 wajib menyaring kata non-keahlian sebelum ditampilkan, langkah 4 menangani sinonim ID/EN, langkah 1 menangani CV PDF/Word; `--top` ≤ 0 kini ditolak dengan pesan jelas.
- riset-calon-pelanggan: `--bobot` negatif kini ditolak (exit 1, pesan jelas); bobot default tetap sama (skor contoh tidak berubah).
