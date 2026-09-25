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

---

## Uji ulang v1.0.1 (penguji independen ke-2, 2026-09-25)
Rincian lengkap: `06-uji-ulang-v1.0.1.md`. Fixture baru: `buat_fixture_uji_ulang.py` (deterministik).
Tes bawaan: **37 tes OK**. SKILL.md 170 baris. Platform: `claude-code (simulasi agent)`.

**Perbaikan terverifikasi:** #1 multi-sheet (`--sheet semua`/daftar; header sama, urutan/kapital beda,
kolom kurang/lebih, sheet tersembunyi, sheet kosong, baris Jumlah/Total/Subtotal/"TOTAL TW4" per sheet) ✔ ·
#2 kutip tak tertutup → GAGAL + nomor baris (4 varian) ✔ · #3 "Nilai terisi" ✔ · #4 penyamaran
NIK/HP/email/rekening + `--tampilkan-pribadi` + peringatan gaji per orang ✔ · #5 "4 A"/"4A" ✔ ·
#6 duplikat di semua subperintah ✔ · #7, #10, #11 ✔.

**Angka:** 3 file baru (XLSX koperasi 6 sheet, CSV marketplace emoji + alamat multi-baris, CSV anggota
NIK/HP `;`) + skenario 01 ulang — total per sheet & gabungan, pivot silang, tren bulanan/mingguan,
top-N, banding periode/sheet → **0 ketidakcocokan** dengan kunci independen.

**Temuan baru:**
- **N1 (P1)** CSV sah ditolak: sel alamat multi-baris yang ≥ 2 barisnya berisi koma → `GAGAL: CSV
  kemungkinan rusak`, tanpa opsi memaksa (alamat Indonesia "Jl. …, No. …⏎Kel. …, Kec. …" sangat umum).
  Gagal aman (bukan angka salah), tetapi memblokir file wajar.
- **N2 (P2)** `--sheet semua` memakai sheet terlihat pertama sebagai acuan; sheet `Ringkasan` di depan →
  semua sheet detail dilewati (transparan lewat peringatan; SKILL.md belum menyuruh agent mengulang dengan daftar sheet).
- N3–N8 (P3): peringatan multi-baris berulang & penomoran baris fisik vs rekaman; "Jumlah Jumlah";
  email tersamar kembar; "Uang Lembur" tidak sensitif & "Simpanan" tanpa Rp; nama sheet berkoma tanpa saran; "baris 4 s.d. 4".

### Skor kualitas uji ulang: **7 / 10** — lulus bersyarat (naik mutu, skor tetap karena N1)
- (+) Kedua P1 lama tertutup; skenario utama (workbook per kuartal) kini dijawab murni lewat script,
  semua angka cocok di 4 file; privasi & peringatan konsisten; 37 tes lulus.
- (−) N1 regresi dari perbaikan #2: file CSV sah yang umum (daftar pelanggan/anggota berisi alamat) tidak bisa dianalisis sama sekali.
- (−) N2 jebakan default `--sheet semua` pada workbook ber-sheet ringkasan.

**Rekomendasi:** perbaiki N1 (heuristik "baris dalam sel tampak seperti rekaman utuh" + opsi
`--izinkan-multibaris` + tes regresi) dan N2 (acuan = kelompok struktur terbesar + 1 kalimat di SKILL.md);
setelah itu cukup cek singkat `alamat-sah.csv`, `pesanan-marketplace-sep.csv`, dan Koperasi `--sheet semua`
→ layak skor 8 dan status `lulus`. N3–N8 boleh menyusul.

---

## Uji ulang v1.0.2 (penguji independen ke-3, cek singkat, 2026-09-25)
Dijalankan dari salinan skill di scratchpad (bukan repo). Versi script `1.0.2`. Tes bawaan: **47 tes OK**.
SKILL.md 174 baris. Platform: `claude-code (simulasi agent)`. Fixture baru: `buat_fixture_uji_v102.py`
(deterministik; kunci `kunci-baru.json` dihitung dari data sumber, tanpa membaca kode skill).

