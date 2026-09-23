# 01 — Toko hijab online, November 2026 (promo 11.11, Hari Pahlawan, gajian tgl 25)

## Skenario
S1 — permintaan normal dan lengkap: jenis usaha fashion/hijab, periode 1 bulan penuh (November = 30 hari), platform konten IG + TikTok,
satu promo nyata dari pengguna (11.11), dan tanggal gajian khusus. Script `buat_kalender.py` dijalankan sungguhan: kerangka `--format json`,
diisi ide oleh agent, lalu diekspor ulang dengan `--isi` ke tabel dan CSV.

## Input pengguna
```
Tolong bikinin kalender konten November 2026 buat toko hijab online aku, Nura Hijab (Bandung). Jualan pashmina ceruty,
bergo instan, sama inner. Jualannya di Shopee & TikTok Shop, kontennya di IG sama TikTok aja. Tgl 11.11 ada promo diskon 20%
semua pashmina + voucher gratis ongkir Shopee. Pembeli kebanyakan karyawati, gajiannya tgl 25.
```

Perintah yang dijalankan:
```bash
python3 scripts/buat_kalender.py --mulai 2026-11-01 \
  --pilar "Promo & Koleksi Baru,OOTD Mix-Match,Edukasi Bahan & Ukuran,Testimoni,Di Balik Layar" \
  --platform "IG,TikTok" --gajian 25 \
  --momen "2026-11-11:Promo 11.11 diskon 20% pashmina + voucher gratis ongkir Shopee:promo" --format json
# (agent mengisi Ide/Hook/CTA) lalu:
python3 scripts/buat_kalender.py --isi kalender.json --format md
python3 scripts/buat_kalender.py --isi kalender.json --format csv --pemisah ";" --output kalender_nura.csv
```

## Output

## Kalender Konten Nura Hijab — 01 Nov 2026 s.d. 30 Nov 2026
Pilar: Promo & Koleksi Baru (7 hari), OOTD Mix-Match (6), Edukasi Bahan & Ukuran (6), Testimoni (6), Di Balik Layar (5) | Platform: IG + TikTok

