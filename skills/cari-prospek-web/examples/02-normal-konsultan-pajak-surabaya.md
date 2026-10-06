# Skenario 2: konsultan pajak mencari klinik swasta & apotek di Surabaya

- Tanggal uji: 2026-10-06 · penguji independen · OpenClaw lokal, model claude-sonnet-5
- Perbandingan lengkap SEBELUM/SESUDAH: `00-openclaw-sebelum-sesudah.md`; verifikasi sumber: `data/verifikasi-sumber.md`

## Input
> Saya konsultan pajak di Surabaya, mau tawarkan jasa pembukuan dan lapor pajak bulanan ke klinik swasta dan apotek di Surabaya. Tolong carikan calon klien yang cocok beserta kontak bisnisnya.

## Output SESUDAH (dengan skill)

Sudah saya susun daftarnya dari sumber publik (direktori faskes BPJS, direktori bisnis lokal, dan situs resmi klinik). Berikut hasilnya:

## Profil ideal & asumsi
- **Jasa ditawarkan:** pembukuan + lapor pajak bulanan (PPh/PPN).
- **Target:** klinik swasta & apotek mandiri di Surabaya — bukan rumah sakit besar atau jaringan nasional (Siloam, Natasha, ZAP, Miracle) karena biasanya sudah punya tim finance/pajak internal.
- **Ciri cocok:** lokasi tunggal atau cabang kecil, badan usaha formal, transaksi harian rutin (klinik/apotek), kemungkinan belum ada staf akuntansi/pajak khusus.

## Tabel prospek (18 baris)

