# Contoh 01 - Rekap multi-kanal (katering harian fiktif "Dapur Bu Rini")
Data fiktif di `examples/data/` (semua nama, nomor, dan alamat fiktif).

> **Disegarkan ke v1.0.12 (2026-10-16):** hasil di bawah adalah keluaran ulang `scripts/olah_masukan.py` v1.0.12 dengan perintah dan data yang sama (sebelumnya ditulis dengan v1.0.1), dan `examples/data/anonim-2026-09.csv` dibuat ulang dari perintah yang sama. Perubahan utama: baris sistem WhatsApp tanpa tanggal ("Pesan ini dihapus") tidak lagi membuang pesan pelanggan di atasnya, sehingga **52 masukan** (dulu 51), **WhatsApp 13** (dulu 12), **keluhan Pengiriman 10 = 19,2%** (dulu 9 = 17,6%), dan **keluhan WhatsApp tanpa balasan 5 dari 7**. Bagian baru sejak v1.0.9–1.0.10 (sentimen per kanal, kalimat ringkasan siap salin, respons staf, rincian keamanan per jenis) ikut tampil. Ini penyegaran contoh, bukan uji baru.

Perintah:
```
python3 scripts/olah_masukan.py examples/data/chat-wa.txt=WhatsApp examples/data/ulasan-shopee.csv=Shopee \
  examples/data/komentar-instagram.txt=Instagram examples/data/survei-pelanggan.csv=Survei --staf "Admin" \
  --simpan-anonim examples/data/anonim-2026-09.csv
```
Hasil script apa adanya (nomor HP, email, alamat, dan nama di data asli sudah tidak muncul):

---
# Rekap Masukan Pelanggan (52 masukan)

Sumber chat-wa.txt (WhatsApp): chat WhatsApp
Sumber ulasan-shopee.csv (Shopee): CSV 26 baris (26 berisi jawaban); kolom teks: "Ulasan"; nilai: "Rating" (skala 1-5); tanggal: "Tanggal" (dibaca hari/bulan)
Sumber komentar-instagram.txt (Instagram): teks tempelan
Sumber survei-pelanggan.csv (Survei): CSV 4 baris (4 berisi jawaban); kolom teks: "Apa yang perlu diperbaiki?", "Yang paling disukai"; nilai: -; tanggal: "Tanggal" (dibaca hari/bulan)
Kanal: Shopee 26, WhatsApp 13, Survei 8, Instagram 5
Sentimen: positif 23 (44.2%), netral 7 (13.5%), negatif 22 (42.3%)
Sentimen per kanal: Shopee: positif 13, netral 2, negatif 11; WhatsApp: positif 4, netral 2, negatif 7; Survei: positif 4, netral 1, negatif 3; Instagram: positif 2, netral 2, negatif 1
Per bulan: 2026-08: 12, 2026-09: 35; 5 tanpa tanggal
Tidak dihitung: pesan staf 3, pesan sistem/media 2

## Kalimat ringkasan siap salin (angka sudah dihitung script - SALIN apa adanya, jangan hitung/tulis ulang)

- Total 52 masukan dari Shopee 26, WhatsApp 13, Survei 8, Instagram 5.
- Keluhan tanpa balasan (WhatsApp): 5 dari 7 keluhan (71,4%); pesan tanpa balasan: 10 dari 13 pesan (76,9%).
- Sentimen per kanal: Shopee: positif 13, netral 2, negatif 11; WhatsApp: positif 4, netral 2, negatif 7; Survei: positif 4, netral 1, negatif 3; Instagram: positif 2, netral 2, negatif 1.
- Pengiriman / ketepatan waktu: 10 keluhan (19,2% dari semua masukan; prioritas Segera).
- Kemasan / packing: 6 keluhan (11,5% dari semua masukan; prioritas Segera).
- Rasa / cita rasa: 4 keluhan (7,7% dari semua masukan; prioritas Segera).
- Keamanan produk (benda asing, basi, sakit): 3 keluhan (5,8% dari semua masukan; prioritas Segera); rincian: hewan/serangga 1, benda asing 2.
- Porsi / ukuran / size: 3 keluhan (5,8% dari semua masukan; prioritas Bulan ini).
- Ketepatan pesanan: 2 keluhan (3,8% dari semua masukan; prioritas Pantau).