| No | Tanggal | Hari | Momen | Pilar | Platform | Format | Ide Konten | Hook / Judul | CTA | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 01 Nov 2026 | Minggu |  | Promo & Koleksi Baru | IG + TikTok | Video pendek + Story/Status | Reveal warna pashmina ceruty yang tersedia bulan ini, jejer semua warna di satu frame | Warna pashmina favoritmu ada di sini? | Komen warna incaranmu | Belum |
| 2 | 02 Nov 2026 | Senin |  | OOTD Mix-Match | IG + TikTok | Video try-on / mix-match | 3 gaya pashmina ceruty untuk ke kantor dalam 30 detik (Senin semangat) | 3 gaya pashmina buat Senin pagi | Simpan video ini buat besok | Belum |
| 3 | 03 Nov 2026 | Selasa |  | Edukasi Bahan & Ukuran | IG + TikTok | Carousel / video tips | Carousel: beda ceruty, voal, dan jersey — mana yang adem & jatuh (bahan dari produk sendiri) | Ceruty itu panas nggak sih? | Tanya bahan di komentar | Belum |
| 4 | 04 Nov 2026 | Rabu |  | Testimoni | IG + TikTok | Foto ulasan / Story | Screenshot ulasan pembeli bergo instan + foto pemakaiannya (dengan izin) | Kata mereka soal bergo instan kami | Baca ulasan lengkap di toko | Belum |
| 5 | 05 Nov 2026 | Kamis |  | Di Balik Layar | IG + TikTok | Video pendek proses | Proses packing pesanan: lipat pashmina, masuk plastik, label — suara ASMR | Packing 50 pesanan pagi ini | Follow biar lihat prosesnya | Belum |
| 6 | 06 Nov 2026 | Jumat |  | Promo & Koleksi Baru | IG + TikTok | Video pendek + Story/Status | Bergo instan untuk Jumat santai: pakai 10 detik tanpa jarum | Jumat ini cukup 10 detik | Cek keranjang kuning / link Shopee di bio | Belum |
| 7 | 07 Nov 2026 | Sabtu |  | OOTD Mix-Match | IG + TikTok | Video try-on / mix-match | Mix-match pashmina dengan outfit weekend: kulot + kardigan | Outfit weekend nggak ribet | Coba dan tag kami | Belum |
| 8 | 08 Nov 2026 | Minggu |  | Edukasi Bahan & Ukuran | IG + TikTok | Carousel / video tips | Video tips: cara pilih inner yang pas di kepala (ukuran & bahan inner) | Inner melorot terus? Cek ini | Tanya ukuran di komentar | Belum |
| 9 | 09 Nov 2026 | Senin |  | Testimoni | IG + TikTok | Foto ulasan / Story | Video pembeli (dengan izin) cerita pakai pashmina ceruty seharian kerja | Seharian kerja, masih rapi? | Baca ulasan lengkap di toko | Belum |
| 10 | 10 Nov 2026 | Selasa | Hari Pahlawan — hari peringatan: konten penghormatan, hindari hard-selling | Di Balik Layar | IG + TikTok | Video pendek proses | Konten penghormatan Hari Pahlawan: kutipan pahlawan perempuan (mis. Cut Nyak Dien) + ucapan terima kasih, TANPA promo | Mengenang pahlawan perempuan kita | Bagikan ke teman | Belum |
| 11 | 11 Nov 2026 | Rabu | Promo 11.11 diskon 20% pashmina + voucher gratis ongkir Shopee; Tanggal kembar 11.11 — musim promo akhir tahun (cek kampanye marketplace) | Promo & Koleksi Baru | IG + TikTok | Video pendek + Story/Status | Pengumuman promo 11.11: diskon 20% semua pashmina + voucher gratis ongkir Shopee (syarat & batas waktu ditulis jelas; cek kampanye resmi) | 11.11: semua pashmina diskon 20% | Klaim voucher & checkout di Shopee hari ini | Belum |
| 12 | 12 Nov 2026 | Kamis |  | OOTD Mix-Match | IG + TikTok | Video try-on / mix-match | Tutorial pashmina ceruty untuk kondangan: gaya lilit simpel | Kondangan weekend? Gaya ini aja | Simpan untuk nanti | Belum |
| 13 | 13 Nov 2026 | Jumat |  | Edukasi Bahan & Ukuran | IG + TikTok | Carousel / video tips | Carousel: cara merawat ceruty biar tidak kusut & awet (cuci tangan, jemur teduh) | Ceruty kusut? Ini caranya | Simpan & share ke teman | Belum |
| 14 | 14 Nov 2026 | Sabtu |  | Testimoni | IG + TikTok | Foto ulasan / Story | Kolase foto pembeli pakai bergo instan (dengan izin), tulis kotanya | Dari Bandung sampai Makassar | Tag kami kalau sudah pakai | Belum |
| 15 | 15 Nov 2026 | Minggu |  | Di Balik Layar | IG + TikTok | Video pendek proses | Di balik layar: pilih kain dan cek jahitan tepi pashmina | Cek jahitan satu per satu | Follow untuk lihat prosesnya | Belum |
| 16 | 16 Nov 2026 | Senin |  | Promo & Koleksi Baru | IG + TikTok | Video pendek + Story/Status | Koleksi baru/restock minggu ini (harga normal, tanpa diskon karangan) | Restock warna yang kemarin habis | Cek keranjang kuning / link Shopee di bio | Belum |
| 17 | 17 Nov 2026 | Selasa |  | OOTD Mix-Match | IG + TikTok | Video try-on / mix-match | OOTD kerja 5 hari dengan 1 pashmina netral | 1 pashmina, 5 hari kerja | Komen warna netral favoritmu | Belum |
| 18 | 18 Nov 2026 | Rabu |  | Edukasi Bahan & Ukuran | IG + TikTok | Carousel / video tips | Video tips: ukuran bergo instan S/M/L cocok untuk wajah & bahu seperti apa (sesuai tabel ukuran toko) | Bergo instan ukuran berapa ya? | Tanya ukuran di komentar | Belum |
| 19 | 19 Nov 2026 | Kamis |  | Testimoni | IG + TikTok | Foto ulasan / Story | Ulasan jujur: kritik pembeli + apa yang kami perbaiki (dengan izin) | Kritik pembeli yang kami dengar | Baca ulasan lengkap di toko | Belum |
| 20 | 20 Nov 2026 | Jumat | Tanggal tua — konten hemat/nilai | Di Balik Layar | IG + TikTok | Video pendek proses | Tanggal tua: tips hemat — 1 pashmina dipakai 3 gaya berbeda | Tanggal tua tetap gaya | Simpan video ini | Belum |
| 21 | 21 Nov 2026 | Sabtu | Tanggal tua — konten hemat/nilai | Promo & Koleksi Baru | IG + TikTok | Video pendek + Story/Status | Tanggal tua: kenalan koleksi (harga normal) — fokus nilai: bahan, ukuran, cara pakai; bukan hard-selling | Kenalan dulu, belinya nanti gajian | Masukkan wishlist dulu | Belum |
| 22 | 22 Nov 2026 | Minggu | Tanggal tua — konten hemat/nilai | OOTD Mix-Match | IG + TikTok | Video try-on / mix-match | Mix-match warna pashmina dengan baju motif (aturan warna sederhana) | Baju motif, pashmina warna apa? | Komen warna bajumu | Belum |
| 23 | 23 Nov 2026 | Senin | Tanggal tua — konten hemat/nilai | Edukasi Bahan & Ukuran | IG + TikTok | Carousel / video tips | Carousel: beda inner ninja, inner bandana, inner rajut — kapan dipakai | Inner mana yang kamu butuh? | Tanya di komentar | Belum |
| 24 | 24 Nov 2026 | Selasa | Tanggal tua — konten hemat/nilai | Testimoni | IG + TikTok | Foto ulasan / Story | Q&A Story: jawab 5 pertanyaan pembeli terbanyak minggu ini | Pertanyaan kalian, kami jawab | Kirim pertanyaan lewat Story | Belum |
| 25 | 25 Nov 2026 | Rabu | Hari Guru Nasional; Hari gajian (tgl 25) | Promo & Koleksi Baru | IG + TikTok | Video pendek + Story/Status | Hari Guru + gajian: ide hadiah pashmina untuk guru; [isi: promo gajian jika ada] — jika tidak ada promo, tampilkan koleksi harga normal | Hadiah kecil untuk guru tercinta | Cek keranjang kuning / link Shopee di bio | Belum |
| 26 | 26 Nov 2026 | Kamis |  | Di Balik Layar | IG + TikTok | Video pendek proses | Di balik layar: sesi foto produk pakai HP di rumah | Foto produk cuma pakai HP | Follow untuk tips lainnya | Belum |
| 27 | 27 Nov 2026 | Jumat |  | Promo & Koleksi Baru | IG + TikTok | Video pendek + Story/Status | 3 produk yang paling sering dibeli bulan ini menurut laporan penjualan toko sendiri [isi: nama 3 produk dari data toko] | Tiga yang paling sering dibeli | Cek keranjang kuning / link Shopee di bio | Belum |
| 28 | 28 Nov 2026 | Sabtu |  | OOTD Mix-Match | IG + TikTok | Video try-on / mix-match | OOTD akhir pekan: pashmina + gamis polos untuk arisan | Siap arisan dalam 5 menit | Tag teman arisanmu | Belum |

