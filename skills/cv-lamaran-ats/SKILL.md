---
name: cv-lamaran-ats
description: Menyesuaikan CV dan surat lamaran dengan lowongan kerja tertentu — profil pengalaman induk (satu sumber kebenaran riwayat asli), evaluasi kecocokan lowongan (skor + alasan + celah), format CV ramah ATS (satu kolom, tanpa tabel/foto), surat lamaran formal & email singkat, pesan WA/LinkedIn ke rekruter, skor kecocokan kata kunci dari script, latihan wawancara metode STAR, dan checklist sebelum kirim. Bahasa Indonesia & Inggris. Gunakan saat pengguna minta bikin/perbaiki CV, sesuaikan CV dengan lowongan, cover letter, surat lamaran kerja, tailor resume, ATS resume, cek kecocokan lowongan (job fit), latihan wawancara kerja, atau apply kerja. Untuk PENCARI kerja — bukan untuk perekrut/HR memasang lowongan (pakai lowongan-kerja).
---

# CV & Lamaran Ramah ATS

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Menyesuaikan CV dan surat lamaran pengguna dengan lowongan kerja tertentu, memakai kata kunci dari lowongan itu — **tanpa mengarang** pengalaman, gelar, sertifikat, atau tanggung jawab yang tidak dimiliki pengguna. Semua proses merujuk ke **profil pengalaman induk** pengguna (satu sumber kebenaran riwayat asli) agar konsisten di setiap lamaran. Hasil akhir: evaluasi kecocokan lowongan (skor + alasan + celah), CV versi ATS siap tempel, surat lamaran, pesan singkat ke rekruter, skor kecocokan kata kunci, dan (bila diminta) latihan wawancara berbasis STAR.

**Versi 1.1.1** (revisi rendah): `scripts/skor_kecocokan.py` menambah STOPWORDS kata pengisi lowongan yang lolos filter ("dipersilakan", "jujur", "melamar", "silakan", dan sejenisnya) agar tidak dihitung sebagai kata kunci; `references/evaluasi-kecocokan.md` sekarang menyebut eksplisit aturan normalisasi bobot saat satu dimensi skor tidak bisa dinilai (bobotnya dikeluarkan & dibagi proporsional ke dimensi lain, bukan dianggap 0). Uji regresi baru `tests/uji_regresi.py` (2 skenario).

## Kapan digunakan
- "Tolong sesuaikan CV saya dengan lowongan ini: [tempel lowongan]"
- "Bikinkan surat lamaran untuk posisi Admin di PT ABC"
- "CV saya kenapa nggak lolos ATS ya?"
- "Bikinkan pesan WA/LinkedIn buat kenalan sama HRD"
- "Review CV saya, cocok nggak sama lowongan Digital Marketing ini?"
- "Saya cocok nggak sih sama lowongan ini? Kasih skor sama alasannya"
- "Bantu saya bikin profil pengalaman biar nggak ngetik ulang tiap lamar kerja"
- "Latih saya wawancara buat posisi ini, pakai metode STAR"

## Kapan TIDAK digunakan
- Pengguna adalah **perekrut/HR** yang mau memasang iklan lowongan → `lowongan-kerja`.
- Pengguna minta CV/portofolio kreatif visual (desain grafis, motion, arsitektur) sebagai satu-satunya versi → tetap buat versi ATS teks dulu, lalu jelaskan versi visual dibuat terpisah dengan alat desain (Canva dsb.), bukan oleh skill ini.
- Pengguna minta menulis pengalaman/gelar/sertifikat/angka pencapaian yang **tidak dia miliki atau tidak bisa dia jelaskan** → tolak dengan sopan, jelaskan risikonya (bisa ketahuan saat wawancara, dan tidak etis), tawarkan alternatif jujur (mis. framing ulang pengalaman yang benar-benar ada).
- Menyusun perjanjian kerja/kontrak → `perjanjian-sederhana`.
- Surat peringatan atau evaluasi karyawan → `surat-peringatan-karyawan`.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Isi lowongan kerja (tempel teks lengkap, atau minimal posisi + kualifikasi + tanggung jawab) | Ya | — (tanyakan) |
| Profil pengalaman induk pengguna (lihat `references/profil-induk.md`): riwayat kerja, pendidikan, keahlian, kontak, ekspektasi gaji | Ya | Jika belum ada, buat sekali di awal (lihat Langkah 1); jika sudah ada CV lama, minta ditempel sebagai bahan |
| Bahasa keluaran: Indonesia / Inggris / dua-duanya | Tidak | Ikuti bahasa lowongan; jika campur, buat versi Indonesia utama |
| Butuh evaluasi kecocokan (skor + alasan) sebelum lanjut? | Tidak | Tawarkan sebelum menyusun CV; buat jika diminta atau pengguna ragu apakah layak melamar |
| Butuh surat lamaran juga? | Tidak | Ya, sertakan versi formal + email singkat |
| Butuh pesan WA/LinkedIn ke rekruter? | Tidak | Tawarkan, buat jika diminta |
| Butuh latihan wawancara STAR? | Tidak | Tawarkan setelah CV & surat lamaran selesai; buat jika diminta |
| Freshgraduate / pindah karier / berpengalaman | Tidak | Tebak dari data yang diberikan; sebutkan asumsi |

