# HASIL UJI INDEPENDEN — kontrak-kerja-pkwt

- **Penguji:** agent terpisah (bukan pembuat), hanya membaca folder skill. Tanggal: **25 September 2026**.
- **Lingkungan:** salinan skill di scratchpad (`uji-pkwt/`), Python 3 standar. Uji simulasi agent → `platform_teruji`: `claude-code (simulasi agent)`.
- **Tes bawaan:** `python3 tests/uji_regresi.py` → **LULUS semua 98 cek** (exit 0).

## 1. Ringkasan skenario
| # | File | Mode | Hasil | Catatan utama |
|---|---|---|---|---|
| 01 | `01-susun-toko-roti-bandung.md` | Susun + Hitung | ✅ Lulus | Kompensasi Rp4.150.000/orang cocok; UMK tidak dikarang; alasan "produk baru" ditulis; 42 jam/minggu dikoreksi |
| 02 | `02-periksa-draf-kafe.md` | Periksa | ✅ Lulus | Masa percobaan, denda Rp10 jt, tanpa BPJS, total 6 tahun (MELEBIHI, batas 31 Okt 2031) semua 🔴 + kalimat pengganti |
| 03 | `03-hitung-kontraktor-putus-dini.md` | Hitung | ✅ Lulus | Rp5.000.000 + Rp1.250.000 + ganti rugi Rp15.000.000 cocok; uang makan dikecualikan; varian tengah bulan menunjukkan temuan S1 |
| 04 | `04-input-tidak-lengkap.md` | Tanya sekali | ✅ Lulus | 8 butir bernomor, jalur cepat, tidak mengarang |
| 05 | `05-diluar-cakupan-berisiko.md` | Tolak + alternatif | ✅ Lulus | Menolak PKWT untuk pekerjaan tetap, di bawah UMK, percobaan, tahan ijazah; pesangon PKWTT ditolak |
| A/B | `00-pembanding-tanpa-skill.md` | — | ✅ Skill jelas lebih baik | 19 vs 5 (dari 20) |
| Pesaing | `00-banding-pesaing.md` | — | ✅ Menang telak | Skill kita 20 · template HR ID (cuplikan) 7 · wshobson `employment-contract-templates` 2 |

## 2. Verifikasi angka independen
Implementasi ulang penguji (Fraction, pencarian bulan penuh linear, kode ditulis sendiri) dibandingkan dengan `hitung_pkwt.py`:
- **20.000 pasangan tanggal acak** (2024–2030, 5 besaran upah termasuk Rp1.000.001 & Rp7.777.777): **0 selisih**.
- **Monotonik** (20.000 kasus): menambah 1 hari di akhir tidak pernah menurunkan masa kerja; memundurkan mulai tidak pernah menaikkan → **0 pelanggaran**.

