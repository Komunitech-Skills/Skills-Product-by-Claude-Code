# Skenario 6 (uji independen) — Input Tidak Lengkap

## Input pengguna
"bikin tulisanku nggak kayak AI"

(Tanpa draf tulisan sama sekali ditempel/dilampirkan.)

## Analisis sesuai SKILL.md
Tabel Input: "Draf tulisan | Ya (wajib) | Tidak ada → minta pengguna tempel drafnya." Tidak ada draf
berarti langkah kerja (baik mode Periksa maupun Perbaiki) tidak bisa dimulai — keduanya diawali "Baca
draf penuh." Tidak ada dasar teks untuk mendeteksi pola apa pun, dan `scripts/cek_pola.py` sendiri
akan menolak input kosong (`ERROR: draf kosong`, exit code 1) — jadi ini juga cocok dengan Batasan
"Input kosong/bukan teks bermakna → beri tahu pengguna, minta draf tulisan yang sebenarnya."

Tidak boleh mengarang draf atau menebak-nebak konteks tanpa ada teks sama sekali — SKILL.md hanya
mengizinkan menebak **konteks/platform** dari isi draf, bukan mengarang drafnya sendiri.

## Output yang seharusnya diberikan ke pengguna
```
Boleh, tapi aku butuh tulisannya dulu ya — tempel draf yang mau dicek/diperbaiki di sini.

Sekalian kalau tahu, ini buat apa (caption medsos, deskripsi produk, chat WA, email, atau artikel)?
Kalau nggak yakin nanti aku tebak dari isinya.
```

Ini **satu pertanyaan** berisi permintaan draf + pertanyaan konteks opsional dalam satu pesan — sesuai
prinsip CLAUDE.md "Jika info kurang, tanyakan **sekali** dalam satu pesan berisi daftar pertanyaan
singkat", bukan berondongan pertanyaan terpisah.

## Verifikasi lewat script (bukti bukan asumsi)
```
$ python3 scripts/cek_pola.py --teks ""
ERROR: draf kosong. Tempel teks lewat --teks, --file, atau stdin.
(exit code 1)
```
Perilaku script konsisten dengan yang diharapkan SKILL.md: gagal jelas, bukan diam-diam mengembalikan
skor 100 palsu untuk input kosong.

## Penilaian penguji
- Tidak mengarang draf, tidak menjalankan mode Periksa/Perbaiki dengan teks kosong.
- Satu pertanyaan balik, singkat, tidak menginterogasi.
- Konsisten dengan Batasan & penanganan error SKILL.md serta perilaku script yang sebenarnya diuji.
- **Lulus.**
