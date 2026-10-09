# HASIL UJI - spesifikasi-produk-usaha v1.0.0

Penguji: agent independen (bukan pembuat), 2026-09-29. Hanya membaca folder skill + CLAUDE.md. Platform: `claude-code (simulasi agent)`. Semua skrip bantu & data uji di scratchpad penguji, bukan di folder skill.

## 1. Audit keamanan & format
| Cek | Hasil |
|---|---|
| Frontmatter hanya `name` + `description`, nama = folder | OK |
| Script hanya pustaka standar (argparse, csv, io, json, re, sys, decimal) | OK |
| Jaringan / subprocess / eval / exec / baca kredensial di `scripts/` | Tidak ada. OK |
| Prompt injection / instruksi tersembunyi di SKILL.md, referensi, templat | Tidak ada. OK |
| API key / data pribadi tertanam | Tidak ada. OK |
| `scripts/__pycache__/` ada di folder kerja | Diabaikan git (.gitignore) dan `build.py` (DIABAIKAN). OK |
| `tests/uji_regresi.py` | 25/25 lulus (dijalankan penguji) |
| `python3 scripts/validate.py --skill spesifikasi-produk-usaha` | "1 skill valid", kode 0 |

### Lisensi & sinyal bukti sumber (menutup PERLU REVIEW pembuat)
Dicek 2026-09-29 lewat GitHub API + raw.githubusercontent.com:
| Sumber | Bintang / fork | Dibuat / push terakhir | Lisensi | NOTICE | Penilaian |
|---|---|---|---|---|---|
| phuryn/pm-skills | 26.657 / 2.839 | 2026-03-01 / 2026-09-14 (~7 bln, aktif) | MIT, "Copyright (c) 2026 Pawel Huryn" | tidak ada (404) | **Kuat** |
| product-on-purpose/pm-skills | 700 / 90 | 2026-01-09 / 2026-09-29 (~8,5 bln, aktif, akun organisasi) | Apache-2.0, "Copyright 2026 Jonathan Prisant" | tidak ada (404) | **Cukup kuat** (>= 500 bintang repo koleksi) |

- `LICENSE-MIT` dan `LICENSE-APACHE` **identik** dengan hulu (diff kosong). Nama pemegang hak cipta di ATTRIBUTION/NOTICE cocok.
- Klaim "repo asal tidak punya NOTICE" **benar** untuk kedua repo.
- Pernyataan perubahan Apache 4(b) ada di ATTRIBUTION.md. Kepatuhan lisensi: **OK**. Label PERLU REVIEW soal bintang/umur **boleh dicabut**.

## 2. Skenario & vonis
| # | Skenario | File | Vonis |
|---|---|---|---|
| 1 | Normal: keripik tempe + 4 ide RICE (format angka Indonesia) | `06-uji-normal-keripik-tempe.md` | LULUS dengan catatan (tenggat halal 17-10-2026 tidak disebut) |
| 2 | Normal: piyama bayi + brief konveksi | `07-uji-normal-piyama-bayi-konveksi.md` | **GAGAL sebagian** (referensi bilang fashion "umumnya tidak perlu izin", padahal pakaian bayi SNI wajib) |
| 3 | Normal: serum maklon + ICE | `08-uji-normal-serum-maklon-ice.md` | LULUS dengan catatan (halal kosmetik wajib 17-10-2026 tidak disebut) |
| 4 | Input tidak lengkap + CSV rusak | `09-uji-input-kurang.md` | LULUS dengan bug (keyakinan 0,9 diterima sebagai 0,9%) |
| 5 | Di luar cakupan (pajak, kontrak, klaim kesehatan, urus izin) | `10-uji-luar-cakupan.md` | LULUS |
| A/B | tanpa vs dengan skill | `00-pembanding-tanpa-skill.md` | Dengan skill **jelas lebih baik** |
| Pesaing | create-prd (phuryn), deliver-prd (PoP) | `00-banding-pesaing.md` | Skill kita **menang** (85 vs 37 vs 33) |

Semua skor RICE/ICE dan HPP di skenario serta contoh 02 pembuat diverifikasi ulang dengan `fractions.Fraction`: **semua cocok** (80; 67,5; 46,67; 12,5; 300; 240; 66,67; 42; 432; 280; 240; 72; HPP 7.500 / 9.000 / 43.450 / 26.700).

## 3. Bug
**B1 - `--kapasitas`: satu ide besar di urutan teratas membuat SEMUA ide jadi "Nanti" (serius).**
CSV `Besar(usaha 15), Sedang(4), Kecil(2)`, `--kapasitas 10` -> ketiganya "Nanti", padahal Sedang+Kecil (6 hari) muat di Sekarang. Penyebab: di `beri_tahap`, begitu satu item tidak muat di Berikutnya, `tahap` dikunci "Nanti" untuk sisa daftar. Roadmap salah tanpa peringatan.

