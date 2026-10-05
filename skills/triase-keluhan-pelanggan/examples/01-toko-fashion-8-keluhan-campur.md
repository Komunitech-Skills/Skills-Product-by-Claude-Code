# Contoh 1: toko fashion, 8 keluhan campur (Shopee, TikTok Shop, Tokopedia, WA, Instagram)

> Contoh rancangan pembuat dengan data fiktif; bukan hasil uji platform. Data mentah: `data/01-toko-fashion.csv`. Bagian "Keluaran di chat" adalah tampilan yang diharapkan pembeli.

## Masukan pengguna
"Ini keluhan yang masuk sejak kemarin dari berbagai tempat, 8 biji. Mana yang harus saya balas dulu? Tolong siapkan balasannya. Toko saya jual baju wanita, rata-rata pesanan Rp150-300 ribu." Lalu menempel 8 keluhan (ringkasnya):
K1 Shopee, blouse linen sobek di ketiak, jahitan lepas, mau ganti atau uang kembali (Rp189.000). K2 Shopee, paket sudah seminggu belum sampai, resi tidak bergerak 3 hari, sudah chat dua kali tanpa kabar, "kalau besok belum jelas saya laporkan ke Shopee dan kasih bintang 1" (Rp325.000). K3 TikTok Shop, pesan kulot ukuran L datang M, bisa tukar? (Rp129.000). K4 ulasan Tokopedia bintang 2, kaos tipis dan tidak sesuai foto (Rp98.000). K5 WA, paket COD ditolak kurir karena tidak di rumah, kini kembali ke penjual, minta dikirim ulang hari ini (Rp875.000, set gamis). K6 Shopee, tanya ready XL kaos putih dan ongkir ke Medan. K7 Instagram, admin slow respon, chat dari kemarin tidak dibalas (Rp159.000). K8 ulasan Shopee bintang 1, blouse sobek, "penjual penipu", minta refund (Rp189.000).

## Keluaran di chat

**Ringkasan:** 8 masuk: 3 P1, 4 P2, 1 pertanyaan biasa (bukan keluhan). 3 perlu keputusan Anda (K5, K2, K8).

| Urut. | Keluhan | Prioritas dan alasan |
|---|---|---|
| 1 | K5 COD ditolak, set gamis | P1: nilai Rp875.000 di atas batas Rp500.000, paket sudah kembali ke toko |
| 2 | K2 belum sampai (Shopee) | P1: ancam lapor dan bintang 1, sudah menunggu 3 hari, mengulang keluhan |
| 3 | K8 blouse sobek, ulasan bintang 1 | P1: tuduhan penipuan di ulasan publik |
| 4 | K1 blouse sobek (Shopee) | P2: perlu bukti foto/video, belum ada ancaman |
| 5 | K7 admin lambat (Instagram) | P2: menunggu sejak kemarin, mengulang |
| 6 | K3 salah ukuran (TikTok Shop) | P2: tukar ukuran, tidak mendesak |
| 7 | K4 kaos tipis (ulasan bintang 2) | P2: ulasan publik |
| 8 | K6 tanya stok dan ongkir | P3: bukan keluhan |

**Draf balasan** (kirim satu per satu lewat kanal masing-masing):

**K5 (WA)**
> Halo Kak, mohon maaf paket set gamisnya belum berhasil diterima. Kakak masih mau kami kirim ulang? Kalau iya, kabari alamat dan jam yang bisa menerima ya, Kak. Kami atur pengirimannya [isian: jadwal kirim ulang; ongkir kirim ulang ditanggung siapa].

Catatan: kirim ulang "hari ini" belum bisa dijanjikan karena paket baru kembali; ongkir **[KEPUTUSAN PEMILIK]**.

**K2 (Shopee)**
> Halo Kak, mohon maaf paketnya belum sampai dan kabarnya terlambat dari kami. Itu pasti bikin cemas. Hari ini kami hubungi ekspedisi dan kabari Kakak lagi sebelum [isian: jam, mis. 16.00]. Boleh kirim tangkapan layar status resinya, Kak?

