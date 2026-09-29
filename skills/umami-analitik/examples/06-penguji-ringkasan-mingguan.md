# 06 (penguji) - Skenario normal 1: ringkasan minggu lalu
Permintaan: "Berapa pengunjung web saya minggu lalu, naik nggak?" Umami 3.4.0 asli, kunci view-only `agen-baca`.
Perintah: `umami.py ringkasan --periode minggu-lalu` -> 11 pengunjung / 12 kunjungan / 23 tayangan, bounce 25%, rata-rata 48 dtk; pembanding 4/4/6.
Verifikasi independen: API mentah `/stats` (Bearer) memberi angka sama (23/11/12/3/580; comparison 6/4/4/2/70). LULUS.
Data uji penguji (fiktif, 3-9 Agu 2026, dikirim lewat /api/send): 3 pengunjung, 6 tayangan, bounce 1 (33,3%), klik-wa 1, UTM whatsapp 1, referrer instagram 1 -> semua cocok dengan keluaran skill.
Catatan: rata-rata lama skill 70 dtk (210/3), hitungan langsung dari tabel DB 73 dtk (220/3): Umami tidak menghitung event penutup dalam totaltime. Skill mengikuti layar Umami (sesuai klaim), tetapi tidak menjelaskan selisih ini.
