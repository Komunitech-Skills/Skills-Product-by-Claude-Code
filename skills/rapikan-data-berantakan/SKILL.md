---
name: rapikan-data-berantakan
description: Merapikan daftar pelanggan, produk, atau penjualan yang berantakan dari ekspor WhatsApp, Shopee, Tokopedia, kasir, atau Excel/CSV. Menyeragamkan ejaan nama (huruf besar-kecil, spasi, singkatan), nomor HP campur 08xx/62xx/+62 menjadi satu format 628xxxxxxxxxx, tanggal campur (5 Okt 2026, 05/10/26) menjadi 2026-10-05, dan harga "Rp 1.500.000"/"150rb"/"1,5jt" menjadi angka; menandai duplikat dan nama mirip untuk diputuskan pengguna tanpa menghapus data diam-diam. Gunakan saat pengguna minta rapikan data, bersihkan data pelanggan, cari duplikat, seragamkan nomor HP, atau menyebut data kacau (clean messy data, data cleaning, dedupe, normalize phone numbers).
---

# Rapikan Data Berantakan

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`). Jangan membuka file selain yang diberikan pengguna dan isi folder skill ini. Script ada di `scripts/` di folder yang sama dengan SKILL.md ini; jangan mencarinya ke seluruh disk. Di Windows, ganti `python3` dengan `python` atau `py`. Jangan menimpa file asli pengguna.

## Tujuan
Mengubah tabel yang kacau menjadi tabel rapi siap pakai (satu baris = satu catatan, satu kolom = satu jenis isi), dengan setiap perubahan tercatat dan setiap keputusan yang berisiko (menggabung nama, membuang duplikat) tetap di tangan pengguna.

## Aturan utama: kerjakan dulu, tanya di akhir
Jika pengguna sudah memberi data (file CSV, ekspor, atau tempelan), JANGAN membalas hanya dengan pertanyaan. Rapikan dulu pakai pengaturan wajar, lalu dalam **satu balasan** berikan berurutan:
1. **Blok angka tetap**: salin APA ADANYA dari keluaran alat (lihat "Aturan angka & nomor baris"), dalam format daftar. Itu sudah memuat jumlah baris, nomor HP/tanggal/nominal yang diperbaiki, telepon rumah, sel dua nomor, baris kembar, nomor sama nama beda, dan sel yang tidak bisa diperbaiki beserta nomor barisnya.
2. **Tabel contoh perbaikan** (5-8 baris: Sebelum -> Sesudah, jenisnya; ambil dari `contoh_perbaikan` di laporan).
3. **Yang perlu keputusan Anda** (daftar bernomor, maksimal 3 butir pertanyaan; lihat "Format balasan").
4. **Asumsi** yang dipakai (mis. "tanggal 05/10/2026 saya baca 5 Oktober").
5. File bersih: tawarkan "balas *kirim file* kalau mau file bersihnya". Jangan menyebut lokasi file atau cara kerjanya kecuali ditanya.

Tanpa data sama sekali: tanyakan sekali (maks. 3 pertanyaan): file/tempelan datanya mana, kolom apa saja, dan untuk apa dipakai (promo WA, laporan, impor ke aplikasi kasir).

## Kapan digunakan
- Ekspor kontak/pelanggan dari WhatsApp, Shopee, Tokopedia, kasir, atau Excel yang nama dan nomornya tidak seragam.
- Sebelum rekap penjualan, kirim promo (ke yang sudah setuju), atau impor data ke aplikasi lain.
- "Ada pelanggan dobel nggak ya?", "tolong seragamkan nomor HP", "tanggalnya campur-campur".

## Kapan TIDAK digunakan
- **Menggabung dengan data dari sumber lain, melengkapi nomor/alamat dari internet, atau mengambil daftar orang dari situs/aplikasi (scraping):** tolak dengan sopan. Skill ini hanya merapikan data yang sudah pengguna punya sendiri. Jelaskan singkat: data orang tidak boleh dikumpulkan atau digabung tanpa dasar yang sah (UU PDP No. 27/2022).
- Analisis penjualan (omzet, produk terlaris) -> pakai skill `rekap-penjualan-csv` setelah data dirapikan.
- Rumus/pivot/grafik Excel -> pakai skill `analisis-excel`.
- File `.xlsx` langsung: minta simpan sebagai CSV dulu (Excel: *File > Save As > CSV UTF-8*; Google Sheets: *File > Download > CSV*).
- Menebak atau mengisi data yang kosong (nomor HP yang hilang, nama yang tidak ada): tidak dilakukan.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| File CSV/TSV atau tempelan data | Ya | - (tanyakan) |
| Kolom nama, HP, tanggal, rupiah | Tidak | Dikenali otomatis dari judul kolom dan isinya; sebutkan hasilnya |
| Jenis tabel: daftar (1 baris = 1 orang/produk) atau transaksi | Tidak | Otomatis: ada kolom tanggal/harga = transaksi |
| Urutan tanggal ambigu (05/10: 5 Okt atau 10 Mei) | Tidak | Hari/bulan (cara Indonesia); tanya bila ada yang ambigu |

## Langkah kerja
1. **Lihat datanya.** Buka beberapa baris pertama: judul kolom, pemisah, ada tidaknya kolom nomor urut. Bila pengguna cuma menempelkan data, simpan dulu sebagai file CSV sementara di folder kerja (judul = baris 1, nomor baris mengikuti urutan tempelan) lalu jalankan alat yang sama; jangan menghitung manual bila Python tersedia.
2. **Rapikan dengan script** `scripts/rapikan.py` (Python standar, tanpa instalasi tambahan):
   ```bash
   python3 <folder-skill-ini>/scripts/rapikan.py <file.csv>
   ```
   - Pemisah (`,` `;` tab), encoding Excel Windows, dan kolom dikenali otomatis. Bila salah, beri `--kolom-nama "Nama Pelanggan|Produk"`, `--kolom-hp "No HP"`, `--kolom-tanggal "Tgl"`, `--kolom-rupiah "Total"`, `--pemisah ";"`.
   - `--jenis daftar` bila 1 baris = 1 pelanggan (nomor HP yang sama ditandai); `--jenis transaksi` bila pelanggan wajar muncul berulang.
   - Hasil ditulis di folder `hasil-rapikan` di sebelah file asli: `<nama>-bersih.csv` dan `laporan.json`. File asli tidak disentuh.
   - Keluaran layar diawali **BLOK ANGKA TETAP** (siap salin ke balasan), lalu bagian "UNTUK AGENT SAJA" (rincian; sampaikan dengan bahasa biasa). Bila keluaran layar terpotong atau tidak terbaca, ambil blok yang sama dari `blok_angka_tetap` di `laporan.json`.
3. **Baca `laporan.json`** untuk: `blok_angka_tetap`, `perbaikan`, `contoh_perbaikan`, `kelompok_nama_mirip`, `duplikat`, `telepon_rumah`, `hp_ganda`, `tidak_bisa_diperbaiki`, `tanggal_ambigu`, `peringatan`. Setiap butirnya memuat `baris` (nomor baris asli di file sumber) dan `isi_asli` (isi sel sebelum diubah).
4. **Sampaikan hasil** dengan format di bawah, termasuk setiap `peringatan` yang relevan.
5. **Terapkan keputusan pengguna** dengan menjalankan ulang (hasil sebelumnya ditimpa di folder `hasil-rapikan`, bukan file asli):
   - Gabung nama: `--gabung-kelompok 1,3` (nomor dari laporan), atau nama baku pilihan sendiri `--nama-baku "2=Muhammad Rizal Pratama"`. `--gabungkan-otomatis` (semua usulan) hanya bila pengguna jelas menyetujui semuanya.
   - Buang duplikat persis: `--buang-duplikat-persis` (baris yang dibuang disimpan di `dibuang-duplikat.csv`, tidak hilang).
   - Tanggal berformat bulan/hari (AS): `--urutan-tanggal mdy`.
   - Dibuka di Excel dan nomor HP berubah jadi `6,28E+11`: `--hp-untuk-excel`. Kolom kosong semua: `--buang-kolom-kosong`.
6. **Serahkan file** hanya bila diminta (lihat "Menyerahkan file").

Jika Python tidak tersedia atau script gagal: rapikan manual dengan `references/aturan-pembersihan.md`, hitung jumlah dan nomor baris satu per satu (telepon rumah tetap tidak masuk kolom HP), dan sebutkan bahwa hasil ini belum diverifikasi alat hitung.

## Aturan angka & nomor baris (wajib, berlaku di semua kanal)
- **Angka dan nomor baris di balasan HANYA disalin dari keluaran alat/laporan**, tidak dihitung, dikira, atau dilihat sekilas sendiri. Kolom "No" di file BUKAN nomor baris (baris spreadsheet = "No" + 1 karena judul = baris 1); pakai nomor `baris` dari laporan.
- Blok angka tetap (baris-barisnya, tanpa baris judul bertanda `===`) disalin **utuh dan berurutan** sebagai daftar (butir dan sub-butir apa adanya), juga di chat Telegram/WhatsApp. Jangan merangkum jadi satu kalimat, jangan menghilangkan butir (terutama telepon rumah, sel dua nomor, sel tidak bisa diperbaiki), jangan mengubah angka. Kata sendiri hanya boleh di tabel contoh, pertanyaan keputusan, dan asumsi.
- Daftar baris kembar, nomor sama nama beda, dan nama mirip juga hanya dari blok/laporan. Jangan membedakan "kembar" dan "mirip" dengan pandangan sekilas: "kembar persis" = butir baris kembar; "nomor sama nama beda" = butir sendiri.
- Berlaku juga **saat sebagian permintaan ditolak** (mis. diminta menggabung data grup WA atau mencari nomor dari Instagram): tolak bagian itu, tetapi pengecekan duplikat/rapikan pada file yang pengguna punya tetap dijalankan dengan alat, dan daftarnya disalin dari blok.
- Nomor di dalam sel (hasil HP, "dipakai sebagai HP") disalin dari blok/laporan, bukan diketik ulang dari ingatan.

## Format balasan
```
<salin blok angka tetap dari alat, apa adanya>

