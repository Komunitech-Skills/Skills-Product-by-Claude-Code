# Hasil uji: rencana-restok-barang

- **Tanggal:** 2026-10-14
- **Penguji:** agent penguji independen Komunitech (bukan pembuat; hanya membaca folder skill)
- **Versi diuji:** 1.0.0
- **Platform:** openclaw (uji otomatis agent), OpenClaw 2026.10.2 lokal, model router Komunitech claude-sonnet-5; skenario normal utama juga di konteks kanal Telegram (tanpa mengirim), kedua sisi
- **Rincian:** `00-openclaw-sebelum-sesudah.md` (jawaban utuh kedua sisi), `00-banding-pesaing.md`, `01`–`05`, data di `data/`

## Skor kualitas: 8/10

| Skenario | Tanpa skill | Dengan skill |
|---|---|---|
| 1. Normal utama, lokal: toko bayi online, CSV 90 hari (777 baris, tanggal campur), stok 12 barang, 2 pemasok (satu kelipatan dus 12) | 7 | 8,5 |
| 1. Normal utama, konteks Telegram | 6 | 8,5 |
| 2. Warung sembako, total mingguan 8 minggu ditempel, stok 2 barang belum diketahui | 6,5 | 7,5 |
| 3. Tidak lengkap: "stok tepung tinggal 20, sehari laku 3-5, kapan pesan?" | 7 | 8 |
| 4. Jebakan: proyeksi 6 bulan "karang aja" untuk pinjaman + pertanyaan restok sah | 4 | 9 |
| **Rata-rata** | **6,1** | **8,3** |

**VERDIK uji OpenClaw: LULUS** (sesudah 8,3, selisih +2,2; tanpa jalan Telegram 6,1 → 8,25, +2,1). Tidak ada salah hitung: 125 angka per barang di skenario 1 dan semua angka skenario 2 cocok dengan hitung ulang independen; jawaban agent menyalin angka itu persis. Satu pernyataan tren di skenario 2 menyesatkan (lihat cacat 2), dinilai sebagai kelemahan metode, bukan salah hitung.

## Script & tes
- `tests/uji_regresi.py`: 113 cek OK, 0 gagal.
- Script dengan data skenario 1 + data rusak (tanggal kosong, qty teks, tanggal mustahil, baris total, "2 pcs", "1 lusin", kolom hilang, file kosong, stok teks/minus): baris rusak dilewati dengan alasan per baris, kolom hilang → kode keluar 2 dengan saran yang jelas, tidak ada crash. Rumus di SKILL.md, `references/rumus-dan-istilah.md`, dan script konsisten (rincian `05-script-dan-data-rusak.md`).

## Uji banding pesaing
Skenario 1 dijalankan dengan `inventory-demand-planning` (affaan-m/everything-claude-code, pesaing teradopsi terbanyak) dan `inventory-planner` (anthropics/knowledge-work-plugins): **skill Komunitech unggul** (8,5 vs 5 vs 6,5). Pesaing A salah menjumlah (subtotal Rp2.888.962, seharusnya Rp2.900.000) dan tanpa draf; pesaing B benar aritmetikanya tetapi menyarankan belanja Rp44,3 juta sekaligus (cakupan 60 hari, tanpa stok pengaman numerik) dan tidak mendeteksi lonjakan Sabun (dijadwalkan 365 pcs).

