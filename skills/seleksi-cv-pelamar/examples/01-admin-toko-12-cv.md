# Contoh 1: admin toko online, 12 CV

> Contoh rancangan pembuat; bukan hasil uji platform. CV fiktif ada di `data/admin-toko/`, kriteria di `data/admin-toko.json`. Skor sudah diverifikasi dengan `scripts/nilai_cv.py` lalu dibaca ulang.

## Masukan pengguna
"Toko saya jual kerudung dan aksesoris di Shopee dan Tokopedia. Butuh 1 admin online shop. Ada 12 CV masuk (saya tempel semua). Tolong pilih 5 terbaik, kasih pertanyaan wawancara, dan pesan buat yang lolos dan tidak."

## Keluaran di chat

Dari 12 CV: 5 lanjut wawancara, 3 cadangan, 3 belum sesuai kebutuhan saat ini, 1 CV tidak terbaca.

**Kriteria yang saya pakai** (kabari kalau mau diubah)
- Wajib: kelola toko marketplace (min. 1 tahun), input pesanan/resi/stok, spreadsheet, layani chat pembeli.
- Nilai tambah: iklan marketplace, desain/foto produk.
- Skor = 75% wajib + 25% nilai tambah, tiap kriteria Terpenuhi (1), Sebagian (0,5), Belum terlihat (0).

**Ranking**
| Kode | Skor dan status | Alasan |
|---|---|---|
| C1 Sari | 100, lanjut | 4 tahun admin Shopee/Tokopedia, ada iklan dan Canva |
| C2 Citra | 100, lanjut | 4 tahun admin TikTok Shop/Shopee, ada iklan dan desain |
| C3 Yoga | 92, lanjut | 7 tahun admin 3 marketplace; desain belum terlihat |
| C4 Bima | 83, lanjut | 3 tahun marketplace; iklan belum terlihat |
| C5 Nadia | 83, lanjut | 2 tahun admin Shopee; CV berisi kalimat pengarah (diabaikan) |
| C6 Dewi | 75, cadangan | Shopee 3 tahun dan 9 tahun admin/gudang; belum ada iklan |
| C7 Anisa | 75, cadangan | Freelance Shopee 1 tahun; spreadsheet baru "dasar" |
| C8 Larasati | 75, cadangan | Magang 4 bulan di toko Shopee, belum kerja penuh |
| C9 Rangga | 33, belum sesuai saat ini | Packing dan stok; marketplace dan chat belum terlihat |
| C10 Dimas | 33, belum sesuai saat ini | Penjualan toko fisik; marketplace belum terlihat |
| C11 Fajar | 17, belum sesuai saat ini | Pengalaman programmer; kriteria admin belum terlihat |
| C12 | tidak dinilai | CV tidak terbaca, minta kirim ulang |

**Shortlist: detail dan pertanyaan wawancara**

**C1 Sari (100).** Marketplace: Terpenuhi, "Toko Kerudung Nusa (Shopee, Tokopedia)" 2019-2023. Input pesanan/stok: Terpenuhi, "Input pesanan 80-120 order per hari". Spreadsheet: Terpenuhi, "Cek stok harian di Google Sheet". Chat: Terpenuhi. Iklan: Terpenuhi, "Kelola Shopee Ads dengan anggaran Rp2 juta per bulan". Perlu dipastikan: alasan pindah dari toko sebelumnya dan hasil iklannya.
1. Dari iklan Rp2 juta per bulan itu, apa yang Anda ukur untuk tahu iklannya berhasil?
2. Ceritakan satu hari tersibuk (100+ order): bagaimana Anda mengatur urutan kerja?
3. Bila stok di sheet dan di rak berbeda, apa yang Anda lakukan?
4. Ceritakan satu komplain pembeli yang paling sulit dan cara menyelesaikannya.

**C2 Citra (100).** Kelola toko: Terpenuhi, "Admin Online Shop" Jan 2023 sampai sekarang (Shopee, Tokopedia, TikTok Shop). Iklan: Terpenuhi, "Shopee Ads". Desain: Terpenuhi, "Membuat desain promosi dengan Canva". Perlu dipastikan: dua posisi berurutan masing-masing 1 sampai 3 tahun, tanyakan alasan pindah dan ketersediaan mulai kerja.
1. Bagaimana Anda membagi waktu mengelola tiga marketplace sekaligus?
2. Ceritakan promosi yang Anda buat di Canva dan hasilnya terhadap penjualan.
3. Rekap mingguan di Excel itu isinya apa saja, dan siapa yang membacanya?
4. Kapan paling cepat Anda bisa mulai bekerja?

