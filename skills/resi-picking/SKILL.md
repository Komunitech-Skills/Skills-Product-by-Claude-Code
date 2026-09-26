---
name: resi-picking
description: Buat daftar ambil barang (picking list) per SKU/rak dan urutan kemas/tempel resi per kurir langsung dari file ekspor pesanan Shopee/Tokopedia/TikTok Shop (CSV), tanpa database/inventori. Pakai saat pengguna minta "buatkan picking list dari file pesanan ini", "urutan resi hari ini", "cocokkan barang dengan resi", packing list, urutan kemas, atau punya puluhan-ratusan pesanan yang harus disiapkan sebelum dikirim. Keywords: picking list, packing list, pick and pack, urutan resi, daftar ambil barang gudang.
---

# resi-picking

## Tujuan
Mengubah file ekspor pesanan marketplace (yang sudah diunduh pengguna sendiri dari Seller Center)
menjadi dua dokumen siap pakai untuk gudang: **daftar ambil barang** (total per SKU/varian, diurutkan
per rak bila ada) dan **urutan kemas/tempel resi** (dikelompokkan per kurir). Alat ini SEKALI JALAN -
tidak menyimpan status "sudah dikemas" antar-hari, tidak memotong stok, dan tidak butuh pendaftaran
SKU lebih dulu. Cocok untuk seller yang cuma mau picking list cepat setiap hari tanpa mengurus
inventori penuh.

## Kapan digunakan
- "Ini file pesanan Shopee hari ini, buatkan daftar ambil barang"
- "Urutan resi/packing hari ini per kurir dong"
- "Cocokkan barang pesanan sama resinya biar admin gudang gak bingung"
- Toko dengan puluhan sampai ratusan pesanan per hari dari Shopee, Tokopedia, atau TikTok Shop
- Punya file lokasi rak dan/atau file stok, mau daftar ambilnya diurutkan per rak dan dicek stoknya

## Kapan TIDAK digunakan
- **Sudah pakai (atau mau mulai pakai) skill `buku-stok`**: buku-stok punya perintah `picking` sendiri
  yang otomatis memotong stok, mengingat pesanan yang sudah pernah diimpor (anti dobel), dan menandai
  pesanan "sudah dikemas" antar-hari. Kalau pengguna sudah/mau punya database stok penuh, arahkan ke
  situ - jangan pakai resi-picking sebagai pengganti.
- **Merapikan/menggabungkan file PDF resi supaya hemat kertas saat mencetak** → skill `pdf-lokal`
  (resi-picking hanya menghasilkan DAFTAR barang & urutan, bukan mengolah file PDF resinya).
- **Menghitung omzet/laba dari pesanan** → `rekap-penjualan-csv` atau `laporan-keuangan-emkm`.
- **Menentukan harga jual** → `harga-jual-marketplace`.
- File yang diberikan bukan ekspor PESANAN (mis. laporan omzet, laporan iklan) → script akan menolak
  dengan jelas karena kolom wajib (No. pesanan, Jumlah) tidak ditemukan; sampaikan itu ke pengguna,
  jangan mengarang daftar.
- Tidak ada scraping/otomatis login ke Shopee/Tokopedia/TikTok Shop untuk mengambil pesanan - selalu
  minta pengguna mengekspor & mengunggah filenya sendiri dari Seller Center.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| File ekspor pesanan (CSV; kalau masih .xlsx, minta disimpan ulang sebagai CSV dari Excel/Google Sheets) | Ya | — (tanyakan) |
| File lokasi rak (CSV: kolom SKU + Lokasi) | Tidak | Daftar ambil diurutkan per SKU saja, tanpa kelompok rak |
| File stok untuk cross-check (CSV; bisa hasil `buku-stok laporan stok --csv`) | Tidak | Tidak ada peringatan "SKU tidak dikenal"/"stok kurang" |
| Urutan di dalam kelompok kurir (nomor resi / nomor pesanan) | Tidak | Nomor resi |

