# 01 — 160 ulasan toko kaos dari CSV Shopee (S1, normal)

## Skenario
Seller fashion kecil mengirim file ekspor ulasan 3 bulan (160 baris) berisi kolom `Nama Pembeli, Produk, Tanggal, Rating, Ulasan`. Data uji dibuat penguji. Isinya bahasa gaul, singkatan, sarkasme ("Mantap, 2 minggu baru nyampe"), negasi ("ga ada yang rusak"), ulasan campur pujian dan keluhan, satu ulasan Sunda, satu ulasan Inggris, emoji saja, ulasan kosong, dan data pribadi pembeli (nama, nomor HP `0812-0000-xxxx`, email fiktif, nomor pesanan, resi, @username).

Cuplikan 5 baris pertama file:
```
Nama Pembeli,Produk,Tanggal,Rating,Ulasan
Siti Fiktif,Kemeja Linen,2026-07-11,1,pengirimannya lama bgt. adminnya jutek
Dewi Sampel,Kaos Oversize,2026-09-12,3,packing rapi tapi paket telat seminggu
Joko Rekaan,Kemeja Linen,2026-08-20,5,"langganan pokoknya, size nya sesuai size chart"
Siti Fiktif,Kemeja Linen,2026-09-20,5,"real pict kak, packingnya aman pake bubble wrap"
```

## Input pengguna
> Ini ulasan toko aku 3 bulan terakhir dari Shopee, filenya ulasan.csv. Keluhan paling banyak apa sih? Terus apa yang harus aku benahi duluan?

## Langkah agent (mengikuti SKILL.md)
1. `python3 scripts/olah_ulasan.py ulasan.csv`: kolom terdeteksi otomatis (`Ulasan`, `Rating`, `Produk`, `Tanggal`), kolom `Nama Pembeli` diabaikan.
2. Verifikasi tema (langkah 3): membaca `contoh` tiap tema, `--detail-tema k_respons`, `--detail-tema k_pengiriman`, dan daftar `perlu_dibaca_agent` (7 bintang tinggi dengan keluhan, 3 bintang rendah tanpa keluhan terdeteksi, 6 belum terklasifikasi).
3. Koreksi tema dicatat di Catatan metode. Hitungan dilakukan dari daftar id ulasan hasil `--detail-tema`, bukan tebakan.

## Output

# Analisis Ulasan — Toko Kaos & Kemeja (Juli–September 2026, 160 ulasan)

## Ringkasan cepat
- Rata-rata **3,88★**. 67,5% ulasan positif (4–5★) dan **18,8% negatif (1–2★)**. Rata-rata turun tiap bulan: Juli 4,07 → Agustus 3,84 → September 3,71.
- Keluhan paling merusak bintang adalah **pengiriman atau proses kirim lambat**: 15 ulasan (9,4%), rata-rata 2,07★. Dari 15 itu, 7 menyebut "pesanan diproses lama, 5 hari baru dikirim", jadi penyebabnya ada di **proses toko**, bukan hanya kurir.
- Pujian terbanyak: **ukuran pas** (33 ulasan), **sesuai foto** (31) dan **pengiriman cepat** (29). Ini bahan konten testimoni.
- **Tindakan paling penting minggu ini:** tetapkan jam potong kirim (pesanan yang masuk sebelum 15.00 dikirim hari itu juga) dan tulis estimasi proses di deskripsi produk dan balasan chat otomatis.

## Sebaran bintang
| Bintang | Jumlah | % |
|---|---|---|
| 5★ | 81 | 50,6% |
| 4★ | 27 | 16,9% |
| 3★ | 22 | 13,8% |
| 2★ | 12 | 7,5% |
| 1★ | 18 | 11,2% |
| **Total** | **160** | rata-rata **3,88★** |

Positif (4–5★): 108 (67,5%) · Netral (3★): 22 (13,8%) · Negatif (1–2★): 30 (18,8%).
Per produk: Kaos Oversize 94 ulasan, rata-rata 4,06★. **Kemeja Linen 66 ulasan, rata-rata 3,62★**, dengan 16 ulasan negatif.

