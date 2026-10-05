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
1. **Ringkasan angka** (satu-dua kalimat): berapa baris, berapa yang sudah diperbaiki per jenis (nomor HP, tanggal, harga, nama), berapa yang tidak bisa diperbaiki.
2. **Tabel contoh perbaikan** (5-8 baris: Sebelum -> Sesudah, jenisnya).
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
1. **Lihat datanya.** Buka beberapa baris pertama: judul kolom, pemisah, ada tidaknya kolom nomor urut. Bila pengguna cuma menempelkan data (di bawah ±40 baris), rapikan langsung dengan aturan di `references/aturan-pembersihan.md` dan beri tahu bahwa ini dikerjakan manual.
2. **Rapikan dengan script** `scripts/rapikan.py` (Python standar, tanpa instalasi tambahan):
   ```bash
   python3 <folder-skill-ini>/scripts/rapikan.py <file.csv>
   ```
   - Pemisah (`,` `;` tab), encoding Excel Windows, dan kolom dikenali otomatis. Bila salah, beri `--kolom-nama "Nama Pelanggan|Produk"`, `--kolom-hp "No HP"`, `--kolom-tanggal "Tgl"`, `--kolom-rupiah "Total"`, `--pemisah ";"`.
   - `--jenis daftar` bila 1 baris = 1 pelanggan (nomor HP yang sama ditandai); `--jenis transaksi` bila pelanggan wajar muncul berulang.
   - Hasil ditulis di folder `hasil-rapikan` di sebelah file asli: `<nama>-bersih.csv` dan `laporan.json`. File asli tidak disentuh.
   - Keluaran layar bertanda "UNTUK AGENT SAJA": baca angkanya, sampaikan dengan bahasa biasa.
3. **Baca `laporan.json`** untuk: `perbaikan` (jumlah per jenis), `contoh_perbaikan`, `kelompok_nama_mirip`, `duplikat`, `tidak_bisa_diperbaiki`, `tanggal_ambigu`, `peringatan`. Semua angka di balasan wajib dari sana, jangan dikira atau dijumlah sendiri.
4. **Sampaikan hasil** dengan format di bawah, termasuk setiap `peringatan` yang relevan.
5. **Terapkan keputusan pengguna** dengan menjalankan ulang (hasil sebelumnya ditimpa di folder `hasil-rapikan`, bukan file asli):
   - Gabung nama: `--gabung-kelompok 1,3` (nomor dari laporan), atau nama baku pilihan sendiri `--nama-baku "2=Muhammad Rizal Pratama"`. `--gabungkan-otomatis` (semua usulan) hanya bila pengguna jelas menyetujui semuanya.
   - Buang duplikat persis: `--buang-duplikat-persis` (baris yang dibuang disimpan di `dibuang-duplikat.csv`, tidak hilang).
   - Tanggal berformat bulan/hari (AS): `--urutan-tanggal mdy`.
   - Dibuka di Excel dan nomor HP berubah jadi `6,28E+11`: `--hp-untuk-excel`. Kolom kosong semua: `--buang-kolom-kosong`.
6. **Serahkan file** hanya bila diminta (lihat "Menyerahkan file").

Jika Python tidak tersedia atau script gagal: rapikan manual dengan `references/aturan-pembersihan.md`, hitung jumlahnya satu per satu, dan sebutkan bahwa hasil ini belum diverifikasi alat hitung.

