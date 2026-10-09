# Uji 07 - Normal 2: piyama bayi, brief ke konveksi

Penguji independen, 2026-09-29, `claude-code (simulasi agent)`. Data fiktif.

**Pengguna:** "Saya mau bikin piyama bayi katun combed 30s motif hewan, ukuran 0-3, 3-6, 6-12 bulan. Jual Rp79.000 per set, margin 45%. Buatkan spesifikasi dan brief untuk konveksi di Bandung. Pesanan awal 300 set."

## Hasil agen (mengikuti SKILL.md)
- Jenis A + C. Templat fashion: bahan katun combed 30s, tabel ukuran per rentang umur dengan kolom cm "[isi dari pola konveksi]" (tidak dikarang), warna/motif, jahitan obras + kancing jepret.
- HPP maksimal = 79.000 x (1 - 0,45) = **Rp43.450** (dicek independen: benar).
- Standar mutu: ukuran sesuai tabel +/- 1 cm, susut setelah cuci diuji, jahitan tidak lepas ditarik, kancing kuat.
- Brief konveksi (`templates/brief-pihak-ketiga.md`): tujuan, spesifikasi, 300 set, tanya MOQ & harga per tingkat, sampel 1 set per ukuran, kriteria terima, tenggat. **Tidak memuat HPP/margin** - sesuai aturan langkah 9. Baik.
- Bagian izin: agen mengambil dari `references/perizinan-produk.md` baris "Fashion & kerajinan: **Umumnya tidak perlu izin edar khusus**" lalu menulis "tidak perlu izin edar khusus; perhatikan label bahan, ukuran, merek".

## Masalah (fakta, dicek 2026-09-29)
Pakaian bayi (menyentuh kulit bayi s/d 36 bulan) terkena **SNI wajib** (zat warna azo, kadar formaldehida, logam terekstraksi) lewat Permenperin No. 7 Tahun 2014 - https://www.kemenperin.go.id/artikel/22114/Kemenperin-Bimbing-IKM-Pakaian-Bayi-Terapkan-SNI-Wajib ; BSN: https://bsn.go.id/main/berita/berita_det/6298 . Mainan anak (bisa jadi produk "kerajinan") juga SNI wajib (Permenperin 55/M-IND/PER/11/2013). Referensi skill tidak menyebut SNI sama sekali, sehingga agen memberi **rasa aman yang salah** kepada pengguna. Brief juga tidak menanyakan ke konveksi apakah kain punya sertifikat SNI/uji lab.

**Vonis: GAGAL sebagian** - format, hitungan, dan brief baik; pengingat legalitas keliru untuk kategori yang realistis bagi UMKM fashion.
