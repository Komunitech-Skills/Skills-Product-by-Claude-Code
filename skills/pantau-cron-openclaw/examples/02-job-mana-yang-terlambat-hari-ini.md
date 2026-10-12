# Skenario 2 (normal kedua): job mana yang terlambat hari ini?

**Input (pesan pengguna, versi 1.0.2):** "Job mana yang terlambat hari ini? Anggap sekarang Senin 12 Oktober 2026 pukul 21.40 WIB. Data pantauan job usaha saya (Toko Bangunan Sinar Jaya) ada di folder pantau-cron di workspace."

**Output SESUDAH (skill aktif):**

> Saya cek folder data pantauan Toko Bangunan Sinar Jaya per Senin 12 Oktober 2026 pukul 21.40 WIB. Hasilnya:
>
> ```
> PANTAU CRON - 12 Okt 21.40 WIB
> BERMASALAH (2 dari 3):
> - HILANG backup-data: belum pernah lapor selesai sejak didaftarkan (2 jadwal terlewat, terakhir 11 Okt 02.00 WIB). Cek apakah langkah "lapor selesai" sudah ditambahkan di akhir jadwal otomatis itu.
> - TERLAMBAT laporan-harian: jadwal 12 Okt 21.00 WIB belum ada kabar "selesai", lewat 40 menit dari jadwal (toleransi 30 menit). Terakhir lapor selesai 11 Okt 21.03 WIB.
> OK (1):
> - tagih-piutang: terakhir lapor selesai 12 Okt 07.46 WIB; berikutnya 13 Okt 07.45 WIB.
> ```
>
> Ringkasnya:
> - **Terlambat hari ini:** `laporan-harian` — harusnya lapor jam 21.00, sampai sekarang (21.40) belum ada kabar selesai, sudah lewat 40 menit dari toleransi 30 menit.
> - **Lebih parah, "hilang":** `backup-data` — sama sekali belum pernah lapor selesai sejak didaftarkan, dua jadwal berturut-turut terlewat (harusnya jalan tiap Minggu dini hari).
> - **Aman:** `tagih-piutang` sudah lapor selesai pagi ini sesuai jadwal.
>
> Saran: untuk `laporan-harian`, cek dulu apakah komputer/perangkat yang menjalankannya sedang mati/tidur sekitar jam 21.00 tadi, atau jadwalnya memang gagal jalan. Untuk `backup-data`, karena tidak pernah lapor sama sekali sejak awal, kemungkinan besar langkah "lapor selesai" belum ditambahkan di akhir jadwalnya — ini perlu dibereskan dulu supaya pantauan ini akurat (bukan cuma soal backup-nya gagal).
>
> Mau saya bantu telusuri salah satunya dulu, atau pasang pengawas otomatis (kabar lewat Telegram tiap kali ada yang terlambat/hilang) supaya tidak perlu cek manual seperti ini lagi?

**Catatan:** keluaran `cek` apa adanya; status cocok dengan hitungan manual dan 200 kasus acak independen. Tanpa skill: laporan-harian benar, tetapi backup-data (2 Minggu terlewat) disebut "tidak relevan hari ini". Nilai: sebelum 6,5 / sesudah 8,5.
