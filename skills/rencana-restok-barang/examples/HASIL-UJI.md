# Hasil uji: rencana-restok-barang

- **Tanggal:** 2026-10-14
- **Penguji:** agent penguji independen Komunitech (bukan pembuat; hanya membaca folder skill)
- **Versi diuji:** 1.0.1 (uji ulang terbatas setelah perbaikan 5 temuan versi 1.0.0)
- **Platform:** openclaw (uji otomatis agent), OpenClaw 2026.10.2 lokal, model router Komunitech claude-sonnet-5; skenario normal utama juga di konteks kanal Telegram (tanpa mengirim)
- **Cakupan uji ulang:** skenario 1 (lokal + Telegram) dan 2, sisi SESUDAH, home baru dengan skill 1.0.1, data & pesan sama dengan putaran 1. Sisi SEBELUM memakai hasil putaran 1. Skenario 3–4 **tidak diulang**; nilainya dari 1.0.0. Banding pesaing dari putaran 1.
- **Rincian:** `00-openclaw-sebelum-sesudah.md` (jawaban utuh, termasuk riwayat 1.0.0), `00-banding-pesaing.md`, `01`–`05`, data di `data/`

## Skor kualitas: 8,5/10

| Skenario | Tanpa skill | Dengan skill 1.0.0 | Dengan skill 1.0.1 |
|---|---|---|---|
| 1. Normal utama, lokal: toko bayi online, CSV 90 hari (777 baris, tanggal campur), stok 12 barang, 2 pemasok (satu kelipatan dus 12) | 7 | 8,5 | **9** |
| 1. Normal utama, konteks Telegram | 6 | 8,5 | **8,5** |
| 2. Warung sembako, total mingguan 8 minggu ditempel, stok 2 barang belum diketahui | 6,5 | 7,5 | **9** |
| 3. Tidak lengkap: "stok tepung tinggal 20, sehari laku 3-5, kapan pesan?" (tidak diulang) | 7 | 8 | 8 |
| 4. Jebakan: proyeksi 6 bulan "karang aja" untuk pinjaman + pertanyaan restok sah (tidak diulang) | 4 | 9 | 9 |
| **Rata-rata** | **6,1** | **8,3** | **8,7** |

**VERDIK uji OpenClaw 1.0.1: LULUS** (sesudah 8,7, selisih +2,6; tanpa jalan Telegram 6,1 → 8,75). Ketepatan angka: skenario 1, 180 dari 182 angka/label cocok dengan hitung ulang independen; skenario 2, 63/63. Dua angka yang beda berasal dari **satu bug presisi script**: Dot Bayi "habis ±139 hari (2 Mar 2027)", seharusnya tepat 140 hari (3 Mar). Barang itu AMAN/stok berlebih, jadi keputusan pesan tidak berubah. Jalan Telegram juga menulis satu keterangan keliru ("Botol Susu dibatasi maksimal 2×", padahal batas tidak terpakai), tanpa mengubah angka. Penguji menilai keduanya **ketidaktepatan kecil tanpa dampak keputusan**, bukan kesalahan angka/fakta yang menggugurkan (lihat PERLU REVIEW).

**Angka kunci 1.0.1 (skenario 1):** pesan sekarang **Rp10.879.000** (Bedak 49, Popok 79, Botol Susu 96 = 8 dus, Tisu 132 = 11 dus) + minggu depan **Rp3.351.000** (Sabun 94 ±17 Okt, Minyak Telon 57 ±18 Okt, Kaos Kaki 48 = 4 dus ±20 Okt); 3 barang akan kosong sebelum kiriman datang (Teether ±4 hari, Botol Susu ±2, Bedak ±1); barang mati Rp2.775.000; stok berlebih Dot 207 pcs Rp1.863.000.

## Script & tes
- `tests/uji_regresi.py`: **139 cek OK, 0 gagal**.
- Script dengan data skenario 1 (nama asli, termasuk "(isi 3)") dan skenario 2 dijalankan ulang; semua angka per barang dihitung ulang independen: hari habis vs lead time & hari kosong, faktor tren + batas 0,5–2×, jumlah per kelipatan dus, nilai Rupiah, deteksi lonjakan + hasil tanpa lonjakan, pencocokan nama. Nama "(isi 3)" kini cocok otomatis; nama yang hanya mirip masuk "MUNGKIN BARANG YANG SAMA" dan ditanyakan. Data rusak & kolom hilang: perilaku sama dengan 1.0.0 (baris dilewati beralasan, kode keluar 2 + saran). Rincian `05-script-dan-data-rusak.md`.

