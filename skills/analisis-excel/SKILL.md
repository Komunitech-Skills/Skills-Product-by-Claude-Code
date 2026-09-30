---
name: analisis-excel
description: Menganalisis file spreadsheet milik pengguna (Excel .xlsx atau CSV, apa pun isinya - biaya, stok, pelanggan, nilai siswa, absensi, keuangan) untuk menjawab pertanyaan bisnis - profil data (kolom, kosong, duplikat, outlier), ringkasan jumlah/rata-rata/median/min/max, pivot/group-by per kategori atau bulan, tren bulanan, top-N/Pareto, perbandingan dua periode atau dua file (persen naik/turun), dan membersihkan data (angka "Rp 1.234.567,89", tanggal campur, spasi, huruf besar-kecil) - dengan tabel Markdown, CSV hasil, narasi temuan bahasa awam, dan saran grafik. Angka dihitung script, bukan dikira. Gunakan saat pengguna mengirim file Excel/CSV dan bertanya "analisis file ini", "total per kategori", "bulan mana paling tinggi", "bandingkan Agustus vs September", "rapikan data Excel", analyze spreadsheet, excel data analysis, pivot table, data cleaning, summary statistics. Bukan untuk rekap penjualan kasir/marketplace (rekap-penjualan-csv), laporan iklan (laporan-iklan-mingguan), statistik lanjut/prediksi/ML.
---

# Analisis Excel & CSV untuk Awam

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Pengguna awam cukup mengirim file Excel/CSV dan bertanya dengan bahasa sehari-hari; agent menjawab
dengan **tabel siap tempel, angka yang dihitung script, narasi temuan, dan saran grafik**. Semua
angka berasal dari `scripts/analisis.py` (Python standar, Decimal untuk uang, bisa baca `.xlsx`
langsung tanpa openpyxl/pandas). Agent **hanya menjelaskan**, tidak menghitung sendiri.

**Jujur soal batas:** skill ini **paling andal untuk tabel rapi** — satu baris judul kolom, lalu satu
baris = satu transaksi/orang/barang. **Laporan berformat** (subtotal per kelompok, baris Total/rekap di
tengah, rincian pembayaran di bawah total, beberapa tabel dalam satu sheet, cetakan multi-halaman)
dikenali sebisanya dengan pengaman umum, tetapi tata letaknya tidak terbatas: untuk file seperti itu
**angka selalu dikonfirmasi ke pengguna** sebelum dianggap final.

## Kapan digunakan
- "Tolong analisis file Excel ini", "isinya apa saja, ada yang aneh?" → `profil`
- "Total/rata-rata pengeluaran berapa?" → `ringkas`
- "Total per kategori/cabang/divisi", "rata-rata nilai per kelas" → `pivot`
- "Bulan mana paling tinggi?", "trennya naik atau turun?" → `tren`
- "10 pelanggan/barang terbesar", "yang paling sedikit" → `top`
- "Bandingkan Agustus vs September", "file bulan ini vs bulan lalu" → `banding`
- "Rapikan data ini (angka Rp, tanggal campur, huruf besar-kecil)" → `bersihkan`

## Kapan TIDAK digunakan
- Rekap **penjualan** dari ekspor kasir/Shopee/Tokopedia berstatus pesanan (omzet, produk terlaris,
  status batal) → `rekap-penjualan-csv`. Data penjualan **buatan sendiri di Excel** (.xlsx) tetap
  memakai skill ini.
- Laporan iklan Meta/TikTok/Shopee/Google Ads → `laporan-iklan-mingguan`.
- Laporan laba rugi/neraca, pajak, gaji → skill keuangan/pajak yang sesuai.
- Statistik lanjut (regresi, uji hipotesis, korelasi), prediksi/forecast, machine learning →
  jelaskan skill ini hanya menganalisis data yang sudah terjadi; sarankan ahli data/statistik.
- Membuat/mengedit file .xlsx (rumus, format, grafik di dalam file) → skill ini hanya **membaca**
  dan menulis CSV hasil.
- File > 50 MB atau > ±300 ribu baris → minta dipecah per bulan/sheet (lihat Batasan).