| Kasus tepi | Script | Manual | Status |
|---|---|---|---|
| 1–30 Jan 2026 (< 1 bulan) | 0 bulan 30 hari → Rp0 | tidak berhak | ✅ |
| 1–28 Feb 2026 (tepat 1 bulan, 28 hari) | 1 bulan → Rp416.667 (upah 5 jt) | 5.000.000/12 = 416.666,67 → 416.667 | ✅ |
| 1 Jan–31 Des 2026 (tepat 12 bulan) | 1 × upah = Rp5.000.000 | ✅ | ✅ |
| 1 Jan 2026–1 Jan 2027 (12 bulan + 1 hari) | 12 + 1/31 → Rp5.013.441 | 12,032258 × 5 jt / 12 = 5.013.440,86 | ✅ |
| 31 Jan–27 Feb 2026 | 1 bulan (tanggal ulang dijepit ke 28 Feb) | ✅ konsisten dengan asumsi | ✅ |
| 31 Jan–28 Feb 2026 | 1 bulan 1 hari → 1,0323 | ✅ | ✅ |
| 31 Jan–29 Feb 2028 (kabisat) | 1 bulan 1 hari → Rp430.108 | ✅ | ✅ |
| 1–28 Feb 2028 (kabisat, 28 dari 29 hari) | 0 bulan 28 hari → Rp0 | ✅ sesuai asumsi | ✅ |
| 29 Feb 2028–28 Feb 2029 | 12 bulan 1 hari → Rp5.014.368 | 12 + 1/29 | ✅ |
| Batas 5 tahun 1 Jan 2026–31 Des 2030 | OK, Rp25.000.000 | 60/12 × 5 jt | ✅ |
| 1 Jan 2026–1 Jan 2031 | MELEBIHI (60 bulan 1 hari) | ✅ | ✅ |
| Perpanjangan (12 + 6, putus di bulan 15) | kompensasi per periode, periode 1 dicatat "dibayar saat periode sebelum perpanjangan selesai" | PP 35/2021 Pasal 15 ayat (4) | ✅ |
| Putus sebelum perpanjangan dimulai | periode 2 "tidak dijalani", ganti rugi hanya sampai akhir periode berjalan + peringatan | ⚠️ tafsir (sudah ditandai PERLU REVIEW di dasar-hukum §3 no. 4) | ✅ |
| **Dua periode 20 hari berturut-turut tanpa jeda** (40 hari terus-menerus) | Rp0 + Rp0, **tanpa peringatan** | masa kerja terus-menerus ≥ 1 bulan → berpotensi berhak | ⚠️ S3 |
| **Putus 15 Feb, kontrak 1 Jan–31 Mar (pekerja mengakhiri, upah 3 jt)** | dijalani 1,5357 + sisa 1,5161 = **3,0518 bulan** (kontrak 3 bulan); ganti rugi Rp4.548.387 | cara kalender: sisa 13/28 + 1 = 1,4643 → Rp4.392.857 | ⚠️ S1 (pekerja bayar Rp155.530 lebih) |
| **Putus 15 Mar 2027 (skenario 03 varian)** | sisa 3,5 bulan → Rp17.500.000 | kalender 3,5161 → Rp17.580.645 | ⚠️ S1 (pekerja kurang Rp80.645) |
| Aditivitas acak (5.000 kasus) | dijalani + sisa ≠ total pada **2.626 kasus (52%)**, selisih maks. 0,093 bulan (±2,8 hari upah) | — | ⚠️ S1 |

Skenario 01 & 03 (utama) **cocok 100%** dengan hitung manual.

## 3. Data rusak
| Input | Hasil | Status |
|---|---|---|
| Tanggal terbalik | ERROR "tanggal akhir lebih awal... Mungkin tertukar?" (exit 2) | ✅ |
| "31/02/2026" (periode & berhenti) | ERROR "tidak ada di kalender" | ✅ |
| "1 Jan 2026", "2026-01-01", "1-1-2026 - 31-12-2026", "Senin, 5 Oktober 2026" | diterima benar | ✅ |
| "Rp5.000.000", "5jt", "5.5jt", "5,5 juta" | diterima benar | ✅ |
| Negatif ("-5000000", "-5jt"), nol, kosong, periode kosong | ERROR jelas, exit 2, tanpa traceback | ✅ |
| "12/31/2026" (format AS) | ERROR "tidak ada di kalender" | ✅ |
| **"Rp 5.000.000,-"** (penulisan rupiah sangat umum) | ERROR "bukan angka rupiah" | ⚠️ R1 |
| **"4.500" / "5.000"** (maksudnya 4,5 jt / 5 jt?) | diterima sebagai **Rp4.500 / Rp5.000** tanpa peringatan | ⚠️ R2 |
| "1/1/2026-31/12/2026" (tanpa spasi) | ERROR dengan contoh format | ✅ (bisa lebih ramah, R1) |
| "Januari 2026 s.d. Desember 2026", "... selama 12 bulan" | ERROR dengan contoh format | ✅ |
| Gaji pokok 2 jt + tunjangan 3 jt | peringatan upah pokok < 75% | ✅ |