## Alasan skor (1.0.1)
- (+) **Akan kosong sebelum barang datang** paling atas, termasuk barang data pendek (Teether ±4 hari) dengan saran 1 dus tanpa jumlah karangan. Cacat 1 versi 1.0.0 tertutup.
- (+) **Tren per barang** dari 4 minggu terakhir vs sebelumnya: Minyak "naik 27 %" → 82 (bukan "stabil"/71); Botol Susu naik 185 % → 96 pcs dengan laju terbaru; batas 0,5× Pelampung disebut terbuka (Telegram). Tidak ada lagi kalimat "tren tidak tajam".
- (+) **Lonjakan** Sabun: disebut "termasuk", dibandingkan dengan hasil tanpa lonjakan (AMAN), ditanyakan "promo/borongan?", dan dijelaskan bahwa tren naik terjadi karena lonjakan itu.
- (+) Nama beda tulis cocok otomatis; satuan sesuai barang (karung, botol, kg, dus); `--lead-time` pengguna tidak ditanyakan ulang.
- (+) Semua kekuatan 1.0.0 tetap: daftar per pemasok, kelipatan dus, tanggal pesan, draf WA siap kirim, barang mati & stok berlebih dalam Rupiah, 3 pertanyaan, disclaimer, format Telegram satu baris per barang.
- (−) Bug presisi script: Dot habis 139 vs 140 hari.
- (−) Telegram: "dibatasi maksimal 2×" untuk barang yang tidak kena batas; Teether di bagian bawah "pesan bila stok tinggal sedikit" agak bertentangan dengan saran "pesan kecil hari ini"; nama file pengguna disebut di asumsi.
- (−) Lokal: Pelampung "habis ±48 hari" tanpa menyebut bahwa itu dengan laju yang dibatasi (1,14 vs nyata 0,61/hari).
- (−) Agent dua kali `find /` untuk mencari script (Telegram, skenario 2).
- Catatan jujur: model dasar tetap kuat (menulis Python sendiri, aritmetika benar). Pembeda utama ada di konsistensi metode, stok pengaman terukur, penanda "akan kosong", tren per barang yang jujur, penanganan lonjakan, draf siap kirim, dan pola penolakan (skenario 4).

## Cacat tersisa & saran (urut dampak)
1. **Presisi laju:** hitung laju dipakai langsung dari laju 4 minggu terakhir bila tidak kena batas (bukan rata-rata × rasio), atau bulatkan laju (mis. 20 desimal) sebelum `habis = ⌊stok ÷ laju⌋`.
2. **Kalimat batas:** untuk barang naik/turun yang tidak kena batas, `kalimat_tren` menyebut "tidak kena batas"; SKILL.md melarang menyebut batas 2×/0,5× bila `tren_dibatasi` salah.
3. **Barang yang kena batas:** tampilkan juga hari habis dengan laju terbaru (Pelampung: ±90 hari dengan 0,61/hari vs ±48 hari dengan 1,14/hari).
4. **Lokasi script:** tulis jalur umum (`~/.openclaw/skills/rencana-restok-barang/scripts/rencana_restok.py`) agar agent tidak `find /`.
5. **Kecil:** SKILL.md "Rumus (persis)" masih memakai "μ" untuk ROP/target/habis (seharusnya "laku/hari dipakai"); ringkasan script "barang mati 0 (modal tertahan Rp0)"; tanggal tanpa tahun di tabel tempel belum terbaca script.

## PERLU REVIEW
- Kurator/pemilik: apakah "habis ±139 hari" (seharusnya 140, barang AMAN) dan keterangan "dibatasi maksimal 2×" di jalan Telegram dihitung sebagai kesalahan angka/fakta. Penguji menilainya ketidaktepatan kecil tanpa dampak keputusan sehingga verdik LULUS. Bila diterapkan ketat, verdik menjadi BELUM sampai cacat 1–2 diperbaiki (perbaikan kecil, bisa diuji ulang cukup dengan script + 1 jalan).
- Default lead time 7 hari (skenario 3, tidak diulang) tetap keputusan produk.
- Pesaing A: LICENSE repo MIT, frontmatter skill menulis Apache-2.0. Hanya dibaca untuk dinilai.

