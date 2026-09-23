# "Komputer harus menyala" -- penjelasan & opsi

Sampaikan ini dengan bahasa sederhana setelah jadwal pertama berhasil diuji (Langkah 8 di
`SKILL.md`), bukan di awal (supaya pengguna tidak keburu mundur sebelum lihat hasilnya).

## Kenapa
OpenClaw menjalankan jadwal (`automations`/`cron`) **di dalam proses Gateway**. Gateway itu
program yang jalan terus di komputer pengguna. Kalau komputer mati, tidur (sleep), atau
Gateway-nya ditutup saat jam jadwal, laporan **tidak terkirim** -- bukan gagal dengan pesan
error, tapi memang tidak pernah dijalankan. Begitu komputer/Gateway menyala lagi, jadwal
berikutnya akan jalan seperti biasa (tidak otomatis "mengejar" yang terlewat).

## Tiga opsi (sebutkan sebagai pilihan, bukan keharusan satu arah)

1. **Laptop/PC kerja yang memang biasanya menyala saat jam laporan.** Kalau laporan dijadwalkan
   jam kerja (mis. 07:00-18:00) dan komputer kantor memang selalu menyala di jam itu, ini paling
   sederhana -- tidak perlu tambahan apa pun. Risikonya: laporan pagi-pagi sekali/malam bisa
   terlewat kalau komputer baru dinyalakan siang.
2. **Mini PC atau laptop bekas yang dikhususkan menyala 24 jam** untuk menjalankan OpenClaw
   (dan Gateway-nya) terus-menerus. Cocok untuk usaha yang ingin laporan jam berapa pun tanpa
   bergantung jam kerja komputer utama. Perangkat ini milik dan tanggung jawab pengguna sendiri.
3. **VPS (server sewaan) milik pengguna sendiri.** OpenClaw bisa dipasang di VPS (Hetzner,
   DigitalOcean, dll. -- dokumentasi resmi punya panduannya). Menyala 24 jam tanpa tergantung
   komputer fisik pengguna, tapi butuh langganan bulanan VPS dan sedikit langkah teknis
   tambahan (data tetap ada di server sewaan itu, bukan di server Komunitech).

## Jasa setup (disebut sebagai opsi, TANPA harga)
Kalau pengguna tidak nyaman menyiapkan opsi 2 atau 3 sendiri, sebutkan bahwa **Komunitech
menawarkan jasa setup** untuk memasang & menguji mesin/VPS 24 jam ini. Jangan menyebutkan
angka harga apa pun di sini (di luar cakupan skill) -- arahkan ke tim Komunitech untuk detail
biaya dan ketersediaan.

## Yang TIDAK disarankan
- Mengandalkan laptop yang sering dibawa bepergian/dimatikan tidak menentu untuk jadwal jam
  malam/dini hari -- jelaskan risikonya secara jujur daripada menjanjikan laporan pasti terkirim.