Catatan: kirim ulang atau refund **[KEPUTUSAN PEMILIK]**. Bila status resi menunjukkan paket hilang, buka klaim ke ekspedisi lewat Shopee. Jangan membalas soal bintang 1.

**K8 (balasan publik di ulasan)**
> Mohon maaf atas pengalaman Kakak, kami ingin menyelesaikannya. Boleh hubungi kami lewat chat toko dengan nomor pesanannya, Kak? Kami tangani segera.

Catatan: tanpa nama atau detail pesanan. Sambil itu hubungi pembeli lewat chat Shopee dengan balasan seperti K1. Refund **[KEPUTUSAN PEMILIK]**. Jangan meminta ulasan dihapus atau diganti.

**K1 (Shopee)**
> Halo Kak, mohon maaf blousenya datang sobek dan jahitannya lepas, pasti mengecewakan. Boleh kirim foto/video bagian yang rusak dan kemasannya (kalau ada video buka paket, mohon dilampirkan)? Setelah kami cek, kami kabari solusinya sebelum [isian: hari/jam].

Catatan: ganti atau refund **[KEPUTUSAN PEMILIK]** sesuai `[isian: kebijakan toko]`. K1 dan K8 sama-sama blouse linen sobek: lihat Pola.

**K7 (Instagram)**
> Halo Kak, mohon maaf chat Kakak terlambat kami balas, itu salah kami. Pesanan Kakak kami cek sekarang dan kabari statusnya sebelum [isian: jam]. Terima kasih sudah sabar ya, Kak.

**K3 (TikTok Shop)**
> Halo Kak, mohon maaf ukurannya keliru. Kami bantu tukar ke ukuran L. Boleh kirim foto label ukuran di kulotnya? Untuk proses tukar, kami arahkan langkahnya [isian: lewat fitur retur TikTok Shop atau kebijakan tukar toko].

**K4 (balasan publik di ulasan Tokopedia)**
> Terima kasih masukannya, Kak. Mohon maaf bahannya kurang sesuai harapan. Boleh hubungi kami lewat chat toko dengan nomor pesanannya? Kami bantu carikan solusinya.

**K6 (Shopee)**
> Halo Kak, kaos polos putih ukuran XL [isian: ready/habis]. Ongkir ke Medan [isian: lihat estimasi di keranjang, tergantung ekspedisi]. Ada yang bisa kami bantu lagi?

**Perlu keputusan Anda**
1. K5, gamis Rp875.000: kirim ulang (ongkir ditanggung siapa) atau batal? Batas: sebelum paket berangkat lagi.
2. K2, belum sampai: bila ekspedisi mengonfirmasi hilang, kirim ulang atau refund? Batas: hari ini (ancaman lapor ke Shopee).
3. K8, blouse sobek dan tuduhan di ulasan publik: ganti atau refund; siapa yang menghubungi pembeli? Batas: hari ini.

**Pola:** 2 keluhan blouse linen yang sobek di bagian jahitan (K1 dan K8). Belum 3, tapi satu lagi berarti masalah batch. Langkah: periksa stok blouse yang sama sebelum dikirim ke pembeli berikutnya.

**Asumsi:** batas "nilai besar" Rp500.000; semua keluhan masuk dalam 1-3 hari terakhir; kebijakan retur toko belum diketahui.
Boleh saya tahu: (1) kebijakan toko untuk barang rusak dan salah ukuran (ganti, refund, atau keduanya)? (2) jam kerja admin untuk menentukan janji waktu? (3) ongkir kirim ulang COD ditanggung siapa?

## Catatan penguji
- Prioritas P1/P2/P3 sesuai pra-pilah data (3/4/1), diverifikasi dengan membaca ulang pesan.
- Nomor HP di K5 tidak diulang di draf maupun rekap.
