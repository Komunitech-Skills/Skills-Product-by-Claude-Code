# 01 — Gamis busui untuk Shopee, Tokopedia, dan TikTok Shop

## Skenario
S1 — permintaan normal dan lengkap: produk fashion dengan spesifikasi ukuran, bahan, warna, dan tiga platform. Script `cek_listing.py`
dijalankan sungguhan untuk ketiga versi.

## Input pengguna
```
Bikinin listing buat gamis busui aku, namanya Gamis Alya dari Rumah Alya (Solo). Bahan katun rayon, ada resleting depan buat menyusui.
Ukuran M (LD 100, PB 135), L (LD 106, PB 137), XL (LD 112, PB 139). Warna navy, sage, mocca. Mau upload di Shopee, Tokopedia, sama TikTok Shop.
```

## Output

## Listing: Gamis Alya — Gamis Busui Katun Rayon

### Kata kunci
- Utama: gamis busui
- Pendukung: katun rayon, resleting depan, gamis menyusui, gamis solo
- Ekor panjang: gamis busui resleting depan, gamis katun rayon adem, gamis menyusui ukuran XL, gamis busui warna sage

### Judul (cek batas terbaru di Seller Center)
| Platform | Judul | Panjang / batas aman |
|---|---|---|
| Shopee | Gamis Busui Katun Rayon Resleting Depan Gamis Alya Ukuran M L XL Navy Sage Mocca | 80/100 |
| Tokopedia | Gamis Busui Katun Rayon Resleting Depan Gamis Alya M L XL | 57/70 |
| TikTok Shop | Gamis Busui Katun Rayon Resleting Depan Ramah Menyusui Ukuran M L XL | 68/100 (min. 25) |

### Deskripsi — Shopee & Tokopedia (1.173 karakter)
```
Gamis busui (gamis menyusui) dari katun rayon yang adem, dengan resleting depan supaya Bunda bisa menyusui tanpa ribet. Nyaman dipakai di rumah, ke pengajian, sampai jalan-jalan bareng si kecil.

✅ Resleting depan, praktis untuk menyusui
✅ Katun rayon, adem dan jatuh saat dipakai
✅ 3 ukuran: M, L, XL dengan lingkar dada 100–112 cm
✅ 3 warna kalem: Navy, Sage, Mocca
✅ Cocok untuk harian, pengajian, dan acara keluarga

SPESIFIKASI
• Nama produk: Gamis Alya by Rumah Alya
• Bahan: katun rayon
• Model: gamis dengan resleting depan (busui friendly)
• Warna: Navy / Sage / Mocca

UKURAN (dalam cm)
• M: lingkar dada 100, panjang badan 135
• L: lingkar dada 106, panjang badan 137
• XL: lingkar dada 112, panjang badan 139
Toleransi ukuran [isi: mis. 1–2 cm]. Bandingkan dengan gamis yang Bunda punya sebelum memilih.

ISI PAKET
• 1 gamis [isi: termasuk/tidak termasuk hijab atau belt]

CARA PERAWATAN
• [isi: saran cuci dari toko, mis. cuci dengan tangan, jangan diperas keras, jemur di tempat teduh]

INFO PENGIRIMAN & GARANSI
• Dikirim dari Solo
• [isi: jadwal kirim & kebijakan retur/tukar ukuran]

Pilih ukuran dan warna, lalu klik Masukkan Keranjang atau Beli Sekarang.
```

### Deskripsi — TikTok Shop (462 karakter)
```
Gamis busui katun rayon dengan resleting depan — adem, praktis untuk menyusui.

✅ Resleting depan untuk menyusui
✅ Katun rayon, adem & jatuh
✅ Ukuran M / L / XL (LD 100 / 106 / 112 cm)
✅ Warna: Navy, Sage, Mocca

UKURAN (cm)
M: LD 100, PB 135
L: LD 106, PB 137
XL: LD 112, PB 139

Isi: 1 gamis [isi: dengan/tanpa hijab]
Perawatan: [isi: saran cuci]
Dikirim dari Solo. [isi: kebijakan retur/tukar ukuran]

Pilih ukuran & warna, lalu klik keranjang untuk checkout.
```

### Hasil cek
`cek_listing.py` — Shopee **LULUS** (judul 80/100, deskripsi 1.173/3.000), Tokopedia **LULUS** (57/70, 1.173/2.000), TikTok Shop **LULUS**
(68/100, min. 25; deskripsi 462/2.000). Tidak ada nomor/link/@akun, tidak ada kata berisiko. Kata kunci utama "gamis busui" di posisi 0 judul.
Batas yang dipakai adalah **batas aman skill, bukan batas resmi — cek batas terbaru di Seller Center**.

📝 Asumsi & yang perlu dilengkapi: toleransi ukuran, isi paket (dengan/tanpa hijab/belt), cara perawatan, jadwal kirim, dan kebijakan retur/tukar
ukuran belum diberikan → ditandai `[isi: …]`. Tidak menulis "premium", "tidak menerawang", "wudhu friendly", atau klaim lain yang tidak disebut.
Target pembeli diasumsikan ibu menyusui. Mau versi judul yang menonjolkan warna, atau deskripsi lebih pendek?

## Catatan penguji
- **Batas karakter dihitung ulang independen** (python `len` & UTF-16): 80, 57, 68 karakter; deskripsi 1.173 & 462 — cocok dengan script ✔.
  Label "cek batas terbaru di Seller Center" ada di judul tabel & hasil cek ✔.
- **Tidak ada klaim karangan:** hanya bahan, resleting depan, ukuran, warna, dan kota dari pengguna. Kata "adem" dan "jatuh" adalah deskripsi karakter
  bahan katun rayon yang umum — masih wajar, tetapi SKILL.md belum membedakan kata sifat bahan dari klaim (ringan).
- Teks deskripsi polos (tanpa markdown), CTA ke tombol platform ✔.
- **Kurang (ringan):** pengecekan kata kunci di script mencari **frasa persis** — kata kunci "gamis katun rayon" dilaporkan "tidak ada" walau judul berisi
  "Gamis Busui Katun Rayon". Agent perlu memilih kata kunci yang cocok persis agar laporan tidak membingungkan.