Jika file pesanan belum dikirim, tanyakan **sekali**: "Kirim file ekspor pesanan hari ini (CSV) ya -
kalau ada, file lokasi rak dan file stok juga boleh disertakan biar daftarnya lebih lengkap." Kalau
pengguna cuma punya file pesanan, tetap jalankan tanpa lokasi/stok dan sebutkan itu sebagai asumsi.

## Langkah kerja
1. Simpan file yang dikirim pengguna ke folder kerja (mis. folder yang sama dengan file pesanan).
2. Jalankan:
   ```bash
   python3 <folder-skill-ini>/scripts/resi.py "pesanan.csv" --json
   ```
   Tambahkan bila tersedia: `--lokasi "lokasi-rak.csv"` dan/atau `--stok "stok.csv"`. Windows: ganti
   `python3` dengan `python` atau `py`.
3. Baca JSON hasilnya:
   - `pemetaan_kolom` — **tunjukkan ke pengguna** kolom mana yang dipakai untuk apa (No. pesanan, SKU,
     Jumlah, dst.), supaya bisa dikoreksi kalau salah tebak. Ini bukan spesifikasi resmi marketplace
     (lihat catatan PERLU REVIEW di bawah), jadi konfirmasi singkat itu penting.
   - Kalau ada field wajib salah petakan, ulangi dengan `--kolom-no-pesanan "Nama Kolom"`,
     `--kolom-sku`, `--kolom-nama`, `--kolom-varian`, `--kolom-qty`, `--kolom-kurir`, `--kolom-resi`,
     `--kolom-catatan`, atau `--kolom-status` (isi `-` untuk sengaja mengabaikan kolom itu).
   - `peringatan` — sampaikan semuanya ke pengguna apa adanya (SKU tak dikenal, jumlah 0/negatif,
     baris duplikat, resi kosong, pesanan dilewati karena batal/retur/belum bayar, dst.).
   - `file_keluaran` — path file `daftar-ambil.md` dan `urutan-resi.md` yang sudah ditulis ke disk;
     tempelkan isinya ke pesan balasan (Markdown-nya langsung terbaca rapi di chat) dan sebutkan lokasi
     filenya untuk dicetak/dibagikan ke admin gudang.
4. Kalau pengguna minta versi HTML (untuk dibuka di browser lalu diprint) atau CSV (untuk Excel),
   jalankan ulang dengan tambahan `--html` dan/atau `--csv`.
5. Kalau gagal (`ok: false`), pesan `error` SUDAH menyebutkan kolom yang ada di file (`kolom_ada`) dan
   kolom yang sempat terdeteksi otomatis (`pemetaan_terdeteksi`, kalau ada) — jangan cuma melaporkan
   "gagal" ke pengguna, langsung **tawarkan** perintah `--kolom-...` yang sesuai dari pesan error itu
   (isi nilainya dengan nama kolom PERSIS dari `kolom_ada`) dan tanyakan konfirmasi kolom mana yang
   dimaksud kalau ada dua yang mirip. Jangan membuat daftar dari data yang tidak lengkap.

## Format Output
Dua dokumen Markdown (isinya juga cocok ditempel langsung ke chat/WA):

```
# Daftar Ambil Barang (Picking)
...
**Total: 4 pesanan aktif, 4 jenis barang, 12 pcs.**

## Pesanan dengan catatan khusus (baca dulu sebelum packing)
- Pesanan #240901A1: "Tolong dibungkus rapi ya kak"

## Ambil di rak
### A1
- [ ] **KAOS-HT-M** Kaos Polos Pria - Hitam - M x 3 pcs (2 pesanan)
...
## Peringatan
- ...
```

```
# Urutan Kemas / Tempel Resi
...
## JNE (2 pesanan)
1. [ ] Pesanan #240901A1 | Resi JX00112233 | KAOS-HT-M x2; TOPI-01 x1 | CATATAN: "..."
...
```

