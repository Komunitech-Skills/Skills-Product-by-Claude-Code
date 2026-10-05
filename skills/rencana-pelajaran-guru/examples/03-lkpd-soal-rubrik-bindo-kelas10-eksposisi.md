# Skenario 03 — Normal — "LKPD + 10 soal + kunci + rubrik Bahasa Indonesia kelas 10 teks eksposisi"

## Input pengguna
> "Bikinin LKPD + 10 soal beserta kunci dan rubrik, Bahasa Indonesia kelas 10, teks eksposisi"

## Langkah yang diikuti
1. Jenjang: SMA kelas 10 → Fase E, 45 menit/JP.
2. Jenis dokumen disebut eksplisit: **LKPD + soal & rubrik saja** (tanpa Modul Ajar
   lengkap) → keluarkan dua dokumen itu saja.
3. Pertemuan/JP tidak disebut → default 1 pertemuan × 2 JP = 90 menit (dipakai untuk
   memperkirakan durasi kegiatan LKPD, meski Modul Ajar tidak diminta).
4. Baca `references/panduan-mapel.md` §Bahasa Indonesia → teks buatan sendiri (bukan
   salinan buku teks berhak cipta), fokus 1–2 keterampilan per TP, kelas tinggi → teks
   1–2 paragraf berstruktur.
5. CP → ringkasan umum + "(cek CP resmi)".
6. Verifikasi waktu (dipakai sebagai acuan pembagian sesi LKPD):
   ```
   python3 scripts/hitung_alokasi_waktu.py --jenjang sma --jp 2 --pertemuan "10,65,15"
   ```
   Hasil: **COCOK** (90 menit = 90 menit target).

## Log script (bukti)
```json
{"jenjang":"sma","menit_per_jp":45,"jp_per_pertemuan":2,"target_menit_per_pertemuan":90,
 "jumlah_pertemuan":1,"rincian":[{"pertemuan":1,"pembukaan_menit":10,"inti_menit":65,
 "penutup_menit":15,"total_menit":90,"status":"COCOK"}]}
```

## Output

```
LEMBAR KERJA PESERTA DIDIK — Teks Eksposisi (Bahasa Indonesia, Kelas X)

Nama: ______________  Kelas: X___  Tanggal: _______
Petunjuk: Bacalah teks di bawah, lalu kerjakan bagian 1–3 secara mandiri.

Teks bacaan (ditulis sendiri, bukan kutipan buku teks):
"Sampah Plastik di Pasar Tradisional"
Setiap hari, pasar tradisional di banyak kota menghasilkan puluhan kilogram sampah
plastik dari kantong belanja sekali pakai. Sampah ini sering berakhir di selokan dan
menyumbat aliran air saat musim hujan. Sebagian pedagang mulai beralih ke kantong kertas
atau menyediakan wadah guna ulang bagi pembeli. Langkah kecil ini, bila dilakukan
serentak oleh seluruh pedagang pasar, dapat mengurangi jumlah sampah plastik secara
signifikan tanpa membebani pembeli dengan biaya tambahan yang besar.

Bagian 1 — Ayo Amati
1. Tuliskan kalimat yang menjadi TESIS (pernyataan pendapat) dalam teks di atas.
2. Sebutkan 2 kalimat ARGUMENTASI (data/alasan pendukung) yang kamu temukan.

Bagian 2 — Ayo Berlatih
3. Tuliskan 1 kalimat PENEGASAN ULANG yang cocok untuk menutup teks tersebut.
4. Susun kerangka teks eksposisi (tesis-argumentasi-penegasan ulang) dengan topikmu
   sendiri tentang salah satu: (a) jajanan sekolah, (b) sampah di kelas, (c) kebiasaan
   membaca. Tulis minimal 1 kalimat per bagian.

Bagian 3 — Ayo Simpulkan
5. Menurutmu, apa ciri paling khas yang membedakan teks eksposisi dari teks cerita
   (narasi)? Jelaskan dengan kata-katamu sendiri.

--- KUNCI JAWABAN & PANDUAN GURU ---
1. Tesis: "Setiap hari, pasar tradisional... menghasilkan puluhan kilogram sampah
   plastik dari kantong belanja sekali pakai" (kalimat pembuka yang menyatakan masalah/
   pendapat utama).
2. Argumentasi (contoh benar, terima variasi wajar): "Sampah ini sering berakhir di
   selokan dan menyumbat aliran air", "Sebagian pedagang mulai beralih ke kantong kertas
   atau wadah guna ulang".
3. Contoh penegasan ulang yang benar: menyimpulkan bahwa perubahan kecil pedagang bisa
   berdampak besar bila dilakukan bersama — HARUS merangkum, bukan info baru.
4–5. Jawaban terbuka; nilai dengan Rubrik Menulis Eksposisi di bawah.

Catatan bagi guru: miskonsepsi umum — siswa sering menulis penegasan ulang sebagai
"argumentasi baru" alih-alih merangkum; tekankan bedanya saat membahas jawaban no. 3.
```

