# 02 — Permintaan singkat: bank jawaban quick reply Shopee (skincare)

**Skenario:** S2 — permintaan malas; info toko hampir tidak ada → buat bank jawaban dengan `[isi ...]`, tanpa mengarang fakta.

**Input pengguna:**
> bikinin dong quick reply shopee buat toko skincare aku, nama tokonya Glowria Fiktif

## Output

## Bank Jawaban CS – Glowria Fiktif (Shopee)
Nada: ramah-sopan · Sapaan: Kak · Tanda tangan: Admin Glowria
(Bagian `[isi ...]` wajib diganti sebelum dipakai. Tiap template ≤ 500 karakter.)

### 1. Sapaan & jam kerja
**[1.1] Salam pertama** — "Halo Kak, selamat datang di Glowria 😊 Ada yang bisa kami bantu? Boleh sebutkan produk atau jenis kulit Kakak ya."
**[1.2] Di luar jam kerja** — "Terima kasih sudah menghubungi Glowria. Admin aktif [isi hari], pukul [isi jam]. Pesan Kakak akan kami balas saat jam kerja ya 🙏"
**[1.3] Sedang ramai** — "Mohon maaf menunggu, Kak. Chat sedang ramai, pesan Kakak kami balas berurutan secepatnya ya."

### 2. Stok & produk
**[2.1] Stok tersedia** — "Ready, Kak! [isi produk + ukuran] tersedia. Silakan langsung checkout ya."
**[2.2] Stok habis** — "Mohon maaf Kak, [isi produk] sedang kosong. Perkiraan restok [isi tanggal / 'belum ada jadwal']. Mau lihat [isi alternatif] dulu?"
**[2.3] Cocok untuk kulit saya?** — "Untuk memastikan, boleh info jenis & keluhan kulit Kakak? Sebagai info, [isi produk] diformulasikan untuk [isi sesuai deskripsi resmi produk]. Jika punya riwayat alergi, sebaiknya coba di area kecil dulu (patch test)."
**[2.4] Keaslian & izin edar** — "Semua produk kami [isi: original/brand sendiri] dan terdaftar BPOM dengan nomor [isi nomor NA/NE]. Nomornya bisa Kakak cek di situs cekbpom.pom.go.id."
**[2.5] Kedaluwarsa** — "Produk yang kami kirim memiliki masa kedaluwarsa minimal [isi] bulan dari tanggal kirim, Kak."

### 3. Harga & promo
**[3.1] Harga & promo** — "Harga [isi produk] Rp [isi]. [Jika ada: Promo [isi] berlaku s.d. [isi tanggal].] Harga final mengikuti yang tampil saat checkout ya, Kak."
**[3.2] Minta diskon** — "Mohon maaf Kak, harga kami sudah harga terbaik. Pantau voucher toko di halaman Glowria ya, siapa tahu ada promo berikutnya 😊"

### 4. Pengiriman
**[4.1] Ongkir** — "Ongkir muncul otomatis saat checkout sesuai alamat Kakak. [Promo gratis ongkir hanya bila benar ada.]"
**[4.2] Jadwal kirim** — "Pesanan sebelum pukul [isi jam] dikirim di hari yang sama (hari kerja), setelahnya dikirim besok ya, Kak."
**[4.3] Lacak paket** — "Nomor resi bisa dicek di menu Pesanan Saya → Lacak. Status terakhir: [isi]. Kalau lewat estimasi, kabari kami ya, Kak."

### 5. Cara order & pembayaran
**[5.1] Cara order** — "Silakan pilih varian lalu checkout langsung di etalase Glowria ya, Kak. Pembayaran mengikuti metode yang tersedia di Shopee."
**[5.2] Pesanan sudah dibayar** — "Terima kasih, pembayaran sudah terkonfirmasi 🙏 Pesanan diproses dan dikirim [isi waktu]."

### 6. Retur & komplain
**[6.1] Kebijakan** — "Pengembalian/penukaran diajukan lewat fitur Pengembalian Barang/Dana di Shopee maksimal [isi sesuai batas platform] setelah pesanan diterima, dengan video unboxing ya, Kak."
**[6.2] Produk rusak/bocor** — "Mohon maaf sekali produknya diterima dalam kondisi [rusak/bocor] 🙏 Boleh kirim foto/video unboxing & nomor pesanannya? Setelah dicek, kami bantu solusinya lewat fitur pengembalian Shopee dan kabari Kakak [isi waktu]."
**[6.3] Salah kirim** — "Mohon maaf Kak, varian yang diterima tidak sesuai 🙏 Boleh kirim foto produk yang diterima & labelnya? Kami bantu penukarannya lewat fitur pengembalian Shopee."
**[6.4] Iritasi/reaksi kulit** — "Kami sangat menyesal Kakak mengalami [keluhan]. Mohon hentikan pemakaian dulu ya, Kak, dan bila berlanjut sebaiknya periksakan ke dokter. Boleh kami minta nomor pesanan, foto produk & kode produksinya? Kami tindak lanjuti langsung dan kabari [isi waktu]."

### 7. Keamanan & penutup
**[7.1] Waspada penipuan** — "Glowria hanya melayani transaksi melalui Shopee. Admin tidak pernah meminta kode OTP, PIN, atau password."
**[7.2] Terima kasih** — "Terima kasih sudah belanja di Glowria, Kak! Kalau ada kendala, chat kami kapan saja 😊"
**[7.3] Minta ulasan (tanpa imbalan)** — "Jika berkenan, ulasan jujur Kakak sangat membantu kami berkembang 🙏"

**Catatan untuk pemilik toko:**
- Isi dulu: jam kerja, nomor BPOM, batas kedaluwarsa, jam potong kirim, dan waktu tindak lanjut komplain. Jangan pakai template [2.4] bila produk belum punya izin edar.
- Klaim manfaat produk ([2.3]) hanya boleh sesuai yang tertulis di kemasan/izin BPOM — hindari klaim "menyembuhkan jerawat", "memutihkan permanen".
- Mau saya isi sekalian? Kirim info di atas, saya lengkapi semua template.

## Catatan penguji
- Bagus: 21 template (dalam rentang 15–30), kategori sesuai SKILL.md, tidak mengarang stok/harga/izin; aturan marketplace (transaksi hanya di platform) dipatuhi.
- Nilai tambah khas skincare (BPOM, patch test, klaim manfaat) muncul karena `references/alur-komplain.md` kasus 7; namun SKILL.md/templates **tidak** punya template BPOM/klaim kosmetik — agent menambahkannya dari pengetahuan umum (ringan: pertimbangkan catatan kategori khusus di `templates/bank-jawaban.md`).
