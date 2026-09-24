# Skenario 2 (S2) — Klinik kecantikan/skincare (kategori sensitif), Facebook + Instagram

**Kategori:** Normal, tapi kategori sensitif (kesehatan/kosmetik + tindakan medis) — menguji apakah
skill benar-benar menahan diri dari klaim menyembuhkan, memastikan BPOM/izin tindakan hanya disebut
kalau dikonfirmasi pengguna, dan menandai bahwa tindakan medis perlu dokter/izin resmi.

## Input pengguna (giliran 1)
> tolong bikinin konten seminggu buat klinik kecantikan aku, di FB sama IG aja

## Output agent (giliran 1) — wawancara profil
```
Oke! Sebelum mulai, aku perlu info dasar klinik kamu dulu (sekali aja, nanti dipakai terus):

1. Nama klinik & layanan/produk utama apa yang mau didorong minggu ini? (mis. facial, laser, skincare
   jual putus, dsb)
2. Target pasien/pelanggannya siapa dan di kota mana?
3. Cara booking/order (WA, telepon, aplikasi) dan kontaknya?
4. Sanggup bikin berapa video pendek minggu ini?
5. PENTING untuk klinik kecantikan: apakah dokter/tenaga medis yang menangani tindakan (bukan hanya
   admin/marketing)? Produk skincare yang dijual sudah terdaftar BPOM (sebutkan kalau ada)? Ada klaim
   yang TIDAK boleh dipakai (mis. "pasti glowing", "hilangkan jerawat permanen")?
```

## Input pengguna (giliran 2)
> 1. Klinik Estetika Glowira, lagi mau dorong facial acne sama serum brightening
> 2. Perempuan 20-35 tahun, Jakarta Selatan, yang punya masalah jerawat/kusam
> 3. WA 0813-0000-5678, atau booking lewat website
> 4. 1 video aja
> 5. Iya ditangani dokter kulit kita, dr. Fiktif (contoh). Serumnya BPOM NA18220100xxx (fiktif ya buat
>    contoh ini). Jangan janji "pasti hilang jerawatnya" soalnya beda-beda tiap orang

## Output agent (giliran 2)

`konten/PROFIL.md` disimpan: Klinik Estetika Glowira — Jakarta Selatan — facial acne, serum brightening —
target perempuan 20-35 dengan masalah jerawat/kusam — booking WA 0813-0000-5678/website — 1 video/minggu
— tindakan ditangani dr. Fiktif (dokter kulit) — serum BPOM NA18220100xxx (fiktif, contoh uji) —
**kategori sensitif: kesehatan & kosmetik** — dilarang klaim "pasti hilang jerawatnya".

```
python3 scripts/nomor_minggu.py --format json
```
(pengguna tidak sebut minggu tertentu → default minggu depan dari hari ini 2026-09-24, Kamis → Senin
berikutnya = **2026-09-28**, label **2026-W40**, diverifikasi sama seperti tes 1 di `HASIL-UJI.md`.)