### Temuan lama → status
| # | Temuan | Bukti ulang | Status |
|---|---|---|---|
| N1 | CSV sah alamat multi-baris berkoma ditolak | `alamat-sah.csv` → 3 baris, Rp 6.000 ✔; `pesanan-marketplace-sep.csv` → 60 baris, Rp 5.627.000, per kota 5/5 cocok kunci | ✔ Beres |
| — | Kutip tak tertutup tetap GAGAL | `kutip-rusak.csv` (uji pertama, baris 2), `kutip-tengah.csv` (baris 7), `kutip-di-akhir.csv` (baris 4) → GAGAL kode 2, **juga dengan `--paksa`**; `kutip-tertutup-jauh.csv` → "kemungkinan rusak" + saran `--paksa` | ✔ |
| — | `--paksa` terdokumentasi & memberi peringatan | SKILL.md (Batasan) + references; keluaran: "⚠️ --paksa: CSV dibaca apa adanya … Angka bisa salah …" | ✔ |
| N2 | `--sheet semua` memakai Ringkasan sebagai acuan | Koperasi → gabungan TW1–TW4, 172 baris, Rp 332.635.000, per TW & per Jenis cocok kunci; catatan "Acuan: TW1 (cocok 4 sheet), bukan 'Ringkasan'"; SKILL.md menyebut `--acuan` & daftar sheet | ✔ Beres |
| N3 | Peringatan multi-baris berulang / nomor fisik vs rekaman | Kini satu peringatan + peta "Baris 2 s.d. 4 di Notepad = baris 2 di Excel" (dicek manual benar) | ✔ (catatan kecil B3) |
| N4 | "Jumlah Jumlah" | "Total kolom Jumlah per Sheet" | ✔ |
| N5 | Email tersamar kembar | `a•••04@contoh.id`, `a•••12@…` — unik | ✔ |
| N6 | Uang Lembur tidak sensitif; Simpanan tanpa Rp | "SENSITIF: NIK, Uang Lembur"; Simpanan Wajib tampil `Rp` | ✔ |
| N7 | Nama sheet berkoma tanpa saran | GAGAL + "nama sheet 'Jan, Feb' = nomor 5 … pakai --sheet \"1,5\""; `--sheet "Jan, Feb"` utuh berhasil | ✔ |
| N8 | "baris 4 s.d. 4" | "baris 4 (baris terakhir file)" | ✔ |

Angka lama juga diulang: skenario 01 `--sheet semua` (499 baris, 496 terisi, Rp 233.556.000) dan anggota per golongan (Rp 63.350.000) → cocok kunci.

### File baru (kunci independen)
| File | Isi | Hasil script vs kunci |
|---|---|---|
| F1 `ekspor-marketplace.csv` | UTF-8 BOM, CRLF, 40 pesanan, alamat 3 baris tiap baris berkoma + angka (RT/RW, kode pos), `""` di produk & catatan, emoji, catatan multi-baris, 6 baris kosong | 40 baris ✔, Rp 6.738.100 ✔, qty 88 ✔, per kota 4/4 ✔, per produk 4/4 ✔ (termasuk `Gamis "Syar'i" 🌙`, `Kerudung Pashmina, Motif 💐`); tidak ditolak ✔ |
| F2 `rekap-wa.csv` | pemisah `;`, `1.234.000,00` campur tanpa desimal, catatan multi-baris berisi `;` dan angka, `""` + emoji | 25 baris ✔, Rp 5.301.500 ✔, per pelanggan 4/4 ✔, banding Agu→Sep Rp 2.129.500 → Rp 3.172.000 ✔ |
| F3 `rusak-tertutup-jauh.csv` | kutip dibuka baris 6, "ditutup" baris 10 | GAGAL "kemungkinan rusak baris 6 s.d. 10" kode 2 ✔ |
| F3c `rusak-terbuka.csv` | kutip dibuka baris 11, tak pernah ditutup | GAGAL "CSV rusak baris 11" kode 2 ✔ |
| F3b `rusak-satu-baris.csv` | kutip dibuka baris 6, ditutup baris 7 (1 baris tertelan, jumlah sel tetap 4) | **Terbaca 19 baris, Rp 205.000 (benar Rp 210.000)** + hanya peringatan lunak "sel multi-baris … wajar bila disengaja" ✘ (B1) |
| F4 `biaya-4-bulan.xlsx` | Ringkasan (sheet pertama) + Jan/Feb/Mar/Apr (baris TOTAL) + Rekap Akhir (sheet terakhir, struktur pivot) | `--sheet semua`: 77 baris ✔, Rp 63.575.000 ✔, pivot Kategori × Sheet 16/16 sel ✔, tren per bulan 4/4 ✔; kedua sheet ringkasan dilewati + peringatan ✔. Tanpa `--sheet` → sheet 'Ringkasan' (sesuai dokumentasi, disebut di sumber) |
| F4b `rekap-mirip.xlsx` | sama, tetapi sheet terakhir "Rekap Kategori" berjudul Tanggal/Kategori/Jumlah (2 dari 3 kolom sama) | **Digabung → Rp 127.150.000 (dobel; benar Rp 63.575.000)**; peringatan hanya "tidak ada kolom Keterangan … cek hasilnya" ✘ (B2) |
| F5 `rincian-mirip-data.csv` | sel sah "Kaos, 2, 50000⏎Topi, 1, 30000⏎Ongkir, 1, 23000" (mirip baris data, 4 kolom) | 10 baris, Rp 1.055.000 ✔ — tidak ditolak (bagus) |

