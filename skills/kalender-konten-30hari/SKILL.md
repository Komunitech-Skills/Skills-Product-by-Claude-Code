---
name: kalender-konten-30hari
description: Menyusun rencana konten 30 hari (Instagram, TikTok, WA Status) yang disesuaikan jenis usaha, dengan pilar konten, momen lokal Indonesia (gajian, tanggal tua, tanggal kembar 9.9–12.12/Harbolnas, Ramadan–Lebaran, hari nasional), ide, hook, dan CTA per hari — output tabel siap tempel ke spreadsheet plus opsi CSV. Gunakan saat pengguna minta kalender konten, jadwal posting, content plan/planner sebulan, atau ide konten harian (content calendar, social media plan, posting schedule). Bukan untuk menulis satu caption (pakai caption-sosmed-umkm).
---

# Kalender Konten 30 Hari

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Memberi pemilik usaha rencana posting sebulan penuh yang sudah jelas "hari ini posting apa", seimbang
antara jualan dan konten bernilai, dan memanfaatkan momen lokal — dalam bentuk tabel yang bisa langsung
ditempel ke Google Sheets/Excel.

## Kapan digunakan
- "Buatin content plan IG & TikTok bulan depan buat warung kopi saya"
- Menyiapkan jadwal konten menjelang 11.11/12.12, Ramadan, atau ulang tahun toko
- Tim/admin sosmed butuh daftar tugas harian yang bisa dicentang

## Kapan TIDAK digunakan
- Menulis caption lengkap satu posting → `caption-sosmed-umkm` (tawarkan setelah kalender jadi)
- Naskah live → `naskah-live-jualan`; pesan broadcast WA → `broadcast-wa`
- Laporan performa/analitik akun (skill ini membuat rencana, bukan analisis data)

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Jenis usaha & produk/jasa utama | Ya | — (tanyakan) |
| Periode (tanggal mulai) | Tidak | Tanggal 1 bulan depan, 30 hari. Jika pengguna menyebut nama bulan, pakai jumlah hari bulan itu (`--hari 31` untuk Oktober) |
| Platform | Tidak | IG + TikTok + WA Status |
| Target pembeli & kota | Tidak | Disimpulkan dari jenis usaha, disebut sebagai asumsi |
| Pilar konten | Tidak | Dari tabel jenis usaha di `references/momen-dan-pilar.md` |
| Tanggal gajian pelanggan | Tidak | Tanggal 25 dan 1 |
| Momen khusus (promo toko, ulang tahun toko, Ramadan/Lebaran/Imlek tahun itu) | Tidak | Hanya momen tanggal tetap; tanggal yang berubah tiap tahun tidak ditebak |
| Kemampuan produksi (mis. hanya sanggup 3 video/minggu) | Tidak | IG/TikTok 1 konten/hari, WA Status harian |
| Format hasil | Tidak | Tabel markdown + tawaran CSV |

Jika info wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor). Jika pengguna ingin cepat,
pakai default dan sebutkan asumsinya di akhir.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
1. **Baca `references/momen-dan-pilar.md`**: pilih 4–5 pilar sesuai jenis usaha (promo maks. ±30%),
   kenali momen di periode itu. Ramadan/Lebaran/Imlek dll. **tidak ditebak**: minta tanggalnya, atau
   tulis "(perkiraan, menunggu sidang isbat / cek SKB 3 Menteri)" memakai tabel di references (mis. awal Ramadan 2027 ±8 Feb 2027). Jangan pernah menulis bahwa tanggal "sudah dicek" kecuali pengguna memberi sumbernya; periksa konsistensi Ramadan–Idulfitri (29/30 hari).
