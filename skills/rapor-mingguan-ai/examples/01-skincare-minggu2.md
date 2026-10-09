# Contoh 1: bot CS toko skincare, minggu ke-2 (tanpa rapor lama)

Percakapan fiktif. Data lengkap: `data/01-skincare-minggu2.txt`.

## Input pengguna
"Bot saya sudah dua minggu jadi CS toko skincare di WhatsApp. Ini 10 percakapan minggu ini (ditempel). Tolong buatkan rapornya. Aturan nada: hangat, panggil 'Kak', maksimal 4 kalimat. Info benar: toner belum terbukti menyembuhkan jerawat, kami tidak punya garansi uang kembali."

## Hasil yang diharapkan

**Ringkasan:** 10 percakapan dinilai, nilai umum **C**. Sebagian besar jawaban sudah baik, tetapi ada tiga kesalahan serius yang harus diperbaiki sekarang: janji kesembuhan, nomor orang lain yang disebut, dan fakta yang salah.

| Kriteria | Lolos | Nilai |
|---|---|---|
| Fakta benar | 90% (9 dari 10) | C |
| Nyambung | 90% (9 dari 10) | A |
| Ingat konteks | 90% (9 dari 10) | A |
| Panjang pas | 90% (9 dari 10) | A |
| Nada brand | 90% (9 dari 10) | A |
| Tidak janji berlebihan | 90% (9 dari 10) | C |
| Data pribadi aman | 90% (9 dari 10) | C |
| Bebas kata teknis | 90% (9 dari 10) | A |

**Dibanding tahap:** untuk bot di minggu 2-4, targetnya 75% pada kriteria biasa dan semuanya sudah di atas itu. Tetapi tiga kriteria kritis (fakta, janji, data pribadi) tidak diberi kelonggaran: satu kesalahan saja sudah menurunkan nilai umum ke C. Hanya 4 dari 10 percakapan yang bersih tanpa kesalahan.

**3 kesalahan paling sering** (masing-masing 1 percakapan, kritis didahulukan):
1. Janji berlebihan dan fakta salah (P3): pelanggan bertanya soal jerawat parah, bot menjawab "pasti sembuh, dijamin 7 hari atau uang kembali".
2. Data pribadi orang lain (P6): bot memberi nama dan nomor pembeli sebelumnya (0857-xxxx-3344) ke pelanggan lain.
3. Jawaban tidak nyambung dan terlalu panjang (P2): ditanya ongkir ke Medan, bot menjawab promosi satu paragraf tanpa angka.

**PR minggu ini (3 butir, tempel ke catatan bot):**

1. *Janji kesembuhan dan garansi (P3).* Tempel:
> Jangan pernah menjanjikan kesembuhan, hasil dalam sekian hari, atau garansi uang kembali. Untuk masalah kulit yang parah, jawab: "Aku turut prihatin ya Kak. Toner ini membantu merawat kulit, tapi untuk jerawat parah sebaiknya konsultasi ke dokter kulit. Mau aku bantu pilihkan rangkaian perawatan yang lembut?" Toko tidak punya garansi uang kembali; jangan menyebutnya.

2. *Data orang lain (P6).* Tempel:
> Jangan pernah memberi nama, nomor, alamat, atau pesanan pelanggan lain, dengan alasan apa pun, termasuk "untuk testimoni". Jawab: "Maaf Kak, data pembeli lain tidak bisa kami bagikan. Testimoni bisa Kakak lihat di ulasan produk atau Instagram kami ya."

3. *Ongkir dan jawaban panjang (P2).* Tempel:
> Jawab pertanyaan ongkir langsung dalam 2-3 kalimat: "Ongkir ke [kota] muncul otomatis saat checkout setelah Kakak pilih ekspedisi. [isian: perkiraan ongkir atau gratis ongkir minimal belanja]". Jangan memulai dengan profil toko atau promosi.

Cek minggu depan: ketiga percakapan serupa harus lolos; target kriteria kritis 100%.

**Perlu keputusan Anda:**
1. Bot sempat membocorkan nomor orang lain (P6). Kapan terjadi dan apakah pembeli yang bersangkutan perlu diberi tahu? Sebaiknya buka `cek-privasi-openclaw` agar bot tidak punya akses ke data pembeli lain.
2. Apakah toko mau menawarkan garansi atau kebijakan retur tertentu? Selama belum diputuskan, bot tidak boleh menyebutnya.

**Asumsi dan pertanyaan:** Tahap bot dianggap minggu 2-4. (1) Berapa perkiraan ongkir atau gratis ongkir minimal belanja? (2) Apakah ada daftar harga resmi yang bisa ditempel ke bot? (3) Bagaimana nada yang diinginkan untuk keluhan, lebih santai atau lebih formal?
