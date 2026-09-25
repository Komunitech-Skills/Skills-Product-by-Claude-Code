# Kecepatan Halaman di HP dengan Jaringan Seluler

Skrip `cek_halaman.py` **tidak bisa** mengukur kecepatan sungguhan (butuh membuka halaman asli dengan koneksi internet, browser, dan mengukur waktu — semua di luar cakupan "baca file HTML lokal"). Bagian ini murni **ceklis manual** berdasarkan hal-hal yang bisa dilihat/ditanyakan tanpa tools berbayar.

Mayoritas pembeli produk UMKM Indonesia mengakses lewat HP dengan jaringan seluler (4G, kadang 3G di luar kota besar) — bukan wifi kantor/kafe yang cepat. Kecepatan yang terasa "biasa saja" saat dites di laptop kantor bisa terasa lambat sekali di kondisi nyata pelanggan.

## Pertanyaan & pengecekan manual

1. **Coba buka sendiri pakai data seluler (bukan wifi).** Matikan wifi HP, buka halaman pakai kuota, rasakan sendiri apakah terasa lambat (lebih dari 3-4 detik untuk mulai terlihat sesuatu terasa lambat bagi kebanyakan pengguna).
2. **Hitung jumlah & ukuran gambar di halaman.** Foto produk langsung dari kamera HP/DSLR biasanya 3-8 MB per foto — kalau dipasang mentah tanpa dikompres, satu halaman bisa memuat puluhan MB, sangat lambat di jaringan seluler. Sarankan kompres gambar (banyak tool gratis online, cari "kompres gambar online gratis") sebelum diunggah, target di bawah 200-300 KB per foto untuk web.
3. **Hitung-hitung otomatis dari page builder/tema yang berat.** Tema WordPress dengan banyak slider/animasi/plugin sekaligus sering jadi penyebab lambat — kalau pengguna tidak tahu, sarankan tanya ke pembuat websitenya atau cek dengan menonaktifkan plugin satu-satu untuk melihat mana yang paling berpengaruh (butuh akses admin, di luar cakupan skill ini untuk dieksekusi langsung).
4. **Cek apakah pakai hosting murah dengan performa lambat** — kalau pengguna tidak tahu, tanyakan kapan terakhir kali komplain "situs lambat" dari pelanggan; kalau sering, bisa jadi memang perlu upgrade hosting (di luar cakupan teknis skill ini, sarankan konsultasi ke penyedia hosting).
5. **PageSpeed Insights (gratis, tanpa akun, tanpa API key):** https://pagespeed.web.dev/ — pengguna cukup tempel URL halamannya sendiri. Skill ini tidak menjalankan tool ini secara otomatis (perlu akses internet real-time ke tool pihak luar), tapi sangat disarankan sebagai langkah lanjutan pengguna sendiri, dan hasilnya bisa ditempel balik ke agent untuk dibantu diartikan.

## Yang TIDAK boleh dijanjikan

- Jangan mengarang angka skor kecepatan (mis. "skor PageSpeed kamu pasti di atas 80") — skill ini tidak mengukur kecepatan sungguhan sama sekali.
- Jangan menjanjikan "setelah ini pasti loading jadi kilat" — cukup sebutkan potensi penyebab & langkah masuk akal, hasil akhirnya tergantung banyak faktor di luar kendali teks/kode halaman (hosting, jaringan pengunjung, dll.).
