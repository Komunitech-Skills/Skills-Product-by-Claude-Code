---
name: listing-marketplace
description: Membuat listing produk siap tempel untuk Shopee, Tokopedia, dan TikTok Shop — judul sesuai batas karakter tiap platform, poin keunggulan, deskripsi lengkap, dan daftar kata kunci — plus cek otomatis panjang teks, info kontak terlarang, dan klaim berisiko. Gunakan saat pengguna minta judul produk, deskripsi produk, optimasi listing/SEO marketplace, atau upload produk ke toko online (product listing, product title, product description, marketplace SEO). Bukan untuk caption posting sosmed (pakai caption-sosmed-umkm).
---

# Listing Marketplace (Shopee, Tokopedia, TikTok Shop)

## Tujuan
Mengubah info produk seadanya menjadi listing yang mudah ditemukan di pencarian marketplace, jelas bagi
pembeli, dan aman dari pelanggaran aturan (teks terpotong, kontak di luar platform, klaim tanpa bukti).

## Kapan digunakan
- "Buatin judul dan deskripsi produk buat Shopee/Tokopedia/TikTok Shop"
- Memperbaiki listing lama yang sepi pengunjung, atau menyesuaikan satu produk untuk beberapa platform
- Mencari kata kunci untuk judul/iklan marketplace

## Kapan TIDAK digunakan
- Caption posting Instagram/TikTok/WA Status → skill `caption-sosmed-umkm`
- Naskah live jualan → `naskah-live-jualan`; menentukan harga jual & potongan admin → `harga-jual-marketplace`
- Membalas ulasan pembeli → `balas-ulasan-pelanggan`
- Produk tiruan (KW/replika) atau produk terlarang → tolak dengan sopan dan jelaskan alasannya

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Nama & jenis produk | Ya | — (tanyakan) |
| Spesifikasi (ukuran/berat/isi, bahan, varian/warna) | Ya | — (tanyakan; jangan dikarang) |
| Platform tujuan | Tidak | Ketiganya: Shopee, Tokopedia, TikTok Shop |
| Keunggulan / pembeda dari produk lain | Tidak | Diturunkan dari spesifikasi, tanpa klaim baru |
| Target pembeli | Tidak | Disimpulkan dari jenis produk, disebut sebagai asumsi |
| Izin/sertifikat (halal, BPOM, PIRT, SNI, garansi resmi) | Tidak | Dianggap **tidak ada** → tidak ditulis |
| Isi paket, cara pakai/perawatan, info pengiriman | Tidak | Bagian dibuat dengan penanda `[isi: ...]` |
| Batas karakter terbaru dari Seller Center | Tidak | Batas aman di `references/batas-platform.md` |

Jika info wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor). Jika pengguna ingin cepat,
lanjutkan dengan penanda `[isi: ...]` untuk data yang belum ada dan sebutkan asumsinya di akhir.

## Langkah kerja
1. **Baca `references/batas-platform.md`** untuk batas aman & aturan konten. Batas di sana belum
   terverifikasi resmi → selalu tulis label "cek batas terbaru di Seller Center".
2. **Susun kata kunci** (lihat references): 1 utama, 3–5 pendukung, 3–6 ekor panjang. Pakai bahasa yang
   diketik pembeli ("gamis busui", bukan "busana muslimah menyusui premium").
3. **Tulis judul per platform** dengan pola `kata kunci utama + pembeda + spesifikasi + isi + fungsi`.
   Kata kunci utama di 40 karakter pertama. Huruf Awal Kapital, tanpa emoji, tanpa kata diulang.
   Tokopedia paling ketat (70) → buat versi paling ringkas.
4. **Tulis 5 poin keunggulan** (manfaat + bukti dari spesifikasi, maks. ±80 karakter per poin). Di Shopee
   dan Tokopedia poin ini diletakkan di awal deskripsi karena tidak ada kolom khusus.
5. **Tulis deskripsi** dengan urutan tetap: pembuka 1–2 kalimat → poin keunggulan → spesifikasi →
   isi paket → cara pakai/perawatan → ukuran/varian → info pengiriman & garansi (hanya yang benar) →
   ajakan beli yang mengarah ke tombol platform ("Klik Beli Sekarang", "Masukkan keranjang").
   TikTok Shop: buat lebih ringkas dan mudah dipindai (pembeli datang dari video).
6. **Cek otomatis** tiap versi dengan script (path relatif terhadap folder SKILL.md ini):
   ```bash
   python3 <folder-skill-ini>/scripts/cek_listing.py --platform tokopedia \
     --judul "..." --deskripsi-file deskripsi.txt --kata-kunci "utama,pendukung1,pendukung2"
   ```
   Windows: ganti `python3` dengan `python` atau `py`. `--platform semua` memeriksa ketiganya; tambah
   `--json` bila perlu. Perbaiki semua temuan **GAGAL**; tinjau **CEK** (klaim harus didukung data pengguna).
   **Jika Python tidak bisa dijalankan:** hitung panjang judul/deskripsi secara manual (hitung per karakter,
   emoji = 2), cocokkan dengan tabel batas, dan periksa manual daftar larangan di checklist. Beri tahu
   pengguna bahwa pengecekan dilakukan manual.