Jika data wajib kurang (terutama riwayat pengalaman pengguna), tanyakan **sekali** dalam satu pesan bernomor, maksimal 5 pertanyaan. Jangan pernah mengisi kekosongan riwayat kerja dengan karangan — minta pengguna mengisi atau kosongkan bagian itu.

## Langkah kerja

1. **Pastikan ada profil pengalaman induk** (lihat `references/profil-induk.md`). Jika pengguna belum pernah membuatnya di sesi ini/sebelumnya: minta CV lama (tempel teksnya, atau baca filenya bila agent bisa membuka file) atau daftar pengalaman/pendidikan/skill secara bebas, lalu susun jadi profil induk mengikuti format di referensi tersebut dan **tampilkan hasilnya ke pengguna** supaya bisa disimpan sendiri sebagai file. Jika pengguna sudah menempelkan profil induknya (dari sesi lalu), pakai itu langsung — jangan minta ulang. Kumpulkan juga **teks lowongan lengkap**. Jangan lanjut ke langkah berikutnya tanpa profil induk dan teks lowongan.

2. **Evaluasi kecocokan lowongan** mengikuti `references/evaluasi-kecocokan.md`: jalankan saringan wajib (syarat mutlak, lokasi, gaji), lalu hitung skor per dimensi berbasis profil induk — hasilkan skor akhir + alasan + celah. Tampilkan ke pengguna dan tanyakan apakah mau lanjut ke penyusunan CV (terutama jika skor di bawah 60 atau ada GAGAL SYARAT). Jika pengguna hanya minta "sesuaikan CV" tanpa evaluasi, tetap tampilkan evaluasi ringkas sebagai bagian dari output, kecuali pengguna secara eksplisit minta dilewati.

3. **Analisis kata kunci lowongan.** Pisahkan tugas: (a) *hard skill/tools* (mis. Excel, Google Ads, SQL, mesin bubut, akuntansi dasar), (b) *kualifikasi* (pendidikan, tahun pengalaman, sertifikasi), (c) *kata sifat/soft skill* yang sering dipakai rekruter (teliti, komunikatif, target-oriented).

4. **Jalankan skor kecocokan** dengan script (lihat bawah) untuk mendapat daftar kata kunci yang sudah/belum muncul di CV pengguna. Jika pengguna belum punya draf CV, lewati langkah ini dulu, susun draf CV pertama, baru jalankan skor pada draf tersebut untuk verifikasi akhir. **Saring hasil script sebelum ditampilkan:** buang kata umum/non-keahlian dan pecahan nama perusahaan yang lolos dari daftar stopword — tampilkan hanya kata kunci yang benar-benar keahlian, alat, atau kualifikasi.

5. **Cocokkan, jangan mengarang.** Untuk tiap kata kunci yang hilang, cek ke pengguna atau ke bahan yang diberikan: apakah dia sebenarnya punya pengalaman itu tapi belum ditulis (→ tambahkan dengan kalimat jujur), atau memang tidak punya (→ **biarkan hilang**, jangan dipaksakan masuk CV). Perhitungkan sinonim ID/EN dan nama lain yang setara (mis. Meta Ads = Facebook Ads, anggaran = budget, Excel = spreadsheet) — tulis istilah persis seperti di lowongan bila pengguna memang punya keahliannya.

6. **Susun CV versi ATS** mengikuti format di bawah: satu kolom, judul bagian standar, tanpa tabel/kolom ganda/foto/ikon/grafik batang skill, font dianggap standar (tidak perlu disebutkan karena ini teks). Urutan bagian: Data Diri → Ringkasan Profil (2–3 kalimat, mengandung kata kunci utama) → Pengalaman Kerja (urutan terbaru dulu, poin dengan kata kerja aktif + hasil terukur jika ada) → Pendidikan → Keahlian → (opsional) Sertifikasi/Organisasi/Bahasa.

