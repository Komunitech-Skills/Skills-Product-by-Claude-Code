> **Sumber keluaran:** penguji independen Akun B, 2026-10-13, Claude Code (simulasi agent), data fiktif; menggantikan contoh lama yang memuat atribut/klaim tanpa sumber.

# Skenario 1 (S1) — Toko kue rumahan, Bekasi, IG+TikTok, minggu berisi tanggal kembar 10.10

**Kategori:** Normal, profil belum ada (wawancara sekali) — minggu spesifik diminta manual (bukan minggu
depan dari hari ini) supaya memuat tanggal kembar 10.10.2026, sekaligus menguji `nomor_minggu.py` pada
minggu nyata. Fokus ulang uji ini: semua fakta usaha harus berasal dari pengguna; yang tidak diberikan
ditulis `[isian: ...]`.

## Input pengguna (giliran 1)
> Buatin paket konten buat usaha kue rumahan aku dong, minggu tanggal 5-11 Oktober 2026. Aku jualan di
> IG sama TikTok.

## Output (giliran 1) — wawancara profil (sekali, sesuai `templates/PROFIL.md`)
```
Sebelum bikin paket kontennya, aku perlu tahu sedikit soal usahamu dulu (cukup sekali ya, nanti dipakai
lagi tiap minggu tanpa tanya ulang). Jawab santai aja, boleh singkat:

1. Nama usaha, produk utama yang mau didorong minggu ini, dan harganya (kalau mau dicantumkan)?
2. Target pembelinya siapa dan di kota/wilayah mana?
3. Order lewat mana (WA/DM/lainnya), dan ada nomor WA yang mau dicantumkan?
4. Sanggup bikin berapa video pendek minggu ini (sisanya foto/Story aja)?
5. Punya PIRT/BPOM/halal yang BENAR-BENAR sudah terdaftar? Ada klaim yang TIDAK boleh dipakai?

Catatan: nama usaha, produk, dan harga tidak bisa kutebak. Kalau belum diisi, kutulis sebagai [isian]
supaya tidak ada angka atau klaim karangan. Untuk hal lain (gaya bahasa, jam posting) bilang aja
"pakai default" kalau mau cepat, nanti kucatat di akhir hasil.
```

## Input pengguna (giliran 2)
> 1. Kue Rumahan Bu Sari, di Bekasi. Lagi mau dorong kue lapis legit sama brownies kukus, nastar toples juga ada
> 2. Ibu-ibu arisan & pekerja kantoran usia 25-45 di Bekasi, buat oleh-oleh/snack kantor
> 3. WA ya, nomornya 0812-0000-1234, DM IG juga boleh
> 4. 2 video aja minggu ini, sisanya foto
> 5. Ada PIRT (P-IRT No. 2023217010203-fiktif ya buat contoh ini). Jangan bilang "paling laris di Bekasi" soalnya belum ada buktinya

## Output (giliran 2)

Profil yang kucatat dari jawabanmu (disimpan ke `konten/PROFIL.md` agar minggu depan tidak ditanya ulang;
tidak ada yang kutambah dari luar jawabanmu):
- Kue Rumahan Bu Sari, Bekasi. Produk: kue lapis legit, brownies kukus, nastar toples. Harga: belum diisi → `[isian]`
- Target: ibu-ibu arisan & pekerja kantoran 25-45 tahun di Bekasi (oleh-oleh/snack kantor)
- Order: WA 0812-0000-1234, DM Instagram. Platform: Instagram & TikTok. Kapasitas: 2 video/minggu, sisanya foto/Story
- Izin: P-IRT No. 2023217010203 (fiktif, contoh uji). Halal/BPOM tidak disebut → tidak dicantumkan
- Dilarang: klaim "paling laris di Bekasi". Kategori sensitif: pangan

Perintah yang dijalankan:
```
python3 scripts/nomor_minggu.py --mulai 2026-10-05 --format json
```
Hasil: minggu **2026-W41** (Senin 05 Okt s.d. Minggu 11 Okt 2026). Satu-satunya momen otomatis:
Sabtu 10 Okt 2026 = **Tanggal kembar 10.10** (tipe promo). Tidak ada gajian maupun hari peringatan di minggu
ini (momen lain kosong di output script).