**Ringkas:** 0 penolakan terhadap file sah (F1, F2, F4, F5, + 3 file uji ulang); semua kutip terbuka hingga akhir file GAGAL; 2 kasus angka salah dengan peringatan lemah (B1, B2).

### Bug baru
| # | Prioritas | Temuan | Saran |
|---|---|---|---|
| B1 | P2 | Kutip nyasar yang "tertutup" di baris berikutnya menelan tepat 1 baris data (jumlah sel rekaman tetap cocok, hanya 1 baris dalam sel mirip data) → total kurang Rp 5.000 tanpa GAGAL; peringatannya dibingkai "wajar bila disengaja". | Anggap curiga juga bila ada **1** baris dalam sel yang terpecah pemisah menjadi ≥ (jumlah kolom − 1) bagian dengan angka di posisi kolom angka, **dan** kolom sel itu biasanya satu baris (mayoritas rekaman lain tidak multi-baris). Minimal: bila hanya 1–2 sel multi-baris di kolom yang biasanya satu baris, ubah peringatan jadi "cek baris N, mungkin tanda kutip nyasar". F5 harus tetap lolos. |
| B2 | P2 | `--sheet semua` menggabungkan sheet rekap di akhir yang judul kolomnya ≥ 50% sama → total dobel. | Lewati (+ peringatan tegas) sheet bernama Rekap/Ringkasan/Total/Summary, atau yang jumlahnya = jumlah sheet lain; minimal naikkan peringatan menjadi "sheet X mungkin rekap — total bisa DOBEL" dan beri 1 kalimat di SKILL.md agar agent memeriksa sheet yang kurang kolom. |
| B3 | P3 | Peringatan menulis "35 sel teks berisi baris baru" padahal 41 sel di 35 baris (yang dihitung = rekaman). | Tulis "35 baris berisi sel multi-baris". |
| B4 | P3 | Pesan "Kolom kolom 'Jumlah' tidak ada" (kata ganda) saat `--acuan Ringkasan`. | Perbaiki teks. |

### Skor kualitas uji ulang v1.0.2: **8 / 10** — layak `lulus`
- (+) N1–N8 semua tertutup dan diverifikasi ulang; file sah yang sulit (alamat 3 baris berangka, `""`, emoji, baris kosong, `;` + desimal koma, sel mirip data) terbaca benar; kutip rusak hingga akhir file selalu GAGAL walau `--paksa`; 47 tes lulus; semua angka file baru cocok kunci independen (kecuali 2 jebakan di bawah).
- (−) B1 & B2: dua pola jebakan yang lebih jarang masih menghasilkan angka salah dengan peringatan terlalu lunak (tidak diam total — ada peringatan — sehingga tidak menurunkan di bawah 8).

**Rekomendasi:** status `lulus`; B1/B2 diperbaiki di v1.0.3 (+ tes regresi F3b, F4b, F5 dari `buat_fixture_uji_v102.py`); B3/B4 boleh menyusul.

