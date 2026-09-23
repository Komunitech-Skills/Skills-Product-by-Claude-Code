# 01 — TikTok Live 60 menit, toko batik (3 produk, diskon persen, bundling, stok nyata)

## Skenario
S1 — permintaan normal dan lengkap: 3 produk dengan jenis promo berbeda (harga live, diskon persen, paket isi 2,
dan satu produk tanpa promo dengan stok terbatas yang **nyata**). Kedua script dijalankan sungguhan.

## Input pengguna
```
Bikinin script live TikTok 1 jam ya, mulai jam 8 malam. Toko Batik Lestari dari Pekalongan.
Produk: Kemeja batik cap pria katun primisima, normal 185rb, pas live 149rb, beli 2 jadi 280rb.
Daster batik rayon allsize (LD 120), 95rb diskon 15%.
Kain batik tulis 2 meter pewarna alam, 650rb gak diskon, stoknya emang cuma 5 lembar bulan ini.
Kirim tiap hari dari Pekalongan, gak ada COD. Retur boleh kalau salah kirim, wajib video unboxing.
```

## Output

## Naskah Live TikTok — Batik Lestari, 60 menit (20.00–21.00 WIB)

### Rundown (dari `susun_segmen.py`)
| Waktu | Segmen | Produk |
|---|---|---|
| 20.00–20.03 | Pembukaan: sapa, hook besar, janji promo live | – |
| 20.03–20.04 | Hook | Kemeja Batik Cap Pria |
| 20.04–20.08 | Demo produk | Kemeja Batik Cap Pria |
| 20.08–20.10 | Harga & promo | Kemeja Batik Cap Pria |
| 20.10–20.12 | CTA & cara checkout | Kemeja Batik Cap Pria |
| 20.12–20.14 | Tanya-jawab | Kemeja Batik Cap Pria |
| 20.14–20.15 | Hook | Daster Batik |
| 20.15–20.19 | Demo produk | Daster Batik |
| 20.19–20.21 | Harga & promo | Daster Batik |
| 20.21–20.23 | CTA & cara checkout | Daster Batik |
| 20.23–20.25 | Tanya-jawab | Daster Batik |
| 20.25–20.26 | Rekap untuk penonton baru | – |
| 20.26–20.27 | Hook | Kain Batik Tulis 2 m |
| 20.27–20.31 | Demo produk | Kain Batik Tulis 2 m |
| 20.31–20.33 | Harga | Kain Batik Tulis 2 m |
| 20.33–20.35 | CTA & cara checkout | Kain Batik Tulis 2 m |
| 20.35–20.37 | Tanya-jawab | Kain Batik Tulis 2 m |
| 20.37–20.48 | Putaran 2: Hook, Demo, Harga, CTA, Tanya-jawab | Kemeja Batik Cap Pria |
| 20.48–20.57 | Tanya-jawab bebas & rekap semua produk | – |
| 20.57–21.00 | Penutup: rekap promo, pengingat checkout, jadwal live berikutnya | – |

### Angka promo (dihitung script)
| Produk | Normal | Harga live | Hemat | Bundling |
|---|---|---|---|---|
| Kemeja Batik Cap Pria | Rp 185.000 | Rp 149.000 | Rp 36.000 (±19%) | Isi 2 Rp 280.000 → Rp 140.000/pcs, hemat Rp 90.000 vs 2× harga normal |
| Daster Batik | Rp 95.000 | Rp 81.000 (diskon 15% = Rp 80.750, dibulatkan ke atas ke Rp 1.000) | Rp 14.000 (±14%) | – |
| Kain Batik Tulis 2 m | Rp 650.000 | – (tanpa promo) | – | – |

⚠️ Karena harga daster dibulatkan ke Rp 81.000, potongan sebenarnya ±14%. Di live, sebut **"hemat Rp 14.000"**,
jangan "diskon 15%". Kalau ingin tetap bisa bilang 15%, pasang harga live Rp 80.750 atau Rp 80.000 di keranjang.

### Naskah

