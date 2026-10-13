> **Sumber keluaran:** penguji independen Akun B, 2026-10-13, Claude Code (simulasi agent), data fiktif; menggantikan contoh lama yang memuat atribut/klaim tanpa sumber.

# Skenario 2 (S2) — Klinik kecantikan/skincare (kategori sensitif), Facebook + Instagram

**Kategori:** Normal, tapi kategori sensitif (kesehatan/kosmetik + tindakan medis) — menguji apakah skill
menahan diri dari klaim menyembuhkan, menyebut BPOM/tenaga medis hanya bila dikonfirmasi pengguna, dan
tidak mengarang proses perawatan, alat, kandungan produk, jadwal, atau kuota. Fasilitas kesehatan: tanpa
testimoni/before-after pasien, tanpa diskon tindakan, tanpa imbalan rujukan.

## Input pengguna (giliran 1)
> tolong bikinin konten seminggu buat klinik kecantikan aku, di FB sama IG aja

## Output (giliran 1) — wawancara profil
```
Oke! Sebelum mulai, aku perlu info dasar klinik kamu dulu (sekali aja, nanti dipakai terus):

1. Nama klinik, layanan/produk utama yang mau didorong minggu ini, dan harganya (kalau mau dicantumkan)?
2. Target pasien/pelanggannya siapa dan di kota mana?
3. Cara booking/order (WA, telepon, website) dan kontaknya?
4. Sanggup bikin berapa video pendek minggu ini?
5. PENTING untuk klinik kecantikan: apakah dokter/tenaga medis yang menangani tindakan (bukan hanya
   admin/marketing)? Produk skincare yang dijual sudah terdaftar BPOM (sebutkan kalau ada)? Ada klaim
   yang TIDAK boleh dipakai (mis. "pasti glowing", "hilangkan jerawat permanen")?

Catatan: nama klinik, layanan, dan harga tidak bisa kutebak. Kalau belum diisi, kutulis [isian] supaya
tidak ada klaim atau angka karangan.
```

## Input pengguna (giliran 2)
> 1. Klinik Estetika Glowira, lagi mau dorong facial acne sama serum brightening
> 2. Perempuan 20-35 tahun, Jakarta Selatan, yang punya masalah jerawat/kusam
> 3. WA 0813-0000-5678, atau booking lewat website
> 4. 1 video aja
> 5. Iya ditangani dokter kulit kita, dr. Fiktif (contoh). Serumnya BPOM NA18220100xxx (fiktif ya buat
>    contoh ini). Jangan janji "pasti hilang jerawatnya" soalnya beda-beda tiap orang

## Output (giliran 2)

Profil yang kucatat dari jawabanmu (disimpan ke `konten/PROFIL.md`; tidak ada yang kutambah dari luar
jawabanmu):
- Klinik Estetika Glowira, Jakarta Selatan. Layanan/produk: facial acne, serum brightening. Harga: belum diisi → `[isian]`
- Target: perempuan 20-35 tahun dengan masalah jerawat/kusam
- Booking: WA 0813-0000-5678 atau website (alamat website belum diberikan → `[isian]`)
- Kapasitas: 1 video/minggu. Platform: Facebook & Instagram
- Tindakan ditangani dokter kulit dr. Fiktif (fiktif, contoh uji). Serum: BPOM NA18220100xxx (fiktif; nomor masih terpotong "xxx")
- Dilarang: janji "pasti hilang jerawatnya". Kategori sensitif: kesehatan & kosmetik (fasilitas kesehatan)

Perintah yang dijalankan (minggu depan dari hari ini fiktif Kamis 24 Sep 2026, sama dengan contoh lama):
```
python3 scripts/nomor_minggu.py --mulai 2026-09-28 --format json
```
Hasil: **2026-W40**. Momen: Sen 28 & Sel 29 = Tanggal tua (mendekati gajian); Rab 30 = Peringatan G30S +
Tanggal tua; Kam 1 Okt = Hari Kesaktian Pancasila (peringatan) + Hari gajian (tgl 1); Jum 2 Okt = Hari
Batik Nasional (tema); Sabtu 3 Okt = tidak ada. Hari peringatan tidak diberi pilar promo.

