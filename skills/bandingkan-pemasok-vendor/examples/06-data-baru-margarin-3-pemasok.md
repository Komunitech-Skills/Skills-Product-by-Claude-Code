# 06 - Tambahan penguji (data baru): usaha roti, 3 penawaran margarin (180 kg, tenggat 6 hari)

- **Tanggal:** 2026-10-14 (putaran 2, versi 1.0.1) · **Penguji:** agent penguji independen (bukan pembuat) · OpenClaw 2026.10.2 lokal, model `claude-sonnet-5`, home bersih berisi hanya skill ini. Hasil SEBELUM/SESUDAH utuh: `00-openclaw-sebelum-sesudah.md`.

## Input (pesan pengguna)
> Halo, saya punya usaha roti rumahan, butuh margarin 180 kg paling lambat 6 hari lagi buat stok pesanan akhir bulan. Tolong bandingin 3 penawaran ini:
>
> [CV Lancar Jaya] Margarin ready kak, 385rb/karton isi 15kg. Ambil 12 karton ke atas jadi 380rb/karton. Min order 10 karton. Ongkir 8rb/karton. Harga sudah termasuk PPN ya kak (kami PKP). Kirim 2 hari. Pembayaran tempo 14 hari.
>
> [Toko Sumber Rejeki] margarin curah 24.900/kg kak, kita bukan PKP. ongkir nanti dihitung sesuai alamat. bisa kirim besok, bayar COD
>
> [PT Margarindo Prima] Harga Rp23.800/kg (belum termasuk PPN 11%). Minimum order 200 kg. Free ongkir. Pengiriman 4-5 hari kerja. Termin: DP 30%, pelunasan 30 hari setelah barang diterima.
>
> Mana yang paling hemat dan aman?

## Output SESUDAH (skill 1.0.1, uji lokal)
> Sudah saya hitung total biaya sampai bayar (bukan cuma harga per kg) untuk kebutuhan 180 kg margarin, tenggat 6 hari:
>
> **Perbandingan 3 penawaran margarin: 180 kg, butuh dalam 6 hari**
> | Pemasok | Total bayar (per kg) | Selisih vs termurah | Skor (peringkat) |
> |---|---|---|---|
> | Toko Sumber Rejeki | Rp4.482.000 (Rp24.900) | termurah sementara | 86,5 (1) |
> | CV Lancar Jaya | Rp4.656.000 (Rp25.867) | lebih mahal Rp174.000 (3,9%) | 81,8 (2) |
> | PT Margarindo Prima | Rp5.283.600 (Rp29.353) | lebih mahal Rp801.600 (17,9%) | 64,2 (3, telat) |
>
> **Rekomendasi: Toko Sumber Rejeki** (peringkat 1).
> - Peringkat: 1. Toko Sumber Rejeki (skor 86,5), 2. CV Lancar Jaya (skor 81,8), 3. PT Margarindo Prima (skor 64,2, melewati tenggat).
> - Toko Sumber Rejeki adalah yang termurah (sementara: ongkir belum diketahui): Toko Sumber Rejeki lebih murah Rp174.000 daripada CV Lancar Jaya untuk 180 kg, termurah berikutnya.
> - Bila jumlahnya 2x (360 kg): termurah tetap Toko Sumber Rejeki (Rp8.964.000).
> - Bila Toko Sumber Rejeki telat 7 hari (tiba hari ke-8, melewati tenggat 6 hari): rekomendasi pindah ke CV Lancar Jaya, yang lebih mahal Rp174.000 (3,9%) daripada Toko Sumber Rejeki.
> - Bila pesanan dibagi 70/30 (Toko Sumber Rejeki 126 kg + CV Lancar Jaya 54 kg, CV wajib beli 150 kg karena minimal order): total Rp7.067.400, lebih mahal Rp2.585.400 (57,7%) daripada semua dari Toko Sumber Rejeki.
> - Ongkir Toko Sumber Rejeki belum diketahui (total di atas belum termasuk ongkir): Toko Sumber Rejeki tetap tidak lebih mahal daripada CV Lancar Jaya selama ongkirnya maksimal Rp174.000 untuk 180 kg (≈Rp966,67/kg).
> - Asumsi pajak: ongkir CV Lancar Jaya dianggap bagian dari harga yang sudah termasuk PPN.
>
> **Rincian singkat:**
> 1. Toko Sumber Rejeki — Rp24.900/kg, non-PKP (tanpa PPN), ongkir belum dihitung, kirim besok (aman tenggat), COD.
> 2. CV Lancar Jaya — Rp380.000/karton isi 15kg (pas 12 karton untuk 180kg), harga sudah termasuk PPN, ongkir Rp96.000 total, kirim 2 hari (aman), tempo 14 hari.
> 3. PT Margarindo Prima — Rp23.800/kg (belum termasuk PPN, jadi efektif lebih mahal), minimal order 200kg (20kg sisa nganggur), ongkir gratis, kirim 5-7 hari kerja ≈7 hari kalender (**melewati tenggat 6 hari**), DP 30% + tempo 30 hari.
>
> **Risiko:**
> - Toko Sumber Rejeki non-PKP dan COD: minta bukti timbangan/kualitas saat barang datang, jangan transfer penuh di muka ke rekening pribadi yang belum dikenal.
> - PT Margarindo berisiko telat untuk kebutuhan 6 hari; jangan andalkan sebagai pemasok utama kali ini.
> - Hanya mengandalkan satu pemasok untuk 180 kg itu rawan — kalau Toko Sumber Rejeki telat/barang bermasalah, stok akhir bulan bisa terganggu.
>
> **Pesan WA (siap kirim):**
>
> *Ke Toko Sumber Rejeki:*
> "Selamat siang kak, untuk pesanan margarin curah 180 kg, mohon info ongkir ke alamat kami berapa ya? Dan apakah bisa dipastikan kirim besok supaya diterima maksimal dalam 6 hari dari sekarang? Terima kasih."
>
> *Ke PT Margarindo Prima:*
> "Selamat siang, untuk kebutuhan kami 180 kg, apakah bisa dipesan sesuai jumlah ini (di bawah minimal 200 kg)? Mohon info juga apakah pengiriman bisa dipercepat agar tiba dalam 6 hari, dan apakah faktur pajak PPN-nya bisa terbit atas nama usaha kami. Terima kasih."
>
> **Data yang belum ada:** [isian: ongkir Toko Sumber Rejeki ke alamat Anda]
> **Asumsi:** Usaha Anda dianggap bukan PKP, jadi PPN dari pemasok PKP (CV Lancar Jaya, PT Margarindo) dihitung sebagai biaya, bukan dikreditkan.
> Catatan: Ini alat bantu keputusan, bukan nasihat pajak/hukum — pastikan harga, PPN, dan syarat tertulis resmi di faktur sebelum deal.
>
> Tiga hal yang bisa mengubah keputusan:
> 1. Berapa ongkir Toko Sumber Rejeki ke alamat usaha Anda?
> 2. Usaha Anda sendiri sudah PKP atau belum (ini menentukan apakah PPN CV Lancar Jaya/Margarindo bisa dikreditkan)?
> 3. Mau langsung PO 180 kg ke Toko Sumber Rejeki sebagai utama, atau tetap jaga-jaga pesan sedikit ke CV Lancar Jaya sebagai cadangan?

