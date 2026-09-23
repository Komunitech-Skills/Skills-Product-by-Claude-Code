# 04 — Input tidak lengkap + minta WhatsApp

**Skenario:** S4. Pengguna tidak menyebut sumber data maupun nomor, dan memilih WhatsApp.

**Input pengguna (persis):**
> kirim ringkasan keuangan bulanan ke WA saya ya

## Output
```
Bisa. Supaya laporannya benar dan terkirim ke tempat yang tepat, saya perlu 3 hal:

1. Sumber datanya di mana? Folder berisi file buku kas (CSV/Excel yang disimpan sebagai CSV:
   tanggal, keterangan, uang masuk/keluar). Kalau belum ada, saya sarankan folder
   Dokumen/Laporan-AI/masuk/keuangan.
2. Jadwal: default saya tanggal 1 setiap bulan pukul 07:00 WIB (untuk bulan sebelumnya).
   Komputer tempat OpenClaw berjalan biasanya menyala jam segitu?
3. Mau dikirim ke mana? Saran saya **Telegram** (bot resmi, tanpa risiko blokir).
   Kalau tetap WhatsApp, syaratnya:
   - pakai **nomor WhatsApp terpisah** untuk OpenClaw (bukan nomor usaha/pribadi utama),
   - laporan hanya ke nomor Anda sendiri, bukan grup/pelanggan,
   - Anda membaca & menyetujui risiko ini:
     "OpenClaw memakai WhatsApp Web (tidak resmi, lewat scan QR), bukan WhatsApp Business API
     resmi. Syarat Layanan WhatsApp melarang pengiriman pesan otomatis massal/non-personal,
     sehingga ada risiko nomor diblokir. Untuk laporan ke diri sendiri risikonya rendah,
     tapi tetap ada. Telegram tidak punya risiko ini."
   Balas "ya, saya mengerti risikonya" + nomor tujuan (format +62...), atau pilih Telegram
   dan kirim chat id Anda.
```

**Lanjutan (disimulasikan):** pengguna memilih WA, menjawab "ya, saya mengerti risikonya", nomor +62 812-0000-0001 (fiktif). Agent memastikan nomor itu ada di `channels.whatsapp.allowFrom` (kunci ini ada di skema konfigurasi OpenClaw 2026.9.5 — dicek), lalu memakai baris akhir `--channel whatsapp --to "+6281200000001"`.

## Catatan penguji
- Tanya sekali, 3 pertanyaan bernomor, default disebutkan — sesuai tabel wawancara (poin 5 penerima tetap wajib).
- Aturan pemilik dipatuhi: Telegram default, WA hanya nomor terpisah + persetujuan tertulis + hanya ke pemilik.
- Perintah kanal yang dirujuk (`openclaw channels add --channel whatsapp`, `openclaw channels login --channel whatsapp`, `channels add --channel telegram --token`) valid menurut `--help` OpenClaw 2026.9.5; login QR tidak bisa diuji di mesin uji.
- Kurang: resep ringkasan bulanan tidak menjelaskan cara menangani bulan tanpa data sebelumnya ("perbandingan terhadap bulan sebelumnya bila tersedia") — ringan.
