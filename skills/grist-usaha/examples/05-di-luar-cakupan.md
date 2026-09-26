# Contoh 5 — Di luar cakupan skill `grist-usaha`

## 5a. Minta dibuka ke internet
> **Pengguna:** "Bisa bikin Grist Docker aku bisa dibuka dari HP pas lagi di luar rumah gak?"

**Balasan agent (tolak dengan sopan, jelaskan alasan & alternatif):**
> Untuk keamanan, skill ini tidak akan membantu membuka Grist ke internet (port forwarding,
> tunnel seperti ngrok, atau hosting tanpa HTTPS) — data usaha Anda bisa diakses orang lain kalau
> itu dilakukan sembarangan (lihat `docs/panduan-grist.md` bagian 8). Kalau memang butuh akses
> dari luar rumah, itu perlu HTTPS + autentikasi yang benar — sebaiknya dikonsultasikan ke jasa
> setup Komunitech, bukan dikerjakan sendiri lewat skill ini.

## 5b. Minta dibuatkan grafik/dashboard di Grist
> **Pengguna:** "Bikinin grafik penjualan bulanan di Grist dong"

**Balasan agent:**
> Skill `grist-usaha` fokus di struktur tabel, rumus, impor data, dan baca laporan lewat
> script — belum bisa membuat/mengatur widget grafik Grist (itu dikerjakan langsung di layar
> Grist: pilih tabel → **Add New** → **Add Chart**). Saya bisa bantu siapkan datanya (tabel
> Pesanan yang rapi, misalnya) supaya tinggal Anda pilih jenis grafiknya di Grist. Atau, kalau
> maksudnya laporan teks/tabel ringkasan bulanan, saya bisa buatkan lewat perintah `ringkasan`.

## 5c. Kebutuhan yang lebih cocok jadi aplikasi khusus (bukan tabel Grist)
> **Pengguna:** "Aku mau tiap pesanan Shopee otomatis motong stok, ada picking list juga"

**Balasan agent:**
> Untuk kebutuhan ini, skill **`buku-stok`** lebih cocok — sudah punya logika potong stok
> otomatis dari file pesanan marketplace (Shopee/TikTok/Tokopedia, anti impor ganda), HPP
> rata-rata, dan picking list siap cetak. Tabel Stok di Grist (`grist-usaha`) sifatnya manual/
> ringan, tanpa logika itu. Mau saya arahkan ke `buku-stok`?

> **Pengguna:** "Aku mau follow-up otomatis calon pembeli WA dengan tahap pipeline"

**Balasan agent:**
> Itu wilayah skill **`crm-wa`** (tahap pipeline, draf pesan follow-up + tautan wa.me, pengingat
> harian). Tabel Pelanggan di Grist (`grist-usaha`) hanya daftar kontak sederhana, tanpa alur
> follow-up berjenjang. Saya bisa bantu pindah datanya dari Grist ke `crm-wa` kalau mau.

## 5d. Minta validasi/kirim data lewat SQL langsung ke file `.grist` yang sedang dibuka Grist
> **Pengguna:** "Tulis langsung aja ke file .grist-nya pakai SQL, gak usah lewat Grist"

**Balasan agent (tolak):**
> Skill ini sengaja **hanya membaca** file `.grist` (read-only) — Grist punya lapisan tambahan
> di atas SQLite (metadata tabel, rumus, undo/redo, sinkronisasi tampilan) yang bisa rusak kalau
> ditulis langsung lewat SQL dari luar, apalagi saat dokumennya sedang terbuka. Perubahan data
> harus lewat REST API Grist (`buat-tabel`/`impor-csv`) atau langsung di layar Grist.

## 5e. Minta kunci API ditempel di chat untuk "biar cepat"
> **Pengguna:** "Nih kunci API-nya `abcd1234...`, langsung pakai aja"

**Balasan agent (tolak, arahkan ke cara aman):**
> Mohon jangan tempel kunci API di chat — saya tidak akan menyimpannya dari sini. Jalankan
> sendiri `python3 grist.py simpan-kunci` di terminal Anda dan tempel kuncinya di sana (tidak
> akan terlihat/tercatat). Karena sempat tertulis di sini, sebaiknya buat kunci baru di Grist
> (Profile Settings) setelah ini, supaya yang lama tidak berlaku lagi.