## Respons staf / penjual

- WhatsApp (chat WhatsApp): 3 dari 13 masukan dibalas <= 24 jam; keluhan TANPA balasan: 5 dari 7
  - belum dibalas: "Kemarin sambalnya kurang, porsi nasinya juga sedikit"
  - belum dibalas: "Kotak nasinya bocor, kuah sayur tumpah ke mana-mana, kecewa"
  - belum dibalas: "Ada rambut di lauknya, jorok banget. Tolong diperiksa"
  - belum dibalas: "Harga naik ya? Agak mahal sekarang, ongkir juga"
  - belum dibalas: "Kurir telat lagi, nunggu lama. Tolong dibenahi"

## Isu teratas (skor = jumlah keluhan x dampak 1-5) - KANDIDAT, verifikasi tiap tema

| # | Tema | Keluhan (% dari semua) | Pujian | Saran | Dampak | Skor | Tren | Kanal | Prioritas |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Pengiriman / ketepatan waktu | 10 (19.2%) | 4 | 2 | 3 | 30 | naik (+3.3 poin) | Instagram, Shopee, Survei, WhatsApp | Segera |
| 2 | Kemasan / packing | 6 (11.5%) | 4 | 0 | 3 | 18 | naik (+6.0 poin) | Shopee, Survei, WhatsApp | Segera |
| 3 | Rasa / cita rasa | 4 (7.7%) | 14 | 0 | 4 | 16 | turun (-11.0 poin) | Shopee | Segera |
| 4 | Keamanan produk (benda asing, basi, sakit) | 3 (5.8%) | 0 | 0 | 5 | 15 | turun (-2.6 poin) | Shopee, WhatsApp | Segera |
| 5 | Porsi / ukuran / size | 3 (5.8%) | 0 | 0 | 3 | 9 | turun (-2.6 poin) | Shopee, Survei, WhatsApp | Bulan ini |
| 6 | Ketepatan pesanan | 2 (3.8%) | 0 | 0 | 4 | 8 | keluhan terlalu sedikit | Shopee, WhatsApp | Pantau |
| 7 | Harga / ongkir | 3 (5.8%) | 3 | 1 | 2 | 6 | keluhan terlalu sedikit | Instagram, Shopee, WhatsApp | Bulan ini |
| 8 | Waktu tunggu / jadwal / antrean | 2 (3.8%) | 0 | 0 | 3 | 6 | keluhan terlalu sedikit | Shopee, WhatsApp | Pantau |
| 9 | Kualitas produk / sesuai foto | 1 (1.9%) | 0 | 0 | 4 | 4 | keluhan terlalu sedikit | Shopee | Pantau |
| 10 | Kebersihan | 1 (1.9%) | 0 | 0 | 3 | 3 | keluhan terlalu sedikit | WhatsApp | Pantau |

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
**Waktu tunggu / jadwal / antrean** (keluhan)
- "Nunggu lama, kurir telat, nasi dingin"
- "Kurir telat lagi, nunggu lama. Tolong dibenahi"
**Kualitas produk / sesuai foto** (keluhan)
- "Nasi hambar dan lauk dingin, tidak sesuai foto"
**Kebersihan** (keluhan)
- "Ada rambut di lauknya, jorok banget. Tolong diperiksa"

## Saran & permintaan

**Pengiriman / ketepatan waktu** (2)
- "Kak [nama] mau tanya, boleh tidak tambah menu vegetarian? Semoga ada paket tanpa daging"
- "Semoga ada paket hemat untuk kantor, hubungi saya di [email]"
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