**[20.00–20.03] Pembukaan**
"Selamat malam Kak, selamat datang di live Batik Lestari langsung dari Pekalongan! Saya [nama host]. Yang baru masuk,
tap love dulu biar nggak ketinggalan ya. Malam ini ada tiga yang mau saya tunjukkan: kemeja batik cap pria yang khusus
live jadi Rp 149.000, daster batik rayon yang adem buat di rumah, dan kain batik tulis pewarna alam yang bulan ini
memang cuma ada 5 lembar." [sapa 3 nama pertama di komentar] [tunjukkan ketiga produk sekilas ke kamera]
"Tulis di komentar Kakak nonton dari kota mana, biar saya sapa satu-satu."

**[20.03–20.04] Hook — Kemeja Batik Cap Pria**
"Bapak-bapak atau Kakak yang cari kemeja batik buat kondangan dan kantor tapi nggak mau yang gerah seharian — ini dia." [angkat kemeja ke kamera]

**[20.04–20.08] Demo — Kemeja Batik Cap Pria**
"Bahannya katun primisima, saya dekatkan ya biar kelihatan seratnya." [dekatkan kain ke kamera, remas pelan lalu lepas]
"Ini batik cap, motifnya dicap dengan canting cap, jadi tiap potong bisa sedikit beda — itu ciri batik cap, bukan cacat."
[bentangkan kemeja, tunjukkan depan-belakang] "Ukuran yang tersedia [isi: daftar ukuran & lingkar dada]. Kalau ragu,
tulis tinggi dan berat badan di komentar, saya bantu pilihkan." [baca komentar ukuran]

**[20.08–20.10] Harga & promo — Kemeja Batik Cap Pria**
"Harga normalnya Rp 185.000. Khusus selama live malam ini jadi Rp 149.000 — hemat Rp 36.000. Mau lebih hemat? Ambil
paket isi 2, Rp 280.000 saja, jadi Rp 140.000 per potong — hemat Rp 90.000 dibanding beli 2 di harga normal. Cocok buat
Bapak dan kakaknya, atau satu buat kantor satu buat kondangan." [pin produk no. 1]
"Stok harga live yang ada di keranjang sekarang [stok nyata] ya Kak, angkanya kelihatan di layar."

**[20.10–20.12] CTA & cara checkout — Kemeja Batik Cap Pria**
"Caranya: klik keranjang kuning di bawah, pilih produk nomor 1, pilih ukuran — kalau mau paket isi 2, pilih varian
'Paket 2' — lalu checkout. Pembayaran pilih yang tersedia di aplikasi ya Kak, untuk toko kami **belum ada COD**.
Pesanan dikirim setiap hari dari Pekalongan." [tunjukkan layar keranjang bila bisa] [sebut nama yang sudah checkout, hanya jika memang terlihat]

**[20.12–20.14] Tanya-jawab — Kemeja Batik Cap Pria**
[baca komentar] "Kak [nama] tanya luntur nggak — [isi: cara cuci/perawatan dari toko]. Kak [nama] tanya ada ukuran
[x] — yang ready yang ada di pilihan varian; kalau tidak muncul berarti sedang kosong."
"Yang sudah yakin, langsung keranjang kuning nomor 1 ya."

**[20.14–20.15] Hook — Daster Batik**
"Nah, buat Ibu-ibu dan Kakak yang di rumah seharian: daster yang adem, longgar, tapi tetap rapi kalau ada tamu — ini." [angkat daster]

**[20.15–20.19] Demo — Daster Batik**
"Bahannya rayon, jatuh dan adem. Saya bentangkan ya." [bentangkan daster, tunjukkan panjang dan motif]
"Ukurannya allsize, lingkar dada 120 cm, jadi longgar. Panjangnya [isi: panjang daster]." [ukur LD pakai meteran di depan kamera]
"Pilihan motif/warna yang ready [isi: daftar motif]." [tunjukkan tiap motif 5–10 detik]

**[20.19–20.21] Harga & promo — Daster Batik**
"Harga normal daster ini Rp 95.000, khusus live jadi Rp 81.000 — hemat Rp 14.000 per potong." [pin produk no. 2]
"Harga live berlaku selama live ini ya Kak."

**[20.21–20.23] CTA & cara checkout — Daster Batik**
"Klik keranjang kuning, pilih produk nomor 2, pilih motif, checkout. Mau sekalian kemejanya buat Bapak? Masukkan dua-duanya
ke keranjang, checkout sekali. Ingat ya, belum ada COD — bayar lewat pilihan pembayaran di aplikasi."

