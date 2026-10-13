---
name: konten-mingguan
description: Menyusun paket konten media sosial 1 minggu (5-7 hari) untuk UMKM/usaha kecil maupun profesional/B2B — per hari: platform, pilar, hook 3 detik, caption siap tempel, naskah video singkat, brief foto/video, hashtag, CTA, dan jam posting — dari profil usaha yang disimpan sekali dan momen minggu itu (gajian, tanggal kembar, hari besar). ATURAN PERTAMA: SELURUH paket post (semua hari, caption lengkap) WAJIB ditulis di balasan chat; file hanya salinan opsional. Dilarang mengarang fakta usaha (promo, harga, kelangkaan, proses, durasi, pengiriman, jam/hari libur, kepopuleran, sterilisasi, sertifikat) yang tidak diberikan pengguna: pakai [isian]. TIDAK memposting otomatis. Bila sebagian permintaan dilarang (testimoni pasien, before-after, diskon tindakan medis klinik): tolak bagian itu (1-2 kalimat + dasar aturan) lalu LANGSUNG serahkan paket pengganti lengkap di balasan yang sama, tanpa tanya izin. Pakai untuk paket konten minggu ini/depan, weekly content plan/pack (sebulan: minta per minggu, 4 paket berurutan).
---

# Konten Mingguan

> **ATURAN PERTAMA (mengalahkan semua yang lain):** SELURUH paket post (setiap hari: hook, caption lengkap, hashtag, CTA, brief) WAJIB ditulis di balasan chat ini juga. Pengguna (mis. Telegram) tidak bisa membuka file. **Jangan menulis file sama sekali kecuali pengguna memintanya**; bila ditulis, file hanya salinan, dibuat SETELAH paket tampil di chat. DILARANG menulis "sudah tampil di atas/di chat di atas/terlampir" kecuali paketnya memang ada di balasan itu. Balasan yang hanya berisi ringkasan, penolakan, atau "tersimpan di file" = GAGAL.
> **Dilarang mengarang fakta usaha (tegas):** SEMUA fakta tentang usaha ini (layanan/produk, proses & cara membuat, durasi, satuan harga, harga, promo, kelangkaan, pengiriman/antar/COD, jam buka & hari libur, kepopuleran/"favorit"/"pasien kami", alat/bahan, sterilisasi, sertifikat/izin) HANYA boleh ditulis bila diberikan pengguna; selain itu tulis `[isian: ...]` atau kalimat umum yang tidak mengklaim fakta. Edukasi umum yang benar untuk semua usaha sejenis boleh.
> - Boleh: "scaling dianjurkan berkala sesuai saran dokter gigi", "Pesan lewat WA" (bila cara order diberikan), "Brownies Rp45.000" (persis seperti diberikan).
> - Tidak boleh (kecuali diberikan pengguna): "alat steril", "scaling 30-60 menit", "pasien kami", "dibuat sesuai pesanan/fresh/handmade", "favorit pelanggan", "Rp45.000 per loyang", "bisa diantar", "Minggu libur", tips simpan kue, "slot/stok terbatas", "tanpa pengawet".
> - Asumsi yang terpaksa dipakai (hari libur, satuan harga, jam tayang, cara pembuatan) WAJIB dicantumkan di daftar asumsi di akhir; lebih baik tidak dipakai.
> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Memberi pemilik usaha paket konten **satu minggu**, siap tempel per hari, tanpa harus memikirkan ide dari
nol setiap minggu — memanfaatkan profil usaha yang sudah tersimpan dan momen minggu itu (gajian, tanggal
kembar, hari besar). Skill ini **hanya menyiapkan**; pengguna sendiri yang menjadwalkan/memposting lewat
aplikasi resmi tiap platform.

