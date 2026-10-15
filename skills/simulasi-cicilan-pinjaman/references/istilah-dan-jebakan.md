# Istilah & Jebakan Umum Cicilan (bahasa awam)

> Dimuat bila pengguna bertanya arti istilah atau bila perlu menjelaskan jebakan. Angka contoh di sini dihitung dengan rumus di `scripts/cicilan.py` (data fiktif).

## Istilah
| Istilah | Arti sederhana |
|---|---|
| Pokok | Uang yang dipinjam (harga − DP). |
| Tenor | Lama cicilan (bulan/tahun/hari). |
| Bunga flat | Bunga dihitung dari **pokok awal** setiap bulan, walau utang sudah berkurang. Cicilan tetap. Umum di leasing motor/mobil/elektronik dan koperasi. |
| Bunga efektif / anuitas | Bunga dihitung dari **sisa utang**. Cicilan tetap, porsi bunga mengecil dan porsi pokok membesar tiap bulan. Umum di KPR dan kredit bank. |
| Bunga efektif setara (EIR/APR) | Satu angka per tahun yang menyamakan semua penawaran: memperhitungkan cara hitung bunga **dan** biaya di muka/bulanan, dihitung dari uang yang benar-benar diterima. Angka inilah yang adil untuk membandingkan. |
| Versi majemuk | (1 + bunga per bulan)^12 − 1. Sedikit lebih tinggi; info tambahan. |
| Provisi | Biaya persen dari pokok, biasanya dibayar/dipotong di awal. |
| Fixed lalu floating | KPR: bunga tetap beberapa tahun pertama, lalu mengikuti bunga pasar. Cicilan bisa naik besar. |

## Jebakan umum (sampaikan netral, dengan angka)
1. **"Bunganya cuma 0,8% per bulan"** — bila flat, 0,8% × 12 = 9,6% per tahun dari pokok awal, setara bunga efektif **±17,3% per tahun** (tenor 12 bulan; ±17,25% untuk 36 bulan). Selalu tanyakan "flat atau efektif?".
2. **Biaya di muka** (admin, provisi, asuransi) membuat bunga efektif setara naik. Contoh fiktif: pinjaman Rp20.000.000, 36 bulan, flat 0,8%/bulan, admin Rp1.000.000 → setara ±17,25% menjadi ±20,97% per tahun.
3. **Dipotong saat cair** — "cair 2 juta" tetapi diterima 1,9 juta, sedangkan bunga dihitung dari 2 juta.
4. **Biaya ikut dicicil** — admin/asuransi ditambahkan ke pinjaman ikut kena bunga.
5. **Bunga 0% tetapi harga kredit lebih tinggi dari harga tunai** — bandingkan total harga lewat kredit dengan harga tunai; selisihnya adalah biaya pinjaman.
6. **KPR fixed murah** — hitung juga cicilan setelah masa fixed dengan beberapa angka floating dari pengguna (ilustrasi berlabel).
7. **Pinjaman harian** — 0,3% per hari terdengar kecil, tetapi 14 hari = 4,2% dari pokok; per tahun ratusan persen. Tambah biaya potong di muka, makin besar.
8. **Denda telat** — tarif per hari dikali tunggakan; tanyakan dasar denda (dari cicilan atau dari pokok) di perjanjian.
9. **Gali lubang tutup lubang** — meminjam baru untuk bayar cicilan lama menambah biaya; arahkan bicara dengan pemberi pinjaman soal restrukturisasi.

## Patokan cicilan aman
Semua cicilan (termasuk yang sudah berjalan) **maks. 30% penghasilan bersih**; 30–35% = waspada; > 35% = berat. Ini patokan hati-hati yang dipakai sebagai asumsi (bukan aturan resmi untuk semua lembaga); sesuaikan bila tanggungan keluarga besar.

Catatan khusus pinjaman daring konsumtif: SEOJK No. 19/SEOJK.06/2025 Romawi XIII angka 2 meminta penyelenggara menilai perbandingan seluruh pembayaran pokok + manfaat ekonomi (ke semua kreditur) dengan penghasilan peminjam, paling tinggi 40% pada 2025 dan 30% sejak 2026. Itu aturan penilaian bagi penyelenggara pinjaman daring, bukan aturan untuk bank atau leasing; patokan 30% di atas tetap asumsi hati-hati skill ini.

