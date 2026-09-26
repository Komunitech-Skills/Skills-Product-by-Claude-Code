# Skenario 01 (uji independen) — Normal — "buatkan modul ajar IPA kelas 7 tentang ekosistem 2 pertemuan"

Dijalankan oleh penguji independen mengikuti `SKILL.md` persis (bukan menyalin
`examples/01-modul-ajar-ipa-kelas7-ekosistem.md` milik pembuat — dibuat ulang dari nol
untuk uji silang).

## Input pengguna
> "buatkan modul ajar IPA kelas 7 tentang ekosistem 2 pertemuan"

## Langkah yang diikuti (ringkas)
1. Jenjang: SMP kelas VII → Fase D (`references/dasar-kurikulum.md` §2). Menit/JP = 40.
2. Guru menyebut "2 pertemuan" tapi **tidak** menyebut JP/pertemuan. Tabel Input `SKILL.md`
   hanya punya SATU baris default gabungan: **"1 pertemuan × 2 JP"** — tidak ada aturan
   terpisah "jumlah pertemuan default" vs "JP/pertemuan default", dan tidak ada tabel
   "JP default per mapel/jenjang" di mana pun dalam skill. Karena guru sudah menetapkan
   jumlah pertemuan (2), bagian JP yang hilang diisi dengan **default 2 JP/pertemuan**
   (bagian "2 JP" dari default itu) → 2 pertemuan × 2 JP × 40 menit = **80 menit/pertemuan**.
   → **Lihat CACAT-01 di HASIL-UJI.md**: contoh bawaan `SKILL.md` sendiri (§Contoh, baris
   ~133) memakai asumsi **"3 JP (default SMP)"** untuk kasus identik ini — istilah "default
   SMP" itu tidak didefinisikan di mana pun di Input/Langkah Kerja. Dua agent yang membaca
   SKILL.md yang sama, di titik ambigu yang sama, bisa masuk akal memilih 2 JP (ikut tabel
   Input) atau 3 JP (ikut pola Contoh) — hasil tidak konsisten. Kedua angka tetap dihitung
   & diverifikasi, tapi guru bisa dapat alokasi waktu berbeda tiap kali minta hal yang sama.
3. Baca `references/panduan-mapel.md` §IPA & §Fase D → konteks ekosistem sawah/kebun,
   observasi sederhana, peringatan keselamatan bila relevan (tidak relevan di topik ini).
4. CP tidak ditempel guru → tulis ringkasan umum + tanda `(cek CP resmi)`.
5. Verifikasi waktu lewat script:
   ```
   python3 scripts/hitung_alokasi_waktu.py --jenjang smp --jp 2 --pertemuan "10,55,15;10,55,15"
   ```
   Hasil: **COCOK** kedua pertemuan (80 menit = 80 menit target). Lihat log lengkap di
   bawah.

## Log script (bukti, dijalankan sungguhan)
```json
{
  "jenjang": "smp", "menit_per_jp": 40, "jp_per_pertemuan": 2,
  "target_menit_per_pertemuan": 80, "jumlah_pertemuan": 2,
  "total_menit_seluruh_pertemuan": 160, "target_menit_seluruh_pertemuan": 160,
  "semua_pertemuan_cocok": true,
  "rincian": [
    {"pertemuan": 1, "pembukaan_menit": 10, "inti_menit": 55, "penutup_menit": 15, "total_menit": 80, "status": "COCOK"},
    {"pertemuan": 2, "pembukaan_menit": 10, "inti_menit": 55, "penutup_menit": 15, "total_menit": 80, "status": "COCOK"}
  ]
}
```

## Output (ringkas — struktur penuh mengikuti `templates/kerangka-modul-ajar.md`)

