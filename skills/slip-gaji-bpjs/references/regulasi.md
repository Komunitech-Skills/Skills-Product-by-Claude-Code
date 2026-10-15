# Dasar Aturan Slip Gaji, BPJS, Lembur & PPh 21 — berlaku per 23 September 2026 (JKK/JKP dicek ulang 15 Oktober 2026)

> Ringkasan untuk alat bantu hitung, bukan nasihat hukum/pajak. Setiap baris diberi status verifikasi, sumber, dan tanggal cek. Angka yang berubah tiap tahun (batas upah JP, UMK) wajib dicek ulang.

Status: **Terverifikasi resmi** = dibaca dari teks peraturan/surat resmi · **Terverifikasi (situs resmi)** = halaman resmi instansi · **Sekunder** = hanya dari sumber non-resmi; dipakai sebagai peringatan, bukan angka pasti.

## BPJS Kesehatan (pekerja penerima upah)
| Fakta | Status | Sumber (dicek 2026-09-23) |
|---|---|---|
| Iuran 5% dari gaji/upah sebulan: 4% pemberi kerja, 1% peserta | Terverifikasi resmi | Perpres 64/2020 (ubah Perpres 82/2018) Pasal 30 ayat (1) — [1] |
| Batas atas gaji/upah dasar iuran Rp12.000.000 | Terverifikasi resmi | Perpres 64/2020 Pasal 32 ayat (1) — [1] |
| Batas bawah = UMK (bila tidak ada UMK: UMP); tidak berlaku bagi pemberi kerja yang mendapat penangguhan upah minimum | Terverifikasi resmi | Perpres 64/2020 Pasal 32 ayat (2)–(4) — [1] |
| Dasar iuran = gaji/upah pokok + tunjangan tetap | Sekunder (definisi resmi yang terbaca hanya untuk kepala/perangkat desa) — skill menyediakan kolom `dasar_bpjs_kesehatan` untuk menimpa | [1], [9] |
| Iuran tambahan anggota keluarga lain (1%/orang) | Tidak dihitung skill | — |

> **Cek versi berlaku:** Perpres 82/2018 jo. Perpres 64/2020 jo. Perpres 59/2024. Pasal iuran (Pasal 30) dan batas Rp12.000.000 (Pasal 32) di atas dibaca dari Perpres 64/2020; teks Perpres 59/2024 belum dibaca ulang untuk pasal itu — cek pasal iuran & plafon versi yang berlaku saat menghitung (status: PERLU REVIEW, verifikasi C28 2026-10-14).

## BPJS Ketenagakerjaan (penerima upah)
| Fakta | Status | Sumber |
|---|---|---|
| JKK yang dibayar pemberi kerja: 0,24% / 0,54% / 0,89% / 1,27% / 1,74% sesuai tingkat risiko (sangat rendah → sangat tinggi) | Terverifikasi resmi (dicek ulang 2026-10-15) | PP 44/2015 Pasal 16 — [2]; artikel resmi BPJSTK 17 Des 2025 menyebut tarif yang sama "menurut PP 6/2025" — [4] |
| Menurut PP 6/2025 Pasal 11 ayat (5) (berlaku 7 Feb 2025): 0,14% dari iuran JKK **direkomposisi** untuk JKP, sehingga porsi JKK murni 0,10% / 0,40% / 0,75% / 1,13% / 1,60%. Ketentuan rekomposisi JKK 0,14% dengan angka yang sama **sudah ada sejak PP 37/2021** Pasal 11 ayat (5) huruf a; PP 6/2025 mempertahankannya, menghapus rekomposisi JKM 0,10% (PP 37/2021 Pasal 11 ayat (5) huruf b), dan menurunkan iuran JKP dari 0,46% ke 0,36%. Ini pembagian di dalam iuran yang sama (0,10 + 0,14 = 0,24, dst.), **bukan** tarif tagihan; skill tetap memakai 0,24–1,74% dan memberi ⚠️ bila pengguna mengisi angka porsi murni | Terverifikasi resmi (dicek 2026-10-15) | PP 6/2025 Pasal 11 ayat (2)–(5) — [12]; PP 37/2021 Pasal 11 ayat (2)–(5) — [13]; [4] |
| JKM 0,30%, dibayar pemberi kerja | Terverifikasi resmi | PP 44/2015 Pasal 18 — [2] |
| Dasar iuran = upah sebulan = upah pokok + tunjangan tetap; upah harian × 25 | Terverifikasi resmi | PP 44/2015 Pasal 19 — [2] |
| JHT 5,7%: 3,7% pemberi kerja + 2% pekerja (tanpa batas upah) | Terverifikasi (situs resmi) | Artikel BPJSTK "Berapa Besaran Iuran JHT, JKK, JKM, JP dan JKP?" 17 Des 2025 — [4] (PP 46/2015) |
| JP 3%: 2% pemberi kerja + 1% pekerja | Terverifikasi (situs resmi) | [4] (PP 45/2015) |
| Batas upah JP **Rp11.086.300 mulai 1 Maret 2026** (sebelumnya Rp10.547.400 sejak Maret 2025) = 10.547.400 × (1 + 5,11%) dibulatkan | Terverifikasi resmi (surat BPJSTK No. B/1226/022026, 25 Feb 2026; dikonfirmasi akun resmi @BPJSTKinfo) | [5], [6] |
| JKP: iuran 0,36% upah sebulan (sebelumnya 0,46% menurut PP 37/2021 [13]) = 0,22% dibayar Pemerintah Pusat + 0,14% rekomposisi iuran JKK (Pasal 11 versi PP 6/2025 hanya menyebut rekomposisi JKK); tidak ada iuran tambahan dari pemberi kerja atau pekerja | Terverifikasi resmi (dicek ulang 2026-10-15) | PP 6/2025 Pasal 11 ayat (2)–(5) — [12]; [4] |
| Diskon 50% iuran JKK industri padat karya tertentu berlaku Feb 2025–Jan 2026 (PP 7/2025 jo. PP 36/2025); perpanjangan setelah Jan 2026 tidak ditemukan | Sekunder + artikel BPJSTK — skill tidak menerapkan diskon; isi `jkk_persen` sendiri bila berlaku | [4], [10] |

