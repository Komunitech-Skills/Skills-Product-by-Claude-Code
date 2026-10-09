# Bank Pesan per Situasi (kerangka, bukan untuk disalin mentah)

Dipakai agent sebagai titik awal. Sesuaikan nama, produk, nada, dan hanya isi fakta yang diberikan pengguna. Data yang belum ada tetap `[isian]`. Setiap pesan WA di bawah 90 kata. Akhiran opt-out (pilih satu, ganti per kanal):
- **WA/Telegram:** `Kalau tidak ingin dapat pesan seperti ini lagi, balas "stop" ya.`
- **Email:** baris kaki `Tidak ingin menerima email ini lagi? [tautan berhenti berlangganan]`

Sapaan: `Kak [nama]` (netral), `Bu/Pak [nama]` bila usia/hubungan jelas. Tanda tangan: `[nama Anda], [nama usaha]`.

## 1. sambutan (pelanggan baru: hari 0, 3, 10, 21)
**Tujuan:** pembeli merasa aman, tahu langkah berikut, dan mudah bertanya.
- **P1 (hari 0):** "Halo Kak [nama], terima kasih sudah pesan [produk] di [nama usaha]. Pesanan Kakak [status: diproses/akan dikirim `[tanggal]`]. Kalau ada yang mau diubah atau ditanyakan, balas saja chat ini. [nama Anda]. [opt-out]"
- **P2 (hari 3):** "Halo Kak [nama], semoga [produk] sudah sampai dengan baik. Satu tips dari kami: [tips cara pakai/simpan yang benar-benar berlaku]. Kalau ada kendala, kabari kami ya. [opt-out]"
- **P3 (hari 10):** "Halo Kak [nama], bagaimana [produk]-nya? Kalau ada yang kurang pas, ceritakan saja, kami senang dengar apa adanya. [opt-out]"
- **P4 (hari 21, hanya bila ada produk lain yang relevan):** "Halo Kak [nama], karena Kakak sudah coba [produk], kami ingin kabari ada [produk lain] yang sering dipilih bersamaan. Kalau tertarik, kami kirimkan info singkatnya. [opt-out]"
**Berhenti:** membalas, komplain, minta berhenti. P4 dilewati bila pelanggan baru saja komplain/retur.

## 2. edukasi (prospek yang sudah minta info: hari 0, 4, 10, 17, 24)
**Tujuan:** memberi manfaat nyata dulu; menjual terakhir dan lembut. Hanya untuk orang yang mendaftar/bertanya sendiri (opt-in), paling cocok lewat email (listmonk) atau saluran Telegram.
- **P1 (0):** "Terima kasih sudah tertarik dengan [topik]. Dalam beberapa minggu ke depan kami kirim [jumlah] pesan singkat tentang [manfaat yang dijanjikan]. Tidak ada kewajiban beli. [opt-out]"
- **P2 (4):** satu pengetahuan: "[Judul]: [3-4 kalimat inti + 1 langkah yang bisa dicoba hari ini]."
- **P3 (10):** "Kesalahan yang paling sering terjadi pada [topik]: [kesalahan] dan cara menghindarinya: [cara]."
- **P4 (17):** contoh nyata dari usaha Anda sendiri: "[kasus nyata yang pengguna ceritakan, tanpa angka karangan]."
- **P5 (24):** "Kalau Kakak ingin [hasil], kami bisa bantu lewat [produk/layanan]. Mau kami kirim [penawaran/katalog/jadwal konsultasi]? Balas 'mau' atau 'nanti dulu', keduanya tidak masalah. [opt-out]"
**Email:** tiap pesan perlu judul (maks. 50 karakter, 2 opsi, tanpa huruf besar semua dan tanpa janji hasil) dan satu ajakan. **Berhenti:** membeli, membalas, berhenti berlangganan.

## 3. keranjang (pesanan tertunda di toko sendiri: hari 0, 1, 3)
**Tujuan:** menawarkan bantuan, bukan menekan. **Hanya** untuk orang yang menghubungi/meninggalkan nomor di toko Anda sendiri (WA, Instagram, situs toko). Jangan menghubungi pembeli marketplace di luar fitur chat marketplace dan jangan mengajak transaksi keluar marketplace (melanggar aturan platform dan UU PDP).
- **P1 (hari 0, sekitar 2-3 jam sesudah): ** "Halo Kak [nama], tadi Kakak sempat lihat [produk] di [nama usaha]. Ada yang bisa kami bantu, misalnya soal ukuran, ongkir, atau cara bayar? [opt-out]"
- **P2 (hari 1):** "Halo Kak [nama], kami cek lagi pesanan [produk] Kakak. Kalau ada hal yang masih membuat ragu (harga, pengiriman, bahan), tanyakan saja, kami jawab apa adanya. Stok [produk] saat ini: [stok sebenarnya/tidak disebut]. [opt-out]"
- **P3 (hari 3):** "Halo Kak [nama], ini pesan terakhir dari kami soal [produk]. Kalau belum jadi, tidak apa-apa. Kalau nanti berminat, chat saja kapan pun. Terima kasih sudah mampir. [opt-out]"
**Diskon/ongkir gratis:** hanya bila pengguna menyebutnya, tulis syarat & tanggal berlaku `[isian]`. Tanpa "tinggal 1 stok" kecuali memang benar. **Berhenti:** pesanan dibayar, membalas, minta berhenti.

