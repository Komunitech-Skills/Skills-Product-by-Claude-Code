# Uji A/B — Skenario 01 TANPA skill vs DENGAN skill

> Penguji independen, 25 September 2026. Input sama persis dengan `01-susun-toko-roti-bandung.md`.
> **Keterbatasan metode (jujur):** tidak tersedia sesi agent kedua yang benar-benar "bersih". Output "tanpa skill" ditulis penguji dengan meniru jawaban umum asisten AI tanpa membuka folder skill (pengetahuan umum hukum ketenagakerjaan, tanpa script). Karena penguji sudah membaca skill, baseline ini cenderung **lebih baik** daripada agent polos sungguhan, jadi perbandingan ini konservatif (menguntungkan pihak tanpa skill).

## Input
> "Saya punya toko roti di Bandung (Roti Hangat, Jl. Sukajadi). Mau rekrut 2 orang bagian produksi, Asep dan Rina, kontrak 1 tahun mulai 1 Oktober 2026. Gaji pokok 3,9 juta + tunjangan tetap 250 ribu, uang makan 20 ribu per hari masuk. Kerja Senin–Sabtu jam 7 pagi sampai 3 sore. Alasannya kami buka lini baru roti beku untuk dijual ke kafe, masih uji pasar setahun. Tolong bikinin kontraknya dan hitung kompensasi akhirnya."

## A. Output TANPA skill (ringkas, representatif)
> **SURAT PERJANJIAN KERJA WAKTU TERTENTU**
> Pihak Pertama: Roti Hangat, Jl. Sukajadi, Bandung, diwakili oleh [Nama Pemilik]. Pihak Kedua: Asep, [alamat].
> Pasal 1 Jabatan: Staf Produksi. Pasal 2 Jangka Waktu: 1 Oktober 2026 – 30 September 2027; dapat diperpanjang sesuai kebutuhan perusahaan dan kinerja karyawan.
> Pasal 3 Jam Kerja: Senin–Sabtu 07.00–15.00, istirahat 1 jam.
> Pasal 4 Gaji: gaji pokok Rp3.900.000, tunjangan tetap Rp250.000, uang makan Rp20.000/hari. UMK Kota Bandung 2026 sekitar Rp4,7 juta, sehingga *disarankan menyesuaikan gaji*.
> Pasal 5 Hak: BPJS Ketenagakerjaan & Kesehatan, THR, cuti 12 hari.
> Pasal 6 Pengakhiran: masing-masing pihak dapat mengakhiri dengan pemberitahuan 30 hari; pihak yang melanggar membayar ganti rugi sesuai peraturan.
> Pasal 7 Kompensasi: sesuai PP 35/2021.
> Pasal 8 Kerahasiaan. Pasal 9 Perselisihan. Tanda tangan bermeterai.
>
> **Kompensasi akhir:** 12 bulan → 1 bulan upah = gaji pokok + tunjangan = **Rp4.150.000** per orang (uang makan tidak termasuk). Untuk 2 orang Rp8.300.000.
> *Catatan: ini bukan nasihat hukum, konsultasikan ke ahli.*

## B. Output DENGAN skill
Lihat `01-susun-toko-roti-bandung.md` (draf 12 pasal lengkap + catatan pengisian + checklist + disclaimer).

## Penilaian berdampingan (skala 0–2 per kriteria)
| # | Kriteria | Tanpa skill | Dengan skill | Catatan |
|---|---|---|---|---|
| 1 | Angka kompensasi benar & dapat diaudit (rumus/script) | 2 | 2 | Keduanya Rp4.150.000; hanya versi skill menampilkan rumus, batas 5 tahun (30 Sep 2031), dan output script |
| 2 | Tidak mengarang data (UMK, identitas, tanggal) | 0 | 2 | Tanpa skill menyebut "UMK Bandung sekitar Rp4,7 juta" tanpa sumber; skill menulis `[isi: UMK ... cek Disnaker]` |
| 3 | Uji kelayakan PKWT (alasan waktu tertentu ditulis & risiko PKWTT) | 0 | 2 | Tanpa skill tidak menulis alasan "produk baru" di kontrak, padahal itu yang menyelamatkan status PKWT |
| 4 | Batas 5 tahun & perpanjangan tertulis | 0 | 2 | Tanpa skill: "diperpanjang sesuai kebutuhan" (tanpa batas) |
| 5 | Larangan masa percobaan dinyatakan eksplisit | 0 | 2 | |
| 6 | Pasal kompensasi & ganti rugi Pasal 62 tertulis jelas (dua arah) | 1 | 2 | Tanpa skill: "sesuai PP 35/2021" dan "pihak yang melanggar" (kabur) |
| 7 | Jam kerja ≤ 40 jam/minggu | 0 | 1 | Tanpa skill menyalin 42 jam/minggu. Dengan skill tertangkap berkat template "40 jam seminggu", tetapi checklist B7 ("7 jam × 6 hari") justru bisa meloloskannya → nilai 1 |
| 8 | Isi minimal PP 35/2021 Pasal 13 + pencatatan 3 hari kerja + bahasa Indonesia/huruf latin | 1 | 2 | Tanpa skill tidak menyebut pencatatan |
| 9 | Terbilang rupiah, `[isi]` terdaftar, checklist tanda tangan | 0 | 2 | |
| 10 | Disclaimer dengan dasar aturan + tanggal + status MK 168 / RUU | 1 | 2 | Tanpa skill: disclaimer generik tanpa dasar & tanggal |
| | **Total (maks 20)** | **5** | **19** | |

## Kesimpulan
Dengan skill **jelas lebih baik** (19 vs 5). Nilai tambah utama bukan pada angka kompensasi (kasus 12 bulan mudah), melainkan pada kepatuhan: alasan PKWT, batas 5 tahun, tanpa masa percobaan, UMK tidak dikarang, jam kerja, pencatatan, dan disclaimer bertanggal. Bahan "sebelum/sesudah" README valid.
