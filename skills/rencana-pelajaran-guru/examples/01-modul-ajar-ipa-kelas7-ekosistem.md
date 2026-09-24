# Contoh 01 — Modul Ajar IPA Kelas 7 tentang Ekosistem

Dijalankan sendiri mengikuti `SKILL.md` (bukan uji independen — lihat `docs/program-beta.md`
untuk uji lanjutan oleh penguji terpisah).

## Input pengguna
> "buatkan modul ajar IPA kelas 7 tentang ekosistem 2 pertemuan"

## Info yang tidak disebutkan → asumsi dipakai
- JP per pertemuan tidak disebutkan → dipakai **3 JP/pertemuan** (alokasi umum IPA SMP),
  40 menit/JP (Fase D, SMP) → **120 menit per pertemuan**.
- Verifikasi lewat script:
  ```
  python3 scripts/hitung_alokasi_waktu.py --jenjang smp --jp 3 --pertemuan "15,90,15;10,95,15"
  ```
  Hasil: kedua pertemuan **COCOK** (120 menit vs target 120 menit). Lihat detail di bawah
  Format Output.

---

# MODUL AJAR — Ilmu Pengetahuan Alam (IPA)

## A. Informasi Umum
| | |
|---|---|
| Nama penyusun | [nama guru] |
| Institusi | [nama sekolah] |
| Tahun ajaran | 2026/2027 |
| Jenjang / Kelas | SMP / VII |
| Fase | D |
| Mata pelajaran | IPA |
| Topik | Ekosistem |
| Alokasi waktu | 2 pertemuan × 3 JP (120 menit/pertemuan) — *asumsi, sesuaikan bila jadwal sekolahmu beda* |
| Kompetensi awal | Siswa sudah mengenal makhluk hidup dan lingkungan sekitar (materi kelas SD) |
| Profil Lulusan yang dituju | Dimensi **Penalaran Kritis** dan **Kesehatan** *(padanan lama: Profil Pelajar Pancasila — Bernalar Kritis)* |
| Sarana & prasarana | Kertas HVS bekas, alat tulis, HP (kamera, untuk pertemuan 2), papan tulis |
| Target peserta didik | Reguler, 32 siswa/kelas |
| Model pembelajaran | Tatap muka, diskusi kelompok kecil (4–5 siswa) |

## B. Komponen Inti

### 1. Capaian Pembelajaran (CP)
*(cek CP resmi — cocokkan dengan dokumen resmi IPA Fase D dari BSKAP No. 046/H/KR/2025)*
Ringkasan umum: pada akhir Fase D, peserta didik memahami interaksi antarkomponen dalam
suatu ekosistem (biotik-abiotik), rantai makanan dan jaring-jaring makanan, serta pengaruh
aktivitas manusia terhadap keseimbangan ekosistem, dan mampu menyampaikan gagasan berbasis
data pengamatan sederhana.

### 2. Tujuan Pembelajaran
1. Menjelaskan komponen biotik dan abiotik pada ekosistem sawah/kebun di sekitar sekolah.
2. Menyusun rantai makanan dan jaring-jaring makanan dari hasil pengamatan sendiri.
3. Menganalisis dampak satu contoh aktivitas manusia (mis. penggunaan pestisida, alih
   fungsi sawah jadi perumahan) terhadap keseimbangan ekosistem tersebut.

### 3. Alur Tujuan Pembelajaran
| Pertemuan | Tujuan Pembelajaran | Indikator ketercapaian |
|---|---|---|
| 1 | TP 1 & 2 | Siswa dapat mendaftar ≥5 komponen biotik & abiotik dan menyusun 1 rantai makanan yang benar urutannya |
| 2 | TP 3 | Siswa dapat menjelaskan minimal 1 sebab-akibat aktivitas manusia terhadap ekosistem dengan alasan logis |

### 4. Pemahaman Bermakna
Ekosistem di sekitar kita (sawah, kebun, sungai kecil) saling terhubung — kalau satu
bagian terganggu (misalnya sawah berubah jadi perumahan atau penggunaan pestisida
berlebihan), dampaknya terasa sampai ke rantai makanan yang lebih tinggi, termasuk manusia.