Tidak terklasifikasi: 4 masukan (2 tanpa tema + 0 bernada keluhan tetapi tidak masuk tabel keluhan + 2 bertema tetapi nadanya belum terbaca). Di antaranya 0 bernada keluhan - WAJIB dibaca & dimasukkan ke tema yang tepat (lewat tema.json atau koreksi bertanda).
Tanpa tema terdeteksi: 2 (3.8%). Kata teratas: mantap, sambal

Tanpa tema / bertema tanpa nada (netral) - bisa keluhan tersirat, baca:
- [tema: pengiriman] "Halo kak, kirim ke [alamat] ya, hubungi [hp]"
- [tema: harga, porsi_ukuran] "Porsi kecil untuk harga segitu"
- "Mantap, terima kasih"
- "Sambal mantap"

Catatan: hasil ini SARINGAN PERTAMA dari kata kunci. Baca kutipan tiap tema & koreksi lewat tema.json. Nama, nomor HP, dll. sudah disamarkan otomatis (tidak sempurna - baca ulang).

---
## Verifikasi agent (contoh catatan metode) - SEMUA tema dibaca, bukan hanya angka
*(Ditulis ulang 2026-10-16 untuk keluaran v1.0.12 di atas.)*
- Baris "Sumber" dicek dulu: kolom teks Shopee = "Ulasan", survei = 2 kolom pertanyaan, tanggal dibaca hari/bulan, tidak ada PERINGATAN. Aman dilanjutkan.
- WhatsApp 13 pesan pelanggan (3 pesan staf dan 2 pesan sistem/media tidak dihitung). Baris "Pesan ini dihapus" tanpa tanggal di akhir ekspor tidak lagi menelan pesan di atasnya, jadi keluhan 22/09 "Kurir telat lagi, nunggu lama. Tolong dibenahi" kini terhitung.
- "Pengiriman" 10 keluhan: semua kutipan memang soal telat/kurir. "Pesanan salah kirim" masuk Ketepatan pesanan saja (tidak dobel). 2 "saran" Pengiriman (menu vegetarian, paket hemat kantor) sebenarnya permintaan menu/paket, bukan pengiriman -> di laporan ditulis di bawah "Varian / menu" dan dicatat di Catatan metode (bisa juga dikoreksi lewat `--koreksi`); angka keluhan tidak terpengaruh.
- "Rasa" 4 keluhan: 2 di antaranya "nasi dingin" karena datang telat -> akar masalahnya pengiriman; di laporan ditulis sebagai satu isu "telat -> nasi dingin" (angka script tidak diubah, penjelasan ditulis di Catatan metode). Keluhan rasa murni = 2 ("hambar").
- "Waktu tunggu" 2 keluhan ("nunggu lama") ikut akar masalah pengiriman yang sama.
- "Kebersihan" 1 dan "Keamanan produk" 3 berasal dari laporan rambut/ulat yang sama -> dilaporkan sekali sebagai isu keamanan (Segera), rincian per jenis: benda asing 2, hewan/serangga 1.
- "Porsi" 3 keluhan sesuai kutipan (sambal kurang, nasi sedikit, porsi kurang banyak).
- Perlu dibaca (4): "Porsi kecil untuk harga segitu" = keluhan porsi/harga tersirat -> disebut di Catatan metode (angka tabel tetap angka script kecuali dikoreksi lewat `--koreksi`); "kirim ke [alamat]" = pesanan biasa, bukan masukan; "Mantap, terima kasih" dan "Sambal mantap" = pujian umum.
- Respons staf: 5 dari 7 keluhan WhatsApp belum dibalas -> masuk daftar tindakan pertama (draf balasan disiapkan, dikirim manusia).
- Tren: Agustus 12 vs September 35 masukan; arah "Pengiriman naik +3,3 poin" dibaca hati-hati (Agustus sedikit). Tema dengan < 3 keluhan tidak diberi tren.