## Keluhan teratas (setelah diverifikasi agent)
| # | Keluhan | Ulasan (% dari 159 ulasan berteks) | Rata-rata ★ | Contoh kutipan (tanpa nama) | Area |
|---|---|---|---|---|---|
| 1 | Pengiriman/proses kirim lambat | 15 (9,4%) | 2,07 | "pesanan diproses lama, 5 hari baru dikirim" · "Mantap, 2 minggu baru nyampe" (sarkas, 1★) | Proses kirim toko + kurir |
| 2 | Salah kirim / barang kurang | 10 (6,3%) | 2,00 | "pesen 3 dateng 2, kurang satu" · "luar biasa, pesen hitam dikirim putih" (sarkas) | Packing (gudang) |
| 3 | Kualitas buruk / cacat | 10 (6,3%) | 2,10 | "sablon luntur sekali cuci" · "jahitan lepas pas dicuci" | Produk/penjahit |
| 4 | Respons admin lambat/jutek | 8 (5,0%) | 1,75 | "chat ga dibales" · "adminnya jutek" | Layanan (admin) |
| 5 | Tidak sesuai deskripsi/foto | 8 (5,0%) | 2,00 | "warnanya beda sama foto" | Listing & foto |
| 6 | Ukuran tidak pas | 8 (5,0%) | 2,88 | "size L kayak M" · "kebesaran padahal udah ikut size chart" | Produk & tabel ukuran |
| 7 | Kemasan kurang aman | 5 (3,1%) | 3,40 | "kemasan basah kena hujan" · "plastiknya sobek pas nyampe" | Packing |
| – | Retur dipersulit, harga mahal, bau apek | masing-masing 1 | – | "refund dipersulit, udah komplain 3x ga ditanggepin" | Pantau |

Sinyal dini: **7 ulasan bintang 4–5 tetap mengeluh**, misalnya "packing rapi. paket telat seminggu" (4★) dan "real pict kak cuma kemasan basah kena hujan" (4★). Pembeli ini masih puas, tapi mulai terganggu.

## Pujian teratas
| # | Pujian | Ulasan (%) | Contoh kutipan |
|---|---|---|---|
| 1 | Ukuran pas / sesuai tabel ukuran | 33 (20,8%) | "ukurannya pas di badan" |
| 2 | Sesuai foto/deskripsi | 31 (19,5%) | "persis kayak di gambar" |
| 3 | Pengiriman cepat | 30 (18,9%) | "sehari langsung sampai" |
| 4 | Harga terjangkau/sepadan | 26 (16,4%) | "worth it sama harganya" |
| 5 | Kemasan rapi & aman | 26 (16,4%) | "packingnya aman pake bubble wrap" |
| 6 | Admin ramah & responsif | 25 (15,7%) | "admin ramah dan sabar jawab pertanyaan" |
| 7 | Kualitas bahan bagus | 25 (15,7%) | "bahannya adem bgt" · "sablonnya awet udah dicuci 5x" |
| 8 | Pembeli berulang | 22 (13,8%) | "udah ke-3 kali belanja disini" |

## Prioritas perbaikan
| Prioritas | Masalah | Bukti | Tindakan konkret | Ukuran keberhasilan |
|---|---|---|---|---|
| **Segera (minggu ini)** | Pesanan lama diproses | 15 ulasan, rata-rata 2,07★; 7 menyebut "5 hari baru dikirim" | Pemilik menetapkan jam potong 15.00. Admin memasang estimasi proses di deskripsi dan balasan otomatis. Pesanan dicek setiap pagi dan sore | Waktu proses ≤ 1 hari kerja; keluhan pengiriman < 5% ulasan bulan depan |
| **Segera** | Salah kirim / kurang isi | 10 ulasan, rata-rata 2,00★ | Buat checklist packing: cocokkan warna, ukuran dan jumlah dengan pesanan, lalu foto isi paket sebelum dilakban. Di jam sibuk, orang kedua mengecek ulang | 0 salah kirim dalam 2 minggu |
| **Segera** (murah) | Admin tidak membalas/jutek | 8 ulasan, rata-rata 1,75★ (terendah) | Pasang balasan otomatis dan jam operasional, siapkan template jawaban (skill `balas-chat-cs`), targetkan balasan < 1 jam di jam kerja | Performa chat di Seller Center naik; 0 keluhan "chat ga dibales" |
| **Bulan ini** | Sablon luntur, jahitan lepas, bahan tipis | 10 ulasan, rata-rata 2,10★ | Bawa kutipan ulasan ke penjahit/penyablon, uji cuci 3x per batch baru, QC 100% sebelum kirim untuk Kemeja Linen | Keluhan kualitas < 3% ulasan |
| **Bulan ini** | Warna beda dari foto & ukuran tidak pas | 8 + 8 ulasan | Foto ulang di cahaya siang tanpa filter (skill `foto-produk-brief`). Tambahkan tabel ukuran dalam cm dan keterangan "model 170 cm pakai L" | Keluhan "tidak sesuai" & ukuran masing-masing < 3% |
| **Pantau** | Kemasan basah/sobek; refund dipersulit | 5 + 1 ulasan | Beri plastik dobel untuk musim hujan. Tulis kebijakan retur singkat di deskripsi | Nol keluhan kemasan basah |

