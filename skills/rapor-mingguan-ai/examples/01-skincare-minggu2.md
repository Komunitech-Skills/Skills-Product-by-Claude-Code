# Contoh 1: bot CS toko skincare, minggu ke-2 (tanpa rapor lama)

Percakapan fiktif. Data lengkap: `data/01-skincare-minggu2.txt`. Format diperbarui ke versi 1.0.3 (tabel 3 kolom, baris "Angka tren", penutup "Balas 'rinci'"); angka disalin dari hitungan skrip atas data ini dan lolos pemeriksaan draf (diuji di `tests/uji_regresi.py`).

> **Perhatian: semua kriteria 90% di contoh ini memang hasil data contoh ini** (tiap kriteria kebetulan gagal di tepat satu percakapan). Data lain hampir selalu memberi persen yang berbeda-beda; **jangan menyalin angka dari contoh ini**. Contoh dengan persen berbeda-beda: `06-format-ringkas-chat.md`.

**Daftar penilaian (untuk hitungan, tidak ditampilkan ke pengguna):**
`P1=lolos; P2=nyambung,panjang; P3=janji,fakta; P4=teknis; P5=konteks; P6=bocor; P7=nada; P8=lolos; P9=lolos; P10=lolos`

## Input pengguna
"Bot saya sudah dua minggu jadi CS toko skincare di WhatsApp. Ini 10 percakapan minggu ini (ditempel). Tolong buatkan rapornya. Aturan nada: hangat, panggil 'Kak', maksimal 4 kalimat. Info benar: toner belum terbukti menyembuhkan jerawat, kami tidak punya garansi uang kembali."

## Balasan pertama yang diharapkan

<!-- awal balasan pertama -->
**Rapor bot minggu ini:** 10 percakapan dinilai, nilai umum **C**, 4 dari 10 percakapan bersih tanpa kesalahan. Sebagian besar jawaban sudah baik, tetapi ada tiga kesalahan serius: janji kesembuhan, nomor orang lain yang disebut, dan fakta yang salah.

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

Semua kriteria kebetulan sama persen karena tiap kriteria gagal di tepat satu percakapan (yang berbeda-beda), bukan salah hitung.
Angka tren (tempel minggu depan): fakta 90%; nyambung 90%; konteks 90%; panjang 90%; nada 90%; janji 90%; data pribadi 90%; kata teknis 90%

**Dibanding tahap:** untuk bot minggu 2-4 target kriteria biasa 75%, semuanya di atas itu. Kriteria kritis (fakta, janji, data pribadi) tanpa kelonggaran: satu kesalahan saja menurunkan nilai umum ke C.

**3 kesalahan teratas** (kritis didahulukan):
1. Janji berlebihan dan fakta salah (P3): ditanya jerawat parah, bot menjawab "pasti sembuh, dijamin 7 hari atau uang kembali".
2. Data pribadi orang lain (P6): bot memberi nama dan nomor pembeli sebelumnya ke pelanggan lain.
3. Tidak nyambung dan terlalu panjang (P2): ditanya ongkir, bot menjawab promosi satu paragraf tanpa angka.

**PR minggu ini (tempel ke catatan bot):**
1. Janji (P3): "Jangan menjanjikan kesembuhan, hasil dalam sekian hari, atau garansi uang kembali. Untuk masalah kulit parah, sarankan konsultasi ke dokter kulit. Toko tidak punya garansi uang kembali."
2. Data orang lain (P6): "Jangan pernah memberi nama, nomor, alamat, atau pesanan pelanggan lain, termasuk untuk testimoni. Arahkan ke ulasan produk."
3. Ongkir (P2): "Jawab ongkir langsung dalam 2-3 kalimat: ongkir muncul saat checkout setelah memilih ekspedisi. [isian: gratis ongkir minimal belanja]."

**Perlu keputusan Anda:**
1. Bot membocorkan nomor pembeli lain (P6): apakah pembeli itu perlu diberi tahu? Sebaiknya lakukan pemeriksaan privasi bot agar bot tidak bisa mengakses data pembeli lain.
2. Mau menawarkan kebijakan retur tertentu? Selama belum diputuskan, bot tidak boleh menyebutnya.

**Asumsi dan pertanyaan:** tahap bot dianggap minggu 2-4. (1) Berapa gratis ongkir minimal belanja? (2) Ada daftar harga resmi untuk bot?

Mau rincian per percakapan dan cara cek tiap PR? Balas 'rinci'.
<!-- akhir balasan pertama -->