## Kapan digunakan
- "Buatkan paket konten minggu ini/minggu depan buat toko saya"
- "Tiap Jumat sore kirimi saya paket konten minggu depan" (lihat `references/openclaw-jadwal.md` untuk versi terjadwal di OpenClaw)
- Sudah ada `konten/PROFIL.md` dan pengguna minta "lanjutkan minggu berikutnya"

## Kapan TIDAK digunakan
- Rencana sebulan penuh (30 hari) sekaligus → kerjakan per minggu: paket minggu ke-1, lalu "lanjutkan minggu berikutnya"
- Hanya satu caption untuk satu posting → tidak perlu paket mingguan; tulis langsung satu caption dengan aturan di `references/gaya-caption.md`
- Rencana kampanye promo (mekanisme diskon, cek margin) → `promo-kalender`
- Shot list foto/video detail per produk → `foto-produk-brief`
- Naskah live selling → `naskah-live-jualan`
- Memposting langsung ke akun media sosial → **skill ini tidak bisa dan tidak akan melakukan ini** (lihat Batasan)

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Profil usaha (`konten/PROFIL.md`) | Ya | Belum ada → wawancara **sekali** pakai daftar di `templates/PROFIL.md` (boleh dijawab ringkas); simpan hasilnya ke `konten/PROFIL.md`. Pengguna ingin cepat → isi kolom kosong dengan asumsi wajar dan sebutkan di akhir — **kecuali field yang TIDAK boleh didefault** (lihat catatan di bawah) |
| Minggu yang dimaksud | Tidak | Minggu depan (Senin berikutnya) dari hari ini |
| Jumlah konten | Tidak | 6 hari (Senin-Sabtu; Minggu istirahat) |
| Promo/momen khusus minggu ini | Tidak | Hanya momen otomatis (gajian, tanggal kembar, hari besar tetap dari script); momen bertanggal berubah (Ramadan/Lebaran/Imlek, libur sekolah) **tidak ditebak** |

Jika `PROFIL.md` belum ada dan pengguna belum menjawab, tanyakan **sekali** dalam satu pesan (maks. 5
pertanyaan bernomor): jenis usaha & produk utama, target pembeli, platform (sebut juga LinkedIn/X bila
usaha ini jasa profesional/B2B), cara order, dan apakah ada klaim BPOM/PIRT/halal yang **benar-benar
dimiliki**. Simpan jawaban ke `konten/PROFIL.md` (salin dari `templates/PROFIL.md`) supaya minggu
berikutnya tidak ditanya ulang.

**Field yang TIDAK boleh didefault, walau pengguna minta "pakai default aja/cepat aja":** nama usaha,
produk/jasa yang dijual, dan harga. Ini fakta spesifik milik pengguna, bukan asumsi gaya/nada yang wajar
ditebak — tanpa ini hasilnya jadi generik atau bahkan salah (harga karangan bisa menyesatkan pembeli).
Kalau info ini benar-benar belum ada, tulis placeholder eksplisit seperti `[nama usaha]`/`[isi harga]` di
hasil dan minta pengguna melengkapinya sebelum dipakai — jangan mengarang angka atau nama.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
1. **Baca atau buat `konten/PROFIL.md`.** Kalau sudah ada, pakai isinya. Kalau belum, wawancara singkat
   (lihat Input), lalu tulis file itu dari `templates/PROFIL.md`. Perhatikan kolom "Larangan klaim" —
   ini menentukan apa yang **tidak boleh** ditulis di konten minggu ini.
2. **Hitung kerangka minggu** (path relatif terhadap folder SKILL.md ini; Windows: `python`/`py`):
   ```bash
   python3 <folder-skill-ini>/scripts/nomor_minggu.py --format json
   # minggu tertentu: --mulai 2026-10-05 (harus tanggal Senin)
   # gajian bukan tgl 25/1: --gajian-tanggal 20,5
   ```
   Script mengembalikan 7 hari (Senin-Minggu) dengan tanggal, nama hari, dan momen otomatis (gajian,
   tanggal kembar 1.1-12.12/Harbolnas, hari besar nasional bertanggal tetap). **Jangan menghitung
   tanggal sendiri.** Momen yang tanggalnya berubah tiap tahun (Ramadan, Lebaran, Imlek, Idul Adha,
   libur sekolah) tidak ada di output script — tanyakan ke pengguna atau tulis label
   **"(perkiraan — cek SKB 3 Menteri/kalender resmi tahun berjalan)"** bila disebutkan tanpa kepastian.
