# Contoh 4 (Uji Independen — Akun B) — Jasa Cuci AC Panggilan di Bekasi

**Input pengguna:**
> "Saya mau buka jasa cuci AC panggilan di daerah Bekasi. Punya alat sendiri, biasanya bantu tetangga/saudara gratis. Ada grup WA warga komplek (~120 orang) tapi belum tentu semua relevan. Rencana harga Rp150.000/unit."

## 1. Hipotesis
> "Kami percaya **warga komplek di Bekasi yang punya AC rumah dan malas cari tukang dadakan** mau membayar **Rp150.000** untuk **jasa cuci AC panggilan ke rumah** karena bisa **AC bersih tanpa ribet cari tukang & nego harga di tempat**. Kami akan tahu ini benar jika minimal 15% dari yang ditawari benar-benar booking dalam 7 hari."

## 2. Metode uji terpilih
Pre-order via broadcast WA ke grup warga komplek (dipilih 18 kontak paling relevan yang diketahui punya AC dari sekitar 120 anggota grup — jumlah aktif punya AC & relevan lebih kecil dari total anggota grup, wajar dipersempit).

## 3. Kriteria lulus/gagal
- Minimal ditawari: 20 (18 yang tersedia < ambang → sesuai SKILL.md, hasil otomatis ditandai "indikasi awal" oleh script, bukan alasan batal uji).
- LULUS ≥15% | LULUS BERSYARAT 8%–<15% | GAGAL <8%. Harga Rp150rb tergolong menengah, ambang default dipertahankan.

## 4. Hasil setelah 7 hari
18 ditawari, 2 booking.

```
$ python3 scripts/hitung_validasi.py --ditawari 18 --preorder 2 --harga 150000 --hpp 60000 --biaya-uji 0
=== HASIL VALIDASI IDE ===
Ditawari       : 18 orang/tampilan
Pre-order/beli : 2
Konversi       : 11.1%
PERINGATAN: jumlah ditawari (18) di bawah ambang sampel minimal (20) — anggap ini INDIKASI AWAL, bukan kesimpulan final.
Klasifikasi    : LULUS BERSYARAT
...
Margin per unit      : Rp90.000  (Rp150.000 - Rp60.000)
Total margin preorder: Rp180.000  (90000 x 2 unit)
Biaya uji            : Rp0
Selisih              : Rp180.000  (SUDAH balik modal uji)
```
Verifikasi independen: 2/18 = 0,1111 → 11,1% ✅ (pembulatan 1 desimal benar). Margin 150.000-60.000=90.000 ✅, ×2=180.000 ✅.

## 5. Keputusan
**UBAH (LULUS BERSYARAT), dengan catatan sampel kecil.** Dua sinyal harus disampaikan bersamaan sesuai SKILL.md: (a) klasifikasi LULUS BERSYARAT → revisi satu variabel (mis. tawarkan diskon booking pertama atau perluas ke grup RT tetangga) lalu uji ulang; (b) peringatan sampel <20 → hasil ini "indikasi awal", jangan buru-buru sewa tempat/beli alat tambahan berdasarkan angka ini saja. Kedua keterangan konsisten satu sama lain (tidak ada kontradiksi antara "UBAH" dan "indikasi awal") — keduanya sama-sama mengarah ke "jangan investasi besar dulu, uji ulang".

## Catatan penguji
- Konsisten dengan Batasan & Penanganan Error SKILL.md poin "Sampel kecil = hasil belum pasti" — script dan narasi keputusan sejalan, tidak ada kasus di mana angka bilang GAGAL tapi rekomendasi bilang LANJUT atau sebaliknya.
- Perlu dicatat: SKILL.md tidak secara eksplisit membahas jasa dengan wilayah geografis terbatas (radius panggilan) sebagai faktor pemilihan kanal — namun ini tidak menghambat penggunaan skill, agent tetap bisa menyimpulkan sendiri secara wajar.
