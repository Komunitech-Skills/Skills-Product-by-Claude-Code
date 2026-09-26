# Contoh 2 - Klinik kecantikan, Meta Ads klik-ke-WhatsApp

> Contoh uji pembuat (simulasi agent, 2026-09-26). Data fiktif yang meniru kasus UMKM nyata;
> bukan hasil uji independen (itu dilakukan penguji terpisah sesuai CLAUDE.md Tahap 6).

## Permintaan pengguna
"Klinik saya pasang iklan IG/FB ke WhatsApp, chat banyak tapi yang booking sedikit. Bisa diaudit? Ini screenshot Ads Manager-nya."

## Bukti yang diberikan (diringkas agent ke file jawaban)
Screenshot Ads Manager (tujuan, pengiriman, hasil, frekuensi), Pengaturan Bisnis > Orang, Kualitas
Akun, dan jawaban admin. Iklan hanya ke WhatsApp (tanpa website) sehingga M01 dan M17
`tidak_berlaku`. Ringkasan: [`02-jawaban-klinik-kecantikan-meta.csv`](02-jawaban-klinik-kecantikan-meta.csv).
Tidak ada data pasien yang diminta atau disimpan.

## Perintah yang dijalankan
```bash
python3 scripts/skor_audit.py hitung examples/02-jawaban-klinik-kecantikan-meta.csv --usaha "Klinik kecantikan (Bandung)" --mulai 2026-09-28
```

## Output script (disalin apa adanya)
```
AUDIT KESEHATAN AKUN IKLAN - Klinik kecantikan (Bandung)
========================================================
Skor gabungan: 33,5 / 100 (Kritis) - FINAL; bobot: satu platform

PER PLATFORM
- Meta Ads (Facebook/Instagram): 33,5/100 (Kritis); bukti 96,2% (final)
    Pelacakan & konversi: 0,0 (bobot 20)
    Struktur & akses akun: 27,3 (bobot 15)
    Target & audiens: 50,0 (bobot 10)
    Anggaran & bidding: 80,0 (bobot 15)
    Materi iklan: 40,9 (bobot 15)
    Halaman tujuan / etalase: 50,0 (bobot 10)
    Frekuensi & kelelahan materi: 0,0 (bobot 10)
    Pengecualian: 25,0 (bobot 5)

PRIORITAS PERBAIKAN (dampak x kemudahan; skor tertinggi dikerjakan dulu)
1. [M04] Akses akun iklan aman - Meta Ads; kritis, mudah; prioritas 15; skor platform naik +6,8 bila beres
   Perbaikan: Nyalakan verifikasi 2 langkah untuk semua admin; hapus akses orang/agensi yang sudah tidak bekerja sama
   Catatan audit: Mantan freelancer masih admin; 2FA belum aktif
2. [M15] Tidak ada iklan ditolak / akun dibatasi - Meta Ads; kritis, mudah; prioritas 15; skor platform naik +6,8 bila beres
   Perbaikan: Hapus klaim berlebihan dan foto sebelum-sesudah; ajukan peninjauan ulang hanya bila yakin iklan sudah sesuai kebijakan
   Catatan audit: 1 iklan ditolak: foto sebelum-sesudah jerawat
3. [M02] Hasil utama yang dioptimalkan benar-benar tercatat - Meta Ads; kritis, sedang; prioritas 10; skor platform naik +12,5 bila beres
   Perbaikan: Samakan event dengan tujuan; perbaiki event yang dobel/tidak terkirim; untuk iklan WA pakai hasil Percakapan dimulai
   Catatan audit: Percakapan dimulai 180 vs chat nyata masuk 131 (selisih 37% > 30%)
4. [M18] Frekuensi tidak berlebihan - Meta Ads; tinggi, mudah; prioritas 9; skor platform naik +10,0 bila beres
   Perbaikan: Perluas audiens atau tambah materi baru; turunkan anggaran bila audiens kecil
   Catatan audit: Frekuensi 7 hari 4.6 di audiens baru
5. [M03] Chat WA dari iklan dicatat sampai jadi order - Meta Ads; tinggi, mudah; prioritas 9; skor platform naik +7,5 bila beres
   Perbaikan: Beri label 'Iklan' di WhatsApp Business untuk chat dari iklan; tiap Sabtu hitung berapa yang jadi order
   Catatan audit: Tidak ada catatan chat yang jadi booking
6. [M05] Tujuan kampanye sesuai hasil yang dicari - Meta Ads; tinggi, mudah; prioritas 9; skor platform naik +4,1 bila beres
   Perbaikan: Buat kampanye baru dengan tujuan yang benar (tujuan tidak bisa diganti di kampanye lama); matikan yang lama setelah yang baru berjalan 3-5 hari
   Catatan audit: 2 dari 3 kampanye pakai Tingkatkan Postingan
7. [M20] Pelanggan lama dikecualikan dari iklan pelanggan baru - Meta Ads; tinggi, mudah; prioritas 9; skor platform naik +3,8 bila beres
   Perbaikan: Tambahkan audiens khusus pembeli/pengirim pesan 180 hari ke kolom Kecualikan
8. [M09] Ada audiens khusus untuk retargeting - Meta Ads; tinggi, sedang; prioritas 6; skor platform naik +5,0 bila beres
   Perbaikan: Buat audiens khusus 'Orang yang berinteraksi dengan akun Instagram 60 hari' dan 'Pengirim pesan 90 hari'; buat kampanye retargeting kecil
9. [M16] Tujuan klik cocok dan siap melayani - Meta Ads; tinggi, sedang; prioritas 6; skor platform naik +5,0 bila beres (status: sebagian)
   Perbaikan: Samakan promo di iklan & halaman; siapkan balasan cepat WA Business; jadwalkan admin jaga di jam iklan paling ramai
   Catatan audit: Balasan WA rata-rata 25 menit
10. [M13] Minimal 3 variasi materi per ad set - Meta Ads; tinggi, sedang; prioritas 6; skor platform naik +2,0 bila beres (status: sebagian)
   Perbaikan: Tambah variasi: 1 foto produk, 1 video testimoni/UGC, 1 carousel/promo; jangan cuma ganti warna
   Catatan audit: Ad set utama hanya 2 iklan
   ...dan 1 perbaikan lain (lihat --json atau antrean).

RENCANA 7 HARI (maks. kira-kira 1-2 jam kerja per hari)
Hari 1 (Senin, 28 Sep 2026):
  - PERBAIKI [M04] Akses akun iklan aman - Nyalakan verifikasi 2 langkah untuk semua admin; hapus akses orang/agensi yang sudah tidak bekerja sama
  - PERBAIKI [M15] Tidak ada iklan ditolak / akun dibatasi - Hapus klaim berlebihan dan foto sebelum-sesudah; ajukan peninjauan ulang hanya bila yakin iklan sudah sesuai kebijakan
Hari 2 (Selasa, 29 Sep 2026):
  - PERBAIKI [M02] Hasil utama yang dioptimalkan benar-benar tercatat - Samakan event dengan tujuan; perbaiki event yang dobel/tidak terkirim; untuk iklan WA pakai hasil Percakapan dimulai
  - PERBAIKI [M18] Frekuensi tidak berlebihan - Perluas audiens atau tambah materi baru; turunkan anggaran bila audiens kecil
Hari 3 (Rabu, 30 Sep 2026):
  - PERBAIKI [M03] Chat WA dari iklan dicatat sampai jadi order - Beri label 'Iklan' di WhatsApp Business untuk chat dari iklan; tiap Sabtu hitung berapa yang jadi order
  - PERBAIKI [M05] Tujuan kampanye sesuai hasil yang dicari - Buat kampanye baru dengan tujuan yang benar (tujuan tidak bisa diganti di kampanye lama); matikan yang lama setelah yang baru berjalan 3-5 hari
  - PERBAIKI [M20] Pelanggan lama dikecualikan dari iklan pelanggan baru - Tambahkan audiens khusus pembeli/pengirim pesan 180 hari ke kolom Kecualikan
Hari 4 (Kamis, 1 Okt 2026):
  - PERBAIKI [M09] Ada audiens khusus untuk retargeting - Buat audiens khusus 'Orang yang berinteraksi dengan akun Instagram 60 hari' dan 'Pengirim pesan 90 hari'; buat kampanye retargeting kecil
Hari 5 (Jumat, 2 Okt 2026):
  - PERBAIKI [M16] Tujuan klik cocok dan siap melayani - Samakan promo di iklan & halaman; siapkan balasan cepat WA Business; jadwalkan admin jaga di jam iklan paling ramai
Hari 6 (Sabtu, 3 Okt 2026):
  - Jangan ubah pengaturan besar; biarkan iklan belajar setelah perbaikan. Catat biaya & hasil harian.
Hari 7 (Minggu, 4 Okt 2026):
  - Ekspor data iklan 7 hari lalu buat laporan dengan skill laporan-iklan-mingguan; audit ulang cek yang sudah diperbaiki dan bandingkan skornya.
Antrean minggu berikutnya: [M13] Minimal 3 variasi materi per ad set; [M11] Batas belanja akun dipasang

Aturan aman: ubah anggaran paling banyak 20% per 2-3 hari dan jangan ubah banyak hal sekaligus di satu kampanye. Skor ini alat bantu prioritas, bukan jaminan hasil iklan.
```

