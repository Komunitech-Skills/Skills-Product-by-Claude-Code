# Contoh 3: jasa servis AC, 4 chat WhatsApp

> Contoh rancangan pembuat dengan data fiktif; bukan hasil uji platform.

## Masukan pengguna
"Saya punya usaha servis AC, ini chat komplain minggu ini. Tolong urutkan dan buatkan balasannya.
A: 'Pak, teknisi kemarin bilang freon habis dan sudah isi Rp350 ribu, tapi hari ini AC dingin lagi tidak. Tolong datang lagi, kalau tidak saya minta uang kembali.'
B: 'Teknisinya datang telat 3 jam tanpa kabar, saya sudah izin kerja. Pelayanan buruk!'
C: 'Setelah diservis, ada bocor air dari AC ke lantai dan merusak lemari kayu saya. Saya minta ganti rugi dan kalau tidak saya laporkan ke BPSK.'
D: 'Pak, servis AC cuci biasa berapa? Bisa Sabtu?'"

## Keluaran di chat

**Ringkasan:** 4 chat: 1 P1, 2 P2, 1 pertanyaan biasa. 1 perlu keputusan Anda (C).

| Urut. | Chat | Prioritas dan alasan |
|---|---|---|
| 1 | C air bocor merusak lemari, minta ganti rugi | P1: ancam lapor BPSK, kerugian benda, nilai belum diketahui |
| 2 | A AC kembali tidak dingin setelah isi freon | P2: hasil kerja bermasalah, ada permintaan uang kembali (Rp350.000) |
| 3 | B teknisi telat 3 jam | P2: komplain layanan, pelanggan sudah izin kerja |
| 4 | D tanya harga cuci AC | P3: bukan keluhan |

**Draf balasan**

**C**
> Selamat siang Pak/Bu, mohon maaf atas kejadian di rumah Bapak/Ibu, kami paham itu merugikan. Kami ingin menangani ini dengan serius. Boleh kirim foto kebocoran dan lemari yang rusak? Pemilik kami akan menghubungi Bapak/Ibu hari ini [isian: jam] untuk membahas langkah berikutnya.

Catatan: **[KEPUTUSAN PEMILIK]**. Jangan menyetujui atau menolak ganti rugi di chat, dan jangan menyalahkan kondisi rumah pelanggan. Minta teknisi menulis kronologi pengerjaan (pipa buangan, kemiringan unit) dan simpan foto/nota. Bila pelanggan membawa ke BPSK, siapkan catatan itu dan minta bantuan ahli hukum; ini bukan nasihat hukum.

**A**
> Selamat siang Pak/Bu, mohon maaf AC-nya kembali kurang dingin setelah servis kemarin. Kami jadwalkan teknisi datang memeriksa kembali pada [isian: hari/jam]. Bisa dikonfirmasi waktunya? Soal biaya pengisian, kami bahas setelah teknisi mengecek penyebabnya.

Catatan: refund Rp350.000 **[KEPUTUSAN PEMILIK]**, sesuai `[isian: garansi servis toko]`. Jangan menyalahkan pelanggan atau teknisi.

**B**
> Selamat siang Pak/Bu, mohon maaf teknisi kami datang terlambat tanpa kabar, padahal Bapak/Ibu sudah mengatur waktu. Itu salah kami. Kami bahas dengan tim agar kabar keterlambatan selalu disampaikan lebih dulu. Untuk kunjungan berikutnya, kami [isian: bentuk kompensasi, bila diputuskan pemilik].

Catatan: kompensasi **[KEPUTUSAN PEMILIK]**; bila belum diputuskan, hapus kalimat terakhir.

**D**
> Selamat siang Pak/Bu, untuk cuci AC [isian: harga per unit, ukuran PK]. Hari Sabtu [isian: jam kosong]. Boleh kirim alamat dan jumlah unitnya?

**Perlu keputusan Anda**
1. C: ganti rugi lemari kayu dan siapa yang menghubungi pelanggan; sebaiknya hari ini karena sudah menyebut BPSK.
2. A: refund biaya freon atau garansi servis ulang tanpa biaya.
3. B: bentuk kompensasi atas keterlambatan teknisi (atau cukup minta maaf).

**Pola:** belum ada (tiap keluhan beda penyebab). Perlu dicatat: keterlambatan teknisi tanpa kabar bisa terulang; usulan aturan "kabari pelanggan bila telat lebih dari 30 menit".

**Asumsi:** semua chat masuk hari ini; garansi servis dan nilai kerugian pada C belum diketahui.
Boleh saya tahu: (1) usaha memberi garansi servis berapa hari? (2) harga cuci AC dan jam kosong hari Sabtu? (3) kerugian pada C kira-kira berapa?
