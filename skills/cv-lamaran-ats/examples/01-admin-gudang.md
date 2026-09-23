# Skenario 1 — Normal: Admin Gudang

## Input pengguna
```
Tolong sesuaikan CV saya dengan lowongan ini:

Lowongan: Staff Admin Gudang
PT Sumber Makmur Logistik - Bekasi

Kualifikasi:
- Pendidikan minimal SMA/SMK sederajat
- Pengalaman minimal 1 tahun sebagai admin gudang atau staff logistik
- Menguasai Microsoft Excel (VLOOKUP, Pivot Table)
- Memahami sistem stok/inventory dan kartu stok
- Teliti, disiplin, dan mampu bekerja di bawah tekanan
- Terbiasa menggunakan aplikasi WMS (Warehouse Management System) menjadi nilai plus
- Mampu mengoperasikan mesin scan barcode

Tanggung jawab:
- Mencatat keluar masuk barang di gudang
- Melakukan stock opname berkala
- Membuat laporan inventory mingguan
- Berkoordinasi dengan tim purchasing dan pengiriman
- Menjaga kerapian dan keamanan gudang

Data saya: Siti Rahma, Bekasi, HP 0812-0000-1111, email siti.rahma@email.com.
Pengalaman: Admin Gudang di CV Berkah Jaya 2022-2024, catat keluar masuk barang pakai
Excel dan kartu stok manual, bikin laporan stok bulanan, bantu stock opname tiap
akhir bulan. Pendidikan: SMK Akuntansi, SMK Negeri 3 Bekasi, lulus 2020.
```

## Output