## 4. setelah-beli (onboarding produk: hari 0, 2, 7, 14)
**Tujuan:** pembeli bisa memakai produk dengan benar dan tahu ke mana bertanya. Cocok untuk produk yang perlu cara pakai (skincare, alat, kursus, jasa berkala).
- **P1 (0):** konfirmasi: "Pesanan [produk] Kakak sudah kami terima. Estimasi [dikirim/selesai]: [tanggal]. Nomor resi/bukti: [isian]. Pertanyaan apa pun, balas chat ini. [opt-out]"
- **P2 (2):** "Kalau [produk] sudah sampai, ini cara pakai singkat: 1) [langkah] 2) [langkah] 3) [langkah]. [Peringatan keamanan bila relevan]. Belum sampai? Kabari kami."
- **P3 (7):** "Bagaimana pengalaman sejauh ini dengan [produk]? Kalau ada yang kurang jelas, kami bantu."
- **P4 (14):** "Tips lanjutan: [perawatan/pemakaian lanjutan yang benar]. Kapan sebaiknya beli lagi/isi ulang: [perkiraan jujur atau 'tergantung pemakaian']. [opt-out]"
**Kategori sensitif** (kesehatan, keuangan): tanpa klaim khasiat dan tanpa data pribadi di chat. **Berhenti:** komplain/retur (alihkan ke `balas-chat-cs`).

## 5. ulasan (hari 1 sesudah diterima/selesai, pengingat hari 6)
**Tujuan:** ulasan jujur dari pembeli. Satu pengingat saja.
- **P1:** "Halo Kak [nama], terima kasih sudah memakai [produk/jasa] kami. Kalau ada waktu, kami berterima kasih sekali bila Kakak mau menulis pengalaman apa adanya di sini: [tautan ulasan]. Kalau ada yang kurang berkenan, kabari kami langsung supaya bisa kami perbaiki. [opt-out]"
- **P2 (hanya bila belum membalas):** "Halo Kak [nama], sekadar mengingatkan satu kali: ulasan Kakak di [tautan ulasan] sangat membantu pelanggan lain. Kalau tidak sempat, tidak apa-apa. Terima kasih. [opt-out]"
**Larangan:** meminta bintang 5, hadiah/diskon untuk ulasan positif, hanya mengirim ke yang puas (menyaring), menulis ulasan palsu. Banyak platform ulasan melarangnya; cek aturan platform yang dipakai. Pelanggan yang menyampaikan kendala: tangani dulu lewat `balas-chat-cs`, jangan kirim pengingat. **Berhenti:** ulasan sudah ada, membalas, komplain.

## 6. perpanjangan (acuan jatuh tempo: hari -14, -7, -2, +3)
**Tujuan:** pelanggan tidak kaget dan mudah memutuskan. Bukan untuk menjebak: sebut harga & cara berhenti dengan jelas.
- **P1 (-14):** "Halo Kak [nama], paket [nama paket] Kakak akan berakhir pada [tanggal]. Kalau mau lanjut, caranya: [cara]. Harga perpanjangan: [harga & masa berlaku yang benar]. [opt-out]"
- **P2 (-7):** "Sepekan lagi [nama paket] berakhir. Selama ini Kakak sudah [hal nyata yang tercatat di data usaha, bila ada]. Pilihan: lanjut, ganti paket, atau berhenti. Kabari kami mana yang cocok."
- **P3 (-2):** "Pengingat terakhir: [nama paket] berakhir [tanggal]. Untuk lanjut tanpa jeda, [cara/batas waktu bayar]. Kalau memilih berhenti, tidak masalah."
- **P4 (+3, hanya bila belum ada kabar):** "Paket [nama paket] Kakak sudah berakhir. Kalau masih butuh, kami bisa bantu aktifkan kembali kapan pun. Kalau tidak, terima kasih sudah bersama kami. [opt-out]"
**Larangan:** perpanjangan otomatis tanpa persetujuan jelas, menyembunyikan cara berhenti, biaya yang tidak disebut. **Berhenti:** sudah bayar/memutuskan, membalas.

## 7. reaktivasi
Jadwal 0, 10, 24 hari. **Isi pesan: pakai skill `aktifkan-kembali-pelanggan`** (segmentasi, hitungan, 3 pesan lengkap). Di sini hanya jadwal dan penghubungnya. Jangan menulis ulang pesannya.

## 8. peluncuran (acuan hari peluncuran: -3, 0, 3, 7)
**Tujuan:** pelanggan/pengikut yang sudah opt-in tahu produk baru dengan jelas. Hanya fakta yang pengguna berikan.
- **P1 (-3):** "Kabar baik dari [nama usaha]: [produk baru] akan hadir pada [tanggal]. [Satu kalimat apa itu & untuk siapa]. Kami kabari lagi saat sudah bisa dipesan. [opt-out]"
- **P2 (0):** "[Produk baru] sudah tersedia. [Apa itu, harga, cara pesan, estimasi kirim]. Pertanyaan? Balas chat ini."
- **P3 (+3):** "Contoh pemakaian [produk baru]: [kasus nyata/foto/cara pakai]." (tanpa testimoni karangan; testimoni hanya yang asli dan seizin pemberi)
- **P4 (+7):** "Pengingat: [produk baru] masih bisa dipesan di [cara]. [Tenggat/stok HANYA bila benar-benar ada]. [opt-out]"
**Berhenti:** membeli (lewati sisa pesan), membalas, minta berhenti.

## Pengingat untuk pemilik (tiap situasi)
Catat di lembar sederhana: nama panggilan, pesan ke berapa, tanggal, status (belum/terkirim/membalas/berhenti). Jangan menyimpan lebih dari yang perlu.
