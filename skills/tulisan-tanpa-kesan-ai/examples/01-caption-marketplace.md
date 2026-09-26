# Contoh 1 — Deskripsi Produk Marketplace (Sepatu Lari)

## Input pengguna
"Perbaiki deskripsi produk sepatu lari ini biar nggak kelihatan AI banget:"

## Draf sebelum (ditempel pengguna)
> Di era digital ini, belanja online menjadi kebiasaan banyak orang. Sepatu lari kami tidak hanya
> nyaman, tetapi juga stylish untuk dipakai sehari-hari. Solusi terbaik nomor satu untuk kamu yang
> aktif! Bahan breathable, ringan, dan tahan lama menjadi kunci kenyamanan kaki seharian. Tak bisa
> dipungkiri, kualitas sol karetnya sangat penting untuk cengkeraman di jalan. Yuk simak detail produk
> selengkapnya! Semoga bermanfaat dan selamat berbelanja! 🔥🔥✨

## Hasil `scripts/cek_pola.py` (dijalankan langsung, tidak diedit)
```
Skor kebersihan pola: 49/100 (makin tinggi makin bersih)
Catatan: heuristik pencocokan kata, bukan pendeteksi AI — baca ulang sendiri.

1. Pola: Pembuka basa-basi (pembuka-basa-basi)
   Kutipan: "Di era digital ini, belanja online menjadi kebiasaan banyak orang."
2. Pola: Kontras biner palsu (kontras-biner)
   Kutipan: "Sepatu lari kami tidak hanya nyaman, tetapi juga stylish untuk dipakai sehari-hari."
3. Pola: Ajakan generik (ajakan-generik)
   Kutipan: "Yuk simak detail produk selengkapnya!"
4. Pola: Menjadi kunci / peran penting (menjadi-kunci)
   Kutipan: "Bahan breathable, ringan, dan tahan lama menjadi kunci kenyamanan kaki seharian."
5. Pola: Tak bisa dipungkiri / sangat penting untuk (tak-dipungkiri)
   Kutipan: "Tak bisa dipungkiri, kualitas sol karetnya sangat penting untuk cengkeraman di jalan."
6. Pola: Emoji berderet (emoji-berderet)
   Kutipan: "🔥🔥✨"
7. Pola: Pembuka/penutup klise (penutup-klise)
   Kutipan: "Semoga bermanfaat dan selamat berbelanja!"
8. Pola: Klaim superlatif tanpa bukti (klaim-superlatif)
   Kutipan: "Solusi terbaik nomor satu untuk kamu yang aktif!"

Total temuan: 10 kemunculan (beberapa pola cocok 2x pada kutipan yang sama)
```

## Hasil perbaikan (mode perbaiki, dikerjakan agent — bukan script)
> Sepatu lari ini pakai bahan breathable yang ringan, cocok dipakai seharian tanpa bikin kaki panas.
> Sol karetnya dirancang untuk cengkeraman lebih baik di aspal maupun trotoar basah. Bentuknya juga
> nyaman dipakai jalan santai, bukan cuma buat lari. Tersedia ukuran 38-43, warna hitam dan abu-abu.

**Yang diubah:**
- Pembuka basa-basi ("Di era digital ini...") → dihapus, langsung masuk ke fakta produk.
- Kontras biner palsu ("tidak hanya nyaman, tetapi juga stylish") → diganti kalimat langsung yang
  lebih spesifik ("nyaman dipakai jalan santai, bukan cuma buat lari").
- Klaim superlatif tanpa bukti ("Solusi terbaik nomor satu") → dihapus karena tidak ada data yang
  menopangnya; diganti manfaat konkret (cengkeraman sol, bahan breathable).
- "Menjadi kunci" & "Tak bisa dipungkiri...sangat penting untuk" → disederhanakan jadi kalimat fakta
  langsung tanpa label kepentingan.
- Ajakan generik ("Yuk simak...") dan penutup klise ("Semoga bermanfaat...") → dihapus; ditutup dengan
  info konkret yang berguna (ukuran & warna tersedia) sebagai pengganti CTA.
- Emoji berderet (🔥🔥✨) → dihapus (konteks deskripsi produk marketplace, bukan caption santai —
  emoji tidak lazim di kolom deskripsi Shopee/Tokopedia).

## Catatan
Skor 49/100 pada draf awal menunjukkan banyak pola terdeteksi — bukan berarti "49% ditulis AI".
Skor ini murni hitungan bobot pola yang cocok, dipakai sebagai titik awal, bukan vonis akhir.
