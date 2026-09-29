# Contoh 01 - Rekap multi-kanal (katering harian fiktif "Dapur Bu Rini")
Data fiktif di `examples/data/` (semua nama, nomor, dan alamat fiktif). Perintah:
```
python3 scripts/olah_masukan.py examples/data/chat-wa.txt=WhatsApp examples/data/ulasan-shopee.csv=Shopee \
  examples/data/komentar-instagram.txt=Instagram examples/data/survei-pelanggan.csv=Survei --staf "Admin"
```
Hasil script apa adanya (nomor HP, email, alamat, dan nama di data asli sudah tidak muncul):

---
# Rekap Masukan Pelanggan (51 masukan)

Kanal: Shopee 26, WhatsApp 12, Survei 8, Instagram 5
Sentimen: positif 24 (47.1%), netral 7 (13.7%), negatif 20 (39.2%)
Per bulan: 2026-08: 12, 2026-09: 34; 5 tanpa tanggal
Tidak dihitung: pesan staf 3, pesan sistem/media 2

## Isu teratas (skor = jumlah keluhan x dampak 1-5)

| # | Tema | Keluhan (% dari semua) | Pujian | Saran | Dampak | Skor | Tren | Kanal | Prioritas |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Pengiriman / ketepatan waktu | 11 (21.6%) | 4 | 0 | 3 | 33 | turun (-4.4 poin) | Instagram, Shopee, Survei, WhatsApp | Segera |
| 2 | Kemasan / packing | 6 (11.8%) | 5 | 0 | 3 | 18 | naik (+6.4 poin) | Shopee, Survei, WhatsApp | Segera |
| 3 | Keamanan pangan / kebersihan | 3 (5.9%) | 0 | 0 | 5 | 15 | turun (-2.5 poin) | Shopee, WhatsApp | Segera |
| 4 | Porsi / ukuran | 3 (5.9%) | 0 | 0 | 3 | 9 | turun (-2.5 poin) | Shopee, Survei, WhatsApp | Bulan ini |
| 5 | Ketepatan pesanan | 2 (3.9%) | 0 | 0 | 4 | 8 | turun (-5.4 poin) | Shopee, WhatsApp | Pantau |
| 6 | Rasa / cita rasa | 2 (3.9%) | 15 | 0 | 4 | 8 | turun (-5.4 poin) | Shopee | Pantau |
| 7 | Harga / ongkir | 3 (5.9%) | 3 | 1 | 2 | 6 | naik (+5.9 poin) | Instagram, Shopee, WhatsApp | Bulan ini |
| 8 | Kualitas produk (barang) | 1 (2.0%) | 0 | 0 | 4 | 4 | naik (+2.9 poin) | Shopee | Pantau |

## Kutipan (sudah disamarkan)

**Pengiriman / ketepatan waktu** (keluhan)
- "Telat sekali, kurir susah dihubungi"
- "Telat lagi 90 menit, sangat mengecewakan"
- "Pesanan salah kirim, tertukar dengan orang lain"
**Kemasan / packing** (keluhan)
- "Kemasan bocor, kuah tumpah"
- "Kemasan penyok dan bocor lagi"
- "Kemasan kadang bocor"
**Keamanan pangan / kebersihan** (keluhan)
- "Ada ulat kecil di sayur! Tolong periksa dapurnya"
- "Ada rambut di dalam nasi, jijik. Tidak akan beli lagi"
- "Ada rambut di lauknya, jorok banget. Tolong diperiksa"
**Porsi / ukuran** (keluhan)
- "Porsi kurang banyak"
- "Kemarin sambalnya kurang, porsi nasinya juga sedikit"
- "Rasa mantap tapi porsi agak sedikit"
**Ketepatan pesanan** (keluhan)
- "Pesanan salah kirim, tertukar dengan orang lain"
- "Pesanan kurang satu kotak, salah hitung"
**Rasa / cita rasa** (keluhan)
- "Nasi hambar dan lauk dingin, tidak sesuai foto"
- "Lumayan, rasanya biasa saja, agak hambar"
**Harga / ongkir** (keluhan)
- "[akun] harganya kok naik, jadi mahal"
- "Harga naik ya? Agak mahal sekarang, ongkir juga"
- "Rasa enak, harga agak mahal sekarang"
**Kualitas produk (barang)** (keluhan)
- "Nasi hambar dan lauk dingin, tidak sesuai foto"

## Saran & permintaan

**Harga / ongkir** (1)
- "Semoga ada paket hemat untuk kantor, hubungi saya di [email]"
**Varian / menu / pilihan** (4)
- "Kak [nama] mau tanya, boleh tidak tambah menu vegetarian? Semoga ada paket tanpa daging"
- "[akun] enak banget kak, kapan ada menu vegetarian?"
- "Semoga ada paket hemat untuk kantor, hubungi saya di [email]"

## Pujian teratas

- Rasa / cita rasa: 15 masukan
- Kemasan / packing: 5 masukan
- Pengiriman / ketepatan waktu: 4 masukan
- Layanan / respons admin: 4 masukan
- Harga / ongkir: 3 masukan

## Perlu dibaca agent

Tanpa tema terdeteksi: 2 (3.9%). Kata teratas: mantap, sambal
- "Mantap, terima kasih"
- "Sambal mantap"

Catatan: tema dari kata kunci = kandidat; verifikasi lewat kutipan. Nama, nomor HP, dll. sudah disamarkan otomatis.


---
## Verifikasi agent (contoh catatan metode)
- "Pengiriman" 11 keluhan: satu kutipan ("Pesanan salah kirim") sebenarnya soal ketepatan pesanan, dihitung ganda karena kata "kirim"; pengiriman murni = 10.
- "Porsi" 3 keluhan sudah sesuai kutipan (sambal kurang, nasi sedikit); kata "kecil" pada "ulat kecil" tidak lagi salah masuk porsi.
- 2 masukan tanpa tema ("Mantap, terima kasih", "Sambal mantap") = pujian umum; tema baru "sambal" dibuat lewat tema.json bila jumlahnya bertambah.
- Tren Agustus (12 masukan) ke September (34 masukan) hanya indikatif karena Agustus dekat batas minimal.
