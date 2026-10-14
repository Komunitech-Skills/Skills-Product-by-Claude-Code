# 02 - Normal kedua: CSV 4 pemasok box kue, "yang penting cepat" (1.000 pcs, 7 hari)

- **Tanggal:** 2026-10-14 (putaran 2, versi 1.0.1) · **Penguji:** agent penguji independen (bukan pembuat) · OpenClaw 2026.10.2 lokal, model `claude-sonnet-5`, home bersih berisi hanya skill ini. Hasil SEBELUM/SESUDAH utuh: `00-openclaw-sebelum-sesudah.md`.

## Input (pesan pengguna)
> Saya admin pembelian toko kue. Penawaran 4 supplier box kue 20x20 sudah saya rangkum di penawaran-box-kue.csv. Butuh 1.000 pcs, harus tiba dalam 7 hari untuk pesanan hampers. Yang penting cepat sampai, harga nomor dua. Pilih yang mana?

## Output SESUDAH (skill 1.0.1, uji lokal)
> **Perbandingan 4 penawaran box kue 20x20: 1.000 pcs, butuh dalam 7 hari**
>
> | Pemasok | Total bayar (per pcs) | Selisih vs termurah | Skor (peringkat) |
> |---|---|---|---|
> | Toko Kemasan Kilat | Rp3.000.000 (Rp3.000) | lebih mahal Rp780.000 (35,1%) | 85,8 (1) |
> | CV Pack Nusantara | Rp2.553.000 (Rp2.553) | lebih mahal Rp333.000 (15,0%) | 57,9 (2) |
> | UD Karton Jaya | Rp2.400.000 (Rp2.400) | lebih mahal Rp180.000 (8,1%) | 54,3 (3) |
> | Percetakan Box Mandiri | Rp2.220.000 (Rp2.220) | termurah | 42,2 (4, telat) |
>
> **Rekomendasi: Toko Kemasan Kilat** (bobot dipakai: lead time 50, biaya 20, termin 10, kualitas 10, MOQ 10 — sesuai prioritas "cepat dulu, harga nomor dua")
> - Peringkat: 1. Toko Kemasan Kilat (skor 85,8), 2. CV Pack Nusantara (skor 57,9), 3. UD Karton Jaya (skor 54,3), 4. Percetakan Box Mandiri (skor 42,2, melewati tenggat).
> - Toko Kemasan Kilat lebih MAHAL Rp780.000 (35,1%) daripada Percetakan Box Mandiri untuk 1.000 pcs. Percetakan Box Mandiri adalah termurah; Toko Kemasan Kilat dipilih karena Percetakan Box Mandiri melewati tenggat (lead time 10 hari, lebih lama dari 7 hari yang kamu butuh).
> - Toko Kemasan Kilat lebih MAHAL Rp600.000 (25,0%) daripada UD Karton Jaya untuk 1.000 pcs. UD Karton Jaya adalah termurah yang tepat waktu (sementara: biaya ambil sendiri belum dihitung); Toko Kemasan Kilat dipilih karena skor gabungannya lebih tinggi (unggul di lead time — kirim besok vs UD Karton Jaya 3-5 hari kerja).
> - Bila pesanan dibagi 70/30 (Toko Kemasan Kilat 700 pcs + UD Karton Jaya 300 pcs): total Rp2.820.000, lebih MURAH Rp180.000 daripada membeli semua dari Toko Kemasan Kilat — opsi ini bisa dipertimbangkan kalau mau hemat sambil tetap aman di tenggat.
> - Biaya ambil sendiri ke UD Karton Jaya belum dihitung: UD Karton Jaya tetap tidak lebih mahal daripada CV Pack Nusantara selama biaya ambilnya (bensin, sewa angkutan, waktu) maksimal Rp153.000 untuk 1.000 pcs.
> - Asumsi pajak: ongkir Percetakan Box Mandiri dianggap bagian dari harga yang sudah termasuk PPN.
>
> **Rincian singkat:**
> 1. Toko Kemasan Kilat — Rp2.700/pcs (per pak isi 50), ongkir Rp15rb/pak (total Rp300rb), non-PKP, kirim besok, bayar COD, belum ada info kualitas, kemasan polos tanpa logo.
> 2. CV Pack Nusantara — Rp2.300/pcs, ongkir franco (gratis), PKP harga belum termasuk PPN (+Rp253rb), lead time 1 minggu, tempo 30 hari, kualitas 4/5, harga berlaku s.d. 31 Okt.
> 3. UD Karton Jaya — Rp2.400/pcs, ambil sendiri di gudang Cikarang (ongkir loco, belum dihitung), non-PKP, lead time 3-5 hari kerja, tempo 14 hari.
> 4. Percetakan Box Mandiri — Rp2.100/pcs di tingkat 1.000, ongkir Rp120rb, harga sudah termasuk PPN, lead time 10 hari (lewat tenggat), DP 50%, kualitas 4/5, cetak logo gratis.
>
> **Risiko:**
> - Toko Kemasan Kilat belum ada penilaian kualitas; cek sampel fisik dulu karena polos tanpa logo.
> - CV Pack Nusantara: harga berlaku hanya sampai 31 Okt — pastikan PO masuk sebelum tanggal itu.
> - UD Karton Jaya mengandalkan ambil sendiri; kalau armada/waktu mepet, ini bisa jadi risiko tersembunyi untuk tenggat 7 hari.
>
> **Pesan WA (siap kirim):**
>
> Ke Toko Kemasan Kilat:
> "Halo, mau konfirmasi untuk pesanan 1.000 pcs box kue 20x20 (20 pak isi 50). Bisa tolong infokan: 1) contoh foto/sampel fisik sebelum PO, 2) apakah ongkir Rp15rb/pak itu final untuk alamat kami, 3) estimasi jam tiba besok supaya kami bisa siapkan tim terima barang. Terima kasih."
>
> Ke UD Karton Jaya:
> "Halo, untuk pesanan 1.000 pcs box kue 20x20, mohon info: 1) apakah bisa diantar (bukan ambil sendiri) dan berapa ongkirnya, 2) kalau tetap ambil sendiri, jam operasional gudang Cikarang untuk pickup, 3) estimasi waktu produksi pastinya (3 atau 5 hari kerja) supaya kami pastikan tiba dalam 7 hari. Terima kasih."
>
> **Data yang belum ada:** [isian: penilaian kualitas Toko Kemasan Kilat; biaya ambil sendiri ke UD Karton Jaya]
> **Asumsi:** Harga bertingkat berlaku untuk seluruh 1.000 pcs; kualitas yang belum dinilai dianggap netral (3/5); pembeli dianggap bukan PKP.
> Perbandingan ini alat bantu keputusan pembelian, bukan nasihat pajak/hukum — pastikan harga, PPN, dan syarat tertulis di penawaran resmi/faktur sebelum PO.
>
> Ada 3 hal yang bisa mengubah hasil ini:
> 1. Kalau kamu oke sedikit telat (misal toleransi 8-10 hari), Percetakan Box Mandiri (termurah, cetak logo gratis) jadi layak dipertimbangkan — mau dicek ulang dengan skenario itu?
> 2. Mau saya hitungkan opsi bagi pesanan 70/30 (Toko Kemasan Kilat + UD Karton Jaya) secara detail untuk hemat Rp180.000?
> 3. Apakah box perlu cetak logo toko, atau polos (seperti Toko Kemasan Kilat) tidak masalah untuk hampers ini?