## Format balasan
```
Selesai dirapikan: <N> baris. Diperbaiki: <a> nomor HP, <b> tanggal, <c> harga, <d> nama.
<k> sel tidak bisa diperbaiki (dibiarkan apa adanya, daftar di bawah).

Contoh perbaikan
| Isi | Sebelum | Sesudah |
|---|---|---|
| Nomor HP | +62 812-3450-0101 | 6281234500101 |
| Tanggal | 7 Okt 2026 | 2026-10-07 |
| Harga | 1,5jt | 1500000 |
| Nama | budi santoso | Budi Santoso |

Perlu keputusan Anda
1. Nama yang tampaknya orang/barang yang sama: "Budi Santoso" / "Bpk. Budi Santoso" / "Santoso Budi" (baris 2-5). Disatukan jadi "Budi Santoso"?
2. Baris persis kembar: 13 dan 14 (Hendra Gunawan, 12 Okt, Rp310.000). Sisakan satu?
3. Tanggal "05/10/2026" dan 7 lainnya bisa 5 Oktober atau 10 Mei; saya baca 5 Oktober. Benar?

Tidak bisa diperbaiki: baris 18 nomor HP "6.28123E+11" (Excel menghilangkan digitnya; perlu ekspor ulang kolom itu sebagai teks), ...

Mau file bersihnya? Balas "kirim file".
```
Aturan penyajian:
- Pilih **maksimal 3** butir keputusan (yang paling berdampak: nama mirip, duplikat, tanggal ambigu); sisanya ringkas dalam satu kalimat dan tawarkan lanjutannya.
- Tulis nomor baris sebagaimana di spreadsheet (judul = baris 1).
- Kata teknis (script, path, JSON, parsing, regex, LULUS, "saya menjalankan") **tidak** muncul di balasan. Katakan hasilnya, bukan prosesnya.
- Nama mirip **tidak pernah digabung** tanpa persetujuan. Tegaskan bahwa tidak ada data yang dihapus; yang diubah hanya format.
- Nomor yang tidak bisa dibaca dibiarkan seperti aslinya, jangan ditebak. Sebut alasannya dalam bahasa biasa.

## Aturan tiap jenis isi (ringkas)
- **Nomor HP:** semua menjadi `62` + nomor tanpa 0 depan (`0812-3450-0101`, `+62 812 3450 0101`, `812 3450 0101` -> `6281234500101`). Nomor ganda dalam satu sel: dipakai yang pertama dan dilaporkan. Telepon rumah (021...) diberi catatan bukan WhatsApp. Nomor luar negeri, terlalu pendek/panjang, atau berhuruf: dibiarkan dan dilaporkan.
- **Tanggal:** semua menjadi `YYYY-MM-DD` (bisa diurutkan dan dibaca semua aplikasi). Jam dibuang dan dilaporkan. Tanggal fiktif (31 Februari) dibiarkan dan dilaporkan. Format `05/10/2026` ambigu bila hari dan bulan sama-sama <= 12: dibaca hari/bulan, dihitung dan ditanyakan; bila ada bukti di kolom yang sama (mis. `10/13/2026`), urutan mengikuti bukti.
- **Rupiah:** menjadi bilangan bulat tanpa titik/"Rp" (`Rp 1.250.000,-` -> `1250000`, `150rb` -> `150000`, `1,5jt` -> `1500000`, "gratis" -> `0`). Sen dibulatkan ke rupiah terdekat dan dilaporkan; `1,500` (koma + 3 digit) dibaca 1.500 dan ditandai.
- **Nama/produk/kota:** spasi ganda dan huruf besar-kecil dirapikan (Title Case; `PT`, `CV`, `iPhone`, `5kg` dijaga). Singkatan dan sapaan (Muh./Muhammad, Bpk., Jogja/Yogyakarta) tidak diubah di data, hanya dipakai untuk mendeteksi kemiripan.
- **Duplikat:** "persis" = semua kolom sama setelah dirapikan (kolom nomor urut diabaikan). Tabel daftar: nomor HP sama ditandai. Tabel transaksi: pelanggan yang sama membeli berulang itu wajar, tidak ditandai. Kolom `_catatan` dan `_grup_duplikat` di file bersih menjelaskan tiap tanda.

## Mencatat supaya rapi (bila diminta saran)
Bila pengguna bertanya cara mencatat agar tidak berantakan lagi, beri 5 aturan singkat dari `references/tabel-rapi.md` (satu baris satu catatan, satu kolom satu jenis isi, tanpa sel gabungan, warna bukan data, tanggal & nomor HP satu format) beserta template kolom untuk usahanya.

## Menyerahkan file
- **Aplikasi desktop (Claude Code, Codex, Cursor):** sebutkan folder `hasil-rapikan` di sebelah file asli dan isi file bersihnya.
- **Chat Telegram/WhatsApp:** lampirkan file bersih bila kanal mendukung. Bila tidak bisa, jangan menyebut jalur file; untuk hasil kecil (<= 30 baris) tempel sebagai tabel, untuk yang besar tawarkan memecahnya.
- File bersih memuat kolom tambahan `_catatan` (apa yang diubah/ditandai), `_grup_duplikat`, dan `_kelebihan` bila ada. Beri tahu bahwa kolom itu boleh dihapus setelah semua keputusan selesai.

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