```
Pengingat izin edar: izin PIRT harus ada SEBELUM kue dijual dan dipromosikan. Kamu sudah menyebut
P-IRT No. 2023217010203; pastikan nomor itu berlaku untuk ketiga produk (lapis legit, brownies, nastar).

# Paket Konten Minggu 2026-W41 — Kue Rumahan Bu Sari
Periode: Senin, 05 Okt 2026 s.d. Minggu, 11 Okt 2026  |  Platform: Instagram, TikTok

## Senin 05 Okt 2026 — Instagram Feed/Foto
Pilar: Perkenalan menu  |  Momen: -  |  Jam disarankan: 11.00 & 19.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Bingung bawa kue apa buat arisan atau ngantor?"
Caption:
Lagi cari kue buat arisan atau camilan rapat di kantor? Kenalan dulu dengan tiga pilihan dari Kue Rumahan
Bu Sari, Bekasi:

🍰 Kue lapis legit
🍫 Brownies kukus
🫙 Nastar toples

Harga & ukuran: [isian: harga dan ukuran/isi tiap produk]

Mau pesan? Chat WA 0812-0000-1234 atau DM Instagram. Biar pesananmu mudah dicatat, tulis produk yang kamu
mau, jumlahnya, dan tanggal acaranya ya, Kak.

Catat dulu di daftar rencana arisan atau acara kantor bulan ini, lalu simpan postingan ini supaya mudah
dicari lagi. 📌
Naskah video ±30 detik: - (format foto, tidak perlu naskah)
Brief foto/video: ketiga produk berjajar di satu meja, cahaya natural dekat jendela, alas polos; pakai foto
milik sendiri. Ambil juga satu foto close-up tiap produk untuk postingan berikutnya.
Hashtag: #kuelapislegit #brownieskukus #nastartoples #kuerumahanbekasi #kuearisan #snackkantor #umkmbekasi
CTA: Chat WA 0812-0000-1234 atau DM Instagram untuk pesan

---

## Selasa 06 Okt 2026 — TikTok/Video pendek (video ke-1 dari 2)
Pilar: Perkenalan menu (video)  |  Momen: -  |  Jam disarankan: 12.00-13.00 & 19.00-22.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Arisan minggu ini, bawa lapis legit, brownies, atau nastar?"
Caption: Arisan atau ngantor minggu ini, kamu pilih yang mana? Ada kue lapis legit, brownies kukus, dan nastar
toples dari Kue Rumahan Bu Sari. Pesan lewat WA 0812-0000-1234, ya, Kak! 🍰
Naskah video ±30 detik:
| Detik | Adegan | Teks di layar | VO/Narasi |
|---|---|---|---|
| 0-3 | Close-up tangan menaruh sepotong kue lapis legit di piring | "Arisan minggu ini bawa apa?" | "Arisan minggu ini, bawa apa ya?" |
| 3-10 | Kue lapis legit di meja, kamera bergeser pelan | "Kue lapis legit" | "Ada kue lapis legit." |
| 10-17 | Potongan brownies kukus di piring | "Brownies kukus" | "Ada brownies kukus." |
| 17-24 | Toples nastar dibuka | "Nastar toples" | "Dan nastar toples." |
| 24-30 | Ketiga produk berjajar, nomor WA di layar | "Pesan: WA 0812-0000-1234 · Harga: [isian]" | "Pesan lewat WA atau DM Instagram, ya, Kak." |
Brief foto/video: rekam vertikal, satu segmen pendek per produk, cahaya terang, teks layar besar. Musik hanya
dari library resmi TikTok/Instagram.
Hashtag: #kuelapislegit #brownieskukus #nastartoples #kuerumahanbekasi
CTA: Pesan lewat WA 0812-0000-1234

---

## Rabu 07 Okt 2026 — Instagram Story (2 slide)
Pilar: Interaksi/polling  |  Momen: -  |  Jam disarankan: 12.00-13.00 & 20.00-22.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Nastar toples atau brownies kukus buat cemilan sore ini?"
Caption: Slide 1: Poll: "Nastar toples 🫙 vs Brownies kukus 🍫 — kamu Team mana?" (stiker poll IG Story)
Slide 2: "Makasih sudah vote! Mau pesan? DM atau WA 0812-0000-1234."
Naskah video: - (format Story, tidak perlu naskah)
Brief foto/video: dua produk berdampingan di meja yang sama, pencahayaan sama rata, sisakan ruang kosong di
tengah untuk stiker poll
Hashtag: (Story cukup 1-2) #kuerumahanbekasi
CTA: Vote di poll, lanjut DM kalau mau pesan

---

## Kamis 08 Okt 2026 — Instagram Feed/Foto
Pilar: Edukasi ringan  |  Momen: -  |  Jam disarankan: 11.00 & 19.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "3 hal yang perlu disiapkan sebelum pesan kue arisan"
Caption:
Mau pesan kue untuk arisan atau acara kantor? Siapkan tiga hal ini dulu supaya pesananmu lancar:

1️⃣ Jumlah orang. Hitung perkiraan tamu yang hadir, termasuk yang mungkin datang belakangan.
2️⃣ Tanggal dan jam acara. Tulis kapan kuenya dibutuhkan.
3️⃣ Pantangan makan. Tanyakan ke tamu apakah ada yang alergi atau punya pantangan, lalu cek bahan produk
sebelum memesan.

Info bahan dan alergen produk Kue Rumahan Bu Sari: [isian: bahan utama dan alergen tiap produk].
Izin edar: P-IRT No. 2023217010203.

Siap pesan? Chat WA 0812-0000-1234 atau DM Instagram, ya, Kak. 🍰
Naskah video ±30 detik: - (format foto/carousel, tidak perlu naskah)
Brief foto/video: carousel 3 slide, satu poin per slide dengan teks besar di latar polos; slide terakhir foto
produk milik sendiri dan nomor WA
Hashtag: #tipsarisan #kuearisan #kuelapislegit #brownieskukus #nastartoples #kuerumahanbekasi #umkmbekasi
CTA: Simpan postingan ini & chat WA 0812-0000-1234 untuk pesan

---

## Jumat 09 Okt 2026 — TikTok/Video pendek (video ke-2 dari 2)
Pilar: Cara pesan  |  Momen: -  |  Jam disarankan: 12.00-13.00 & 19.00-22.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Pesan kue arisan cuma butuh tiga langkah"
Caption: Pesan kue buat arisan atau kantor ternyata gampang, Kak. Chat WA 0812-0000-1234, tulis pesananmu, lalu
[isian: langkah ketiga — pembayaran dan pengambilan/pengiriman]. Simpan videonya biar nggak lupa! 📌
Naskah video ±30 detik:
| Detik | Adegan | Teks di layar | VO/Narasi |
|---|---|---|---|
| 0-3 | Layar HP membuka chat WhatsApp | "Pesan kue cuma 3 langkah" | "Pesan kue arisan cuma butuh tiga langkah." |
| 3-10 | Rekam layar: mengetuk nomor WA | "1. Chat WA 0812-0000-1234" | "Satu, chat kami lewat WhatsApp atau DM Instagram." |
| 10-18 | Rekam layar: contoh pesan yang diketik | "2. Tulis produk, jumlah, tanggal acara" | "Dua, tulis kue yang kamu mau, jumlahnya, dan tanggal acaranya." |
| 18-26 | [isian: adegan sesuai langkah ketiga] | "3. [isian: langkah ketiga]" | "[isian: narasi langkah ketiga sesuai cara Bu Sari]" |
| 26-30 | Ketiga produk berjajar + nama usaha | "Kue Rumahan Bu Sari · Bekasi" | "Kue Rumahan Bu Sari, Bekasi. Sampai ketemu di chat!" |
Brief foto/video: rekam layar chat contoh memakai nomor sendiri; jangan tampilkan chat pelanggan asli (data
pribadi, UU PDP). Musik hanya dari library resmi platform.
Hashtag: #caramemesan #kuearisan #kuerumahanbekasi #kuelapislegit
CTA: Chat WA 0812-0000-1234 atau DM Instagram

---

## Sabtu 10 Okt 2026 — Instagram Feed/Foto (Promo)
Pilar: Promo tanggal kembar  |  Momen: Tanggal kembar 10.10  |  Jam disarankan: 10.00-12.00 (akhir pekan bergeser lebih siang, perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Tanggal kembar 10.10, sudah pesan kue untuk akhir pekan?"
Caption:
Selamat tanggal kembar 10.10, Kak! 🎉

[isian: promo 10.10 yang benar-benar kamu tawarkan — bentuk promo, produk yang ikut, syarat, dan sampai kapan
berlaku. Hapus baris ini kalau tidak ada promo]

Ada acara keluarga, arisan, atau kumpul-kumpul di akhir pekan ini? Kue lapis legit, brownies kukus, dan
nastar toples dari Kue Rumahan Bu Sari bisa kamu pesan lewat WA 0812-0000-1234 atau DM Instagram.

Bingung memilih? Pilih sesuai selera dan jumlah tamu, lalu tanya saja lewat chat. Tulis produk, jumlah,
dan tanggal acaranya ya. 🍰
Naskah video ±30 detik: - (format foto, tidak perlu naskah)
Brief foto/video: ketiga produk bersanding dengan properti angka "10.10" (kertas tulisan tangan atau print
sederhana), cahaya terang, foto milik sendiri
Hashtag: #tanggalkembar #1010 #kuelapislegit #brownieskukus #nastartoples #kuerumahanbekasi #umkmbekasi
CTA: Chat WA 0812-0000-1234 atau DM Instagram; sebut produk, jumlah, dan tanggal acara
(Minggu 11 Okt: istirahat, sesuai default 6 hari.)

---

📝 Asumsi: (1) 6 hari, Senin-Sabtu, sesuai default; Minggu istirahat. (2) Nada santai-sopan dan sapaan "Kak"
(belum kamu tentukan; default templat). (3) Jam posting memakai acuan umum per platform, bukan data akunmu.
(4) Tidak ada promo selain momen 10.10 dari script; bentuk promonya kukosongkan sebagai [isian].
(5) Sabtu hanya Feed karena kuota 2 video sudah dipakai Selasa & Jumat.

Yang perlu kamu isi sebelum posting (belum kamu sebutkan, jadi kutandai [isian], bukan kukarang):
(a) harga dan ukuran/isi tiap produk, (b) promo 10.10: ada atau tidak, (c) bahan utama dan alergen tiap
produk, (d) langkah pembayaran dan pengambilan/pengiriman. Kirim jawabannya, caption langsung kurapikan.

⚠️ Ingat: paket ini belum terposting — jadwalkan sendiri lewat Meta Business Suite/TikTok Studio (lihat
`references/jadwal-platform.md`), atau aktifkan pengingat harian OpenClaw. Paket ini tidak kusimpan ke
file; bilang "simpan" kalau mau salinan `konten/minggu-2026-W41.md`.

Mau aku bantu sekalian: (a) pasang pengingat otomatis Jumat sore + pengingat harian lewat OpenClaw, (b)
buat brief foto detail produk (`foto-produk-brief`), atau (c) buatkan naskah live jualan untuk hari
Sabtu 10.10 (`naskah-live-jualan`)?
```