## Batas biaya pinjaman daring (pinjol/LPBBTI) — cek ulang sebelum dipakai
**Dasar:** SEOJK No. 19/SEOJK.06/2025 tentang Penyelenggaraan Layanan Pendanaan Bersama Berbasis Teknologi Informasi, Romawi XIV angka 2–3, ditetapkan dan berlaku sejak **31 Juli 2025**. SEOJK No. 19/SEOJK.06/2023 (termasuk jadwal turunnya batas yang ada di dalamnya) sudah **dicabut** oleh SEOJK 2025 itu (Romawi XXII angka 1) — jangan dipakai lagi.

Batas dihitung **per hari kalender dari nilai pinjaman (nilai pendanaan) yang tercantum di perjanjian**:

| Jenis & nilai pinjaman | Tenor sampai 6 bulan | Tenor di atas 6 bulan |
|---|---|---|
| Konsumtif | 0,3% per hari | 0,2% per hari |
| Produktif, nilai paling tinggi Rp50 juta | 0,275% per hari | 0,1% per hari |
| Produktif, nilai di atas Rp50 juta | 0,1% per hari | 0,1% per hari |

- **Yang dibatasi ("manfaat ekonomi"):** bunga/margin + biaya administrasi/komisi/fee platform + biaya lain, **selain** denda keterlambatan, biaya tanda tangan elektronik yang diamankan sertifikat elektronik, dan pajak (Romawi XIV angka 2).
- **Cara hitung** (mengikuti simulasi di SEOJK yang sama): total manfaat ekonomi ÷ (nilai pinjaman × jumlah hari tenor). Contoh: pinjaman Rp2.000.000, 14 hari, bunga 0,3%/hari (Rp84.000) + admin Rp100.000 dipotong saat cair → Rp184.000 ÷ (Rp2.000.000 × 14) = 0,657% per hari, di atas batas konsumtif 0,3%.
- **Asumsi skill ini:** "6 bulan" dihitung 180 hari (simulasi SEOJK menghitung tenor 5 bulan = 150 hari dan 7 bulan = 210 hari). Untuk tenor 181–184 hari, hasil hitungan memberi catatan: bila perjanjian menyebut tenornya 6 bulan, pakai batas tenor sampai 6 bulan.
- Hitungan otomatis hanya untuk pinjaman bertenor hari (dibayar sekali di akhir). Untuk pinjaman daring yang dicicil bulanan, jangan menyimpulkan lolos/tidak lolos batas; sampaikan biayanya dan arahkan ke OJK.

Aturan ini sudah pernah diganti (SEOJK 2023 dicabut oleh SEOJK 2025), dan OJK dapat mengevaluasi batasnya secara berkala (Romawi XIV angka 7). Di balasan selalu tulis "cek aturan OJK terbaru di ojk.go.id" dan ajak cek legalitas penyelenggara (Kontak OJK 157). Bila pengguna tidak menyebut jenisnya, hitungan memakai konsumtif dan mencatatnya sebagai asumsi (pinjaman untuk modal usaha = produktif, batasnya berbeda). Bila nilai pinjaman di perjanjian tidak jelas, jangan sebut angka batas; cukup sampaikan biaya per hari hasil hitungan dan arahkan ke OJK. Angka dan nomor bagian dicocokkan dengan teks PDF resmi SEOJK 19/SEOJK.06/2025 di ojk.go.id (verifikasi Komunitech 2026-10-15).

## Kredit bank: minta konversi flat → efektif tertulis
Untuk kredit dari **bank umum konvensional**, POJK No. 13 Tahun 2024 (Transparansi dan Publikasi Suku Bunga Dasar Kredit bagi Bank Umum Konvensional) mengarahkan bank memberi tahu nasabah konversi bunga flat ke setara efektif dalam surat penawaran kredit (*offering letter*). Aturan ini untuk bank umum konvensional, bukan untuk leasing non-bank; untuk penawaran selain dari bank tetap minta rincian bunga dan biaya tertulis, lalu hitung bunga efektif setara dengan skill ini.

## Bahan rujukan bagi pengguna
- Daftar penyelenggara pinjaman daring berizin: situs resmi OJK (ojk.go.id), Kontak OJK 157.
- Tabel angsuran resmi & rincian biaya tertulis dari lembaga pembiayaan sebelum tanda tangan.
