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
| Momen khusus (promo toko, ulang tahun toko, Ramadan/Lebaran/Imlek tahun itu) | Tidak | Momen tanggal tetap + Ramadan/Idulfitri/Imlek dari tabel perkiraan script (berlabel "perkiraan"); hari besar lain tidak ditebak |
| Kemampuan produksi (mis. hanya sanggup 3 video/minggu) | Tidak | IG/TikTok 1 konten/hari, WA Status harian |
| Format hasil | Tidak | Tabel ringkas di chat + file `kalender.csv` / `kalender.md` (lengkap) |

Jika info wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor). Jika pengguna ingin cepat,
pakai default dan sebutkan asumsinya di akhir.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
0. **Tulis "Fakta dari pengguna" dulu (wajib).** Daftar butir yang *benar-benar* disebut pengguna, dengan
   kata-kata pengguna (usaha, produk, harga, layanan seperti "bisa antar jemput", cara order, kota, kemampuan
   produksi, promo, tanggal khusus). Setiap klaim layanan/produk/promo, angka, dan **tanggal** di kalender,
   tips, dan catatan harus bisa ditelusuri ke daftar ini **atau ke output script**; selain itu `[isi: ...]`.
   Simpan salinan persis pesan pengguna sebagai `fakta.txt` untuk langkah 4.