## Uji ulang v1.0.3 (penguji independen ke-4, cek singkat, 2026-09-25)
Dijalankan dari salinan skill di scratchpad. Versi script `1.0.3`. Tes bawaan: **60 tes OK**. Platform: `claude-code (simulasi agent)`.
Fixture baru: `buat_fixture_uji_v103.py` (deterministik; `kunci-v103.json` dihitung dari data sumber, tanpa membaca kode skill).

### B1–B4 (fixture `buat_fixture_uji_v102.py`)
| # | Bukti ulang | Status |
|---|---|---|
| B1 | F3b → `GAGAL: CSV kemungkinan rusak … baris 7 tampak seperti baris data utuh … kemungkinan 1 baris data HILANG`, kode 2; `--paksa` → Rp 205.000 + "PERINGATAN TEGAS … angka bisa KURANG"; F5 (sah) tetap Rp 1.055.000 | ✔ Beres |
| B2 | F4b `--sheet semua` → Rp 63.575.000 (77 baris) ✔; "Sheet 'Rekap Kategori' TIDAK digabung … total DOBEL … --sertakan" | ✔ Beres |
| B3 | F1 → "35 baris berisi sel multi-baris (41 sel …)" | ✔ Beres |
| B4 | `--acuan Ringkasan` → "Kolom 'Jumlah' tidak ada" (tanpa kata ganda) | ✔ Beres |
Regresi F1 (Rp 6.738.100/40), F2 (Rp 5.301.500/25), F4 (Rp 63.575.000/77) tetap cocok kunci.

### File baru → hasil (a = benar, b = gagal/peringatan tegas, c = salah diam-diam)
| File | Isi | Kunci | Hasil script | Nilai |
|---|---|---|---|---|
| C1 `kutip-awal` | kutip nyasar baris data pertama, "tertutup" tanda inci baris 3 | 20 baris, 375.000 | GAGAL kemungkinan rusak baris 2 s.d. 3, kode 2 | b ✔ |
| C2 `kutip-tengah` | kutip nyasar baris 11, tertutup baris 13 (2 baris tertelan) | 20, 446.000 | GAGAL baris 11 s.d. 13, "2 baris data HILANG" | b ✔ |
| C3 `kutip-akhir` | kutip nyasar di baris terakhir, tak tertutup | 20, 431.000 | GAGAL CSV rusak baris 21 (baris terakhir) | b ✔ |
| C4 `alamat-sah-plus-nyasar` | 12 alamat 3 baris sah + `""`, SATU kutip nyasar di kolom Alamat (ditutup kutip pembuka alamat baris berikutnya) | 24 baris, 750.000 | **25 baris, 667.500 dari 22 nilai**; peringatan hanya "multi-baris … wajar bila disengaja", "2 tanggal tidak valid", "1 nilai Jumlah tidak dihitung" (padahal 2 nilai hilang: 40.000 + 42.500; baris 18–19 hanya 2–3 sel) | **c−** (ada peringatan, tapi tidak menyebut kemungkinan rusak & mengecilkan kerugian) |
| C5 `sah-alamat-3-baris` | CSV SAH: alamat 3 baris berkoma/berangka + catatan multi-baris ("Bayar: transfer, 50%⏎sisa: COD") | 30, 1.061.250 | **GAGAL "kemungkinan rusak … 14 baris data HILANG … perbaiki tanda kutip"**; `--paksa` → Rp 1.061.250 ✔ + "PERINGATAN TEGAS angka bisa KURANG" | b (positif palsu; jalan keluar ada) |
| C6 `sah-satu-catatan-mirip-data` | satu-satunya sel multi-baris, baris keduanya mirip data (`2026-09-09,Teh,retur,12000`) | 18, 566.000 | 566.000/18 ✔ + peringatan "cek baris 9, mungkin kutip nyasar" | a ✔ |
| C7 `sah-catatan-baris-baru` | 2 catatan berbaris baru biasa | 15, 556.000 | 556.000/15 ✔ + peringatan lunak | a ✔ |
| C8 `baris-kurang-sel` | tanpa kutip; baris 11 hanya 3 sel (kolom Barang terlewat, angka 18.000 jatuh ke Barang) | 20, 346.000 | **328.000 "dari 19 baris" (20 baris data), TANPA peringatan apa pun** | **c ✘** |
| X1 `rekap-bernama-Sheet4` | Sep/Okt/Nov + "Sheet4" rekap per kategori, judul kolom sama | 45, 10.685.000; per kategori 4 nilai | 10.685.000/45 ✔, pivot 4/4 ✔; Sheet4 dilewati + peringatan DOBEL | a ✔ |
| X2 `rekap-bernama-Okt` | Sheet1–3 data + "Okt" = rekap per bulan, judul sama | 43, 9.945.000 | 9.945.000/43 ✔; Okt dilewati + peringatan | a ✔ |
| X3 `Rekap-berisi-data` | "Rekap Des" sebenarnya data Desember | tanpa: 21/3.535.000; dengan: 33/6.615.000 | default dilewati + saran `--sertakan`; `--sertakan "Rekap Des"` → 6.615.000/33 ✔ | a ✔ |
| X4 `satu-bulan-kosong` | Jan/Feb/Mar/Apr, Feb judul saja | 28, 6.930.000; per bulan 3/3 | 6.930.000/28 ✔, tren 3/3 ✔; Feb "TIDAK digabung: tidak ada baris data" | a ✔ (catatan B9) |
| X5 `rekap-tidak-persis` | seperti X1, rekap selisih Rp 5.000 dari jumlah sebenarnya | 45, 10.685.000 | 10.685.000/45 ✔; Sheet4 dilewati, tapi teks "= 10.690.000 = jumlah gabungan" (tidak sama) | a ✔ (catatan B8) |