## Catatan penguji
**Karangan di contoh lama (sudah dihapus; tidak ada di input pengguna):** "dipanggang 18 lapis satu-satu",
"18 lapis vs 9 lapis", "bahan dipilih sendiri tiap minggu, dipanggang di rumah, bukan produksi massal",
"selalu ludes duluan", "dikukus ±40 menit, dicek manual", "tekstur lumer/fudgy", "kita kirim area Bekasi",
"kita bantu hitung porsinya", tips simpan kue ("tahan seminggu", plastic wrap, kulkas), testimoni "Kak Rina"
(karangan walau diberi catatan fiktif), promo "beli 1 lapis legit gratis 3 nastar", kode "1010", "ukuran
standar", "stok harian terbatas/produksi manual tiap hari/pre-order besok". Contoh lama juga menulis "Arsip
disimpan" dan "tidak ada asumsi tambahan" padahal pengguna tidak meminta file dan banyak hal diasumsikan.

**Cara menanganinya sekarang:** fakta yang dipakai hanya nama usaha, kota, tiga produk, target, WA/DM IG,
kuota 2 video, nomor PIRT, dan larangan "paling laris" (semua dari pengguna). Harga, ukuran, promo 10.10,
bahan/alergen, serta langkah bayar & ambil/kirim ditulis `[isian: ...]` dan ditanyakan di akhir. Edukasi
Kamis berisi saran umum bagi pembeli (hitung tamu, tanggal acara, tanya pantangan makan), bukan klaim tentang
produk atau proses. Tidak ada angka atau klaim eksternal tanpa sumber. Testimoni diganti polling dan edukasi
karena pengguna tidak memberi testimoni asli.

**Sengaja tidak diklaim:** kelangkaan/stok, proses pembuatan dan durasinya, bahan, masa simpan, pengiriman,
kepopuleran, "halal"/BPOM. Nomor PIRT dipakai persis seperti diberikan (hanya di postingan Kamis).

**Diverifikasi:** `nomor_minggu.py --mulai 2026-10-05` dijalankan; label W41 dan momen 10.10 (Sabtu) cocok.
Hook ≤ 12 kata; caption Feed 80-150 kata, TikTok 1-3 kalimat, Story ≤ 20 kata/slide; promo 1 dari 6 hari
(±17%); jam Story memakai baris khusus Story di `references/gaya-caption.md`. Trade-off: tanpa atribut produk,
caption lebih umum dan pengguna perlu mengisi 4 hal di akhir. Catatan SKILL.md (tidak diubah, skill tidak lagi
diiterasi): ATURAN PERTAMA berbunyi "jangan menulis file sama sekali kecuali diminta", sedangkan Langkah 1
meminta `konten/PROFIL.md` disimpan; di contoh ini profil disimpan, paket tidak.