2. **Buat kerangka tanggal** dengan script (path relatif terhadap folder SKILL.md ini; Windows: `python`/`py`):
   ```bash
   python3 <folder-skill-ini>/scripts/buat_kalender.py --mulai 2026-10-01 --hari 31 \
     --pilar "Menu & Promo,Proses Dapur,Ulasan Pelanggan,Tips Kopi,Hiburan" --platform "IG,TikTok,WA Status" \
     --momen "2026-10-17:Ulang tahun kedai ke-3:promo" --format json
   ```
   Script mengisi tanggal, nama hari, momen (tanggal kembar, Harbolnas, gajian, tanggal tua, hari nasional),
   dan rotasi pilar: hari promo dipaksa ke pilar promo; hari peringatan (30 Sep, 1 Okt, 10 Nov) dan
   tanggal tua tidak pernah diberi pilar promo. Jika momen promo pengguna jatuh di hari peringatan, script
   **tidak** menjadwalkannya sebagai promo dan menulis PERINGATAN — sampaikan ke pengguna dan sarankan geser tanggal.
   Di hari peringatan, isi dengan konten penghormatan/edukasi, bukan testimoni jualan. Nama pilar promo harus mengandung kata "Promo" atau "Jual" agar dikenali.
3. **Isi kolom Ide Konten, Hook / Judul, CTA** untuk setiap baris: spesifik untuk produk pengguna
   (bukan "posting produk"), sesuai pilar & momen, dan realistis untuk UMKM (bisa dibuat dengan HP).
   Hook ≤ 10 kata. CTA sesuai cara order pengguna. Boleh ubah pilar satu hari bila momen menuntut.
   **Dilarang** urgensi/kelangkaan palsu di hook, ide, dan CTA ("stok terbatas", "hari terakhir", "buruan sebelum kehabisan", "harga belum naik") dan testimoni/angka karangan, kecuali fakta itu diberikan pengguna. Syarat layanan yang tidak diberikan ("tanpa minimal", "gratis jemput") ditulis `[isi: ...]`.
   Jika kemampuan produksi terbatas (mis. 3 video/minggu), tandai hari sisanya "WA Status/Story saja"
   di kolom Format — jangan membuat rencana yang tidak sanggup dijalankan.
4. **Ekspor**: simpan hasil isian sebagai JSON (bentuk sama dengan output `--format json`), lalu:
   ```bash
   python3 <folder-skill-ini>/scripts/buat_kalender.py --isi kalender.json --format md
   python3 <folder-skill-ini>/scripts/buat_kalender.py --isi kalender.json --format csv --pemisah ";" --output kalender.csv
   ```
   `--isi` menghitung ulang nama hari dan momen dari tanggal, memberi tanda baris yang idenya masih kosong,
   dan memberi PERINGATAN bila ada promo/diskon di hari peringatan atau pilar promo di tanggal tua
   (sertakan `--momen` & `--gajian` yang sama seperti langkah 2). Perbaiki barisnya sebelum menyerahkan hasil.
   Pemisah `;` untuk Excel berbahasa Indonesia, `,` untuk Google Sheets. File CSV disimpan UTF-8 (BOM)
   agar emoji/huruf terbaca di Excel.
5. **Jika Python tidak bisa dijalankan:** susun tanggal & nama hari manual (cek hari pertama dengan
   kalender), tandai momen dari references, rotasi pilar berurutan, lalu tulis tabel/CSV sendiri
   (bungkus sel yang berisi pemisah dengan tanda kutip). Beri tahu pengguna bahwa tanggal dicek manual.
6. Tutup dengan 3–5 tips eksekusi (batch produksi konten di akhir pekan, siapkan stok foto, cek
   Insight/Analytics untuk jam posting) dan tawarkan membuat caption lengkap untuk hari tertentu.

## Format output
```
## Kalender Konten <nama usaha> — <tgl mulai> s.d. <tgl selesai>
Pilar: <pilar 1> (x hari), <pilar 2> (x hari), ...  | Platform: ...

| No | Tanggal | Hari | Momen | Pilar | Platform | Format | Ide Konten | Hook / Judul | CTA | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 01 Okt 2026 | Kamis | ... | ... | ... | ... | ... | ... | ... | Belum |
... (semua hari, jangan dipotong)

📥 Versi CSV: <blok ```csv``` atau nama file hasil --output>
💡 Tips eksekusi: ...
📝 Asumsi: ...
```
Jangan menyingkat tabel dengan "dst." — pengguna butuh semua hari.