**B2 - Keyakinan pecahan diterima diam-diam (serius).** `keyakinan = 0,9` / `0.8` dibaca 0,9% sehingga skor 100x lebih kecil (Tas kertas: 1,35, seharusnya 135). Pengguna awam sering menulis keyakinan sebagai pecahan.

**B3 - Referensi izin tidak akurat/kurang untuk kategori realistis (serius untuk domain sensitif).**
- Tidak ada **SNI wajib** sama sekali; baris "Fashion & kerajinan: umumnya tidak perlu izin edar khusus" menyesatkan untuk **pakaian bayi** (Permenperin 7/2014) dan **mainan anak** (Permenperin 55/M-IND/PER/11/2013). Sumber: kemenperin.go.id/artikel/22114, bsn.go.id berita 6298.
- Halal: tidak menyebut tenggat **17 Oktober 2026** untuk makanan-minuman UMK dan untuk **kosmetik** (PP 42/2024). Sumber: bpjph.halal.go.id/detail/bpjph-17-oktober-2026-produk-makanan-minuman-umk-harus-sudah-bersertifikat-halal-bagaimana-dengan-produk-luar-negeri/ ; bpjph.halal.go.id/read/bpjph-produk-kosmetik-wajib-bersertifikat-halal-pada-oktober-2026 . Baris halal hanya menyebut "pangan/minuman".
- PIRT: tidak menyebut dasar aturan (**Peraturan BPOM No. 4 Tahun 2024**) dan pengecualian penting: pangan yang butuh **penyimpanan/distribusi dingin atau beku**, kemasan kedap/steril, produk **SNI wajib** (AMDK, garam beryodium), **klaim kesehatan/gizi**, BTP, pangan bayi, alkohol; serta pangan dengan daya simpan < 7 hari tidak wajib SPP-IRT. Sumber: indramayu.pom.go.id/berita/jenis-pangan-yang-wajib-dan-tidak-wajib-mengurus-spp-irt ; pom.go.id penjelasan publik pangan beku.
- Tidak membedakan jamu/herbal (obat tradisional, izin BPOM TR) dari pangan.
- DJKI tanpa tautan: resmi `https://merek.dgip.go.id` / `https://www.dgip.go.id` (tarif UMK Rp500.000/kelas per PP 30/2026, berlaku 1-8-2026 - hanya info, tarif jangan ditulis di skill kecuali diberi tanggal).
- Yang **akurat**: sppirt.pom.go.id, cekbpom.pom.go.id, notifkos.pom.go.id (notifikasi kosmetik, Perban BPOM 21/2022 & 17/2023), bpjph/ptsp.halal.go.id, self declare + pendamping PPH untuk UMK, oss.go.id.

**B4 - Contoh 01 pembuat bertentangan dengan aturan PIRT.** Teh serai jahe botol ditulis "Penyimpanan: dingin" lalu diarahkan ke PIRT. Produk yang butuh rantai dingin tidak dapat SPP-IRT (Perban BPOM 4/2024). Contoh tidak diubah penguji (tugas: jangan memperbaiki skill); lihat permintaan perbaikan F4.

**Minor**
- B5: `10,000` (ribuan gaya Inggris) dibaca 10 tanpa peringatan.
- B6: header kolom salah/berbahasa Inggris hanya memunculkan "kolom 'nama' kosong"; seharusnya "kolom wajib tidak ditemukan: nama, jangkauan, ...".
- B7: `--kapasitas` dengan `--metode ice` diabaikan diam-diam.
- B8: aturan sepertiga: n=4 -> 2/2/0 (tahap Nanti kosong); dua ide skor sama bisa terpisah ke tahap berbeda. Contoh 01 menulis langganan = "Nanti" padahal keluaran default contoh 02 = "Berikutnya" (hanya benar dengan `--kapasitas 10`).
- B9: tidak ada bagian **metrik keberhasilan** (kelebihan pesaing).

## 4. Skor: **6 / 10 - TIDAK LULUS (revisi, lalu uji ulang independen)**
Alasan:
- (+) Struktur 11 bagian sangat pas untuk UMKM, brief tanpa data internal, penolakan klaim kesehatan, alur tanya-sekali, script Decimal dengan 25 uji regresi, format angka Indonesia benar; menang jelas di A/B dan banding pesaing.
- (-) Dua bug script menghasilkan angka/roadmap **salah tanpa peringatan** (B1, B2) - melanggar prinsip "Reliable: angka dihitung".
- (-) Referensi izin, domain sensitif, memberi rasa aman keliru (pakaian bayi/mainan tanpa SNI), melewatkan tenggat halal yang jatuh 18 hari lagi, dan tidak mencantumkan dasar aturan + tanggal berlaku (Tahap 4 butir 5). Contoh 01 sendiri keliru arah izin.
Setelah F1-F5 diperbaiki, perkiraan skor 8.