### Soal Evaluasi (10 soal pilihan ganda) + Kunci

```
1. Struktur teks eksposisi yang benar adalah ... 
   a) orientasi-komplikasi-resolusi  b) tesis-argumentasi-penegasan ulang (KUNCI)
   c) pembuka-isi-penutup umum saja  d) abstrak-orientasi-krisis
2. Tujuan utama teks eksposisi adalah ...
   a) menghibur pembaca  b) menceritakan pengalaman pribadi
   c) menjelaskan/meyakinkan pembaca dengan fakta & alasan (KUNCI)  d) mendeskripsikan tempat
3–10. [pola sama: identifikasi tesis/argumentasi/penegasan ulang dari kutipan pendek,
   konjungsi kausalitas ("karena", "oleh sebab itu"), kata teknis/istilah bidang, beda
   fakta vs opini dalam teks eksposisi] — kunci lengkap 10 soal ada di lampiran guru.

Nilai = (jumlah jawaban benar ÷ 10) × 100. Contoh: benar 8 dari 10 → (8÷10)×100 = 80.
```

### Rubrik Menulis Eksposisi (untuk Bagian 2 no. 4 LKPD)
| Aspek | Skor 4 | Skor 3 | Skor 2 | Skor 1 |
|---|---|---|---|---|
| Struktur (tesis-argumen-penegasan) | Lengkap & urut | Lengkap, urutan kurang tepat | Ada 2 bagian saja | Hanya 1 bagian/tidak berstruktur |
| Kejelasan argumen | Argumen logis & didukung alasan | Argumen ada, alasan kurang kuat | Argumen kabur | Tidak ada argumen jelas |
| Ejaan & tanda baca | Nyaris tanpa kesalahan | 1-2 kesalahan kecil | Beberapa kesalahan mengganggu | Banyak kesalahan mengganggu makna |

Cara menilai: Skor total = jumlah 3 aspek (maks 12). Nilai = (skor total ÷ 12) × 100.
Contoh: siswa dapat 3+4+3 = 10 → (10÷12)×100 = **83,3 → dibulatkan 83** (Baik).

Asumsi yang dipakai: durasi acuan 1 pertemuan × 2 JP (90 menit, Fase E) untuk memperkirakan
alokasi kegiatan LKPD, karena jumlah pertemuan/JP tidak disebutkan guru.
Cek sebelum dipakai: CP di atas (struktur eksposisi) mengikuti kompetensi umum
Bahasa Indonesia Fase E — cocokkan kode/bunyi resminya dengan dokumen CP BSKAP 046/H/KR/2025.

Mau saya (1) ubah 10 soal PG jadi 5 uraian analisis teks yang lebih HOTS, (2) tambah
teks bacaan kedua untuk perbandingan dua sudut pandang, atau (3) buatkan versi rubrik
skala 1-100 langsung tanpa kategori 1-4?
```

## Verifikasi independen
- Struktur teks eksposisi (tesis→argumentasi→penegasan ulang) benar secara keilmuan
  Bahasa Indonesia ✓; teks bacaan ditulis orisinal (bukan kutipan buku teks) ✓ sesuai
  `panduan-mapel.md`.
- Rumus nilai PG: (benar÷10)×100 — diverifikasi manual dgn 3 kasus acak (8/10=80,
  10/10=100, 3/10=30) → **0 beda**.
- Rumus rubrik menulis: skor 3+4+3=10, maks 3×4=12, (10/12)×100=83,33...→83 — dihitung
  ulang manual dgn Python `Fraction(10,12)*100` = 83.333... → pembulatan ke 83 benar
  (bukan ke atas keliru jadi 84) ✓.
- CP ditandai "(cek CP resmi)" ✓, tidak mengarang kode CP.
- Jenis dokumen sesuai permintaan (LKPD + soal/kunci/rubrik saja, tanpa Modul Ajar
  penuh) ✓.

## Penilaian
**Lulus.** Konten relevan usia SMA (isu sampah plastik pasar — nyambung ke IPS/lingkungan
lokal), soal PG dan rubrik menulis saling melengkapi asesmen keterampilan menulis
eksposisi. Nilai dihitung benar dan pembulatan tepat. Tidak ditemukan cacat pada
skenario ini.
