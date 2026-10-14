# 02 - Normal kedua: CSV 4 pemasok box kue, "yang penting cepat" (1.000 pcs, 7 hari)

- **Tanggal:** 2026-10-14 · **Penguji:** agent penguji independen (bukan pembuat) · OpenClaw 2026.10.2 lokal, model `claude-sonnet-5`, home berisi hanya skill ini. Hasil SEBELUM/SESUDAH utuh: `00-openclaw-sebelum-sesudah.md`.

## Input (pesan pengguna)
> Saya admin pembelian toko kue. Penawaran 4 supplier box kue 20x20 sudah saya rangkum di penawaran-box-kue.csv. Butuh 1.000 pcs, harus tiba dalam 7 hari untuk pesanan hampers. Yang penting cepat sampai, harga nomor dua. Pilih yang mana?

## Output SESUDAH (skill aktif)
> **Perbandingan 4 penawaran box kue 20x20: 1.000 pcs, butuh dalam 7 hari**
> Yang paling murah (Percetakan Box Mandiri, Rp2.220/pcs) justru **melewati tenggat 7 hari** (lead time 10 hari), jadi tidak disarankan meski termurah. Karena prioritasnya kecepatan dulu baru harga, pemenangnya **Toko Kemasan Kilat** — satu-satunya yang pasti tiba sebelum tenggat (lead time 1 hari), dengan selisih harga +Rp780.000 dari yang termurah.
>
> | Pemasok | Total bayar (per pcs) | Selisih vs termurah | Skor (peringkat) |
> |---|---|---|---|
> | Toko Kemasan Kilat | Rp3.000.000 (Rp3.000) | +Rp780.000 (+35,1%) | 85,8 (1) |
> | CV Pack Nusantara | Rp2.553.000 (Rp2.553) | +Rp333.000 (+15,0%) | 57,9 (2) |
> | UD Karton Jaya | Rp2.400.000 (Rp2.400) | +Rp180.000 (+8,1%) | 54,3 (3) |
> | Percetakan Box Mandiri | Rp2.220.000 (Rp2.220) | termurah | 42,2 (4) — telat |
>
> **Rekomendasi: Toko Kemasan Kilat**
> 1. Satu-satunya yang jelas tiba dalam tenggat (lead time 1 hari vs kebutuhan 7 hari) — sesuai prioritas "cepat dulu, harga nomor dua".
> 2. Total Rp3.000.000 untuk 1.000 pcs (Rp3.000/pcs), COD — tidak ada risiko DP ke pemasok yang belum dikenal.
> 3. Catatan: polos tanpa logo (tidak seperti Percetakan Box Mandiri yang cetak logo gratis tapi telat); kualitas belum dinilai, perlu cek sampel dulu sebelum order 1.000 pcs.
>
> **Rincian singkat:**
> - Toko Kemasan Kilat: Rp2.700/pcs (dari harga per pak isi 50), beli 1.000 pcs, ongkir Rp300.000 (dari Rp15rb/pak), tanpa PPN (non-PKP), lead time 1 hari, COD.
> - CV Pack Nusantara: Rp2.300/pcs (berlaku ≥500), ongkir franco (gratis), PPN Rp253.000 (PKP, harga diasumsikan belum termasuk PPN), lead time 7 hari (pas di tenggat, berisiko), tempo 30 hari.
> - UD Karton Jaya: Rp2.400/pcs, ambil sendiri di Cikarang (biaya ambil belum dihitung), tanpa PPN, lead time 7 hari kalender (dari "3-5 hari kerja", pas di tenggat), tempo 14 hari.
> - Percetakan Box Mandiri: Rp2.100/pcs (tingkat ≥1.000), ongkir Rp120.000, PPN Rp220.000 (sudah termasuk harga), lead time **10 hari — lewat tenggat**, DP 50%.
>
> **Kalau kondisinya berubah:**
> - Jumlah 2x (2.000 pcs): rekomendasi tetap Toko Kemasan Kilat (Rp6.000.000); Percetakan Box Mandiri jadi termurah (Rp4.320.000) tapi tetap telat.
> - Bila Percetakan Box Mandiri (termurah) telat 7 hari lagi (jadi 17 hari): rekomendasi tetap Toko Kemasan Kilat; dibanding UD Karton Jaya hemat Rp180.000.
> - Bagi pesanan 70/30 (Toko Kemasan Kilat + UD Karton Jaya): total Rp2.820.000, tapi UD Karton Jaya lead time-nya pas 7 hari (berisiko mepet) dan ongkir ambil sendiri belum masuk hitungan.
>
> **Risiko yang perlu dijaga:** Toko Kemasan Kilat belum punya catatan kualitas (nilai dianggap netral 3/5) — minta sampel sebelum order 1.000 pcs sekaligus; "lead time 1 hari" perlu dipastikan untuk kuantitas 1.000 pcs (bukan stok kecil); CV Pack Nusantara harga berlaku hanya sampai 31 Okt; harga sampel vs produksi massal bisa beda.
>
> **Pesan WA ke pemasok (siap kirim):**
>
> Ke Toko Kemasan Kilat:
> "Selamat siang, untuk pesanan 1.000 pcs box kue 20x20, apakah stok ready untuk jumlah segitu dan tetap bisa dikirim besok? Boleh minta foto/sampel barang sebelum kami konfirmasi pesanan? Terima kasih."
>
> Ke UD Karton Jaya:
> "Selamat siang, terima kasih penawarannya. Kalau kami ambil sendiri di gudang Cikarang, apakah ada biaya tambahan di luar harga barang? Dan lead time 3-5 hari kerja itu dihitung dari kapan? Terima kasih."
>
> Ke CV Pack Nusantara:
> "Selamat siang, terima kasih penawarannya. Mohon konfirmasi harga Rp2.300/pcs itu sudah termasuk PPN atau belum, dan bisa terbit faktur pajak atas nama usaha kami? Terima kasih."
>
> **Data yang belum ada:** [isian: biaya ambil barang sendiri ke UD Karton Jaya], [isian: harga CV Pack Nusantara sudah/belum termasuk PPN — dihitung belum termasuk; bila sudah termasuk, total turun Rp253.000]
>
> **Asumsi:** usaha Anda bukan PKP (PPN pemasok PKP dihitung sebagai biaya, bukan dikreditkan); bobot penilaian saya geser ke prioritas kecepatan (lead time 50, biaya 20, termin 10, kualitas 10, MOQ 10) sesuai permintaan "cepat dulu, harga nomor dua"; harga bertingkat berlaku untuk seluruh jumlah yang dibeli; kualitas yang belum dinilai dianggap netral (3/5).
>
> Catatan: alat bantu keputusan pembelian, bukan nasihat pajak/hukum; pastikan harga & PPN tertulis di penawaran/faktur resmi sebelum deal.
>
> Tiga hal yang paling menentukan kalau mau saya hitung ulang lebih presisi:
> 1. Biaya ambil sendiri ke UD Karton Jaya (bensin/ongkos jemput) — kalau ini besar, posisinya bisa turun lebih jauh.
> 2. Harga CV Pack Nusantara sudah termasuk PPN atau belum?
> 3. Apakah lead time 1 hari Toko Kemasan Kilat itu memang berlaku untuk 1.000 pcs sekaligus, atau perlu dikonfirmasi ulang ke mereka?