## Contoh
**Input pengguna:** "Tolong bikin kalender konten Oktober 2026 buat Kedai Kopi Lereng di Malang, jual
kopi susu gula aren 18 ribu dan biji kopi arabika Malang. Order lewat GoFood/GrabFood dan WA. Tanggal 17
ulang tahun kedai ke-3, ada promo beli 2 gratis 1."

**Output (cuplikan):**
```
| No | Tanggal | Hari | Momen | Pilar | Platform | Format | Ide Konten | Hook / Judul | CTA | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 01 Okt 2026 | Kamis | Hari Kesaktian Pancasila; Hari gajian (tgl 1) — hari peringatan... | Proses Dapur | IG + TikTok + WA Status | Video pendek proses | Video tenang proses menyeduh arabika Malang pagi hari; tanpa promo karena hari peringatan | Pagi yang tenang di Kedai Lereng | Mampir pagi ini | Belum |
| 2 | 02 Okt 2026 | Jumat | Hari Batik Nasional | Ulasan Pelanggan | IG + TikTok + WA Status | Foto ulasan / Story | Foto pelanggan berbatik yang ngopi di kedai + kutipan ulasannya (dengan izin) | Hari Batik, ngopinya juga rapi | Tag teman kantormu | Belum |
| 10 | 10 Okt 2026 | Sabtu | Tanggal kembar 10.10 — musim promo akhir tahun | Menu & Promo | IG + TikTok + WA Status | Video pendek + Story/Status | [isi: promo 10.10 jika ada]. Jika tidak ada: video "menu favorit malam minggu" | Malam minggu ngopi apa? | Order lewat WA/GoFood | Belum |
| 17 | 17 Okt 2026 | Sabtu | Ulang tahun kedai ke-3 | Menu & Promo | IG + TikTok + WA Status | Video pendek + Story/Status | Video terima kasih 3 tahun + promo beli 2 gratis 1 (syarat & batas waktu ditulis jelas) | 3 tahun, makasih Arek Malang! | Datang langsung / order WA | Belum |
| 28 | 28 Okt 2026 | Rabu | Hari Sumpah Pemuda | Tips Kopi | IG + TikTok + WA Status | Carousel / video tips | Carousel "kenalan sama arabika Malang": asal, rasa, cara seduh — bangga kopi lokal | Kopi lokal, dari lereng ke gelasmu | Simpan & bagikan ke teman | Belum |
```
📝 Asumsi: gajian tgl 25 & 1; promo 10.10 belum ditentukan pengguna sehingga diberi alternatif non-promo.

## Checklist sebelum mengirim hasil
- [ ] Jumlah baris = jumlah hari; tanggal & nama hari dari script (atau dicek manual)
- [ ] Tiap baris punya ide spesifik, hook, dan CTA; tidak ada "dst."
- [ ] Porsi promo ±20–30% (script memberi peringatan bila > 40%); hari peringatan tanpa hard-selling
- [ ] Momen bertanggal tidak tetap diberi label "(perkiraan, menunggu sidang isbat / cek SKB 3 Menteri)" atau dari pengguna; tidak ada klaim "sudah dicek" tanpa sumber
- [ ] Tidak ada urgensi/kelangkaan palsu di CTA ("stok terbatas", "hari terakhir") kecuali dari pengguna
- [ ] Tidak ada klaim yang tidak diberikan pengguna (halal, BPOM, terlaris) dan promo yang tidak disebut pengguna ditandai `[isi: ...]`
- [ ] Konten yang memakai foto/ulasan pelanggan diberi catatan "dengan izin"
- [ ] Opsi CSV ditawarkan, dengan pemisah sesuai aplikasi pengguna

## Batasan & penanganan error
- Skill tidak memposting otomatis dan tidak membaca statistik akun; jam posting hanya saran awal.
- Kampanye marketplace (tanggal kembar, Harbolnas) berubah tiap tahun → selalu label "cek kampanye/jadwal resmi".
- Script menolak tanggal tidak valid, jumlah hari di luar 7–92, pilar < 2 atau duplikat, dan JSON rusak,
  dengan pesan bahasa Indonesia. Perbaiki input lalu jalankan ulang.
- Periode lebih dari 31 hari boleh (maks. 92) tapi sarankan dipecah per bulan agar ide tetap segar.