**[20.23–20.25] Tanya-jawab — Daster Batik**
[baca komentar] "Kak [nama], untuk busui [isi: ada/tidak ada kancing depan — jangan dijawab kalau belum tahu]. Kak [nama]
tanya panas nggak — rayon ini adem dipakai di rumah, saya pegang ya biar kelihatan jatuhnya." [demo 10 detik]

**[20.25–20.26] Rekap untuk penonton baru**
"Buat yang baru masuk, selamat datang! Malam ini: kemeja batik cap pria Rp 149.000, paket isi 2 Rp 280.000 — keranjang
nomor 1. Daster batik rayon Rp 81.000 — keranjang nomor 2. Sebentar lagi kain batik tulis pewarna alam."

**[20.26–20.27] Hook — Kain Batik Tulis 2 m**
"Yang ini beda kelas: kain batik tulis, dikerjakan tangan, pewarna alam. Bulan ini memang cuma ada 5 lembar." [angkat kain perlahan]

**[20.27–20.31] Demo — Kain Batik Tulis 2 m**
"Panjangnya 2 meter, saya bentangkan." [bentangkan penuh] "Coba lihat bagian ini — garis cantingnya tidak sama persis,
karena ditulis tangan. Warnanya dari pewarna alam [isi: bahan pewarna, mis. dari toko], jadi warnanya lebih lembut."
[tunjukkan bagian depan dan belakang kain; batik tulis biasanya tembus ke belakang — **sebut hanya jika memang begitu**]
"Bisa dijahit jadi kemeja, kebaya, atau dipakai sebagai kain."

**[20.31–20.33] Harga — Kain Batik Tulis 2 m**
"Harganya Rp 650.000, tidak ada potongan karena ini dikerjakan tangan dan jumlahnya sedikit. Stoknya bulan ini 5 lembar,
dan yang tersisa di keranjang sekarang [stok nyata] — bisa Kakak lihat sendiri di layar." [pin produk no. 3]

**[20.33–20.35] CTA & cara checkout — Kain Batik Tulis 2 m**
"Kalau Kakak sudah lama cari batik tulis untuk acara penting, klik keranjang kuning nomor 3, checkout. Kami kemas dengan
rapi dan dikirim dari Pekalongan."

**[20.35–20.37] Tanya-jawab — Kain Batik Tulis 2 m**
[baca komentar] "Kak [nama] tanya asli tulis atau printing — ini batik tulis, [isi: bukti yang dimiliki toko, mis. proses
produksi sendiri]. Saya dekatkan lagi ke kamera ya." "Kak [nama] tanya cara cuci — [isi: cara perawatan dari toko]."

**[20.37–20.48] Putaran 2 — Kemeja Batik Cap Pria**
- *[20.37–20.38] Hook:* "Yang baru gabung dan cari kemeja batik adem buat kantor — pas banget, kita bahas lagi."
- *[20.38–20.42] Demo:* [pakaikan ke manekin/model bila ada, tunjukkan kerah dan jahitan] "Lihat kerahnya, jahitannya rapi."
- *[20.42–20.44] Harga:* "Normal Rp 185.000, live Rp 149.000, hemat Rp 36.000. Paket isi 2 Rp 280.000, jadi Rp 140.000 per potong." [pin produk no. 1]
- *[20.44–20.46] CTA:* "Keranjang kuning, nomor 1, pilih ukuran, checkout. Tanpa COD ya Kak."
- *[20.46–20.48] Tanya-jawab:* [jawab pertanyaan ukuran dari komentar]

**[20.48–20.57] Tanya-jawab bebas & rekap semua produk**
"Sekarang saya jawab semua pertanyaan yang tadi terlewat ya." [baca komentar dari atas] Di sela-sela, rekap: "Kemeja
Rp 149.000 (nomor 1), paket isi 2 Rp 280.000; daster Rp 81.000 (nomor 2); kain batik tulis Rp 650.000 (nomor 3), stok
[stok nyata]." [pin bergantian sesuai pertanyaan]

