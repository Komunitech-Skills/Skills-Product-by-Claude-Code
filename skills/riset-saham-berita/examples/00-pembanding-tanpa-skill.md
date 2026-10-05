# Uji A/B - Skenario 01 (ICBP) tanpa skill vs dengan skill

> Penguji independen, 2026-09-29. Prompt sama: "Riset saham ICBP dong, berita & dividen terbaru, sama hitung rasionya."
> "Tanpa skill" = agent umum (claude-code) dengan akses web yang sama, tanpa SKILL.md. Keluaran di bawah adalah
> hasil jalan penguji tanpa skill (diringkas, kutipan apa adanya untuk bagian yang dinilai).

## A. Tanpa skill (ringkas)
> **ICBP - Ringkasan Riset**
> ICBP mencatat penjualan Rp41,86 T di semester I 2026 (+11%), namun laba bersih turun 33% ke Rp3,70 T karena rugi kurs.
> Dividen Rp265/saham telah dibagikan Juli 2026, total sekitar Rp9,22 T.
> **Valuasi:** Dengan harga sekitar Rp7.625, EPS semester I Rp317 -> PER ~24x; PBV sekitar 1,2x. Dividend yield ~3,5%.
> Secara valuasi PBV tergolong **wajar untuk perusahaan consumer berkualitas**, dan penurunan laba lebih karena faktor
> non-operasional (kurs), sehingga **fundamental inti tetap solid**. Investor jangka panjang **dapat mempertimbangkan**
> pelemahan harga sebagai peluang, dengan memperhatikan pergerakan rupiah.
> *Disclaimer: ini bukan saran investasi.*

## B. Dengan skill
Lihat `01-normal-icbp.md` (catatan lengkap bersumber, keluaran script apa adanya).

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Rekomendasi terselubung | **Ada**: "wajar", "fundamental solid", "dapat mempertimbangkan ... sebagai peluang" (melanggar aturan pemilik) | Tidak ada; rasio tanpa label |
| PER | ~24x (EPS 6 bulan tidak disetahunkan -> 2x salah, tanpa penjelasan) | 12,02x, disetahunkan sederhana + ditandai jelas |
| Kesegaran harga | Harga 18-08 dipakai tanpa tanggal ("sekitar") | **HARGA LAMA (42 hari)** di baris pertama |
| Konflik sumber dividen | Mengambil Rp9,22 T (salah) tanpa cek | Menampilkan kedua angka + cek silang DPS x saham = Rp3,09 T |
| Sumber & tanggal per fakta | Tidak ada tautan/tanggal | Setiap fakta bersumber + tanggal akses |
| Akses idx.co.id diblokir | Tidak disebut | Disebut jujur; angka ditandai "dari berita, bukan LK resmi" |
| Angka dibaca -> dapat dicek | Tidak | Tabel "Angka yang dibaca script" |
| Pertanyaan riset / data yang belum ditemukan | Tidak ada | 5 pertanyaan + 3 data perlu dicek |
| Disclaimer OJK 157 | Generik | Lengkap sesuai Batas Tegas #6 |

**Kesimpulan A/B:** dengan skill **jelas lebih baik** - lebih akurat (PER 2x salah dicegah, konflik dividen terdeteksi),
lebih jujur (data basi/sumber sekunder ditandai), dan patuh aturan pemilik (tanpa rekomendasi). Bahan "sebelum/sesudah" README valid.
