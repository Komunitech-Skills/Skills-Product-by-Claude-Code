# Contoh 3: staf akuntansi, 10 CV

> Contoh rancangan pembuat; bukan hasil uji platform. CV fiktif ada di `data/staf-akuntansi/`, kriteria di `data/staf-akuntansi.json`. Skor diverifikasi dengan `scripts/nilai_cv.py` lalu dibaca ulang.

## Masukan pengguna
"CV Maju Bersama, distribusi bahan bangunan, butuh staf akuntansi. Syaratnya pengalaman minimal 2 tahun, bisa Accurate atau Excel, rekonsiliasi bank, laporan keuangan; plus kalau paham PPh 21 dan PPN. 10 CV, pilih 4."

## Keluaran di chat

Dari 10 CV: 4 lanjut wawancara, 3 cadangan, 3 belum sesuai kebutuhan saat ini (1 di antaranya belum terlihat pengalaman akuntansinya, perlu dikonfirmasi).

**Kriteria yang saya pakai**
- Syarat dasar: pengalaman akuntansi/pembukuan minimal 2 tahun.
- Wajib: perangkat akuntansi (Accurate/Zahir/MYOB/Excel), rekonsiliasi bank, laporan keuangan.
- Nilai tambah: pajak PPh 21/PPN (min. 1 tahun), hutang piutang.

**Ranking**
| Kode | Skor dan status | Alasan |
|---|---|---|
| C1 Tiara | 100, lanjut | 5 tahun akuntansi dan pajak; Accurate, e-Faktur, Coretax |
| C2 Retno | 94, lanjut | 7 tahun staf akuntansi; hutang piutang belum terlihat |
| C3 Mei Lin | 94, lanjut | 3 tahun staf akuntansi + bendahara; tidak pakai Accurate (Zahir) |
| C4 Siska | 94, lanjut | 3 tahun akuntansi, Accurate Online, PPh 21 |
| C5 Budi | 83, cadangan | 12 tahun, terakhir Kepala Akuntansi; rekonsiliasi belum terlihat |
| C6 Arief | 83, cadangan | 3 tahun Accurate; laporan keuangan belum terlihat |
| C7 Taufik | 77, cadangan | 3 tahun pembukuan di Excel/Zahir; laporan keuangan belum terlihat |
| C8 Alya | 66, belum sesuai saat ini | Magang 6 bulan dan lulusan baru; belum mencapai 2 tahun |
| C9 Yusuf | 29, belum sesuai saat ini | Catat kas di gudang; jurnal dan laporan belum terlihat |
| C10 Hendro | 17, perlu konfirmasi | Pengalaman proyek konstruksi; pengalaman akuntansi belum terlihat |

**Shortlist: detail dan pertanyaan**

**C1 Tiara (100).** Pengalaman: Terpenuhi, "Staf Akuntansi dan Pajak" 2019-2024. Perangkat: Terpenuhi, "hutang piutang di Accurate". Rekonsiliasi: Terpenuhi, "Rekonsiliasi bank dan hutang piutang". Laporan: Terpenuhi, "laporan keuangan bulanan dan tahunan". Pajak: Terpenuhi, "PPh 21, PPh 23, dan PPN (e-Faktur, Coretax)". Perlu dipastikan: skala transaksi per bulan.
1. Berapa kira-kira jumlah transaksi dan karyawan yang Anda urus per bulan?
2. Ceritakan kasus rekonsiliasi bank yang selisihnya sulit ditemukan.
3. Bagaimana Anda menutup buku bulanan dalam urutan langkah?
4. Ceritakan satu kali SPT Masa terlambat atau salah dan penanganannya.

**C2 Retno (94).** Pengalaman: Terpenuhi, "Staf Akuntansi" 2017-2024. Perangkat: Terpenuhi, "Input jurnal, buku besar... di Accurate". Laporan: Terpenuhi. Pajak: Terpenuhi, "PPh 21 dan PPN lewat e-Faktur". Hutang piutang: Belum terlihat. Perlu dipastikan: pengelolaan hutang piutang.
1. Bagaimana Anda mencatat dan menagih piutang yang jatuh tempo?
2. Ceritakan analisis biaya di Excel (pivot) yang pernah mengubah keputusan.
3. Apa yang Anda lakukan bila faktur pajak mitra tidak sesuai?
4. Kapan Anda bisa mulai bekerja?

