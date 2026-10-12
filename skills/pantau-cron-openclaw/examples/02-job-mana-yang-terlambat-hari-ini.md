# Skenario 2 (normal kedua: job mana yang terlambat?)

**Input (pesan pengguna):** "Job mana yang terlambat hari ini? Anggap sekarang Senin 12 Oktober 2026 pukul 21.40 WIB. Data pantauan job usaha saya (Toko Bangunan Sinar Jaya) ada di folder pantau-cron di workspace."

**Output SESUDAH (skill aktif):**

> Hasil pengecekan pantauan job Toko Bangunan Sinar Jaya per Senin 12 Okt 2026, 21.40 WIB:
>
> ```
> PANTAU CRON - 12 Okt 21.40 WIB
> 2 job bermasalah dari 3:
> - HILANG backup-data: belum pernah ada ping sejak didaftarkan (2 jadwal terlewat, terakhir 11 Okt 02.00 WIB). Cek apakah baris ping sudah ditambahkan di akhir job.
> - TERLAMBAT laporan-harian: jadwal 12 Okt 21.00 WIB belum ada ping, lewat 40 menit dari jadwal (toleransi 30 menit). Ping terakhir 11 Okt 21.03 WIB.
> - OK tagih-piutang: ping terakhir 12 Okt 07.46 WIB; berikutnya 13 Okt 07.45 WIB.
> ```
>
> Ringkasnya:
> - **Terlambat**: `laporan-harian` (jadwal 21.00, sudah lewat 40 menit, belum ada tanda selesai).
> - **Hilang** (lebih serius): `backup-data` — sejak didaftarkan belum pernah ada tanda selesai sama sekali, sudah 2 jadwal mingguan terlewat.
> - **Aman**: `tagih-piutang`, sudah lapor tepat waktu pagi tadi.
>
> Saran: untuk `laporan-harian`, cek dulu apakah gateway/komputer sedang mati atau job-nya error barusan (`openclaw automations runs <id>`). Untuk `backup-data`, karena belum pernah lapor sama sekali sejak awal, kemungkinan besar baris "ping" di akhir job itu belum ditambahkan atau job-nya tidak punya izin menjalankan perintah — ini perlu dicek lebih dulu sebelum menyalahkan jadwalnya.

**Catatan penguji:** Kebenaran: kedua sisi benar (backup-data HILANG: 2 jadwal Minggu 4 & 11 Okt terlewat, belum pernah ping; laporan-harian TERLAMBAT, jadwal 12 Okt 21.00, 40 menit dari jadwal / 10 menit lewat batas toleransi 30; tagih-piutang OK, ping 07.46). Diverifikasi independen. SEBELUM menghitung manual dari berkas (benar, tetapi memeriksa log hanya lewat baca file; bahasa 'sudah 2 minggu tidak jalan' agak berlebihan). SESUDAH menjalankan skrip dengan jam simulasi 21.40 WIB (--sekarang) dan --tanpa-catat, menempelkan laporan 'PANTAU CRON' apa adanya (siap diteruskan ke Telegram) + ringkasan tiga baris + saran penelusuran. Kurang: laporan skrip menaruh baris '- OK tagih-piutang' di bawah judul '2 job bermasalah dari 3' (membingungkan); saran masih menyebut 'gateway' dan 'openclaw automations runs <id>' (istilah teknis).

**Skor:** sebelum 7,5, sesudah 8,5. Perbandingan lengkap: `00-openclaw-sebelum-sesudah.md`.