3. **Pilih 5-7 hari** sesuai kapasitas produksi di `PROFIL.md` (default 6: Senin-Sabtu). Prioritaskan
   hari bermomen (gajian, tanggal kembar, hari besar relevan produk) untuk pilar promo; hari peringatan
   (mis. Hari Pahlawan, G30S) **tidak** diberi pilar promo/hard-selling — isi edukasi/apresiasi.
4. **Tentukan pilar & platform per hari.** Campur pilar (jangan promo setiap hari — target ±20-30%
   seperti di `promo-kalender`) dan format sesuai platform aktif di `PROFIL.md`
   (Reels/TikTok untuk video pendek, Feed untuk foto rapi, Story/WA Status untuk info cepat/promo harian,
   **LinkedIn Post/Carousel** untuk konten profesional/B2B, **X/Twitter** untuk update singkat/thread).
5. **Isi tiap hari** dengan `templates/paket-mingguan.md` sebagai kerangka:
   - **Momen**: salin **SEMUA** entri momen hari itu dari output script (bisa lebih dari satu, mis.
     gajian + hari peringatan bersamaan) — jangan memilih sebagian, karena kombinasinya menentukan
     apakah hari itu boleh dipakai untuk pilar promo (lihat langkah 3).
   - **Hook 3 detik**: kalimat/pertanyaan pembuka, ≤ 12 kata, spesifik untuk produk (bukan generik).
   - **Caption siap tempel**: ikuti gaya & aturan panjang di tabel `references/gaya-caption.md`.
   - **Naskah video ±30 detik**: tabel detik-adegan-teks layar-VO, hanya untuk hari berformat video.
   - **Brief foto/video singkat**: 2-4 baris (sudut, cahaya, properti) — versi ringkas; untuk brief detail
     per produk, tawarkan `foto-produk-brief`.
   - **Hashtag**: 5-10 relevan (umum + niche + lokasi bila ada), **bukan** tempelan hashtag masal yang
     tidak nyambung produk.
   - **CTA**: sesuai cara order di `PROFIL.md`.
   - **Jam posting disarankan**: gunakan jam umum di `references/gaya-caption.md` per platform, tulis
     jelas **"perkiraan umum — cek Insights/Analytics akun sendiri untuk jam terbaik"**.
6. **Terapkan aturan iklan** dari `references/aturan-iklan.md` ke SETIAP hari: tanpa klaim menyembuhkan/
   jaminan untung/"terbaik no.1" tanpa bukti dari pengguna; produk kesehatan/kosmetik/keuangan/pangan →
   sisipkan peringatan singkat (cek BPOM/PIRT/OJK sesuai kategori); musik/gambar berhak cipta hanya yang
   diizinkan di `PROFIL.md`.
   **Izin edar:** bila produk pangan olahan/minuman, kosmetik, suplemen, atau obat tradisional/obat, ingatkan di awal paket (satu kalimat) bahwa izin edar BPOM / PIRT-SPP-IRT (atau sertifikat halal bila dicantumkan) harus ada **sebelum** dijual dan dipromosikan. Bila pengguna bilang izin "belum ada/masih proses", tampilkan peringatan ini lebih tegas dan jangan menulis klaim izin/BPOM di konten mana pun.