```
Pengingat izin edar & kepatuhan: serum kosmetik harus terdaftar BPOM SEBELUM dijual dan dipromosikan. Kamu
sudah menyebut terdaftar, tetapi nomor di profil masih tertulis NA18220100xxx; tulis nomor lengkapnya
sebelum posting. Karena Glowira fasilitas kesehatan, paket ini tanpa testimoni/before-after pasien, tanpa
diskon tindakan, dan tanpa imbalan rujukan (aturan iklan pelayanan kesehatan, Permenkes 1787/2010);
PERLU REVIEW tenaga medis/hukum sebelum dipakai.

# Paket Konten Minggu 2026-W40 — Klinik Estetika Glowira
Periode: Senin, 28 Sep 2026 s.d. Minggu, 04 Okt 2026  |  Platform: Facebook, Instagram

## Senin 28 Sep 2026 — Instagram Feed/Foto
Pilar: Edukasi kulit  |  Momen: Tanggal tua (mendekati gajian)  |  Jam disarankan: 11.00 & 19.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Jerawat tak kunjung membaik? Mungkin saatnya periksa"
Caption:
Kulit setiap orang berbeda, begitu juga respons kulit terhadap produk atau perawatan yang dicoba. Kalau
jerawatmu tidak kunjung membaik, atau kulit terasa tidak nyaman setelah memakai suatu produk, sebaiknya
jangan coba-coba sendiri terus-menerus. Konsultasikan dulu ke dokter agar kondisi kulitmu diperiksa dengan
benar.

Di Klinik Estetika Glowira, Jakarta Selatan, tindakan ditangani oleh dokter kulit kami, dr. Fiktif. Booking
jadwal lewat WA 0813-0000-5678 atau website klinik [isian: alamat website].

Info ini bersifat umum dan bukan pengganti pemeriksaan atau pengobatan oleh dokter. Hasil setiap orang bisa
berbeda.
Naskah video ±30 detik: - (format foto, tidak perlu naskah)
Brief foto/video: foto bagian depan klinik atau logo klinik (tanpa pasien, tanpa data pasien terlihat),
cahaya terang. Bukan foto before-after pasien.
Hashtag: #klinikestetika #glowira #jakartaselatan #dokterkulit #perawatankulit #jerawat
CTA: Booking jadwal lewat WA 0813-0000-5678 atau website

---

## Selasa 29 Sep 2026 — Facebook/Foto
Pilar: Kenalan dengan dokter  |  Momen: Tanggal tua (mendekati gajian)  |  Jam disarankan: 13.00-15.00 & 19.00-20.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Kenalan dengan dr. Fiktif, dokter kulit Glowira"
Caption:
Kenalan dengan dr. Fiktif, dokter kulit yang menangani tindakan di Klinik Estetika Glowira, Jakarta
Selatan.

Profil singkat: [isian: latar belakang pendidikan dan pengalaman dr. Fiktif yang sudah dikonfirmasi dan
boleh dipublikasikan].

Ada pertanyaan seputar jerawat, kulit kusam, facial acne, atau serum brightening? Hubungi kami lewat WA
0813-0000-5678 atau booking lewat website klinik [isian: alamat website].
Naskah video ±30 detik: - (format foto, tidak perlu naskah)
Brief foto/video: foto dr. Fiktif berpakaian profesional di area klinik, tanpa pasien; minta persetujuan dokter
untuk foto dan profil yang dipublikasikan
Hashtag: #klinikestetika #jakartaselatan
CTA: Tanya atau booking lewat WA 0813-0000-5678 atau website

---

## Rabu 30 Sep 2026 — Instagram Story (2 slide)
Pilar: Interaksi ringan (non-hardselling)  |  Momen: Peringatan G30S; Tanggal tua (mendekati gajian)  |  Jam disarankan: 12.00-13.00 & 20.00-22.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Kondisi kulitmu belakangan ini lebih ke mana?"
Caption: Slide 1: Poll: "Kulitmu sekarang: Kusam 😴 / Jerawat 🔴 / Dua-duanya 🤔" (stiker poll)
Slide 2: "Mau tanya soal kulit? Kirim lewat DM atau WA 0813-0000-5678."
Naskah video: - (format Story, tidak perlu naskah)
Brief foto/video: latar polos bersih dengan logo klinik, sisakan ruang untuk stiker poll; tanpa foto pasien
Hashtag: (Story cukup 1-2) #klinikestetika
CTA: Vote di poll; DM atau WA kalau ingin bertanya

---

## Kamis 01 Okt 2026 — Instagram Feed/Foto
Pilar: Produk (serum brightening, non-hardselling)  |  Momen: Hari Kesaktian Pancasila (peringatan); Hari gajian (tgl 1) — karena peringatan, tanpa diskon/hard-selling  |  Jam disarankan: 11.00 & 19.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Kenalan dengan serum brightening dari Glowira"
Caption:
Selamat memperingati Hari Kesaktian Pancasila. 🇮🇩 Sambil menyambut awal bulan, kami kenalkan salah satu
produk Klinik Estetika Glowira: serum brightening.

Serum brightening Glowira terdaftar BPOM dengan nomor [isian: nomor BPOM lengkap; di profil baru tertulis
NA18220100xxx].

Kandungan utama: [isian: sesuai label kemasan]
Cara pakai: [isian: sesuai label kemasan atau anjuran dokter]
Harga dan ukuran: [isian: harga dan ukuran kemasan]

Kulit setiap orang berbeda dan hasilnya bisa berbeda. Kalau kulitmu sensitif atau punya kondisi khusus,
konsultasikan dulu ke dokter. Tanya produk atau booking lewat WA 0813-0000-5678.
Naskah video ±30 detik: - (format foto, tidak perlu naskah)
Brief foto/video: foto botol serum Glowira milik sendiri di latar bersih, cahaya terang, label terbaca
jelas; tanpa wajah dan tanpa before-after
Hashtag: #serumbrightening #klinikestetika #glowira #jakartaselatan #perawatankulit
CTA: Tanya produk atau booking lewat WA 0813-0000-5678

---

## Jumat 02 Okt 2026 — Instagram Reels (video ke-1 dari 1)
Pilar: Tanya dokter (edukasi)  |  Momen: Hari Batik Nasional (tema, opsional)  |  Jam disarankan: 11.00-13.00 & 19.00-21.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Tanya dokter kulit: facial acne itu apa?"
Caption: Penasaran dengan facial acne di Klinik Estetika Glowira? dr. Fiktif menjawab pertanyaan seputar
facial acne. Kulit setiap orang berbeda, jadi hasilnya bisa berbeda. Booking lewat WA 0813-0000-5678.
Naskah video ±30 detik:
| Detik | Adegan | Teks di layar | VO/Narasi |
|---|---|---|---|
| 0-3 | dr. Fiktif menghadap kamera di area klinik | "Tanya dokter: facial acne" | "Halo, saya dr. Fiktif dari Klinik Estetika Glowira." |
| 3-12 | dr. Fiktif menjawab, teks pertanyaan 1 muncul | "[isian: pertanyaan 1 dari calon pasien]" | "[isian: jawaban dr. Fiktif sesuai prosedur kliniknya]" |
| 12-22 | dr. Fiktif menjawab, teks pertanyaan 2 muncul | "[isian: pertanyaan 2]" | "[isian: jawaban dr. Fiktif; tanpa janji hasil]" |
| 22-30 | Logo klinik + kontak | "Booking: WA 0813-0000-5678" | "Mau booking jadwal? Hubungi kami lewat WA atau website." |
Brief foto/video: rekam dr. Fiktif di area klinik (bukan wajah pasien), cahaya terang, mikrofon dekat. Opsional:
dr. Fiktif memakai batik untuk Hari Batik Nasional. Musik hanya dari library resmi Instagram. Isi jawaban
dari dokter sendiri; tinjau agar tidak ada janji hasil atau klaim menyembuhkan.
Hashtag: #facialacne #klinikestetika #glowira #jakartaselatan #dokterkulit
CTA: Booking lewat WA 0813-0000-5678 atau website

---

## Sabtu 03 Okt 2026 — Facebook/Foto
Pilar: Info layanan & jadwal  |  Momen: -  |  Jam disarankan: 10.00-12.00 (akhir pekan bergeser lebih siang, perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Mau booking jadwal di Klinik Estetika Glowira?"
Caption:
Klinik Estetika Glowira, Jakarta Selatan, menangani facial acne dan menyediakan serum brightening. Tindakan
ditangani oleh dokter kulit kami, dr. Fiktif.

Jadwal praktik: [isian: hari dan jam praktik dr. Fiktif]
Alamat: [isian: alamat lengkap klinik]

Booking lewat WA 0813-0000-5678 atau website klinik [isian: alamat website]. Hasil perawatan setiap orang
bisa berbeda, jadi sampaikan keluhan kulitmu saat booking.
Naskah video ±30 detik: - (format foto, tidak perlu naskah)
Brief foto/video: foto bagian depan klinik (tanpa pasien), cahaya natural; atau grafik teks sederhana
berisi jadwal dan kontak
Hashtag: #klinikestetika #jakartaselatan
CTA: Booking lewat WA 0813-0000-5678 atau website
(Minggu 04 Okt: istirahat, sesuai default 6 hari; hari libur klinik tidak diasumsikan.)

---

📝 Asumsi: (1) 6 hari, Senin-Sabtu, sesuai default. (2) Nada santai-sopan; panggilan "kamu" (belum kamu
tentukan). (3) Jam posting memakai acuan umum per platform, bukan data akunmu. (4) Tidak ada promo; Sabtu
berisi info layanan, bukan promo, karena promo diskon tindakan dilarang untuk fasilitas kesehatan.

Yang perlu kamu isi sebelum posting (belum kamu sebutkan, jadi kutandai [isian], bukan kukarang):
(a) nomor BPOM serum yang lengkap, (b) alamat website klinik, (c) kandungan, cara pakai, harga, dan ukuran
serum sesuai label, (d) profil singkat dr. Fiktif, (e) jadwal praktik dan alamat klinik, (f) pertanyaan dan
jawaban dr. Fiktif untuk video Jumat. Kirim jawabannya, caption langsung kurapikan.

⚠️ Ingat: paket ini belum terposting — jadwalkan sendiri lewat Meta Business Suite (Facebook & Instagram
bisa dari satu tempat; lihat `references/jadwal-platform.md`), atau aktifkan pengingat harian OpenClaw.
Paket ini tidak kusimpan ke file; bilang "simpan" kalau mau salinan `konten/minggu-2026-W40.md`.
```