### 5. Pertanyaan Pemantik
- "Kalau semua katak di sawah dekat rumahmu tiba-tiba hilang, apa yang mungkin terjadi
  pada jumlah hama dan hasil panen petani?"
- "Pernahkah kamu melihat sawah di sekitar rumahmu berubah jadi perumahan atau ruko? Apa
  yang terjadi pada hewan-hewan yang tadinya tinggal di sana?"

### 6. Kegiatan Pembelajaran

#### Pertemuan 1 (120 menit — pembukaan 15’ + inti 90’ + penutup 15’, **status COCOK**)
**Pembukaan (15 menit)**
- Guru menyapa, mengecek kehadiran, dan mengajukan pertanyaan pemantik pertama.
- Asesmen diagnostik: kuis lisan 3 pertanyaan cepat ("Sebutkan 3 makhluk hidup yang biasa
  kamu lihat di sawah/kebun dekat rumah", "Apa bedanya makhluk hidup dan benda mati?",
  "Pernah dengar kata 'ekosistem'? Menurutmu artinya apa?") — dicatat guru untuk melihat
  kesiapan kelas, tidak dinilai.

**Inti (90 menit)**
- (20’) Guru menjelaskan konsep komponen biotik & abiotik dengan contoh sawah/kebun sekolah,
  disertai gambar/foto nyata bila memungkinkan.
- (40’) Kerja kelompok (4–5 siswa): tiap kelompok mengamati foto/ilustrasi ekosistem sawah
  yang dibagikan guru (atau mengamati langsung kebun sekolah bila memungkinkan), mendaftar
  komponen biotik-abiotik yang ditemukan, lalu menyusun 1 rantai makanan di LKPD.
