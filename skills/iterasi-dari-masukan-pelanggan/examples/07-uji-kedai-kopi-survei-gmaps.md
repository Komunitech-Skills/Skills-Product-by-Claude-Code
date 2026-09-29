# Uji 07 (normal 2) - Kedai kopi: Google Form (CSV ; , Windows-1252) + ulasan Google Maps tempelan
Penguji independen, 2026-09-29. Data fiktif.

## Data
- `survei-gform.csv`, disimpan **cp1252** (ada "café"), pemisah `;`, CRLF. Kolom: `Timestamp;Nama;No HP;Beri nilai 0-10 untuk kedai kami;
  Apa yang perlu kami perbaiki?;Menu apa yang ingin ditambah?` - 12 baris Agustus-September.
- `gmaps.txt` 10 ulasan tempelan dengan format bintang campur: `★★★★★ ...`, `5 | ...`, `2/5 - ...`.

Perintah: `python3 scripts/olah_masukan.py survei-gform.csv=Survei gmaps.txt=GoogleMaps --simpan-anonim anon.csv`

## Yang berjalan baik
- Encoding cp1252 terbaca (fallback latin-1), pemisah `;` dikenali, kolom Nama/No HP tidak dibaca.
- Ketiga format bintang tempelan terbaca (termasuk "2/5 - ...").
- Kolom judul bebas "Apa yang perlu kami perbaiki?" dikenali lewat aturan panjang teks.
- Hitungan diverifikasi ulang: semua cocok (n=21).

## Temuan
1. **Skala nilai 0-10 dibaca sebagai bintang 1-5 (KRITIS untuk survei).** `re.search(r"[1-5]")` mengambil digit pertama:
   nilai 10 -> bintang 1 ("ga ada, pertahankan!" jadi **negatif**), nilai 4 -> positif, nilai 5 -> bintang 5 sehingga "harga naik tp porsi
   sama aja" dihitung **pujian harga**, nilai 6/7/8/9 -> kosong. Sentimen survei jadi terbalik.
2. **"kurang + kata positif"** ("toiletnya kurang bersih", bintang 4) = 0 skor lalu ikut bintang -> **pujian kebersihan**. Pola "kurang enak/
   kurang bersih/kurang ramah" sangat umum; "kurang" perlu diperlakukan sebagai penegasi.
3. Kolom "Menu apa yang ingin ditambah?" (Oat milk, Less sugar option, Paket hemat pelajar) **tidak dibaca**, tanpa pemberitahuan
   (rata-rata panjang 7,9 < 8 karakter). Permintaan menu hilang dari laporan.
4. Tema bawaan tidak punya **tempat/fasilitas** (wifi, AC, parkir, toilet, colokan, musik) dan **waktu tunggu/antrean** - keluhan terbanyak
   kedai kopi. "AC kurang dingin" masuk **Pengiriman** (kata "dingin"); "antrian lama" masuk Stok; 7 dari 21 (33%) tanpa tema.
5. "Perlu dibaca agent" hanya menampilkan 5 contoh dari 7 tanpa tema; 2 sisanya ("AC mati, panas bgt", "harga naik...") hanya terlihat lewat JSON/CSV.
6. **Tren menyesatkan pada data kecil:** "Pengiriman naik +40 poin" dari 0/6 ke 2/5; "Keamanan turun -16,7 poin" padahal laporan rambut
   (Google Maps, tanpa tanggal) tidak ikut tren. Script tetap mencetak tren walau SKILL.md sendiri bilang < 30 masukan = arah saja.

## Label manual vs script
16 dari 21 masukan adalah keluhan. Script menandai keluhan bertema benar pada 6 (toilet kotor, pesanan tertukar, pelayan judes, menunggu 30 menit,
mahal, rambut) + 1 salah tema (AC -> pengiriman). Recall ≈ 38%. Isu #1 (rambut = Segera) benar; kelompok fasilitas (wifi 2, AC 2, parkir 2,
toilet 2, musik 1 = 9 keluhan, isu terbesar) **tidak muncul** sampai agent membuat tema.json.

## Nilai skenario: 5/10
