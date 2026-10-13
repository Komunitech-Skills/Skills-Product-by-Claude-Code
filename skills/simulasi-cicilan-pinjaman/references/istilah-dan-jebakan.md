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

## Batas biaya pinjaman daring (pinjol/LPBBTI) — cek ulang sebelum dipakai
| Jenis | Batas yang dicatat untuk 2026 (tenor > 6 bulan) | Dasar |
|---|---|---|
| Konsumtif | 0,1% per hari | SEOJK No. 19/SEOJK.06/2023 (penurunan bertahap: 0,3% 2024 → 0,2% 2025 → 0,1% 2026) |
| Produktif | 0,067% per hari | SEOJK yang sama |

Akhir 2024 OJK menyesuaikan batas manfaat ekonomi berdasarkan **tenor pinjaman** (≤ 6 bulan vs > 6 bulan). Angka di tabel berlaku untuk tenor > 6 bulan; untuk tenor ≤ 6 bulan (termasuk pinjaman harian 7–30 hari) angkanya tidak dicatat di sini — jangan dikarang, tulis "cek aturan OJK terbaru". Nomor SEOJK diverifikasi di ojk.go.id (2026-10-06); angka dicatat dari riset internal Komunitech (26 September 2026). Batas ini mencakup bunga dan biaya lain ("manfaat ekonomi"). Aturan dapat berubah — di balasan selalu tulis "cek aturan OJK terbaru di ojk.go.id" dan ajak cek legalitas penyelenggara (Kontak OJK 157). Bila ragu, jangan sebut angka batas; cukup sampaikan biaya per hari hasil hitungan dan arahkan ke OJK.

## Bahan rujukan bagi pengguna
- Daftar penyelenggara pinjaman daring berizin: situs resmi OJK (ojk.go.id), Kontak OJK 157.
- Tabel angsuran resmi & rincian biaya tertulis dari lembaga pembiayaan sebelum tanda tangan.