| No | Nama usaha | Kota | Jenis | Alasan cocok | Skor | Kontak bisnis publik | Sumber (URL) | Dicek |
|---|---|---|---|---|---|---|---|---|
| 1 | Klinik Mitra Sehat | Surabaya | Klinik pratama (faskes BPJS) | Klinik mandiri lokasi tunggal, kemungkinan belum ada tim akunting sendiri | Tinggi | (031) 7524408 / 70759770 | lokanesia.com/klinik-pratama-di-surabaya | 6 Okt 2026 |
| 2 | Klinik Medico Sier | Surabaya | Klinik pratama, buka 24 jam | Operasi 24 jam = volume transaksi tinggi, butuh laporan pajak rutin | Tinggi | (031) 8434056 | lokanesia.com/klinik-pratama-di-surabaya | 6 Okt 2026 |
| 3 | Klinik Optima | Surabaya | Klinik pratama | Klinik mandiri skala kecil-menengah | Sedang | (031) 8720733 | lokanesia.com/klinik-pratama-di-surabaya | 6 Okt 2026 |
| 4 | Klinik Jemursari Empat | Surabaya | Klinik pratama | Klinik kecil, cocok jasa pembukuan sederhana | Sedang | (031) 8418414 | lokanesia.com/klinik-pratama-di-surabaya | 6 Okt 2026 |
| 5 | Klinik Prameswari | Surabaya | Klinik pratama | Klinik mandiri lokasi tunggal (Gubeng) | Sedang | (031) 5029118 | lokanesia.com/klinik-pratama-di-surabaya | 6 Okt 2026 |
| 6 | Klinik Kebangkitan | Surabaya | Klinik pratama | Klinik mandiri, berpotensi belum ada staf pajak tetap | Sedang | (031) 71258886 | lokanesia.com/klinik-pratama-di-surabaya | 6 Okt 2026 |
| 7 | Klinik Anugerah Karya Medika 102 | Surabaya | Klinik pratama | Klinik mandiri lokasi tunggal | Sedang | (031) 78071401 | lokanesia.com/klinik-pratama-di-surabaya | 6 Okt 2026 |
| 8 | Klinik Nayaka Husada 03 | Surabaya | Klinik pratama | Klinik mandiri lokasi tunggal (Asemrowo) | Sedang | (031) 5343154 | lokanesia.com/klinik-pratama-di-surabaya | 6 Okt 2026 |
| 9 | BRI Medika Surabaya | Surabaya | Klinik umum | Nama korporat, menandakan ada badan usaha formal | Tinggi | (031) 8472120 | alamatsehat.com/klinik-24-jam-di-surabaya | 6 Okt 2026 |
| 10 | Klinik Utama Pusura Sungkono | Surabaya | Klinik utama | Status "Utama" = skala lebih besar, laporan pajak bulanan rutin relevan | Tinggi | (031) 5612120 | alamatsehat.com/klinik-24-jam-di-surabaya | 6 Okt 2026 |
| 11 | Klinik Utama Rawat Inap Kartika | Surabaya | Klinik utama + rawat inap | Ada rawat inap = skala operasi & kompleksitas pajak lebih besar | Tinggi | (031) 5042395 | alamatsehat.com/klinik-24-jam-di-surabaya | 6 Okt 2026 |
| 12 | Klinik Medis Pusura | Surabaya | Klinik umum | Klinik mandiri di pusat kota (Genteng) | Sedang | (031) 5317334 | alamatsehat.com/klinik-24-jam-di-surabaya | 6 Okt 2026 |
| 13 | Klinik Waluyo Jati | Surabaya | Klinik utama (umum, gigi, spesialis saraf) | Multi-layanan = kompleksitas pembukuan lebih tinggi, klien ideal jasa pajak bulanan | Tinggi | (031) 5026014 | semuabis.com/klinik-waluyo-jati-surabaya; alamat dikonfirmasi di klinikwaluyojati.com | 6 Okt 2026 |
| 14 | QDerma Clinic | Surabaya | Klinik estetik/kecantikan | Klinik kecantikan independen, biasanya belum punya tim finance internal | Tinggi | 0812 9548 5757 (Telepon/WA, halaman Contact resmi) | qdermaclinicsby.com/contact | 6 Okt 2026 |
| 15 | Apotek & Lab Klinik 2 Oscar | Surabaya | Apotek + lab klinik | Kombinasi apotek & lab klinik, transaksi harian tinggi | Tinggi | (031) 5033067 | surabaya.lokanesia.com/daftar-lengkap-alamat-apotek-di-surabaya | 6 Okt 2026 |
| 16 | Apotek AHA Medica | Surabaya | Apotek mandiri | Apotek independen, lokasi komersial Dharmawangsa | Sedang | (031) 5032819 | surabaya.lokanesia.com/daftar-lengkap-alamat-apotek-di-surabaya | 6 Okt 2026 |
| 17 | Apotek Adam Farma | Surabaya | Apotek mandiri | Apotek independen lokasi tunggal (Tenggilis Mejoyo) | Sedang | (031) 8439919 | surabaya.lokanesia.com/daftar-lengkap-alamat-apotek-di-surabaya | 6 Okt 2026 |
| 18 | Apotek Asri Farma | Surabaya | Apotek mandiri | Apotek independen di kawasan Gubeng, lalu lintas tinggi (dekat kampus/RS) | Sedang | (031) 5923908 | surabaya.lokanesia.com/daftar-lengkap-alamat-apotek-di-surabaya | 6 Okt 2026 |

## 3 prospek prioritas

1. **Klinik Utama Rawat Inap Kartika** (Jl. Ngagel Jaya Utara No.28A) — status "Utama + Rawat Inap" berarti transaksi dan kewajiban pajaknya lebih kompleks dari klinik pratama biasa.
   *Pembuka:* "Selamat siang, saya konsultan pajak di Surabaya — melihat Klinik Kartika melayani rawat inap, biasanya pembukuan dan lapor pajak bulanannya cukup menyita waktu tim. Boleh saya kirim info singkat jasa kami?"

2. **Klinik Waluyo Jati** (Jl. Ambengan No.68) — punya 3 layanan (umum, gigi, spesialis saraf) dalam satu klinik, artinya pencatatan pendapatan per layanan lebih rumit dan cocok dibantu jasa pembukuan.
   *Pembuka:* "Selamat siang, saya lihat Klinik Waluyo Jati punya layanan umum, gigi, dan spesialis saraf — pasti pencatatan transaksinya cukup banyak. Kami bantu pembukuan & lapor pajak bulanan supaya Bapak/Ibu fokus ke pelayanan pasien saja."

