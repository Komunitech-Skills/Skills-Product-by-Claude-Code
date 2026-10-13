# 02 — Shopee Live 30 menit, kopi bubuk 3 varian + voucher berkuota

## Skenario
S2 — permintaan normal: live singkat (30 menit) di jam istirahat siang, 3 produk, satu paket bundling, dan voucher
toko dengan kuota nyata. Durasi sempit → script otomatis memakai pola ringkas.

## Input pengguna
```
Minta naskah shopee live 30 menit jam 12 siang buat Kopi Lereng Merapi. Arabika Gayo 200gr normal 85rb live 75rb,
kalau ambil 2 jadi 150rb. Robusta Temanggung 250gr 45rb live 39rb. House blend 250gr 55rb diskon 20%, bulatin ke 500an aja.
Ada voucher toko potongan 10rb min belanja 100rb, kuotanya 50. Kopinya giling sesuai pesanan (halus/sedang/kasar),
roasting tiap Senin. Kirim dari Sleman, bisa COD.
```

## Output

## Naskah Live Shopee — Kopi Lereng Merapi, 30 menit (12.00–12.30 WIB)

### Rundown (pola ringkas, dari `susun_segmen.py`)
| Waktu | Segmen | Produk |
|---|---|---|
| 12.00–12.03 | Pembukaan | – |
| 12.03–12.10 | Hook 1' · Demo 2' · Harga 1' · CTA 2' · Tanya-jawab 1' | Arabika Gayo 200 g |
| 12.10–12.17 | Hook 1' · Demo 2' · Harga 1' · CTA 2' · Tanya-jawab 1' | Robusta Temanggung 250 g |
| 12.17–12.18 | Rekap untuk penonton baru | – |
| 12.18–12.25 | Hook 1' · Demo 2' · Harga 1' · CTA 2' · Tanya-jawab 1' | House Blend 250 g |
| 12.25–12.27 | Tanya-jawab bebas & rekap | – |
| 12.27–12.30 | Penutup | – |

### Angka promo (dihitung script)
| Produk | Normal | Harga live | Hemat | Bundling |
|---|---|---|---|---|
| Arabika Gayo 200 g | Rp 85.000 | Rp 75.000 | Rp 10.000 (±11%) | Isi 2 Rp 150.000 → Rp 75.000/pcs (hemat Rp 20.000 vs 2× harga normal; **sama** dengan 2× harga live) |
| Robusta Temanggung 250 g | Rp 45.000 | Rp 39.000 | Rp 6.000 (±13%) | – |
| House Blend 250 g | Rp 55.000 | Rp 44.000 (diskon 20%, sudah pas kelipatan Rp 500) | Rp 11.000 (20%) | – |
| Voucher toko | Potongan Rp 10.000, min. belanja Rp 100.000, kuota 50 (sisa kuota dibaca dari layar) | | | |

⚠️ Paket isi 2 Arabika (Rp 150.000) harganya **sama** dengan beli 2 di harga live (2 × Rp 75.000). Jangan bilang "paket lebih
hemat dari harga live". Yang jujur: "hemat Rp 20.000 dibanding harga normal", atau ubah harga paket (mis. Rp 145.000) jika memang ingin paket lebih murah.

### Naskah

**[12.00–12.03] Pembukaan**
"Selamat siang Kak, selamat datang di live Kopi Lereng Merapi dari Sleman! Saya [nama host]. Yang lagi istirahat makan siang,
pas banget — 30 menit ke depan kita ngobrol kopi. Siang ini Arabika Gayo jadi Rp 75.000, Robusta Temanggung Rp 39.000, dan
House Blend Rp 44.000. Ada juga voucher toko potongan Rp 10.000 untuk belanja minimal Rp 100.000 — klaim dulu di layar sebelum
checkout ya." [tunjuk ikon voucher di layar] [sapa 3 nama pertama di komentar]

**[12.03–12.04] Hook — Arabika Gayo**
"Suka kopi yang [isi: ciri rasa Arabika Gayo dari toko, mis. tingkat pahit/asam/aroma]? Kenalan sama Arabika Gayo ini." [angkat kemasan]