## Input
| Info | Wajib? | Default bila tidak disebut |
|---|---|---|
| File `.xlsx`/`.xlsm`/`.csv`/`.tsv`/`.txt` | Ya | — (minta dikirim) |
| Pertanyaan/tujuan | Tidak | Jalankan `profil` lalu `ringkas`, beri 3 temuan utama |
| Sheet (bila workbook > 1 sheet) | Tidak | Sheet pertama yang terlihat; sebutkan ke pengguna. Pertanyaan lintas sheet (mis. "Jan–Sep" di sheet per bulan/kuartal) → `--sheet semua` |
| Kolom kategori / nilai / tanggal | Tidak | Tebak dari hasil `profil` (kolom teks / angka-uang / tanggal) dan **sebutkan asumsinya** |
| Periode pembanding | Untuk `banding` | Tanyakan; bila pengguna mau cepat, bandingkan 2 bulan terakhir yang ada di data |

Bila informasi kurang, tanyakan **sekali** dalam satu pesan singkat (mis. "Kolom mana yang berisi
nilai uangnya: Nominal atau Harga? Mau dibandingkan bulan apa dengan apa?"). Bila pengguna bilang
"langsung aja", pakai default di atas dan tulis asumsinya di awal jawaban.

## Langkah kerja
Path script relatif terhadap folder SKILL.md ini. **Windows:** ganti `python3` dengan `python` atau `py`.

1. **WAJIB: jalankan `profil` dulu sebelum menyebut angka apa pun** (juga bila pengguna sudah
   menyebut kolom):
   ```bash
   python3 <folder-skill-ini>/scripts/analisis.py profil "<file>" [--sheet "Nama Sheet"]
   ```
   Workbook banyak sheet: `daftar "<file>"` untuk melihat semua sheet. Dari hasil `profil` catat
   nama kolom persis, tipe (tanggal/angka/teks/kode), kolom uang, dan peringatan.
   **Cek sekilas (v1.0.7, wajib):** `profil` menampilkan **5 baris pertama & 5 baris terakhir yang
   DIPAKAI**, tabel **baris DIKELUARKAN**, dan tabel **kemungkinan baris ringkasan**. Periksa dengan
   mata: adakah baris yang jelas bukan transaksi tetapi ikut dipakai — label Total/Subtotal/Jumlah/
   Rekap/Saldo, "<Nama> Total", rincian bayar (Tunai/QRIS/Transfer/Debit), judul bagian (mis.
   "PENGELUARAN"), judul kolom kedua, "Halaman 1 dari 2", baris kelompok yang angkanya = jumlah
   baris-baris di bawahnya (pivot yang disalin)? **Judul kolom** juga dicek (v1.0.8): nama kolom
   berupa tanggal/angka (mis. "2026-09-01", "150000") berarti tabel tanpa judul kolom — script
   memberi PERINGATAN TEGAS dan memakai Kolom1..N; tanyakan nama kolomnya ke pengguna. Kalau ada masalah dan script tidak menyebutnya,
   **jangan beri angka final**: tanyakan sekali ke pengguna, lalu ulangi dengan `--buang-baris N`
   atau `--sampai-baris N` / `--mulai-baris N`.
   **Satu sheet per bulan/kuartal/cabang** dan pertanyaannya mencakup beberapa sheet → pakai
   `--sheet semua` (semua sheet terlihat) atau `--sheet "Q1,Q2,Q3"` di subperintah mana pun.
   Script menggabungkan sheet yang judul kolomnya sama, membuang baris TOTAL tiap sheet, dan
   menambah kolom `Sheet` (bisa dipakai `--grup Sheet`). **Jangan** menjumlah hasil per sheet
   sendiri. **Sheet rekap/ringkasan dilewati** (v1.0.3) agar total tidak DOBEL: nama berisi
   Ringkasan/Rekap/Total/Summary/Resume, isinya = jumlah sheet lain, atau sedikit baris berlabel
   bulan/triwulan → peringatan "TIDAK digabung: tampak sheet REKAP"; paksa ikut dengan
   `--sertakan "<nama>"` hanya bila pengguna memastikan sheet itu data. Peringatan
   "kemungkinan DOBEL HITUNG" → sampaikan ke pengguna dan pakai total tanpa sheet itu. Acuan
   struktur = sheet yang paling banyak cocok (ganti dengan `--acuan "TW1"`). Bila ada peringatan
   "TIDAK digabung" untuk sheet yang dibutuhkan, ulangi dengan daftar sheet, mis. `--sheet "TW1,TW2,TW3,TW4"`.
2. **Jalankan subperintah yang menjawab pertanyaan** (nama kolom tidak peka huruf besar-kecil,
   boleh sebagian nama bila unik):
   ```bash
   python3 <...>/analisis.py ringkas  "<file>" [--kolom "Nominal"]
   python3 <...>/analisis.py pivot    "<file>" --grup "Kategori" --nilai "Nominal" [--fungsi jumlah|rata|median|hitung|min|max] [--kolom-pivot "Divisi"]
   python3 <...>/analisis.py pivot    "<file>" --grup "Tanggal" --per bulan --nilai "Nominal"
   python3 <...>/analisis.py tren     "<file>" --nilai "Nominal" [--tanggal "Tanggal"] [--per bulan|minggu|hari|kuartal|tahun]
   python3 <...>/analisis.py tren     "<file.xlsx>" --sheet semua --nilai "Total"      # gabung sheet Q1+Q2+Q3
   python3 <...>/analisis.py top      "<file>" --grup "Pelanggan" --nilai "Total" --n 10 [--terbawah]
   python3 <...>/analisis.py banding  "<file>" --nilai "Nominal" --periode-a 2026-08 --periode-b 2026-09 [--grup "Kategori"]
   python3 <...>/analisis.py banding  "<file-lama>" --file-b "<file-baru>" --nilai "Total" [--grup "Produk"]
   python3 <...>/analisis.py bersihkan "<file>" --keluar "<file>-bersih.csv" [--excel-id] [--buang-duplikat]
   ```
   Opsi umum semua subperintah: `--sheet` (+ `--acuan`, `--sertakan`), `--baris-header N` (alias `--header-baris`),
   `--tanpa-header` (tabel tanpa baris judul kolom; = `--baris-header 0`), `--filter "Kolom=A|B"`,
   `--buang-baris 5,9` / `--pertahankan-baris 12` (gabungan sheet: `"TW1:7"`; lihat langkah 3),
   `--mulai-baris N` / `--sampai-baris N` (hanya baca sebagian baris file, mis. satu tabel dari dua),
   `--dari 2026-07 --sampai 2026-09`, `--tipe "No HP=kode"`, `--urutan-tanggal mdy`,
   `--keluar hasil.csv` (simpan tabel hasil), `--excel-id` (CSV untuk Excel berbahasa Indonesia:
   pemisah `;` dan koma desimal), `--json` (keluaran mesin), `--tampilkan-pribadi` (lihat Aturan). Periode: `2026-09`, `Sep 2026`,
   `2026`, `Q3 2026`, `2026-09-01..2026-09-15`.
3. **Baca keluaran** (Markdown siap tempel). Salin tabel **apa adanya**; jangan mengubah angka,
   pembulatan, atau persen. **WAJIB** baca dua blok di paling atas keluaran (JSON:
   `baris_dikeluarkan`, `kemungkinan_ringkasan`, `total_alternatif`):
   - **"BARIS DIKELUARKAN"** → sebutkan ke pengguna baris mana yang tidak dihitung dan isinya
     (rumus SUM/AVERAGE, Total/Grand Total di bawah tabel, catatan kaki, Saldo Awal).
   - **"PERINGATAN TEGAS — Kemungkinan baris ringkasan ikut terhitung"** → baris itu MASIH dihitung.
     **Jangan beri angka final** sebelum: tanya pengguna **sekali** ("Baris 14 berisi Jumlah=4.860.000
     tanpa keterangan — itu baris total (rumus) atau transaksi?") **atau** tampilkan **kedua total**
     (DENGAN dan TANPA baris itu, dari pesan script). Bila pengguna menjawab "itu total", ulangi perintah
     dengan `--buang-baris N[,M]`; bila "itu data", pakai hasil awal (atau `--pertahankan-baris N`).
     Alasan kandidat (v1.0.7): label ringkasan di mana pun pada baris yang kolom lainnya kosong
     ("Jakarta Total" dari Excel *Data › Subtotal*), angka = jumlah blok baris tepat di atasnya, dan
     **rincian** (baris Tunai/QRIS/Transfer yang jumlahnya = baris Total → bisa dobel). v1.0.8: juga baris
     **terisi lengkap** — angka di ≥ 2 kolom = jumlah blok di atasnya ("Subtotal Cabang X", "Grand Total",
     "TOTAL" jurnal), "Jumlah Hadir"/"Total" di kolom tanggal/angka, label = judul kelompok sebelumnya
     ("SEMEN" … "Subtotal Semen", "Jawa" … "Jawa Total"), dan **subtotal di atas anak-anaknya** (pivot
     bentuk ringkas: "Jawa 5.000.000" lalu "Kopi", "Teh"). "TANPA SEMUA baris
     itu" = total tanpa semua kandidat; per kandidat juga ditampilkan. Bila pengguna bilang hanya
     sebagian yang ringkasan, buang baris itu saja. v1.0.9: kelompok pivot beranak **satu** ("Bogor 9"
     lalu "Kopi 9") tidak lagi membatalkan deteksi kelompok lain.
   - **PENGAMAN SILANG Grand Total (v1.0.9, lapis kedua untuk tata letak yang belum dikenal):** angka baris
     Total/Grand Total/Jumlah di file (yang dikeluarkan, atau kandidat di baris terakhir) dibandingkan
     dengan total hitungan script per kolom. **"PERINGATAN TEGAS — PENGAMAN SILANG: Total hitungan ≠ …"**
     (mis. "tepat 2×" = subtotal/baris kelompok ikut terhitung) → **jangan beri angka final**; tampilkan
     kedua angka (hitungan & Grand Total di file) dan tanya pengguna / cek tata letak dengan `profil`.
     "PENGAMAN SILANG: … = total TANPA baris kandidat" → total TANPA kemungkinan besar benar (tetap
     konfirmasi). Catatan "Pengaman silang: … COCOK dengan baris 'Total' di file" → keyakinan naik;
     sebutkan ke pengguna ("cocok dengan Grand Total di file Anda"). v1.0.10: angka Total di file hanya
     jadi total alternatif bila ada "Kemungkinan DOBEL HITUNG" (tepat 2×/3×). Bila pesan berkata "Total di
     file (Y) tidak sama dengan jumlah baris data (X) … BUKAN jawaban alternatif" → **jangan pakai Y sebagai
     jawaban**; beri X, katakan Total di file perlu dicek, dan sebutkan penyebab dari pesan (mis. "baris 4, 7
     berisi angka yang tersimpan sebagai teks — SUM Excel tidak menjumlahkannya"). "PERINGATAN" tanpa
     TEGAS = penyebab ditemukan / sebagian kolom beda → X boleh diberikan sebagai hasil.
   - **`GAGAL: File ini berisi LEBIH DARI SATU TABEL`** → jelaskan ke pengguna; tanyakan tabel mana
     yang dimaksud, lalu ulangi dengan `--sampai-baris N` (tabel pertama) atau `--mulai-baris N`
     (tabel kedua) sesuai pesan. Jangan pakai `--paksa` untuk menggabungkan tabel berbeda.
4. **Tulis jawaban** dengan format di bawah. Narasi hanya boleh memakai angka yang ada di
   keluaran script (bagian "Temuan" sudah berisi fakta terhitung).
5. **Tawarkan langkah lanjut** yang relevan (mis. setelah `pivot` → "mau saya lihat trennya per
   bulan?"), dan tawarkan `--keluar` bila pengguna ingin tabelnya dibuka di Excel.
6. **File baru (`bersihkan`, `--keluar`) hanya setelah pengguna setuju:** sebutkan dulu path lengkap
   file yang akan dibuat (mis. "Saya simpan versi bersih ke `<folder-kerja>/biaya-bersih.csv`, oke?"),
   tulis setelah ia mengiyakan. File asli **tidak pernah** diubah/ditimpa; path `--keluar` tidak boleh
   sama dengan file asli. Bila pengguna minta "langsung aja", tetap sebutkan path file yang dibuat, dan file yang sudah ada tidak pernah ditimpa tanpa izin.
   **Sebelum memakai `--keluar`, cek apakah file itu sudah ada.** Bila ada, tanyakan: "File X sudah ada,
   timpa atau simpan sebagai X-2?". Jangan menimpa tanpa jawaban tegas; "langsung aja" bukan izin
   menimpa. `--timpa` hanya dipakai setelah pengguna setuju (tanpa `--timpa`, script menolak dengan
   "GAGAL: File keluaran sudah ada").
   Peringatan script seperti "rumus tanpa nilai tersimpan" disampaikan apa adanya beserta sarannya
   (buka di Excel lalu Simpan); jangan menilai sendiri bahwa dampaknya "tidak signifikan".

Bila script gagal (kode keluar 2) → baca pesan `GAGAL:` (sudah berbahasa awam), sampaikan ke
pengguna, dan ikuti sarannya (mis. sebutkan kolom yang tersedia, minta simpan ulang file).
Bila Python sama sekali tidak tersedia → ikuti `references/rumus-excel-manual.md` (langkah
Excel/Google Sheets yang setara), dan katakan hasil **belum diverifikasi script**.

## Format output
```
**Jawaban singkat:** <1–2 kalimat menjawab pertanyaan pengguna, dengan angka dari script>

<tabel Markdown dari script, apa adanya>

**Temuan:**
1. <fakta terhitung + artinya dalam bahasa awam>
2. ...
3. ...

**Saran grafik:** <dari script + 1 kalimat cara buatnya di Excel/Sheets>

**Perlu dicek:** <baris yang DIKELUARKAN + isinya; kemungkinan baris ringkasan + total DENGAN/TANPA
(bila belum dikonfirmasi pengguna); lalu peringatan script lain, diringkas bahasa awam>
(Asumsi: <kolom/sheet/periode yang dipakai>) — File hasil: <nama CSV bila --keluar>
```
Template lengkap: `templates/laporan-analisis.md`. Angka rupiah pakai titik ribuan (`Rp 1.250.000`),
persen 1 desimal dengan koma (`12,5%`).

## Contoh
**Pengguna:** "Ini file biaya operasional kantor (Excel). Pengeluaran paling besar di mana, dan
September naik berapa dibanding Agustus?"

**Agent:** `profil` → kolom `Tanggal` (tanggal), `Kategori` (teks), `Nominal` (angka, uang); lalu
`pivot --grup Kategori --nilai Nominal` dan `banding --nilai Nominal --periode-a 2026-08
--periode-b 2026-09 --grup Kategori`. Jawaban: "Pengeluaran terbesar adalah Sewa, Rp 13.500.000
(48,9% dari total). September naik 73,5% dibanding Agustus (Rp 7.555.000 → Rp 13.110.000),
terutama karena Transport naik Rp 4.955.000 (ada ganti ban Rp 5.400.000)..." + tabel + peringatan
(1 sel rumus tanpa nilai tersimpan, baris TOTAL dilewati, "listrik & air"/"LISTRIK & AIR" digabung).
Contoh lengkap nyata: `examples/uji-pembuat-01-biaya-operasional-xlsx.md`.

## Aturan penting
- **Jangan mengarang angka.** Setiap angka di jawaban harus ada di keluaran script. Bila perlu
  angka yang belum ada, jalankan subperintah lagi (mis. `--filter`).
- **Sampaikan semua peringatan** yang memengaruhi angka: nilai tidak valid yang tidak dihitung,
  baris Total yang dilewati, rumus tanpa nilai, sel gabungan, tanggal ambigu, periode tidak penuh,
  kategori yang digabung. Jangan disembunyikan.
- **Periode tidak penuh** (mis. data September baru sampai tanggal 26) → jangan menyimpulkan
  "turun" tanpa menyebutnya; tawarkan pembanding rata-rata per hari (sudah dihitung `banding`).
- **Tanggal ambigu** (semua tanggal ≤ 12, mis. 01/02/2026) → tanya pengguna format hari/bulan
  atau bulan/hari; bila bulan/hari, ulangi dengan `--urutan-tanggal mdy`.
- **"Rata-rata" ambigu** (mis. rata-rata jam lembur per catatan atau per karyawan?) → tanyakan
  sekali; `pivot --fungsi rata` = rata-rata per baris yang terisi (kolom "Nilai terisi" = pembaginya).
- **Kolom "Baris" vs "Nilai terisi"**: Baris = semua baris di kelompok; Nilai terisi = yang angkanya
  dihitung. Bila berbeda, sebutkan sel kosong yang tidak dihitung.
- **Kolom kode** (No HP, NIK, kode barang, nomor urut) tidak pernah dijumlah. Bila script salah
  mengira, perbaiki dengan `--tipe "Kolom=kode"` atau `--tipe "Kolom=angka"`.
- **Korelasi ≠ sebab.** Tulis "naik bersamaan", bukan "menyebabkan". Saran harus dari data
  (hindari saran generik).
- **Data pribadi (UU PDP):** script menyamarkan NIK/No HP/email/rekening di tabel (`3201•••…408`).
  Salin apa adanya; **jangan** menambah `--tampilkan-pribadi` kecuali pengguna pemilik data sendiri
  memintanya secara tegas, dan ingatkan agar hasilnya tidak dibagikan. Bila script memperingatkan
  "data SENSITIF" (mis. gaji per orang), sampaikan peringatannya dan tawarkan agregat per
  divisi/jabatan. Jangan kutip isi baris per orang di narasi.
- File pengguna diproses **lokal**; jangan mengunggah isinya ke layanan eksternal.

## Batasan & penanganan error
Rincian lengkap: `references/format-didukung.md`.
- **Format:** `.xlsx`/`.xlsm` (dibaca langsung: teks bersama, angka, tanggal serial Excel sistem
  1900 & 1904 — termasuk bug 29-Feb-1900 yang ditandai tidak valid —, beberapa sheet termasuk
  gabungan `--sheet semua`, sel kosong, sel gabungan) dan CSV (UTF-8, UTF-8 BOM, UTF-16, cp1252/ANSI; pemisah `,` `;` tab `|`, baris
  `sep=;`). `.xls` lama, `.ods`, file berkata sandi → pesan jelas agar disimpan ulang sebagai .xlsx/CSV.
- **Header tidak di baris 1** (ada judul laporan di atas) → dideteksi otomatis dan diberitahukan;
  koreksi dengan `--baris-header N`.
- **Tabel tanpa judul kolom (v1.0.8):** bila "judul kolom" terpilih berisi tanggal/angka yang jenisnya
  sama dengan isi kolom di bawahnya → baris itu DIHITUNG sebagai data, kolom dinamai Kolom1..N, dan
  PERINGATAN TEGAS. Tahun (2024, 2025) dan nomor urut (1, 2, 3) sebagai judul kolom tetap dianggap judul.
  Bila baris 1 ternyata memang judul, ulangi dengan `--baris-header 1`.
- **Judul kelompok satu sel** (mis. "SEMEN", "CAT" di atas barang-barangnya; ≥ 2 baris seperti itu) →
  dilewati + disebut di "BARIS DIKELUARKAN" (v1.0.8). **CSV e-Faktur lama (FK/LT/OF)** → `GAGAL` khusus
  + jalan keluar `--paksa --filter "FK=FK"`. Kolom Tahun/Masa Pajak/Bulan berisi bilangan bulat = periode
  (tidak dijumlah). Kolom **nomor urut** (judul No/No./Nomor/#, atau Kolom1 tabel tanpa judul berisi 1, 2,
  3, … n) tidak dijumlah; judul kolom tahun tampil "2023", bukan "2.023" (v1.0.9).
- **Cetakan multi-halaman (v1.0.7):** judul kolom yang berulang (≥ 50% nama kolom sama di posisi yang
  sama, tanpa angka), judul laporan yang berulang, dan "Halaman x dari y"/"Page x of y" dilewati + info.
  **Judul kolom BERBEDA di tengah** (tabel kedua) → `GAGAL` + nomor baris awal tabel kedua (lihat langkah 3).
- **Rumus tanpa nilai tersimpan** (file dari aplikasi lain) → dianggap kosong + peringatan
  "buka di Excel lalu Simpan". **Galat Excel** (`#N/A`, `#DIV/0!`) → kosong + peringatan.
- **Sel gabungan**: teks yang digabung ke bawah disalin ke tiap baris (agar bisa dikelompokkan);
  angka gabungan tidak disalin (agar tidak dobel); gabungan mendatar (judul) diabaikan.
- **Angka meragukan** (`15.000.00`, `15000.500`, notasi ilmiah `1,5E+06`) sengaja tidak ditebak →
  dilaporkan "tidak valid" dengan nomor barisnya.
- **Batas ukuran:** file ≤ 50 MB (lebih besar ditolak kecuali `--paksa`), nyaman hingga ±300 ribu
  baris; pivot silang maks. 15 kolom. Tidak untuk data "big data".
- **Pembulatan:** perhitungan memakai Decimal presisi penuh; tampilan rupiah dibulatkan ke rupiah
  terdekat, persen 1 desimal (0,5 menjauhi nol). CSV hasil menyimpan hingga 2 desimal.
- **Keamanan CSV hasil:** teks yang diawali `=`, `+`, `-`, `@` diberi awalan `'` agar tidak
  dieksekusi sebagai rumus saat dibuka di Excel. File asli tidak pernah diubah.
- **Baris ringkasan & catatan (v1.0.6–1.0.7) — dikeluarkan otomatis HANYA bila tidak ambigu:** (a) XLSX: sel
  berisi rumus agregat (SUM/SUBTOTAL/AVERAGE/COUNT/MIN/MAX/AGGREGATE) atas baris lain, termasuk daftar sel
  `=SUM(C5,C9,C12)` dan `=C5+C9+C12`; (b) blok **ekor**
  tabel: baris berlabel Total/Jumlah/Grand Total/Rata-rata/Saldo Akhir… (label di sel teks pertama),
  catatan kaki (Catatan/NB/Sumber/Dicetak…, walau berisi angka), teks saja yang dipisah baris kosong;
  (c) **kepala**: judul laporan di atas header, "Saldo Awal" tepat di bawah header. Semua disebut dengan isinya.
  **Selain itu TIDAK dibuang** (kategori "Total"/"Rata-rata" di tengah, Subtotal di tengah, angka tanpa label
  yang = jumlah/rata-rata di atasnya, nilai polos tanpa rumus, "<Nama> Total", rincian Tunai/QRIS di bawah
  Total, subtotal/total terisi lengkap, subtotal pivot di atas kelompok) → tetap dihitung + PERINGATAN
  TEGAS + total alternatif; ikuti langkah 3. Pengaman umum ini
  **mengurangi**, bukan menghapus, risiko tata letak baru — karena itu cek sekilas di langkah 1 wajib.
  Rincian: `references/format-didukung.md`.
- **Aturan jumlah kolom CSV (v1.0.4–1.0.5):** setiap baris data wajib punya jumlah kolom yang **sama
  dengan judul kolom**. Boleh: sel kosong berlebih di ujung kanan, dan baris yang kekurangan sel
  **hanya di kolom paling kanan yang memang sering kosong** (mis. "Catatan") selama isi baris tidak
  bergeser → dianggap kosong + info. Selain itu → `GAGAL: Jumlah kolom tidak cocok di N baris data …`
  + nomor baris, isinya, dan kemungkinan penyebab (sel terlewat di tengah, koma di teks tanpa kutip,
  kutip nyasar, catatan di tengah tabel). Sampaikan ke pengguna dengan bahasa awam dan minta ia
  memperbaiki baris itu di Excel. `--paksa` hanya bila pengguna tetap ingin melihat hasil;
  "PERINGATAN TEGAS … MUNGKIN SALAH" wajib disampaikan.
- **CSV tanda kutip tak tertutup** sampai akhir file → selalu `GAGAL: CSV rusak ... baris N` (juga
  dengan `--paksa`). Kutip nyasar yang "tertutup" di baris lain dan kebetulan tetap cocok jumlah
  kolomnya → `GAGAL: CSV kemungkinan rusak … N baris data HILANG` (hanya pada kolom yang biasanya
  satu baris). Sel multi-baris yang sah (alamat "Jl. …, No. …⏎Kel. …, Kec. …", catatan "50%⏎sisa")
  terbaca biasa + info ringan; tidak perlu dipermasalahkan.
- **Tanpa traceback:** semua masalah input keluar dengan kode 2 dan pesan `GAGAL: ...` berbahasa awam.