**[20.57–21.00] Penutup**
"Terima kasih Kak sudah nemenin Batik Lestari malam ini! Harga live berlaku sampai live ini selesai, jadi yang masih di
keranjang, checkout sekarang ya. Semua pesanan dikirim dari Pekalongan. Live berikutnya [isi: hari & jam live berikutnya].
Follow akun kami biar dapat notifikasi. Sampai jumpa!"

### Jawaban cepat pertanyaan penonton
| Pertanyaan | Jawaban |
|---|---|
| "Harganya berapa?" | "Kemeja Rp 149.000 selama live Kak [nama], normalnya Rp 185.000 — keranjang nomor 1. Daster Rp 81.000 — nomor 2." |
| "Ukuran kemejanya?" | "[isi: tabel ukuran]. Sebut tinggi & berat badan, saya bantu pilihkan." |
| "Daster muat LD berapa?" | "Allsize, lingkar dada 120 cm, Kak." |
| "Bahannya panas nggak?" | "Kemeja katun primisima, daster rayon. Saya dekatkan ke kamera ya biar kelihatan." |
| "Bisa COD?" | "Maaf Kak, belum ada COD. Pilihan pembayaran muncul saat checkout." |
| "Kapan dikirim?" | "Pesanan dikirim setiap hari dari Pekalongan." |
| "Bisa retur/tukar?" | "Retur bisa kalau salah kirim, wajib video unboxing ya Kak." |
| "Ongkirnya berapa?" | "Ongkir dihitung otomatis sesuai alamat saat checkout." |
| "Batik tulisnya asli?" | "[isi: fakta dari toko]. Detail ada di deskripsi produk." |
| "Mahal amat kain tulisnya" | "Makasih masukannya Kak. Ini dikerjakan tangan dan pewarna alam. Kalau mau yang lebih terjangkau, ada kemeja batik cap Rp 149.000." |

### Catatan untuk host
- Angka `[stok nyata]` dibaca dari layar, **jangan dikarang**. Untuk kain tulis, "5 lembar bulan ini" boleh diucapkan karena itu fakta dari pemilik.
- Jangan ucapkan "diskon 15%" untuk daster — potongan setelah pembulatan ±14% (Rp 14.000).
- Hal yang perlu dilengkapi: tabel ukuran kemeja, panjang daster, daftar motif, cara perawatan, bukti/penjelasan batik tulis, jadwal live berikutnya.
- Asumsi: nama host `[nama host]`; tidak ada voucher/bonus; CTA hanya lewat keranjang TikTok (tidak ke WA/transfer).

## Catatan penguji
- **Angka diverifikasi independen** (python terpisah, `math.ceil`): 185.000 − 149.000 = 36.000 → 19,46% → 19% ✔;
  280.000 ÷ 2 = 140.000 ✔; 2 × 185.000 − 280.000 = 90.000 ✔; 95.000 × 85% = 80.750 → dibulatkan ke atas ke 1.000 = 81.000 ✔,
  hemat 14.000 = 14,7% → 14% ✔. Rundown: total 60 menit, jam benar ✔.
- **Urgensi jujur:** hanya "5 lembar bulan ini" (fakta dari pengguna) dan `[stok nyata]`; tidak ada hitung mundur palsu,
  "tinggal 3", atau jumlah pembeli karangan. CTA ke keranjang, bukan WA.
- **Bagus:** script mencegah host mengucapkan "diskon 15%" yang sebenarnya 14%; naskah berupa kalimat siap ucap dengan arahan aksi.
  Data yang tidak diberikan (ukuran kemeja, cara cuci, bukti batik tulis) dibiarkan `[isi: …]`.
- **Kurang:** (1) rekap untuk penonton baru pertama baru di menit ke-25 dan berikutnya baru menit ke-48 (celah 22 menit), padahal
  docstring script menjanjikan "setiap ±15 menit"; (2) `hitung_promo.py` tidak bisa dipakai untuk produk tanpa promo — wajar,
  tetapi SKILL.md tidak menyebut bahwa produk tanpa promo cukup ditulis manual; (3) persen "±19%" memakai tanda "±" padahal sudah
  dibulatkan ke bawah — lebih jujur "hampir 20%" atau "19%".