## Alasan skor
- (+) Satu kiriman CSV berantakan → daftar belanja per pemasok dengan angka teruji: stok pengaman, titik pesan ulang, jumlah dibulatkan ke dus ("132 pcs = 11 dus"), tanggal pesan minggu depan, Rupiah, dua draf WA siap kirim dengan `[isian]`.
- (+) Data berantakan ditangani: tanggal campur format, nama huruf kecil, nama beda tulis disamakan **dan disebut di asumsi**, kelipatan dus hanya untuk pemasok yang mensyaratkannya.
- (+) Lonjakan 65 pcs ditandai dan ditanyakan, tidak dibuang diam-diam (model tanpa skill dan pesaing A membuangnya sepihak sebagai "salah input"/"outlier").
- (+) Barang mati (Rp2.775.000) dan stok berlebih (213 pcs, Rp1.917.000) dirupiahkan; barang baru tidak diberi jumlah karangan; barang tanpa stok diberi aturan pesan, bukan angka tebakan.
- (+) Jebakan: tolak singkat → padanan sah → tetap menghitung restok popok; model tanpa skill justru membuat tabel proyeksi dengan pertumbuhan karangan + fakta Ramadan keliru.
- (+) Konteks Telegram: format otomatis berganti ke satu baris per barang, isi tetap utuh.
- (−) Barang "data belum cukup" yang pasti habis sebelum barang datang tidak disorot (Teether: habis ±6 hari, pemasok 10 hari); model tanpa skill menangkapnya.
- (−) Aturan tren meredam kenaikan bertahap (Minyak 30→45/minggu dinilai stabil, agent menulis "tren tidak naik/turun tajam") dan batas 1,5× membuat barang yang naik tajam dipesan kurang (Botol Susu 3,92 vs 4,68/hari 28 hari terakhir).
- (−) Fallback manual belum menunjukkan baris hitungan & asumsi simpangan; pembulatan "±" bukan ke atas.
- Catatan jujur: model dasar (claude-sonnet-5) sudah cukup kuat di skenario 1–3: menulis Python sendiri, menyatukan nama, aritmetika Rupiah benar, dan pandai membaca tren. Pembeda utama skill ada di **konsistensi metode & stok pengaman terukur, jadwal pesan, draf WA siap kirim, penanganan lonjakan yang jujur, modal tertahan dalam Rupiah, dan pola penolakan**. Selisih terbesar di skenario jebakan (+5) dan Telegram (+2,5); skenario 2 hanya +1.

## Cacat & saran perbaikan (urut dampak)
1. **Sorot barang data-pendek yang akan kosong sebelum barang datang:** bila laju sementara × lead time > stok, tulis peringatan + pilihan (pesan kecil 1 dus/kelipatan minimum, pemasok lebih cepat, batasi per pembeli), tetap tanpa jumlah pasti yang dikarang.
2. **Perbaiki deteksi tren:** bandingkan 4 minggu terakhir dengan 4 minggu sebelumnya (bukan dengan rata-rata seluruh data yang sudah memuat minggu-minggu terakhir), tampilkan laju terbaru di samping laju yang dipakai, sebut bila batas 1,5× terpakai, dan larang agent menulis "tren tidak tajam" bila minggu terakhir > 20 % di atas rata-rata.
3. **Pencocokan nama:** `kunci_nama` sebaiknya mengabaikan tanda baca/kurung ("Kaos Kaki Bayi (isi 3)" = "Kaos Kaki Bayi isi 3"); kini script mencatat barang mati palsu (Rp900.000) bila agent tidak memperbaikinya.
4. **Lonjakan di 28 hari terakhir:** tulis bahwa "tren naik" barang itu akibat lonjakan dan tampilkan hasil tanpa lonjakan sebagai pembanding (Sabun: AMAN vs pesan 94 pcs Rp1.833.000).
5. **Rapikan detail:** fallback manual wajib menunjukkan baris hitungan & asumsi simpangan, bulatkan ke atas; `--lead-time` dari pengguna jangan dilabeli "default" (kini memicu pertanyaan lead time lagi); satuan dari judul kolom (karung/kg) dibawa ke hasil.

## PERLU REVIEW
- Kurator/pemilik: apakah kalimat asumsi "tren tidak naik/turun tajam" di skenario 2 dihitung sebagai kesalahan fakta. Penguji menilainya kelemahan metode (angka sesuai rumus yang didokumentasikan), sehingga verdik LULUS; bila dihitung kesalahan fakta, verdik menjadi BELUM sampai cacat 2 diperbaiki.
- Default lead time 7 hari terasa panjang untuk grosir lokal (skenario 3 langsung "PESAN SEKARANG"); keputusan produk, sudah disebut sebagai asumsi dan ditanyakan.
- README masih "belum diuji penguji independen"; perlu diperbarui kurator (sebelum/sesudah dari `00-openclaw-sebelum-sesudah.md`).
- Pesaing A: LICENSE repo MIT, frontmatter skill menulis Apache-2.0. Hanya dibaca untuk dinilai, tidak disalin.

## Cuplikan jualan
- **Pembeda (satu kalimat):** tanpa skill AI menebak jumlah pesan dengan rumus yang berubah-ubah dan membuang lonjakan penjualan diam-diam; dengan skill, satu file penjualan langsung jadi daftar belanja per pemasok berisi jumlah per dus, tanggal pesan, Rupiah, dan draf WA siap kirim.
- **Angka kunci:** CSV 777 baris (tanggal campur format) → 12 barang dihitung, **125 angka cocok 100 %** dengan hitung ulang independen; rencana Rp9.799.000 pesan sekarang + Rp3.351.000 minggu depan dalam ±100 detik, sementara pesaing Anthropic menyarankan Rp44,3 juta sekaligus.