7. Sajikan output sesuai format, lalu tawarkan revisi (nada, fokus kata kunci, versi lebih pendek).

## Format output
````
## Listing: <nama produk>

### Kata kunci
- Utama: ...
- Pendukung: ..., ..., ...
- Ekor panjang: ..., ..., ...

### Judul (cek batas terbaru di Seller Center)
| Platform | Judul | Panjang / batas aman |
|---|---|---|
| Shopee | ... | 78/100 |
| Tokopedia | ... | 64/70 |
| TikTok Shop | ... | 81/100 (min. 25) |

### Deskripsi — Shopee & Tokopedia (<panjang> karakter)
```
<teks siap tempel, tanpa format markdown: pakai ✅ / • dan baris kosong>
```

### Deskripsi — TikTok Shop (<panjang> karakter)
```
<versi ringkas siap tempel>
```

### Hasil cek
<ringkasan temuan script atau "dicek manual">

📝 Asumsi & yang perlu dilengkapi: <daftar [isi: ...] dan asumsi>
````
Teks di dalam blok kode harus polos (tanpa `**tebal**`/`#`) karena kolom deskripsi marketplace tidak
membaca markdown.

## Contoh
**Input pengguna:** "Tolong bikinin listing buat sambal cumi asin 'Dapur Bu Ratmi' dari Sidoarjo, botol
200 ml, level pedas sedang & pedas banget, tanpa pengawet, tahan 1 bulan di suhu ruang, sudah PIRT
3203xxxxxxxxx-27, halal belum. Jual di Shopee sama Tokopedia."

**Output (ringkas):**
````
### Kata kunci
- Utama: sambal cumi
- Pendukung: sambal cumi asin, sambal botol, sambal pedas, oleh oleh sidoarjo
- Ekor panjang: sambal cumi asin pedas tanpa pengawet, sambal cumi botol 200 ml, lauk praktis anak kos

### Judul (cek batas terbaru di Seller Center)
| Platform | Judul | Panjang / batas aman |
|---|---|---|
| Shopee | Sambal Cumi Asin Pedas 200 ml Tanpa Pengawet Dapur Bu Ratmi Oleh Oleh Sidoarjo | 78/100 |
| Tokopedia | Sambal Cumi Asin Pedas 200 ml Tanpa Pengawet Oleh Oleh Sidoarjo | 63/70 |

### Deskripsi — Shopee & Tokopedia
```
Sambal cumi asin buatan Dapur Bu Ratmi, Sidoarjo. Tinggal buka botol, langsung jadi lauk
teman nasi hangat.

✅ Tanpa pengawet
✅ Tahan ±1 bulan di suhu ruang
✅ 2 level: Pedas Sedang & Pedas Banget
✅ Botol 200 ml, praktis untuk stok lauk & bekal
✅ Terdaftar PIRT No. 3203xxxxxxxxx-27

SPESIFIKASI
• Isi: 200 ml
• Varian: Pedas Sedang / Pedas Banget
• Daya simpan: ±1 bulan suhu ruang; simpan di kulkas setelah dibuka [isi: daya simpan setelah dibuka]
...
Pilih level pedas, lalu klik Masukkan Keranjang. Pesanan dikirim dari Sidoarjo.
```
📝 Asumsi: kata "halal" tidak ditulis karena belum bersertifikat; bahan botol & rasa tidak dideskripsikan
karena tidak disebutkan. Lengkapi [isi: ...] sebelum tayang.
````

## Checklist sebelum mengirim hasil
- [ ] Panjang judul & deskripsi ≤ batas aman tiap platform (script lulus atau dicek manual), ada label "cek batas terbaru"
- [ ] Kata kunci utama ada di 40 karakter pertama judul; tidak ada kata diulang >2 kali
- [ ] Tidak ada nomor HP/WA, link, @akun, email, atau ajakan transaksi di luar platform
- [ ] Tidak ada klaim yang tidak diberikan pengguna (halal, BPOM, SNI, original, terlaris, termurah, klaim kesehatan)
- [ ] Tidak menyebut merek lain untuk numpang pencarian
- [ ] Semua spesifikasi berasal dari pengguna; yang belum ada ditandai `[isi: ...]`
- [ ] Teks deskripsi polos (tanpa markdown) dan siap tempel

## Batasan & penanganan error
- Batas karakter di skill adalah batas aman, bukan batas resmi. Jika pengguna menyebut batas terbaru,
  jalankan script dengan `--batas-judul` / `--batas-deskripsi` sesuai angka itu.
- Skill tidak bisa melihat data pencarian marketplace secara langsung. Kata kunci adalah usulan; sarankan
  pengguna mencocokkan dengan saran pencarian di aplikasi.
- Harga, biaya admin, dan ongkir tidak dikarang. Jika diminta, arahkan ke `harga-jual-marketplace`.
- Pengguna meminta klaim tanpa bukti ("tulis aja halal") → jelaskan risikonya (produk diturunkan, sanksi
  hukum perlindungan konsumen) dan tawarkan kalimat alternatif yang jujur.
- Script error (file tidak ada, platform tidak dikenal, bukan UTF-8) → baca pesan error bahasa Indonesia,
  perbaiki argumen, atau lanjutkan cek manual.
