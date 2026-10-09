# Contoh 3 - Kursus Excel online, Google Ads

> Contoh uji pembuat (simulasi agent, 2026-09-26; output diperbarui ke v1.0.1). Data fiktif yang meniru kasus UMKM nyata;
> bukan hasil uji independen (itu dilakukan penguji terpisah sesuai CLAUDE.md Tahap 6).

## Permintaan pengguna
"Saya jualan kursus Excel online lewat Google Ads, klik banyak tapi pendaftar sedikit. Audit dong."

## Bukti yang diberikan (diringkas agent ke file jawaban)
Screenshot Tujuan > Konversi, setelan kampanye (jaringan, lokasi), daftar kata kunci, laporan
istilah penelusuran 30 hari, dan tab Aset. Kursus melayani seluruh Indonesia sehingga G08
`tidak_berlaku`. Ringkasan: [`uji-pembuat-03-jawaban-kursus-online-google.csv`](uji-pembuat-03-jawaban-kursus-online-google.csv).

## Perintah yang dijalankan
```bash
python3 scripts/skor_audit.py hitung examples/uji-pembuat-03-jawaban-kursus-online-google.csv --usaha "Kursus Excel online" --mulai 2026-09-28
```

## Output script (disalin apa adanya)
```
AUDIT KESEHATAN AKUN IKLAN - Kursus Excel online
================================================
Skor gabungan: 43,3 / 100 (Kritis) - FINAL; bobot: satu platform

PER PLATFORM
- Google Ads: 43,3/100 (Kritis); bukti 93,3% (final)
    Pelacakan & konversi: 42,9 (bobot 25)
    Struktur & akses akun: 59,1 (bobot 15)
    Target & audiens: 0,0 (bobot 10)
    Anggaran & bidding: 100,0 (bobot 15)
    Materi iklan: 37,5 (bobot 10)
    Halaman tujuan / etalase: 50,0 (bobot 10)
    Pengecualian: 0,0 (bobot 15)

PRIORITAS PERBAIKAN (dampak x kemudahan; skor tertinggi dikerjakan dulu)
1. [G02] Hanya aksi bernilai yang jadi konversi utama - Google Ads; kritis, mudah; prioritas 15; skor platform naik +8,9 bila beres
   Perbaikan: Ubah aksi yang tidak bernilai menjadi Sekunder
   Catatan audit: "Kunjungan halaman" ikut jadi konversi Utama
2. [G15] Istilah penelusuran dicek dan kata kunci negatif dipasang - Google Ads; tinggi, mudah; prioritas 9; skor platform naik +11,3 bila beres
   Perbaikan: Tambahkan istilah yang tidak relevan sebagai kata kunci negatif di kampanye Penelusuran dan di Performance Max (berlaku untuk inventaris Penelusuran & Shopping)
   Catatan audit: Pencarian "kursus excel gratis pdf" menghabiskan 22% biaya
3. [G03] Cara hitung konversi benar - Google Ads; tinggi, mudah; prioritas 9; skor platform naik +5,4 bila beres
   Perbaikan: Ubah pengaturan Hitungan pada aksi konversi
   Catatan audit: Lead dihitung Setiap
4. [G07] Kampanye Penelusuran tidak ikut Jaringan Display - Google Ads; tinggi, mudah; prioritas 9; skor platform naik +4,1 bila beres
   Perbaikan: Hapus centang Jaringan Display di kampanye Penelusuran
   Catatan audit: Jaringan Display masih dicentang
5. [G12] Iklan responsif kuat - Google Ads; tinggi, mudah; prioritas 9; skor platform naik +3,8 bila beres (status: sebagian)
   Perbaikan: Isi 10-15 judul & 4 deskripsi: kata kunci, harga/jadwal, keunggulan, ajakan
   Catatan audit: Kekuatan iklan Rata-rata
6. [G09] Jenis pencocokan sesuai kesiapan data - Google Ads; tinggi, sedang; prioritas 6; skor platform naik +10,0 bila beres
   Perbaikan: Ubah kata kunci luas menjadi frasa/tepat sampai konversi tercatat stabil
   Catatan audit: Semua kata kunci luas + Maksimalkan klik
7. [G06] Kampanye dipisah per tujuan dan produk - Google Ads; tinggi, sedang; prioritas 6; skor platform naik +2,0 bila beres (status: sebagian)
   Perbaikan: Pisahkan kampanye merek vs umum; satu grup iklan untuk satu tema kata kunci
   Catatan audit: Merek & umum tercampur di satu kampanye
8. [G14] Halaman tujuan relevan dan cepat - Google Ads; tinggi, sulit; prioritas 3; skor platform naik +5,0 bila beres (status: sebagian)
   Perbaikan: Buat halaman khusus per produk/kelas; kompres gambar; taruh tombol WA di atas
   Catatan audit: Tombol WA ada tapi halaman lambat di HP
9. [G16] Daftar negatif bersama - Google Ads; sedang, mudah; prioritas 3; skor platform naik +3,8 bila beres
   Perbaikan: Buat satu daftar negatif umum dan terapkan ke semua kampanye Penelusuran & Performance Max, atau pakai kata kunci negatif tingkat akun
10. [G13] Aset tambahan terpasang - Google Ads; sedang, mudah; prioritas 3; skor platform naik +2,5 bila beres
   Perbaikan: Tambahkan sitelink (Jadwal, Harga, Testimoni, Kontak) dan callout (Sertifikat, Cicilan, dll.)
   Catatan audit: Belum ada sitelink

RENCANA 7 HARI (maks. kira-kira 1-2 jam kerja per hari)
Hari 1 (Senin, 28 Sep 2026):
  - PERBAIKI [G02] Hanya aksi bernilai yang jadi konversi utama - Ubah aksi yang tidak bernilai menjadi Sekunder
  - PERBAIKI [G15] Istilah penelusuran dicek dan kata kunci negatif dipasang - Tambahkan istilah yang tidak relevan sebagai kata kunci negatif di kampanye Penelusuran dan di Performance Max (berlaku untuk inventaris Penelusuran & Shopping)
  - PERBAIKI [G03] Cara hitung konversi benar - Ubah pengaturan Hitungan pada aksi konversi
Hari 2 (Selasa, 29 Sep 2026):
  - PERBAIKI [G07] Kampanye Penelusuran tidak ikut Jaringan Display - Hapus centang Jaringan Display di kampanye Penelusuran
  - PERBAIKI [G12] Iklan responsif kuat - Isi 10-15 judul & 4 deskripsi: kata kunci, harga/jadwal, keunggulan, ajakan
Hari 3 (Rabu, 30 Sep 2026):
  - PERBAIKI [G09] Jenis pencocokan sesuai kesiapan data - Ubah kata kunci luas menjadi frasa/tepat sampai konversi tercatat stabil
Hari 4 (Kamis, 1 Okt 2026):
  - PERBAIKI [G06] Kampanye dipisah per tujuan dan produk - Pisahkan kampanye merek vs umum; satu grup iklan untuk satu tema kata kunci
Hari 5 (Jumat, 2 Okt 2026):
  - PERBAIKI [G14] Halaman tujuan relevan dan cepat - Buat halaman khusus per produk/kelas; kompres gambar; taruh tombol WA di atas
Hari 6 (Sabtu, 3 Okt 2026):
  - Jangan ubah pengaturan besar; biarkan iklan belajar setelah perbaikan. Catat biaya & hasil harian.
Hari 7 (Minggu, 4 Okt 2026):
  - Ekspor data iklan 7 hari lalu buat laporan dengan skill laporan-iklan-mingguan; audit ulang cek yang sudah diperbaiki dan bandingkan skornya.
Antrean minggu berikutnya: [G16] Daftar negatif bersama; [G13] Aset tambahan terpasang

Aturan aman: ubah anggaran paling banyak 20% per 2-3 hari dan jangan ubah banyak hal sekaligus di satu kampanye. Skor ini alat bantu prioritas, bukan jaminan hasil iklan.
```