## Contoh
**Input pengguna:** "Ini file pesanan Shopee hari ini (pesanan-shopee.csv), sama file lokasi rak
(lokasi-rak.csv) sama file stok dari buku-stok (stok.csv). Buatkan picking list dan urutan resinya."

**Perintah:**
```bash
python3 scripts/resi.py pesanan-shopee.csv --lokasi lokasi-rak.csv --stok stok.csv --json
```

**Output (ringkas):** lihat contoh lengkap di `examples/01-picking-dasar/` (input & hasil nyata dari
uji, termasuk peringatan SKU tak dikenal dan stok menipis).

## Batasan & penanganan error
- Hanya membaca **CSV**. File `.xlsx`/`.xls` asli ditolak dengan pesan jelas: minta pengguna Save As
  / Simpan sebagai CSV dulu dari Excel/Google Sheets.
- Baris yang dilewati selalu dilaporkan dengan alasan & nomor baris: nomor pesanan rusak (mis.
  `2,4E+17` akibat dibuka di Excel), tanpa nomor pesanan, jumlah tidak terbaca, jumlah 0/negatif,
  tanpa identitas barang (SKU & nama sama-sama kosong), baris duplikat persis, dan baris
  ringkasan/"Total" di ekspor (diabaikan, tidak dianggap item pesanan lain).
- Pesanan berstatus batal/dibatalkan/retur/refund/belum bayar (kalau kolom status terdeteksi)
  dikeluarkan dari daftar ambil & urutan resi, tapi tetap dihitung & dilaporkan jumlahnya.
- Kalau kolom status **tidak** terdeteksi sama sekali, semua baris dianggap perlu dikemas — beri tahu
  pengguna dan sarankan mengekspor pesanan berstatus "Perlu Dikirim" saja bila platformnya bisa
  memfilter itu, supaya pesanan yang sudah dikirim tidak ikut muncul lagi.
- "SKU tidak dikenal" dan "stok kemungkinan kurang" hanya muncul kalau `--stok` diberikan; tanpa itu,
  script tidak tahu SKU mana yang belum terdaftar.
- **PERLU REVIEW:** nama kolom ekspor Seller Center berubah-ubah antar waktu dan negara. Kata kunci
  deteksi di `scripts/resi.py` (variabel `SINONIM_PESANAN`) disusun dari panduan/forum seller, dari
  skill `buku-stok`, dan (untuk TikTok Shop) dari halaman bantuan resmi - rincian mana yang
  **terverifikasi** vs **best-effort** (dugaan, belum dicocokkan ke ekspor asli) ada di
  `references/sumber-kolom-marketplace.md`, termasuk URL sumber + tanggal cek. Karena itu langkah 3
  di atas WAJIB menunjukkan pemetaan kolom ke pengguna sebelum daftar dipakai. Sejak v1.0.1, deteksi
  memakai pencocokan **kata/token utuh** (bukan potongan huruf) yang tidak pandang huruf besar/kecil,
  diakritik, underscore, atau spasi, sehingga sinonim pendek seperti "kurir"/"invoice"/"sku" ikut
  terdeteksi di dalam nama kolom gabungan (mis. "Nama Kurir", "No. Invoice"). Kalau pemetaan tetap
  salah/kurang, error dan hasil sukses SAMA-SAMA menyebutkan kolom yang ada di file dan flag
  `--kolom-...` yang persis untuk membetulkan secara manual - tidak perlu menunggu pembaruan skill.
- Tidak ada scraping, login browser, atau API resmi marketplace di skill ini. Input murni dari file
  yang diunduh pengguna sendiri.
- Bukan alat inventori: tidak memotong stok, tidak mengingat "sudah dikemas" dari hari sebelumnya. Untuk
  itu pakai skill `buku-stok`.