## Mengapa ada skenario ini
"Contoh ringkas" di SKILL.md 1.0.1 berisi data dan jawaban skenario 1, jadi penguji menambah data yang tidak ada di skill dengan tingkat kesulitan setara:
- Lancar Jaya: harga per karton isi 15 kg, tingkat harga tepat di batas 12 karton, PKP harga sudah termasuk PPN, ongkir per karton.
- Sumber Rejeki: non-PKP, ongkir belum diketahui.
- Margarindo: PKP belum PPN, MOQ 200 kg di atas kebutuhan, "4-5 hari kerja" melewati tenggat, DP 30% + tempo 30 hari.

Data hitung ulang penguji: `data/s1v-margarin-penguji.json`, `data/verifikasi-penguji-1.0.1.py`.

## Catatan penguji
- **Nilai SESUDAH 8** (lokal) dan **7,5** (Telegram); SEBELUM **6**.
- Semua rupiah, peringkat, dan rekomendasi benar di kedua konteks:
  - Sumber Rejeki Rp4.482.000 "termurah sementara".
  - Lancar Jaya Rp4.656.000 (DPP 4.194.595, PPN 461.405).
  - Margarindo Rp5.283.600 (telat; sisa 20 kg, modal tertahan Rp528.360).
  - **Batas ongkir Rp174.000 (≈Rp966,67/kg).**
- Model dasar justru merekomendasikan Lancar Jaya sebagai "paling hemat" tanpa batas ongkir, dan membuat klaim kualitas tanpa dasar.
- **Cacat (minor, tidak mengubah rupiah/peringkat/rekomendasi):**
  1. Lokal: lead time Margarindo dikutip "5-7 hari kerja" (penawaran: "4-5 hari kerja").
  2. Telegram: skor Margarindo 58,9; seharusnya 64,2. Agent menyingkat termin menjadi "DP 30% sisa 30 hari", lalu script membacanya diam-diam sebagai pelunasan saat barang tiba (tempo hilang tanpa peringatan), sementara rincian tetap menulis "DP 30% + pelunasan 30 hari".

