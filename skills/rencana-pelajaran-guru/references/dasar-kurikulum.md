# Dasar aturan Kurikulum Merdeka & Pembelajaran Mendalam (dicek 2026-09-24)

Ringkasan ini dipakai `SKILL.md` sebagai acuan. Regulasi pendidikan Indonesia sering
diperbarui — **selalu utamakan Capaian Pembelajaran (CP) resmi dan aturan sekolah/yayasan
sendiri** di atas ringkasan ini. Terakhir diverifikasi lewat pencarian web (bukan akses
langsung situs Kemendikdasmen dari lingkungan kerja) pada **2026-09-24**.

## 1. Payung hukum yang berlaku (2025/2026)

| Regulasi | Mengatur |
|---|---|
| **Permendikbudristek No. 12 Tahun 2024** | Kurikulum Merdeka ditetapkan sebagai kurikulum nasional (struktur mata pelajaran, alokasi jam per jenjang). |
| **Permendikdasmen No. 13 Tahun 2025** | Penguatan kebijakan lewat **Pembelajaran Mendalam (Deep Learning)** — bukan kurikulum baru, satuan pendidikan boleh tetap memakai Kurikulum 2013 atau Kurikulum Merdeka. Mengganti istilah **"Profil Pelajar Pancasila"** (6 dimensi) menjadi **"Profil Lulusan"** (8 dimensi), terintegrasi dengan Permendikdasmen No. 10/2025 (Standar Kompetensi Lulusan) dan No. 12/2025 (Standar Isi). Menambahkan mapel pilihan Koding & Kecerdasan Artifisial (kelas 5–12, bertahap). |
| **Keputusan Kepala BSKAP No. 046/H/KR/2025** | Capaian Pembelajaran (CP) terbaru untuk PAUD, pendidikan dasar, dan menengah — **mencabut** CP lama (BSKAP No. 32/H/KR/2024). CP tetap tersusun dalam **6 fase (A–F)**. |

**Kesimpulan praktis untuk skill ini:**
- Struktur **Modul Ajar** (pengganti istilah RPP di Kurikulum Merdeka) dan komponen CP/ATP
  tetap dipakai.
- Istilah **"Profil Lulusan" (8 dimensi)** adalah istilah terbaru; **"Profil Pelajar
  Pancasila" (6 dimensi)** masih lazim dipakai sekolah yang belum memperbarui dokumen —
  skill ini memakai istilah yang guru minta, dan bila tidak disebutkan memakai istilah
  terbaru "Profil Lulusan" sambil mencatat padanan dimensi lama jika relevan.
- **Nama 8 dimensi Profil Lulusan (Permendikdasmen No. 10 Tahun 2025 tentang SKL; dicek 2026-10-01)** — salin persis, jangan diparafrasekan: (1) Keimanan dan Ketakwaan terhadap Tuhan YME, (2) Kewargaan, (3) Penalaran Kritis, (4) Kreativitas, (5) Kolaborasi, (6) Kemandirian, (7) Kesehatan, (8) Komunikasi. Padanan lama (Profil Pelajar Pancasila, 6 dimensi): Bernalar Kritis -> Penalaran Kritis, Gotong Royong -> Kolaborasi, Mandiri -> Kemandirian, Kreatif -> Kreativitas. Verifikasi ulang ke dokumen resmi Kemendikdasmen bila ragu.
- **"Deep Learning"/Pembelajaran Mendalam** adalah *pendekatan* (berkesadaran, bermakna,
  menggembirakan) yang menekankan pembelajaran lintas tema/mapel dan pemahaman mendalam —
  bukan format dokumen baru. Skill ini menambahkan sentuhan pendekatan ini (kaitkan topik
  dengan konteks nyata siswa, hindari sekadar hafalan) tanpa mengubah struktur Modul Ajar.

## 2. Fase Capaian Pembelajaran (CP)

| Fase | Jenjang / kelas |
|---|---|
| A | SD/MI kelas 1–2 |
| B | SD/MI kelas 3–4 |
| C | SD/MI kelas 5–6 |
| D | SMP/MTs kelas 7–9 |
| E | SMA/SMK/MA kelas 10 |
| F | SMA/SMK/MA kelas 11–12 |

**PENTING — jangan mengarang teks CP.** Kode dan bunyi CP resmi per mata pelajaran dan
fase ditetapkan BSKAP No. 046/H/KR/2025 dan bisa berubah/direvisi. Skill ini **tidak**
menyimpan basis data teks CP resmi. Jika guru tidak menempelkan teks CP dari dokumen
resmi, tulis CP sebagai **ringkasan umum** yang ditandai jelas `(cek CP resmi — cocokkan
dengan dokumen resmi mapel & fase ini)`, dan susun Tujuan Pembelajaran + Alur Tujuan
Pembelajaran dari ringkasan itu. Ini sama seperti prinsip *copyright guardrail* pada
skill sumber (`k12-lesson-plan-creation`, Anthropic/Learning Commons): jangan mereproduksi
teks kurikulum resmi verbatim tanpa sumber yang dipastikan.

## 3. Alokasi waktu 1 Jam Pelajaran (JP)