## Data
`data/penawaran-box-kue.csv`: harga per pak isi 50 + ongkir per pak (Kilat), harga bertingkat tepat di batas 1.000 dan sudah termasuk PPN (Mandiri), loco + "3-5 hari kerja" (Karton Jaya), PKP belum PPN + franco + tempo 30 hari (Pack Nusantara).

## Catatan penguji
- **Nilai SESUDAH 7,5** (SEBELUM 6,5).
- Bobot diubah sesuai permintaan "cepat dulu, harga nomor dua" (lead 50, biaya 20, termin 10, kualitas 10, MOQ 10) dan disebut di asumsi. Skor 85,8/57,9/54,3/42,2 dihitung ulang penguji: benar. Dengan bobot default, rekomendasi akan CV Pack Nusantara (76,8 vs 76,1, "hampir seri"), jadi pengubahan bobot memang menentukan.
- Semua angka benar: Kilat 1.000 × Rp2.700 + 20 pak × Rp15.000 = Rp3.000.000; Mandiri Rp2.220.000 (DPP 2.000.000, PPN 220.000) telat; Pack Nusantara 2.300.000 + PPN 253.000; Karton Jaya Rp2.400.000 + `[isian: biaya ambil]`, 3-5 hari kerja = 7 hari kalender.
- **Cacat:** "rekomendasi tetap Toko Kemasan Kilat; dibanding UD Karton Jaya hemat Rp180.000" salah subjek (selisih itu milik Percetakan Box Mandiri; Kilat lebih mahal Rp600.000). PPN CV Pack Nusantara dianggap "belum jelas" lalu ditanyakan lewat WA, padahal CSV menulis `belum` (cacat script). "Satu-satunya yang pasti tiba" berlebihan.
- Model dasar (SEBELUM) juga memilih Kilat, tetapi menulis total Mandiri tanpa ongkir.