## Ide konten dari pujian
1. **Carousel IG + foto katalog Shopee**: Hook "Ukurannya beneran sesuai size chart?" berisi tabel ukuran dalam cm dan kutipan "size nya sesuai size chart". CTA: "Cek tabel ukuran di slide 3 sebelum checkout."
2. **Reels/TikTok 15 detik, ASMR packing**: Hook "Begini kaos kamu dikemas". Kutipan: "packingnya aman pake bubble wrap". CTA: "Order hari ini, dikirim hari ini sebelum jam 15.00". Pakai ini **hanya setelah jam potong benar-benar berjalan**.
3. **Carousel "Foto katalog vs kiriman pembeli"**: Kutipan "persis kayak di gambar". Foto dari pembeli hanya dipakai **dengan izin** pembeli, dan identitasnya diburamkan.
4. **Story "Kata pelanggan yang balik lagi"**: 3 kutipan, misalnya "udah ke-3 kali belanja disini" dan "sablonnya awet udah dicuci 5x". CTA: "Klik keranjang di bio."
5. (Edukasi dari keluhan) **Video "Cara pilih ukuran kaos oversize"**: menjawab keluhan "size L kayak M" tanpa membantah pembeli.

## Catatan metode
- 160 ulasan dibaca, 159 berteks (1 kosong), semuanya berbintang. Kolom nama pembeli diabaikan. Nomor HP, email, nomor pesanan, resi, @akun dan sapaan+nama di kutipan sudah disamarkan. Laporan ini tidak memuat identitas pembeli.
- **Koreksi tema oleh agent**, dicek dengan `--detail-tema`:
  - *Respons admin*: script menghitung 14. Enam di antaranya adalah kalimat "pesanan diproses lama…", dan kata "pesanan" terbaca sebagai "pesan/chat". Keenamnya dikeluarkan. "kurir kasar lempar paket" dipindah ke kemasan/kurir, dan "komplain 3x ga ditanggepin" ditambahkan, sehingga totalnya **8**.
  - *Pengiriman*: ditambah 2 ulasan (sarkasme "Mantap, 2 minggu baru nyampe" dan "resi … ga gerak2"), dari 13 menjadi **15**.
  - *Salah kirim*: ditambah 1 ulasan sarkas ("luar biasa, pesen hitam dikirim putih"). *Kualitas*: ditambah "resletingnya macet". *Ukuran*: ditambah "size L kayak M" dan ulasan Sunda "rada alit ukuranana" (agak kecil).
  - *Rasa*: dihapus, karena "baunya apek" pada kaos adalah keluhan bau, bukan rasa.
  - *Pujian*: ditambah ulasan Inggris "Good quality, fast delivery, will buy again" (kualitas, pengiriman, beli lagi), "bahan tebel ga nerawang" dan "ga terlalu tipis" (kualitas), serta "ga ada yang rusak… aman semua" (kemasan).
- Skor prioritas memakai bobot 1★=5 … 5★=1: pengiriman 59, salah kirim 40, kualitas 39, respons 34, tidak sesuai 32, ukuran 25, kemasan 13.
- Peringatan script: 15 teks ulasan sama persis dengan ulasan lain (ulasan pendek seperti "chat ga dibales"), tetap dihitung.
- Batasan: kamus tidak mengenali sarkasme. Karena itu semua ulasan bintang rendah tanpa keluhan terdeteksi sudah dibaca manual. Penyebab keterlambatan (toko vs kurir) adalah dugaan dari kutipan dan perlu dicek di data pesanan.

## Catatan penguji
- **Verifikasi independen (python terpisah):** sebaran 5★ 81, 4★ 27, 3★ 22, 2★ 12, 1★ 18 dan rata-rata 3,8813 cocok 100% dengan script (3,88). Persen sebaran cocok.
- Tema dibandingkan dengan label ground truth penguji. Setelah koreksi agent, hasil cocok untuk semua keluhan kecuali kualitas: ground truth 11, laporan 10, karena "harga mahal ga sebanding kualitas" sengaja tetap dicatat sebagai harga. **Tanpa koreksi agent, prioritas #1 salah** (script menaruh "Respons admin" di urutan teratas dengan skor 52, padahal skor sebenarnya 34). Penyebabnya bug regex: pola `(?:chat|pesan)\w*` di `k_respons` ikut menangkap kata "pesanan". Langkah verifikasi di SKILL.md menangkapnya karena kutipan contoh pertama tema respons jelas soal proses kirim. Namun `--kamus-tambahan` hanya bisa **menambah** pola, tidak bisa mengecualikan, jadi agent harus mengoreksi jumlah secara manual dari daftar id.
- Masking: nama di kolom, "Kak Rina", "mba Dewi", "bu Agus", nomor HP, resi, nomor pesanan dan @username tersamarkan. **Bocor sebagian:** email `uji.fiktif@contoh.id` terpotong menjadi `…email aku uji` di `klausa_cocok`, karena kalimat dipecah di titik sebelum disamarkan. Nama tanpa sapaan juga ikut ke `kata_teratas` (lihat HASIL-UJI).
- Bagus: sinyal bintang tinggi + keluhan, daftar "perlu dibaca", tabel prioritas dengan ukuran keberhasilan, dan ide konten yang patuh izin.
