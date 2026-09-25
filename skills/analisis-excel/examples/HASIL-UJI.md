# HASIL UJI — analisis-excel (Tahap 6, penguji independen)

- **Tanggal:** 2026-09-25 · **Penguji:** agent terpisah dari pembuat, hanya membaca folder skill
  (plus sekilas `skills/rekap-penjualan-csv/SKILL.md` untuk cek batas cakupan).
- **Lingkungan:** Linux, Python 3.11.15, tanpa openpyxl/pandas. Skill disalin ke scratchpad dan dijalankan dari sana.
- **Platform teruji:** `claude-code (simulasi agent)` saja.
- **Fixture:** `examples/buat_fixture_uji.py` (deterministik; XLSX ditulis tangan meniru Excel, dicek
  bisa dibuka openpyxl/pandas). LibreOffice headless di lingkungan uji gagal memuat file apa pun, jadi tidak dipakai.
- **Tes bawaan:** `python3 tests/uji_regresi.py` → **26 tes OK**.

## Ringkasan skenario
| # | Skenario | Hasil | File |
|---|---|---|---|
| 01 | Toko bangunan, XLSX 3 sheet kuartal + sheet tersembunyi, 499 baris, Rp teks, rumus tanpa nilai, TOTAL | Semua angka cocok kunci; **perlu improvisasi untuk gabung sheet** | `01-toko-bangunan-xlsx-3-sheet.md` |
| 02 | HRD lembur CSV cp1252 `;` | Angka cocok; ambiguitas "rata-rata" & kolom Baris menyesatkan | `02-hrd-lembur-csv-cp1252.md` |
| 03 | Bendahara iuran, header baris 4, kosong, duplikat | Total cocok; "4 A" ≠ "4A" memecah pivot kelas | `03-bendahara-iuran-header-baris4.md` |
| 04 | Input tidak lengkap | ✔ tanya sekali, default jelas, pesan GAGAL awam | `04-input-tidak-lengkap.md` |
| 05 | ML / 2 GB / NIK & gaji dikirim keluar | ✔ ditolak/diarahkan; script tidak menahan output per orang | `05-di-luar-cakupan.md` |
| A/B | Tanpa vs dengan skill (skenario 01) | Dengan skill **jelas lebih baik** (tanpa skill: total dobel, 4 bulan salah) | `00-pembanding-tanpa-skill.md` |
| Pesaing | anthropics/skills `xlsx` (+pandas) | Skill kita **unggul** 4,5 vs 2,3; ClawHub/skills.sh diblokir proxy → perlu diulang | `00-banding-pesaing.md` |

## Verifikasi angka independen (parser/kunci sendiri, tanpa membaca kode script)
- **Skenario 01–03:** jumlah, rata-rata, median, min/max, pivot kategori/divisi/kelas, tren 9 bulan,
  % perubahan (Q3/Q2 −28,8%, bulan-ke-bulan), top-5, Pareto % → **semua cocok** (tabel di tiap file).
  Nomor baris outlier & sel rumus kosong dicek dengan openpyxl: benar.
- **Tanggal serial 1900:** 1→1900-01-01, 59→1900-02-28, **60→ditandai tidak valid + peringatan** (29-Feb-1900 palsu),
  61→1900-03-01, 46290→2026-09-25, 46290,75→2026-09-25 (jam dibuang), 0,5 berformat tanggal → "12:00" dilaporkan tidak valid. ✔
- **Tanggal serial 1904:** 0→1904-01-01, 59→1904-02-29, 60→1904-03-01, 44828→2026-09-25; workbook 1904 penuh memberi tren identik dengan versi 1900. ✔
- **Angka:** `1.234.567,89`→1234567,89 · `Rp 1.250.000,-`→1250000 · `(1.000)`→−1000 · `-Rp 5.000`/`5.000-`→−5000 ·
  `Rp. 25000`/`IDR 25.000`→25000 · `1 234 567`→1234567 · `12,5%`→12,5 · `15.000.00`, `1,5E+06`, `US$ 5`, `1,5jt`, `2 juta` → tidak valid & dilaporkan.
  Jumlah terpaksa-angka Rp 5.258.147 = hitungan sendiri 5.258.147,39 ✔. Catatan: kolom campuran ini jatuh ke tipe
  "teks" tanpa `--tipe` (≥70% aturan) — sesuai dokumentasi.
