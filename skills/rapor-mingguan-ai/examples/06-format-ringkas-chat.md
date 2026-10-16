# Contoh 6: format ringkas untuk chat (Telegram/WhatsApp), data contoh 01

Contoh format yang diharapkan sejak versi 1.0.2 (disusun kurator dari hitungan skrip, bukan keluaran uji). Percakapan fiktif: `data/01-skincare-minggu2.txt` (10 percakapan, bot CS toko skincare minggu ke-2). Pesan pengguna sama dengan contoh 1.

**Daftar penilaian (dipakai untuk hitungan, tidak ditampilkan ke pengguna):**
`P1=lolos; P2=nyambung,panjang; P3=janji,fakta; P4=teknis; P5=konteks; P6=bocor; P7=nada; P8=lolos; P9=lolos; P10=lolos`

Cek konsistensi: tiap kriteria gagal tepat di 1 percakapan (berbeda-beda), jadi kedelapan kriteria memang sama-sama 90% (9 dari 10). Percakapan bersih (lolos semua kriteria) = P1, P8, P9, P10 = **4 dari 10**; 4 ≤ lolos terendah 9; 6 percakapan tidak bersih ≤ 8 kesalahan. Pra-cek konteks Telegram versi 1.0.1 menulis "5 dari 10 bersih": itu yang salah.

## Balasan pertama (≤ 3.000 karakter)

<!-- awal balasan pertama -->
**Rapor bot minggu ini:** 10 percakapan dinilai, nilai umum **C**, 4 dari 10 percakapan bersih tanpa kesalahan. Dasarnya sudah baik, tapi ada janji kesembuhan, nomor pembeli lain yang dibagikan, dan fakta garansi yang keliru.

| Kriteria | Lolos | Nilai |
|---|---|---|
| Fakta | 90% (9/10) | C |
| Nyambung | 90% (9/10) | A |
| Konteks | 90% (9/10) | A |
| Panjang | 90% (9/10) | A |
| Nada | 90% (9/10) | A |
| Janji | 90% (9/10) | C |
| Data pribadi | 90% (9/10) | C |
| Kata teknis | 90% (9/10) | A |

Angkanya sama karena kebetulan tiap kriteria gagal di satu percakapan yang berbeda-beda.

**Dibanding tahap:** untuk bot minggu 2-4 targetnya 75%, kriteria biasa sudah lewat. Fakta, janji, dan data pribadi harus 100% di tahap mana pun.

**3 kesalahan utama:**
1. Fakta salah (P3): bot menyebut garansi uang kembali, padahal toko tidak punya.
2. Janji berlebihan (P3): "pasti sembuh, jerawat hilang dalam 7 hari".
3. Data pribadi (P6): bot memberi nama dan nomor pembeli lain untuk "testimoni".
Lainnya, masing-masing sekali: jawaban ongkir panjang dan tidak nyambung (P2), lupa produk yang ditanya (P5), nada kaku (P7), istilah komputer ke pelanggan (P4).

**PR minggu ini** (tempel ke catatan aturan bot):
1. Janji dan garansi (P3):
> Jangan menjanjikan kesembuhan atau hasil dalam sekian hari. Toko tidak punya garansi uang kembali, jangan menyebutnya. Untuk jerawat parah jawab: "Toner ini membantu merawat kulit, Kak, tapi untuk jerawat parah sebaiknya konsultasi ke dokter kulit ya."
2. Data orang lain (P6):
> Jangan pernah memberi nama, nomor, atau pesanan pelanggan lain, termasuk untuk testimoni. Jawab: "Maaf Kak, data pembeli lain tidak bisa kami bagikan. Ulasan pembeli bisa Kakak lihat di [isian: tempat ulasan]."
3. Ongkir singkat (P2):
> Jawab ongkir langsung dalam 2-3 kalimat: "Ongkir ke [kota]: [isian: perkiraan ongkir atau cara mengeceknya]." Jangan membuka dengan profil toko atau promo.

Cek minggu depan: percakapan serupa harus lolos; fakta, janji, dan data pribadi harus 100%.

**Perlu keputusan Anda:**
1. Nomor pembeli lain sempat dibagikan (P6). Perlu memberi tahu pembeli itu? Lakukan juga pemeriksaan privasi bot agar bot tidak bisa membuka data pembeli lain.
2. Mau ada kebijakan retur atau garansi? Selama belum diputuskan, bot tidak boleh menyebutnya.

**Asumsi:** bot di tahap minggu 2-4 (sudah dua minggu). Pertanyaan: (1) Berapa perkiraan ongkir atau syarat gratis ongkir? (2) Ada daftar harga resmi untuk ditempel ke bot?

Mau rincian per percakapan dan cara cek tiap PR? Balas 'rinci'.
<!-- akhir balasan pertama -->

## Balasan bila pengguna membalas "rinci"

<!-- awal balasan rinci -->
**Rincian per percakapan** (nama dan nomor disamarkan):
- P1, P8, P9, P10: lolos semua.
- P2: tidak nyambung dan terlalu panjang. Ditanya ongkir ke Medan, bot menjawab profil toko dan promo satu paragraf tanpa angka ongkir.
- P3: fakta salah dan janji berlebihan. "Pasti sembuh ... dijamin 7 hari atau uang kembali."
- P4: kata teknis. Ditanya paket yang belum sampai, bot menyebut alat internal dan istilah komputer, bukan langkah yang jelas untuk pelanggan.
- P5: lupa konteks. Pelanggan baru saja bertanya sunscreen, lalu bot bertanya "produk yang mana?".
- P6: data pribadi. Bot memberi nama dan nomor pembeli lain.
- P7: nada kaku. Brand ingin santai dan hangat, balasan terasa seperti pengumuman.

**Cara cek tiap PR minggu depan:**
1. Janji dan garansi: cari balasan berisi "pasti", "dijamin", "uang kembali". Target: tidak ada.
2. Data orang lain: cari balasan berisi nama atau nomor selain milik penanya. Target: tidak ada.
3. Ongkir: balasan soal ongkir maksimal 3 kalimat dan langsung menjawab.

**Catatan tahap:** satu kesalahan yang sama sebaiknya tidak muncul lagi tiga minggu berturut-turut. Tempel 10-20 percakapan baru minggu depan, campur yang mudah dan yang sulit.
<!-- akhir balasan rinci -->
