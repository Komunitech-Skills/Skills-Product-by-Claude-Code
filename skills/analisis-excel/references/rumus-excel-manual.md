# Langkah Manual & Rumus Excel yang Setara

Dipakai bila Python tidak bisa dijalankan. Hasil manual **belum diverifikasi script** — sampaikan
ini ke pengguna. Rumus ditulis untuk Excel/Google Sheets berbahasa Inggris; di Excel berbahasa
Indonesia pemisah argumen biasanya `;` (bukan `,`).

Misalkan data di sheet `Data`, judul kolom di baris 1, data baris 2–500:
A = Tanggal, B = Kategori, C = Keterangan, D = Nominal.

## 0. Rapikan data dulu (setara `bersihkan`)
| Masalah | Solusi di Excel |
|---|---|
| Spasi berlebih di teks | Kolom bantu `=TRIM(B2)` lalu salin → *Paste Values* |
| Huruf besar-kecil beda ("kopi" vs "Kopi") | `=PROPER(TRIM(B2))` (atau `UPPER`) |
| Angka tersimpan sebagai teks "Rp 1.234.567,89" | Excel ID: *Data → Text to Columns* atau `=VALUE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(D2;"Rp";"");".";"");",";"."))` di Excel Inggris. Cek hasilnya! |
| Tanggal teks "25/09/2026" tidak dikenali | `=DATE(RIGHT(A2;4); MID(A2;4;2); LEFT(A2;2))` (hanya untuk format dd/mm/yyyy yang rapi) |
| Baris "TOTAL" di bawah tabel | Hapus barisnya atau jangan ikutkan dalam rentang rumus (agar tidak terhitung dua kali) |
| Sel gabungan (merge) di kolom kategori | Blok kolom → *Unmerge* → *Go To Special → Blanks* → ketik `=` + sel di atasnya → Ctrl+Enter |

## 1. Profil (setara `profil`)
| Pertanyaan | Rumus |
|---|---|
| Banyak baris berisi | `=COUNTA(B2:B500)` |
| Sel kosong | `=COUNTBLANK(D2:D500)` |
| Nilai unik (Excel 365/Sheets) | `=COUNTA(UNIQUE(B2:B500))` |
| Baris duplikat | *Data → Remove Duplicates* (catat jumlah yang dihapus), atau kolom bantu `=COUNTIFS(A:A;A2;B:B;B2;D:D;D2)>1` |
| Outlier (IQR 1,5×) | Q1 `=QUARTILE.INC(D2:D500;1)`, Q3 `=QUARTILE.INC(D2:D500;3)`, batas bawah `=Q1-1,5*(Q3-Q1)`, batas atas `=Q3+1,5*(Q3-Q1)`; hitung `=COUNTIF(D2:D500;">"&batas_atas)+COUNTIF(D2:D500;"<"&batas_bawah)` |

Script memakai metode yang sama dengan `QUARTILE.INC` / `PERCENTILE.INC`.

## 2. Ringkasan (setara `ringkas`)
`=SUM(D2:D500)`, `=AVERAGE(D2:D500)`, `=MEDIAN(D2:D500)`, `=MIN(D2:D500)`, `=MAX(D2:D500)`,
`=COUNT(D2:D500)` (banyak angka). Rentang tanggal: `=MIN(A2:A500)` & `=MAX(A2:A500)` (format sel
sebagai tanggal).

## 3. Pivot / group-by (setara `pivot`)
- Cara termudah: blok tabel → *Insert → PivotTable* → seret Kategori ke **Rows**, Nominal ke
  **Values** (Sum). Ganti ke Average/Count lewat *Value Field Settings*.
- Rumus: `=SUMIFS(D:D; B:B; "Sewa")`, rata-rata `=AVERAGEIFS(D:D; B:B; "Sewa")`,
  banyak baris `=COUNTIFS(B:B; "Sewa")`. % dari total = jumlah kategori ÷ `SUM(D:D)`.
- Per bulan: kolom bantu `=TEXT(A2;"yyyy-mm")` lalu SUMIFS pada kolom bantu itu, atau di
  PivotTable klik kanan tanggal → *Group → Months + Years*.

## 4. Tren (setara `tren`)
Jumlah per bulan (lihat poin 3), lalu perubahan vs bulan sebelumnya:
`=(Bulan_ini - Bulan_lalu) / Bulan_lalu` (format %). Bila bulan lalu 0 → tulis "tidak dihitung",
jangan dibagi nol. Periksa bulan pertama/terakhir apakah penuh (tanggal awal = 1 dan tanggal akhir
= akhir bulan); bila tidak, beri catatan.

## 5. Top-N (setara `top`)
PivotTable → urutkan Values dari terbesar → *Filter → Top 10*. Atau Excel 365:
`=TAKE(SORTBY(UNIQUE(B2:B500); SUMIFS(D2:D500;B2:B500;UNIQUE(B2:B500)); -1); 10)`.
% kumulatif (Pareto) = jumlah berjalan ÷ total.

## 6. Banding dua periode (setara `banding`)
`=SUMIFS(D:D; A:A; ">="&DATE(2026;8;1); A:A; "<="&DATE(2026;8;31))` untuk Agustus, sama untuk
September. Selisih = B − A; perubahan % = (B − A) ÷ A. Periode beda panjang → bandingkan juga
rata-rata per hari (jumlah ÷ banyak hari kalender).

## 7. Pembulatan
Tampilkan rupiah `=ROUND(x;0)`, persen 1 desimal `=ROUND(x*100;1)`. `ROUND` Excel membulatkan
0,5 menjauhi nol — sama dengan script.