1. **Baca `references/momen-dan-pilar.md`**: pilih 4–5 pilar sesuai jenis usaha (promo maks. ±30%),
   kenali momen di periode itu. Ramadan/Idulfitri/Imlek **tidak ditebak dan tidak dihitung sendiri**: script
   otomatis mengambilnya dari tabel perkiraan (sama dengan references, berlabel "perkiraan, menunggu sidang
   isbat / cek SKB 3 Menteri"). Bila pengguna memberi tanggalnya, pakai `--awal-ramadan` / `--idulfitri` /
   `--imlek`. Tahun di luar tabel → minta tanggal ke pengguna atau `[isi: tanggal]`. Jangan pernah menulis bahwa
   tanggal "sudah dicek" kecuali pengguna memberi sumbernya.
   **Satu-satunya sumber tanggal hari besar = kolom Momen dari script.** Tanggal yang disebut di tips, catatan,
   dan ringkasan wajib disalin dari tabel (bukan nomor baris, bukan ingatan).
> **Alur ringan (wajib, agar balasan tidak kena batas waktu):** script dipanggil **2 kali saja** — kerangka
> (langkah 2) dan finalisasi (langkah 4). Jangan menulis JSON besar, jangan mengekspor md/csv/cek terpisah, dan
> jangan menulis ulang seluruh kalender di chat: tabel chat dicetak oleh script.

2. **Buat kerangka tanggal** (sekali; path relatif terhadap folder SKILL.md ini; Windows: `python`/`py`):
   ```bash
   python3 <folder-skill-ini>/scripts/buat_kalender.py --mulai 2026-10-01 --hari 31 \
     --pilar "Menu & Promo,Proses Dapur,Ulasan Pelanggan,Tips Kopi,Hiburan" --platform "IG,TikTok,WA Status" \
     --momen "2026-10-17:Ulang tahun kedai ke-3:promo" --format ringkas
   ```
   Platform = yang disebut pengguna saja (tidak disebut → default, dan tulis di Asumsi).
   Script mengisi tanggal, nama hari, momen (tanggal kembar, Harbolnas, gajian, tanggal tua, hari nasional,
   dan — bila periode menyentuhnya — "Ramadan hari ke-N", Nuzulul Qur'an, 10 malam terakhir, batas THR ±H-7,
   H-1, Idulfitri, Lebaran H+1, Pasca-Lebaran, Imlek), dan rotasi pilar: hari promo dipaksa ke pilar promo; hari
   peringatan (30 Sep, 1 Okt, 10 Nov), Idulfitri & H+1, dan tanggal tua tidak pernah diberi pilar promo. Jika
   momen promo pengguna jatuh di hari peringatan, script menulis PERINGATAN — sampaikan dan sarankan geser tanggal.
   **Momen dari script tidak boleh dihapus atau diganti**; ide di hari Ramadan harus nyambung dengan fasenya
   (sahur/buka, THR, 10 malam terakhir, persiapan Lebaran). Nama pilar promo harus mengandung "Promo" atau "Jual".
3. **Tulis isian ringan `isi.txt`** — satu baris per hari, **tanpa** mengulang tanggal/momen/pilar:
   ```
   No | Format | Ide Konten | Hook / Judul | CTA
   1 | Video IG+TikTok | Video tangan Bu Sari mengoles selai ke adonan nastar | Nastar buat meja Lebaranmu | Order lewat WA
   2 | Foto IG saja | Foto toples nastar Rp95.000 dari atas, latar kain batik | Satu toples, satu meja tamu | Order lewat WA
   ```
   Format `-` = format bawaan kerangka. Tulis per blok **±10 baris per tulis/append** (jangan satu tulisan
   raksasa). Ide ≤ 15 kata, hook ≤ 10 kata, CTA sesuai cara order pengguna; spesifik untuk produk pengguna dan bisa
   dibuat dengan HP. Jangan memakai tanda `|` di dalam teks.
   **Dilarang mengarang** (script menandai GAGAL): urgensi/kelangkaan ("stok terbatas", "hari terakhir"), rasa/
   tekstur/isi ("renyah", "lumer", "isi nanasnya padat"), cara buat ("dicetak satu-satu", "handmade"), janji kirim/
   jadwal toko ("besok dikirim", "pre-order dibuka", "toko libur", "sudah buka lagi"), layanan ("gratis ongkir",
   "tanpa minimal"), testimoni/angka — kecuali disebut pengguna. Yang belum diketahui → `[isi: ...]`.
   Jika kemampuan produksi terbatas (mis. 2 video/minggu), hanya hari terpilih yang "Video", sisanya "Foto/Story saja".
   Tulis juga `catatan.txt`: 3–5 tips eksekusi + Asumsi (default yang dipakai: gajian, platform, promo `[isi]`).
   Tanggal hari besar di catatan **disalin dari kerangka**, bukan dari ingatan atau nomor baris.
4. **Finalisasi — SATU perintah** (argumen kerangka sama seperti langkah 2):
   ```bash
   python3 <folder-skill-ini>/scripts/buat_kalender.py --mulai 2026-10-01 --hari 31 --pilar "..." --platform "..." \
     --momen "..." --isi isi.txt --catatan catatan.txt --fakta-file fakta.txt \
     --judul "Kalender Konten Kedai Kopi Lereng" --pemisah ";" --selesai hasil-kalender
   ```
   Script menyimpan `hasil-kalender/kalender.md` (tabel lengkap 11 kolom), `kalender.csv` (UTF-8 BOM; `;` untuk
   Excel Indonesia, `,` untuk Google Sheets), dan `ringkas.md`, mencetak **tabel ringkas untuk chat** (1 baris per
   hari + Hook & CTA 3 hari pertama), lalu cek-silang: klaim karangan per baris, tanggal hari besar di tabel &
   catatan, dan Ramadan yang hilang. Bila `HASIL: GAGAL`, perbaiki **hanya** baris/kalimat yang disebut (edit
   kecil), lalu jalankan perintah yang sama **sekali lagi** (maks. 2 kali ulang). Bagian "CEK-SILANG" tidak
   ditempel ke pengguna.
   (Masih didukung: `--isi kalender.json` hasil `--format json`, dan `--cek-teks jawaban.md`.)
5. **Jika Python tidak bisa dijalankan:** susun tanggal & nama hari manual (cek hari pertama dengan
   kalender), tandai momen dari references, rotasi pilar berurutan, lalu tulis tabel ringkas yang sama sendiri dan
   tawarkan CSV. Beri tahu pengguna bahwa tanggal dicek manual, dan cek manual dengan "Cek-silang fakta" di bawah.
6. **Kirim jawaban:** tempel tabel ringkas dari output script + tips + Asumsi + lokasi file. Caption lengkap
   **tidak** ditulis kecuali diminta; bila diminta, maksimal 3–5 hari per balasan (mulai hari pertama atau hari
   yang diminta), sisanya ditawarkan.
7. Tutup dengan 3–5 tips eksekusi (batch produksi konten di akhir pekan, siapkan stok foto, cek
   Insight/Analytics untuk jam posting) dan tawarkan membuat caption lengkap untuk hari tertentu.

## Format output
Chat (dicetak script lewat `--selesai`, ditempel apa adanya):
```
## Kalender Konten <nama usaha> — <tgl mulai> s.d. <tgl selesai>
Pilar: <pilar 1> (x hari), ...  | Platform: ...

| No | Tanggal | Hari | Momen | Format | Ide Konten |
|---|---|---|---|---|---|
| 1 | 01 Okt 2026 | Kamis | ... | ... | ... |
... (semua hari, 1 baris per hari, jangan dipotong)

Hook & CTA 3 hari pertama (semua hari ada di file): ...
📥 File: hasil-kalender/kalender.csv (+ kalender.md tabel lengkap)
💡 Tips eksekusi: ...
📝 Asumsi: ...
```
File `kalender.md`/`.csv` berisi 11 kolom lengkap: No, Tanggal, Hari, Momen, Pilar, Platform, Format, Ide Konten,
Hook / Judul, CTA, Status. Jangan menyingkat dengan "dst." — pengguna butuh semua hari.

## Contoh
**Input pengguna:** "Tolong bikin kalender konten Oktober 2026 buat Kedai Kopi Lereng di Malang, jual
kopi susu gula aren 18 ribu dan biji kopi arabika Malang. Order lewat GoFood/GrabFood dan WA. Tanggal 17
ulang tahun kedai ke-3, ada promo beli 2 gratis 1."

**Output (cuplikan isi `kalender.md`; di chat tampil versi ringkas 6 kolom):**
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

## Cek-silang fakta (wajib, sebelum mengirim)
- [ ] Setiap tanggal hari besar di tabel, tips, catatan, dan asumsi **sama persis** dengan kolom Momen script (tidak memakai nomor baris sebagai tanggal)
- [ ] Bila periode mencakup Ramadan: label "Ramadan hari ke-N" ada di kolom Momen, tidak diganti "Tanggal tua", dan ide memakai fase Ramadan/THR/Lebaran
- [ ] Layanan/syarat (gratis antar-jemput, tanpa minimal, express), promo, testimoni, angka — masing-masing punya butir di "Fakta dari pengguna"; selain itu `[isi: ...]`
- [ ] Tidak ada rasa/tekstur, cara buat, janji kirim, atau jadwal buka/tutup toko yang tidak disebut pengguna
- [ ] Platform yang tidak disebut pengguna tercantum di Asumsi
- [ ] `--selesai` menulis `HASIL: LULUS` (atau cek manual sudah dilakukan dan disebut ke pengguna)

## Checklist sebelum mengirim hasil
- [ ] Jumlah baris = jumlah hari; tanggal & nama hari dari script (atau dicek manual)
- [ ] Tiap baris punya ide spesifik, hook, dan CTA; tidak ada "dst."
- [ ] Porsi promo ±20–30% (script memberi peringatan bila > 40%); hari peringatan tanpa hard-selling
- [ ] Momen bertanggal tidak tetap diberi label "(perkiraan, menunggu sidang isbat / cek SKB 3 Menteri)" atau dari pengguna; tidak ada klaim "sudah dicek" tanpa sumber
- [ ] Tidak ada urgensi/kelangkaan palsu di CTA ("stok terbatas", "hari terakhir") kecuali dari pengguna
- [ ] Tidak ada klaim yang tidak diberikan pengguna (halal, BPOM, terlaris) dan promo yang tidak disebut pengguna ditandai `[isi: ...]`
- [ ] Konten yang memakai foto/ulasan pelanggan diberi catatan "dengan izin"
- [ ] File CSV disebut lokasinya, dengan pemisah sesuai aplikasi pengguna
- [ ] Script hanya dipanggil untuk kerangka + finalisasi (+ maks. 2 ulang bila GAGAL)

## Batasan & penanganan error
- Skill tidak memposting otomatis dan tidak membaca statistik akun; jam posting hanya saran awal.
- Kampanye marketplace (tanggal kembar, Harbolnas) berubah tiap tahun → selalu label "cek kampanye/jadwal resmi".
- Script menolak tanggal tidak valid, jumlah hari di luar 7–92, pilar < 2 atau duplikat, JSON rusak, dan baris `isi.txt` yang kolomnya bukan 4/5 atau nomornya di luar periode,
  dengan pesan bahasa Indonesia. Perbaiki input lalu jalankan ulang.
- Periode lebih dari 31 hari boleh (maks. 92) tapi sarankan dipecah per bulan agar ide tetap segar.