**Ringkas:** 13 file; 8 a, 4 b (satu positif palsu dengan jalan keluar), **1 c (C8) + 1 c− (C4)**. Tidak ada file sah yang ditolak tanpa jalan keluar.

### Bug baru
| # | Prioritas | Temuan | Saran |
|---|---|---|---|
| B5 | P1 | **Baris CSV dengan sel lebih SEDIKIT dari judul kolom tidak diperingatkan** (C8): angka jatuh ke kolom teks, total kurang 18.000 diam-diam. Baris dengan sel lebih BANYAK sudah diperingatkan — kasus kebalikannya belum. Ini juga akar C4 (baris 18–19 hanya 2–3 sel). | Hitung rekaman yang jumlah selnya < jumlah judul (abaikan baris kosong total); peringatan tegas "baris N hanya k dari m kolom — angka mungkin bergeser/tidak terhitung"; ≥1 baris kurang sel + sel multi-baris di sekitarnya → perlakukan sebagai "kemungkinan rusak" (GAGAL, `--paksa`). Tes regresi C4, C8. |
| B6 | P2 | Positif palsu (C5): ekspor sah dengan alamat 3 baris berkoma + catatan "Bayar: transfer, 50%⏎sisa: COD" ditolak dan pesan menyuruh "perbaiki tanda kutip", "14 baris HILANG". Awam tidak bisa menilai; agent mengikuti SKILL.md akan menyalahkan file yang benar. | Baris lanjutan hanya dianggap "mirip data" bila jumlah bagiannya ≈ jumlah kolom **dan** tiap rekaman tetap punya jumlah sel = judul setelah dibaca normal (rekaman utuh = bukti file sah). Bila semua rekaman utuh dan jumlah baris konsisten, turunkan ke peringatan. Tes regresi C5 (harus terbaca tanpa `--paksa`). |
| B7 | P3 | C4: peringatan "multi-baris … wajar bila disengaja" tetap lunak walau ada tanggal tidak valid di baris sesudah sel multi-baris. | Gabungkan dengan B5. |
| B8 | P3 | X5: pesan "jumlah … = 10.690.000 = jumlah gabungan" padahal gabungan 10.685.000. | Tulis "≈ (selisih Rp 5.000)" bila tidak persis. |
| B9 | P3 | X4: tren menulis "Penurunan terbesar: Feb 2026 (-100,0%)" untuk sheet kosong. | Kecualikan periode tanpa data dari "penurunan terbesar"; cukup "Feb 2026 tanpa data". |

