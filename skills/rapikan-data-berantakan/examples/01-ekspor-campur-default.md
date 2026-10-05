# 01. Ekspor pelanggan campur (kerjakan dulu, tanya di akhir)

**Berkas:** `examples/data-contoh.csv` (40 baris data fiktif: nama, nomor, dan transaksi karangan, bukan orang nyata).
**Pesan pengguna:** "Ini ekspor pelanggan toko online saya, berantakan banget. Tolong rapikan."

**Cara dijalankan (untuk penguji):** `python3 scripts/rapikan.py examples/data-contoh.csv`

## Balasan yang diharapkan (utuh di chat)

Bagian daftar di bawah disalin apa adanya dari keluaran alat (versi 1.0.1); angka dan nomor baris tidak dihitung sendiri oleh agent.

Selesai dirapikan: 40 baris data; di file bersih: 40 baris, tidak ada baris yang dihapus.
- Nomor HP diseragamkan ke format 62: 34
- Telepon rumah/kantor (bukan WhatsApp; dipisah ke kolom _telepon_rumah, tidak ada di kolom HP): 1 sel
  - baris 24 "(021) 555-0123"
- Sel berisi lebih dari satu nomor: 1 sel
  - baris 23 "0831 4444 5555 / 0896 6666 7777" -> dipakai sebagai HP: 6283144445555; nomor lain dicatat: 6289666667777
- Tanggal diseragamkan ke YYYY-MM-DD: 37
- Tanggal ambigu (bisa hari/bulan atau bulan/hari; dibaca hari/bulan kecuali ada bukti lain): 8 -> baris 2, 5, 6, 11, 12, 13, 14, 41
- Nominal rupiah jadi angka: 34
- Nama/produk/kota dirapikan huruf dan spasinya: 7
- Baris kembar persis (semua kolom sama): 2 grup
  - baris 13 & 14 (Hendra Gunawan)
  - baris 15 & 16 (Toko Maju Jaya)
- Nomor HP sama tetapi nama beda (belum tentu orang yang sama, TIDAK digabung): 3 kelompok
  - baris 2, 3, 4, 5, 6 (Bpk. Budi Santoso / Budi Santosa / Budi Santoso / Santoso Budi)
  - baris 9 & 10 (Muh. Rizal Pratama / Muhammad Rizal Pratama)
  - baris 11 & 12 (Dewi Lestari / Dewi Lestary)
- Nama mirip yang menunggu keputusan: 4 kelompok
  - no. 1: "Budi Santoso" (baris 2 & 3) / "Bpk. Budi Santoso" (baris 4) / "Budi Santosa" (baris 5) / "Santoso Budi" (baris 6)
  - no. 2: "Muh. Rizal Pratama" (baris 9) / "Muhammad Rizal Pratama" (baris 10)
  - no. 3: "Dewi Lestari" (baris 11) / "Dewi Lestary" (baris 12)
  - no. 4: "Yogyakarta" (baris 19 & 21) / "Jogja" (baris 20)
- Sel tidak bisa diperbaiki (dibiarkan apa adanya): 9 sel di 8 baris
  - baris 17 kolom Tanggal Order "31/02/2026": tanggal tidak ada di kalender (mis. 31 Februari)
  - baris 18 kolom No HP "0812-ABC-5555": ada huruf di dalam nomor
  - baris 19 kolom No HP "6.28123E+11": nomor berubah jadi notasi ilmiah oleh Excel (digitnya sudah hilang); ekspor ulang dengan kolom bertipe teks
  - baris 20 kolom No HP "0812345": panjang nomor HP tidak wajar (6 angka setelah 0/62; wajar 9-12)
  - baris 21 kolom No HP "+60 12 345 6789": tampaknya nomor luar negeri (bukan +62)
  - baris 21 kolom Total Bayar "abc": bukan angka rupiah yang dikenali
  - baris 31: baris hampir kosong: hanya berisi nomor urut
  - baris 32: jumlah kolom kurang (6 dari 7); dilengkapi kosong
  - baris 33: jumlah kolom berlebih; kemungkinan koma/pemisah di dalam isi sel yang tidak diberi tanda kutip

**Contoh perbaikan**
| Isi | Sebelum | Sesudah |
|---|---|---|
| Nomor HP | +62 812-3450-0101 | 6281234500101 |
| Nomor HP | 0812.3450.0101 | 6281234500101 |
| Tanggal | 7 Okt 2026 | 2026-10-07 |
| Tanggal | Senin, 5 Oktober 2026 | 2026-10-05 |
| Harga | Rp1.250.000,- | 1250000 |
| Harga | 1,5jt / 150rb | 1500000 / 150000 |
| Nama | budi santoso | Budi Santoso |
| Nama | siti  rahmawati (spasi ganda) | Siti Rahmawati |

**Perlu keputusan Anda**
1. Nama yang tampaknya sama (kelompok no. 1-4 di daftar atas). Mau disatukan? Usul saya: nama yang paling sering muncul. "Budi Santosa" (baris 5) bisa saja orang lain; ini tebakan dari nomor HP yang sama.
2. Dua pasang baris kembar persis (baris 13 & 14, baris 15 & 16). Sisakan satu per pasang?
3. Telepon rumah di baris 24 ("(021) 555-0123") tidak saya masukkan ke kolom HP karena bukan WhatsApp. Dikosongkan saja, atau Anda minta nomor WA-nya ke pelanggan?

**Asumsi:** tanggal "05/10/2026" dan 7 lainnya saya baca 5 Oktober (hari/bulan); harga "Rp 1.500,50" dibulatkan ke 1501; 2 isian "-"/"N/A" dikosongkan; 1 harga "gratis" dicatat 0; 1 jam dibuang dari tanggal.

Mau file bersihnya? Balas "kirim file".

## Verifikasi angka (independen dari script)
Dihitung terpisah dari data mentah:
- HP: 39 sel terisi, 4 tidak bisa diperbaiki, 1 telepon rumah (baris 24) dipisah dari kolom HP -> 34 diubah (tidak ada yang sudah berformat 628).
- Tanggal: 39 terisi, 1 tidak valid (31/02) -> 38 terbaca; 1 sudah ISO (baris 3) -> 37 diubah.
- Harga: 39 terisi, 2 placeholder jadi kosong, 1 "abc" -> 36 terbaca; 2 sudah bilangan polos (baris 3 dan 10) -> 34 diubah.
- Tanggal ambigu (hari dan bulan sama-sama <= 12 dan berbeda): baris 2, 5, 6, 11, 12, 13, 14, 41 = 8.
- 5 Oktober 2026 memang hari Senin (cocok dengan "Senin, 5 Oktober 2026").
- Uji otomatis `tests/uji_rapikan.py` memeriksa nilai per baris dari data ini.
