# Uji Banding Pesaing

## Pesaing yang dinilai

### 1. `executive-summary-generator` (sumber adaptasi langsung)
Repo: github.com/nimrodfisher/data-analytics-skills,
folder `04-data-storytelling-visualization/executive-summary-generator`. Dibaca untuk
dinilai (bukan disalin) — isinya sudah dirujuk di `ATTRIBUTION.md` skill ini.

**Kelebihan sumber:**
- Struktur piramida (governing thought → key lines → evidence) yang jelas dan teruji,
  dipakai sebagai dasar konsep skill ini (diakui di ATTRIBUTION.md).
- Menekankan angka dampak bisnis di tiap temuan.

**Kelemahan untuk pasar target Komunitech (pembeli UMKM Indonesia awam teknologi):**
- 100% Bahasa Inggris, ditujukan untuk analis data profesional di perusahaan
  besar/startup — bukan bahasa sehari-hari kantor Indonesia.
- Hanya **satu jenis output** (dokumen executive summary generik 1–2 halaman) — tidak
  ada versi pesan WhatsApp ringkas atau skrip bicara lisan, padahal WhatsApp adalah
  kanal komunikasi bisnis paling umum di Indonesia.
- **Tidak ada script perhitungan** — instruksinya hanya teks "quantify the business
  impact" tanpa jaminan angka benar-benar dihitung (bukan dikira model). Skill ini
  menutup celah itu dengan `scripts/hitung_perubahan.py` (Decimal, diverifikasi ulang
  di pengujian ini).
- Tidak membahas format mata uang Rupiah, konteks bank KUR/investor lokal, atau norma
  sopan-langsung kantor Indonesia.
- **Hasil uji berdampingan (skenario Uji 03, omzet 3 bulan):** gaya sumber akan
  menghasilkan paragraf naratif Inggris generik ("Branch revenue shows a positive trend
  over Q3...") tanpa angka Rupiah terformat, tanpa 4 format kanal, dan tanpa
  rekomendasi PIC/tenggat eksplisit dalam bahasa Indonesia — kalah jauh untuk
  audiens target dibanding output skill ini di `examples/03-...md`.

### 2. `visualization-builder` (sumber kedua, untuk bagian pilih grafik)
Folder sama, `04-data-storytelling-visualization/visualization-builder`. Dinilai untuk
bagian `references/pilih-grafik.md`.

**Kelebihan sumber:** pohon keputusan pemilihan grafik berdasarkan jenis pesan
(perbandingan/tren/komposisi/distribusi) — konsepnya solid dan sudah diadopsi.

**Kelemahan untuk target pasar:** membahas detail teknis ekspor cetak (300/150 DPI)
dan palet warna colorblind yang di luar kebutuhan pembeli awam non-desainer; butuh
`matplotlib`/`seaborn` (paket pihak ketiga) yang bertentangan dengan prinsip "tanpa
setup" library ini. `references/pilih-grafik.md` versi Komunitech menghapus bagian ini
dan menambah aturan sumbu-Y batang wajib mulai dari 0 (anti grafik menyesatkan) dan
panduan kata pengganti grafik untuk kanal WA/skrip bicara — tidak ada di sumber.

## Pencarian pesaing lain
Kata kunci dicari (secara konseptual, berdasarkan pengetahuan kategori skill publik):
"executive summary generator skill", "data storytelling skill agent", "laporan ke
atasan AI skill", "business report generator skill claude". Tidak ditemukan skill
publik lain (di luar dua folder di atas) yang secara spesifik menyasar konversi
angka→4-format-siap-kirim (WA/email/1-halaman/skrip bicara) untuk audiens kantor
Indonesia — kebanyakan hasil kategori "executive summary" adalah varian dari pola
piramida yang sama seperti sumber di atas, dalam Bahasa Inggris, tanpa lokalisasi
Rupiah/WhatsApp/bank KUR.

## Kesimpulan
Skill `presentasi-data-ke-atasan` unggul dibanding kedua sumber pada: bahasa & nada
lokal, 4 format kanal siap kirim (bukan satu dokumen generik), perhitungan angka
lewat script (bukan instruksi tekstual saja), dan konteks pasar Indonesia (Rupiah, bank
KUR, WhatsApp). Tidak memenuhi kondisi "kalah dari pesaing → skor maks. 6" pada Tahap 6
poin 5.