### Skor kualitas uji ulang v1.0.3: **7 / 10** — tetap `lulus`, perbaiki B5 sebelum `beta`
- (+) B1–B4 tuntas; semua kutip nyasar murni (awal/tengah/akhir) GAGAL tegas; rekap bernama biasa ("Sheet4", "Okt", selisih kecil) terdeteksi; "Rekap" berisi data bisa dimasukkan dengan `--sertakan`; sheet kosong aman; 60 tes lulus.
- (−) B5: satu jenis kesalahan ketik sederhana (baris kurang kolom) menghasilkan angka salah **tanpa peringatan** — pelanggaran langsung prinsip "reliable"; C4 bernasib sama sebagian. B6: file sah realistis ditolak dengan pesan yang menyalahkan pengguna (ada `--paksa`).

## Uji ulang v1.0.4 (penguji independen ke-5, cek, 2026-09-25)
Dijalankan dari salinan skill di scratchpad. Versi script `1.0.4`. Tes bawaan: **68 tes OK**. Platform: `claude-code (simulasi agent)`.
Fixture baru: `buat_fixture_uji_v104.py` (deterministik; `kunci-v104.json` dihitung dari data sumber, tanpa membaca kode skill).
Bentuk file **meniru pola** ekspor nyata (bukan salinan file asli).

### Regresi semua fixture lama (`buat_fixture_uji*.py`, v1.0.0–v1.0.3) — tidak ada salah diam-diam
- Skenario 01 Q1 67.313.000/147, `--sheet semua` 233.556.000/499 (1900 & 1904) ✔; 02 lembur 745,5 jam/383 ✔; 03 iuran 5.525.000/91 (+3 duplikat diperingatkan) ✔.
- Koperasi `--sheet semua` 332.635.000/172 (Ringkasan dilewati) ✔; pesanan marketplace 5.627.000/60 ✔; anggota koperasi 63.350.000 (+2 duplikat) ✔.
- F1 6.738.100/40, F2 5.301.500/25, F4 & F4b 63.575.000/77, F5 1.055.000/10 ✔; F3/F3b/F3c GAGAL ✔ (F3b `--paksa` 205.000 + PERINGATAN TEGAS ✔).
- C1–C3 GAGAL ✔; **C4 kini GAGAL** "baris 18–19 hanya 2/3 dari 4 kolom" ✔ (B5/B7 beres); **C5 kini terbaca tanpa `--paksa`** 1.061.250/30 ✔ (B6 beres); C6 566.000, C7 556.000 ✔; **C8 GAGAL baris 11** ✔, `--paksa` 328.000 + PERINGATAN TEGAS ✔.
- X1 10.685.000/45, X2 9.945.000/43, X3 3.535.000 → `--sertakan` 6.615.000/33, X4 6.930.000/28, X5 10.685.000 dengan "10.690.000 ≈" ✔ (B8 beres).
- File rusak (kosong, korup.xlsx, bukan-excel, tanpa-sheet, kutip tak tertutup) → GAGAL kode 2 tanpa traceback ✔.