## Penjelasan bahasa awam yang ditambahkan agent (3 masalah terbesar)
1. **"Kunjungan halaman" dihitung sebagai konversi utama.** Google mengira setiap pengunjung
   adalah "hasil", jadi iklan dioptimalkan untuk pengunjung, bukan pendaftar. Benahi (±10 menit):
   Tujuan → Konversi → aksi "Kunjungan halaman" → jadikan Sekunder.
2. **22% biaya habis untuk pencarian seperti "kursus excel gratis pdf".** Orang yang mencari
   "gratis/pdf" hampir tidak pernah membeli kursus. Tambahkan kata kunci negatif: gratis, pdf,
   download, lowongan.
3. **Pendaftaran dihitung "Setiap".** Satu orang yang mengisi formulir dua kali tercatat 2 pendaftar,
   angka jadi terlihat lebih bagus dari kenyataan. Ubah menjadi "Satu".

## Catatan pemeriksaan pembuat
- G11 `tidak_tahu` (keparahan tinggi, bukan kritis) sehingga tidak masuk CEK DULU. Cakupan: berlaku 45 (G08 tidak berlaku), diketahui 42 → 93,3%.
- G09 berstatus gagal dengan kemudahan sedang → prioritas 3×2 = 6; urutan sesuai rumus.
