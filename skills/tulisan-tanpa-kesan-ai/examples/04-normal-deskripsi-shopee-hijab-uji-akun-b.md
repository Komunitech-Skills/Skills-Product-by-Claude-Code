# Skenario 4 (uji independen) — Normal 2: Deskripsi Produk Shopee Hijab

## Input pengguna
"Cek dulu deskripsi produk hijab ini, kedengeran AI banget nggak:
Di era modern ini, hijab menjadi salah satu kebutuhan fashion wanita muslimah. Hijab pashmina kami
tidak hanya nyaman dipakai, tetapi juga adem sepanjang hari. Bahan yang kami gunakan cepat, mudah, dan
terpercaya untuk segala aktivitas. Produk kami menjadi solusi terbaik untuk kamu yang mencari hijab
berkualitas. Tersedia 15 pilihan warna, bahan voal premium anti panas. Yuk order sekarang juga!"

Kata "cek dulu...AI banget nggak" → **mode Periksa** (tabel Input SKILL.md: kata "cek"/"apakah ini
AI" tanpa minta tulis ulang → mode periksa).

## Jalankan `scripts/cek_pola.py`
```
Skor kebersihan pola: 71/100 (makin tinggi makin bersih)
1. Pembuka basa-basi — "Di era modern ini, hijab menjadi salah satu kebutuhan fashion wanita muslimah."
2. Kontras biner palsu — "Hijab pashmina kami tidak hanya nyaman dipakai, tetapi juga adem sepanjang hari."
3. Menjadi kunci / peran penting — "Produk kami menjadi solusi terbaik untuk kamu yang mencari hijab
   berkualitas."
4. Tiga-serangkai berulang — "Bahan yang kami gunakan cepat, mudah, dan terpercaya untuk segala
   aktivitas." (catatan: ironis — "terpercaya" dipakai untuk BAHAN kain, bukan konteks yang biasanya
   dipakai tiga-serangkai ini; tetap valid sebagai pola tiga-serangkai generik)
5. Klaim superlatif tanpa bukti — "Produk kami menjadi solusi terbaik untuk kamu yang mencari hijab
   berkualitas."
Total temuan: 5
```
Verifikasi manual: "Yuk order sekarang juga!" bukan pola dari daftar (bukan "yuk simak", melainkan CTA
langsung yang sah) — script benar tidak menandainya, dan agen juga tidak menambahkannya sebagai
temuan karena memang bukan basa-basi, ini CTA valid.

## Output yang diberikan ke pengguna (mode Periksa — TIDAK menulis ulang penuh)

```
🔍 Hasil periksa (skor kebersihan pola: 71/100 — makin tinggi makin bersih dari pola AI)
Catatan: ini bukan pendeteksi AI, hanya penanda pola yang bisa kamu cek sendiri.

1. Pola: Pembuka basa-basi
   Kutipan: "Di era modern ini, hijab menjadi salah satu kebutuhan fashion wanita muslimah."
   Perbaikan: hapus, langsung ke fakta produk (bahan/model hijabnya).

2. Pola: Kontras biner palsu
   Kutipan: "Hijab pashmina kami tidak hanya nyaman dipakai, tetapi juga adem sepanjang hari."
   Perbaikan: gabung jadi satu klaim langsung, mis. "adem dipakai seharian, bahannya menyerap keringat."

3. Pola: Tiga-serangkai berulang
   Kutipan: "Bahan yang kami gunakan cepat, mudah, dan terpercaya untuk segala aktivitas."
   Perbaikan: ganti kata sifat generik dengan fakta bahan konkret, mis. sebut nama bahannya (voal
   premium) dan kenapa itu bagus, bukan tiga kata sifat umum.

4. Pola: Menjadi kunci / peran penting + Klaim superlatif tanpa bukti (kutipan sama)
   Kutipan: "Produk kami menjadi solusi terbaik untuk kamu yang mencari hijab berkualitas."
   Perbaikan: hapus label "solusi terbaik" tanpa bukti; ganti dengan fakta spesifik (jumlah warna,
   bahan, harga) yang sudah kamu sebutkan sendiri di kalimat berikutnya.

Tidak ada pola mencurigakan lain di bagian: "Tersedia 15 pilihan warna, bahan voal premium anti
panas. Yuk order sekarang juga!" — bagian ini sudah konkret dan bersih dari pola AI.

Mau saya perbaiki sekalian? (ketik "perbaiki" atau kirim ulang minta ditulis ulang)
```

## Penilaian penguji
- Mode Periksa dijalankan dengan benar: **tidak menulis ulang penuh**, hanya kutipan + nama pola +
  saran singkat 1 kalimat per temuan, sesuai format output SKILL.md.
- Tidak mengklaim persentase "AI-generated" — hanya "skor kebersihan pola", sesuai Batasan.
- Menyebutkan eksplisit bagian yang sudah bersih ("Tersedia 15 pilihan warna...") sesuai format output.
- Diakhiri tawaran "Mau saya perbaiki sekalian?" sesuai Langkah kerja Periksa #5.
- **Lulus.**
