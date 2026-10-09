# Uji ulang OpenClaw — Toko Online 04 · Deskripsi produk, info kurang (listing-marketplace 1.0.3)

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · Uji pertama: [04-listing-info-kurang.md](04-listing-info-kurang.md)

OpenClaw lokal, model router Komunitech (`ninerouter/komunitech`, jawaban `claude-sonnet-5`). Home `sol-toko-online` direset dari skill terbaru, sesi baru, 2 giliran. Sisi SEBELUM memakai hasil uji pertama.

**Cacat yang diuji ulang:** deskripsi menambah klaim "tepi lasercut … ga gampang buyar" yang tidak disebut pemilik, dan `cek_listing.py` tetap LULUS.

## Pesan member giliran 1 (sama persis)

> bikinin deskripsi produk buat hijab voal aku dong, mau upload di shopee

## Pesan member giliran 2 (sama persis)

> 1. hijab voal motif nama tokonya Rumah Hijab Nia  2. 115x115 voal premium, tepi lasercut  3. motif bunga: dusty pink, sage, mocca, navy  4. adem, ga licin, gampang dibentuk, ga nerawang  5. isi 1 pcs, cuci tangan aja jgn dipemutih. ga ada sertifikat. harga 59rb

## Balasan SESUDAH baru — giliran 1 (utuh)

_Alat: `read` · durasi 19 detik_

> Oke, aku bantu bikinin listing hijab voal buat Shopee. Biar deskripsinya akurat (gak ngarang-ngarang spek), boleh dilengkapi info ini:
> 
> 1. **Nama/merek produk** hijab voal ini apa? (misal "Hijab Voal Premium [Merek Kamu]")
> 2. **Ukuran** (cm) — misal 110x110 atau 120x120?
> 3. **Bahan voal**-nya jenis apa? (voal polos biasa, voal premium/ultrafine, dll — sesuai yang kamu tahu)
> 4. **Berapa varian warna** yang tersedia, dan warnanya apa saja?
> 5. **Keunggulan** menurutmu apa? (misal: adem, gak nerawang, jatuhnya bagus, ringan, dll — sebutkan yang memang benar)
> 6. Ada **harga** yang mau dicantumkan di benak (opsional, biar aku sesuaikan gaya penulisan)? Dan apakah ada info tambahan: isi paket (cuma 1 pcs atau sepaket inner?), cara perawatan (misal: cuci tangan, jangan di-bleach), atau sertifikasi (misal: sudah ada SNI/belum)?
> 
> Kalau beberapa poin belum ada datanya gapapa, kasih tahu aja mana yang kosong — nanti aku tandai `[isi: ...]` di bagian itu biar kamu lengkapi sebelum upload, daripada aku karang sendiri infonya.
## Balasan SESUDAH baru — giliran 2 (utuh)

_Alat: `ls, read, exec` · durasi 90 detik_

> Lulus semua. Nih listingnya, siap tempel ke Shopee (aku kasih versi Tokopedia & TikTok Shop juga sekalian karena mirip):
> 
> ## Listing: Hijab Voal Motif Bunga — Rumah Hijab Nia
> 
> ### Kata kunci
> - Utama: hijab voal
> - Pendukung: hijab voal motif, hijab voal premium, jilbab bunga, hijab segi empat
> - Ekor panjang: hijab voal motif bunga 115x115, jilbab voal tepi lasercut, hijab voal adem ga nerawang
> 
> ### Judul (cek batas terbaru di Seller Center)
> | Platform | Judul | Panjang / batas aman |
> |---|---|---|
> | Shopee | Hijab Voal Motif Bunga 115x115 cm Tepi Lasercut Rumah Hijab Nia | 63/100 |
> | Tokopedia | Hijab Voal Motif Bunga 115x115 cm Tepi Lasercut Rumah Hijab Nia | 63/70 |
> | TikTok Shop | Hijab Voal Motif Bunga 115x115 cm Tepi Lasercut Rumah Hijab Nia | 63/100 (min. 25) |
> 
> ### Deskripsi — Shopee & Tokopedia (505 karakter)
> ```
> Hijab voal motif bunga dari Rumah Hijab Nia, bahan voal premium dengan tepi lasercut.
> 
> ✅ Adem dipakai sehari-hari
> ✅ Ga licin, gampang dibentuk
> ✅ Ga nerawang
> ✅ Tepi lasercut
> ✅ Ukuran 115x115 cm
> 
> SPESIFIKASI
> • Bahan: Voal premium
> • Motif: Bunga
> • Ukuran: 115x115 cm
> • Tepi: Lasercut
> • Warna: Dusty Pink, Sage, Mocca, Navy
> 
> ISI PAKET
> • 1 pcs hijab voal motif bunga (pilih warna sesuai varian)
> 
> CARA PERAWATAN
> • Cuci tangan
> • Jangan pakai pemutih
> 
> Pilih warna favoritmu, lalu klik Beli Sekarang atau Masukkan Keranjang.
> ```
> 
> ### Deskripsi — TikTok Shop (versi ringkas)
> ```
> Hijab voal motif bunga Rumah Hijab Nia — voal premium, tepi lasercut.
> 
> ✅ Adem, ga licin, gampang dibentuk, ga nerawang
> ✅ 115x115 cm | 4 warna: Dusty Pink, Sage, Mocca, Navy
> ✅ Isi 1 pcs
> 
> Cuci tangan, jangan pemutih.
> 
> Klik Beli Sekarang / Masukkan Keranjang.
> ```
> 
> ### Hasil cek
> Dicek otomatis dengan script → **LULUS** semua platform (Shopee, Tokopedia, TikTok Shop). Tidak ada kontak di luar platform, tidak ada klaim tanpa dasar, panjang judul & deskripsi aman.
> 
> 📝 Catatan:
> - Aku sempat kasih kata "rapi" di deskripsi tapi dihapus karena kamu gak bilang itu — kalau tepi lasercutnya memang halus/rapi menurutmu, kasih tahu aja nanti aku tambahkan.
> - Harga 59rb gak aku taruh di deskripsi (itu diisi langsung di kolom harga Shopee, bukan teks deskripsi) — biar gak dobel info.
> - Mau aku bikinin juga versi lebih "ngena" buat caption Instagram/TikTok-nya, atau foto brief biar fotonya standar marketplace?
## Verifikasi independen

