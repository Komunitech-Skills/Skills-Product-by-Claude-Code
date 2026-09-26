# Utang, Pinjol, dan Gali Lubang Tutup Lubang

> Dicek 26 September 2026 lewat pencarian web (sumber di bawah). Aturan & angka bisa berubah — sarankan pengguna mengecek ulang di situs resmi OJK/BI. Ini informasi umum, bukan nasihat hukum atau keuangan.

## Batas bunga yang dipakai script sebagai "alarm"
| Jenis | Batas | Dasar | Dipakai untuk |
|---|---|---|---|
| Kartu kredit | 1,75% per bulan (±21% per tahun) | Ketentuan Bank Indonesia, berlaku sejak Juli 2021, masih dipertahankan | Peringatan bila bunga kartu kredit yang dimasukkan lebih tinggi |
| Pinjaman daring (pinjol/LPBBTI) konsumtif | 0,1% per hari (2026) — sebelumnya 0,3% (2024) dan 0,2% (2025) | SEOJK No. 19/SEOJK.05/2023 (penurunan bertahap) | Bunga > ±3% per bulan → curigai pinjol ilegal |
| Pinjol produktif | 0,067% per hari (2026) | SEOJK yang sama | Informasi |

Catatan: "manfaat ekonomi" pinjol legal mencakup bunga dan biaya lain; bila total biaya yang diminta jauh di atas batas, itu tanda bahaya.

## Cara cek legalitas pinjol (sebelum meminjam atau bila ragu)
- Situs resmi OJK: **ojk.go.id** → daftar penyelenggara fintech lending (LPBBTI) berizin. Per 31 Agustus 2026 tercatat **94** penyelenggara berizin.
- **Kontak OJK 157** (telepon).
- **WhatsApp OJK 081-157-157-157** — kirim nama aplikasi yang ingin dicek.
- Aktivitas keuangan ilegal diberantas oleh **Satgas PASTI** (Satuan Tugas Pemberantasan Aktivitas Keuangan Ilegal); pengaduan pinjol ilegal bisa disampaikan lewat kanal OJK di atas.

## Ciri pinjol ilegal (sampaikan ke pengguna dengan bahasa sederhana)
- Tidak terdaftar/berizin OJK; nama aplikasi sering berganti.
- Meminta akses **kontak, galeri, lokasi** — lalu dipakai untuk menagih ke orang lain.
- Bunga/biaya tidak jelas, potongan besar di muka ("cair 1 juta, diterima 600 ribu"), tenor sangat pendek (7–14 hari).
- Menawarkan lewat SMS/WA pribadi tanpa diminta.
- Penagihan dengan ancaman, makian, atau menyebar data.

## Gali lubang tutup lubang — mengapa berbahaya
Meminjam di tempat baru untuk membayar cicilan lama tidak mengurangi utang; justru **menambah biaya** (bunga + biaya admin kedua) dan memperpendek waktu. Pola umumnya: 1 pinjol → 3 pinjol → penagihan dari banyak pihak.
Yang disarankan skill ini:
1. **Stop menambah utang baru** (termasuk paylater untuk belanja rutin).
2. Daftar semua utang (template `templates/daftar-utang.md`), hitung bunga efektifnya.
3. Susun anggaran zero-based; cari uang ekstra dari pos Keinginan.
4. Jalankan Avalanche/Snowball dengan anggaran tetap.
5. Jika total cicilan tidak tertanggung: hubungi kreditur **resmi** untuk restrukturisasi (perpanjangan tenor, keringanan) — minta tertulis.
6. Penagihan dengan ancaman/penyebaran data: simpan bukti, adukan ke OJK (157); bila ada ancaman pidana, laporkan ke polisi.
7. Jangan menyarankan "tidak usah bayar" untuk utang yang sah; utang ke pinjol **ilegal** tetap arahkan ke kanal pengaduan resmi.

## Bunga flat vs efektif
- **Flat:** bunga dihitung dari pokok awal sepanjang tenor. Umum di leasing motor/mobil dan sebagian KTA/koperasi.
- **Efektif (anuitas/menurun):** bunga dihitung dari sisa pokok. Umum di KPR, kartu kredit, sebagian KTA bank.
- Flat 12%/th tenor 24 bulan ≈ efektif **21,57%/th**; flat 10%/th tenor 12 bulan ≈ efektif **17,97%/th**. Selalu bandingkan penawaran dengan angka efektif (`python3 scripts/keuangan.py konversi-flat ...`).

## Kartu kredit & paylater
- Bayar **minimum** saja = sisa tagihan tetap berbunga; utang lama sekali lunasnya. Relaksasi BI sampai 31 Desember 2026: pembayaran minimum 5% dan denda maksimal Rp100.000 (cek ulang setelah tanggal itu).
- Paylater = utang. Catat sebagai utang di daftar, bukan sebagai "cara bayar".

## Sumber (diakses 26 September 2026)
- Bisnis.com — "Daftar 94 Pinjol Resmi OJK per Agustus 2026": https://finansial.bisnis.com/read/20260810/563/1994930/daftar-94-pinjol-resmi-ojk-per-agustus-2026-cek-legalitas-sebelum-pinjam
- Portal.id — "OJK Catat Ada 94 Pinjol Legal, Masyarakat Diminta Cek ke Kontak 157": https://portal.id/ojk-catat-ada-94-pinjol-legal-masyarakat-diminta-cek-ke-kontak-157/
- Periskop.id — "Ciri Pinjol Ilegal dan Cara Cek Legalitasnya di Kanal Resmi OJK": https://periskop.id/pembiayaan/20260817/ciri-pinjol-ilegal-cara-cek-legalitas
- OJK — Infografis pemberantasan pinjol ilegal: https://ojk.go.id/id/berita-dan-kegiatan/info-terkini/Pages/Infografis-OJK-Bersama-Kementerian-atau-Lembaga-Terkait-Berkomitmen-Berantas-Pinjol-Ilegal.aspx
- Bisnis.com — "Kisi-kisi Aturan Baru Pinjol" (SEOJK 19/2023): https://finansial.bisnis.com/read/20231112/563/1713428/kisi-kisi-aturan-baru-pinjol-dari-batasan-utang-hingga-penurunan-bunga
- ANTARA — "OJK tetapkan suku bunga pinjol produktif 0,067 persen/hari pada 2026": https://www.antaranews.com/berita/3848418/ojk-tetapkan-suku-bunga-pinjol-produktif-0067-persen-hari-pada-2026
- ANTARA — "BI pertahankan batas maksimum suku bunga kartu kredit 1,75 persen": https://www.antaranews.com/berita/3319017/bi-pertahankan-batas-maksimum-suku-bunga-kartu-kredit-175-persen
- CNBC Indonesia — "Segini Batas Maksimum Bunga Kartu Kredit Indonesia" (2026): https://www.cnbcindonesia.com/market/20260818084032-17-760171/segini-batas-maksimum-bunga-kartu-kredit-indonesia-ritel
- Infobanknews — BI perpanjang keringanan tagihan kartu kredit hingga 31 Desember 2026: https://infobanknews.com/bi-perpanjang-keringanan-tagihan-kartu-kredit-hingga-31-desember-2026
