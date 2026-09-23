# Skenario 2 — Normal: Digital Marketing Specialist (lowongan Inggris, CV campur ID/EN)

## Input pengguna
```
Bikinkan surat lamaran dan sesuaikan CV saya dengan lowongan ini ya:

Digital Marketing Specialist - PT Kreasi Digital Nusantara (Jakarta Selatan)

Requirements:
- Minimum Bachelor degree in Marketing, Communication, or related field
- 2+ years experience in digital marketing, preferably F&B industry
- Proficient in Google Ads, Google Analytics, and Meta Ads Manager
- Strong understanding of SEO (Search Engine Optimization) and content strategy
- Experience managing social media campaigns (Instagram, TikTok)
- Familiar with budgeting and ROI reporting
- Good copywriting skills in Bahasa Indonesia and English

Responsibilities:
- Plan and execute paid campaigns across Google and Meta platforms
- Monitor campaign performance and optimize budget allocation
- Coordinate with content team for creative assets
- Prepare monthly performance reports for management

Data saya: Budi Santoso, Jakarta, 0813-0000-2222, budi.santoso@email.com.
Pengalaman: Marketing Executive di PT Kopi Nusantara 2022-2024, ngurus iklan
Instagram dan Facebook buat promosi produk kopi, bikin laporan performa campaign
bulanan buat manajemen, atur anggaran iklan bulanan dan analisis hasil penjualan.
Pendidikan S1 Ilmu Komunikasi, Universitas Indonesia, lulus 2021.
```

## Output