## Lembur (PP 35/2021)
| Fakta | Status | Sumber |
|---|---|---|
| Lembur maks 4 jam/hari & 18 jam/minggu (tidak termasuk hari istirahat/libur resmi) | Terverifikasi resmi | PP 35/2021 Pasal 26 — [3] |
| Upah sejam = 1/173 × upah sebulan | Terverifikasi resmi | Pasal 32 ayat (2) — [3] |
| Hari kerja: jam pertama 1,5×, jam berikutnya 2× upah sejam | Terverifikasi resmi | Pasal 31 ayat (1) — [3] |
| Hari istirahat/libur, 6 hari kerja: jam 1–7 2×, jam 8 3×, jam 9–11 4×; libur di hari kerja terpendek: jam 1–5 2×, jam 6 3×, jam 7–9 4× | Terverifikasi resmi | Pasal 31 ayat (2) — [3] |
| Hari istirahat/libur, 5 hari kerja: jam 1–8 2×, jam 9 3×, jam 10–12 4× | Terverifikasi resmi | Pasal 31 ayat (3) — [3] |
| Dasar: upah pokok + tunjangan tetap (100%); bila ada tunjangan tidak tetap dan pokok+tetap < 75% total upah, dasar = 75% total upah | Terverifikasi resmi | Pasal 32 ayat (3)–(4) — [3] |
| Pekerja golongan jabatan tertentu (diatur di PK/PP/PKB) tidak wajib dibayar lembur | Terverifikasi resmi | Pasal 27 — [3] |

## Upah
| Fakta | Status | Sumber |
|---|---|---|
| UMK/UMP ditetapkan gubernur setiap tahun — **skill tidak menyimpan angka UMK**, pengguna mengisi | — | SK Gubernur/Disnaker setempat |
| Upah pokok minimal 75% dari (upah pokok + tunjangan tetap) | Sekunder | PP 36/2021 Pasal 7 ayat (2) — [11] |
| Usaha mikro & kecil dikecualikan dari upah minimum dengan syarat tertentu | Sekunder | PP 36/2021 Pasal 36 — [11] |

## PPh 21
Semua fakta PPh 21 (tabel TER, PTKP, Pasal 17, biaya jabatan, Masa Pajak Terakhir, PMK 105/2025 DTP) sama dengan skill `pph21-ter`; statusnya **terverifikasi resmi** dari PP 58/2023, PMK 168/2023, UU HPP, dan PMK 105/2025 — [7], [8]. Yang khusus relevan untuk slip gaji:
- Premi JKK, JKM, dan iuran BPJS Kesehatan yang dibayar pemberi kerja **masuk penghasilan bruto** PPh 21 (PMK 168/2023 Pasal 5 ayat (3) huruf d–e).
- Iuran JHT & JP bagian pemberi kerja **bukan** objek PPh 21 (Pasal 7 huruf c); JHT 2% + JP 1% bagian karyawan menjadi **pengurang** saat hitung ulang Desember (Pasal 10 ayat (1) huruf b).
- Desember / bulan berhenti kerja wajib hitung ulang setahun, sehingga slip bulan itu butuh data Januari s.d. bulan lalu.
- PPh 21 DTP: PPh 21 tetap dipotong, lalu nilai yang sama dibayar tunai ke karyawan dan tidak dikenai pajak, sehingga gaji bersih tidak berkurang karena pajak; bagian DTP tidak disetor ke negara (PMK 105/2025 Pasal 2 ayat 1, Pasal 5, Pasal 6 ayat 6, Lampiran B). Rincian & kutipan: `references/dtp-pmk105.md`.

