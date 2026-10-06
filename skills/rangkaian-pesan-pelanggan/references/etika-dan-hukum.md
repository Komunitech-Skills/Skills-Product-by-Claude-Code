# Etika & Dasar Hukum Rangkaian Pesan Pelanggan

> Bukan nasihat hukum. Ringkasan praktis; dicek terakhir 2026-10-06 mengacu pada rujukan yang sama dengan skill `aktifkan-kembali-pelanggan` dan `pesan-prospek-wa` (rincian pasal ada di sana). Untuk volume besar atau industri teregulasi, konsultasikan ke konsultan hukum/perlindungan data.

## Prinsip
1. **Hubungan yang jelas:** penerima pernah membeli, bertanya, atau mendaftar di usaha Anda. Bukan database beli/bocoran/scraping.
2. **Manusia yang mengirim (WA).** AI menyiapkan pesan dan jadwal; pemilik menekan kirim, membaca balasan, memutuskan lanjut atau berhenti. OpenClaw (cron) hanya boleh **mengingatkan pemilik** di Telegram.
3. **Opt-out di setiap pesan** dan dihormati di semua kanal.
4. **Data minimal:** nama panggilan, kanal kontak, tahap rangkaian, status. Tidak menyimpan alasan pribadi atau data sensitif.
5. **Tanpa urgensi palsu, klaim karangan, testimoni/ulasan palsu.**

## UU PDP (No. 27/2022)
Nomor HP, email, dan riwayat belanja adalah data pribadi. Memprosesnya butuh dasar yang sah (mis. persetujuan atau kepentingan yang sah) dan penerima berhak menarik persetujuan/menghentikan pemrosesan. Karena itu "stop" wajib dihormati, tidak boleh dilewati lewat kanal lain, dan perlu dicatat. Memakai data orang lain secara melawan hukum diancam pidana, sehingga daftar nomor beli/bocoran ditolak.
- **Email/newsletter:** gunakan daftar yang dikumpulkan dengan persetujuan jelas (idealnya konfirmasi ganda) dan tautan berhenti berlangganan (lihat `listmonk-newsletter`).
- **Telegram:** bot resmi hanya bisa menulis ke orang yang sudah memulai chat dengannya, pas untuk opt-in sungguhan.

## UU Perlindungan Konsumen (No. 8/1999) dan UU ITE
Informasi harga, stok, promo, dan hadiah harus benar dan bisa dipenuhi; pernyataan menyesatkan dilarang. Itu dasar larangan "stok terakhir/hari ini saja" yang tidak benar dan ulasan palsu. Tenggat promo ditulis hanya bila sungguh ada, lengkap dengan tanggal berlaku.

## Keamanan akun WhatsApp
WhatsApp Web lewat OpenClaw bukan jalur resmi; nomor bisa diblokir. Skill ini tidak mengirim apa pun. Batas pegangan: maksimal 10 pesan per hari dari satu nomor (naik hanya atas permintaan pemilik; di atas 15 tidak disarankan), satu pesan per pelanggan per hari, jam 09.00-20.00 setempat, tidak hari Minggu, beri jeda antar pesan. Bila ada laporan spam/blokir, hentikan dan periksa isi pesan serta daftar sasaran.

## Aturan platform
Marketplace dan platform ulasan memiliki aturan sendiri (mis. tentang menghubungi pembeli di luar chat platform dan imbalan untuk ulasan). Cek aturan Pusat Penjual/Bantuan platform yang Anda pakai; skill ini tidak mengklaim isi aturan terbaru.

## Kapan tidak menghubungi
Sudah minta berhenti; sedang punya keluhan/sengketa belum selesai (selesaikan dulu); pembelian sensitif (kesehatan, keuangan pribadi) sehingga hanya pengingat umum tanpa rincian; nomor yang jelas bukan milik orangnya lagi.