```
# Paket Konten Minggu 2026-W40 — Klinik Estetika Glowira
Periode: Senin, 28 Sep 2026 s.d. Sabtu, 03 Okt 2026  |  Platform: Facebook, Instagram

## Senin 28 Sep 2026 — Instagram Feed/Foto
Pilar: Edukasi kulit  |  Momen: -  |  Jam disarankan: 11.00 & 19.30 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Jerawat gak selalu soal cuci muka doang, lho"
Caption:
Jerawat bisa dipengaruhi banyak hal — hormon, stres, sampai produk yang gak cocok di kulit. Bukan cuma
soal rajin cuci muka. Kalau jerawatmu gak kunjung membaik, sebaiknya konsultasi ke dokter kulit biar
tahu penyebab dan penanganan yang tepat buat kulitmu — bukan sekadar coba-coba produk.
Mau konsultasi sama dr. Fiktif di Klinik Estetika Glowira? Booking lewat WA, Kak.
⚠️ Bukan pengganti pemeriksaan/pengobatan dokter langsung — ini info umum, hasil tiap orang beda.
Order/Booking: WA 0813-0000-5678
Naskah video: - (format foto, tidak perlu naskah)
Brief foto/video: foto suasana klinik yang bersih & profesional (ruang tunggu/konsultasi), BUKAN foto
before-after pasien tanpa izin tertulis
Hashtag: #klinikkecantikan #jakartaselatan #kulitsehat #konsultasidokterkulit
CTA: Booking konsultasi lewat WA

---

## Selasa 29 Sep 2026 — Facebook/Foto
Pilar: Profil dokter & kepercayaan  |  Momen: -  |  Jam disarankan: 13.00-15.00 & 19.00-20.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Kenalan sama dr. Fiktif, dokter kulit di Glowira"
Caption:
Di balik layanan facial acne & perawatan kulit di Glowira, ada dr. Fiktif yang menangani langsung
konsultasi dan tindakan. Jadi kamu gak cuma ketemu terapis, tapi juga bisa konsultasi medis soal
kondisi kulitmu. Booking konsultasi lewat WA ya, Kak.
Naskah video: - (format foto, tidak perlu naskah)
Brief foto/video: foto dokter dengan atribut profesional (jas/name tag) di ruang praktik, pencahayaan
terang & rapi
Hashtag: #dokterkulit #kliniksehat #jaksel (0-3 hashtag, sesuai gaya Facebook)
CTA: Booking konsultasi lewat WA

---

## Rabu 30 Sep 2026 — TikTok/(dilewati — pengguna tidak pilih TikTok)
(Hari ini tetap diisi lewat Facebook/IG mengikuti platform aktif pengguna)

## Rabu 30 Sep 2026 — Instagram Story
Pilar: Interaksi ringan (non-hardselling — hari ini Peringatan G30S)  |  Momen: Peringatan G30S; Tanggal
tua (mendekati gajian)  |  Jam disarankan: 11.00-13.00 & 19.00-21.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Kulitmu lagi kusam, berjerawat, atau kombinasi?"
Caption: Poll: "Kondisi kulitmu sekarang: Kusam 😴 / Jerawat aktif 🔴 / Kombinasi keduanya 🤔" (stiker poll)
Brief foto/video: foto produk skincare Glowira di meja bersih, ruang kosong untuk stiker poll
Hashtag: (tidak perlu, Story) 
CTA: Vote, lanjut DM kalau mau rekomendasi

---

## Kamis 01 Okt 2026 — Instagram Feed/Foto
Pilar: Produk (serum brightening, non-hardselling)  |  Momen: Hari Kesaktian Pancasila (peringatan) +
Hari gajian (tgl 1) — hari ini bertepatan peringatan nasional, jadi tetap non-hardselling/tanpa diskon
walau juga tanggal gajian  |  Jam disarankan: 11.00 & 19.30 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Kandungan niacinamide di serum ini bantu tampilan kulit kusam"
Caption:
Serum brightening Glowira (BPOM NA18220100xxx) mengandung niacinamide untuk membantu tampilan kulit
terlihat lebih cerah & merata. Hasil bisa berbeda tiap orang tergantung kondisi kulit masing-masing —
konsultasikan dulu ke dokter kami kalau kamu punya kondisi kulit sensitif/khusus.
Booking konsultasi lewat WA.
Naskah video: - (format foto, tidak perlu naskah)
Brief foto/video: foto botol serum dengan pencahayaan bersih, tanpa before-after
Hashtag: #serumbrightening #skincareBPOM #kulitkusam #glowirajaksel
CTA: Booking konsultasi lewat WA
Catatan kepatuhan: hari ini bertepatan Hari Kesaktian Pancasila (peringatan) — caption tetap edukatif
produk (bukan diskon/hardsell) sesuai checklist SKILL.md.

---

## Jumat 02 Okt 2026 — Instagram Reels
Pilar: Proses treatment (edukasi)  |  Momen: Hari Batik Nasional (tema, opsional disinggung)  |  Jam
disarankan: 11.00-13.00 & 19.00-21.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Ini yang terjadi pas kamu facial acne di klinik (bukan di rumah)"
Naskah video ±30 detik:
| Detik | Adegan | Teks di layar | VO/Narasi |
|---|---|---|---|
| 0-3 | Ruang treatment, alat facial disiapkan | "Ini bedanya facial di klinik" | "Ini yang terjadi pas kamu facial acne di klinik, bukan di rumah" |
| 3-15 | Proses konsultasi kulit dengan dokter/terapis (tanpa menampilkan wajah pasien asli tanpa izin) | "Konsultasi dulu, bukan asal ekstraksi" | "Kulitmu dicek dulu sama dokter, baru ditentukan langkah yang cocok" |
| 15-25 | Alat/produk steril ditata rapi | "Alat & produk medis, bukan alat rumahan" | "Semua pakai alat & produk yang ditangani tenaga medis terlatih" |
| 25-30 | Logo klinik + kontak | "Booking: WA 0813-0000-5678" | "Mau coba? Booking konsultasi dulu ya lewat WA" |
Brief foto/video: rekam ruang treatment & alat (bukan wajah pasien asli tanpa izin tertulis — pakai
model staf/tim internal yang setuju direkam, atau tanpa wajah sama sekali)
Hashtag: #facialacne #kliniksehat #treatmentkulit #jaksel
CTA: Booking konsultasi lewat WA

---

## Sabtu 03 Okt 2026 — Facebook/Foto
Pilar: Promo ringan (akhir pekan)  |  Momen: -  |  Jam disarankan: 10.00-12.00 (akhir pekan bergeser
lebih siang, perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Weekend, waktunya rawat kulit tanpa buru-buru"
Caption:
Konsultasi awal di Glowira, kami bantu cek kondisi kulitmu dulu sebelum menentukan perawatan yang cocok
— bukan langsung jual paket. Booking slot weekend lewat WA, kuota terbatas sesuai jadwal dokter (bukan
gimmick, memang jadwal praktik terbatas).
Naskah video: - (format foto, tidak perlu naskah)
Brief foto/video: suasana klinik weekend yang santai, cahaya natural
Hashtag: #konsultasikulit #weekendcare #jaksel
CTA: Booking slot weekend lewat WA

---

📥 Arsip disimpan: konten/minggu-2026-W40.md
📝 Asumsi: tidak ada asumsi tambahan — profil dijawab lengkap di wawancara giliran 2.
⚠️ Ingat: paket ini belum terposting — jadwalkan sendiri lewat Meta Business Suite (Facebook & Instagram
bisa dari satu tempat), atau aktifkan pengingat harian OpenClaw.

⚠️ Catatan khusus kategori sensitif (kesehatan/kosmetik): semua caption di atas sudah dicek tanpa klaim
menyembuhkan/jaminan hasil, mencantumkan disclaimer "bukan pengganti pemeriksaan dokter" di konten
edukasi kulit, dan menghindari before-after pasien tanpa izin. BPOM produk hanya disebut karena kamu
konfirmasi sudah terdaftar — pastikan nomor yang ditulis di atas benar sebelum posting.
```

