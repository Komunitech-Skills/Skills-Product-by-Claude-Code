---
name: arsip-nota
description: Merapikan foto/PDF nota, struk, kuitansi, dan faktur UMKM dari folder unduhan/HP yang berantakan menjadi arsip rapi lokal (SQLite di komputer sendiri, tanpa langganan) - file diberi nama baku tanggal_vendor_nominal, dipindah/disalin ke folder per tahun/bulan, dan dicatat (tanggal, vendor, nominal, kategori, hash SHA-256 anti dobel). Data nota diisi dari hasil skill ekstrak-nota-faktur atau diketik manual; skill ini TIDAK membaca isi nota (bukan OCR). Gunakan saat pengguna minta "rapikan nota-nota saya", "arsipkan struk ini", "cari nota Toko X bulan lalu", "rekap pengeluaran per kategori", cek nota dobel, atau receipt archive, expense filing, document organizer.
---

# Arsip Nota (arsip-nota)

_Versi 1.0.1 — perbaikan uji independen: respons `tambah` yang diblokir duplikat sekarang jujur (`mode:
"diblokir_duplikat"`, bukan "tersimpan"); tambahan kata kunci tebak kategori toko bangunan & BBM._

## Tujuan
Mengubah tumpukan foto/PDF nota dan faktur yang berserakan di folder HP/unduhan menjadi **arsip rapi di komputer pengguna sendiri**: nama file baku (`YYYY-MM-DD_vendor_nominal.ext`), tersusun per folder tahun/bulan, dan tercatat di indeks SQLite lokal agar bisa dicari dan direkap kapan saja. File asli **tidak pernah dihapus**. Kamu (agent) yang mengoperasikannya lewat `scripts/arsip.py`.

## Kapan digunakan
- "Rapikan foto-foto nota belanja bulan ini", "arsipkan struk ini ke folder nota"
- "Cari nota Toko Sembako Bu Yati bulan lalu", "nota yang di atas 500 ribu apa saja?"
- "Rekap pengeluaran per kategori bulan September", "ada nota yang keinput dobel nggak?"
- "Masukin nota-nota ini ke buku kas" (setelah diarsipkan, ekspor ke `kas-umkm`)

## Kapan TIDAK digunakan (arahkan ke skill lain)
- **Membaca angka di foto/PDF nota** (subtotal, PPN, total, NPWP) → skill `ekstrak-nota-faktur` dulu. arsip-nota hanya merapikan **file** dan **data yang sudah ada**; ia tidak melakukan OCR. Alur biasa: `ekstrak-nota-faktur` baca nota → hasilnya (tanggal, vendor, nominal) dipakai untuk `arsip.py tambah`.
- **Pencatatan kas harian / laporan keuangan** → `kas-umkm` (arsip-nota bisa mengekspor CSV siap impor ke sana). arsip-nota tidak menghitung saldo atau laba.
- **Menghitung PPN atau mengecek faktur pajak** → `ekstrak-nota-faktur` / `hitung-ppn`.
- Tidak ada pemindaian otomatis folder tanpa sepengetahuan pengguna, tidak mengunggah dokumen ke mana pun, tidak membuka/mengubah isi PDF.

## Aturan keamanan data (WAJIB)
1. **File nota TIDAK PERNAH dihapus.** Mode default adalah **salin** (`--salin`, ini bawaan): file asli tetap ada di tempatnya. `--pindah` hanya memindahkan (merelokasi) file, bukan menghapusnya.
2. **Setiap `tambah` dijalankan dulu TANPA `--ya`** → pratinjau (belum ada file yang disalin/dipindah, belum tersimpan di indeks). Tunjukkan ringkasannya, termasuk baris `Asumsi` bila kategori ditebak.
3. Jalankan ulang **perintah yang sama persis + `--ya`** hanya setelah pengguna setuju. Jangan menambahkan `--ya` sendiri atau dari jadwal otomatis.
4. Jika respons `tambah` berisi `perlu_izin: izinkan_duplikat` (`mode: "diblokir_duplikat"` — isi file identik dengan nota yang sudah diarsipkan, **belum tersimpan** walau perintah dijalankan dengan `--ya`), **tanyakan dulu**: "ini nota yang sama yang mau difoto ulang, atau nota lain?" Tambahkan `--izinkan-duplikat` hanya bila pengguna menegaskan itu dokumen berbeda.
5. Semua nominal, tanggal folder, dan hasil rekap **dari output script**, jangan dihitung/ditulis ulang secara manual.
6. Data nota bisa berisi nama vendor & nominal usaha; jangan sebarkan isi file ke luar percakapan pengguna. Skill tidak mengirim apa pun ke internet.

