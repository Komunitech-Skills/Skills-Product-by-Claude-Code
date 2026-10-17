# Gelombang Telegram A3 — pantau-cron-openclaw 1.0.5 (Akun A, 2026-10-17)

Uji di grup Telegram sungguhan, bot pertama @KTclaude1_bot, OpenClaw 2026.10.2. Sisi DENGAN saja (permintaan Akun B 04:15 UTC). Topik **1949**.

| Giliran | Pesan (bot penguji kedua) | Balasan bot pertama |
|---|---|---|
| 1 (04:31 UTC, pesan 1950) | Minta pantau laporan harian 21.00 & tagih piutang 07.45 Senin–Jumat, kabari lewat Telegram bila gagal | Pesan 1952: mencatat 2 jadwal ke pemantauan (toleransi 30 menit, jadwal berikut benar: 17 Okt 21.00, 19 Okt 07.45), jujur bahwa jadwal bernama itu **belum ada** di bot ini, rencana 3 langkah (kalimat lapor-selesai, 2 pengawas tanpa biaya token, satu uji peringatan dulu), tanya ya/tidak + 3 pertanyaan |
| 2 (04:33 UTC, pesan 1953) | "ya" + (a) buatkan jadwalnya, (b) kirim ke topik grup ini, (c) 30 menit cukup | Pesan 1985 (±19 menit kemudian): **menolak tujuan grup** — laporan penjualan/piutang & peringatan berisi angka usaha hanya ke chat pribadi; meminta ID chat pribadi; menyiapkan contoh isi kedua laporan dari data contoh; tidak membuat jadwal apa pun |

## Hasil
- **TIDAK TUNTAS (tanpa skor).** Kunci LOLOS Akun B ("pesan jadwal yang masuk grup = isi laporan utuh"; "rencana menyebut tiap jadwal dijalankan sekali") tidak bisa diperiksa: (1) di bot pertama jadwal sumber belum ada (di bot kedua sudah ada sisa uji lama), (2) skill menolak tujuan kirim grup karena aturan privasinya sendiri — perilaku yang benar untuk data usaha. ID chat pribadi sengaja tidak diberikan (bukan data uji).
- Rencana giliran 1 menyebut "satu uji peringatan dulu", **bukan** "tiap jadwal dijalankan sekali" → kunci rencana 1.0.5 belum terlihat di bot ini.
- Tidak ada jadwal/automation baru yang dibuat di bot pertama (tidak ada yang perlu dihapus).
- Catatan mutu: bahasa awam, jujur soal batas uji; jawaban giliran 2 butuh ±19 menit (banyak langkah alat).

## Saran untuk Akun B
Uji jalan-sekali 1.0.5 sebaiknya di bot kedua (jadwal sumber sudah ada) atau dengan prasyarat: jadwal contoh dibuat lebih dulu dan pesan uji menyatakan tujuan kirim = chat pribadi pemilik (atau skill diberi pengecualian tertulis untuk grup uji). Keputusan revisi di Akun B.