7. **Tawarkan versi "visual" terpisah** (boleh pakai tabel/warna/ikon) hanya jika pengguna secara eksplisit minta untuk dikirim langsung ke perusahaan yang tidak pakai sistem ATS (mis. lewat email langsung ke pemilik usaha kecil) — jelaskan bahwa versi ATS tetap yang utama untuk lamaran online/portal karier.

8. **Susun surat lamaran** (jika diminta/default): versi formal Bahasa Indonesia untuk email/portal resmi, dan versi email singkat (3–4 kalimat) untuk lampiran cepat. Isi: posisi yang dilamar, satu-dua kalimat kecocokan berbasis kata kunci lowongan, ajakan untuk wawancara, lampiran CV.

9. **Susun pesan WA/LinkedIn ke rekruter** (jika diminta): sopan, singkat (maks. 4–5 kalimat), sebut posisi & sumber info lowongan, satu kalimat kecocokan, tanya kelanjutan proses. Jangan terkesan mendesak.

10. **Periksa etika data pribadi.** JANGAN sertakan NIK, agama, status pernikahan, suku, atau foto di CV **kecuali** pengguna secara eksplisit memintanya (biasanya untuk instansi tertentu yang mewajibkan). Ingatkan pengguna bila dia menyertakan data sensitif tanpa diminta lowongan.

11. **Jalankan checklist** sebelum menyerahkan hasil akhir (lihat Checklist di bawah).

12. **Latihan wawancara STAR** (opsional, jika diminta — biasanya setelah CV & surat lamaran selesai): ikuti `references/wawancara-star.md`. Ambil contoh situasi dari profil pengalaman induk, petakan ke kompetensi yang diminta lowongan, susun draf jawaban STAR, siapkan jawaban pertanyaan sulit umum, dan tawarkan sesi roleplay tanya-jawab. Jangan mengarang situasi STAR — jika profil induk belum punya cukup contoh, tanyakan dulu ke pengguna.

### Menjalankan skor kecocokan (script)
Path relatif terhadap folder yang berisi SKILL.md ini. Di Windows, ganti `python3` dengan `python` atau `py`.

```bash
python3 <folder-skill-ini>/scripts/skor_kecocokan.py --cv cv.txt --lowongan lowongan.txt --format teks
```

- Simpan isi CV (draf) ke file teks (`cv.txt`) dan isi lowongan ke file teks (`lowongan.txt`) terlebih dulu.
- Tambahkan `--format json` bila butuh data terstruktur, atau `--top 40` untuk menganalisis lebih banyak kata kunci pada lowongan panjang.
- Script hanya menghitung **kemunculan kata**, bukan menilai kualitas CV. Perlakukan hasilnya sebagai bahan diskusi dengan pengguna, bukan perintah untuk menambah kata secara membabi buta.
- **Fallback tanpa Python:** baca lowongan dan CV berdampingan, garis bawahi manual kata benda/istilah yang muncul berulang di lowongan (nama tools, keahlian, jenjang pendidikan), lalu cek satu per satu apakah ada di CV. Beri tahu pengguna bahwa pengecekan ini dilakukan manual, bukan lewat script.

## Format output

```
## Evaluasi Kecocokan Lowongan
(format lengkap: lihat references/evaluasi-kecocokan.md — skor per dimensi, alasan, celah, rekomendasi)

## Skor Kecocokan Kata Kunci
<X>% kata kunci lowongan ditemukan di CV (<n_cocok>/<n_total>)

Kata kunci yang sudah ada: ...
Kata kunci yang belum terlihat (cek relevansi, jangan dikarang): ...

## CV Versi ATS (Bahasa Indonesia)
[Nama Lengkap]
[Kota] · [No. HP] · [Email] · [LinkedIn jika ada]

RINGKASAN PROFIL
...

PENGALAMAN KERJA
[Jabatan] — [Perusahaan] ([Bulan Tahun]–[Bulan Tahun])
- ...

PENDIDIKAN
[Jenjang, Jurusan] — [Institusi] ([Tahun lulus])

KEAHLIAN
...

## Surat Lamaran (Formal)
...

## Email Singkat
Subjek: Lamaran Posisi <Nama Posisi> – <Nama Pelamar>
...

## Pesan WA/LinkedIn ke Rekruter (opsional)
...

## Latihan Wawancara STAR (opsional, jika diminta)
(format lengkap: lihat references/wawancara-star.md — pertanyaan perilaku + draf jawaban STAR dari profil induk, pertanyaan sulit umum, pertanyaan balik ke pewawancara)

## Checklist Sebelum Kirim
- [ ] ...

## Asumsi
- ...
```