3. **QDerma Clinic** (Ruko Bukit Darmo Golf R No.9) — klinik kecantikan independen dengan kontak WA bisnis jelas di situs resminya, kemungkinan belum punya staf pajak khusus.
   *Pembuka:* "Selamat siang, saya konsultan pajak di Surabaya, lihat QDerma Clinic di Bukit Darmo — kami biasa bantu klinik kecantikan independen urus pembukuan dan lapor pajak bulanan supaya lebih praktis. Boleh kenalan dulu?"

Pesan lengkap satu-satu sebaiknya pakai skill `pesan-prospek-wa` saat mau kirim beneran.

## CSV siap tempel
```
nama,kota,jenis,alasan,skor,kontak,website,sumber,tanggal_cek
"Klinik Mitra Sehat",Surabaya,"Klinik pratama","Klinik mandiri lokasi tunggal",Tinggi,"(031) 7524408 / 70759770","","https://lokanesia.com/klinik-pratama-di-surabaya/","6 Okt 2026"
"Klinik Medico Sier",Surabaya,"Klinik pratama 24 jam","Operasi 24 jam, volume transaksi tinggi",Tinggi,"(031) 8434056","","https://lokanesia.com/klinik-pratama-di-surabaya/","6 Okt 2026"
"Klinik Optima",Surabaya,"Klinik pratama","Klinik mandiri skala kecil-menengah",Sedang,"(031) 8720733","","https://lokanesia.com/klinik-pratama-di-surabaya/","6 Okt 2026"
"Klinik Jemursari Empat",Surabaya,"Klinik pratama","Klinik kecil",Sedang,"(031) 8418414","","https://lokanesia.com/klinik-pratama-di-surabaya/","6 Okt 2026"
"Klinik Prameswari",Surabaya,"Klinik pratama","Klinik mandiri lokasi tunggal",Sedang,"(031) 5029118","","https://lokanesia.com/klinik-pratama-di-surabaya/","6 Okt 2026"
"Klinik Kebangkitan",Surabaya,"Klinik pratama","Klinik mandiri",Sedang,"(031) 71258886","","https://lokanesia.com/klinik-pratama-di-surabaya/","6 Okt 2026"
"Klinik Anugerah Karya Medika 102",Surabaya,"Klinik pratama","Klinik mandiri lokasi tunggal",Sedang,"(031) 78071401","","https://lokanesia.com/klinik-pratama-di-surabaya/","6 Okt 2026"
"Klinik Nayaka Husada 03",Surabaya,"Klinik pratama","Klinik mandiri lokasi tunggal",Sedang,"(031) 5343154","","https://lokanesia.com/klinik-pratama-di-surabaya/","6 Okt 2026"
"BRI Medika Surabaya",Surabaya,"Klinik umum","Nama korporat, badan usaha formal",Tinggi,"(031) 8472120","","https://alamatsehat.com/klinik-24-jam-di-surabaya/","6 Okt 2026"
"Klinik Utama Pusura Sungkono",Surabaya,"Klinik utama","Skala lebih besar",Tinggi,"(031) 5612120","","https://alamatsehat.com/klinik-24-jam-di-surabaya/","6 Okt 2026"
"Klinik Utama Rawat Inap Kartika",Surabaya,"Klinik utama + rawat inap","Rawat inap, skala & kompleksitas pajak besar",Tinggi,"(031) 5042395","","https://alamatsehat.com/klinik-24-jam-di-surabaya/","6 Okt 2026"
"Klinik Medis Pusura",Surabaya,"Klinik umum","Klinik mandiri pusat kota",Sedang,"(031) 5317334","","https://alamatsehat.com/klinik-24-jam-di-surabaya/","6 Okt 2026"
"Klinik Waluyo Jati",Surabaya,"Klinik utama multi-layanan","Multi-layanan, kompleksitas pembukuan tinggi",Tinggi,"(031) 5026014","https://www.klinikwaluyojati.com/","https://www.semuabis.com/klinik-waluyo-jati-surabaya-031-5026014","6 Okt 2026"
"QDerma Clinic",Surabaya,"Klinik estetik/kecantikan","Klinik independen, belum ada tim finance internal",Tinggi,"0812 9548 5757","https://www.qdermaclinicsby.com","https://www.qdermaclinicsby.com/contact","6 Okt 2026"
"Apotek & Lab Klinik 2 Oscar",Surabaya,"Apotek + lab klinik","Transaksi harian tinggi",Tinggi,"(031) 5033067","","https://surabaya.lokanesia.com/daftar-lengkap-alamat-apotek-di-surabaya/","6 Okt 2026"
"Apotek AHA Medica",Surabaya,"Apotek mandiri","Lokasi komersial Dharmawangsa",Sedang,"(031) 5032819","","https://surabaya.lokanesia.com/daftar-lengkap-alamat-apotek-di-surabaya/","6 Okt 2026"
"Apotek Adam Farma",Surabaya,"Apotek mandiri","Apotek independen lokasi tunggal",Sedang,"(031) 8439919","","https://surabaya.lokanesia.com/daftar-lengkap-alamat-apotek-di-surabaya/","6 Okt 2026"
"Apotek Asri Farma",Surabaya,"Apotek mandiri","Kawasan Gubeng, lalu lintas tinggi",Sedang,"(031) 5923908","","https://surabaya.lokanesia.com/daftar-lengkap-alamat-apotek-di-surabaya/","6 Okt 2026"
```