```
## Skor Kecocokan Kata Kunci
(dihitung dengan scripts/skor_kecocokan.py dari draf CV di bawah vs teks lowongan)
48% kata kunci lowongan ditemukan di draf CV (12/25)

Kata kunci yang sudah ada: gudang, admin, staff, stok, barang, bekasi, disiplin, excel,
kartu, keluar, laporan, masuk

Kata kunci yang belum terlihat (cek relevansi, jangan dikarang): inventory, logistik,
aplikasi, barcode, berkoordinasi, keamanan, kerapian, management (dari "WMS")
Catatan: beberapa kata di daftar mentah script (mis. "mampu", "bawah", "bekerja",
"berkala", "makmur") bukan kata kunci relevan (kata umum/bagian nama perusahaan) —
diabaikan saat menyusun CV.

Saya cek dulu ke Ibu Siti: apakah pernah pakai aplikasi WMS (Warehouse Management
System) atau alat scan barcode di CV Berkah Jaya? Kalau belum pernah, saya tidak akan
menuliskannya — biar CV tetap jujur, saya hanya akan menonjolkan pengalaman stock
opname dan pencatatan stok yang memang sudah dimiliki.

(Asumsi karena tidak dijawab: belum pernah pakai WMS/barcode scanner — kata itu
sengaja TIDAK dimasukkan ke CV.)

## CV Versi ATS (Bahasa Indonesia)
Siti Rahma
Bekasi · 0812-0000-1111 · siti.rahma@email.com

RINGKASAN PROFIL
Admin Gudang dengan 2 tahun pengalaman mencatat keluar-masuk barang, mengelola kartu
stok, dan melakukan stock opname bulanan. Teliti dan terbiasa bekerja dengan target
laporan inventory yang akurat.

PENGALAMAN KERJA
Admin Gudang — CV Berkah Jaya (2022–2024)
- Mencatat keluar masuk barang menggunakan Microsoft Excel dan kartu stok manual
- Menyusun laporan stok bulanan untuk atasan sebagai bahan evaluasi inventory
- Membantu pelaksanaan stock opname setiap akhir bulan untuk memastikan kesesuaian
  data fisik dan catatan

PENDIDIKAN
SMK, Akuntansi — SMK Negeri 3 Bekasi (2020)

KEAHLIAN
Microsoft Excel, pencatatan stok/kartu stok, stock opname, ketelitian, disiplin

## Surat Lamaran (Formal)
Bekasi, [tanggal]

Kepada Yth.
HRD PT Sumber Makmur Logistik
di Bekasi

Dengan hormat,

Saya Siti Rahma, bermaksud melamar posisi Staff Admin Gudang di PT Sumber Makmur
Logistik. Selama 2 tahun bekerja sebagai Admin Gudang di CV Berkah Jaya, saya
terbiasa mencatat keluar-masuk barang, mengelola kartu stok, dan melakukan stock
opname bulanan menggunakan Microsoft Excel — sejalan dengan kebutuhan posisi ini.

Bersama surat ini saya lampirkan CV sebagai bahan pertimbangan. Saya terbuka untuk
dihubungi guna wawancara lebih lanjut.

Hormat saya,
Siti Rahma

## Email Singkat
Subjek: Lamaran Posisi Staff Admin Gudang – Siti Rahma

Selamat siang,

Saya Siti Rahma, ingin melamar posisi Staff Admin Gudang di PT Sumber Makmur
Logistik. Saya memiliki pengalaman 2 tahun sebagai Admin Gudang, terbiasa mencatat
stok dan membuat laporan inventory dengan Excel. CV terlampir untuk pertimbangan
Bapak/Ibu. Terima kasih.

Hormat saya,
Siti Rahma
0812-0000-1111

## Checklist Sebelum Kirim
- [x] Tidak ada pengalaman/gelar/sertifikat yang dikarang — WMS/barcode scanner
      sengaja tidak ditambahkan karena belum dikonfirmasi dimiliki
- [x] CV versi ATS: satu kolom, tanpa tabel/foto/grafik skill
- [x] Tidak ada NIK/agama/status pernikahan
- [ ] Nama file disarankan: `CV - Siti Rahma - Staff Admin Gudang.pdf`
- [ ] Simpan sebagai PDF sebelum dikirim
- [ ] Cek typo & konsistensi tanggal sebelum kirim
- [x] Skor kecocokan kata kunci sudah dijalankan dan disampaikan
- [x] Disclaimer: skor kata kunci adalah proksi sederhana, bukan jaminan lolos ATS/rekruter

## Asumsi
- Bahasa keluaran: Indonesia (mengikuti bahasa lowongan)
- Belum pernah menggunakan aplikasi WMS/barcode scanner → tidak dicantumkan di CV
- Surat lamaran & email singkat disertakan (default karena tidak diminta sebaliknya)
```

## Catatan penguji
- Skor 48% (12/25) cocok persis dengan hasil script `skor_kecocokan.py` dan dengan
  perhitungan ulang independen (lihat `HASIL-UJI.md`).
- **Cacat sedang ditemukan saat menjalankan langkah 3–4 SKILL.md**: daftar "kata kunci
  hilang" mentah dari script berisi kata yang bukan keyword sesungguhnya —
  "mampu", "bawah", "bekerja", "berkala", "makmur" (bagian nama perusahaan
  "Sumber Makmur"). SKILL.md tidak secara eksplisit menyuruh agent menyaring kata
  non-relevan ini sebelum ditampilkan ke pengguna; saya (penguji, berperan sebagai
  agent) menyaringnya secara manual berdasarkan penilaian sendiri sebelum
  menuliskan ke output "Kata kunci yang belum terlihat" versi ringkas, tapi
  seorang agent lain yang kurang hati-hati bisa saja menyalin daftar mentah
  apa adanya dan menyuruh pengguna menambahkan kata "mampu"/"bawah" ke CV —
  ini akan terlihat aneh dan tidak profesional. Root cause: stopword list script
  belum memasukkan kata umum seperti "mampu", "bawah", "bekerja", "berkala",
  dan tidak ada penyaringan nama perusahaan.
- Alur "cek dulu ke pengguna apakah punya pengalaman X" (WMS/barcode) berjalan
  sesuai langkah 4 SKILL.md — tidak mengarang.