- (30’) Presentasi singkat 3–4 kelompok (5 menit/kelompok) + tanggapan guru meluruskan
  miskonsepsi umum (mis. "matahari bukan makhluk hidup tapi termasuk komponen abiotik
  penting").

**Penutup (15 menit)**
- Formatif: guru berkeliling selama kerja kelompok mengamati LKPD tiap kelompok (lembar
  pengamatan sederhana: sudah/belum bisa membedakan biotik-abiotik, sudah/belum bisa
  menyusun rantai makanan yang urut).
- Simpulan bersama + pertanyaan pemantik untuk pertemuan 2 diberikan sebagai bahan pikir di
  rumah (bukan tugas wajib).

#### Pertemuan 2 (120 menit — pembukaan 10’ + inti 95’ + penutup 15’, **status COCOK**)
**Pembukaan (10 menit)**
- Guru mengulas singkat rantai makanan pertemuan 1, lalu menyampaikan pertanyaan pemantik
  kedua (sawah berubah jadi perumahan).

**Inti (95 menit)**
- (25’) Diskusi kelas: dampak alih fungsi lahan sawah/kebun terhadap ekosistem — guru
  memandu dengan data sederhana (mis. cerita/berita lokal tentang sawah yang menyempit).
- (40’) Kerja kelompok: tiap kelompok memilih 1 aktivitas manusia (alih fungsi lahan,
  pestisida berlebihan, atau sampah plastik di sungai dekat sawah) dan menganalisis
  dampaknya terhadap rantai makanan yang disusun di pertemuan 1, dituliskan di LKPD.
- (30’) Presentasi kelompok + diskusi kelas tentang solusi sederhana yang bisa dilakukan
  siswa/keluarga (mis. tidak membuang sampah ke saluran air sawah).

**Penutup (15 menit)**
- Sumatif: 5 soal uraian singkat (lihat Lampiran) dikerjakan individu, 10 menit terakhir.
- Refleksi penutup pertemuan (lihat bagian 9).

### 7. Asesmen
| Jenis | Kapan | Instrumen | Yang dinilai |
|---|---|---|---|
| Diagnostik | Awal pertemuan 1 | Kuis lisan 3 pertanyaan | Kesiapan/pengetahuan awal tentang makhluk hidup & ekosistem |
| Formatif | Selama kerja kelompok pertemuan 1 & 2 | Lembar pengamatan guru (checklist per kelompok) | Proses menyusun rantai makanan & analisis dampak |
| Sumatif | Akhir pertemuan 2 | 5 soal uraian + kunci + rubrik (lihat Lampiran) | Ketercapaian TP 1–3 |

### 8. Pengayaan & Remedial (Diferensiasi)
- **Pengayaan** (sudah menguasai rantai makanan dasar): diminta menyusun **jaring-jaring
  makanan** (menghubungkan ≥2 rantai makanan) dan menjelaskan efek berantai bila satu
  spesies hilang.
- **Remedial** (masih tertukar biotik-abiotik/urutan rantai makanan): pendampingan
  kelompok kecil dengan kartu bergambar komponen ekosistem yang bisa disusun manual
  (menyusun kartu = memvisualkan rantai makanan, tidak hanya menulis).
- **Diferensiasi proses:** kelompok kesiapan awal rendah mendapat daftar komponen ekosistem
  sawah sebagai bank kata bantu; kelompok kesiapan tinggi menyusun sendiri tanpa bank kata.
- **Diferensiasi produk:** presentasi boleh dalam bentuk lisan, poster gambar, atau
  diagram — siswa memilih sesuai gaya belajarnya (visual/kinestetik/auditori).

### 9. Refleksi
- **Refleksi guru:** Apakah siswa bisa membedakan biotik-abiotik dengan tepat? Bagian mana
  yang paling banyak butuh pengulangan?
- **Refleksi peserta didik:**
  1. Apa hal baru yang kamu pelajari hari ini tentang ekosistem di sekitarmu?
  2. Bagian mana yang masih membingungkan?
  3. Satu hal yang akan kamu lakukan setelah tahu dampak sampah/pestisida ke ekosistem?

## C. Lampiran

### LKPD — "Ekosistem Sawah di Sekitar Kita"

```
Nama: ______________________   Kelas: VII___   Tanggal: _______

Petunjuk: Kerjakan bersama kelompokmu (4–5 orang). Amati gambar ekosistem sawah yang
dibagikan gurumu, lalu jawab pertanyaan berikut.

Bagian 1 — Ayo Amati
1. Tuliskan 5 komponen biotik (makhluk hidup) yang kamu temukan di gambar:
   _____________________________________________
2. Tuliskan 3 komponen abiotik (benda tak hidup) yang kamu temukan:
   _____________________________________________

Bagian 2 — Ayo Berlatih
3. Susun 1 rantai makanan dari komponen yang kamu temukan (contoh bentuk:
   padi → tikus → ular → elang):
   _____ → _____ → _____ → _____
4. (Pertemuan 2) Pilih salah satu: alih fungsi sawah jadi perumahan / pestisida
   berlebihan / sampah plastik di saluran air. Jelaskan dalam 3–4 kalimat apa
   dampaknya pada rantai makanan yang kamu susun di nomor 3.
   _____________________________________________

Bagian 3 — Ayo Simpulkan
5. Menurut kelompokmu, apa yang terjadi kalau salah satu makhluk hidup di rantai
   makananmu tiba-tiba hilang semua? Jelaskan alasannya.
   _____________________________________________

---
KUNCI JAWABAN & PANDUAN GURU (halaman terpisah)

1–2. Jawaban bervariasi sesuai gambar yang dibagikan guru — cek minimal 5 biotik & 3
     abiotik disebut benar (biotik = makhluk hidup: padi, tikus, ular, elang, katak,
     serangga; abiotik = benda tak hidup: air, tanah, sinar matahari, udara).
3. Urutan rantai makanan harus logis: produsen (tumbuhan) → konsumen 1 (herbivora) →
   konsumen 2 (karnivora) → konsumen 3 (jika ada). Contoh benar: padi → tikus → ular →
   elang. Tolak urutan terbalik (mis. elang → tikus → padi).
4. Jawaban kualitatif, nilai berdasarkan: (a) menyebut sebab-akibat yang masuk akal,
   (b) mengaitkan ke rantai makanan miliknya sendiri.
5. Jawaban terbuka; kunci konsepnya: hilangnya satu spesies memutus rantai makanan dan
   bisa membuat populasi lain melonjak (tanpa pemangsa) atau menurun (kehilangan sumber
   makanan) — bukan sekadar "ekosistem rusak" tanpa penjelasan.

Catatan bagi guru: miskonsepsi umum — siswa sering menganggap matahari/air bukan bagian
ekosistem karena "bukan makhluk hidup". Tekankan abiotik tetap komponen ekosistem yang
penting.
```

### Soal Evaluasi (Sumatif) + Kunci + Rubrik

```
SOAL URAIAN — IPA: Ekosistem (Kelas VII) — waktu 10 menit, 5 soal, tiap soal skor maks. 20

1. Sebutkan 2 komponen biotik dan 2 komponen abiotik pada ekosistem sawah. (skor 20)
2. Susun sebuah rantai makanan yang benar dari komponen berikut: elang, padi, tikus, ular.
   (skor 20)
3. Jelaskan apa yang dimaksud "jaring-jaring makanan" dan bedanya dengan "rantai
   makanan". (skor 20)
4. Sebuah sawah diubah menjadi perumahan. Jelaskan 2 dampak yang mungkin terjadi pada
   ekosistem di sekitarnya. (skor 20)
5. Menurutmu, apa satu tindakan sederhana yang bisa dilakukan siswa untuk menjaga
   ekosistem sawah/kebun di sekitar sekolah? Jelaskan alasannya. (skor 20)

--- KUNCI JAWABAN & RUBRIK (halaman guru) ---

1. Biotik: contoh padi, tikus, ular, katak, elang (sebutkan 2 apa saja yang benar).
   Abiotik: contoh air, tanah, sinar matahari, udara (sebutkan 2 apa saja yang benar).
   Skor 20 = keempatnya benar & tepat kategori; 10 = hanya 2-3 benar; 0 = salah kategori
   semua.

2. Urutan benar: padi → tikus → ular → elang (produsen → konsumen 1 → konsumen 2 →
   konsumen 3). Skor 20 = urutan tepat; 10 = komponen benar tapi urutan salah; 0 = tidak
   menjawab/asal.

3. Jaring-jaring makanan = gabungan beberapa rantai makanan yang saling berhubungan dalam
   satu ekosistem (satu makhluk hidup bisa dimakan oleh lebih dari satu jenis pemangsa).
   Rantai makanan = urutan tunggal makan-dimakan. Skor 20 = kedua konsep dijelaskan benar
   dan beda ditunjukkan; 10 = hanya salah satu dijelaskan benar; 0 = tertukar/salah total.

4. Contoh dampak yang diterima: berkurangnya habitat hewan sawah (tikus, katak, burung),
   hilangnya sumber makanan bagi predator alami, berkurangnya lahan resapan air/rawan
   banjir, terputusnya rantai makanan lokal. Skor 20 = 2 dampak logis & relevan
   dijelaskan; 10 = 1 dampak logis; 0 = tidak relevan/tidak menjawab.

5. Jawaban terbuka (mis. tidak membuang sampah ke saluran air sawah, mengajak keluarga
   mengurangi penggunaan pestisida rumah tangga, ikut program penghijauan sekolah).
   Skor 20 = tindakan konkret + alasan masuk akal; 10 = tindakan disebut tanpa alasan
   jelas; 0 = tidak relevan/tidak menjawab.

Nilai akhir = jumlah skor 5 soal (maksimum 100). Contoh: siswa mendapat 20+10+20+20+10 = 80.

Kategori (sesuaikan KKM sekolah):
90–100 Sangat Baik · 80–89 Baik · 70–79 Cukup · <70 Perlu Bimbingan/remedial
```

---

## Catatan penutup untuk guru (bagian akhir output skill)
```
Asumsi yang dipakai: 2 pertemuan × 3 JP (120 menit/pertemuan) — sesuaikan bila alokasi
IPA di sekolahmu berbeda. Alokasi ini sudah diverifikasi lewat
scripts/hitung_alokasi_waktu.py: kedua pertemuan berstatus COCOK (120 menit = 3 JP × 40 menit).

Cek sebelum dipakai: CP di atas adalah ringkasan umum — cocokkan dengan dokumen CP resmi
IPA Fase D dari sekolah/dinasmu (lihat references/dasar-kurikulum.md).

Mau saya (1) buatkan versi soal yang lebih menantang untuk kelas unggulan, (2) tambahkan
lembar pengamatan langsung ke kebun sekolah sebagai pengganti gambar, atau (3) buatkan versi
Bahasa Inggris untuk kelas bilingual?
```