## Keputusan desain (bukan aturan)
- Iuran BPJS dan lembur dibulatkan ke rupiah terdekat per komponen; PPh 21 dibulatkan ke bawah. Belum dicocokkan dengan aplikasi BPJS/Coretax; bila berbeda, ikuti sistem resmi.
- PPh 21 dihitung dengan skema "dipotong dari gaji" (bukan gross-up/tunjangan pajak).

## Sumber
1. Perpres 64/2020 (salinan): https://www.llg-bwi.org/file_publish/Perpres%20Nomor%2064%20Tahun%202020.pdf · JDIH BPK: https://peraturan.bpk.go.id/Details/136650/perpres-no-64-tahun-2020
2. PP 44/2015 (situs resmi BPJSTK): https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104557_PP%2044%20Tahun%202015.pdf
3. PP 35/2021 (JDIH Kemnaker): https://jdih.kemnaker.go.id/asset/data_puu/PP352021.pdf
4. BPJS Ketenagakerjaan, "Berapa Besaran Iuran JHT, JKK, JKM, JP dan JKP?" (17 Des 2025): https://www.bpjsketenagakerjaan.go.id/artikel/18913/artikel-berapa-besaran-iuran-jht,-jkk,-jkm,-jp-dan-jkp — catatan: artikel ini masih menulis batas JP lama "Rp 10.547.000" (salah ketik dari 10.547.400) dan belum memuat kenaikan Maret 2026 — untuk 2026 gunakan surat B/1226/022026 [5]. Bagian JKP artikel ini masih memuat contoh rekomposisi JKM yang tidak disebut di PP 6/2025 Pasal 11 (rekomposisi JKM 0,10% berasal dari PP 37/2021 [13] dan dihapus PP 6/2025); untuk JKP ikuti PP 6/2025 [12].
5. Surat BPJS Ketenagakerjaan Jakarta Ceger No. B/1226/022026 (25 Feb 2026) "Ketentuan Batas Upah dan Manfaat Jaminan Pensiun Tahun 2026" (salinan): https://494075.fs1.hubspotusercontent-na1.net/hubfs/494075/compliance-portal/notification-number-b1226022026.pdf
6. Akun resmi BPJS Ketenagakerjaan @BPJSTKinfo (Mar 2026): https://x.com/BPJSTKinfo/status/2028647882178388161
7. PMK 168/2023: https://jdih.kemenkeu.go.id/dok/pmk-168-tahun-2023 · PP 58/2023: https://jdih.kemenkeu.go.id/dok/pp-58-tahun-2023
8. PMK 105/2025: https://jdih.kemenkeu.go.id/dok/pmk-105-tahun-2025
9. Perpres 82/2018 (JDIH BPK): https://peraturan.bpk.go.id/Details/94711/perpres-no-82-tahun-2018
10. Berita perpanjangan diskon JKK s.d. Jan 2026: https://nasional.kontan.co.id/news/aturan-direvisi-diskon-50-iuran-jkk-untuk-industri-padat-karya-hingga-januari-2026
11. PP 36/2021 (JDIH Kemnaker): https://jdih.kemnaker.go.id/asset/data_puu/PP362021.pdf (dokumen pindaian; pasal dikutip dari sumber sekunder, belum dibaca langsung)
12. PP 6/2025 tentang Perubahan atas PP 37/2021 tentang Penyelenggaraan Program JKP, ditetapkan & diundangkan 7 Februari 2025, berlaku sejak diundangkan (JDIH Kemnaker, dibaca 2026-10-15): https://jdih.kemnaker.go.id/peraturan/detail/2640/peraturan-pemerintah-nomor-6-tahun-2025 · PDF: https://jdih.kemnaker.go.id/asset/data_puu/2025pp006.pdf
13. PP 37/2021 tentang Penyelenggaraan Program JKP (JDIH Kemnaker; dokumen pindaian tanpa lapisan teks, Pasal 11 dibaca langsung dari halaman 9 pada 2026-10-15): https://jdih.kemnaker.go.id/asset/data_puu/PP372021.pdf