## 4. Kebenaran hukum (web, 25 Sep 2026)
| Poin | Skill | Hasil cek | Sumber |
|---|---|---|---|
| Larangan masa percobaan PKWT (Pasal 58 UU 13/2003 jo. UU 6/2023; PP 35/2021 Pasal 12): batal demi hukum, masa kerja tetap dihitung | ✅ | Benar | https://wageindicator.org/id-id/bekerja-di-indonesia/hukum-tenaga-kerja/kontrak-dan-pemecatan/pkwt/ ; https://dataon.com/id-id/blog/aturan-pkwt-terupdate/ |
| Batas 5 tahun termasuk perpanjangan (PP 35/2021 Pasal 8; MK 168 memaknai Pasal 56 ayat (3)); Pasal 57 ayat (1) bahasa Indonesia & huruf latin | ✅ | Benar | https://www.antaranews.com/berita/4434957/mk-jangka-waktu-pkwt-paling-lama-lima-tahun ; https://news.detik.com/berita/d-7616825/putusan-mk-pkwt-paling-lama-5-tahun-termasuk-jika-ada-perpanjangan ; ikhtisar mkri.id |
| Kompensasi Pasal 15 (≥ 1 bulan terus-menerus; perpanjangan dibayar per periode, ayat (4)), Pasal 16 (12 bln = 1× upah; proporsional), Pasal 17 (putus dini: dari masa yang dijalani) | ✅ | Benar | https://www.hukumonline.com/klinik/a/karyawan-kontrak-iresign-i--berhak-dapat-uang-kompensasi-lt61e4f5b10be77/ ; https://jdih.sukoharjokab.go.id/berita/detail/karyawan-kontrak-resign-berhak-dapat-uang-kompensasi |
| Pasal 62 UU 13/2003: ganti rugi upah sampai akhir jangka waktu, dua arah | ✅ | Benar (cara pro-rata hari tidak diatur → asumsi skill) | idem |
| Putusan MK 168/PUU-XXI/2023 (31 Okt 2024), UU baru ±2 tahun | ✅ | Benar | ikhtisar mkri.id |
| Status UU Ketenagakerjaan baru per 25 Sep 2026 | "belum disahkan, target Oktober 2026" | **Benar** — Wamenaker (23–24 Sep 2026) menargetkan Oktober 2026 | https://www.liputan6.com/bisnis/read/8298473/ruu-pelindungan-ketenagakerjaan-target-teken-oktober-2026 ; https://economy.okezone.com/read/2026/09/24/320/3243879/ruu-pelindungan-ketenagakerjaan-ditargetkan-rampung-oktober-2026 |
| Disclaimer di setiap output | ✅ | Ada teks baku (dasar-hukum §6) + footer script | — |
| Angka UMK | Tidak disimpan, tidak dikarang | ✅ di semua skenario | — |

Catatan: sumber sekunder populer (cuplikan Talenta) masih menulis "PKWT maks. 2 tahun + 1 kali perpanjangan 1 tahun" — aturan usang; skill kita benar.

## 5. Bug / temuan berprioritas
### Tinggi
- *(tidak ada)* — tidak ditemukan angka salah pada rumus utama, klaim hukum salah, atau data dikarang.