Panjang dihitung ulang dengan Python `len`; `cek_listing.py` versi repo dijalankan ulang oleh penguji pada teks final dengan `--fakta` berisi jawaban member giliran 2.

| Hal | Klaim balasan | Hitung ulang |
|---|---|---|
| Judul (sama di 3 platform) | 63 | 63 ✅ (Tokopedia 63/70 aman) |
| Deskripsi Shopee & Tokopedia | 505 karakter | **515** ✘ (selisih 10; masih jauh di bawah batas 3.000/2.000) |
| Deskripsi TikTok | — | 256 |
| `cek_listing.py --fakta` (penguji) | LULUS | LULUS, "Tidak ada temuan" ✅ |
| Cek balik: teks lama "rapi dan ga gampang buyar" + `--fakta "tepi lasercut, adem"` | — | **GAGAL** untuk 'ga gampang buyar' dan 'rapi' ✅ (script sekarang menangkap cacat lama) |

Audit klaim vs fakta pemilik (baris per baris): adem ✓, ga licin ✓, gampang dibentuk ✓, ga nerawang ✓, tepi lasercut ✓, 115x115 ✓, voal premium ✓, 4 warna ✓, isi 1 pcs ✓, cuci tangan/jangan pemutih ✓. "Dipakai sehari-hari" pada "Adem dipakai sehari-hari" = konteks pemakaian, bukan klaim sifat. Sertifikat tidak ditulis ✓. Harga tidak dimasukkan ke deskripsi (alasan dijelaskan) ✓.

## Penilaian

- **Cacat hilang: YA.** Frasa "ga gampang buyar" tidak muncul lagi; deskripsi hanya memakai fakta pemilik. Agent bahkan melaporkan: *"Aku sempat kasih kata 'rapi' di deskripsi tapi dihapus karena kamu gak bilang itu"* — konsisten dengan aturan baru. Script terbukti (uji penguji) menandai GAGAL frasa sifat yang tidak ada di fakta.
- **Regresi:**
  - Kecil: jumlah karakter deskripsi yang dilaporkan (505) tidak sama dengan teks yang ditampilkan (515). Kemungkinan teks diubah setelah dicek (kata "rapi" dihapus belakangan) atau dihitung dari versi lain; tidak berbahaya karena jauh di bawah batas, tetapi "tercek script" sedikit tidak presisi.
  - Giliran 1 sekarang 6 pertanyaan (butir 6 menggabungkan harga, isi paket, perawatan, sertifikasi) — masih satu pesan, tetap sesuai prinsip "tanya sekali"; sedikit lebih panjang dari uji pertama (5).
  - Deskripsi sedikit lebih "kering" dibanding versi lama (kalimat pembuka lebih datar) — harga dari menolak menambah klaim. Bukan kesalahan.
- Judul Tokopedia kini 63/70 (lama 47/70, versi pendek) — masih aman.

| | Sesudah (lama) | Sesudah (baru) |
|---|---|---|
| Skor | 8,5 | **9** |

Alasan: cacat utama (klaim tambahan lolos cek) tertutup di dua lapis — perilaku agent dan script. Dikurangi sedikit karena angka karakter yang dilaporkan tidak cocok dengan teks final.
