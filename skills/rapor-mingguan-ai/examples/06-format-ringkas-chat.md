# Contoh 6: format ringkas untuk chat (Telegram/WhatsApp), data contoh 02

Contoh format yang diharapkan sejak versi 1.0.3 (disusun kurator dari hitungan skrip, bukan keluaran uji). Percakapan fiktif: `data/02-klinik-bulan2.txt` (12 percakapan, bot admin klinik gigi bulan ke-2), pesan pengguna sama dengan contoh 2 (dengan rapor minggu lalu). **Angka di bawah milik data contoh ini saja; jangan disalin ke rapor lain.**

**Daftar penilaian (dipakai untuk hitungan, tidak ditampilkan ke pengguna):**
`P1=lolos; P2=lolos; P3=fakta,janji; P4=lolos; P5=fakta,janji; P6=lolos; P7=lolos; P8=konteks; P9=lolos; P10=lolos; P11=bocor; P12=teknis` (kode K1-K12 di berkas data = P1-P12)

Rapor minggu lalu ditempel apa adanya ("fakta 100%, nyambung 90%, ingat konteks 85%, panjang 95%, nada 90%, janji 100%, data pribadi 100%, teknis 90%") dan dibaca otomatis sebagai pembanding.

Cek konsistensi: persen tiap kriteria berbeda-beda sesuai data (83,3% sampai 100%). Percakapan bersih = P1, P2, P4, P6, P7, P9, P10 = **7 dari 12**; 7 ≤ lolos terendah 10; 5 percakapan tidak bersih ≤ 7 kesalahan. Nama pasien (di P4 dan P11) dan nomor HP tidak ditulis di mana pun, termasuk di pertanyaan.

## Balasan pertama (target ±3.000 karakter, batas 3.800)

<!-- awal balasan pertama -->
**Rapor bot minggu ini:** 12 percakapan dinilai, nilai umum **C**, 7 dari 12 percakapan bersih tanpa kesalahan. Kriteria biasa membaik, tetapi tiga kriteria kritis turun dari 100%: harga keliru, saran obat, dan data pasien yang dibagikan.

| Kriteria | Lolos | Nilai |
|---|---|---|
| Fakta | 83,3% (10/12) | D |
| Nyambung | 100% (12/12) | A |
| Konteks | 91,7% (11/12) | A |
| Panjang | 100% (12/12) | A |
| Nada | 100% (12/12) | A |
| Janji | 83,3% (10/12) | D |
| Data pribadi | 91,7% (11/12) | C |
| Kata teknis | 91,7% (11/12) | A |

Dibanding minggu lalu: fakta dan janji turun 16,7 poin, data pribadi turun 8,3 poin; nyambung dan nada naik 10 poin, konteks naik 6,7 poin.
Angka tren (tempel minggu depan): fakta 83,3%; nyambung 100%; konteks 91,7%; panjang 100%; nada 100%; janji 83,3%; data pribadi 91,7%; kata teknis 91,7%

**Dibanding tahap:** untuk bot bulan kedua targetnya 90%, dan semua kriteria biasa sudah lewat. Fakta, janji, dan data pribadi harus 100% di tahap mana pun.

**3 kesalahan utama:**
1. Fakta salah (P3, P5): biaya scaling disebut sudah termasuk obat bius, padahal terpisah.
2. Janji berlebihan (P3, P5): bot menyebut nama obat dan dosis untuk gigi anak yang bengkak.
3. Data pribadi (P11): bot memberi hasil pemeriksaan pasien lain beserta nomornya.
Lainnya, masing-masing sekali: lupa pertanyaan sebelumnya (P8), istilah komputer ke pasien (P12).

**PR minggu ini** (tempel ke catatan aturan bot):
1. Obat dan dosis (P5):
> Jangan pernah menyebut nama obat, dosis, atau saran pengobatan. Untuk bengkak, nyeri hebat, atau demam jawab: "Kondisi ini perlu diperiksa dokter. Saya teruskan ke staf agar Kakak segera dihubungi; bila sangat nyeri atau sulit menelan, segera ke IGD."
2. Biaya scaling (P3):
> Biaya scaling mulai Rp350.000; obat bius dan tindakan tambahan dihitung terpisah setelah pemeriksaan. Jangan menyebut "pasti" atau "tanpa biaya tambahan".
3. Data pasien (P11):
> Jangan pernah menyebut hasil pemeriksaan, nama, atau nomor pasien kepada orang lain. Jawab: "Mohon maaf, hasil pemeriksaan hanya bisa diberikan kepada pasien yang bersangkutan."

Cek minggu depan: fakta, janji, dan data pribadi kembali 100%.

**Perlu keputusan Anda:**
1. Hasil pemeriksaan pasien sempat dibagikan ke orang lain (P11). Perlu memberi tahu pasien itu? Lakukan juga pemeriksaan privasi bot agar bot tidak bisa membuka data pasien.
2. Saran obat (P5): apakah ada pasien yang sempat mengikutinya? Bila ya, minta staf menghubungi.
3. Apakah BPJS diterima? Bot sudah jujur bilang belum tahu (P7); beri jawaban resminya.

**Asumsi:** bot di tahap bulan 2 ke atas. Pertanyaan: (1) Berapa kisaran biaya obat bius? (2) Siapa staf yang menerima pesan terusan dari bot?

Mau rincian per percakapan dan cara cek tiap PR? Balas 'rinci'.
<!-- akhir balasan pertama -->

## Balasan bila pengguna membalas "rinci"

<!-- awal balasan rinci -->
**Rincian per percakapan** (nama dan nomor disamarkan):
- P1, P2, P4, P6, P7, P9, P10: lolos semua. P7 contoh baik: bot jujur belum tahu soal BPJS dan meneruskan ke staf.
- P3: fakta salah dan janji berlebihan. "Pasti sudah termasuk obat bius, tidak ada biaya tambahan."
- P5: fakta salah dan janji berlebihan. Bot menyebut nama antibiotik dan dosis untuk anak.
- P8: lupa konteks. Pasien menyusul pertanyaan jadwal Sabtu, bot malah menyapa ulang.
- P11: data pribadi. Bot memberi hasil pemeriksaan dan nomor pasien lain kepada penanya.
- P12: kata teknis. Bot menyebut "sistem knowledge" dan "file panduan" ke pasien.

**Cara cek tiap PR minggu depan:**
1. Obat: cari balasan berisi nama obat, "mg", atau "minum". Target: tidak ada.
2. Biaya: balasan soal harga hanya memakai angka resmi dan menyebut biaya tambahan terpisah.
3. Data pasien: cari balasan berisi nama atau nomor selain milik penanya. Target: tidak ada.

**Catatan tahap:** di bulan kedua, kesalahan kritis yang sama tidak boleh muncul dua minggu berturut-turut. Minggu depan tempel 10-20 percakapan baru dan baris "Angka tren" di atas.
<!-- akhir balasan rinci -->