## Data
`data/penawaran-box-kue.csv` (harga per pak isi 50 + ongkir per pak; tingkat tepat di batas 1.000 dan sudah termasuk PPN; loco + "3-5 hari kerja"; PKP `belum` + franco + tempo 30).

## Catatan penguji (1.0.1)
- **Nilai SESUDAH 8** (SEBELUM 6,5).
- Bobot "cepat dulu" disebut terbuka. Skor 85,8/57,9/54,3/42,2 dan semua rupiah benar. Kalimat bersubjek benar:
  - Kilat lebih MAHAL Rp780.000 (35,1%) daripada Mandiri (telat).
  - Kilat lebih MAHAL Rp600.000 (25,0%) daripada Karton Jaya (termurah yang tepat waktu).
  - Bagi 70/30 "lebih MURAH Rp180.000".
  - Batas biaya ambil Karton Jaya Rp153.000 (= 2.553.000 − 2.400.000).
- Cacat `belum` sudah hilang: PPN CV Pack Nusantara dibaca "belum termasuk (+Rp253rb)", tanpa `[isian]` atau WA palsu.
- Kekurangan:
  - 4.553 karakter, melebihi batas ±4.000 di SKILL.md (Telegram memecahnya jadi 2 pesan).
  - Bagi 70/30 disebut "tetap aman di tenggat", padahal porsi Karton Jaya tiba pas hari ke-7 dan biaya ambilnya belum dihitung (keduanya disebut di bagian risiko).
  - WA ke Kilat menanyakan ongkir yang sudah tertulis.
  - Agent menjalankan `find /` untuk mencari CSV.

## Riwayat
- 1.0.0: SESUDAH 7,5. "Kilat hemat Rp180.000 dibanding Karton Jaya" salah subjek; PPN CV Pack Nusantara ditanyakan padahal CSV menulis `belum`.
