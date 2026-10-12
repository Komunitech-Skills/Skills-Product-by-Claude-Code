# Skenario 2 (normal kedua)

**Input (pesan pengguna, versi 1.0.1):** "Job mana yang terlambat hari ini? Anggap sekarang Senin 12 Oktober 2026 pukul 21.40 WIB. Data pantauan job usaha saya (Toko Bangunan Sinar Jaya) ada di folder pantau-cron di workspace."

**Output SESUDAH (skill aktif):**

> PANTAU CRON - 12 Okt 21.40 WIB
> BERMASALAH (2 dari 3):
> - HILANG backup-data: belum pernah ada ping sejak didaftarkan (2 jadwal terlewat, terakhir 11 Okt 02.00 WIB). Cek apakah baris ping sudah ditambahkan di akhir job.
> - TERLAMBAT laporan-harian: jadwal 12 Okt 21.00 WIB belum ada ping, lewat 40 menit dari jadwal (toleransi 30 menit). Ping terakhir 11 Okt 21.03 WIB.
> OK (1):
> - tagih-piutang: ping terakhir 12 Okt 07.46 WIB; berikutnya 13 Okt 07.45 WIB.
>
> Saran: cek dulu **backup-data** (paling parah, belum pernah lapor sama sekali sejak didaftarkan — kemungkinan baris "lapor selesai" belum terpasang atau job-nya error), baru lihat **laporan-harian** yang baru telat 40 menit.

**Catatan penguji:** SEBELUM 7 / SESUDAH 8,5. SEBELUM: benar untuk laporan-harian (batas 21.30, lewat 10 menit dari toleransi) dan tagih-piutang OK; tetapi backup-data disebut 'tidak relevan hari ini' dan 'tidak bisa pastikan' padahal dua jadwal Minggu (4 dan 11 Okt) jelas terlewat dan job tak pernah lapor; urutan prioritas keliru (fokus laporan-harian). Tanpa kesalahan angka. SESUDAH: keluaran `cek` apa adanya (HILANG backup-data, 2 jadwal terlewat; TERLAMBAT laporan-harian 40 menit; OK tagih-piutang, ping 07.46), cocok dengan hitungan independen; saran prioritas benar. Kekurangan: kata 'ping'/'baris ping' di kalimat script dan saran ('baris lapor selesai') agak teknis untuk awam.

Perbandingan lengkap: `00-openclaw-sebelum-sesudah.md`.
