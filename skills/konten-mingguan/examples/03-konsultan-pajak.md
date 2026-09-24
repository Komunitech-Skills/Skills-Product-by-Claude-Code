# Skenario 3 (S3) — Konsultan pajak/keuangan freelance, LinkedIn + Instagram

**Kategori:** Normal, tapi kategori sensitif (jasa keuangan) + platform **LinkedIn** yang TIDAK ada di
tabel referensi skill (`references/gaya-caption.md` hanya mencakup IG/TikTok/Facebook/WA Status). Ini
sengaja dipakai untuk menguji bagaimana skill menangani platform di luar tabelnya.

## Input pengguna (giliran 1)
> bikinin paket konten mingguan buat jasa konsultan pajak freelance aku, posting di linkedin sama
> instagram

## Output agent (giliran 1) — wawancara profil
```
Siap! Sebelum mulai, aku perlu info dasar jasa kamu dulu (sekali aja):

1. Nama usaha/personal brand & layanan utama apa yang mau didorong minggu ini? (mis. lapor SPT tahunan,
   konsultasi pajak UMKM, dsb)
2. Target kliennya siapa (individu/UMKM/perusahaan) dan di mana biasanya kamu dapat klien?
3. Cara klien menghubungi/order jasa (WA, email, form, DM)?
4. Sanggup bikin berapa video pendek minggu ini, sisanya tulisan/foto aja?
5. Ada sertifikasi/izin resmi yang mau dicantumkan (mis. terdaftar sebagai Kuasa Wajib Pajak/brevet
   pajak)? Ada klaim yang TIDAK boleh dipakai (mis. "pasti hemat pajak", "dijamin lolos audit")?

Catatan: LinkedIn belum punya panduan gaya caption/jam posting khusus di skill ini (referensi yang ada
baru IG/TikTok/Facebook/WA Status) — aku akan sesuaikan sendiri pakai prinsip yang sama (profesional,
ringkas, tanpa jargon berlebihan) dan tandai jam postingnya sebagai perkiraan yang lebih kasar dari
platform lain. Kalau kamu sudah tahu jam ramai audiens LinkedIn-mu sendiri, kasih tahu ya.
```

## Input pengguna (giliran 2)
> 1. Nama usaha "Konsul Pajak by Dina", fokus konsultasi & lapor SPT Tahunan UMKM
> 2. Pemilik UMKM & freelancer yang bingung lapor pajak sendiri, biasanya dari LinkedIn & rekomendasi
> 3. WA 0817-0000-9012 atau form di link bio
> 4. 1 video aja
> 5. Aku terdaftar Kuasa Wajib Pajak (fiktif untuk contoh ini, nomor KWP-2026-0001xxx). Jangan janji
>    "pasti hemat pajak" atau "dijamin gak kena periksa" ya, itu gak bisa dijamin siapapun

## Output agent (giliran 2)

`konten/PROFIL.md` disimpan: Konsul Pajak by Dina — jasa konsultasi & lapor SPT Tahunan UMKM — target
pemilik UMKM & freelancer — order WA 0817-0000-9012/form bio — 1 video/minggu — terdaftar Kuasa Wajib
Pajak KWP-2026-0001xxx (fiktif, contoh uji) — **kategori sensitif: keuangan** — dilarang klaim "pasti
hemat pajak"/"dijamin gak kena periksa".

```
python3 scripts/nomor_minggu.py --format json
```
Minggu default (sama seperti S2, dijalankan hari yang sama): **2026-W40**, Senin 28 Sep – Sabtu 03 Okt
2026.

