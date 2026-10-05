# Cara kerja skor prioritas

## RICE (bila ada angka perkiraan)
`skor = jangkauan x dampak x (keyakinan/100) / usaha`
- **Jangkauan:** perkiraan berapa orang/pembeli tersentuh dalam satu periode (mis. 3 bulan). Contoh: pengikut yang bisa dijangkau, jumlah pesanan/bulan.
- **Dampak:** 0,25 (kecil sekali), 0,5 (kecil), 1 (sedang), 2 (besar), 3 (sangat besar) per orang.
- **Keyakinan:** persen (100 = ada data/uji; 80 = cukup yakin; 50 = tebakan; di bawah itu = hampir spekulasi).
- **Usaha:** total orang-hari kerja (riset, uji, produksi awal, desain, promosi).

## ICE (bila hanya punya perasaan)
`skor = dampak x keyakinan x kemudahan`, masing-masing 1-10 (kemudahan 10 = sangat mudah/murah).

## Cara membaca
Skor tinggi = layak lebih dulu. Skor hanya membandingkan **ide di daftar yang sama** dengan metode yang sama. Dua ide seri: yang usahanya lebih kecil didahulukan. Ide berskor tinggi tapi keyakinan rendah: uji kecil dulu.

## Format CSV
RICE: `nama,jangkauan,dampak,keyakinan,usaha`. ICE: `nama,dampak,keyakinan,kemudahan`. Pemisah `,` `;` atau tab. Desimal `0,5` atau `0.5`; ribuan `1.500` (titik + tepat 3 angka) dibaca 1500. Judul kolom Inggris (name, reach, impact, confidence, effort, ease) juga diterima; kolom wajib yang hilang disebut namanya.
- `10,000` (satu koma + tepat 3 angka) **ditolak karena ambigu** (sepuluh ribu gaya Inggris, atau 10 gaya Indonesia): minta pengguna menulis `10000`, `10.000`, atau `10`. `10,000,000` (dua koma atau lebih) dibaca sepuluh juta.
- Keyakinan RICE ditulis **persen 0-100**. Nilai 0 < k <= 1 tanpa tanda `%` (mis. `0,8`) ditolak dengan pesan "0,8 maksudnya 80%?". Bila memang kurang dari 1 persen, tulis `0,8%`.

## Pembagian tahap (roadmap)
- **Tanpa `--kapasitas`:** Sekarang = sepertiga teratas (dibulatkan ke atas), Berikutnya = separuh sisanya (dibulatkan ke atas), Nanti = sisanya. Jadi 3 ide = 1/1/1, 4 = 2/1/1, 5 = 2/2/1, 6 = 2/2/2, 7 = 3/2/2. Ide dengan skor **sama persis** ikut tahap ide di atasnya (bisa membuat tahap berikutnya lebih sedikit/kosong; script memberi catatan).
- **Dengan `--kapasitas N` (RICE):** N = orang-hari yang tersedia per tahap. Ide diisi ke Sekarang menurut urutan skor selama total usaha <= N; ide yang tidak muat **dilewati** (tidak mengunci tahap) dan ide berikutnya yang muat tetap masuk. Sisanya diisi ke Berikutnya dengan cara sama, lalu sisanya Nanti. Ide yang usahanya > N selalu Nanti dengan catatan "pecah jadi langkah kecil".
- `--kapasitas` pada ICE diabaikan dengan PERINGATAN (ICE tidak punya kolom usaha).

## Rumus manual (bila script tidak bisa jalan)
Contoh RICE: jangkauan 500, dampak 1, keyakinan 80%, usaha 4 orang-hari: 500 x 1 x 0,8 / 4 = 100.

## Kerangka pendukung (opsional)
- Prioritaskan **masalah pembeli**, bukan daftar fitur; tanya "pembeli mana yang kesulitan apa, seberapa sering?"
- MoSCoW (Harus/Sebaiknya/Bisa/Tidak sekarang) boleh dipakai sebagai penyaring awal untuk fitur pengiriman ke pihak lain.
- Kano (dasar/kinerja/kejutan): untuk memahami harapan pembeli, bukan untuk mengurutkan.