```
## Skor Kecocokan Kata Kunci
20% kata kunci lowongan ditemukan di draf CV awal (5/25)

Sudah ada: digital, marketing, ads, campaign, copywriting
Belum terlihat (dicek satu per satu ke Ibu/Bapak Budi sebelum ditambahkan):
- google, analytics → Sudahkah pernah pakai Google Ads / Google Analytics secara
  langsung, atau selama ini hanya Instagram & Facebook Ads?
- meta → CV menyebut "Facebook Ads", yang sama dengan "Meta Ads" (Meta = nama
  perusahaan induk Facebook/Instagram) — akan ditulis "Meta Ads Manager (Facebook &
  Instagram)" agar cocok dengan istilah di lowongan TANPA menambah klaim baru.
- seo, engine → Apakah pernah mengerjakan SEO/optimasi mesin pencari?
- budget, budgeting → CV menyebut "anggaran iklan" (istilah Indonesia untuk
  "budget/budgeting") — akan disamakan istilahnya di CV, bukan kemampuan baru.
- bachelor, degree, communication → sudah relevan (S1 Ilmu Komunikasi), hanya beda
  penulisan; akan ditulis dalam Bahasa Inggris juga di bagian pendidikan bila mau
  kirim CV versi Inggris.

Jawaban pengguna (diasumsikan default karena tidak dibalas ulang): belum pernah pakai
Google Ads/Analytics atau mengerjakan SEO secara langsung → kedua hal itu TIDAK
ditambahkan ke CV. Istilah "anggaran" dan "Facebook Ads" disamakan penulisannya
dengan "budget" dan "Meta Ads" karena itu pengalaman yang sama, hanya beda istilah —
bukan menambah pengalaman baru.

## CV Versi ATS (Bahasa Indonesia)
Budi Santoso
Jakarta · 0813-0000-2222 · budi.santoso@email.com

RINGKASAN PROFIL
Digital Marketing dengan 2 tahun pengalaman mengelola Meta Ads (Facebook &
Instagram) dan pelaporan performa campaign untuk brand F&B, termasuk pengelolaan
budget iklan bulanan.

PENGALAMAN KERJA
Marketing Executive — PT Kopi Nusantara (2022–2024)
- Mengelola Meta Ads (Facebook & Instagram Ads) untuk promosi produk kopi
- Menyusun laporan performa campaign bulanan untuk manajemen
- Mengatur budget iklan bulanan dan menganalisis hasil penjualan sebagai bahan
  evaluasi ROI

PENDIDIKAN
S1, Ilmu Komunikasi — Universitas Indonesia (2021)

KEAHLIAN
Copywriting, Meta Ads Manager (Facebook & Instagram), pelaporan campaign,
manajemen budget iklan

## Surat Lamaran (Formal)
Jakarta, [tanggal]

Kepada Yth.
Tim Rekrutmen PT Kreasi Digital Nusantara
di Jakarta Selatan

Dengan hormat,

Saya Budi Santoso, bermaksud melamar posisi Digital Marketing Specialist di PT
Kreasi Digital Nusantara. Selama 2 tahun sebagai Marketing Executive di PT Kopi
Nusantara, saya mengelola Meta Ads (Facebook & Instagram), menyusun laporan
performa campaign, dan mengatur budget iklan untuk brand F&B — pengalaman yang
relevan dengan kebutuhan posisi ini.

Saya lampirkan CV untuk bahan pertimbangan Bapak/Ibu, dan terbuka untuk dihubungi
guna wawancara lebih lanjut.

Hormat saya,
Budi Santoso

## Email Singkat
Subjek: Lamaran Posisi Digital Marketing Specialist – Budi Santoso

Selamat siang,

Saya Budi Santoso, ingin melamar posisi Digital Marketing Specialist. Saya memiliki
pengalaman 2 tahun mengelola Meta Ads dan pelaporan campaign untuk brand F&B. CV
terlampir untuk pertimbangan. Terima kasih.

Hormat saya,
Budi Santoso
0813-0000-2222

## Checklist Sebelum Kirim
- [x] Tidak ada pengalaman/gelar/sertifikat yang dikarang — Google Ads/Analytics
      dan SEO TIDAK ditambahkan karena belum pernah dipakai
- [x] CV versi ATS: satu kolom, tanpa tabel/foto
- [x] Tidak ada NIK/agama/status pernikahan
- [ ] Nama file disarankan: `CV - Budi Santoso - Digital Marketing Specialist.pdf`
- [ ] Simpan sebagai PDF sebelum dikirim
- [ ] Cek typo & konsistensi tanggal sebelum kirim
- [x] Skor kecocokan kata kunci sudah dijalankan dan disampaikan
- [x] Disclaimer: skor kata kunci adalah proksi sederhana, bukan jaminan lolos ATS

## Asumsi
- Belum pernah pakai Google Ads/Google Analytics/SEO secara langsung → tidak
  ditambahkan ke CV
- "Anggaran" dan "Facebook Ads" disamakan istilah dengan "budget" dan "Meta Ads"
  karena itu pengalaman yang sama (bukan penambahan pengalaman baru)
- Bahasa keluaran: Indonesia (CV versi Inggris bisa dibuat terpisah bila diminta)
```

## Catatan penguji
- Skor 20% (5/25) cocok dengan hasil script dan verifikasi manual independen.
- **Baik:** skill menangani sinonim "Meta" vs "Facebook" dan "budget" vs "anggaran"
  dengan benar sesuai prinsip Langkah 4 (menyamakan istilah untuk pengalaman yang
  SAMA, bukan mengarang baru) — ini nilai tambah nyata dibanding sekadar
  menambahkan kata dari daftar "hilang" secara membabi buta.
- **Cacat ringan:** SKILL.md tidak secara eksplisit mencontohkan langkah "samakan
  istilah sinonim/bilingual" ini — perilaku baik di atas adalah interpretasi agent,
  bukan instruksi tertulis. Saran: tambahkan satu kalimat di Langkah 4 SKILL.md,
  mis. "termasuk menyamakan istilah sinonim ID/EN (mis. anggaran=budget,
  Meta=Facebook) untuk pengalaman yang sama, tanpa menganggapnya pengalaman baru."
  agar konsisten di semua sesi.
- Kata "google" dan "engine" muncul di daftar hilang; wajar karena memang tidak
  ada di CV — sudah ditangani dengan benar (ditanyakan, tidak dikarang).
