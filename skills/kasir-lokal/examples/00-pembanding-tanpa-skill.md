# 00 — Uji A/B: skenario 01 (warung kopi sehari) TANPA skill vs DENGAN skill

Penguji: agent penguji independen (simulasi, Claude Code), 2026-09-23/24. Permintaan & urutan pesan sama dengan `01-warung-kopi-sehari-penuh.md`. Versi "tanpa skill" dikerjakan seperti AI agent biasa yang tidak membaca skill apa pun (boleh berhitung sendiri, boleh membuat file bila berinisiatif).

## Permintaan pembuka
> pakai kasir buat kedai saya ya. nama Kedai Kopi Senja, Jl. Contoh No. 1 Bandung, telp 0812-0000-1111. belum PKP, printer 58. ini menunya (produk.csv)

| | TANPA skill | DENGAN skill kasir-lokal |
|---|---|---|
| Jawaban pembuka | "Saya tidak punya aplikasi kasir, tapi bisa membantu mencatat penjualan di chat ini. Saya sudah baca menu Anda (15 item). Kirim pesanan satu per satu, saya hitung totalnya. Untuk jangka panjang, saya sarankan aplikasi kasir (Moka/Majoo/Olsera) atau template Excel; mau saya buatkan template Excel dengan rumus?" | Database kasir lokal dibuat + 15 produk diimpor dari CSV Excel (`;`, BOM, "Rp 18.000") dengan pratinjau pemetaan kolom → "ya" → tersimpan + backup otomatis. |
| Penyimpanan data | Hanya di riwayat chat; hilang saat sesi baru / konteks penuh. | Satu file SQLite di komputer pemilik; nota bernomor N-YYMMDD-0001 permanen. |

## Nota pertama: "dua kopi susu, satu roti bakar keju, bayar tunai 50rb"

**TANPA skill:**
```
Pesanan:
- 2 Kopi Susu Gula Aren x Rp 18.000 = Rp 36.000
- 1 Roti Bakar Keju x Rp 17.000 = Rp 17.000
Total: Rp 53.000
Dibayar: Rp 50.000
Kurang Rp 3.000 — mohon tambahkan pembayaran.
```
(Hitungan benar. Tidak ada nomor nota, tidak tersimpan, "kopi susu" langsung diasumsikan Gula Aren tanpa diberitahu.)

**DENGAN skill:** script menolak "Pembayaran KURANG Rp 3.000", lalu setelah dikoreksi memberi pratinjau bernomor `N-260924-0001`, menyebut *"'kopi susu' dibaca sebagai Kopi Susu Gula Aren (KSGA)"*, menyimpan hanya setelah "ya".

## Titik-titik yang membedakan (diuji pada 12 nota yang sama)

| Kejadian | TANPA skill | DENGAN skill |
|---|---|---|
| "es teh 2 sama roti bakar" (ambigu) | Cenderung menebak Es Teh Manis & Roti Bakar Coklat (varian termurah/pertama) atau bertanya — tidak konsisten. | Selalu ditolak + daftar pilihan (Es Teh Manis/Lemon, Roti Bakar Coklat/Keju). |
| Diskon bertingkat "3 es teh manis diskon 10%+5%" | Dihitung di kepala: 18.000 − 10% = 16.200 − 5% = 15.390 (benar), tetapi aturan pembulatan tidak tertulis & bisa berbeda tiap nota. | 2.610 diskon, aturan pembulatan tetap (rupiah terdekat per langkah), sama di semua nota. |
| Dobel ketik nota 19:05 | Tidak terdeteksi — tercatat dua kali di rekap chat. | "Isi nota SAMA PERSIS dengan N-260924-0011 … kemungkinan tercatat dobel" + `--ya` ditolak tanpa izin. |
| Void nota 11:45 | Nota dihapus dari daftar di chat, tanpa jejak. | Entri balik R-260924-0001 beralasan; nota asal tetap ada; uang kembali per metode asal. |
| Retur 1 cappuccino dari nota berdiskon nota 10% | Tidak ada aturan baku: bisa mengembalikan 22.000 (harga), 21.000 (harga − separuh diskon item), atau 18.900 (benar) tergantung cara agent menalar; selisihnya Rp 2.100–3.100. | 18.900 (baris bersih 37.800 ÷ 2), cocok dengan verifikasi independen. |
| Tutup kasir "uang di laci 425.000" | Harus menjumlah ulang semua pesan hari itu; kas awal, kembalian per nota (termasuk kembalian dari nota campuran QRIS+tunai N-0010), refund void/retur, kas keluar harus diingat semua. Hasilnya bisa benar bila agent teliti, tetapi tidak ada mekanisme yang menjamin; satu nota terlewat/dobel langsung membuat selisih palsu. (Catatan jujur: penguji tidak dapat "melupakan" skill sepenuhnya, jadi versi tanpa skill dinilai dari kemampuan yang tersedia, bukan dari satu kesalahan hitung yang terjadi.) | "Seharusnya Rp 425.990, dihitung Rp 425.000, SELISIH KURANG Rp 990" + total non-tunai per metode untuk dicocokkan mutasi bank. Terverifikasi independen. |
| Rekap harian | Ringkasan teks bebas; per jam & per produk hanya jika diminta; format berubah-ubah. | Format tetap siap Telegram: kotor, diskon, retur/void, bersih, per metode, 10 produk terlaris, per jam. |
| Rekap otomatis ke Telegram | Menjelaskan secara umum ("bisa pakai bot Telegram/Zapier"). | Perintah OpenClaw siap pakai (cron 21.00 WIB, hanya-baca), sintaks cocok dengan CLI asli. |
| Struk 58 mm | Teks struk di chat; tidak ada file siap cetak dengan ukuran kertas benar. | File HTML dengan `@page 58mm`, lebar teks 32 kolom, dicek Chromium → PDF 57,8 mm, 1 halaman, tidak terpotong. |
| Besok / bulan depan | Tidak ada data kemarin (kecuali pengguna menyalin sendiri). | Rekap bulanan/tahunan + omzet untuk PPh final dari data yang sama. |

## Penilaian
| Kriteria | Tanpa skill | Dengan skill |
|---|:-:|:-:|
| Hitungan satu nota | 8 | 10 |
| Konsistensi & anti-salah (ambigu, dobel, bayar kurang) | 4 | 10 |
| Void/retur dengan jejak | 2 | 9 |
| Tutup kasir & selisih | 3 | 10 |
| Data tersimpan lintas hari | 1 | 10 |
| Struk siap cetak | 3 | 8 |
| Rekap siap kirim & jadwal | 4 | 9 |

**Kesimpulan:** dengan skill **jelas jauh lebih baik**. Tanpa skill, agent hanya menjadi kalkulator chat tanpa memori permanen; hitungan satu nota bisa benar, tetapi tutup kasir, retur berdiskon nota, deteksi dobel, dan rekap lintas hari tidak dapat diandalkan. Skill menambah nilai yang tidak bisa diberikan AI biasa: database lokal, nomor nota, jejak koreksi, rekonsiliasi laci, struk ukuran printer, dan ekspor ke skill lain. Bahan "sebelum/sesudah" README valid.