### File baru → hasil (a = benar, b = gagal/peringatan tegas + jalan keluar, c = salah diam-diam, d = ditolak padahal awam wajar berharap terbaca)
| File | Pola ekspor | Kunci | Hasil script | Nilai |
|---|---|---|---|---|
| N1 `shopee-judul-catatan-kaki` | 3 baris judul laporan, baris Total, "Dicetak oleh: … pada …" 1 sel | 20 baris, 3.709.200 | GAGAL "baris 27: hanya 1 dari 7 kolom → Dicetak oleh…"; `--paksa` → 3.709.200 ✔ (Total dilewati) tapi "21 baris data" | **d** |
| N2 `tokopedia-rp-catatan-2-baris` | judul 1 baris, "Rp1.250.000", 2 baris catatan kaki (1 & 2 sel) | 15, 2.280.000 | GAGAL 2 baris; `--paksa` → 2.280.000 ✔ + "tanggal tidak valid baris 20: '15'", "17 baris data" | **d** |
| N3 `tiktok-baris-deskripsi` | baris ke-2 = deskripsi kolom, tanggal m/d/Y AM | 18, 2.050.000, qty 36 | 2.050.000 & 36 ✔; deskripsi → "1 nilai tidak valid (baris 2)" per kolom; format AS terdeteksi; "19 baris data" | a |
| N4 `bca-mutasi` | metadata rekening di atas, kolom tanpa judul (CR/DB), Saldo Awal/Mutasi/Saldo Akhir di bawah (2–3 sel) | 16; CR 3.800.000; DB 11.060.000 | GAGAL 4 baris; `--paksa` → 14.860.000 ✔, pivot "Kolom E" CR 3.800.000 / DB 11.060.000 ✔ + "(kosong)" 4 baris | **d** |
| N5 `mandiri-kolom-ganda` | 2 kolom "Description", angka "1,500,000.00" berkutip, koma di ujung | Debit 2.595.000; Credit 2.860.000 | ✔ keduanya; "Description (2)" ✔. Catatan: `Transaction Code` ikut dijumlah (121.161), Credit tanpa "Rp" sedangkan Debit ber-"Rp" | a (catatan B13) |
| N6 `google-form` | timestamp d/m/Y H:M:S, kotak centang "Kopi, Teh", alamat 3 baris, catatan 2 baris, "55rb" | 22; 1.825.000 dari 20; 2 tidak valid | ✔ persis; "2 nilai tidak valid (baris 7 '55rb', 18 '25rb')" | a |
| N7 `excel-titikkoma-kolom-kosong` | cp1252, `;`, kolom tanpa judul di tengah, "1.250.000", 3 baris `;;;;;` | 17; 9.842.500; qty 145 | ✔ persis | a |
| N8 `kolom-catatan-opsional` | kolom terakhir "Catatan" hanya diisi sebagian, tanpa koma di ujung (13 baris 3 sel) | 20, 520.000 | **GAGAL 13 baris** "angka bisa masuk ke kolom yang salah"; `--paksa` → 520.000 ✔ | **d** (terberat: pesan menakutkan & salah — angka tidak bergeser) |
| N9 `sel-terlewat-tengah` | sel Pelanggan terlewat di baris 11 | 20, 512.000 | GAGAL baris 11 ✔; `--paksa` 497.000 + PERINGATAN TEGAS | b ✔ |
| N10 `kutip-inci-panggilan` | `Pipa PVC 3"` (kutip di tengah sel), `"Ucup" Warung` (kutip di awal sel) | 15, 827.500 | ✔; "Ucup Warung" kehilangan kutip (kosmetik) | a |
| N11 `excel-sum-tanpa-label` | baris SUM **tanpa label** `,,,4860000` + baris `,,Rata-rata,405000` | 12, 4.860.000 | **10.125.000 "dari 14 baris", tanpa peringatan apa pun** (dobel + rata-rata ikut) | **c ✘** |
| N12 `footer-berpadding` | catatan kaki dengan padding koma penuh ("Dicetak oleh: admin,,,") | 10, 835.000 | total 835.000 ✔, tetapi "12 baris data", tanggal akhir "30 Sep 2026" (dari catatan kaki), pivot "(kosong) 2 baris" — tanpa peringatan | a− (total benar; jumlah baris & rentang tanggal salah diam-diam) |
| N13 `subtotal-per-hari` | baris "Subtotal" per hari (label di kolom 2), SKU 13 digit | 12, 1.020.000 | ✔ "3 baris Total/Jumlah dilewati (6, 11, 16)"; SKU = teks | a |
Tambahan ad hoc: `,,Total,…` dan `,,Grand Total,…` di kolom ke-3 → dilewati ✔; `,,Total,…` + `,,Rata-rata,405000` → **Rata-rata ikut dijumlah** (5.265.000 vs 4.860.000) **c ✘**.

**Ringkas:** 13 file; 7 a (1 a−), 1 b, **1 c (N11, + varian Rata-rata)**, **4 d (N1, N2, N4, N8 = 31%)**. Semua d punya jalan keluar `--paksa` yang menghasilkan total benar, tetapi jumlah baris membengkak.

