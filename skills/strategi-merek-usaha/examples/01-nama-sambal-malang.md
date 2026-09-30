# Contoh 1: Nama usaha sambal cobek rumahan (Malang)

**Input pengguna:** "Bantu cari nama untuk sambal cobek rumahan saya, Malang, dijual lewat Shopee dan WA, pembeli ibu-ibu dan anak kos. Merek yang saya tahu: Sambal Bu Rudy, Sambal Nusantara, ABC Sambal."

**Asumsi:** gaya ramah dan berbau Jawa Timur, 2-3 suku kata, tanpa Inggris.

**Nilai manual (pendapat, bukan fakta):** `nama.csv`
```
nama,aman_makna,khas,relevan
Sambal Mbok Jum,4,4,4
Sambel Pedas Nusantara,5,1,5
Sambalku,5,2,4
Sambal Ndeso,3,4,4
Pedas Kuy,4,3,3
Rasa Srikandi,5,4,2
Sambal Cobek Rina,5,4,5
Cabe Gendis,4,4,4
Sambal Bejo,2,3,3
Sambal Kencur Kita,5,3,5
```
Catatan arti: "ndeso" dan "bejo" (Jawa) punya nuansa; **perlu ditanyakan ke penutur asli** apakah cocok untuk pembeli sasaran. "Gendis" diduga berarti gula dalam bahasa Jawa: **perlu dikonfirmasi**.

**Hasil script** (`python3 scripts/skor_nama.py nama.csv --merek "Sambal Bu Rudy, Sambal Nusantara, ABC Sambal"`):
```
 #  Nama                      Skor  Huruf Suku  Status / catatan
 1  Cabe Gendis               86.0     10    4  layak dicek
 2  Pedas Kuy                 84.0      8    3  layak dicek
 3  Sambalku                  80.0      8    3  layak dicek
 4  Sambal Cobek Rina         79.0     15    6  layak dicek
 5  Rasa Srikandi             78.0     12    5  layak dicek
 6  Sambal Mbok Jum           78.0     13    4  layak dicek
 7  Sambal Ndeso              76.0     11    4  layak dicek
 8  Sambal Kencur Kita        74.0     16    6  layak dicek
 9  Sambal Bejo               68.0     10    4  layak dicek
10  Sambel Pedas Nusantara    60.0     20    8  layak dicek; mirip 'Sambal Nusantara' (80% ejaan)
SETARA: 'Cabe Gendis' dan 'Pedas Kuy' selisih <= 5 poin.
```

**Jawaban agent (ringkas):**
Tiga teratas: **Cabe Gendis** (86), **Pedas Kuy** (84), **Sambalku** (80). Cabe Gendis dan Pedas Kuy SETARA, jadi jangan diputuskan hanya dari skor. Pedas Kuy bernuansa gaul (cocok anak kos, kurang cocok untuk ibu-ibu?); Sambalku sangat umum (skor `khas` 2), kemungkinan banyak yang memakai.

Yang perlu kamu cek sendiri (semuanya **belum dicek**):
| Nama | Domain .id/.com | IG/TikTok | Nama toko Shopee | PDKI kelas 30 |
|---|---|---|---|---|
| Cabe Gendis | belum dicek | belum dicek | belum dicek | belum dicek |
| Pedas Kuy | belum dicek | belum dicek | belum dicek | belum dicek |
| Sambalku | belum dicek | belum dicek | belum dicek | belum dicek |
Uji ucap: kirim voice note "Cabe Gendis" ke 5 orang, minta ditulis. Langkah PDKI: `references/cek-merek-pdki.md`. Ini bukan nasihat hukum; bila ada nama mirip, tanyakan konsultan KI.
Mau saya buatkan tagline dan bio dari nama pilihanmu?