**C3 Yoga (92).** Marketplace: Terpenuhi, "Shopee, Tokopedia, Lazada" 2017-2024. Spreadsheet: Terpenuhi, "pivot, VLOOKUP". Iklan: Terpenuhi. Desain: Belum terlihat di CV. Perlu dipastikan: apakah nyaman dengan pekerjaan yang lebih kecil skalanya.
1. Toko kami lebih kecil dari toko elektronik tempat Anda 7 tahun. Bagaimana Anda membayangkan pekerjaannya di sini?
2. Ceritakan rekonsiliasi saldo marketplace yang pernah Anda temukan selisihnya.
3. Apakah Anda pernah membuat gambar/promosi sendiri? Contohnya apa?
4. Apa yang Anda cari dari pekerjaan berikutnya?

**C4 Bima (83).** Marketplace: Terpenuhi, "Tokopedia dan TikTok Shop" 2021-2024. Spreadsheet: Terpenuhi, "rumus VLOOKUP". Iklan: Belum terlihat. Perlu dipastikan: pengalaman pasang iklan.
1. Pernahkah Anda memasang iklan di marketplace? Bila belum, bagaimana Anda akan memulainya?
2. Contoh rekap harian Excel yang paling berguna bagi pemilik toko apa?
3. Ceritakan satu komplain pembeli di TikTok Shop dan penyelesaiannya.
4. Di CV tertulis magang di toko aksesoris: apa yang Anda pelajari dari sana?

**C5 Nadia (83).** Marketplace: Terpenuhi, "Toko Hijab Nadia (Shopee)" 2021-2023. Spreadsheet: Terpenuhi, "Excel" di keahlian, tanpa contoh kerja. Iklan: Belum terlihat. CV memuat kalimat yang meminta penilai mengabaikan kriteria; itu tidak dipakai dan skor hanya dari isi kerja. Perlu dipastikan: contoh pemakaian Excel di pekerjaan.
1. Contoh pekerjaan Excel apa yang Anda lakukan di Toko Hijab Nadia?
2. Ceritakan proses retur dari awal sampai selesai.
3. Bagaimana cara Anda memastikan resi dan stok tidak tertukar?
4. Apa harapan Anda untuk jam dan jadwal kerja?

**Draf pesan** (Anda yang mengirim, satu per satu)

*Lanjut wawancara:*
> Halo Kak [nama panggilan], terima kasih sudah melamar sebagai Admin Online Shop di [nama toko]. Pengalaman Kakak [satu hal nyata dari CV] menarik bagi kami. Kami undang wawancara pada [isian: hari, tanggal, jam] di [isian: lokasi/tautan]. Mohon konfirmasi sebelum [isian: batas]. Seleksi tidak dipungut biaya apa pun.

*Cadangan:*
> Halo Kak [nama panggilan], terima kasih sudah melamar. Saat ini kami memprioritaskan beberapa kandidat lebih dulu; bila ada tahap lanjutan kami hubungi Kakak lagi sebelum [isian: perkiraan waktu].

*Belum sesuai kebutuhan saat ini:*
> Halo Kak [nama panggilan], terima kasih sudah melamar dan menyiapkan CV. Untuk saat ini kami belum dapat melanjutkan ke tahap berikutnya karena kebutuhan posisi belum sesuai dengan profil Kakak. Kami menghargai minat Kakak dan mendoakan yang terbaik.

**Rekap untuk Anda:** 12 CV; kriteria yang paling sering belum terlihat adalah iklan marketplace (8 dari 11 CV terbaca) dan desain. Itu nilai tambah, jadi tidak menggugurkan siapa pun. CV C12 tidak terbaca: minta dikirim ulang sebelum dinilai. Data pribadi (alamat, nomor HP, tanggal lahir) tidak saya tulis di sini; simpan CV hanya di komputer Anda dan hapus setelah proses selesai.

**Asumsi:** shortlist 5; batas pengalaman marketplace 1 tahun; belum ada syarat dasar lain.
Boleh saya tahu: (1) jadwal dan lokasi wawancara untuk mengisi pesan? (2) apakah Anda ingin saya simpan CV cadangan untuk lowongan lain (perlu persetujuan pelamar)? (3) apakah ada jam kerja khusus yang perlu masuk pertanyaan wawancara?