7. **Arsip file: hanya bila pengguna memintanya**, dan setelah paket lengkap tampil di chat: simpan ke `konten/minggu-<label_minggu>.md` (mis. `minggu-2026-W40.md`) memakai `templates/paket-mingguan.md`. Tanpa permintaan, jangan menulis file (tawarkan saja).
   **Tolak sebagian, serahkan semuanya (wajib):** bila permintaan memuat unsur terlarang (testimoni/before-after
   pasien, diskon tindakan medis, imbalan rujukan, klaim menyembuhkan, dsb.), tulis 1-2 kalimat penolakan + dasar
   aturannya di bagian atas, lalu **di balasan yang SAMA langsung serahkan paket lengkap pengganti yang aman**
   (default 5-6 hari, setiap hari lengkap: judul/topik, caption siap tempel, ide visual, hashtag, CTA, hari tayang).
   **DILARANG** berhenti di penolakan, hanya menawarkan daftar topik, atau bertanya "boleh saya lanjutkan?/mau
   dibuatkan yang aman?" — penolakan bukan alasan menunda hasil. Info yang kurang diisi placeholder/asumsi, bukan
   pertanyaan izin. Berlaku untuk SEMUA jenis usaha, bukan hanya klinik.
8. **Sampaikan ke pengguna** dalam format output di bawah. **Caption lengkap + hashtag + hook + CTA setiap hari WAJIB tampil di chat** (lihat ATURAN PERTAMA); file arsip bukan pengganti. Bila terlalu panjang, kirim bertahap per 2-3 hari, bukan dipangkas. Lalu lalu tawarkan: (a) automation mingguan +
   pengingat harian lewat OpenClaw (`references/openclaw-jadwal.md`), (b) buat brief foto detail lewat
   `foto-produk-brief`, (c) buat naskah live untuk salah satu hari lewat `naskah-live-jualan`.
9. **Jika Python tidak bisa dijalankan:** hitung tanggal manual dari kalender (Senin minggu depan dari
   hari ini), tandai tanggal kembar (tanggal = bulan) dan gajian (tgl 25 & 1) sendiri, beri tahu pengguna
   bahwa tanggal dihitung manual dan belum diverifikasi script.

## Format output
```
[Bila ada unsur terlarang: 1-2 kalimat "Tidak saya buatkan: <unsur> — <dasar aturan>", lalu LANGSUNG paket di bawah, tanpa pertanyaan izin]

# Paket Konten Minggu <label_minggu> — <nama usaha>
Periode: <Senin, tgl> s.d. <Minggu, tgl>  |  Platform: <daftar>

## <Hari> <tanggal> — <Platform>/<Format>
Pilar: <pilar>  |  Momen: <momen atau "-">  |  Jam disarankan: <jam> (perkiraan umum)
Hook 3 detik: "<hook>"
Caption:
<caption siap tempel>
Naskah video ±30 detik: <tabel ringkas atau "- (format foto, tidak perlu naskah)">
Brief foto/video: <2-4 baris>
Hashtag: <daftar>
CTA: <cta>
--- (ulangi per hari, 5-7 hari) ---

(Baris arsip HANYA bila pengguna meminta file: "📥 Salinan: konten/minggu-<label_minggu>.md")
📝 Asumsi: <daftar asumsi yang dipakai bila profil belum lengkap>
(Penutup HANYA pernyataan, bukan izin: satu kalimat asumsi + tawaran opsional. Jangan akhiri dengan "boleh saya lanjutkan?".)
⚠️ Ingat: paket ini belum terposting — jadwalkan sendiri lewat Meta Business Suite/TikTok Studio (lihat `references/jadwal-platform.md`), atau aktifkan pengingat harian OpenClaw.
```

## Contoh
**Input pengguna:** "Buatin paket konten minggu depan buat kedai kopi saya. Jual kopi susu gula aren 18rb,
order lewat WA/GoFood. Sanggup 2 video seminggu, sisanya foto/Story aja."