### Sedang
- **S1 — Pecahan ganti rugi Pasal 62 tidak konsisten dengan pecahan masa dijalani.** Lokasi: `scripts/hitung_pkwt.py` fungsi `hitung()` bagian "ganti rugi Pasal 62" (`masa(mulai_sisa, periode_jalan[1])` dijangkar dari hari setelah berhenti). Akibat: dijalani + sisa ≠ panjang kontrak pada ±52% kasus (selisih s.d. ±0,09 bulan ≈ 2,8 hari upah), bisa merugikan pekerja atau pengusaha (contoh: Rp155.530 lebih mahal bagi pekerja; Rp80.645 kurang bagi pekerja). **Usulan:** hitung sisa = `bulan_desimal(total periode berjalan) − bulan_desimal(dijalani)` (aditif, konsisten), atau pro-rata kalender (sisa hari bulan berjalan ÷ hari bulan kalender itu + bulan penuh). Tambah tes aditivitas di `tests/uji_regresi.py` dan perbarui Rumus no. 4 di SKILL.md.
- **S2 — Checklist B7 salah hitung jam kerja.** Lokasi: `references/checklist-periksa.md` baris B7: "Sesuaikan 7 jam × 6 hari atau 8 jam × 5 hari". 7 × 6 = **42 jam**, melebihi 40 jam. Aturan: 7 jam/hari **dan** 40 jam/minggu untuk 6 hari kerja (mis. 5 × 7 jam + 1 × 5 jam). **Usulan:** tulis "40 jam/minggu: 6 hari (mis. Senin–Jumat 7 jam, Sabtu 5 jam) atau 5 hari × 8 jam". Tambah juga ke mode Susun langkah cek jam kerja; naikkan risiko ke 🔴 bila jauh di atas 40 jam tanpa lembur (skenario 02: 66 jam).
- **S3 — Periode berturut-turut yang masing-masing < 1 bulan diberi Rp0 tanpa peringatan.** Lokasi: `hitung()` loop kompensasi (`berhak = bp >= 1` per periode). PP 35/2021 Pasal 15 menyebut masa kerja "paling sedikit 1 bulan **secara terus-menerus**"; 20 + 20 hari tanpa jeda = 40 hari terus-menerus. **Usulan:** bila periode < 1 bulan diikuti perpanjangan tanpa jeda, beri peringatan "masa kerja terus-menerus sudah ≥ 1 bulan; kompensasi berpotensi terutang — PERLU REVIEW", atau gabungkan periode tersebut.

### Rendah
- **R1 — Parser rupiah menolak "Rp 5.000.000,-"** (akhiran ",-" sangat umum di Indonesia) dan periode tanpa spasi "1/1/2026-31/12/2026". Lokasi: `parse_rupiah()`, `PEMISAH_PERIODE`. Usulan: buang akhiran `,-`/`.-`; izinkan `-` tanpa spasi di antara dua tanggal berformat angka.
- **R2 — Upah tidak wajar diterima diam-diam** ("4.500" → Rp4.500). Usulan: peringatan bila upah bulanan < Rp500.000 ("mungkin maksudnya 4,5 juta?").
- **R3 — Tidak ada panduan untuk beberapa pekerja sekaligus** (skenario 01: 2 orang). Usulan: satu kalimat di SKILL.md "PKWT dibuat per orang; buat satu draf + daftar identitas per pekerja, total kompensasi = jumlah per orang".
- **R4 — Tanggal mulai tidak diketahui** padahal script mewajibkan `--periode` (skenario 04). Usulan: SKILL.md menyebut "tanpa tanggal: pakai rumus 12 bulan = 1× upah / n bulan ÷ 12, beri label dihitung manual, tanggal tetap `[isi]`".
- **R5 — Mode Periksa, total > 5 tahun:** script tetap menjumlah kompensasi seluruh 72 bulan (Rp18 jt). Wajar tetapi mudah disalahbaca; usulan tambahan kalimat di peringatan "angka periode setelah batas 5 tahun hanya ilustrasi".

## 6. Skor kualitas: **8/10**
Alasan:
- (+) Uji A/B jelas lebih baik (19 vs 5), menang telak atas pesaing (20 vs 7 vs 2) → tidak terkena batas maks. 6.
- (+) Angka skenario 01 & 03 cocok 100%; 20.000 kasus acak cocok dengan implementasi independen; penanganan tanggal/kabisat/akhir bulan konsisten; data rusak ditangani tanpa traceback; 98 tes bawaan lulus.
- (+) Hukum benar per 25 Sep 2026, status MK 168/RUU jujur, UMK tidak dikarang, disclaimer konsisten, penolakan permintaan berisiko sopan dan bermanfaat.
- (−) S1 (inkonsistensi pro-rata ganti rugi, selisih kecil tetapi nyata dalam uang), S2 (checklist jam kerja salah hitung), S3 (kasus periode pendek berturut-turut) → belum 9.
- Rekomendasi: **lulus uji (≥ 7)**; perbaiki S1–S3 sebelum `beta` (perbaikan kecil, tidak perlu uji ulang penuh — cukup tes regresi tambahan + cek ulang skenario 03 varian). Jadwalkan tinjau ulang dasar hukum awal November 2026 (UU Ketenagakerjaan baru ditargetkan Oktober 2026).