### Penilaian pesan untuk awam (d)
- N1/N2/N4: pesan menampilkan isi baris ("Dicetak oleh…", "Saldo Akhir : | 5240000.00") sehingga agent bisa menebak itu catatan kaki; tetapi **teks pesan tidak pernah menyebut "catatan di bawah tabel"** (SKILL.md menyebutnya, pesan GAGAL tidak), dan alasan "angka bisa masuk ke kolom yang salah" tidak benar untuk catatan kaki. Menyuruh awam "buka di Notepad, perbaiki" file ekspor Shopee/BCA setiap bulan = gesekan tinggi; ekspor mutasi BCA **selalu** punya baris saldo di bawah → tiap pemakaian ditolak.
- N8: 13 baris ditolak padahal hanya kolom opsional di ujung yang tidak diketik; saran "perbaiki 13 baris" tidak realistis. Aturan "sel kosong di ujung kanan boleh" hanya berlaku bila komanya ada — perbedaan yang tidak terlihat awam di Excel.
- Saran: **baris pendek di ujung file (setelah baris data utuh terakhir)** → abaikan + info "N baris catatan di bawah tabel diabaikan: 'Dicetak oleh…', 'Saldo Akhir…'" (tetap GAGAL bila ada baris data utuh sesudahnya). **Baris pendek di tengah** yang sel-selnya cocok tipe kolomnya (tanggal di kolom tanggal, angka di kolom angka) dan hanya kolom teks/kosong di ujung yang hilang → terima + info; bila ada angka jatuh ke kolom teks (N9, C8) → tetap GAGAL.

### Bug baru
| # | Prioritas | Temuan | Saran |
|---|---|---|---|
| B10 | **P1** | N11: baris SUM tanpa label (`,,,4860000`, pola umum Excel: rumus =SUM di bawah kolom) ikut dijumlah → total **dobel diam-diam**; baris berlabel "Rata-rata" di bawah Total juga ikut dijumlah. | Baris yang tanpa teks/tanggal dan hanya berisi angka di kolom nilai, terutama di ujung tabel, dan nilainya = jumlah (atau rata-rata) baris di atasnya → lewati seperti baris Total + peringatan. Tambah label Rata-rata/Rerata/Average/Grand Total/Subtotal/Saldo ke daftar baris ringkasan. Uji juga di XLSX (belum diuji di sini). Tes regresi N11 + varian. |
| B11 | P2 | N1/N2/N4/N8 (d): catatan kaki & kolom opsional di ujung ditolak; pesan tidak menyebut "catatan di bawah tabel" dan menakuti dengan "kolom yang salah". | Lihat saran di atas; minimal ubah pesan GAGAL: bila semua baris bermasalah ada di ujung file → "Tampaknya baris catatan di bawah tabel (…). Hapus baris itu, atau ulangi dengan --paksa (angka tabel tidak terpengaruh)". |
| B12 | P3 | N12 (dan N1/N2/N4 dengan `--paksa`): baris catatan dihitung sebagai "baris data" (12 bukan 10), tanggal di catatan kaki memperpanjang rentang data, pivot memunculkan "(kosong)". | Baris tanpa nilai di kolom angka dan berlabel catatan (Dicetak/Catatan/Sumber/Saldo/Mutasi) di ujung → keluarkan dari hitungan + info. |
| B13 | P3 | N5: `Transaction Code` (kode 4 digit) dijumlah; format "Rp" tidak konsisten antara Debit dan Credit. | Nama kolom berisi Code/Kode/No/ID → tipe kode. |

### Skor kualitas uji ulang v1.0.4: **6 / 10** — **belum lulus ke `beta`**; revisi B10 (wajib) dan B11, lalu uji ulang independen
- (+) Aturan jumlah kolom menutup B5/B7 (C4, C8, N9 GAGAL tegas dengan nomor & isi baris); B6/B8/B9 beres; semua fixture lama tetap benar; format bank/marketplace yang rapi (Mandiri, TikTok, Google Form, Excel `;` cp1252, subtotal berlabel) terbaca benar; 68 tes lulus.
- (−) Target "0 salah diam-diam" belum tercapai: **baris SUM tanpa label / baris Rata-rata (N11) menggandakan total tanpa peringatan** — pola Excel yang sangat umum pada pengguna awam. Selain itu 4 dari 13 ekspor realistis (31%) ditolak, termasuk **setiap** mutasi BCA dan file dengan kolom catatan opsional; `--paksa` menyelamatkan totalnya, tetapi awam dipaksa melewati pesan yang menyalahkan file yang sebenarnya sehat.