## Catatan penguji
**Bagus:**
- Tidak ada satu pun klaim "menyembuhkan"/"pasti hilang jerawat" — konsisten memakai bahasa "membantu
  tampilan", "hasil bisa berbeda tiap orang", sesuai tabel kategori sensitif di `references/aturan-iklan.md`.
- Disclaimer "Bukan pengganti pemeriksaan/pengobatan dokter" disisipkan di konten edukasi kulit (Senin),
  persis sesuai tabel peringatan kategori Kesehatan di `references/aturan-iklan.md`.
- BPOM hanya disebut karena pengguna eksplisit konfirmasi ("Iya ditangani dokter... BPOM NA1822...") —
  skill tidak mengarang nomor atau mengasumsikan izin.
- Tindakan medis (facial acne) secara eksplisit ditandai ditangani dokter, bukan sekadar "admin"/marketing
  — ini menjawab poin brief soal "izin tindakan medis".
- Brief foto secara eksplisit menghindari before-after pasien tanpa izin — inisiatif bagus (walau
  SKILL.md tidak menyebutkan before-after secara eksplisit, lihat cacat di bawah).
- Hari peringatan (1 Okt, Hari Kesaktian Pancasila) tetap ditangani non-hardselling sesuai checklist,
  **meskipun** tanggal itu juga hari gajian (tgl 1) — SKILL.md §Langkah kerja 3 eksplisit bilang hari
  peringatan tidak boleh diberi pilar promo, dan aturan itu diikuti dengan benar (promo dipindah ke
  Sabtu). Catatan: draf awal penguji sempat lupa mencantumkan momen "Hari gajian (tgl 1)" dan "Peringatan
  G30S" secara lengkap di kolom Momen (sudah dikoreksi) — ini human error penguji saat transkripsi
  output JSON script ke format akhir, bukan bug skill; tapi ini justru jadi pengingat: SKILL.md tidak
  punya *checklist* eksplisit "pastikan semua momen dari JSON script disalin ke output, tidak dipilih
  sebagian" — risiko agen lain sungguhan melewatkan momen sekunder seperti yang penguji alami sendiri.

**Kurang / catatan:**
- **Cacat sedang (ringan-sedang):** SKILL.md dan `references/aturan-iklan.md` **tidak secara eksplisit**
  menyebut aturan "jangan pakai foto before-after pasien tanpa izin" — padahal ini salah satu risiko
  paling umum di industri klinik kecantikan (data pribadi pasien + potensi klaim hasil berlebihan lewat
  foto, bukan cuma teks). Penguji menambahkannya sendiri karena mengikuti semangat aturan data pribadi
  (UU PDP) di `references/aturan-iklan.md`, tapi ini seharusnya eksplisit ditulis di skill (mis. tambah
  baris di tabel kategori sensitif "Kesehatan/klinik" atau di `references/aturan-iklan.md`), supaya
  agent lain yang menjalankan skill ini tidak melewatkannya. Lihat saran di `HASIL-UJI.md`.
- Output agent sempat "typo langkah" menulis heading duplikat "Rabu 30 Sep 2026" dua kali dalam draf
  kerja (satu placeholder salah pilih format TikTok padahal platform aktif hanya FB+IG) sebelum
  dikoreksi — ini murni human/agent-simulation slip saat menyusun contoh, BUKAN bug di skill (SKILL.md
  sendiri sudah benar mengarahkan "sesuai platform aktif di PROFIL.md"). Dicatat untuk transparansi.
- Sama seperti S1: jam posting Instagram Story dan Reels menaksir dari tabel Feed/Reels karena
  `gaya-caption.md` tidak merinci jam khusus per format (Story vs Feed vs Reels) — lihat cacat gabungan
  di `HASIL-UJI.md`.
