# Contoh 2: kafe, 5 ulasan Google Maps / GoFood / GrabFood

> Contoh rancangan pembuat dengan data fiktif; bukan hasil uji platform. Data mentah: `data/02-kafe-ulasan.csv`.

## Masukan pengguna
"Kafe saya dapat 5 ulasan baru. Mana yang harus ditangani dulu dan balasannya apa? Saya pemilik, admin cuma satu orang."
(1) Google, bintang 1: pesan lewat GoFood, es kopi tumpah separuh, nasi goreng dingin banget, tidak akan pesan lagi. (2) GoFood, bintang 2, Rp78.000: menunggu hampir 1 jam padahal estimasi 25 menit. (3) Google, bintang 1: "habis makan di sini perut saya sakit dan muntah malam harinya, ayam kayaknya kurang matang, saya akan laporkan ke dinas kesehatan". (4) Google, bintang 5, pujian. (5) GrabFood, bintang 3, Rp45.000: porsi lebih kecil dari foto, tapi rasanya enak.

## Keluaran di chat

**Ringkasan:** 5 ulasan: 1 P1 (kesehatan dan ancaman lapor), 2 P2, 1 P3, 1 pujian. 1 perlu keputusan Anda (K3).

| Urut. | Ulasan | Prioritas dan alasan |
|---|---|---|
| 1 | K3 sakit perut setelah makan | P1: keamanan pangan, ancam lapor, ulasan publik |
| 2 | K2 pesanan terlambat 1 jam | P2: ulasan publik bintang 2 |
| 3 | K1 minuman tumpah, makanan dingin | P2: ulasan publik bintang 1, kemasan pengantaran |
| 4 | K5 porsi lebih kecil dari foto | P3: bintang 3, ada saran |
| 5 | K4 pujian | P3: bukan keluhan, cukup dibalas terima kasih |

**Draf balasan** (balasan publik singkat; tanpa nama atau data pesanan):

**K3 (Google Maps)**
> Terima kasih sudah memberi tahu kami, Kak. Kami prihatin mendengar Kakak sakit. Keselamatan pelanggan penting bagi kami dan kami ingin memeriksanya. Boleh hubungi kami lewat [isian: WA/telepon kafe] agar kami bisa mencatat kejadiannya? Semoga Kakak lekas pulih.

Pesan pribadi untuk pemilik (bukan untuk dikirim ke pelanggan): ini kasus **[KEPUTUSAN PEMILIK]**. Cek bahan dan cara masak ayam hari itu, catat suhu dan penyimpanan, dan jangan menyimpulkan penyebabnya di balasan. Tidak memberi saran obat. Kalau pelanggan menghubungi, pemilik yang menjawab.

**K2 (GoFood)**
> Terima kasih masukannya, Kak. Mohon maaf pesanannya datang lebih lama dari estimasi. Kami cek alur dapur dan pengantaran pada jam itu supaya tidak terulang. Kami senang bila Kakak mau memberi kami kesempatan lagi.

**K1 (Google Maps)**
> Mohon maaf pesanan Kakak sampai dalam kondisi tumpah dan sudah dingin. Itu bukan standar kami. Kami perbaiki cara kemasan minuman dan makanan untuk pesan antar. Bila berkenan, hubungi kami lewat [isian: kanal] agar kami bisa membantu.

**K5 (GrabFood)**
> Terima kasih sudah menyukai rasanya, Kak, dan terima kasih atas masukan soal porsi. Kami cek lagi foto menu supaya sesuai dengan yang diterima pelanggan.

**K4 (Google Maps)**
> Terima kasih banyak, Kak! Senang Kakak nyaman. Sampai jumpa lagi.

**Perlu keputusan Anda**
1. K3, dugaan keracunan makanan, bintang 1 publik: siapa yang menghubungi pelanggan dan apakah ada pemeriksaan dapur hari ini? Batas: hari ini.

**Pola:** K1 dan K2 sama-sama soal pesan antar (kemasan dan waktu). Bila ada satu lagi minggu ini, periksa kemasan antar dan jam sibuk dapur.

**Asumsi:** ulasan ditampilkan publik; tidak ada data nomor pesanan sehingga tidak bisa mencocokkan ke kasir.
Boleh saya tahu: (1) kafe punya kanal chat/WA yang boleh disebut di balasan publik? (2) pesan antar memakai kemasan khusus atau kemasan biasa? (3) siapa yang menghubungi pelanggan untuk kasus K3?
