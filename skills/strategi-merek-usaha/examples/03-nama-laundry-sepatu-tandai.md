# Contoh 3: Nama dengan TANDAI (mirip merek dan arti buruk)

**Input:** "Nama untuk jasa cuci sepatu di Malang. Yang sudah ada: Kicks Clean, Sneakers Cleaning Malang, Shoe Care."
Nilai manual dan hasil (`python3 scripts/skor_nama.py nama.csv --merek "Kicks Clean, Sneakers Cleaning Malang, Shoe Care"`):
```
 #  Nama                      Skor  Huruf Suku  Status / catatan
 1  Sol Sehat                 86.0      8    3  layak dicek
 2  Kilap Sepatu              81.0     11    5  layak dicek
 3  Kicks Klinik              76.0     11    3  layak dicek; ejaan: 3 konsonan berturut
 4  Kicksclean                71.0     10    3  TANDAI: terlalu mirip 'Kicks Clean'; ...
 5  Shoe Spa Arema            70.0     12    6  layak dicek
 6  Sepatu Kinclong Malang    68.0     20    7  layak dicek; ejaan: 3 konsonan berturut
 7  Jamban Sneakers           57.0     14    5  TANDAI: arti/konotasi negatif
SETARA: 'Sol Sehat' dan 'Kilap Sepatu'
```
**Jawaban agent:** "Kicksclean" tinggal spasinya berbeda dari "Kicks Clean", jadi tidak saya rekomendasikan. "Jamban Sneakers" saya tandai karena kata "jamban" bernuansa negatif untuk jasa kebersihan. "Sol Sehat" dan "Kilap Sepatu" setara; "Kilap Sepatu" terdengar umum, jadi kemungkinan banyak yang memakai (perlu cek). "Shoe Spa Arema" dihitung 6 suku kata karena nama Inggris dihitung kira-kira; uji ucap tetap perlu. Cek domain, handle, dan PDKI (kelas 37 atau kelas jasa lain yang sesuai, tanyakan konsultan) **belum dilakukan**.