- **Data rusak:** file kosong / hanya BOM / hanya header, XLSX korup, XLSX terpotong, ".xlsx" berisi teks, workbook tanpa sheet,
  file tidak ada, sheet tidak ada, kolom tidak ada, kolom teks untuk `--nilai`, tidak ada kolom tanggal untuk `tren` →
  semua `GAGAL:` awam, kode 2, tanpa traceback. ✔ **Kecuali tanda kutip tak tertutup (bug #2).**
  `.xls` palsu berisi CSV tetap terbaca (deteksi berdasarkan isi) ✔. Injeksi rumus CSV (`=`,`+`,`@`) diberi `'` ✔.

## Bug & temuan (berprioritas)
| # | Prioritas | Temuan | Lokasi | Usulan perbaikan |
|---|---|---|---|---|
| 1 | **P1** | Tidak ada analisis lintas sheet. Workbook "satu sheet per bulan/kuartal" sangat umum di UMKM; pertanyaan Jan–Sep memaksa agent menjumlah sendiri (melanggar "Jangan mengarang angka") atau berimprovisasi (bersihkan→gabung CSV, peringatan per sheet hilang). | `scripts/analisis.py` `baca_grid`/`--sheet`; SKILL.md Langkah kerja | Tambah `--sheet semua` / `--sheet "Q1,Q2,Q3"`: gabung sheet yang judul kolomnya sama, tambah kolom `Sheet`, kumpulkan peringatan per sheet. Dokumentasikan di SKILL.md + contoh. |
| 2 | **P1** | CSV dengan tanda kutip tak tertutup **diam-diam menelan semua baris berikutnya** ke satu sel: `Ani,5000 / "Budi,6000 / Cici,7000 / …` → total Rp 5.000 (seharusnya 35.000), kode 0, tanpa peringatan. `references/format-didukung.md` menjanjikan pesan "CSV rusak". | `baca_csv` | Parse dengan `strict=True` atau deteksi sel berisi baris baru + pemisah/sel sangat panjang → `GAGAL: CSV rusak (tanda kutip tidak tertutup di sekitar baris N)`. Tambah tes regresi. |
| 3 | P2 | Kolom "Baris" di `pivot`/`top` menghitung baris termasuk nilai kosong, sementara rata-rata/jumlah memakai nilai terisi (Produksi 135 vs pembagi 133; Q2 171 vs 170). Tidak ada peringatan sel kosong di `pivot`. | `cmd_pivot`, `cmd_top` | Tambah kolom "Terisi" atau hitung Baris = terisi; peringatan "N sel kosong tidak dihitung". |
| 4 | P2 | Privasi: `top --grup NIK` menampilkan NIK lengkap; `top --grup Nama --nilai "Gaji Pokok"` menampilkan gaji per orang. Referensi mengklaim label sensitif tidak ditampilkan di `top`. | `cmd_top` | Samarkan label kolom sensitif (`3201…2408`) dan beri peringatan tegas saat nilai sensitif ditampilkan per orang; atau selaraskan dokumentasi. |
| 5 | P2 | Penyeragaman kategori hanya huruf besar-kecil/spasi tepi; `4 A` vs `4A` (juga "Cab. Bogor"/"Cabang Bogor") tetap terpisah → pivot kelas pecah jadi 9 baris. | `_ketik` / penyeragaman teks | Kunci pembanding tanpa spasi internal (dan tanpa titik) untuk usulan penggabungan + laporkan. |
| 6 | P2 | Duplikat & sel kosong hanya diperingatkan di `profil`; `pivot`/`top` yang angkanya terpengaruh tidak menyebutnya. | peringatan per subperintah | Ulangi peringatan duplikat/kosong di semua subperintah yang menghitung. |
| 7 | P3 | `banding` dua sheet file yang sama berlabel "A: Penjualan 2026.xlsx vs B: Penjualan 2026.xlsx"; baris "Sumber" hanya menyebut sheet A. | `_data_banding` label | Default label = nama sheet bila file sama. |
| 8 | P3 | Tidak ada deteksi duplikat berdasarkan kunci (NIS+Bulan) — dobel "dobel input?" lolos (+Rp 50.000). | `bersihkan` | Opsi `--kunci-duplikat "NIS,Bulan"` (lapor saja, tidak hapus diam-diam). |
| 9 | P3 | Tidak ada hitung-unik / rata-rata per entitas (rata jam lembur per karyawan). SKILL.md tidak menyuruh agent menanyakan arti "rata-rata". | SKILL.md Aturan penting; `--fungsi` | Tambah `--fungsi unik` atau `--per-entitas "Nama"`; aturan: tanya "rata-rata per catatan atau per orang?". |
| 10 | P3 | Kolom teks nama bulan (Juli/Agustus/September) diurut abjad di `--kolom-pivot`/pivot. | urutan pivot | Kenali nama bulan ID/EN sebagai urutan kronologis. |
| 11 | P3 | Pivot dengan nilai negatif menghapus kolom "% dari total" tanpa penjelasan. | `cmd_pivot` | Tambah catatan "persen tidak ditampilkan karena ada nilai negatif (retur)". |
| 12 | P3 | Peringatan periode tidak penuh muncul hanya karena tidak ada transaksi pada 1 Jul ("data 2 Jul s.d. 30 Sep"). | `cmd_banding` | Toleransi beberapa hari di tepi periode, atau ubah kalimat menjadi "data pertama 2 Jul". |
| 13 | P3 | "5 nilai tidak valid" tetapi hanya 4 contoh disebut, tanpa "dll."; baris CSV berkolom lebih (koma tak dikutip) diam-diam membuat "Kolom C"; saran "Histogram kolom angka" muncul walau tak ada kolom angka; `1,5jt`/`2 juta` tidak didukung (dilaporkan). | berbagai | Perhalus pesan; peringatan jumlah kolom tidak konsisten; pertimbangkan dukungan `rb/jt/juta`. |

Tidak ditemukan: perintah berbahaya, akses jaringan, pembacaan kredensial, prompt injection. File asli tidak diubah.

## Cakupan vs `rekap-penjualan-csv`
Batasnya jelas di description & "Kapan TIDAK" (penjualan kasir/marketplace dengan status pesanan → rekap-penjualan-csv).
Namun skenario 01 (file penjualan toko dari Excel) wajar jatuh ke analisis-excel karena rekap-penjualan-csv
menolak `.xlsx`. Usul: di SKILL.md tulis "data penjualan buatan sendiri di Excel → skill ini; ekspor
Shopee/Tokopedia/kasir berstatus pesanan → rekap-penjualan-csv".

## Skor kualitas: **7 / 10** — lulus bersyarat
Alasan:
- (+) Semua angka di 3 skenario normal, tanggal serial 1900/1904 (termasuk serial 60), format angka Indonesia,
  dan data rusak diverifikasi cocok; pesan galat awam; Python standar saja; peringatan transparan.
- (+) A/B jelas lebih baik (tanpa skill: total 2× lipat, 4 bulan salah); unggul atas anthropics/skills `xlsx`.
- (−) Bug #2 memberi **angka salah tanpa peringatan** (melanggar prinsip Reliable), walau pemicunya jarang.
- (−) Gap #1 membuat skenario utama (workbook per periode) tidak bisa dijawab murni lewat script.
- (−) Privasi di `top` (#4) bergantung pada kepatuhan agent.

**Rekomendasi:** perbaiki #1 dan #2 (dan idealnya #3–#5) sebelum status `lulus`, lalu uji ulang singkat
oleh penguji independen (skenario 01 dengan `--sheet semua`, CSV kutip rusak, top NIK). Banding pesaing perlu
diulang terhadap ClawHub `ivangdavila/data-analysis` dari lingkungan yang tidak memblokir clawhub.ai.
