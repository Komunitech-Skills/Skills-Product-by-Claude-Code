# Contoh 2 — Jasa Laundry Sepatu

**Input pengguna:**
> "Saya mau buka jasa laundry sepatu di rumah, worth it enggak ya sebelum saya sewa tempat & beli alat lengkap? Saya punya IG dengan sekitar 400 follower (rata-rata story dilihat 120-an), dan ada warung fotokopi teman deket kampus yang mau dititipi flyer."

## 1. Hipotesis
> "Kami percaya **mahasiswa/anak kos di sekitar kampus yang sepatunya kotor tapi malas cuci sendiri** mau membayar **Rp35.000/pasang** untuk **jasa cuci sepatu (ambil-antar area kampus)** karena bisa **hemat waktu & sepatu jadi bersih tanpa ribet**. Kami akan tahu ini benar jika minimal 15% dari yang ditawari benar-benar order dalam 7 hari."

## 2. Metode uji terpilih
Gabungan **polling story Instagram** (400 follower, cukup di atas ambang 100) + **titip flyer di warung fotokopi** dekat kampus. Dihitung **gabung total** (disepakati dengan pengguna karena keduanya sama-sama menyasar audiens kampus).

## 3. Kriteria lulus/gagal
Harga Rp35rb tergolong menengah (bukan impulsif, bukan mahal) → pakai ambang default 15%/8%. Minimal ditawari 20 — target realistis karena rata-rata views story 120 + estimasi ~40 orang lewat warung fotokopi selama seminggu.

## 4. Pesan yang dipakai
Story IG:
```
Lagi mikir mau buka jasa laundry sepatu (ambil-antar area kampus) 🤔
Cuci bersih, sepatu wangi, gak perlu repot cuci sendiri
Harga rencana: Rp35.000/pasang

Kalau ada, kamu bakal pakai? [Ya, mau! / Nanti dulu]

(DM aku kalau mau coba duluan pas udah buka 😊)
```
Flyer di warung fotokopi memakai pitch titip warung yang disesuaikan jadi ajakan DM IG.

## 5. Hasil setelah 7 hari
Story dilihat 118 orang, 9 vote "Ya, mau!" tapi hanya 6 yang lanjut DM serius. Warung fotokopi: ~35 orang lewat (estimasi pemilik warung), 2 DM masuk dari flyer. Total ditawari = 118 + 35 = 153, total pre-order (DM serius) = 6 + 2 = 8.

```
$ python3 scripts/hitung_validasi.py --ditawari 153 --preorder 8 --harga 35000
=== HASIL VALIDASI IDE ===
Ditawari       : 153 orang/tampilan
Pre-order/beli : 8
Konversi       : 5.2%
Ambang         : LULUS >= 15% | LULUS BERSYARAT >= 8% | GAGAL < 8%
Klasifikasi    : GAGAL
Saran          : Data belum mendukung ide ini dalam bentuk sekarang — pertimbangkan HENTIKAN atau pivot besar. Kumpulkan alasan penolakan dari form pencatatan sebagai bahan ide berikutnya (brainstorming-ide-usaha).
```

Catatan: perhitungan awal (hanya menghitung vote polling "Ya" sebagai pre-order, 9+2=11 dari 153 = 7,2%) juga masih di bawah ambang GAGAL kalau dihitung longgar. Karena keduanya konsisten di bawah 8%, hasil **GAGAL** cukup meyakinkan meski memakai cara hitung yang lebih longgar sekalipun.

Alasan yang sempat ditanyakan ke beberapa yang menjawab "nanti dulu": mayoritas bilang "Rp35rb kemahalan buat cuci sepatu sendiri, biasanya cuma perlu sikat cepat" dan "gak tahu berapa lama prosesnya" (masalah kejelasan, bukan cuma harga).

## 6. Keputusan
Skenario di atas menunjukkan **GAGAL** murni (untuk latihan skenario kedua yang berbeda hasil dari Contoh 1). Namun andaikan hasil riil pengguna berada di kisaran 8%–<15% (mis. konversi 10%) — skenario ini ditulis ulang di bawah sebagai ilustrasi **LULUS BERSYARAT**, karena itu klasifikasi paling sering menuntut revisi eksplisit:

> Andai konversi = 10%: **LULUS BERSYARAT.** Alasan penolakan dominan soal harga & kejelasan proses → UBAH satu variabel: turunkan harga awal jadi Rp25.000 (promo perkenalan) DAN tambahkan info "estimasi selesai 1x24 jam, ambil-antar gratis area kampus" di pesan berikutnya. Uji ulang 7 hari dengan hipotesis baru sebelum sewa tempat/beli alat lengkap. Jangan ubah target pembeli sekaligus — supaya jelas variabel mana yang memperbaiki hasil.