Contoh perbaikan
| Isi | Sebelum | Sesudah |
|---|---|---|
| Nomor HP | +62 812-3450-0101 | 6281234500101 |
| Tanggal | 7 Okt 2026 | 2026-10-07 |
| Harga | 1,5jt | 1500000 |
| Nama | budi santoso | Budi Santoso |

Perlu keputusan Anda
1. Nama yang tampaknya orang/barang yang sama: "Budi Santoso" / "Bpk. Budi Santoso" / "Santoso Budi" (baris dari blok). Disatukan jadi "Budi Santoso"?
2. Baris persis kembar: baris 13 & 14 (dari blok). Sisakan satu?
3. Telepon rumah di baris 31 tidak ikut kolom HP. Mau dikosongkan saja, atau dicari nomor WA-nya ke pelanggan?

Asumsi: tanggal "05/10/2026" dibaca 5 Oktober (hari/bulan); harga dibulatkan ke rupiah terdekat.

Mau file bersihnya? Balas "kirim file".
```
Aturan penyajian:
- Pilih **maksimal 3** butir keputusan, urutan prioritas: (1) nama mirip / nomor sama nama beda, (2) baris kembar persis, (3) telepon rumah dan sel dua nomor bila data dipakai untuk WhatsApp/promo. Tanggal ambigu cukup di "Asumsi" kecuali ada bukti kolom bercampur (peringatan alat); sisanya ringkas dalam satu kalimat dan tawarkan lanjutannya.
- Nomor baris sebagaimana di spreadsheet (judul = baris 1), langsung dari blok/laporan.
- Kata teknis (script, path, JSON, parsing, regex, LULUS, "saya menjalankan") **tidak** muncul di balasan. Katakan hasilnya, bukan prosesnya.
- Nama mirip **tidak pernah digabung** tanpa persetujuan. Tegaskan bahwa tidak ada data yang dihapus; yang diubah hanya format.
- Nomor yang tidak bisa dibaca dibiarkan seperti aslinya, jangan ditebak. Sebut alasannya dalam bahasa biasa.

## Aturan tiap jenis isi (ringkas)
- **Nomor HP:** semua menjadi `62` + nomor tanpa 0 depan (`0812-3450-0101`, `+62 812 3450 0101`, `812 3450 0101` -> `6281234500101`). Nomor ganda dalam satu sel: dipisah; nomor **seluler** pertama jadi HP, nomor lain dicatat di `_catatan` (tidak dibuang). **Telepon rumah/kantor** (kode area 021, 022, 0274, ... dan 0800) **tidak pernah masuk kolom HP**: dipindah ke kolom `_telepon_rumah` (kolom HP dikosongkan bila tidak ada nomor seluler lain), ditandai "bukan WhatsApp", dan **jangan disebut sebagai nomor WA/siap kirim promo**. Nomor luar negeri, terlalu pendek/panjang, atau berhuruf: dibiarkan dan dilaporkan.
- **Tanggal:** semua menjadi `YYYY-MM-DD` (bisa diurutkan dan dibaca semua aplikasi). Jam dibuang dan dilaporkan. Tanggal fiktif (31 Februari) dibiarkan dan dilaporkan. Format `05/10/2026` ambigu bila hari dan bulan sama-sama <= 12: dibaca hari/bulan, dihitung dan ditanyakan; bila ada bukti di kolom yang sama (mis. `10/13/2026`), urutan mengikuti bukti.
- **Rupiah:** menjadi bilangan bulat tanpa titik/"Rp" (`Rp 1.250.000,-` -> `1250000`, `150rb` -> `150000`, `1,5jt` -> `1500000`, "gratis" -> `0`). Sen dibulatkan ke rupiah terdekat dan dilaporkan; `1,500` (koma + 3 digit) dibaca 1.500 dan ditandai.
- **Nama/produk/kota:** spasi ganda dan huruf besar-kecil dirapikan (Title Case; `PT`, `CV`, `iPhone`, `5kg` dijaga). Singkatan dan sapaan (Muh./Muhammad, Bpk., Jogja/Yogyakarta) tidak diubah di data, hanya dipakai untuk mendeteksi kemiripan.
- **Duplikat:** "persis" = semua kolom sama setelah dirapikan (kolom nomor urut diabaikan). Tabel daftar: nomor HP sama ditandai. Tabel transaksi: pelanggan yang sama membeli berulang itu wajar, tidak ditandai. Kolom `_catatan` dan `_grup_duplikat` di file bersih menjelaskan tiap tanda.

## Mencatat supaya rapi (bila diminta saran)
Bila pengguna bertanya cara mencatat agar tidak berantakan lagi, beri 5 aturan singkat dari `references/tabel-rapi.md` (satu baris satu catatan, satu kolom satu jenis isi, tanpa sel gabungan, warna bukan data, tanggal & nomor HP satu format) beserta template kolom untuk usahanya.

## Menyerahkan file
- **Aplikasi desktop (Claude Code, Codex, Cursor):** sebutkan folder `hasil-rapikan` di sebelah file asli dan isi file bersihnya.
- **Chat Telegram/WhatsApp:** lampirkan file bersih bila kanal mendukung. Bila tidak bisa, jangan menyebut jalur file; untuk hasil kecil (<= 30 baris) tempel sebagai tabel, untuk yang besar tawarkan memecahnya.
- File bersih memuat kolom tambahan `_catatan` (apa yang diubah/ditandai), `_telepon_rumah`, `_grup_duplikat`, dan `_kelebihan` bila ada. Beri tahu bahwa kolom itu boleh dihapus setelah semua keputusan selesai.

## Privasi data pelanggan (wajib)
- Data pelanggan diproses di komputer pengguna dan **tidak dikirim ke layanan atau alat lain**. Jangan mengunggah, meneruskan, atau menyalinnya ke tempat lain tanpa diminta jelas.
- Nama dan nomor adalah data pribadi (UU PDP No. 27/2022). Bila hasilnya akan dibagikan ke grup tim, tawarkan versi tersamar (nomor tinggal 4 digit terakhir) atau angka agregat saja.
- Merapikan data **bukan** izin menghubungi: nomor di daftar yang sudah bersih tidak otomatis boleh dikirimi promo. Hanya pelanggan yang setuju (opt-in); tanpa broadcast/blast.
- Jangan menyimpan isi data di memori/catatan agent; file hasil hanya di folder kerja pengguna.

## Batasan & penanganan error
- Tabel dengan baris judul ganda di atas, sel gabungan, atau beberapa tabel dalam satu lembar: minta pengguna memisahkan dulu, atau jelaskan bagian yang tidak terbaca.
- Kolom tidak dikenali otomatis: sebutkan kolom yang terdeteksi, minta koreksi sekali saja.
- Nama mirip itu **tebakan**: "Ani" dan "Anis" bisa dua orang. Keputusan selalu di pengguna.
- Ribuan nilai nama unik dalam satu kolom: pencarian nama mirip dibatasi; sebutkan bahwa hasil kelompok nama belum menyeluruh.
- Jangan menjanjikan "100% bersih": katakan apa yang diperbaiki, apa yang ditandai, dan apa yang dibiarkan.
- Pembulatan rupiah: setengah rupiah ke atas (sesuai standar library Komunitech); bukan dokumen pajak, belum dicocokkan dengan Coretax.
