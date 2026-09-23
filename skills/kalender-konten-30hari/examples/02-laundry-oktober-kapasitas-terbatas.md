# 02 — Laundry, Oktober 2026 penuh (31 hari), kapasitas video terbatas

## Skenario
S2 — permintaan normal dengan batasan produksi ("cuma sanggup 3 video seminggu"), platform IG + WA Status, dan promo gajian nyata
25–27 Oktober. Periode yang diminta "bulan Oktober" (31 hari), jadi script dijalankan dengan `--hari 31`, bukan default 30.

## Input pengguna
```
Bikinin jadwal konten Oktober buat Laundry Wangi Sejati di Depok ya. Aku cuma sanggup bikin video 3x seminggu, sisanya foto atau
status WA aja. Posting di IG sama status WA. Tiap gajian tgl 25-27 Oktober ada diskon 10% cuci kiloan. Order lewat WA, bisa antar jemput.
```

Perintah yang dijalankan:
```bash
python3 scripts/buat_kalender.py --mulai 2026-10-01 --hari 31 \
  --pilar "Hasil Kerja,Tips Perawatan,Promo,Testimoni,Tim & Proses" --platform "IG,WA Status" \
  --momen "2026-10-25:Promo gajian diskon 10% cuci kiloan (25–27 Okt):promo" \
  --momen "2026-10-26:Promo gajian hari ke-2:promo" --momen "2026-10-27:Promo gajian hari terakhir:promo" --format json
python3 scripts/buat_kalender.py --isi kalender.json --format md
python3 scripts/buat_kalender.py --isi kalender.json --format csv --pemisah "," --output kalender_laundry.csv
```

## Output

## Kalender Konten Laundry Wangi Sejati — 01 Okt 2026 s.d. 31 Okt 2026
Pilar: Hasil Kerja (6 hari), Tips Perawatan (6), Promo (9), Testimoni (5), Tim & Proses (5) | Platform: IG + WA Status
Video: 3 per minggu (Senin–Minggu) — hari lain ditandai "Foto/Story IG + WA Status saja".