## Output SESUDAH konteks Telegram
> Udah aku hitung landed cost-nya (harga + ongkir + PPN) buat kebutuhan 180 kg dalam 6 hari:
>
> **Perbandingan 3 penawaran margarin: 180 kg, butuh dalam 6 hari**
> | Pemasok | Total bayar (per kg) | Selisih vs termurah | Skor (peringkat) |
> |---|---|---|---|
> | Toko Sumber Rejeki | Rp4.482.000 (Rp24.900) | termurah sementara | 86,5 (1) |
> | CV Lancar Jaya | Rp4.656.000 (Rp25.867) | lebih mahal Rp174.000 (3,9%) | 81,8 (2) |
> | PT Margarindo Prima | Rp5.283.600 (Rp29.353) | lebih mahal Rp801.600 (17,9%) | 58,9 (3, telat) |
>
> **Rekomendasi: Toko Sumber Rejeki** (peringkat 1)
> - Peringkat: 1. Toko Sumber Rejeki (skor 86,5), 2. CV Lancar Jaya (skor 81,8), 3. PT Margarindo Prima (skor 58,9, melewati tenggat).
> - Toko Sumber Rejeki adalah yang termurah (sementara: ongkir belum diketahui): Toko Sumber Rejeki lebih MURAH Rp174.000 daripada CV Lancar Jaya untuk 180 kg, termurah berikutnya.
> - Bila pesanan naik 2x (360 kg): termurah tetap Toko Sumber Rejeki (Rp8.964.000).
> - Bila Toko Sumber Rejeki telat sampai hari ke-8 (lewat tenggat 6 hari): rekomendasi pindah ke CV Lancar Jaya, yang lebih MAHAL Rp174.000 (3,9%) daripada Toko Sumber Rejeki.
> - Ongkir Toko Sumber Rejeki belum diketahui: tetap tidak lebih mahal daripada CV Lancar Jaya selama ongkirnya maksimal Rp174.000 untuk 180 kg (setara Rp966,67/kg).
> - Asumsi pajak: ongkir CV Lancar Jaya dianggap bagian dari harga yang sudah termasuk PPN.
>
> **Rincian singkat:**
> 1. Toko Sumber Rejeki — Rp24.900/kg, tanpa PPN (non-PKP), ongkir belum dihitung, kirim besok (1 hari), bayar COD.
> 2. CV Lancar Jaya — 180 kg dapat harga tingkat Rp25.333/kg (PPN sudah termasuk, PKP), ongkir Rp96.000 (8rb×12 dus), kirim 2 hari, tempo 14 hari.
> 3. PT Margarindo Prima — wajib beli 200 kg (sisa 20 kg modal tertahan ~Rp528.360), Rp23.800/kg belum PPN (+PPN jadi Rp29.353/kg efektif), ongkir gratis, kirim 5 hari kerja = 7 hari kalender → **lewat tenggat 6 hari**, DP 30% + pelunasan 30 hari.
>
> **Risiko:**
> - Toko Sumber Rejeki pemasok baru buat kamu, margarin curah (bukan kemasan pabrik) — kualitas/konsistensi perlu dicek, apalagi bayar COD tanpa tempo.
> - Ongkir Toko Sumber Rejeki belum pasti, bisa menggeser peringkat kalau ternyata mahal.
> - PT Margarindo lead time-nya mepet/lewat tenggat untuk kebutuhan 6 hari ini — baru cocok kalau stok lagi aman buat pesanan berikutnya.
>
> **Pesan WA (siap kirim):**
>
> *Ke Toko Sumber Rejeki:*
> "Selamat siang kak. Mau tanya, ongkir margarin curah 180 kg ke [isian: alamat/kecamatan] berapa ya? Terus harga Rp24.900/kg ini berlaku sampai kapan? Boleh tahu juga kualitas/mereknya apa, karena ini pesanan pertama kami — kalau ada rekomendasi ulasan pembeli lain boleh dishare. Terima kasih kak."
>
> *Ke CV Lancar Jaya:*
> "Selamat siang kak. Kalau kami ambil 12 dus (180 kg) sesuai harga Rp380rb/karton, apakah ongkirnya bisa digratiskan (franco)? Dan harga ini berlaku sampai kapan ya? Mohon info juga apakah bisa terbit faktur pajak atas nama usaha kami. Terima kasih."
>
> **Data yang belum ada:** [isian: ongkir Toko Sumber Rejeki ke alamat Anda]
> **Asumsi:** Usaha Anda dianggap bukan PKP, jadi PPN dari pemasok PKP dihitung sebagai biaya; harga bertingkat berlaku untuk seluruh jumlah yang dibeli.
>
> Disclaimer: perbandingan ini alat bantu keputusan pembelian, bukan nasihat pajak/hukum — pastikan harga, PPN, dan syarat sesuai faktur resmi.
>
> Tiga hal yang paling nentuin pilihan akhir:
> 1. Ongkir Toko Sumber Rejeki ke alamat kamu berapa?
> 2. Kamu udah pernah pakai margarin curah dari Toko Sumber Rejeki, atau ini pemasok baru buat kamu?
> 3. Mau siapkan CV Lancar Jaya sebagai cadangan kalau ongkir Toko Sumber Rejeki ternyata mahal atau kualitasnya kurang cocok?