**C3 Mei Lin (94).** Pengalaman: Terpenuhi, "Staf Akuntansi" 2016-2019 (3 tahun). Perangkat: Terpenuhi, "Excel, Zahir". Rekonsiliasi: Terpenuhi, "rekonsiliasi bank" (bendahara paruh waktu 2021-2024). Laporan: Terpenuhi. Pajak: Terpenuhi, "PPN masukan dan keluaran" (PPh 21 belum terlihat). Perlu dipastikan: jeda 2019-2021 dan kesiapan memakai Accurate.
1. Bagaimana Anda mempelajari Accurate bila belum pernah memakainya?
2. Boleh ceritakan kegiatan Anda pada 2020?
3. Ceritakan pekerjaan PPN yang paling rumit yang pernah Anda urus.
4. Bagaimana Anda menjaga ketelitian bila pekerjaan paruh waktu tumpang tindih jadwal?

**C4 Siska (94).** Pengalaman: Terpenuhi, "Staf Akuntansi" 2023-sekarang (3 tahun) setelah admin keuangan 2021-2022. Perangkat: Terpenuhi, "Jurnal harian di Accurate Online". Rekonsiliasi: Terpenuhi. Laporan: Terpenuhi, "laporan keuangan sederhana" (di posisi sebelumnya; kedalamannya ditanyakan). Pajak: Terpenuhi, "Hitung PPh 21 karyawan 12 orang". Perlu dipastikan: kedalaman laporan keuangan dan alasan pindah.
1. Laporan keuangan apa saja yang sudah Anda susun sendiri sampai selesai?
2. Apa yang Anda cari dari tempat kerja baru dibanding sekarang?
3. Bagaimana langkah Anda menghitung PPh 21 bulanan untuk karyawan baru dan yang resign?
4. Ceritakan kesalahan pencatatan yang pernah Anda temukan dan perbaiki.

**Draf pesan** (Anda yang mengirim satu per satu)

*Lanjut wawancara:*
> Yth. [Bapak/Ibu nama], terima kasih telah melamar sebagai Staf Akuntansi di CV Maju Bersama. Pengalaman Anda [satu hal nyata dari CV] sesuai kebutuhan kami. Kami undang wawancara pada [isian: hari, tanggal, jam] di [isian: lokasi/tautan]. Mohon konfirmasi kehadiran sebelum [isian: batas]. Proses seleksi tidak dipungut biaya apa pun.

*Cadangan:*
> Yth. [Bapak/Ibu nama], terima kasih telah melamar. Saat ini kami memprioritaskan beberapa kandidat lebih dulu; bila ada tahap lanjutan kami hubungi Anda lagi sebelum [isian: perkiraan waktu].

*Belum sesuai kebutuhan saat ini:*
> Yth. [Bapak/Ibu nama], terima kasih telah melamar dan menyiapkan CV. Untuk saat ini kami belum dapat melanjutkan ke tahap berikutnya karena kebutuhan posisi belum sesuai dengan profil Anda. Kami menghargai minat Anda dan mendoakan yang terbaik.

**Rekap untuk Anda:** 10 CV; rekonsiliasi bank dan laporan keuangan paling sering belum terlihat (3 dan 4 dari 10). C10 (Hendro) ditandai belum memenuhi syarat dasar karena pengalaman akuntansinya belum terlihat; bila Anda mau memastikan, satu pesan klarifikasi cukup sebelum dikesampingkan. Alamat, nomor HP, dan tanggal lahir tidak saya tulis; simpan CV hanya di komputer Anda dan hapus setelah proses selesai.

**Asumsi:** syarat 2 tahun dihitung dari rentang tahun di CV; jabatan "Bendahara paruh waktu" dihitung pengalaman keuangan.
Boleh saya tahu: (1) jadwal dan lokasi wawancara? (2) apakah Accurate wajib bisa sejak hari pertama atau boleh belajar? (3) kisaran gaji untuk pertanyaan ekspektasi?