**Output (cuplikan, 1 dari 6 hari):**
```
## Kamis 01 Okt 2026 — WA Status/Story
Pilar: Promo Gajian  |  Momen: Hari gajian (tgl 1) — TAPI juga Hari Kesaktian Pancasila (peringatan):
konten dibuat non-hardselling, promo dipindah ke esok  |  Jam disarankan: 11.00 & 17.00 (perkiraan umum)
Hook 3 detik: "Gajian udah cair?"
Caption: "Rayakan gajian pertama bulan ini dengan ngopi santai. Kopi susu gula aren, tetap Rp18.000.
Order gampang lewat WA/GoFood ya! ☕"
Brief foto/video: foto gelas kopi dekat jendela, cahaya pagi, tanpa promo besar-besaran (hari peringatan)
Hashtag: #kopisusu #kedaikopi #gajian #ngopiyuk
CTA: Order lewat WA/GoFood
```
📝 Asumsi: profil belum lengkap → target pembeli disimpulkan "pekerja & mahasiswa sekitar kedai"; jam
posting pakai acuan umum WA Status siang & sore.

**Contoh permintaan sebagian terlarang (klinik):** "Buatin konten seminggu klinik gigi saya: testimoni pasien
+ before-after (pasien sudah izin) + diskon scaling 20% pasien baru."

**Output yang benar (cuplikan):**
```
Tidak saya buatkan testimoni pasien, before-after, dan diskon tindakan: iklan/publikasi pelayanan kesehatan
(Permenkes 1787/2010) melarangnya, walau pasien sudah izin (PERLU REVIEW tenaga medis/hukum). Ini paket 6 hari
pengganti yang aman, siap tempel:

## Senin 12 Okt 2026 — Instagram/Feed
Pilar: Edukasi  |  Momen: -  |  Jam disarankan: 19.00 (perkiraan umum)
Hook 3 detik: "Sikat gigi 2x sehari, tapi karang gigi tetap ada?"
Caption: "Karang gigi tidak hilang dengan sikat biasa. Pemeriksaan rutin tiap 6 bulan membantu ... Jadwal praktik &
booking: lihat bio."
Brief foto/video: foto ruang praktik rapi (tanpa pasien), cahaya terang.
Hashtag: #klinikgigi #sehatgigi #edukasigigi
CTA: Booking jadwal lewat WA
... (Selasa-Sabtu lengkap dengan format yang sama)
📝 Asumsi: nama klinik/jadwal praktik memakai placeholder [isi]; paket 6 hari (Senin-Sabtu) tanpa klaim hari libur klinik.
```
Salah: berhenti setelah penolakan dengan pertanyaan "boleh saya lanjutkan dengan konten edukasi?".

## Checklist sebelum mengirim hasil
- [ ] Tanggal & momen dari `nomor_minggu.py` (atau dihitung manual dengan keterangan jelas)
- [ ] Jumlah hari sesuai kapasitas produksi di `PROFIL.md`, bukan dipaksa 7 hari
- [ ] Hari peringatan/hari duka tidak diberi pilar promo/hard-selling
- [ ] Tidak ada klaim yang dilarang di `PROFIL.md` (BPOM/PIRT/halal/jaminan hasil/"terbaik no.1")
- [ ] Kategori sensitif (kesehatan/kosmetik/keuangan/pangan) diberi peringatan singkat
- [ ] Setiap caption punya hook, CTA, dan panjang sesuai platform
- [ ] Ditulis jelas bahwa paket ini **belum terposting** dan jam posting adalah **perkiraan**
- [ ] **Apakah semua post (setiap hari, caption lengkap) ada di balasan chat ini?** Bukan hanya di file. Jangan menulis "sudah tampil di atas" bila tidak
- [ ] Tidak ada promo/harga/combo/kelangkaan/klaim produksi karangan; semua dari pengguna atau `[isian]`
- [ ] Setiap klaim tentang usaha ini (layanan, proses, durasi, satuan, pengiriman, jam/hari libur, kepopuleran, sterilisasi, sertifikat) berasal dari pengguna atau `[isian]`?
- [ ] Semua asumsi (hari libur, satuan harga, jam tayang, minggu yang dipilih dan alasannya) tercantum di daftar asumsi akhir?
- [ ] Ejaan hashtag dicek huruf demi huruf (mis. `#klinikgigi`, bukan `#kliniktgigi`) dan nama usaha/kata baku benar
- [ ] File arsip hanya ditulis bila diminta, dan setelah chat
- [ ] Bila ada unsur terlarang: penolakan singkat + paket lengkap pengganti ada di balasan yang sama (tanpa pertanyaan izin)