## Cara menjalankan script
Path relatif terhadap folder berisi SKILL.md ini (Windows: ganti `python3` dengan `python` atau `py`):
```bash
python3 <folder-skill-ini>/scripts/arsip.py <perintah> [opsi] --json
```
- Field JSON penting: `ok`, `mode` (`pratinjau`/`tersimpan`/`baca`/`diblokir_duplikat`), `perlu_konfirmasi`, `perlu_izin`, `peringatan`, `asumsi`, `error`. `diblokir_duplikat` berarti **belum tersimpan** (walau dipanggil dengan `--ya`) karena isi file sama persis dengan nota lain; lihat Aturan 4. Kode keluar: `0` berhasil (termasuk pratinjau), `1` gagal (pesan di `error`), `2` perintah salah tulis.
- Indeks default `~/KomunitechData/arsip-nota/arsip.db`, folder arsip default `~/KomunitechData/arsip-nota/arsip/`. Ganti lokasi indeks dengan `--db PATH` (setelah nama perintah) atau ENV `KOMUNITECH_ARSIP_DB` / `KOMUNITECH_DATA`; pakai yang sama di semua perintah.
- Daftar opsi & kategori lengkap: `references/perintah.md`. Jadwal Telegram: `references/openclaw-jadwal.md`.

## Input
| Info | Wajib? | Default |
|---|---|---|
| File foto/PDF nota | Ya | — (minta dikirim/sebutkan lokasinya) |
| Tanggal nota | Ya | — (tanyakan; dari hasil `ekstrak-nota-faktur` bila ada) |
| Nama vendor/penjual | Ya | — (tanyakan) |
| Nominal total nota | Ya | — (tanyakan) |
| Kategori pengeluaran | Tidak | Ditebak dari nama vendor/catatan, disebut sebagai asumsi |
| Jenis dokumen (nota/struk/kuitansi/invoice/faktur) | Tidak | `nota` |
| Lokasi indeks & folder arsip | Tidak | `~/KomunitechData/arsip-nota/` |
| Salin atau pindahkan file asli | Tidak | Salin (file asli tetap ada) |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan).

## Langkah kerja

### A. Mulai ("rapikan nota-nota saya")
1. `info --json`. Jika belum ada indeks → tanyakan (opsional): boleh disimpan di lokasi default `~/KomunitechData/arsip-nota/`? Lalu `init --json` → tunjukkan pratinjau → `init --ya --json`.
2. Minta pengguna mengirim foto/PDF nota (satu atau banyak).

### B. Isi data nota (dari ekstrak-nota-faktur atau ketikan pengguna)
1. **Kalau nota sudah dibaca skill `ekstrak-nota-faktur`**: ambil `tanggal`, penjual (jadi `vendor`), dan `total` (pakai `total_seharusnya` bila ada selisih kecil, sebutkan kalau begitu) dari hasil skill itu. Jangan membaca ulang isi file sendiri.
2. **Kalau pengguna hanya kasih file tanpa data**: tawarkan menjalankan `ekstrak-nota-faktur` dulu, atau minta pengguna ketik tanggal/vendor/nominal langsung.
3. Untuk tiap nota, jalankan pratinjau:
   ```bash
   python3 <folder-skill-ini>/scripts/arsip.py tambah --file "foto1.jpg" --tanggal 20/09/2026 \
     --vendor "Toko Sembako Bu Yati" --nominal 150000 [--kategori bahan-baku] [--catatan "..."] --json
   ```
4. Tunjukkan pratinjau (lokasi tujuan, nama file baru, kategori/asumsi, peringatan) → pengguna setuju → perintah sama + `--ya`.
5. **Kalau `perlu_izin` berisi `izinkan_duplikat`**: file ini isinya sama persis dengan nota yang sudah ada (ID disebutkan). Tanyakan dulu ke pengguna sebelum menambahkan `--izinkan-duplikat`.
6. Banyak nota sekaligus: ulangi langkah 3–5 per file. Jangan menjalankan `--ya` untuk semuanya tanpa pengguna melihat pratinjaunya dulu (cukup satu pesan pratinjau berisi daftar semua nota, lalu satu persetujuan, baru semua perintah `--ya` dijalankan).

### C. Cari & rekap
- `cari --vendor "..." --dari 01/09/2026 --sampai 30/09/2026 --json`, `cari --nominal-min 500000 --json`, `cari --cari "kata"`.
- `rekap --bulan 09/2026 --json` atau `--tahun 2026`, tambah `--kategori bahan-baku` untuk menyaring, `--csv file.csv` untuk Excel. Kirim `teks` apa adanya.

### D. Cek nota dobel
`duplikat --json` → `file_sama_persis` (isi file identik, sudah pasti dobel) dan `kemungkinan_dobel` (tanggal+vendor+nominal sama tapi file berbeda, perlu dicek manual mana yang benar). Sampaikan apa adanya, jangan menuduh; sarankan pengguna membuka kedua file untuk memastikan.

