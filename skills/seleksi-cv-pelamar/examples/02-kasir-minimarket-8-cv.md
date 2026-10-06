# Contoh 2: kasir minimarket, 8 CV

> Contoh rancangan pembuat; bukan hasil uji platform. CV fiktif ada di `data/kasir-minimarket/`, kriteria di `data/kasir-minimarket.json`. Skor diverifikasi dengan `scripts/nilai_cv.py` lalu dibaca ulang.

## Masukan pengguna
"Minimarket saya buka 2 shift. Cari 3 kasir. Ada 8 CV. Pilih 3 yang paling siap, kasih pertanyaan wawancara, dan pesannya."

## Keluaran di chat

Dari 8 CV: 3 lanjut wawancara, 2 cadangan, 3 belum sesuai kebutuhan saat ini.

**Kriteria yang saya pakai**
- Wajib: pengalaman kasir (min. 1 tahun), mesin kasir/POS dan pembayaran digital (QRIS/EDC), hitung dan rekap kas, bisa kerja shift.
- Nilai tambah: stok dan penataan rak, pernah melatih atau memimpin.
- Bagian data fisik dan data pribadi di CV tidak dinilai.

**Ranking**
| Kode | Skor dan status | Alasan |
|---|---|---|
| C1 Rudi | 100, lanjut | 11 tahun kasir dan supervisor, jadwal shift 6 orang |
| C2 Rini | 100, lanjut | 7 tahun kasir minimarket, melatih kasir baru |
| C3 Eko | 88, lanjut | 5 tahun kasir toko grosir, QRIS dan setoran harian |
| C4 Maya | 88, cadangan | 4 tahun kasir minimarket; melatih/memimpin belum terlihat |
| C5 Galih | 66, cadangan | 1 tahun kasir toko roti; shift belum terlihat |
| C6 Putri | 56, belum sesuai saat ini | 1 tahun kasir pengganti warung; mesin POS belum terlihat |
| C7 Winda | 36, belum sesuai saat ini | Baru PKL kasir 3 bulan; belum ada pengalaman kerja penuh |
| C8 Ilham | 0, belum sesuai saat ini | Pengalaman operator produksi; belum ada pengalaman kasir |

**Shortlist: detail dan pertanyaan**

**C1 Rudi (100).** Kasir: Terpenuhi, "Kasir dan Supervisor Toko" 2010-2021 (toko serba ada). POS/QRIS: Terpenuhi, di keahlian "mesin POS, QRIS" (tanpa contoh kerja, jadi ditanyakan). Rekap kas: Terpenuhi, "Rekap kas harian dan laporan penjualan". Shift: Terpenuhi, "jadwal shift 6 orang". Perlu dipastikan: apakah nyaman kembali menjadi kasir (bukan supervisor) dan kesediaan jam malam.
1. Bila selisih kas Rp50.000 di akhir shift, apa langkah Anda sebelum melapor?
2. Pernah memakai QRIS dan EDC? Ceritakan satu kendala dan penyelesaiannya.
3. Posisi ini kasir, bukan supervisor. Bagaimana Anda memandangnya?
4. Ceritakan cara Anda mengatur jadwal shift 6 orang yang adil.

**C2 Rini (100).** Kasir: Terpenuhi, "Kasir Senior" 2017-2020 setelah kasir 2012-2016. POS/QRIS: Terpenuhi, "Mesin kasir POS, EDC, QRIS". Rekap kas: Terpenuhi, "selisih kas harian". Melatih: Terpenuhi, "Melatih kasir baru". Perlu dipastikan: ada jeda 2021-2025 yang tidak ditulis; tanyakan kegiatan dan kesiapan kembali.
1. Boleh ceritakan apa yang Anda kerjakan sejak 2021, dan seberapa siap kembali bekerja shift?
2. Bagaimana Anda melatih kasir baru supaya cepat tidak salah kembalian?
3. Pernah menemukan uang palsu atau QRIS palsu? Apa langkah Anda?
4. Tunjukkan cara menutup kas harian yang Anda biasa pakai.

**C3 Eko (88).** Kasir: Terpenuhi, "Kasir" 2019-2024 (juga pramuniaga 2015-2018). POS/QRIS: Terpenuhi, "Kasir tunai dan QRIS". Rekap kas: Terpenuhi, "Hitung uang kas dan setoran harian". Shift: Terpenuhi, "Shift bergantian". Melatih: Belum terlihat. Perlu dipastikan: apakah toko grosir berbeda dengan minimarket (kecepatan antrean).
1. Kecepatan antrean di minimarket berbeda dengan grosir; bagaimana Anda menyesuaikan?
2. Bila pelanggan komplain harga di kasir tidak sama dengan rak, apa yang Anda lakukan?
3. Pernah memegang peran memimpin atau melatih rekan? Ceritakan.
4. Ceritakan satu hari tersibuk dan cara Anda menjaga hitungan tetap akurat.

**Draf pesan** (Anda yang mengirim satu per satu)

*Lanjut wawancara:*
> Halo [nama panggilan], terima kasih sudah melamar sebagai Kasir di [nama minimarket]. Pengalaman Anda [satu hal nyata dari CV] sesuai dengan yang kami cari. Kami undang wawancara pada [isian: hari, tanggal, jam] di [isian: alamat]. Mohon konfirmasi sebelum [isian: batas]. Seleksi tidak dipungut biaya apa pun.

*Cadangan:*
> Halo [nama panggilan], terima kasih sudah melamar sebagai Kasir. Saat ini kami memprioritaskan beberapa kandidat lebih dulu; bila ada kebutuhan lanjutan kami hubungi Anda lagi sebelum [isian: perkiraan waktu].

*Belum sesuai kebutuhan saat ini:*
> Halo [nama panggilan], terima kasih sudah melamar dan menyiapkan CV. Untuk saat ini kami belum dapat melanjutkan karena kebutuhan posisi kasir kami belum sesuai dengan profil Anda. Kami menghargai minat Anda dan mendoakan yang terbaik.

**Rekap untuk Anda:** 8 CV; syarat paling sering belum terlihat adalah "bisa shift" (3 dari 8) dan mesin POS (2 dari 8). Karena shift adalah syarat kerja yang sah, tanyakan langsung di wawancara. Data fisik di salah satu CV (tinggi dan berat badan) tidak saya pakai dan tidak saya tulis; Anda tidak perlu memintanya dari pelamar lain. Simpan CV hanya di komputer Anda dan hapus setelah proses selesai.

**Asumsi:** pengalaman kasir minimal 1 tahun; 3 orang untuk dua shift.
Boleh saya tahu: (1) jadwal wawancara dan alamat minimarket? (2) apakah shift malam wajib atau bergilir? (3) kapan kasir baru harus mulai?