| Jenjang | 1 JP |
|---|---|
| SD/MI | 35 menit |
| SMP/MTs | 40 menit |
| SMA/MA/SMK | 45 menit |

Total menit pertemuan = jumlah JP × menit per JP jenjang tersebut. Contoh: SMP 3 JP =
3 × 40 = 120 menit. Skill ini **menghitung** total menit ini (lihat
`scripts/hitung_alokasi_waktu.py`), tidak menerka-nerka, dan memberi peringatan bila
jumlah menit kegiatan (pembukaan+inti+penutup) tidak sama dengan total JP yang diminta.

## 4. Komponen Modul Ajar (ringkas)

**A. Informasi Umum** — identitas (nama guru/sekolah, mapel, jenjang/kelas, fase,
alokasi waktu), kompetensi awal (prasyarat), Profil Lulusan/Profil Pelajar Pancasila yang
dituju, sarana-prasarana, target peserta didik, model pembelajaran.

**B. Komponen Inti** — Capaian Pembelajaran, Tujuan Pembelajaran (kata kerja operasional,
terukur), Alur Tujuan Pembelajaran (bila lebih dari 1 pertemuan/unit), pemahaman bermakna,
pertanyaan pemantik, kegiatan pembelajaran (pembuka–inti–penutup per pertemuan), asesmen
(diagnostik/formatif/sumatif beserta instrumennya), pengayaan & remedial (diferensiasi
konten/proses/produk), refleksi guru dan peserta didik.

**C. Lampiran** — LKPD, bahan bacaan/materi ajar ringkas, glosarium, daftar pustaka,
rubrik penilaian.

**RPP 1 lembar** memuat versi ringkas komponen inti saja (tujuan, langkah kegiatan
singkat, asesmen) — dipakai sebagian sekolah/dinas sebagai pelengkap administrasi,
**bukan pengganti** Modul Ajar lengkap untuk pengarsipan kurikulum.

## 5. Catatan format sekolah berbeda-beda

Setiap sekolah/yayasan/dinas boleh punya format Modul Ajar/RPP tersendiri (kop surat,
urutan komponen, kolom tanda tangan kepala sekolah, dll). **Jika guru melampirkan atau
menyebut template sekolahnya, ikuti template itu** — isi templatenya dengan hasil
langkah kerja skill ini, jangan memaksakan format Komunitech.

## Sumber (diakses 2026-09-24)

- Kemendikdasmen — siaran pers Permendikdasmen No. 13/2025: https://www.kemendikdasmen.go.id/siaran-pers/13278-permendikdasmen-nomor-13-tahun-2025-menguatkan-arah-kebijakan-melalui-pembelajaran-mendalam
- GTK Kemendikdasmen — siaran pers Permendikdasmen No. 13/2025: https://gtk.kemendikdasmen.go.id/news/siaran-pers/c034d26f-83b6-4b4b-926c-b572e665e477
- Puslapdik Kemendikdasmen — Permendikdasmen No. 13/2025 memperkuat K13 & Kurikulum Merdeka: https://puslapdik.kemendikdasmen.go.id/permendikdasmen-no-13-tahun-2025-memperkuat-kurikulum-2013-dan-kurikulum-merdeka/
- detikEdu — Profil Pelajar Pancasila ganti istilah jadi Profil Lulusan (8 dimensi): https://www.detik.com/edu/sekolah/d-8024208/profil-pelajar-pancasila-kini-ganti-istilah-jadi-profil-lulusan-apa-bedanya
- detikEdu — Kemendikdasmen ganti P5 jadi Profil Lulusan 8 dimensi: https://www.detik.com/edu/sekolah/d-7807992/kemendikdasmen-ganti-p5-jadi-profil-lulusan-8-dimensi
- Peraturan BPK — teks Permendikdasmen No. 13 Tahun 2025 (PDF resmi): https://peraturan.bpk.go.id/Download/384307/Permendikdasmen-no-13-tahun-2025.pdf
- Blog Susanto — ringkasan alokasi JP per jenjang berdasarkan Permendikdasmen No. 13/2025: https://blogsusanto.com/jam-pelajaran-kurikulum-merdeka-tahun-ajaran-2025-2026-berdasarkan-permendikdasmen-nomor-13-2025/
- Kutipan berita CP terbaru (BSKAP No. 046/H/KR/2025 mencabut No. 32/H/KR/2024, fase A–F tetap): https://news.detik.com/berita/d-8022378/link-download-pdf-capaian-pembelajaran-cp-terbaru-2025-cek-di-sini dan https://www.imrantululi.net/read/285/kemendikdasmen-luncurkan-capaian-pembelajaran-terbaru-2025-untuk-dukung-kurikulum-merdeka-berbasis-deep-learning

**Disclaimer:** ringkasan ini disusun dari liputan media pendidikan dan situs resmi
Kemendikdasmen per tanggal akses di atas, bukan salinan hukum lengkap. Untuk kebutuhan
formal (akreditasi, supervisi dinas, pengarsipan kurikulum operasional satuan
pendidikan/KOSP), rujuk teks resmi peraturan dan CP dari sumber di atas atau dari dinas
pendidikan/yayasan setempat.