## Catatan kejujuran
- **18 baris** semua punya alamat + telepon + sumber. Sebagian besar nomor (klinik pratama) berasal dari direktori faskes BPJS dan direktori lokal (lokanesia.com, alamatsehat.com, semuabis.com), bukan situs resmi klinik itu sendiri — karena mayoritas klinik kecil/apotek mandiri tidak punya situs resmi.
- **QDerma Clinic** terverifikasi langsung dari halaman Contact situs resminya — paling solid.
- **Klinik Waluyo Jati**: nomor dari direktori bisnis, alamat dikonfirmasi silang dengan situs resminya sendiri.
- Nomor di direktori faskes BPJS (lokanesia.com) tercantum sebagai kontak resmi faskes, tapi sebaiknya dikonfirmasi ulang lewat telepon/WA sebelum kunjungan pertama, karena data bisa berubah.
- Saya **tidak memasukkan** rumah sakit besar/jaringan nasional (RS PHC, Siloam, RKZ, Natasha, ZAP, Miracle) karena biasanya sudah punya tim finance internal — kurang cocok sebagai target jasa pembukuan independen.

## Langkah lanjut
Hubungi satu-satu lewat telepon/WA bisnis di atas, sebutkan sumber kontaknya (mis. "nomor ini kami lihat di direktori faskes"), jangan kirim massal. Kalau mau, saya bisa bantu susun draf pesan pembuka WA lengkap pakai skill `pesan-prospek-wa`.

Tiga hal untuk dikonfirmasi dari Anda:
1. Mau saya perluas juga ke apotek jaringan kecil (bukan apotek K-24/Kimia Farma) atau tetap fokus independen seperti ini?
2. Perlu saya tambahkan klinik gigi/klinik hewan sebagai kategori tambahan, atau tetap klinik umum + apotek saja?
3. Mau saya lanjut buat draf pesan WA pembuka untuk 3 prospek prioritas sekarang?

## Catatan penguji
Skor 8,5 (SEBELUM 6). Verifikasi penguji: 17 dari 18 baris cocok persis dengan URL sumber, 1 tidak bisa dibuka (403), 0 karangan. SEBELUM tidak memberi URL per baris; penguji hanya bisa membuktikan 1 dari 14. Kekurangan: dua kali menyebut "skill `pesan-prospek-wa`" ke pengguna (kata proses).
