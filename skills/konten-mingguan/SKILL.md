---
name: konten-mingguan
description: Menyusun paket konten media sosial 1 minggu (5-7 hari) untuk UMKM/usaha kecil maupun profesional/B2B — per hari berisi platform (Instagram/TikTok/Facebook/WA Status/LinkedIn/X-Twitter) & format, pilar konten, hook 3 detik, caption siap tempel, naskah video singkat, brief foto/video, hashtag, CTA, dan jam posting saran — dari profil usaha yang disimpan sekali dan momen minggu itu (gajian, tanggal kembar, hari besar, cek Ramadan/Lebaran). TIDAK memposting otomatis ke Instagram/TikTok/Facebook/LinkedIn — hanya menyiapkan draf untuk dijadwalkan sendiri. Gunakan saat pengguna minta "paket konten minggu ini/depan", "rencana konten mingguan", weekly content plan/pack, atau content calendar untuk 1 minggu (bukan 30 hari — untuk sebulan penuh pakai kalender-konten-30hari).
---

# Konten Mingguan

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
- Rencana sebulan penuh (30 hari) → `kalender-konten-30hari`
- Hanya satu caption untuk satu posting → `caption-sosmed-umkm`
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
   seperti di `kalender-konten-30hari`/`promo-kalender`) dan format sesuai platform aktif di `PROFIL.md`
   (Reels/TikTok untuk video pendek, Feed untuk foto rapi, Story/WA Status untuk info cepat/promo harian,
   **LinkedIn Post/Carousel** untuk konten profesional/B2B, **X/Twitter** untuk update singkat/thread).
5. **Isi tiap hari** dengan `templates/paket-mingguan.md` sebagai kerangka:
   - **Momen**: salin **SEMUA** entri momen hari itu dari output script (bisa lebih dari satu, mis.
     gajian + hari peringatan bersamaan) — jangan memilih sebagian, karena kombinasinya menentukan
     apakah hari itu boleh dipakai untuk pilar promo (lihat langkah 3).
   - **Hook 3 detik**: kalimat/pertanyaan pembuka, ≤ 12 kata, spesifik untuk produk (bukan generik).
   - **Caption siap tempel**: ikuti gaya & aturan panjang `caption-sosmed-umkm` (bila skill itu terpasang,
     rujuk untuk variasi tambahan; bila tidak, tulis sendiri dengan aturan yang sama — lihat tabel di
     `references/gaya-caption.md`).
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
7. **Simpan arsip** hasil isian ke `konten/minggu-<label_minggu>.md` (label dari output script, mis.
   `minggu-2026-W40.md`) di workspace pengguna, memakai isi lengkap `templates/paket-mingguan.md`.
8. **Sampaikan ke pengguna** dalam format output di bawah, lalu tawarkan: (a) automation mingguan +
   pengingat harian lewat OpenClaw (`references/openclaw-jadwal.md`), (b) buat brief foto detail lewat
   `foto-produk-brief`, (c) buat naskah live untuk salah satu hari lewat `naskah-live-jualan`.
9. **Jika Python tidak bisa dijalankan:** hitung tanggal manual dari kalender (Senin minggu depan dari
   hari ini), tandai tanggal kembar (tanggal = bulan) dan gajian (tgl 25 & 1) sendiri, beri tahu pengguna
   bahwa tanggal dihitung manual dan belum diverifikasi script.

## Format output
```
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

📥 Arsip disimpan: konten/minggu-<label_minggu>.md
📝 Asumsi: <daftar asumsi yang dipakai bila profil belum lengkap>
⚠️ Ingat: paket ini belum terposting — jadwalkan sendiri lewat Meta Business Suite/TikTok Studio (lihat "Cara jadwalkan sendiri" di file arsip), atau aktifkan pengingat harian OpenClaw.
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
Caption: "Rayakan gajian pertama bulan ini dengan ngopi santai. Kopi susu gula aren favorit, tetap Rp18.000.
Order gampang lewat WA/GoFood ya! ☕"
Brief foto/video: foto gelas kopi dekat jendela, cahaya pagi, tanpa promo besar-besaran (hari peringatan)
Hashtag: #kopisusu #kedaikopi #gajian #ngopiyuk
CTA: Order lewat WA/GoFood
```
📝 Asumsi: profil belum lengkap → target pembeli disimpulkan "pekerja & mahasiswa sekitar kedai"; jam
posting pakai acuan umum WA Status siang & sore.

## Checklist sebelum mengirim hasil
- [ ] Tanggal & momen dari `nomor_minggu.py` (atau dihitung manual dengan keterangan jelas)
- [ ] Jumlah hari sesuai kapasitas produksi di `PROFIL.md`, bukan dipaksa 7 hari
- [ ] Hari peringatan/hari duka tidak diberi pilar promo/hard-selling
- [ ] Tidak ada klaim yang dilarang di `PROFIL.md` (BPOM/PIRT/halal/jaminan hasil/"terbaik no.1")
- [ ] Kategori sensitif (kesehatan/kosmetik/keuangan/pangan) diberi peringatan singkat
- [ ] Setiap caption punya hook, CTA, dan panjang sesuai platform
- [ ] Ditulis jelas bahwa paket ini **belum terposting** dan jam posting adalah **perkiraan**
- [ ] Arsip `konten/minggu-<label_minggu>.md` disimpan

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
- **Klinik/kecantikan/kesehatan**: foto/video before-after dan testimoni pasien **wajib** ada izin
  tertulis dari pasien (lihat `references/aturan-iklan.md`). Tanpa izin tertulis, materi itu **tidak**
  dipakai di paket — tawarkan alternatif (fasilitas, alat, edukasi umum).
- `nomor_minggu.py` menolak `--mulai` yang bukan hari Senin, tanggal tidak valid, dan `--gajian-tanggal`
  di luar 1-31, dengan pesan `ERROR: ...` (exit code ≠ 0). Perbaiki input lalu jalankan ulang.
- Momen bertanggal berubah (Ramadan/Lebaran/Imlek/libur sekolah) tidak pernah ditebak tanpa kepastian
  dari pengguna atau ditandai jelas sebagai perkiraan.
- Fitur jadwal native platform (Meta Business Suite, TikTok Studio) bisa berubah — `references/jadwal-platform.md`
  mencantumkan tanggal terakhir dicek; bila sudah lama, sarankan pengguna mengecek langsung di aplikasi.
- Otomasi (Jumat sore + pengingat harian) memerlukan OpenClaw dengan Gateway menyala terus; di platform
  tanpa penjadwal (Claude Code/Codex/Cursor tanpa OpenClaw), skill tetap berguna dipanggil manual kapan
  saja — lihat `references/openclaw-jadwal.md`.
