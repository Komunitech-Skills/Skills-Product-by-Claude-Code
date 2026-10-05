# Catatan pembuat — laporan-iklan-mingguan v1.0.2 (perbaikan N1 & N2, 2026-09-26)

- **Peran:** pembuat/perevisi skill, **bukan** penguji independen. Menindaklanjuti
  `examples/06-uji-ulang-v1.0.1.md` (uji ulang Akun B, skor 7/10, lulus bersyarat). `HASIL-UJI.md` dan
  file uji Akun B **tidak diubah**.
- **Lingkungan:** Linux, Python 3.11. Data reproduksi dibuat oleh `gen.py` di scratchpad `iklan2/`
  (bukan repo), meniru bentuk file K2, K12, dan K3 varian di laporan Akun B. Semua data fiktif.
- **Status turun ke `uji`.** Versi ini wajib diuji ulang oleh penguji independen sebelum naik ke beta.

## Reproduksi sebelum → sesudah

| ID | Kasus | v1.0.1 | v1.0.2 |
|---|---|---|---|
| N1 | Meta `Campaign name`+`Ad set name`+`Ad name`, 3 iklan di "Kamp", Advantage+ Catalog Rp 1.080.735 dengan `Results` kosong | 1 baris "Kamp"; saran "Belum ada kampanye yang menonjol"; catatan sel kosong menulis **Rp 4.423.002** | Dirinci per `Ad name`. **Advantage+ Catalog** di PERLU PERHATIAN no. 1 dan saran no. 1. Catatan: "kosong di 1 baris (Advantage+ Catalog) … biayanya (**Rp 1.080.735**)". Total tetap Rp 4.423.002 |
| N1 | Iklan sama di 2 ad set (K12) | "Kamp" 1 baris (atau Set0/Set1/Set2 bila tanpa `Campaign name`) | "Iklan Hijab (Set0)", "Iklan Hijab (Set1)", "Iklan Mukena". Total Rp 2.445.600 |
| N2 | Total Rp 500.001 berlabel `Total of 2 campaigns` / `Totals` / `Total Akun` | **Rp 1.000.001**, tanpa ⚠️, label tampil sebagai kampanye | **Rp 500.000**, 1 baris total dilewati dan dicatat |
| N2 | TikTok harian 21 baris, `Total of 3 campaigns` di kolom tanggal, biaya selisih Rp 0,01 | **Rp 6.399.400**; ⚠️ hanya "tanggal tidak terbaca" | **Rp 3.199.700**, periode 2026-09-14 s.d. 2026-09-20, tanpa ⚠️ tanggal palsu |
| N2 | Label tak dikenal sama sekali (`Σ semua`, Rp 650.001 vs 650.000) | Rp 1.300.001 tanpa ⚠️ | Rp 650.000 + ⚠️ "hampir sama (selisih ≤ 2%) … dianggap baris TOTAL" |

## Perubahan

**N1: level rincian.** Bila file memuat ≥ 2 kolom nama yang terisi dari hierarki iklan > grup iklan
(`Ad set name`/`Ad group name`/`Ad group`/`Nama set iklan`) > kampanye, script memakai level **paling
rinci**. Levelnya ditulis di Catatan beserta cara kembali ke rincian per kampanye
(`--kolom-nama "Campaign name"`). `--kolom-nama` dari pengguna tetap dihormati. Kolom yang kosong
semua dilewati, misalnya `Ad name` kosong sehingga `Ad set name` yang dipakai. Nama iklan yang sama di
induk berbeda diberi nama induk terdekat dalam kurung. JSON menambah `level_rincian` dan
`kolom_induk`.

Catatan sel kosong kini menghitung **baris** yang selnya kosong, termasuk jumlah baris dan biaya baris
itu sendiri. Sebelumnya yang dihitung adalah biaya seluruh kampanye bernama sama. Ini juga memperbaiki
R-b: data harian 7 baris kini tertulis "7 baris".

**N2: deteksi baris total dan pengaman silang.**
1. `jenis_label_total()` memeriksa kata kepala di awal sel (`total(s)`, `grand total(s)`,
   `sub total(s)`, `jumlah`, `summary`, `ringkasan`, `keseluruhan`, `overall`, `semua kampanye`,
   `all campaigns`), lalu menilai sisa teksnya:
   - **kuat:** tidak ada sisa, atau sisa diawali tanda baca/angka.
   - **sedang:** sisa hanya berisi kata cakupan (of, all, akun, account, campaigns, kampanye, iklan,
     keseluruhan, …) dan angka.
   - **lemah:** sisa berisi kata lain, misalnya "Total Look Hijab". Baris ini tetap dihitung.

   Label kuat dan sedang dilewati. Label sedang yang biayanya tidak ≈ jumlah baris lain diberi ⚠️
   ("bila itu kampanye sungguhan, ganti namanya").
2. **Pengaman silang angka.** Baris berbiaya terbesar dibandingkan dengan jumlah semua baris lain
   (minimal 2 baris lain berbiaya > 0):
   - Biaya, tayangan, dan klik sama persis → dibuang + ⚠️. Ini perilaku v1.0.1.
   - Ketiganya selisih ≤ 2% → dibuang + ⚠️ "hampir sama". Ini baru.
   - Hanya biayanya yang selisih ≤ 2% → **tetap dihitung**, tetapi diberi ⚠️ "TERHITUNG DUA KALI:
     seharusnya Rp X, bukan Rp Y". Ini baru.

   Batas 2% sengaja dibuat sempit. Dengan begitu, kampanye dominan (mis. 90% dari jumlah baris
   lain) tidak memicu ⚠️ palsu, dan kampanye berlabel "Total …" dengan anggaran bulat tidak dibuang
   diam-diam.

Semua hitungan tetap `Decimal`. Pembulatan tidak berubah: rupiah dan persen dibulatkan ke terdekat
(0,5 menjauhi nol).

## Tes
- `python3 tests/uji_regresi.py`: **63 tes OK**, yaitu 49 lama (tidak ada yang diubah) + 14 baru
  (`UjiN1LevelRincian` 6, `UjiN2BarisTotal` 8).
- 14 tes baru dijalankan terhadap salinan `laporan_iklan.py` v1.0.1 (HEAD sebelum commit ini) di
  scratchpad. Hasilnya **13 gagal**. Yang lulus adalah tes penjaga
  `test_kampanye_dominan_tidak_diberi_peringatan_palsu`, yang memang harus tetap lulus.
- `python3 scripts/validate.py --skill laporan-iklan-mingguan`: ✅ valid.
- `bash scripts/uji_openclaw.sh` tidak dijalankan ulang karena frontmatter tidak berubah.

## Belum ditangani (rendah, dari 06)
- **R-a:** `Nilai konv.` (Google UI Indonesia) belum dikenali, dan platform "Tidak diketahui" untuk
  UI Indonesia.
- **R-c:** `Periode Data` di baris info Shopee belum dipakai.
- **R-d:** `--omzet -5jt` tanpa `=` masih jatuh ke pesan argparse Inggris.

## Saran untuk penguji independen berikutnya
Ulangi K2, K12, K3 varian, dan matriks label N2 dengan file buatan sendiri. Coba juga:
- label total lain (bahasa campur, huruf besar/kecil);
- ekspor TikTok `Ad group name`/`Ad name` dan Google `Ad group`;
- kampanye asli yang biayanya kebetulan ≈ jumlah kampanye lain. Yang diharapkan: hanya ⚠️, tidak
  dibuang.