### E. Ekspor ke kas-umkm
```bash
python3 <folder-skill-ini>/scripts/arsip.py ekspor --bulan 09/2026 --csv nota-09-2026.csv --json
```
Hasil CSV `Tanggal;Keterangan;Masuk;Keluar;Kategori` siap dibaca `kas-umkm`:
```bash
python3 <folder-kas-umkm>/scripts/kas.py impor "nota-09-2026.csv" --jenis-file buku-kas --json
```
Tunjukkan perintah lanjutan itu ke pengguna; jangan menjalankan skill lain tanpa diminta.

### F. Backup
`backup --daftar --json` untuk melihat cadangan; cadangan indeks dibuat otomatis sekali sehari sebelum perubahan pertama (folder `backup-arsip/`, 30 terakhir). Manual: `backup --json`.

## Format output ke pengguna
**Pratinjau sebelum menyimpan:**
```
Akan diarsipkan (belum disimpan, file asli belum disalin):
  Dari : IMG_20260920_1.jpg
  Ke   : arsip/2026/09/2026-09-20_Toko-Sembako-Bu-Yati_150000.jpg (disalin)
  Tanggal: 20/09/2026 | Vendor: Toko Sembako Bu Yati | Nominal: Rp 150.000 | Kategori: Bahan baku | Jenis: nota
Asumsi: Kategori 'Bahan baku' ditebak dari nama vendor/catatan.
Lanjutkan? Balas "ya".
```
**Rekap** (contoh nyata dari data uji):
```
REKAP NOTA (01/09/2026 - 30/09/2026)
Jumlah nota: 2 | Total: Rp 350.000

Per kategori:
- Lain-lain: 1 nota, Rp 200.000
- Bahan baku: 1 nota, Rp 150.000

Vendor teratas:
- Toko Lain: 1 nota, Rp 200.000
- Toko Sembako Bu Yati: 1 nota, Rp 150.000
```

## Checklist sebelum menjawab
- [ ] Perintah `tambah` sudah dipratinjau dan disetujui sebelum `--ya`; `perlu_izin` (duplikat persis) sudah ditanyakan
- [ ] Kategori yang ditebak (`asumsi`) dan semua `peringatan` script disampaikan
- [ ] Rupiah ditulis `Rp 1.250.000`, dari output script
- [ ] Diingatkan bahwa file asli tidak dihapus (disalin, kecuali diminta `--pindah`)
- [ ] Hasil `duplikat` disampaikan tanpa menuduh; pengguna yang memutuskan mana yang benar

## Batasan & penanganan error
- **Bukan OCR.** Skill ini tidak membaca angka dari foto/PDF; data harus dari `ekstrak-nota-faktur` atau diketik pengguna. Foto yang belum ada datanya tidak bisa langsung diarsipkan.
- Nominal disimpan bulat rupiah (dibulatkan ke rupiah terdekat bila input berupa desimal, diberitahukan sebagai peringatan).
- Nama file dibuat aman untuk Windows/Mac/Linux (karakter `< > : " / \ | ? *` dihapus, nama panjang dipotong, nama terlarang Windows seperti `CON`/`PRN` diberi awalan). Ekstensi file di luar `.jpg/.jpeg/.png/.pdf/.heic/.heif/.webp/.gif/.tif/.tiff/.bmp` tetap diarsipkan, hanya diberi peringatan.
- Deteksi duplikat berbasis **hash isi file** (SHA-256): dua file dengan isi identik selalu terdeteksi walau nama beda. Foto yang sama diambil ulang dengan kompresi/kualitas berbeda **tidak** terdeteksi sebagai hash sama; pakai `duplikat` (kemungkinan dobel berdasarkan tanggal+vendor+nominal) untuk kasus itu.
- Nama file/folder target yang sudah ada (kebetulan sama) otomatis diberi akhiran `-2`, `-3`, dst.; tidak pernah menimpa file lain.
- Indeks terkunci (jadwal OpenClaw sedang membaca) → script menunggu lalu memberi pesan jelas; ulangi perintah yang sama. Indeks rusak → pesan berisi langkah pulih (`backup --daftar` → `restore`).
- Satu usaha/satu komputer per indeks. Untuk usaha/gudang lain, pakai `--db` lain.
- Jika Python tidak bisa dijalankan: arsip tidak bisa dioperasikan lewat script. Katakan terus terang, bantu pasang Python (python.org). Sementara itu, sarankan pengguna membuat folder per bulan secara manual dan mengganti nama file sesuai pola `YYYY-MM-DD_vendor_nominal`, diberi label "belum tercatat di indeks".