## Contoh

**Input pengguna:** "Sesuaikan CV saya dengan lowongan Digital Marketing Specialist ini [tempel lowongan]. Pengalaman saya: Marketing Executive di PT Kopi Nusantara 2022–2024, urus Instagram Ads dan laporan performa campaign."

**Output (ringkas):**
```
## Skor Kecocokan Kata Kunci
48% kata kunci lowongan ditemukan di draf CV (12/25)
Belum terlihat: google ads, google analytics, seo, budget, brand f&b
→ Ditanyakan ke pengguna: apakah pernah pakai Google Ads/Analytics? (jawaban menentukan apakah ditambahkan)

## CV Versi ATS
Budi Santoso
Jakarta · 0812xxxxxxx · budi@email.com

RINGKASAN PROFIL
Digital Marketing dengan 2 tahun pengalaman mengelola Instagram Ads dan
pelaporan performa campaign untuk brand F&B...

PENGALAMAN KERJA
Marketing Executive — PT Kopi Nusantara (2022–2024)
- Mengelola Instagram Ads untuk promosi produk kopi, meningkatkan interaksi akun
- Menyusun laporan performa campaign bulanan untuk manajemen
...
```

## Checklist sebelum mengirim hasil
- [ ] Tidak ada pengalaman/gelar/sertifikat yang dikarang — semua berasal dari data pengguna
- [ ] CV versi ATS: satu kolom, tanpa tabel/kolom ganda/foto/grafik skill
- [ ] Tidak ada NIK/agama/status pernikahan kecuali diminta pengguna
- [ ] Nama file disarankan: `CV - [Nama] - [Posisi].pdf` (spasi diganti sesuai kebiasaan, hindari karakter aneh)
- [ ] Ingatkan simpan sebagai **PDF** sebelum dikirim (bukan .docx, agar format tidak berubah)
- [ ] Ingatkan cek typo & konsistensi tanggal/format sebelum kirim
- [ ] Skor kecocokan kata kunci sudah dijalankan dan disampaikan ke pengguna
- [ ] Disclaimer disampaikan: skor kata kunci adalah proksi sederhana, bukan jaminan lolos ATS/rekruter
- [ ] Evaluasi kecocokan (skor + alasan + celah) sudah disampaikan sebelum atau bersama CV
- [ ] Ekspektasi gaji yang dipakai berasal dari isian pengguna sendiri, bukan taksiran pasar yang dikarang

## Batasan & penanganan error
- Skill ini **tidak menjamin lolos ATS, lolos seleksi, atau diterima kerja** — hasil bergantung pada sistem ATS masing-masing perusahaan (berbeda-beda) dan penilaian manusia setelahnya. Sampaikan ini sebagai disclaimer singkat di output.
- Jika pengguna hanya punya sedikit pengalaman relevan (freshgraduate/pindah karier), jangan memaksakan kata kunci yang tidak nyambung; sarankan menonjolkan proyek kuliah, organisasi, magang, atau transferable skill yang jujur.
- Jika lowongan yang ditempel ternyata bukan lowongan kerja (mis. iklan produk), beri tahu pengguna dan minta teks lowongan yang benar.
- Jika script Python gagal dijalankan atau tidak tersedia, pakai fallback manual di atas dan sampaikan ke pengguna bahwa skor belum diverifikasi lewat script.
- Jangan mengirim isi CV/data pribadi pengguna ke layanan eksternal mana pun; semua proses berjalan lokal. Skill ini **tidak melakukan scraping otomatis** ke LinkedIn/portal kerja mana pun — lowongan hanya diproses dari teks yang ditempel pengguna.
- **CPNS/BUMN:** skill ini hanya membantu menyesuaikan CV/surat lamaran dan menilai kecocokan umum; **tidak** mengecek syarat administratif spesifik suatu formasi/periode (usia, IPK, jenis kebutuhan) — arahkan pengguna ke pengumuman resmi instansi/BKN/portal rekrutmen BUMN yang dituju.
- Latihan wawancara STAR adalah simulasi bantu-belajar berbasis pengalaman nyata pengguna — bukan jaminan hasil wawancara sungguhan, dan tidak menggantikan riset pengguna tentang perusahaan.
- Untuk kasus hukum ketenagakerjaan (kontrak, PHK, perselisihan, negosiasi gaji yang sudah masuk ranah kontrak) → arahkan ke konsultan/pengacara, di luar cakupan skill ini.
