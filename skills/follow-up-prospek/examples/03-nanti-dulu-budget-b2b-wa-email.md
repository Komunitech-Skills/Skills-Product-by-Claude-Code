# 03 — "Nanti dulu, budget baru ada November" (B2B, WA + email)

**Skenario:** S3 — tahap C ("nanti dulu"), jarak longgar mengikuti waktu yang disebut prospek, dua saluran.

**Input pengguna:**
> Saya trainer public speaking, usaha saya Suara Percaya Diri Fiktif. Tadi (23 Sept) Bu Sari, HR Manager PT Arunika Fiktif, bilang tertarik training 2 hari untuk 20 staf sales (penawaran Rp 30 juta) tapi anggaran training baru cair awal November. Tolong bikinin follow-up WA dan email, yang sopan ya, jangan kesannya ngejar.

**Perintah script:**
```bash
python3 scripts/jadwal_followup.py --mulai 2026-09-23 --hari "7,40,60"
```
(Jarak mengikuti pola tahap C: nilai tanpa meminta ±H+7, cek ulang di awal November sesuai janji prospek, pamit ±3 minggu kemudian.)

## Output

### Balasan langsung (hari ini) · WA
Siap, Bu Sari, terima kasih sudah dikabari. Boleh saya hubungi lagi di awal November saat anggaran sudah tersedia? Kalau sebelum itu ada pertanyaan soal materi atau jadwal, silakan chat saja, Bu.

### Jadwal follow-up – Bu Sari, PT Arunika Fiktif ("nanti dulu" – budget November)
Kontak terakhir (H+0): Rabu, 23 September 2026

| Ke | Rencana | Tanggal kirim | Catatan |
|---|---|---|---|
| 1 | H+7 | Rabu, 30 September 2026 | - |
| 2 | H+40 | Senin, 2 November 2026 | - |
| 3 | H+60 | Senin, 23 November 2026 | digeser dari Minggu |

### Pesan ke-1 · Rabu, 30 September 2026 · WA
Selamat pagi, Bu Sari. Tidak perlu dibalas, hanya berbagi: latihan 5 menit "satu pesan, satu angka" yang sering kami pakai agar tim sales lebih ringkas saat presentasi ke klien. Semoga bermanfaat untuk tim Ibu 🙏

### Pesan ke-1 · Rabu, 30 September 2026 · Email
Subjek: Materi singkat untuk tim sales PT Arunika Fiktif

Yth. Ibu Sari,
Terima kasih atas obrolan minggu lalu. Sambil menunggu anggaran November, berikut satu latihan singkat yang bisa langsung dicoba tim sales: setiap presentasi dibuka dengan satu pesan utama dan satu angka pendukung, lalu dilatih 5 menit berpasangan. Tidak perlu dibalas — semoga bermanfaat.
Salam,
[Nama] – Suara Percaya Diri Fiktif · WA 0812-0000-4401 · [email]

### Pesan ke-2 · Senin, 2 November 2026 · WA
Selamat pagi, Bu Sari. Sesuai obrolan kita bulan September, saya izin menanyakan kembali soal training public speaking 2 hari untuk tim sales. Apakah sekarang waktu yang pas untuk membahas jadwal, atau lebih baik saya hubungi lagi di waktu lain?

### Pesan ke-2 · Senin, 2 November 2026 · Email
Subjek: Re: Penawaran Training Public Speaking – PT Arunika Fiktif

Yth. Ibu Sari,
Sesuai pembicaraan kita pada 23 September, saya izin menanyakan kembali rencana training public speaking 2 hari untuk 20 staf sales (penawaran Rp 30.000.000). Jika anggaran sudah tersedia, saya bisa mengirim dua pilihan tanggal pelaksanaan di bulan November–Desember. Jika belum, cukup kabari waktu yang lebih tepat.
Salam,
[Nama] – Suara Percaya Diri Fiktif · WA 0812-0000-4401 · [email]

### Pesan ke-3 · Senin, 23 November 2026 · WA
Selamat pagi, Bu Sari. Sepertinya training ini belum jadi prioritas saat ini, dan itu tidak apa-apa. Saya tidak akan mengirim pengingat lagi. Kalau nanti tim sales butuh pelatihan, saya siap membantu kapan saja. Terima kasih atas waktunya 🙏

### Pesan ke-3 · Senin, 23 November 2026 · Email
Subjek: Menutup penawaran training public speaking

Yth. Ibu Sari, sepertinya training ini belum menjadi prioritas saat ini, dan kami sangat memahaminya. Kami tidak akan mengirim pengingat lagi; penawaran tetap bisa diperbarui kapan pun dibutuhkan. Terima kasih atas waktu Ibu.
Salam, [Nama] – Suara Percaya Diri Fiktif

### Aturan main
- Kirim pukul 09.00–11.00 atau 13.00–15.00 hari kerja; hindari salat Jumat & larut malam.
- Jika Bu Sari membalas → hentikan urutan dan tanggapi. Jika ia menyebut waktu baru, jadwalkan ulang dari tanggal itu.
- "Tanya atasan dulu" → tawarkan ringkasan 1 halaman untuk atasan. "Mahal" → tanyakan anggaran, tawarkan versi 1 hari/peserta lebih sedikit (bukan langsung diskon).

### Asumsi
- Latihan "satu pesan, satu angka" adalah contoh konten — ganti dengan tips khas Anda sendiri.
- Tanggal libur nasional November tidak diketahui; jika ada, sebutkan agar jadwal digeser.
- Pesan ke-2 sengaja di 2 November (Senin pertama bulan November) sesuai "awal November".

## Catatan penguji
- Tanggal benar (30 Sep Rabu; 2 Nov Senin; H+60 = 22 Nov Minggu → 23 Nov Senin).
- Bagus: menghormati waktu yang disebut prospek, pesan ke-1 "tidak perlu dibalas", email di thread untuk pesan lanjutan, pamit sopan.
- Kurang (ringan): SKILL.md tahap C menyarankan `--hari "7,21,45"` generik; menyesuaikan ke "awal November" butuh agent menghitung offset sendiri (H+40). Script bisa menerima tanggal absolut (mis. `--tanggal 2026-11-02`) agar tidak perlu menghitung manual.
