# Contoh 01 - Rekap multi-kanal (katering harian fiktif "Dapur Bu Rini")
Data fiktif di `examples/data/` (semua nama, nomor, dan alamat fiktif). Perintah (script v1.0.1):
```
python3 scripts/olah_masukan.py examples/data/chat-wa.txt=WhatsApp examples/data/ulasan-shopee.csv=Shopee \
  examples/data/komentar-instagram.txt=Instagram examples/data/survei-pelanggan.csv=Survei --staf "Admin" \
  --simpan-anonim examples/data/anonim-2026-09.csv
```
Hasil script apa adanya (nomor HP, email, alamat, dan nama di data asli sudah tidak muncul):

---
# Rekap Masukan Pelanggan (51 masukan)

Sumber chat-wa.txt (WhatsApp): chat WhatsApp
Sumber ulasan-shopee.csv (Shopee): CSV 26 baris (26 berisi jawaban); kolom teks: "Ulasan"; nilai: "Rating" (skala 1-5); tanggal: "Tanggal"
Sumber komentar-instagram.txt (Instagram): teks tempelan
Sumber survei-pelanggan.csv (Survei): CSV 4 baris (4 berisi jawaban); kolom teks: "Apa yang perlu diperbaiki?", "Yang paling disukai"; nilai: -; tanggal: "Tanggal"
Kanal: Shopee 26, WhatsApp 12, Survei 8, Instagram 5
Sentimen: positif 23 (45.1%), netral 7 (13.7%), negatif 21 (41.2%)
Per bulan: 2026-08: 12, 2026-09: 34; 5 tanpa tanggal
Tidak dihitung: pesan staf 3, pesan sistem/media 2

## Isu teratas (skor = jumlah keluhan x dampak 1-5) - KANDIDAT, verifikasi tiap tema

| # | Tema | Keluhan (% dari semua) | Pujian | Saran | Dampak | Skor | Tren | Kanal | Prioritas |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Pengiriman / ketepatan waktu | 9 (17.6%) | 4 | 0 | 3 | 27 | stabil (+1.0 poin) | Instagram, Shopee, Survei, WhatsApp | Segera |
| 2 | Kemasan / packing | 6 (11.8%) | 4 | 0 | 3 | 18 | naik (+6.4 poin) | Shopee, Survei, WhatsApp | Segera |
| 3 | Rasa / cita rasa | 4 (7.8%) | 14 | 0 | 4 | 16 | turun (-10.8 poin) | Shopee | Segera |
| 4 | Keamanan produk (benda asing, basi, sakit) | 3 (5.9%) | 0 | 0 | 5 | 15 | turun (-2.5 poin) | Shopee, WhatsApp | Segera |
| 5 | Porsi / ukuran / size | 3 (5.9%) | 0 | 0 | 3 | 9 | turun (-2.5 poin) | Shopee, Survei, WhatsApp | Bulan ini |
| 6 | Ketepatan pesanan | 2 (3.9%) | 0 | 0 | 4 | 8 | keluhan terlalu sedikit | Shopee, WhatsApp | Pantau |
| 7 | Harga / ongkir | 3 (5.9%) | 3 | 1 | 2 | 6 | keluhan terlalu sedikit | Instagram, Shopee, WhatsApp | Bulan ini |
| 8 | Kualitas produk / sesuai foto | 1 (2.0%) | 0 | 0 | 4 | 4 | keluhan terlalu sedikit | Shopee | Pantau |
| 9 | Kebersihan | 1 (2.0%) | 0 | 0 | 3 | 3 | keluhan terlalu sedikit | WhatsApp | Pantau |
| 10 | Waktu tunggu / antrean | 1 (2.0%) | 0 | 0 | 3 | 3 | keluhan terlalu sedikit | Shopee | Pantau |

## Kutipan (sudah disamarkan)