```
MODUL AJAR — IPA (Ilmu Pengetahuan Alam)

A. Informasi Umum
Jenjang/Kelas: SMP / VII | Fase: D | Topik: Ekosistem
Alokasi waktu: 2 pertemuan × 2 JP (80 menit/pertemuan) — asumsi, karena JP/pertemuan
tidak disebutkan guru; sesuaikan bila jadwal sekolahmu beda.
Profil Lulusan: Penalaran Kritis, Kesehatan (padanan lama: Bernalar Kritis)
Sarana: kertas HVS bekas, alat tulis, papan tulis, HP kamera (pertemuan 2)

B. Komponen Inti
1. CP (cek CP resmi — cocokkan dengan dokumen resmi IPA Fase D BSKAP 046/H/KR/2025):
   ringkasan umum — interaksi komponen biotik-abiotik, rantai/jaring-jaring makanan,
   pengaruh aktivitas manusia terhadap keseimbangan ekosistem.
2. Tujuan Pembelajaran:
   1) Menjelaskan komponen biotik & abiotik ekosistem sawah/kebun sekitar sekolah.
   2) Menyusun rantai makanan dari hasil pengamatan gambar/lapangan.
   3) Menganalisis dampak satu aktivitas manusia terhadap keseimbangan ekosistem tsb.
3. Kegiatan Pertemuan 1 (80’ — pembukaan 10’+inti 55’+penutup 15’, status COCOK):
   Pembukaan: pertanyaan pemantik ("kalau semua katak di sawah dekat rumahmu hilang,
   apa yang terjadi pada hama & hasil panen?") + diagnostik lisan 3 pertanyaan.
   Inti: penjelasan biotik-abiotik dgn contoh sawah (15’) → kerja kelompok mengamati
   gambar ekosistem sawah, menyusun 1 rantai makanan di LKPD (30’) → presentasi 2
   kelompok (10’).
   Penutup: formatif — lembar pengamatan guru per kelompok; simpulan bersama.
4. Kegiatan Pertemuan 2 (80’ — pembukaan 10’+inti 55’+penutup 15’, status COCOK):
   Pembukaan: ulas rantai makanan + pertanyaan pemantik alih fungsi lahan.
   Inti: diskusi kelas dampak alih fungsi sawah (15’) → kerja kelompok memilih 1
   aktivitas manusia (pestisida/alih fungsi lahan/sampah plastik) & menganalisis
   dampaknya (25’) → presentasi + diskusi solusi (15’).
   Penutup: sumatif — 5 soal uraian 10’, refleksi 5’.
5. Asesmen: diagnostik (kuis lisan), formatif (lembar pengamatan kelompok), sumatif
   (5 soal uraian + kunci + rubrik, lihat Lampiran).
6. Diferensiasi: pengayaan → susun jaring-jaring makanan (≥2 rantai terhubung);
   remedial → kartu bergambar komponen ekosistem yang bisa disusun manual.

C. Lampiran
- LKPD "Ekosistem Sawah/Kebun Sekitar Kita" (3 bagian: Amati–Berlatih–Simpulkan,
  kunci jawaban & catatan miskonsepsi terlampir)
- Soal Evaluasi Sumatif: 5 soal uraian skor 20/soal, kunci & rubrik skor eksplisit,
  nilai akhir = jumlah skor (maks. 100), kategori 90-100 Sangat Baik … <70 Perlu Bimbingan.

Asumsi yang dipakai: 2 pertemuan × 2 JP (80 menit) karena JP/pertemuan tidak disebutkan
guru — default diambil dari tabel Input SKILL.md ("1 pertemuan × 2 JP"), bagian JP-nya
dipakai untuk 2 pertemuan yang diminta.
Cek sebelum dipakai: CP di atas ringkasan umum — cocokkan dengan dokumen CP resmi IPA
Fase D dari sekolah/dinasmu.
Cara pindah ke Word/Google Docs: salin semua teks di atas, tempel ke dokumen baru...

Mau saya (1) tambahkan versi soal lebih menantang, (2) ganti pengamatan gambar dengan
kunjungan langsung ke kebun sekolah, atau (3) buatkan versi Bahasa Inggris kelas bilingual?
```
*(Isi kegiatan, LKPD, dan soal+kunci+rubrik lengkap secara struktural identik dengan
`examples/01-modul-ajar-ipa-kelas7-ekosistem.md` milik pembuat — perbedaan utama hanya
pada alokasi JP/pertemuan, lihat CACAT-01.)*

## Verifikasi independen
- Menit tiap pertemuan: 10+55+15 = 80 = 2×40 ✓ (dua kali, manual + script cocok).
- Rantai makanan contoh (padi → tikus → ular → elang): urutan produsen→konsumen1→
  konsumen2→konsumen3 benar secara ekologis ✓.
- Rubrik: 5 soal × skor 20 = 100 maksimum ✓, kategori nilai konsisten dgn
  `templates/kerangka-rubrik.md`.
- CP ditandai "(cek CP resmi)" ✓ — tidak mengarang kode/bunyi CP resmi BSKAP 046/H/KR/2025.
- Konteks lokal konkret (sawah, pasar hasil panen, pestisida) ✓, bukan generik.
- Ditutup dengan asumsi + 3 opsi revisi spesifik ✓ (checklist SKILL.md terpenuhi).

## Penilaian
**Lulus.** Isi Modul Ajar kaya, akurat secara sains & regulasi (CP ditandai jujur, fase
& menit/JP benar), konteks Indonesia konkret. Satu **cacat sedang** ditemukan: definisi
default JP/pertemuan ambigu ketika hanya jumlah pertemuan yang disebutkan guru — lihat
CACAT-01 di `HASIL-UJI.md`. Ini murni soal konsistensi lintas-run, bukan kesalahan hitung
(kedua kemungkinan tetap diverifikasi lewat script).