| No | Tanggal | Hari | Momen | Pilar | Platform | Format | Ide Konten | Hook / Judul | CTA | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 01 Okt 2026 | Kamis | Hari Kesaktian Pancasila; Hari gajian (tgl 1) — hari peringatan: konten penghormatan, hindari hard-selling | Hasil Kerja | IG + WA Status | Reels/video pendek + WA Status | Hari Kesaktian Pancasila: foto tim laundry + ucapan menghormati, tanpa promo walau hari gajian | Mengenang, lalu bekerja lebih baik | Bagikan ke keluarga | Belum |
| 2 | 02 Okt 2026 | Jumat | Hari Batik Nasional | Tips Perawatan | IG + WA Status | Foto/Story IG + WA Status saja | Hari Batik: tips mencuci kemeja batik agar warna awet (cuci terpisah, jangan diperas keras) | Batik kesayangan, jangan asal cuci | Simpan tips ini | Belum |
| 3 | 03 Okt 2026 | Sabtu |  | Promo | IG + WA Status | Reels/video pendek + WA Status | Before-after jaket kotor setelah dicuci (jaket milik pelanggan, dengan izin) | Jaket dekil jadi kinclong lagi | Chat WA untuk antar-jemput | Belum |
| 4 | 04 Okt 2026 | Minggu |  | Testimoni | IG + WA Status | Foto/Story IG + WA Status saja | Screenshot chat testimoni pelanggan (nama & nomor disamarkan, dengan izin) | Kata pelanggan minggu ini | Chat WA untuk order | Belum |
| 5 | 05 Okt 2026 | Senin |  | Tim & Proses | IG + WA Status | Foto/Story IG + WA Status saja | Foto proses sortir pakaian per warna sebelum dicuci | Kenapa bajumu kami pisah warna? | Tanya proses kami via WA | Belum |
| 6 | 06 Okt 2026 | Selasa |  | Hasil Kerja | IG + WA Status | Reels/video pendek + WA Status | Video lipatan rapi pakaian 1 kantong laundry kiloan | Selesai dilipat, tinggal masuk lemari | Chat WA untuk antar-jemput | Belum |
| 7 | 07 Okt 2026 | Rabu |  | Tips Perawatan | IG + WA Status | Foto/Story IG + WA Status saja | Tips hilangkan noda kopi di kemeja putih di rumah | Noda kopi? Jangan panik dulu | Simpan tips ini | Belum |
| 8 | 08 Okt 2026 | Kamis |  | Promo | IG + WA Status | Reels/video pendek + WA Status | Info layanan & harga normal cuci kiloan + antar-jemput [isi: harga & area] | Cucian numpuk? Kami jemput | Chat WA untuk order | Belum |
| 9 | 09 Okt 2026 | Jumat |  | Testimoni | IG + WA Status | Foto/Story IG + WA Status saja | Ulasan Google Maps pelanggan (dengan izin) jadi Story | Bintang dari pelanggan kami | Tulis ulasanmu di Google Maps | Belum |
| 10 | 10 Okt 2026 | Sabtu | Tanggal kembar 10.10 — musim promo akhir tahun (cek kampanye marketplace) | Promo | IG + WA Status | Reels/video pendek + WA Status | Tanggal 10.10: [isi: promo 10.10 jika ada]. Jika tidak ada promo: video 'cucian weekend beres, kamu tinggal santai' | Weekend santai, cucian beres | Chat WA untuk antar-jemput | Belum |
| 11 | 11 Okt 2026 | Minggu |  | Tim & Proses | IG + WA Status | Foto/Story IG + WA Status saja | Kenalan dengan tim: siapa yang menyetrika hari ini | Tangan di balik bajumu yang rapi | Sapa tim kami di komentar | Belum |
| 12 | 12 Okt 2026 | Senin |  | Hasil Kerja | IG + WA Status | Foto/Story IG + WA Status saja | Foto hasil cuci sepatu kanvas (jika layanan tersedia [isi: ya/tidak]) | Sepatu putih lagi, siap dipakai | Chat WA untuk order | Belum |
| 13 | 13 Okt 2026 | Selasa |  | Tips Perawatan | IG + WA Status | Reels/video pendek + WA Status | Video tips: cara baca label perawatan di baju | Simbol di label baju artinya apa? | Simpan & share | Belum |
| 14 | 14 Okt 2026 | Rabu |  | Promo | IG + WA Status | Foto/Story IG + WA Status saja | Story: jadwal antar-jemput minggu ini [isi: hari & jam] | Jadwal jemput cucian minggu ini | Balas Status untuk booking | Belum |
| 15 | 15 Okt 2026 | Kamis |  | Testimoni | IG + WA Status | Reels/video pendek + WA Status | Video testimoni singkat pelanggan langganan (dengan izin) | Langganan sejak awal buka | Chat WA untuk order | Belum |
| 16 | 16 Okt 2026 | Jumat |  | Tim & Proses | IG + WA Status | Foto/Story IG + WA Status saja | Foto mesin & deterjen yang dipakai (sebut merek/jenis hanya jika pemilik setuju) | Yang kami pakai untuk cucianmu | Tanya via WA | Belum |
| 17 | 17 Okt 2026 | Sabtu |  | Hasil Kerja | IG + WA Status | Reels/video pendek + WA Status | Video before-after bed cover (dengan izin) | Bed cover bersih, tidur lebih nyenyak | Chat WA untuk antar-jemput | Belum |
| 18 | 18 Okt 2026 | Minggu |  | Tips Perawatan | IG + WA Status | Foto/Story IG + WA Status saja | Tips menjemur pakaian saat musim hujan di rumah | Hujan terus, baju apek? | Simpan tips ini | Belum |
| 19 | 19 Okt 2026 | Senin |  | Promo | IG + WA Status | Foto/Story IG + WA Status saja | Info layanan ekspres [isi: ada/tidak, harga normal] | Butuh cepat? Tanya layanan ekspres | Chat WA untuk order | Belum |
| 20 | 20 Okt 2026 | Selasa | Tanggal tua — konten hemat/nilai | Testimoni | IG + WA Status | Reels/video pendek + WA Status | Tanggal tua: video tips hemat — kapan cuci sendiri, kapan laundry | Tanggal tua, cucian tetap beres | Simpan video ini | Belum |
| 21 | 21 Okt 2026 | Rabu | Tanggal tua — konten hemat/nilai | Tim & Proses | IG + WA Status | Foto/Story IG + WA Status saja | Story: proses setrika uap kemeja kerja | Kemeja kerja licin tanpa ribet | Tanya via WA | Belum |
| 22 | 22 Okt 2026 | Kamis | Hari Santri | Hasil Kerja | IG + WA Status | Reels/video pendek + WA Status | Hari Santri: video merapikan sarung & baju koko pelanggan (dengan izin), ucapan Selamat Hari Santri | Sarung & koko rapi untuk ngaji | Chat WA untuk antar-jemput | Belum |
| 23 | 23 Okt 2026 | Jumat | Tanggal tua — konten hemat/nilai | Tips Perawatan | IG + WA Status | Foto/Story IG + WA Status saja | Tanggal tua: tips merawat handuk supaya tidak bau | Handuk bau apek? Coba ini | Simpan tips ini | Belum |
| 24 | 24 Okt 2026 | Sabtu | Tanggal tua — konten hemat/nilai | Testimoni | IG + WA Status | Foto/Story IG + WA Status saja | Kolase ulasan pelanggan bulan ini (dengan izin) | Terima kasih sudah percaya | Tulis ulasanmu di Google Maps | Belum |
| 25 | 25 Okt 2026 | Minggu | Promo gajian diskon 10% cuci kiloan (25–27 Okt); Hari gajian (tgl 25) | Promo | IG + WA Status | Reels/video pendek + WA Status | Pengumuman promo gajian: diskon 10% cuci kiloan, 25–27 Oktober (syarat ditulis jelas) | Gajian: cuci kiloan diskon 10% | Chat WA sebelum 27 Oktober | Belum |
| 26 | 26 Okt 2026 | Senin | Promo gajian hari ke-2 | Promo | IG + WA Status | Foto/Story IG + WA Status saja | Pengingat promo hari ke-2: foto tumpukan cucian yang sudah siap antar | Diskon 10% masih sampai besok | Chat WA untuk antar-jemput | Belum |
| 27 | 27 Okt 2026 | Selasa | Promo gajian hari terakhir | Promo | IG + WA Status | Reels/video pendek + WA Status | Hari terakhir promo: video singkat proses jemput cucian | Hari terakhir diskon 10% cuci kiloan | Chat WA hari ini | Belum |
| 28 | 28 Okt 2026 | Rabu | Hari Sumpah Pemuda | Tim & Proses | IG + WA Status | Foto/Story IG + WA Status saja | Sumpah Pemuda: kenalan dengan tim muda laundry + semangat kerja | Pemuda di balik laundry kami | Sapa tim di komentar | Belum |
| 29 | 29 Okt 2026 | Kamis |  | Hasil Kerja | IG + WA Status | Reels/video pendek + WA Status | Video before-after kemeja putih menguning (dengan izin) | Kemeja kuning jadi cerah lagi | Chat WA untuk order | Belum |