## Batasan & penanganan error
- **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.
- **Skill ini TIDAK memposting** ke Instagram/TikTok/Facebook/WA dan tidak login ke akun media sosial
  mana pun. Permintaan "postingkan otomatis" atau "login-kan akun IG saya" **ditolak** — jelaskan bahwa
  paket dikirim ke pengguna untuk dijadwalkan sendiri (lihat `references/jadwal-platform.md`), dan
  tolak setiap permintaan otomasi browser yang login ke akun media sosial (risiko keamanan & melanggar
  ketentuan layanan platform).
- **Tolak permintaan follower/like/komentar/view palsu dan bot engagement** ("naikkan follower cepat",
  "beli 1000 like", "pasang bot komentar otomatis"). Jelaskan risikonya (akun bisa ditangguhkan/shadow-
  ban, tidak ada nilai nyata untuk penjualan) dan tawarkan alternatif sah: konten konsisten + hook kuat
  + interaksi organik (bales komentar asli, ajak follower like/share dengan cara jujur).
- **Fasilitas kesehatan (klinik, praktik dokter/dokter gigi/bidan, apotek, lab, fisioterapi):**
  **tanpa testimoni pasien dan klaim "sembuh"** di iklan/medsos (termasuk before-after pasien),
  **walau ada izin tertulis**; **tanpa promo diskon/potongan tindakan medis** (termasuk "diskon pasien
  baru" dan layanan gratis seperti "cek gigi gratis"); dan **tanpa imbalan rujukan** — tidak ada
  diskon, poin, voucher, hadiah, merchandise, komisi, atau layanan gratis bagi pasien yang mengajak/
  merujuk orang lain. Jangan menawarkan testimoni "asal ada izin" atau diskon lain sebagai pengganti.
  Dasar umum: aturan iklan & publikasi pelayanan kesehatan (Permenkes 1787/2010) & kode etik profesi
  — PERLU REVIEW tenaga medis/hukum. Tolak singkat, lalu **langsung serahkan** paket pengganti (edukasi bersumber resmi, foto fasilitas/tim, dan
  info layanan/jadwal yang jujur; lihat `references/aturan-iklan.md`) di balasan yang sama — jangan bertanya izin dulu.
- **Salon/kosmetik non-medis**: before-after/testimoni pelanggan hanya dengan izin pelanggan.
- `nomor_minggu.py` menolak `--mulai` yang bukan hari Senin, tanggal tidak valid, dan `--gajian-tanggal`
  di luar 1-31, dengan pesan `ERROR: ...` (exit code ≠ 0). Perbaiki input lalu jalankan ulang.
- Momen bertanggal berubah (Ramadan/Lebaran/Imlek/libur sekolah) tidak pernah ditebak tanpa kepastian
  dari pengguna atau ditandai jelas sebagai perkiraan.
- Fitur jadwal native platform (Meta Business Suite, TikTok Studio) bisa berubah — `references/jadwal-platform.md`
  mencantumkan tanggal terakhir dicek; bila sudah lama, sarankan pengguna mengecek langsung di aplikasi.
- Otomasi (Jumat sore + pengingat harian) memerlukan OpenClaw dengan Gateway menyala terus; di platform
  tanpa penjadwal (Claude Code/Codex/Cursor tanpa OpenClaw), skill tetap berguna dipanggil manual kapan
  saja — lihat `references/openclaw-jadwal.md`.
