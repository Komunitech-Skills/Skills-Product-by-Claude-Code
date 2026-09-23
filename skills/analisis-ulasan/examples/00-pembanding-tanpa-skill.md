# 00 — Uji A/B: S1 tanpa skill vs dengan skill

**Input (sama dengan S1):** "Ini ulasan toko aku 3 bulan terakhir dari Shopee, filenya ulasan.csv. Keluhan paling banyak apa sih? Terus apa yang harus aku benahi duluan?" (160 ulasan uji, lihat `01-…`)

## A. Tanpa skill (agent umum, tanpa membaca skill apa pun)
Agent umum membuka CSV, menghitung bintang dengan python singkat, lalu mengelompokkan keluhan dengan pencarian kata kunci sederhana (`lama|telat`, `kecil|gede`, `jutek|dibales`, …). Output yang dihasilkan:

> **Ringkasan ulasan (160 ulasan)**
> Rata-rata rating 3,88. Bintang 5: 81, bintang 4: 27, bintang 3: 22, bintang 2: 12, bintang 1: 18.
>
> **Keluhan terbanyak:**
> 1. Pengiriman lama (±16 ulasan), contoh: "Kak Rina tolong cek pesanan no 2409230000XYZ12 blm sampe, wa saya 0812-0000-1234"
> 2. Salah kirim (±10 ulasan)
> 3. Kualitas bahan: tipis, luntur, jahitan lepas (±10 ulasan)
> 4. Admin lambat balas / jutek (±8 ulasan)
> 5. Tidak sesuai foto (±8), ukuran (±7), kemasan (±5)
>
> **Pujian:** banyak yang bilang sesuai foto, pengiriman cepat, packing rapi, dan harga murah.
>
> **Saran:**
> - Percepat pengiriman, mungkin ganti ekspedisi.
> - Lebih teliti saat packing.
> - Tingkatkan kualitas bahan.
> - Balas chat lebih cepat.
> - Perbaiki foto produk.

## B. Dengan skill `analisis-ulasan`
Lihat `01-toko-kaos-160-ulasan-csv.md`: laporan lengkap 7 bagian.

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Sebaran bintang & rata-rata | Benar (hitungan sederhana) | Benar + persen positif/netral/negatif, per produk, per bulan (tren turun 4,07 → 3,71) |
| Jumlah per tema | Perkiraan "±", kata kunci kasar (mis. "lama" juga menangkap hal lain) | Dihitung script, **diverifikasi** lewat kutipan, koreksi dicatat. Cocok dengan ground truth penguji di 6 dari 7 tema keluhan |
| Privasi | **Mengutip nomor pesanan & nomor HP pembeli apa adanya** | Nama, nomor, resi, @akun disamarkan; checklist privasi |
| Sarkasme | Tidak dibahas | "Mantap, 2 minggu baru nyampe" dikenali dan dihitung sebagai keluhan |
| Prioritas | Daftar saran umum ("tingkatkan kualitas", "ganti ekspedisi") | Urutan berbasis frekuensi × keparahan bintang, dengan tindakan spesifik (jam potong 15.00, checklist packing) dan **ukuran keberhasilan** |
| Diagnosis penyebab | "Ganti ekspedisi". Ini salah arah, karena bukti menunjukkan masalah ada di **proses toko** ("5 hari baru dikirim") | Memisahkan proses toko vs kurir dan menyebutnya sebagai dugaan yang perlu dicek |
| Ide konten | Tidak ada | 5 ide dengan hook, kutipan, CTA, dan aturan izin |
| Sinyal dini | Tidak ada | 7 ulasan bintang 4–5 yang mengeluh |

## Penilaian
Skill **jelas lebih baik**: lebih akurat dalam diagnosis, aman privasi, dan langsung bisa dipakai untuk rapat tim. Nilai tambah terbesar ada di prioritas + ukuran keberhasilan, penyamaran data pribadi, dan verifikasi tema.

Catatan jujur: untuk **hitungan jumlah per tema** saja, agent umum yang teliti bisa mendekati angka skill. Tanpa langkah verifikasi, script skill justru **salah menaruh "Respons admin" di peringkat 1** (bug regex "pesanan"→"pesan"). Keunggulan skill bergantung pada agent benar-benar menjalankan langkah 3 (verifikasi).