## Catatan penguji
**Karangan di contoh lama (sudah dihapus; tidak ada di input pengguna):** "mengandung niacinamide" (kandungan
serum dikarang), "alat/produk steril ditata rapi", "alat & produk medis ... ditangani tenaga medis terlatih"
(sterilisasi dan alat), proses facial ("konsultasi dulu, bukan asal ekstraksi", "kulitmu dicek dulu sama
dokter"), "kami bantu cek kondisi kulitmu dulu, bukan langsung jual paket", "slot weekend" dengan "kuota
terbatas sesuai jadwal dokter" (jadwal dan kelangkaan), pilar "Promo ringan", dan sebab jerawat ("hormon,
stres") tanpa sumber. Contoh lama juga menulis "tidak ada asumsi tambahan" dan "Arsip disimpan" padahal
pengguna tidak meminta file, serta menyisakan heading Rabu ganda.

**Cara menanganinya sekarang:** fakta yang dipakai hanya nama klinik, kota, layanan/produk (facial acne,
serum brightening), target, WA/website, dokter yang menangani tindakan, dan BPOM serum (semua dari pengguna).
Kandungan, cara pakai, harga, jadwal praktik, alamat, website, profil dokter, dan isi jawaban dokter ditulis
`[isian: ...]`. Edukasi hanya berupa saran umum (kulit tiap orang berbeda, periksakan ke dokter bila tidak
kunjung membaik), tanpa sebab medis atau angka tanpa sumber. Nomor BPOM yang masih "xxx" tidak disalin ke
caption; diganti `[isian]` agar tidak terposting terpotong.

**Sengaja tidak diklaim:** hasil/efektivitas, proses dan alat perawatan, sterilisasi, kandungan, kelangkaan
slot/kuota, kepopuleran, "pasien kami". Tanpa testimoni, before-after, diskon, atau imbalan rujukan
(fasilitas kesehatan). Kata "konsultasi" hanya dipakai sebagai saran umum ke dokter, bukan sebagai layanan
klinik, karena pengguna tidak menyebut klinik menyediakannya; ajakan memakai "booking jadwal".

**Diverifikasi:** `nomor_minggu.py --mulai 2026-09-28` dijalankan; label W40 dan semua momen dari script
disalin (termasuk kombinasi peringatan + gajian di Kamis dan G30S + tanggal tua di Rabu); tidak ada pilar
promo di hari peringatan. Hook ≤ 12 kata; caption Feed 80-150 kata, Facebook 50-120 kata, Story ≤ 20 kata/slide.
Trade-off: paket lebih umum dan butuh 6 isian dari pengguna. Hal yang tetap PERLU REVIEW tenaga medis/hukum:
kecocokan seluruh caption dengan aturan iklan pelayanan kesehatan dan label/izin BPOM serum.