## Cuplikan jualan
- **Pembeda (satu kalimat):** tanpa skill, AI menebak jumlah pesan dengan rumus berubah-ubah dan membuang lonjakan penjualan diam-diam; dengan skill, satu file penjualan langsung jadi daftar belanja per pemasok (jumlah per dus, tanggal pesan, Rupiah, draf WA) dengan barang yang akan kosong sebelum kiriman datang di paling atas.
- **Angka kunci:** CSV 777 baris (tanggal campur format) → rencana **Rp10.879.000 pesan sekarang + Rp3.351.000 minggu depan** dalam ±100 detik, 3 barang yang akan kosong ditandai paling atas. Pesaing Anthropic menyarankan Rp44,3 juta sekaligus (putaran 1).

## Riwayat

### Versi 1.0.0 (2026-10-14): 6,1 → 8,3, LULUS
**Skor kualitas 1.0.0: 8/10**

| Skenario | Tanpa skill | Dengan skill |
|---|---|---|
| 1. Normal utama, lokal: toko bayi online, CSV 90 hari (777 baris, tanggal campur), stok 12 barang, 2 pemasok (satu kelipatan dus 12) | 7 | 8,5 |
| 1. Normal utama, konteks Telegram | 6 | 8,5 |
| 2. Warung sembako, total mingguan 8 minggu ditempel, stok 2 barang belum diketahui | 6,5 | 7,5 |
| 3. Tidak lengkap: "stok tepung tinggal 20, sehari laku 3-5, kapan pesan?" | 7 | 8 |
| 4. Jebakan: proyeksi 6 bulan "karang aja" untuk pinjaman + pertanyaan restok sah | 4 | 9 |
| **Rata-rata** | **6,1** | **8,3** |

**VERDIK uji OpenClaw: LULUS** (sesudah 8,3, selisih +2,2; tanpa jalan Telegram 6,1 → 8,25, +2,1). Tidak ada salah hitung: 125 angka per barang di skenario 1 dan semua angka skenario 2 cocok dengan hitung ulang independen; jawaban agent menyalin angka itu persis. Satu pernyataan tren di skenario 2 menyesatkan (lihat cacat 2), dinilai sebagai kelemahan metode, bukan salah hitung.

**Cacat 1.0.0 (ditangani di 1.0.1; bagian hitungan manual di butir 5 belum diuji ulang karena skenario 3 tidak diulang):**
1. **Sorot barang data-pendek yang akan kosong sebelum barang datang:** bila laju sementara × lead time > stok, tulis peringatan + pilihan (pesan kecil 1 dus/kelipatan minimum, pemasok lebih cepat, batasi per pembeli), tetap tanpa jumlah pasti yang dikarang.
2. **Perbaiki deteksi tren:** bandingkan 4 minggu terakhir dengan 4 minggu sebelumnya (bukan dengan rata-rata seluruh data yang sudah memuat minggu-minggu terakhir), tampilkan laju terbaru di samping laju yang dipakai, sebut bila batas 1,5× terpakai, dan larang agent menulis "tren tidak tajam" bila minggu terakhir > 20 % di atas rata-rata.
3. **Pencocokan nama:** `kunci_nama` sebaiknya mengabaikan tanda baca/kurung ("Kaos Kaki Bayi (isi 3)" = "Kaos Kaki Bayi isi 3"); kini script mencatat barang mati palsu (Rp900.000) bila agent tidak memperbaikinya.
4. **Lonjakan di 28 hari terakhir:** tulis bahwa "tren naik" barang itu akibat lonjakan dan tampilkan hasil tanpa lonjakan sebagai pembanding (Sabun: AMAN vs pesan 94 pcs Rp1.833.000).
5. **Rapikan detail:** fallback manual wajib menunjukkan baris hitungan & asumsi simpangan, bulatkan ke atas; `--lead-time` dari pengguna jangan dilabeli "default" (kini memicu pertanyaan lead time lagi); satuan dari judul kolom (karung/kg) dibawa ke hasil.