## Penjelasan bahasa awam yang ditambahkan agent (3 masalah terbesar)
1. **Mantan freelancer masih admin dan verifikasi 2 langkah belum aktif.** Kalau akunnya dibajak,
   iklan bisa dipakai orang lain dan kartu Anda yang ditagih. Benahi hari ini (±15 menit):
   Pengaturan Bisnis → Orang → hapus akses → aktifkan verifikasi 2 langkah semua admin.
2. **Iklan foto sebelum-sesudah jerawat ditolak.** Iklan kecantikan dengan foto sebelum-sesudah
   melanggar kebijakan Meta dan penolakan berulang bisa membatasi akun. Ganti dengan video dokter/
   terapis menjelaskan perawatan, tanpa janji hasil.
3. **Tidak ada catatan chat yang jadi booking.** Meta mencatat 180 "percakapan", tapi hanya 131
   chat masuk dan tidak diketahui berapa yang booking — jadi belum tahu iklan mana yang benar-benar
   menghasilkan pasien. Beri label "Iklan" di WhatsApp Business dan hitung tiap Sabtu.

## Catatan pemeriksaan pembuat
- Cakupan: berlaku 52 (M01 & M17 tidak berlaku), diketahui 50 (M07 & M19 tidak_tahu, masing-masing
  bobot 1) → 96,2%. Skor 33,5 cocok dengan hitung ulang independen di tests/uji_skor_audit.py (test_06).
- Skill tidak menilai klaim medis; hanya menandai risiko kebijakan iklan (sesuai keputusan pemilik
  untuk domain kesehatan).