**[12.04–12.06] Demo — Arabika Gayo**
"Biji kopinya saya tuang ya, lihat warnanya." [tuang biji ke piring kecil, dekatkan ke kamera]
"Kami roasting setiap Senin, dan kopinya digiling sesuai pesanan Kakak: halus untuk tubruk atau mesin, sedang untuk V60 atau
drip, kasar untuk French press. Pilih di varian saat checkout." [tunjukkan contoh hasil giling bila ada]

**[12.06–12.07] Harga & promo — Arabika Gayo**
"Harga normal Rp 85.000, khusus live Rp 75.000 — hemat Rp 10.000. Ambil 2 bungkus Rp 150.000, hemat Rp 20.000 dari harga normal." [pin produk no. 1]

**[12.07–12.09] CTA — Arabika Gayo**
"Klik ikon tas belanja di bawah, pilih produk nomor 1, pilih gilingan — halus, sedang, atau kasar — lalu checkout. Dua bungkus
Arabika sudah Rp 150.000; tambah satu Robusta, belanjanya lewat Rp 100.000 dan voucher potongan Rp 10.000 bisa dipakai.
Bisa COD ya Kak, pilih saat checkout."

**[12.09–12.10] Tanya-jawab — Arabika Gayo**
[baca komentar] "Kak [nama] tanya tanggal roasting — kami roasting tiap Senin. Kak [nama] tanya asam nggak — [isi: profil rasa dari toko]."

**[12.10–12.11] Hook — Robusta Temanggung**
"Yang butuh kopi 'nendang' buat melek sampai sore — ini Robusta Temanggung." [angkat kemasan]

**[12.11–12.13] Demo — Robusta Temanggung**
"Kemasan 250 gram. Saya seduh tubruk sebentar ya, biar kelihatan." [seduh dengan air panas, aduk, tunjukkan ampas turun]
"Pilihan gilingannya sama: halus, sedang, kasar."

**[12.13–12.14] Harga & promo — Robusta Temanggung**
"Normal Rp 45.000, live Rp 39.000 — hemat Rp 6.000." [pin produk no. 2]

**[12.14–12.16] CTA — Robusta Temanggung**
"Tas belanja, nomor 2, pilih gilingan, checkout. Mau pakai voucher Rp 10.000? Gabungkan dengan produk lain sampai minimal
Rp 100.000. Sisa kuota vouchernya sekarang [stok nyata: sisa kuota voucher] — angkanya kelihatan di layar ya."

**[12.16–12.17] Tanya-jawab — Robusta Temanggung**
[baca komentar] "Kak [nama] tanya awet berapa lama — [isi: saran penyimpanan & masa simpan dari toko]."

**[12.17–12.18] Rekap untuk penonton baru**
"Yang baru masuk, selamat siang! Arabika Gayo Rp 75.000 (nomor 1), 2 bungkus Rp 150.000. Robusta Temanggung Rp 39.000 (nomor 2).
Voucher Rp 10.000 untuk belanja minimal Rp 100.000 — klaim di layar. Sekarang House Blend."

**[12.18–12.19] Hook — House Blend**
"Bingung pilih arabika atau robusta? House Blend ini campuran keduanya, pas buat kopi susu di rumah." [angkat kemasan]

**[12.19–12.21] Demo — House Blend**
"Saya bikinkan kopi susu sederhana ya: kopi tubruk, tambah susu." [seduh + tuang susu, tunjukkan warnanya]
"Komposisi campurannya [isi: persentase arabika/robusta jika toko mau menyebut]."

**[12.21–12.22] Harga & promo — House Blend**
"Normal Rp 55.000, live diskon 20% jadi Rp 44.000 — hemat Rp 11.000." [pin produk no. 3]

**[12.22–12.24] CTA — House Blend**
"Tas belanja, nomor 3, pilih gilingan, checkout. Satu House Blend plus dua Robusta sudah Rp 122.000 — lewat minimal belanja voucher.
COD bisa ya Kak."

