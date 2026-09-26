# Template Jawaban Analisis

Isi bagian dalam `< >` hanya dengan angka/teks dari keluaran `scripts/analisis.py`.

---

**Jawaban singkat:** <jawab langsung pertanyaan pengguna dalam 1–2 kalimat, dengan angka kunci>

<tabel Markdown dari script — tempel apa adanya>

**Temuan:**
1. <fakta terbesar + artinya bagi usaha, mis. "Sewa memakan hampir separuh biaya (48,9%)">
2. <perubahan/tren penting + penyebab yang terlihat di data, tanpa klaim sebab-akibat>
3. <hal yang perlu ditindaklanjuti / dicek>

**Saran grafik:** <saran dari script>. Cara cepat di Excel: blok tabel → *Insert* → <jenis grafik>.
Di Google Sheets: *Insert → Chart* → pilih <jenis grafik>.

**Perlu dicek:**
- <peringatan script 1, bahasa awam>
- <peringatan script 2>

_Asumsi: sheet <nama>, kolom nilai <nama>, kolom kategori <nama>, periode <…>._
_File hasil: <nama-file.csv> (bisa dibuka di Excel)._ ← hanya bila memakai `--keluar`

---

## Kalimat siap pakai
- Naik/turun: "<Periode B> <naik/turun> <x,x%> dibanding <periode A> (<Rp A> → <Rp B>)."
- Bagian dari total: "<Kategori> menyumbang <x,x%> dari total <Rp …>."
- Pareto: "<N> dari <M> <kategori> sudah mencakup ≥ 80% total — fokus di sini dulu."
- Rata-rata vs median: "Rata-rata <Rp …> tertarik oleh beberapa nilai besar; nilai 'biasa' (median) <Rp …>."
- Periode tidak penuh: "Data <bulan> baru sampai tanggal <d>, jadi belum bisa dibandingkan penuh."