## 5. Permintaan perbaikan (untuk pembuat)
- **F1 (B1)** `beri_tahap`: item yang tidak muat tidak boleh mengunci tahap; lewati ke item berikutnya yang muat (atau tandai item > kapasitas sebagai "Nanti - lebih besar dari kapasitas" lalu lanjutkan). Tambah uji regresi `Besar(15),Sedang(4),Kecil(2), kapasitas 10 -> Nanti, Sekarang, Sekarang`.
- **F2 (B2)** keyakinan 0 < k <= 1: tolak baris dengan pesan "keyakinan ditulis persen 0-100; 0,8 maksudnya 80?" (jangan dikonversi diam-diam). Tambah uji regresi.
- **F3 (B3)** revisi `references/perizinan-produk.md`: tambah baris SNI wajib (pakaian bayi, mainan anak, AMDK, dll. + tautan BSN/Kemenperin); halal: tenggat 17-10-2026 untuk makanan-minuman UMK dan kosmetik (+ barang gunaan tertentu), dasar UU 33/2014 & PP 42/2024; PIRT: dasar Perban BPOM 4/2024 + daftar pengecualian (dingin/beku, kedap/steril, SNI wajib, klaim, BTP, bayi, alkohol) + daya simpan < 7 hari; baris jamu/herbal -> BPOM TR; tautan DJKI resmi. Setiap baris diberi "dasar aturan + dicek <tanggal>".
- **F4 (B4)** contoh 01: ganti "Penyimpanan: dingin" atau tulis bahwa produk yang butuh rantai dingin kemungkinan harus izin edar BPOM MD, bukan PIRT; samakan roadmap dengan keluaran default contoh 02 atau sebut `--kapasitas 10`.
- **F5 (B9)** tambah butir "Ukuran keberhasilan" (1-3 target terukur) di bagian 1/2 templat - ditulis ulang dengan cara sendiri.
- F6 (minor): pesan kolom hilang (B6), peringatan `10,000` (B5), peringatan `--kapasitas` diabaikan pada ICE (B7), dokumentasikan perilaku seri/sepertiga (B8).
- Katalog: `platform_teruji` cukup `claude-code (simulasi agent)` setelah lulus; status tetap `uji` sampai uji ulang.

---
## Catatan revisi 1.0.1 (oleh pembuat, 2026-09-29) - menunggu uji ulang independen
- **F1:** `beri_tahap` dengan `--kapasitas`: ide yang tidak muat dilewati (tidak mengunci tahap); ide > kapasitas -> Nanti + catatan "pecah jadi langkah kecil". Uji regresi: `Besar(15),Sedang(4),Kecil(2)`, kap 10 -> Nanti, Sekarang, Sekarang; plus kasus lewati-lalu-lanjut.
- **F2:** keyakinan 0 < k <= 1 tanpa `%` ditolak: "keyakinan ditulis persen 0-100; 0,9 maksudnya 90%?"; `0,9%` eksplisit tetap diterima. Uji regresi ditambah.
- **F3:** `references/perizinan-produk.md` ditulis ulang, diverifikasi via situs resmi (dicek 2026-09-29): SNI wajib pakaian bayi (Permenperin 7/2014), mainan (Permenperin 24/2013 jo. 55/2013 jo. 111/2015), AMDK/garam; halal UMK makanan-minuman 17-10-2026 + kosmetik & sandang/aksesori mulai 18-10-2026 (UU 33/2014, PP 42/2024); PIRT = Perban BPOM 4/2024 + pengecualian (dingin/beku, kedap, SNI wajib, klaim, bayi, BTP, alkohol) & daya simpan < 7 hari; jamu -> BPOM TR (Perban BPOM 25/2023); merek.dgip.go.id; NIB PP 28/2025. Tiap baris punya dasar aturan + tanggal cek.
- **F4:** contoh 01: teh disimpan dingin -> BPOM MD, bukan PIRT (dengan pilihan ubah proses), tenggat halal, tabel izin; roadmap = keluaran default contoh 02.
- **F5:** "Ukuran keberhasilan" (1-3 target terukur) di bagian 2 templat, Format Output, cek akhir, dan contoh 01.
- **F6:** `10,000` ditolak sebagai ambigu (`10,000,000` diterima); kolom wajib hilang -> "kolom wajib tidak ditemukan: ..." + judul terbaca, judul Inggris diterima; `--kapasitas` pada ICE -> PERINGATAN (stdout, stderr, JSON); pembagian tanpa kapasitas 4 ide = 2/1/1, skor seri ikut tahap atas (didokumentasikan di `references/prioritas.md`).
- PERLU REVIEW sumber di ATTRIBUTION.md dicabut berdasar verifikasi penguji.
- `tests/uji_regresi.py`: 40/40 lulus. `validate.py --skill spesifikasi-produk-usaha`: valid. Versi 1.0.1, status tetap `uji`.