📥 Versi CSV: `kalender_laundry.csv` (pemisah koma untuk Google Sheets, UTF-8). Pakai Excel berbahasa Indonesia? Minta versi pemisah `;`.

💡 Tips eksekusi:
- Rekam 3 video minggu depan sekaligus di hari yang sepi (mis. Senin siang) — cukup HP + cahaya jendela.
- Kumpulkan izin pelanggan untuk foto before-after & testimoni sejak awal bulan (tanya via WA saat cucian diantar).
- WA Status paling efektif untuk pelanggan sekitar: unggah 1–3 status per hari, ulang info antar-jemput di hari promo.
- Cek Insight IG di pertengahan bulan untuk jam posting terbaik.
- Mau saya buatkan caption untuk tanggal 25–27 atau pesan broadcast WA promo gajian? (skill `caption-sosmed-umkm` / `broadcast-wa`)

📝 Asumsi: periode 1–31 Oktober 2026 (satu bulan penuh); gajian tanggal 25 & 1 (default) — tanggal 1 jatuh di Hari Kesaktian Pancasila sehingga
tidak dipakai untuk promo; promo **hanya** 25–27 Oktober, hari berpilar "Promo" lainnya diisi info layanan dengan harga normal `[isi: …]`; 10.10 tidak
ada promo (disiapkan alternatif); layanan cuci sepatu & ekspres belum tentu ada (`[isi: …]`); semua foto/ulasan pelanggan dengan izin.

## Catatan penguji
- **Tanggal & hari diverifikasi independen** (rumus Zeller): 31/31 benar (1 Okt 2026 = Kamis, 31 Okt = Sabtu). Tidak ada promo di 1 Okt (hari
  peringatan sekaligus hari gajian) ✔. Promo 9/31 = 29% ✔. Video per minggu ISO: 2, 3, 3, 3, 3 ✔ (≤ 3 sesuai kemampuan).
- **Bagus:** kemampuan produksi dihormati lewat kolom Format; promo 10.10 tidak dikarang; tidak ada klaim (merek deterjen hanya jika pemilik setuju).
- **Kurang:** (1) Default skill **30 hari** — bila agent mengikuti default secara harfiah untuk "bulan Oktober", tanggal 31 Okt hilang. SKILL.md tabel Input
  sebaiknya menulis "Periode: 1 bulan kalender penuh bila pengguna menyebut nama bulan (28–31 hari)". (2) Script tetap memaksa pilar promo di 10.10 walau
  usaha jasa lokal tidak ikut kampanye marketplace — agent harus menetralkan sendiri (ringan). (3) Kolom Format untuk kapasitas produksi harus diubah manual di JSON; script tidak punya opsi `--video-per-minggu` (saran fitur).