📥 Versi CSV: `kalender_nura.csv` (pemisah `;` untuk Excel berbahasa Indonesia, UTF-8 BOM). Untuk Google Sheets, minta versi pemisah koma.

💡 Tips eksekusi:
- Rekam 6–8 video sekaligus tiap Sabtu (try-on & tutorial), sisanya tinggal diunggah sesuai tanggal.
- Siapkan foto flat-lay semua warna pashmina sekali di awal bulan untuk dipakai berulang.
- Mulai "pemanasan" 11.11 di Story tanggal 9–10 **tanpa** hard-selling di tanggal 10 (Hari Pahlawan).
- Cek Insight IG & Analytics TikTok setelah 2 minggu untuk menyesuaikan jam posting (titik awal: ±11.30–13.00 dan ±19.00–21.00).
- Mau saya buatkan caption lengkap untuk tanggal 11 dan 25? (pakai skill `caption-sosmed-umkm`)

📝 Asumsi: gajian hanya tanggal 25 (sesuai pengguna, bukan default 25 & 1); promo hanya 11.11 — hari berpilar "Promo & Koleksi Baru" lainnya diisi
koleksi/restock **dengan harga normal**, tanpa diskon karangan; tanggal 25 (Hari Guru + gajian) diberi `[isi: promo gajian jika ada]`; mekanisme kampanye
11.11 di Shopee dicek di jadwal resmi; semua ulasan/foto pembeli dipakai **dengan izin**.

## Catatan penguji
- **Tanggal & nama hari diverifikasi independen** dengan rumus Zeller (tanpa `datetime`): 30/30 baris benar (1 Nov 2026 = Minggu, 30 Nov = Senin).
- **Tidak ada promo di hari peringatan:** 10 Nov (Hari Pahlawan) otomatis diberi pilar non-promo dan ide penghormatan tanpa jualan ✔.
- Porsi promo 7/30 = 23% (dalam rentang 20–30%). Hook semua ≤ 10 kata (dicek script). Tidak ada klaim "terlaris" — hari ke-27 memakai
  "paling sering dibeli menurut data toko" dengan `[isi: …]`.
- **Kurang:** (1) script memberi pilar promo ke **tanggal tua** 21 Nov (rotasi biasa), padahal references §2 bilang tanggal tua "bukan hard-selling";
  agent harus mengubah isinya sendiri menjadi konten nilai. (2) Kolom Format "Video pendek + Story/**Status**" tetap muncul walau platform tanpa WA Status (ringan).