```
# Paket Konten Minggu 2026-W40 — Konsul Pajak by Dina
Periode: Senin, 28 Sep 2026 s.d. Sabtu, 03 Okt 2026  |  Platform: LinkedIn, Instagram

## Senin 28 Sep 2026 — LinkedIn/Tulisan
Pilar: Edukasi pajak UMKM  |  Momen: -  |  Jam disarankan: 08.00-09.00 atau 12.00-13.00 (perkiraan kasar,
belum ada acuan khusus LinkedIn di skill ini — cek Analytics LinkedIn-mu sendiri untuk jam terbaik)
Hook 3 detik: "3 kesalahan UMKM saat lapor SPT Tahunan sendiri"
Caption:
Banyak pemilik UMKM baru sadar salah lapor SPT Tahunan setelah kena teguran. 3 kesalahan yang paling
sering saya temui: (1) salah pilih tarif PPh Final, (2) lupa lapor walau omzet kecil/nihil, (3) gak
simpan bukti potong. Kalau kamu masih bingung soal ini, yuk diskusi — DM atau WA aku.
Ini bukan nasihat pajak untuk kasus spesifikmu; tiap usaha beda, sebaiknya konsultasi langsung sebelum
ambil keputusan.
Order/Konsultasi: WA 0817-0000-9012
Naskah video: - (format tulisan, tidak perlu naskah)
Brief foto/video: foto profesional di meja kerja dengan laptop/dokumen pajak (rapi, tanpa data klien
asli terlihat di layar/dokumen)
Hashtag: #pajakumkm #sptTahunan #konsultanpajak #umkmindonesia (LinkedIn: 3-5 hashtag relevan, gaya
lebih formal dibanding IG)
CTA: DM/WA untuk konsultasi

---

## Selasa 29 Sep 2026 — Instagram Feed/Foto
Pilar: Edukasi pajak (repurpose dari LinkedIn, gaya lebih ringkas)  |  Momen: -  |  Jam disarankan:
11.00 & 19.30 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Omzet kecil tetap wajib lapor SPT? Ini jawabannya"
Caption:
Banyak yang kira omzet kecil = gak perlu lapor pajak. Faktanya, kalau kamu punya NPWP aktif, SPT
Tahunan tetap wajib dilapor walau nihil. Telat/gak lapor bisa kena sanksi administrasi.
Bingung cara lapornya? Yuk konsultasi dulu sebelum deadline. Setiap kondisi usaha beda, jadi ini bukan
pengganti konsultasi langsung untuk kasusmu.
Order: WA 0817-0000-9012 / link bio
Naskah video: - (format foto, tidak perlu naskah)
Brief foto/video: infografis sederhana "Wajib lapor walau nihil? YA" dengan ikon dokumen, warna netral
profesional
Hashtag: #pajakumkm #sptnihil #freelancerindonesia #konsultanpajak #umkmindonesia
CTA: WA untuk konsultasi sebelum deadline

---

## Rabu 30 Sep 2026 — LinkedIn/Video pendek
Pilar: Kredibilitas (perkenalan jasa)  |  Momen: Peringatan G30S (non-hardselling hari ini)  |  Jam
disarankan: 08.00-09.00 (perkiraan kasar, belum ada acuan khusus LinkedIn — cek Analytics sendiri)
Hook 3 detik: "Kenapa harus pakai Kuasa Wajib Pajak terdaftar, bukan sembarang jasa?"
Naskah video ±30 detik:
| Detik | Adegan | Teks di layar | VO/Narasi |
|---|---|---|---|
| 0-3 | Dina duduk di meja kerja, kamera menghadap ke depan | "Kenapa harus KWP terdaftar?" | "Kenapa harus pakai Kuasa Wajib Pajak yang terdaftar resmi, bukan sembarang jasa?" |
| 3-15 | Tunjukkan dokumen/sertifikat KWP (blur nomor asli bila perlu privasi) | "Terdaftar resmi (KWP-2026-0001xxx)" | "Karena aku terdaftar resmi sebagai Kuasa Wajib Pajak, bukan asal ngerti pajak doang" |
| 15-25 | Dina menjelaskan singkat manfaat konsultasi | "Konsultasi = paham posisi pajakmu" | "Konsultasi bareng aku bantu kamu paham posisi pajak usahamu, bukan janji hemat pajak instan" |
| 25-30 | Kontak & CTA | "WA: 0817-0000-9012" | "Kalau mau ngobrol soal pajak usahamu, WA aku aja" |
Brief foto/video: rekam wajah langsung (talking head), pencahayaan wajah jelas, background rapi/profesional
Hashtag: #kuasawajibpajak #konsultanpajak #pajakindonesia
CTA: WA untuk konsultasi
Catatan kepatuhan: hari ini Peringatan G30S — konten tetap non-promo (tidak ada penawaran/diskon),
murni edukasi & kredibilitas, sesuai checklist SKILL.md.

---

## Kamis 01 Okt 2026 — Instagram Story
Pilar: Interaksi ringan  |  Momen: Hari Kesaktian Pancasila (peringatan, non-hardselling) + Hari gajian
(tgl 1)  |  Jam disarankan: 11.00-13.00 & 19.00-21.00 (perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Sejauh mana kamu ngerti soal SPT usahamu sendiri?"
Caption: Poll: "SPT Tahunan usahamu: Sudah lapor tiap tahun ✅ / Sering telat 😅 / Belum pernah ngerti
caranya 🤯" (stiker poll IG Story)
Brief foto/video: teks pertanyaan di atas background warna netral/brand, tanpa data klien
Hashtag: (Story tidak perlu)
CTA: Vote, lanjut DM kalau mau tanya lebih lanjut

---

## Jumat 02 Okt 2026 — LinkedIn/Tulisan
Pilar: Studi kasus umum (tanpa data klien asli)  |  Momen: Hari Batik Nasional (tema, tidak dipaksakan
disinggung)  |  Jam disarankan: 08.00-09.00 atau 12.00-13.00 (perkiraan kasar — cek Analytics sendiri)
Hook 3 detik: "Contoh: UMKM kuliner omzet Rp40 juta/bulan, pajaknya berapa?"
Caption:
Ilustrasi umum (bukan data klien nyata): UMKM kuliner dengan omzet sekitar Rp40 juta/bulan biasanya
kena PPh Final UMKM 0,5% dari omzet bulanan sesuai PP 55/2022 (berlaku untuk WP dengan peredaran bruto
tertentu, dengan batas waktu pemanfaatan tarif final sesuai ketentuan — cek posisi usahamu tetap
disarankan lewat konsultasi, karena ada syarat & batas waktu yang bisa berbeda tiap usaha).
Contoh ini hanya ilustrasi kasar untuk edukasi, bukan perhitungan pajak final usahamu — tiap usaha
wajib dihitung sesuai kondisi masing-masing.
Mau tahu posisi pajak usahamu yang sebenarnya? DM/WA untuk konsultasi.
Naskah video: - (format tulisan, tidak perlu naskah)
Brief foto/video: grafis sederhana ilustrasi perhitungan (angka contoh, bukan data asli)
Hashtag: #pph final #pajakumkm #konsultanpajak #ppUMKM
CTA: DM/WA untuk konsultasi posisi pajak usahamu

---

## Sabtu 03 Okt 2026 — Instagram Feed/Foto
Pilar: Ajakan konsultasi (soft, bukan hardsell)  |  Momen: -  |  Jam disarankan: 10.00-12.00 (akhir
pekan bergeser lebih siang, perkiraan umum — cek Insights akun sendiri)
Hook 3 detik: "Weekend, waktu yang pas buat beresin dokumen pajak numpuk"
Caption:
Sebelum makin numpuk, yuk mulai rapikan dokumen pajak usahamu akhir pekan ini. Kalau butuh teman
diskusi buat mastiin langkahnya benar, aku siap bantu konsultasi — santai dulu ngobrol posisi pajakmu,
gak langsung dipaksa ambil paket apa-apa.
Order/Konsultasi: WA 0817-0000-9012
Naskah video: - (format foto, tidak perlu naskah)
Brief foto/video: foto dokumen tertata rapi + secangkir kopi, suasana santai weekend, tanpa data klien asli
Hashtag: #pajakumkm #konsultanpajak #weekendproductive
CTA: WA untuk ngobrol santai soal pajak usahamu

---

📥 Arsip disimpan: konten/minggu-2026-W40.md
📝 Asumsi: tidak ada asumsi tambahan — profil dijawab lengkap di wawancara giliran 2. Jam posting
LinkedIn adalah **perkiraan kasar** (bukan dari tabel referensi skill yang teruji, karena LinkedIn belum
tercakup di `references/gaya-caption.md`) — sebaiknya dikoreksi sendiri dari Analytics LinkedIn Dina.
⚠️ Ingat: paket ini belum terposting — jadwalkan sendiri (LinkedIn: jadwalkan lewat fitur native LinkedIn
bila tersedia di akunmu, atau kirim manual; Instagram: Meta Business Suite), atau aktifkan pengingat
harian OpenClaw.

⚠️ Catatan khusus kategori sensitif (jasa keuangan): tidak ada janji hemat pajak/lolos audit di semua
konten. Contoh perhitungan pajak di hari Jumat memakai angka ILUSTRASI, bukan data klien nyata, dan
diberi disclaimer eksplisit "hanya ilustrasi kasar, bukan perhitungan pajak usahamu" sesuai
`references/aturan-iklan.md` (kategori Keuangan/investasi/pinjaman).
```

