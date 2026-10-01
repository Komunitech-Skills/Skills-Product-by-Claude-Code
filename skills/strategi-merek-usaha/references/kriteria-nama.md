# Kriteria Nama & Aturan Skor

## Kriteria yang dihitung script (skala 1-5)
| Kriteria | Aturan skor | Catatan |
|---|---|---|
| panjang (huruf tanpa spasi/simbol) | <3: 2; 3-8: 5; 9-10: 4; 11-12: 3; 13-15: 2; >15: 1 | Nama pendek mudah diingat dan muat di handle. |
| suku_kata | 2-3: 5; 4: 4; 1: 3; 5: 2; >=6: 1 | Tiap vokal = 1 suku kata; ai/au/oi dihitung 1; kata tanpa vokal (mis. KPK) dibaca per huruf. Nama Inggris dan singkatan bervokal kira-kira. |
| ejaan | Mulai 5; angka/simbol -2; huruf sama 3x berturut -1; 3 konsonan berturut (ng/ny/sy/kh/gh dihitung satu) -1; huruf q/x -1; minimum 1 | Ejaan aneh membuat pelanggan salah cari di marketplace. |
| kemiripan | Rasio kemiripan (difflib) tertinggi terhadap daftar merek pengguna, diambil yang lebih besar dari **ejaan** (huruf saja) dan **bunyi kira-kira** (c/q/ck→k, ph/v→f, z→s, x→ks, ee/ea→i, oo→u, y akhir→i, -s jamak setelah konsonan dibuang, huruf ganda dirapatkan): >=0,85: 1 (TANDAI); 0,75-0,84: 2; 0,65-0,74: 3; 0,50-0,64: 4; <0,50: 5. Nama yang memuat/dimuat merek (>=4 huruf), atau memuat semua kata khas merek (bunyinya), dianggap >=0,9 | "Kicks Klin" vs "Kick Clean" = sama bunyinya (TANDAI). Normalisasi bunyi hanya perkiraan; tetap uji ucap dan cek PDKI. Tanpa daftar merek: 3 "belum diperiksa". |
| kata Inggris buruk (tanda, bukan skor) | Nama/kata di nama yang ejaan atau bunyinya mirip (>= 0,85; kata < 5 huruf harus sama persis) dengan daftar kata Inggris berkonotasi buruk di script → TANDAI | Contoh: "Sneakuy" ~ "sneaky" (licik), "Dirtee" ~ "dirty". Daftar ringkas; arti di bahasa daerah & slang lain tetap dinilai manual lewat `aman_makna`. |

## Kriteria nilai manual (1-5, oleh agent bersama pengguna)
| Kriteria | 5 berarti | 1 berarti |
|---|---|---|
| aman_makna | Tidak ada arti negatif/lucu di bahasa Indonesia, daerah, slang, atau saat disingkat | Ada arti buruk/vulgar (nama TANDAI, tidak dipilih) |
| khas | Jelas beda dari pesaing yang dikenal | Sama/generik seperti banyak usaha lain |
| relevan | Langsung mengingatkan produk/manfaat | Tidak ada hubungan; perlu banyak penjelasan |

Kosong = 3 dan dicatat "belum dinilai".

## Bobot awal (jumlah 100)
panjang 10, suku_kata 10, ejaan 10, kemiripan 20, aman_makna 20, khas 15, relevan 15. Ubah lewat `--bobot`. Pemilik ingin nama yang unik? Naikkan `khas`. Ingin aman dari kemiripan? Naikkan `kemiripan`.

## Uji ucap (5 orang, 5 menit)
1. Ucapkan nama lewat voice note ke 5 orang berbeda usia/daerah. Minta mereka menuliskannya. Berapa yang benar?
2. Tanya: "Kamu bayangkan ini jual apa?"
3. Tanya: "Ada arti lain di daerahmu?"
4. Nama lolos bila >= 4 dari 5 benar mengeja dan tidak ada arti buruk.

## Pola nama untuk UMKM Indonesia
- Deskriptif + pembeda: "Sambal Cobek Rina", "Laundry Sepatu Kilap".
- Kata daerah/serapan yang maknanya dipastikan penutur asli.
- Gabungan dua kata pendek: "Cabe Gendis".
- Awalan/akhiran: -ku, Kita, Nusa. Hati-hati: pola ini sangat ramai, skor `khas` biasanya rendah.
- Hindari: angka acak, huruf ganda gaya ("Kopiii"), singkatan tanpa cerita, kata yang identik dengan merek besar.

## Menamai produk di bawah satu usaha
Pilih struktur: (a) nama induk + deskripsi ("Dapur Rina Sambal Bawang"), atau (b) tiap produk punya nama sendiri. Struktur (a) lebih murah dan mudah untuk usaha kecil.
