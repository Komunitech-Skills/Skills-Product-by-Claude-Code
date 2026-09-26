# Contoh 1 — Kopi Susu Gula Aren Kemasan Literan

**Input pengguna:**
> "Saya mau coba jual kopi susu gula aren kemasan literan buat dijual online, tapi belum tahu bakal laku atau enggak. Saya punya sekitar 150 kontak WA yang lumayan aktif (teman kantor, tetangga, komunitas arisan RT). Rencana harga Rp45.000/liter."

## 1. Hipotesis
> "Kami percaya **warga di sekitar rumah & teman kantor yang suka ngopi tapi malas antre kedai** mau membayar **Rp45.000** untuk **kopi susu gula aren kemasan literan (cukup untuk 4-5 gelas)** karena bisa **menghemat waktu & uang dibanding beli satuan di kedai setiap hari**. Kami akan tahu ini benar jika minimal 15% dari orang yang ditawari benar-benar pre-order dalam 7 hari."

## 2. Metode uji terpilih
**Pre-order via broadcast WA** — dipilih karena punya 150 kontak relevan (jauh di atas ambang minimal 30).

## 3. Kriteria lulus/gagal
- Minimal ditawari: 20 (akan kirim ke 60 kontak paling relevan dari 150, bukan semua sekaligus agar tidak spam)
- LULUS: konversi ≥15%
- LULUS BERSYARAT: 8%–<15%
- GAGAL: <8%
(Pakai ambang default — harga Rp45rb tergolong menengah, tidak perlu penyesuaian.)

## 4. Pesan yang dikirim
```
Halo Rani! 👋

Aku lagi coba mulai jual kopi susu gula aren kemasan literan — cukup buat 4-5 gelas, tinggal simpan di kulkas, praktis buat stok di rumah/kantor.

Harga: Rp45.000 / liter
Bisa custom manis (normal/less sugar)

Kalau 15 orang minat, aku mulai produksi minggu ini.
Mau pesan? Balas "MAU + jumlah" ke chat ini sebelum Jumat ya. 🙏

Kopi Aren Bu Sari
```
Dikirim ke 60 kontak yang relevan (bukan grup keluarga jauh) selama 7 hari.

## 5. Hasil setelah 7 hari
Data dicatat di form pencatatan: 60 ditawari, 11 pre-order.

```
$ python3 scripts/hitung_validasi.py --ditawari 60 --preorder 11 --harga 45000 --hpp 22000 --biaya-uji 30000
=== HASIL VALIDASI IDE ===
Ditawari       : 60 orang/tampilan
Pre-order/beli : 11
Konversi       : 18.3%
Ambang         : LULUS >= 15% | LULUS BERSYARAT >= 8% | GAGAL < 8%
Klasifikasi    : LULUS
Saran          : Datanya cukup mendukung untuk LANJUT: mulai produksi/investasi bertahap. Lanjutkan ke skill hitung-hpp (HPP & BEP rinci) dan harga-jual-marketplace (harga jual final).

=== MARGIN & BIAYA UJI ===
Margin per unit      : Rp23.000  (Rp45.000 - Rp22.000)
Total margin preorder: Rp253.000  (23000 x 11 unit)
Biaya uji            : Rp30.000
Selisih              : Rp223.000  (SUDAH balik modal uji)
```

## 6. Keputusan
**LANJUT.** Konversi 18,3% di atas ambang LULUS (15%), sudah balik modal uji dengan margin bersih Rp223.000 dari 11 pre-order. Alasan 2-3 orang menolak: "belum butuh sekarang" (bukan soal harga) — tidak perlu revisi harga. Langkah berikut: produksi 11 pesanan + stok cadangan kecil, lalu lanjut ke `hitung-hpp` untuk menghitung HPP & BEP produksi rutin bulanan, dan `harga-jual-marketplace` bila mau mulai jualan di Shopee/TikTok Shop juga.