**[12.24–12.25] Tanya-jawab — House Blend**
[baca komentar] Jawab dari bank jawaban di bawah.

**[12.25–12.27] Tanya-jawab bebas & rekap**
"Saya jawab pertanyaan yang tadi terlewat ya." [baca komentar] "Rekap: Arabika Rp 75.000, Robusta Rp 39.000, House Blend Rp 44.000,
voucher Rp 10.000 min. Rp 100.000, sisa kuota [stok nyata]."

**[12.27–12.30] Penutup**
"Terima kasih sudah ngopi bareng Kopi Lereng Merapi siang ini! Harga live berlaku sampai live selesai jam 12.30. Pesanan dikirim dari
Sleman, bisa COD. Live berikutnya [isi: jadwal]. Follow toko kami ya. Selamat lanjut kerja, Kak!"

### Jawaban cepat pertanyaan penonton
| Pertanyaan | Jawaban |
|---|---|
| "Harganya berapa?" | "Arabika Rp 75.000, Robusta Rp 39.000, House Blend Rp 44.000 selama live, Kak [nama]." |
| "Bisa digiling?" | "Bisa, pilih halus/sedang/kasar di varian saat checkout." |
| "Roasting kapan?" | "Kami roasting setiap Senin." |
| "Bisa COD?" | "Bisa Kak, pilih COD saat checkout." |
| "Voucher nggak bisa dipakai?" | "Cek minimal belanja Rp 100.000 dan pastikan klaim voucher di layar live dulu sebelum checkout." |
| "Ongkir berapa?" | "Dihitung otomatis sesuai alamat saat checkout; dikirim dari Sleman." |
| "Kopinya halal?" | "Untuk info sertifikasi, cek deskripsi produk ya Kak." (sertifikat tidak diberikan pemilik) |
| "Ada yang tanpa ampas?" | "Pilih gilingan sedang dan seduh pakai saringan/V60 ya Kak." |

### Catatan untuk host
- Sisa kuota voucher dibaca dari layar (`[stok nyata]`), jangan dikarang. Jangan hitung mundur "voucher habis 5 menit lagi" kecuali memang berakhir.
- Jangan bilang paket isi 2 Arabika "lebih murah dari harga live" (harganya sama).
- Hal yang perlu dilengkapi: profil rasa (termasuk ciri rasa di hook Arabika Gayo; belum diberikan pengguna, jadi ditulis `[isi: ...]`), saran penyimpanan/masa simpan, komposisi House Blend, jadwal live berikutnya.
- Asumsi: host `[nama host]`; voucher berlaku untuk semua produk; urutan produk Arabika dulu karena harganya tertinggi & ada paket.

## Catatan penguji
- **Angka diverifikasi independen:** 45.000−39.000 = 6.000 → 13,3% → 13% ✔; 85.000−75.000 = 10.000 → 11,7% → 11% ✔; paket 2×85.000−150.000 = 20.000 ✔;
  55.000 × 80% = 44.000 (sudah kelipatan 500) → 20% ✔; contoh keranjang 44.000 + 2×39.000 = 122.000 ≥ 100.000 ✔; 2×75.000 + 39.000 = 189.000 ✔.
- **Urgensi jujur:** hanya kuota voucher nyata (dibaca dari layar) dan batas waktu live. Tidak ada klaim halal karangan (dijawab "cek deskripsi").
- **Temuan:** `hitung_promo.py` **tidak memberi peringatan** bila harga per pcs paket **sama** dengan harga live satuan (hanya bila lebih mahal,
  baris 177: `per_pcs > live`). Di sini agent harus menangkapnya sendiri. Saran: ubah jadi `per_pcs >= live` dengan pesan "paket tidak lebih
  hemat dari harga live satuan; jangan sebut lebih hemat".
- Pola ringkas 30 menit tetap memberi rekap di menit 17 ✔. Naskah siap ucap, CTA ke tas belanja Shopee.