**Pengiriman / ketepatan waktu** (keluhan)
- "Telat sekali, kurir susah dihubungi"
- "Telat lagi 90 menit, sangat mengecewakan"
- "Pesanan datang telat 2 jam, nasi sudah dingin. Kecewa"
**Kemasan / packing** (keluhan)
- "Kemasan bocor, kuah tumpah"
- "Kemasan penyok dan bocor lagi"
- "Kemasan kadang bocor"
**Rasa / cita rasa** (keluhan)
- "Pesanan datang telat 2 jam, nasi sudah dingin. Kecewa"
- "Nunggu lama, kurir telat, nasi dingin"
- "Nasi hambar dan lauk dingin, tidak sesuai foto"
**Keamanan produk (benda asing, basi, sakit)** (keluhan)
- "Ada ulat kecil di sayur! Tolong periksa dapurnya"
- "Ada rambut di dalam nasi, jijik. Tidak akan beli lagi"
- "Ada rambut di lauknya, jorok banget. Tolong diperiksa"
**Porsi / ukuran / size** (keluhan)
- "Porsi kurang banyak"
- "Kemarin sambalnya kurang, porsi nasinya juga sedikit"
- "Rasa mantap tapi porsi agak sedikit"
**Ketepatan pesanan** (keluhan)
- "Pesanan salah kirim, tertukar dengan orang lain"
- "Pesanan kurang satu kotak, salah hitung"
**Harga / ongkir** (keluhan)
- "[akun] harganya kok naik, jadi mahal"
- "Harga naik ya? Agak mahal sekarang, ongkir juga"
- "Rasa enak, harga agak mahal sekarang"
**Kualitas produk / sesuai foto** (keluhan)
- "Nasi hambar dan lauk dingin, tidak sesuai foto"
**Kebersihan** (keluhan)
- "Ada rambut di lauknya, jorok banget. Tolong diperiksa"
**Waktu tunggu / antrean** (keluhan)
- "Nunggu lama, kurir telat, nasi dingin"

## Saran & permintaan

**Harga / ongkir** (1)
- "Semoga ada paket hemat untuk kantor, hubungi saya di [email]"
**Varian / menu / pilihan** (3)
- "Kak [nama] mau tanya, boleh tidak tambah menu vegetarian? Semoga ada paket tanpa daging"
- "[akun] enak banget kak, kapan ada menu vegetarian?"
- "Tolong tambah menu sayur tanpa santan"

## Pujian teratas

- Rasa / cita rasa: 14 masukan
- Pengiriman / ketepatan waktu: 4 masukan
- Kemasan / packing: 4 masukan
- Layanan / respons admin & staf: 4 masukan
- Harga / ongkir: 3 masukan

## Perlu dibaca agent

Tanpa tema terdeteksi: 2 (3.9%). Kata teratas: mantap, sambal
- "Mantap, terima kasih"
- "Sambal mantap"

Catatan: hasil ini SARINGAN PERTAMA dari kata kunci. Baca kutipan tiap tema & koreksi lewat tema.json. Nama, nomor HP, dll. sudah disamarkan otomatis (tidak sempurna - baca ulang).

---
## Verifikasi agent (contoh catatan metode) - SEMUA tema dibaca, bukan hanya angka
- Baris "Sumber" dicek dulu: kolom teks Shopee = "Ulasan", survei = 2 kolom pertanyaan, tidak ada PERINGATAN. Aman dilanjutkan.
- "Pengiriman" 9 keluhan: semua kutipan memang soal telat/kurir. "Pesanan salah kirim" kini masuk Ketepatan pesanan saja (tidak dobel).
- "Rasa" 4 keluhan: 2 di antaranya "nasi dingin" karena datang telat -> akar masalahnya pengiriman; di laporan ditulis sebagai satu isu
  "telat -> nasi dingin" (angka script tidak diubah, penjelasan ditulis di Catatan metode). Keluhan rasa murni = 2 ("hambar").
- "Kebersihan" 1 dan "Keamanan produk" 3 berasal dari laporan rambut/ulat yang sama -> dilaporkan sekali sebagai isu keamanan (Segera).
- "Porsi" 3 keluhan sesuai kutipan (sambal kurang, nasi sedikit, porsi kurang banyak).
- 2 masukan tanpa tema ("Mantap, terima kasih", "Sambal mantap") = pujian umum; tema "sambal" dibuat lewat `tambah_kata` bila bertambah.
- Tren: Agustus 12 vs September 34 masukan; arah "Pengiriman stabil" dibaca hati-hati (Agustus sedikit). Tema dengan < 3 keluhan tidak diberi tren.