## Catatan penguji
**Bagus:**
- Tidak ada satu pun janji "pasti hemat pajak"/"dijamin gak kena periksa" — semua ajakan berbunyi
  "konsultasi", "diskusi", "ngobrol posisi pajakmu", sesuai larangan eksplisit dari pengguna & tabel
  Keuangan di `references/aturan-iklan.md` (tanpa janji imbal hasil/hasil pasti).
- Contoh perhitungan pajak (Jumat) jelas ditandai **ilustrasi**, bukan data klien nyata, dan disclaimer
  "bukan perhitungan pajak usahamu" — ini penting karena angka pajak yang dikarang tanpa disclaimer bisa
  menyesatkan pembaca awam.
- Skill secara jujur memberi tahu di awal (giliran 1) bahwa LinkedIn belum punya tabel referensi
  khusus, dan konsisten memberi label "perkiraan kasar" di setiap jam posting LinkedIn — ini penanganan
  yang jujur terhadap keterbatasan, bukan mengarang seolah-olah ada data.

**Kurang / catatan (cacat nyata pada skill, bukan simulasi):**
- **Cacat SEDANG:** SKILL.md, `templates/PROFIL.md`, dan `references/gaya-caption.md` sama sekali tidak
  menyebut **LinkedIn** sebagai platform yang didukung, padahal target audiens skill ("pengusaha s/d
  usaha mapan dan profesional") sangat mungkin memakai LinkedIn (konsultan, jasa profesional, B2B).
  Deskripsi SKILL.md pun hanya menyebut "Instagram/TikTok/Facebook" di bagian Batasan. Akibatnya:
  (a) `templates/PROFIL.md` baris 23 "Platform aktif (IG/TikTok/FB/WA Status...)" perlu diisi manual di
  luar opsi yang disediakan, (b) tidak ada panduan panjang caption/hashtag/jam posting LinkedIn yang
  teruji, sehingga agent terpaksa menaksir sendiri dengan kualitas tidak konsisten antar-run.
  **Saran perbaikan konkret:** tambah baris LinkedIn di tabel `references/gaya-caption.md` (panjang
  caption 150-300 kata gaya profesional/storytelling, hashtag 3-5, jam ramai umum B2B 07.30-09.00 &
  12.00-13.00 hari kerja) dan tambahkan "LinkedIn" ke daftar opsi platform di `templates/PROFIL.md`
  baris 23 dan ke deskripsi SKILL.md.
- Naskah video LinkedIn (Rabu) memakai format "talking head" yang sebenarnya lebih umum dipakai untuk
  Reels/TikTok — SKILL.md tidak membedakan gaya naskah video per platform (LinkedIn video native vs
  Reels/TikTok), walau dalam praktik keduanya cukup mirip untuk video edukasi singkat. Ini **cacat
  ringan**, bukan salah signifikan.
