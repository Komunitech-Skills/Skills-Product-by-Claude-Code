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

## Uji ulang v1.0.5 (penguji independen ke-6, cek, 2026-09-25)
Dijalankan dari salinan skill di scratchpad. Versi script `1.0.5`. Tes bawaan: **82 tes OK** (±23 dtk). Platform: `claude-code (simulasi agent)`.
Fixture baru: `buat_fixture_uji_v105.py` (deterministik; `kunci-v105.json` dihitung dari data sumber, **tanpa membaca kode skill**). Fokus: data ASLI yang ikut terbuang karena dikira baris ringkasan/catatan.

### Regresi semua fixture lama (v1.0.0–v1.0.4) — tidak ada regresi
- 01 Q1 67.313.000/147, `--sheet semua` 233.556.000/499 (1900 & 1904) ✔; 02 lembur 745,5/383 ✔; 03 iuran 5.525.000/91 (+TOTAL dilewati, +3 duplikat) ✔; file rusak/kosong/korup/tanpa sheet → GAGAL kode 2 ✔.
- Koperasi `--sheet semua` 332.635.000/172 ✔; marketplace 5.627.000/60 ✔; anggota 63.350.000 ✔; kutip rusak GAGAL ✔.
- F1 6.738.100/40, F2 5.301.500/25, F4 & F4b 63.575.000/77, F5 1.055.000/10 ✔; F3/F3b/F3c GAGAL ✔.
- C1–C4, C8 GAGAL ✔ (C8 `--paksa` 328.000 + PERINGATAN TEGAS); C5 1.061.250/30, C6 566.000, C7 556.000 ✔; X1–X5 ✔ (X3 `--sertakan` 6.615.000/33).
- v1.0.4: **N1, N2, N4, N8 kini terbaca tanpa `--paksa`** dengan jumlah baris benar (20/15/16/20) + info catatan kaki/kolom opsional (B11 beres); **N11 kini 4.860.000/12** + SUM & Rata-rata disebut (B10 beres); **N12 kini 10 baris** + info catatan (B12 beres); N3, N5–N7, N10, N13 tetap ✔; N9 tetap GAGAL ✔.

### File baru → hasil (a = benar, b = gagal/peringatan tegas + jalan keluar, b− = angka default SALAH tetapi baris yang dibuang disebut beserta isinya + `--pertahankan-total`, c = salah diam-diam, d = ditolak padahal wajar)
| File | Pola | Kunci | Hasil script | Nilai |
|---|---|---|---|---|
| R1 `bernomor-baris3-jumlah` | kolom No/Qty/Harga/Total semua angka; baris 2 = baris 1, baris 3 = baris 1+2 di SEMUA kolom | 10, 725.000 | 725.000/10 ✔ | a |
| R2 `satu-kolom-nominal` | satu kolom: 25rb, 25rb, 50rb, 100rb (= jumlah di atas) … | 8, 370.000 | 370.000/8 ✔ (+ info duplikat) | a |
| R3 `kas-tanggal-sekali` | buku kas, tanggal/keterangan hanya di transaksi pertama per hari; baris 5 (70.000) kebetulan = jumlah di atas | 8, 396.000 | **326.000/7**; "baris 5: \| \| 70000 = jumlah kolom di atasnya … DOBEL" | **b−** |
| R3c `kas-akhir-sama-jumlah` | transaksi lanjutan terakhir tanpa label = jumlah di atas | 4, 120.000 | **60.000/3** + peringatan berisi baris 5 | **b−** |
| R4 `masuk-keluar-banyak-nol` | Masuk/Keluar banyak 0, baris tanpa label, Keluar = jumlah di atas tetapi Masuk tidak | Masuk 595.000, Keluar 680.000 | ✔ keduanya | a |
| R5 `produk-bernama-total` | "Paket Total Care", "Jumlah Besar…", "Setoran Saldo Awal Bulan", "Grand Total Kids Toy", "Subtotal Snack Box", "Rata-rata Air…", + produk bertanggal bernama persis "TOTAL" & "Jumlah" | 10, 1.022.000 | nama mengandung kata → tetap data ✔; "TOTAL"/"Jumlah" bertanggal dibuang (950.000/8) + disebut isinya | b |
| R6 `kategori-rata-rata` | penilaian kinerja "Rata-rata"/"Di atas rata-rata"/"Di bawah rata-rata", kolom Bonus | 8, 6.000.000; Rata-rata 4 baris 3.000.000 | **3.000.000/4 — 4 dari 8 pegawai dibuang** sebagai "baris Total/Jumlah" (isi baris disebut) | **b− (serius)** |
| R6b `penilaian-kolom-1` | sama, kategori di kolom 1 | 4, 3.000.000 | **2.000.000/2** | **b− (serius)** |
| R7 `kerusakan-total` | klaim asuransi, Jenis Kerusakan = Total/Sebagian | 5, 210.500.000 | **5.500.000/3 — 97% nilai hilang** (2 klaim "Total" dibuang, disebut isinya) | **b− (serius)** |
| R8 `catatan-kaki-berangka` | 6 data + "Catatan: 2 pesanan retur senilai,,150000" + "Harga sudah termasuk PPN 11%" | 6, 715.000 | GAGAL "baris 10 hanya 1 dari 3 kolom"; `--paksa` → 865.000 (catatan 150.000 ikut) | **d** |
| R8c `catatan-1-sel-berangka` | 2 catatan kaki 1 sel berisi angka ("Ongkir 15000…", "PPN 11%") | 6, 715.000 | GAGAL 2 baris (catatan teks tanpa angka di N1 diterima) | **d** |
| R8d `catatan-berangka-3-sel` | hanya "Catatan: … senilai,,150000" di bawah tabel | 6, 715.000 | **865.000/7**; satu-satunya tanda: "Tanggal: 1 nilai tidak valid (baris 10: 'Catatan…')" — tidak disebut bahwa 150.000 ikut dijumlah | **c ✘** |
| R9 `subtotal-berlabel-kelompok-1-baris` | "Subtotal Cabang A/B/C" + Grand Total; cabang B 1 baris | 6, 1.700.000 | 1.700.000/6 ✔, 4 baris disebut | a |
| R10 `subtotal-tanpa-label` | subtotal per cabang TANPA label; cabang B 1 baris | 6, 1.700.000 | **2.100.000/7**: subtotal A (=jumlah di atas) & C (kebetulan "= rata-rata") dibuang, **subtotal B 400.000 ikut dijumlah tanpa pesan** | **c ✘** |
| R11 `kas-sum-average.xlsx` | XLSX; baris 3 = baris 2 (tanpa label), baris 6 data = jumlah di atas (tanpa label), lalu SUM & AVERAGE (sel rumus) | 5, 10.700.000 | **18.190.000/6**: baris data 6 dibuang (disebut), **SUM 10.700.000 & AVERAGE 2.140.000 ikut dijumlah tanpa pesan**; sama persis pada versi CSV | **c ✘ (terberat)** |
| R11b `sum-average-biasa.xlsx` | SUM & AVERAGE (rumus) tanpa baris kebetulan | 3, 3.850.000 | ✔ keduanya dibuang & disebut (pesan menulis "1283333.33333333") | a |
| R12 / R12b `bulan-angka` | Tahun/Bulan sebagai angka (Bulan 3 = 1+2, Mar = Jan+Feb) | 12, 70.700.000 | ✔ | a |
| R13 `waktu-pembeli-kosong` | pembeli anonim kosong, 15.000 berulang, "Bu Ani" 45.000 = jumlah di atas | 4, 90.000 | ✔ | a |
| R14 `iuran-baris-belum-lengkap.xlsx` | baris tanpa tanggal/nama 75.000 = rata-rata di atas | 4, 275.000 | ✔ | a |
| R16 `nilai-polos-sama-jumlah.xlsx` | XLSX, nilai **polos (bukan rumus)** tanpa label = jumlah di atas | 4, 2.400.000 | **1.350.000/3**, pesan menyebut "baris rumus SUM/AVERAGE" padahal sel tidak berumus | **b−** |
| P1 `shopee-nilai-berulang` | Total Pembayaran berulang, satu = jumlah dua sebelumnya, produk "Paket Total Care" | 10, 1.115.000 | ✔ | a |
| P2 `tokopedia-ringkasan-bawah` | judul di atas, "Rp150.000", Total Penjualan & Rata-rata per pesanan di bawah | 5, 825.000 | ✔ 2 baris ringkasan disebut | a |
| P3 `bca-keterangan-saldo-total` | mutasi "1.000.000,00", kolom CR/DB tanpa judul, keterangan "…SALDO AWAL ARISAN", "…TOTAL BAYAR PESANAN", Saldo Awal/Mutasi/Saldo Akhir di bawah | 4, 1.520.000 | ✔ transaksi berketerangan SALDO/TOTAL tetap data; 4 baris saldo disebut | a |
| P4 `google-form-donasi` | timestamp d/m/Y H:M:S, satu donasi = jumlah dua sebelumnya | 5, 500.000 | ✔ (+ info tanggal ambigu, wajar) | a |
Tambahan ad hoc (tidak masuk skrip): kolom paling kanan "Diskon" (angka) sering kosong → 360.000 ✔ a; baris tanpa Barang tapi ada Diskon (angka bergeser) → GAGAL ✔ b; baris tanpa nilai Jumlah → GAGAL ✔ b; XLSX gaya sel gabung, baris 2 = baris 1 tanpa label → tetap data ✔ a.

**Ringkas:** 25 file; **13 a, 1 b, 6 b−, 3 c (R8d, R10, R11), 2 d (R8, R8c)**. Setiap baris yang dibuang oleh aturan label/SUM **disebut beserta isinya** (syarat "pengguna bisa melihat" terpenuhi untuk b−), **kecuali** kasus c: angka yang *ikut* dijumlah (subtotal B, SUM/AVERAGE setelah baris kebetulan, catatan berangka) tidak disebut sama sekali.

### Kinerja 50 ribu baris (5 kolom, + baris SUM tanpa label di akhir)
CSV: `ringkas` 5,9 dtk, `pivot` 6,2 dtk; XLSX: 4,6 / 4,2 dtk. Total 12.498.522.152 ✔ (SUM akhir terdeteksi & disebut). Layak.

### Bug baru
| # | Prioritas | Temuan | Saran |
|---|---|---|---|
| B14 | **P1** | Label ringkasan dicocokkan pada sel **mana pun** tanpa cek angka: nilai kategori "Rata-rata" (R6/R6b, penilaian kinerja — umum di HR) dan "Total" (R7, jenis kerusakan) membuang setengah data / 97% nilai; baris bertanggal bernama produk "TOTAL" juga dibuang (R5). Pesan "baris Total/Jumlah dilewati agar tidak dobel" membuat agent & awam menerimanya. | Baris berlabel hanya dianggap ringkasan bila: label di sel teks pertama **dan** baris tanpa tanggal/ID; **atau** angkanya ≈ jumlah/rata-rata kelompok di atas. Nilai yang muncul ≥ 2× di satu kolom = kategori, bukan label. Selebihnya tetap data + info ringan. Tes regresi R5, R6, R6b, R7 + N13/P2/P3 tetap lulus. |
| B15 | **P1** | Aturan "baris tanpa label = jumlah/rata-rata di atas" bersifat serakah dan berjalan dari atas: transaksi asli yang kebetulan sama dibuang (R3, R3c, R16), dan karena itu **baris SUM/AVERAGE asli sesudahnya tidak lagi cocok dan ikut dijumlah diam-diam** (R11: 18.190.000 vs 10.700.000). Pada XLSX, sel bernilai polos disebut "baris rumus SUM". | XLSX: pakai isi rumus (`SUM`/`AVERAGE`/`SUBTOTAL` atas rentang kolom yang sama) sebagai bukti; sel tanpa rumus **jangan** dibuang oleh aturan ini. CSV: evaluasi blok baris tanpa label di **ujung** tabel dari bawah (baris terakhir = jumlah semua data di atas), bukan di tengah; kandidat di tengah → pertahankan + peringatan "mungkin baris SUM, cek". Tes regresi R3, R3c, R11 (xlsx & csv), R16, N11. |
| B16 | P2 | Subtotal per kelompok tanpa label (R10) hanya sebagian terdeteksi (satu karena kebetulan = rata-rata); subtotal kelompok 1 baris ikut dijumlah (+400.000 diam-diam). | Kenali pola: beberapa baris tanpa label yang masing-masing = jumlah baris sejak baris-tanpa-label sebelumnya → buang semua secara konsisten (termasuk kelompok 1 baris) + sebut; pola tidak konsisten → GAGAL/peringatan tegas. |
| B17 | P2 | Catatan kaki berangka: 3 sel "Catatan: …,,150000" ikut dijumlah (R8d, hanya tanda tak langsung "tanggal tidak valid"); catatan 1 sel yang berisi angka ("Ongkir 15000…", "PPN 11%") ditolak GAGAL (R8, R8c) padahal catatan teks biasa diterima. | Baris sesudah baris data utuh terakhir yang diawali Catatan/Keterangan/Note/Ket/`*` → blok catatan (info + isi), walau berisi angka; angka di dalam teks tidak membatalkan status catatan. Nilai tidak valid di kolom tanggal pada baris yang angkanya ikut dijumlah → peringatan tegas. |
| B18 | P3 | Pesan menampilkan rata-rata mentah "1283333.33333333" (R11b). | Format rupiah seperti tabel. |

### Skor kualitas uji ulang v1.0.5: **6 / 10** — **belum lulus ke `beta`**; revisi B14 & B15 (wajib), B16–B17, lalu uji ulang independen
- (+) B10–B12 dari v1.0.4 tuntas: SUM/Rata-rata di ujung, catatan kaki, mutasi BCA, kolom opsional di kanan kini terbaca benar tanpa `--paksa`; semua fixture lama tetap benar; nama produk yang *mengandung* Total/Jumlah/Saldo aman; ekspor Shopee/Tokopedia/BCA/Google Form realistis benar; setiap baris yang dibuang disebut dengan isinya; 82 tes lulus; 50 ribu baris < 7 dtk.
- (−) Perbaikan menukar satu jenis salah diam-diam dengan jenis baru: **3 file salah diam-diam** (R11 terberat: total 70% terlalu besar karena baris SUM & AVERAGE ikut dijumlah setelah satu transaksi asli dibuang) dan **6 file dengan angka default salah** karena data asli dibuang (R6/R7: kategori "Rata-rata"/"Total" menghapus 50–97% nilai). Pesannya jujur, tetapi berbunyi seperti tindakan yang benar ("agar tidak dobel"), sehingga awam hampir pasti menerimanya. Aturan label & SUM perlu bukti tambahan (posisi, rumus XLSX, cek angka) sebelum membuang baris.

---

## Uji ulang v1.0.6 (penguji independen ke-7, cek, 2026-09-25)
Dijalankan dari salinan skill di scratchpad. Versi script `1.0.6`. Tes bawaan: **94 tes OK** (±29 dtk). Platform: `claude-code (simulasi agent)`.
Fixture baru: `buat_fixture_uji_v106.py` (deterministik; `kunci-v106.json` dihitung dari data sumber, **tanpa membaca kode skill**). XLSX ditulis tangan dengan sel `<f>` + nilai tersimpan.

### 1. Regresi semua fixture lama (v1.0.0–v1.0.5) — tidak ada (c)
- v1.0.0–v1.0.4: 01 Q1 67.313.000/147, `--sheet semua` 233.556.000/499 (1900 & 1904) ✔; lembur 745,5 ✔; iuran 5.525.000/91 ✔; koperasi 332.635.000 ✔; F1/F2/F4/F4b/F5, C5–C7, X1–X5 (X3 `--sertakan "Rekap Des"` 6.615.000/33) ✔; N1–N8, N10, N12 ✔; semua file rusak/kosong/C1–C4/C8/F3*/N9 tetap GAGAL ✔ (C8 `--paksa` + TEGAS).
- **N11 & N13 berubah a → b**: baris SUM/subtotal tanpa label di tengah kini dihitung + PERINGATAN TEGAS; total alternatif TANPA = 4.860.000 / 1.020.000 = kunci ✔ (sesuai prinsip v1.0.6).
- v1.0.5 (semua b−/c sebelumnya): **R6, R7 kini a** (kategori "Rata-rata"/"Total" tetap data: 6.000.000 / 210.500.000); **R8, R8c, R8d kini a** (catatan berangka dikeluarkan + disebut, 715.000); **R11 kini a** (5.350.000 polos tetap data + TEGAS, SUM & AVERAGE rumus dikeluarkan → 10.700.000); R3, R3c, R5, R6b, R16 → angka default = kunci + TEGAS (b); R9, R10 → TEGAS, alternatif 1.700.000 ✔ (b); sisanya a. **0 c, 0 d.**

### 2. File baru → hasil (a = benar, b = peringatan tegas + total alternatif benar / gagal-jelas, c = salah diam-diam, d = ditolak padahal wajar)
| File | Pola | Kunci | Hasil script (`ringkas`) | Nilai |
|---|---|---|---|---|
| S1 `subtotal-sum-berlabel.xlsx` | "Subtotal Cabang X" `=SUM(Cn:Cm)` di tengah + "GRAND TOTAL" `=C5+C9+C12` | 8, 6.425.000 | ✔ 4 baris dikeluarkan + disebut | a |
| S1b `subtotal-sum-tanpa-label.xlsx` | subtotal `=SUM` tanpa label; grand total `=SUM(C5,C9,C12)` tanpa label | 8, 6.425.000 | 3 subtotal dikeluarkan ✔; grand total **tidak dikenali sebagai rumus agregat** → dihitung (12.850.000) + TEGAS, alternatif 6.425.000 ✔ | b |
| S1c `grandtotal-plus-tanpa-label.xlsx` | grand total `=C5+C9+C12` tanpa label | 8, 6.425.000 | sama dengan S1b (TEGAS, alternatif ✔) | b |
| S2 `sum-mendatar-per-baris.xlsx` | Total `=SUM(B2:D2)` per baris (mendatar) = DATA | 5, 1.765.000 | ✔ tidak ada yang dibuang | a |
| S2b `rumus-kali-per-baris.xlsx` | `=B2*C2` per baris + TOTAL berlabel `=SUM` | 5, 3.830.000, qty 1.032 | ✔ | a |
| S2c `average-mendatar-nilai-siswa.xlsx` | `=AVERAGE(B2:D2)` per siswa = DATA | 4, Σrata 315 | ✔ | a |
| S3 `ekspor-kasir-tanpa-rumus.xlsx` | judul 2 baris; ekor: "Total Penjualan", "Tunai", "QRIS" (rincian bayar) | 6, 159.000, qty 10 | **477.000/9 (3× lipat)**; "Total Penjualan" disebut TEGAS "di tengah tabel", alternatif TANPA = **318.000 (juga salah)**; Tunai & QRIS **tidak disebut sama sekali** | **c ✘** |
| S4 `mutasi-multi-halaman.csv` | 2 halaman: header berulang, "Halaman 1 dari 2", judul berulang | 7, 6.335.000 (CR 4.250.000, DB 2.085.000) | ✔ angka & pivot CR/DB; header berulang dilewati + info. Catatan: "Halaman 1 dari 2" & "MUTASI REKENING" terhitung sebagai 2 baris kosong (n=9, pivot "(kosong)" 2 baris) | a (−) |
| S5 `dua-tabel.csv` | tabel Penjualan, baris kosong, "PENGELUARAN", tabel kedua (header beda) | tabel 1: 3 baris, 390.000 | tabel 2 **digabung** ke tabel 1: n=7, Qty = **535.006** (Nominal pengeluaran masuk ke Qty), "Sewa lapak" jadi Produk; hanya tanda tak langsung ("PENGELUARAN"/"Tanggal" bukan tanggal). Nominal 390.000 benar kebetulan | **c ✘** |
| S6 `gaji-total-divisi.csv` | ",Total Divisi X" di tengah (kolom Nama) + GRAND TOTAL | 6, GP 27.000.000, Tunj 3.050.000 | ekor (Total Divisi Admin + GRAND TOTAL) dikeluarkan; baris 5 & 7 TEGAS, alternatif 27.000.000 / 3.050.000 ✔ | b |
| S6b `gaji-total-divisi-kolom1` | "Total Divisi X" di kolom 1, tanpa grand total | sama | sama ✔ | b |
| S7 `retur-negatif.csv` | `-350000`, `(75.000)`, `-Rp 50.000`, qty `-1` | 7, 1.675.000 | ✔ (kurung dibaca negatif) | a |
| S8 `duplikat-sah.csv` | 2 pasang baris identik (pembelian ulang sah) | 8, 214.000 | ✔ dihitung + info duplikat | a |
| S9 `total-di-atas-rumus.xlsx` | baris "Jumlah" `=SUM(B3:B6)` tepat di bawah header | 4, 1.560.000 | ✔ dikeluarkan + disebut | a |
| S10 `kebetulan-lalu-total.csv` | 300.000 = 100rb+200rb (data), lalu "Total" | 3, 600.000 | ✔ | a |
| S11 `excel-data-subtotal.xlsx` | gaya Excel *Data › Subtotal*: "Jakarta Total" `=SUBTOTAL(9,…)` + "Grand Total" | 6, 11.200.000 | ✔ 4 baris dikeluarkan | a |
| S12 `data-subtotal-nilai-polos.csv` | S11 disimpan sebagai CSV (nilai polos): "Jakarta Total", "Bandung Total", "Surabaya Total" di tengah | 6, 11.200.000 | **22.400.000/9 (dobel)**, hanya "Grand Total" ekor dikeluarkan; **tidak ada TEGAS/peringatan apa pun**; "Jakarta Total" hanya tampak sebagai kategori | **c ✘ (terberat)** |

**Ringkas:** 17 file baru; **10 a, 4 b, 3 c (S3, S5, S12), 0 d**. Jalan keluar manual bekerja: S3 `--buang-baris 12,13,14` → 159.000 ✔; S12 `--buang-baris 4,6,10` → 11.200.000 ✔ — tetapi agent tidak punya alasan menjalankannya karena script tidak memberi tanda.

### 3. Uji alur agent (mengikuti SKILL.md persis)
**AF1 — S6** "Ini rekap gaji September. Total gaji pokok & tunjangan per divisi berapa?" → `profil` (TEGAS + BARIS DIKELUARKAN + data SENSITIF), `pivot --grup Divisi`, lalu `--buang-baris 5,7` untuk versi alternatif. Jawaban agent:
> **Jawaban singkat:** Sebelum angka final, satu hal perlu dipastikan: baris 5 ("Total Divisi Produksi") dan baris 7 ("Total Divisi Gudang") tampaknya baris **total**, bukan pegawai, tetapi saat ini masih ikut dihitung. **Bila keduanya baris total** (paling mungkin): gaji pokok **Rp 27.000.000**, tunjangan **Rp 3.050.000** (6 pegawai). **Bila dihitung sebagai data:** Rp 44.400.000 / Rp 5.100.000. Betul baris 5 & 7 itu total?
> *(tabel pivot TANPA baris 5 & 7: Produksi Rp 13.500.000 · Admin Rp 9.600.000 · Gudang Rp 3.900.000 · TOTAL Rp 27.000.000)*
> **Perlu dicek:** baris 10 (Total Divisi Admin) & 11 (GRAND TOTAL = Rp 27.000.000) sudah tidak dihitung; data gaji = data pribadi (UU PDP), bagikan hanya agregat per divisi.

Kandidat disebut, kedua total ditampilkan, pertanyaan sekali ✔. GRAND TOTAL di file (27.000.000) menguatkan versi TANPA.

**AF2 — S1b** "Total omzet semua cabang berapa?" → `ringkas` + `pivot --grup Cabang`. Jawaban agent:
> **Jawaban singkat:** Total omzet **Rp 6.425.000** bila baris 13 (angka Rp 6.425.000 tanpa keterangan, persis = jumlah baris di atasnya) adalah baris grand total; **Rp 12.850.000** bila itu transaksi. Mohon konfirmasi baris 13. Per cabang: B Rp 2.475.000, A Rp 2.450.000, C Rp 1.500.000.
> **Perlu dicek:** 3 baris subtotal rumus `=SUM` (baris 5, 9, 12) sudah tidak dihitung.

Kandidat disebut, kedua total ✔; tabel pivot mentah memuat "(kosong) Rp 6.425.000 50%" — agent wajib menjelaskannya (SKILL.md sudah cukup: "baris itu MASIH dihitung").

**Penilaian alur:** bila script memberi TEGAS, SKILL.md langkah 3 + format "Perlu dicek" membuat agent **tidak** memberi satu angka final ✔ (2/2). Kelemahan ada di hulu: S12 (tanpa tanda) → agent pasti menjawab satu angka salah (22.400.000); S3 → agent menampilkan "477.000 atau 318.000", keduanya salah, karena SKILL.md tidak menyuruh memeriksa baris ekor yang tidak disebut.

### 4. Uji A/B ulang skenario 01 ("kategori paling laku, tren bulanan, Q2 vs Q3")
| | TANPA skill (parser XLSX stdlib cepat, seperti biasa ditulis agent; pandas tidak tersedia) | DENGAN skill v1.0.6 | Kunci |
|---|---|---|---|
| Grand total | 465.064.000 (baris TOTAL ikut → dobel), 494 baris | 233.556.000 / 499 baris, 3 baris TOTAL `=SUM` disebut | 233.556.000 |
| Semen | 83.532.000 (+ "SEMEN" & "semen " terpisah) | 105.444.000 | 105.444.000 |
| Rumus tanpa nilai / teks "Rp" / retur | hilang tanpa pesan | disebut (Nilai terisi 496) | 3 / 4 / 1 |
| Tren & Q2 vs Q3 | tidak dihitung | 9 bulan = kunci; Q3 −28,8% | ✔ |
Kesimpulan: dengan skill **jelas lebih baik** (sama dengan uji sebelumnya).

### Bug baru
| # | Prioritas | Temuan | Saran |
|---|---|---|---|
| B19 | **P1** | Hasil *Data › Subtotal* Excel yang disimpan sebagai CSV/nilai polos ("Jakarta Total" — kata Total di **akhir** label, di kolom pertama, angka = jumlah kelompok di atasnya) **tidak dikenali sama sekali** → total dobel diam-diam (S12). Padahal "Total Divisi X" (Total di awal) di S6 sudah memicu TEGAS. | Label tengah berawalan **atau berakhiran** Total/Subtotal/Jumlah (mis. `^.+ Total$`) → TEGAS + alternatif, terutama bila angkanya = jumlah baris sejak baris berlabel sebelumnya. Tes regresi S12 (+ variasi "Total Jakarta", "Jakarta Jumlah"). |
| B20 | **P1** | Ekor ekspor kasir: "Total Penjualan" diikuti rincian pembayaran tanpa kata kunci ("Tunai", "QRIS") → "Total Penjualan" dianggap *di tengah*, Tunai/QRIS dihitung diam-diam; total alternatif pun salah (318.000 vs 159.000) (S3). | Sesudah baris data utuh terakhir, baris ringkasan berlabel pertama memulai **blok ekor**: baris sesudahnya yang jarang terisi (tanpa ID/tanggal/qty) ikut blok itu → dikeluarkan + disebut, atau minimal masuk TEGAS dan alternatif "tanpa baris 12–14". Tambah kata kunci Tunai/QRIS/Debit/Kartu/Kembalian/Pembayaran di ekor. |
| B21 | P2 | Dua tabel dalam satu file (S5) digabung diam-diam; kolom Qty berisi nominal pengeluaran (535.006), "Sewa lapak" jadi produk. Tanda hanya "nilai tanggal tidak valid". | Baris semua-teks di tengah yang berbeda dari header utama, sesudah baris kosong/judul → GAGAL/TEGAS "tabel kedua mulai baris N; analisis tabel 1 saja atau `--baris-header N`". |
| B22 | P3 | `=SUM(C5,C9,C12)` (SUM daftar sel) tanpa label tidak dianggap rumus agregat (S1b) → TEGAS alih-alih dikeluarkan otomatis (alternatif benar, jadi aman). | Terima SUM/SUBTOTAL dengan daftar referensi sel baris lain sebagai rumus agregat. |
| B23 | P3 | Baris "Halaman 1 dari 2"/judul berulang di tengah mutasi terhitung sebagai baris data kosong (n=9, pivot "(kosong)") (S4); total benar. | Perlakukan seperti header berulang: lewati + info. |

### Skor kualitas uji ulang v1.0.6: **6 / 10** — **belum lulus ke `beta`**; perbaiki B19 & B20 (wajib), B21, lalu uji ulang independen singkat
- (+) Prinsip v1.0.6 tepat dan terbukti: semua fixture lama tanpa (c)/(d) — R6/R7/R8*/R11 dari v1.0.5 kini benar; rumus XLSX dipakai sebagai bukti (SUM/SUBTOTAL/AVERAGE atas baris lain dikeluarkan, SUM/AVERAGE **mendatar** dan `=B*C` tetap data); kandidat ambigu selalu disertai total DENGAN/TANPA yang benar; alur agent AF1/AF2 menyebut kandidat dan tidak memberi satu angka final; negatif, kurung akuntansi, duplikat sah, header berulang ditangani; 94 tes lulus; A/B tetap unggul telak.
- (−) Masih **3 dari 17 file baru salah diam-diam**, dua di antaranya format yang sangat umum bagi UMKM: CSV hasil *Data › Subtotal* Excel (S12, total dobel tanpa peringatan apa pun) dan ekspor kasir dengan rincian Tunai/QRIS di bawah total (S3, total 3× lipat, alternatif pun salah). Karena script tidak memberi tanda, SKILL.md tidak bisa mencegah agent menjawab angka salah. Keduanya perbaikan deteksi yang terlokalisasi (bukan desain ulang), jadi skor 7+ realistis setelah B19–B20.

## Uji ulang v1.0.7 (penguji independen ke-8, cek, 2026-09-25)
Dijalankan dari salinan skill di scratchpad (`uji8-ax/`). Versi script `1.0.7`. Tes bawaan: **107 tes OK** (±36 dtk). Platform: `claude-code (simulasi agent)`.
Fixture baru: `buat_fixture_uji_v107.py` (deterministik; `kunci-v107.json` dihitung dari data sumber, **tanpa membaca kode skill**). XLSX ditulis tangan, **nilai polos tanpa rumus** (meniru "tempel sebagai nilai").

### 1. Regresi semua fixture lama (v1.0.0–v1.0.6) — tidak ada (c)
- v1.0.0–v1.0.5: semua angka = kunci seperti uji v1.0.6 (01 Q1 67.313.000/147; `--sheet semua` 233.556.000/499 untuk 1900 & 1904; lembur 745,5; iuran 5.525.000/91; koperasi 332.635.000; F1/F2/F4/F4b/F5; C5–C7; X1–X5, X3 `--sertakan "Rekap Des"` 6.615.000/33; N1–N8, N10–N13; P1–P4; R1–R16). File rusak/kosong/C1–C4/C8/F3*/N9 tetap GAGAL; C8 `--paksa` + TEGAS. N11, N13, R3, R3c, R5, R6b, R9, R10, R11, R16 tetap b (TEGAS + alternatif = kunci).
- v1.0.6: **S3 c → b** (TEGAS, alternatif TANPA = 159.000 = kunci, qty 10); **S5 c → b** (GAGAL "LEBIH DARI SATU TABEL: tabel kedua mulai baris 6"); **S12 c → b** (3 baris "X Total" kandidat, alternatif 11.200.000 = kunci); **S1b, S1c b → a** (6.425.000, grand total rumus dikeluarkan); S4 a (n=7, "Halaman" tidak lagi jadi baris); S6/S6b b; sisanya a. **0 c, 0 d.**

### 2. File baru → hasil (a = benar, b = TEGAS + alternatif benar / gagal-jelas, c = salah diam-diam di script, d = ditolak padahal wajar)
Kolom "Agent": apakah `profil` wajib + cek sekilas (5 baris pertama/terakhir) memperlihatkan masalahnya → (c) **tertangkap** atau **berisiko lolos**.
| File | Pola | Kunci | Hasil script | Nilai | Agent |
|---|---|---|---|---|---|
| V1 `stok-kategori-subtotal-lengkap.xlsx` | baris judul kategori (1 sel "SEMEN") + "Subtotal Semen" **terisi di semua kolom** (nilai) + TOTAL | 7 barang, stok 293, nilai 19.845.000 | TOTAL ekor dikeluarkan ✔; 3 subtotal **ikut diam-diam** → 586 / **39.690.000 (dobel)**; judul kategori jadi 3 baris data kosong (n=13) | c | tertangkap (baris 5, 10, 14 "Subtotal …" tampak di cek sekilas); `--buang-baris 5,10,14` → 293 / 19.845.000 ✔ |
| V2 `pivot-nilai-id.xlsx` | pivot Excel ID disalin nilai: "Jumlah dari Penjualan/Label Kolom", "Label Baris", "Total Keseluruhan" (baris & kolom) | Sep 2.850.000; total 7.850.000 | judul kolom baris 2 ✔; baris Total Keseluruhan dikeluarkan ✔; semua kolom = kunci | a | — |
| V3 `pivot-ringkas-en.csv` | pivot bentuk ringkas: "Jawa 5.000.000" (subtotal **di atas** anak Kopi/Teh), "Sumatra", Grand Total | 4 daun, 7.500.000 | Grand Total dikeluarkan ✔; Jawa & Sumatra **ikut diam-diam** → **15.000.000** | c | **berisiko lolos** (6 baris tampak, tetapi tidak ada label; SKILL.md tidak menyebut pola "subtotal di atas kelompok") |
| V4 `absensi-jumlah-hadir.csv` | per karyawan 5 hari + baris "Budi, Jumlah Hadir, 4, 31" (terisi lengkap) | 15 baris, jam 93 | **186 (dobel)**, n=18, tanpa kandidat | c | tertangkap (baris terakhir "Andi · Jumlah Hadir" tampak; Tanggal "Tidak valid 3"; Status berisi "4"); dua baris lain harus dicari agent sendiri (`--filter "Tanggal=Jumlah Hadir"` → 93 ✔, tetapi nomor baris tidak diberikan) |
| V5 `jurnal-umum-total-lengkap.csv` | `;` + angka ID; baris akhir "30/09/2026; JU-TOTAL; TOTAL; Total jurnal September; 80.750.000; 80.750.000" | 10 baris, D=K=80.750.000 | baris TOTAL (label di kolom ke-3, semua kolom terisi) **tidak dikenali** → **161.500.000** | c | tertangkap (baris terakhir tampak jelas) |
| V6 `cabang-subtotal-lengkap.csv` | "Subtotal Cabang X" di kolom Produk, tanggal/cabang/qty/omzet terisi + "Grand Total" terisi | 8 baris, 4.620.000 (Bekasi 1.560.000, Bogor 1.410.000, Depok 1.650.000) | **13.860.000 (3×)**, pivot "Semua Cabang" 33,3%; tanpa kandidat | c | tertangkap (AF1 di bawah) |
| V7 `efaktur-fk-of.csv` | e-Faktur lama: rekaman FK/LT/OF, jumlah kolom berbeda | DPP 17.500.000 | `GAGAL: Jumlah kolom tidak cocok di 6 baris` (pesan umum, tidak menyebut format e-Faktur) | b | — |
| V8 `coretax-faktur-keluaran.csv` | daftar faktur gaya Coretax, NPWP 16 digit, nomor faktur 14 digit | DPP 23.900.000, DPP NL 21.908.334, PPN 2.629.000 | ✔; NPWP & nomor faktur = kode (tidak dijumlah), NPWP ditandai sensitif | a | (catatan: "Masa Pajak=45", "Tahun=10.130" ikut dijumlah di `ringkas` — kosmetik) |
| V9 `gobiz-transaksi.csv` | waktu ISO `2026-09-01T11:23:45+07:00`, `Rp45.000`, `-Rp9.000` | kotor 395.000, komisi −79.000, bersih 306.000 | ✔ termasuk pivot per hari | a | — |
| V10 `grabmerchant-angka-inggris.csv` | `"52,000.00"` gaya Inggris, "01 Sep 2026 11:23" | 288.000 / 57.600 / 230.400 | ✔ | a | — |
| V11 `eropa-koma-desimal.csv` | `;`, `2,5`, `1.200`, `1.049,99` | Menge 1.216,25; Betrag 4.321,47 | ✔ | a | — |
| V12 `bulan-melebar.xlsx` | Produk × Jan..Des + kolom Total + baris TOTAL | per bulan (Jan 2.700.000 … Des 2.900.000), 33.600.000 | ✔ TOTAL dikeluarkan, semua kolom bulan = kunci | a | — |
| V13 `tanpa-header.csv` | tabel tanpa baris judul kolom (baris 1 = transaksi) | 6 baris, 1.015.000 | baris 1 dipakai sebagai judul kolom ("2026-09-01", "150000") **tanpa peringatan** → 5 baris, **865.000**; `--baris-header 0` diterima tetapi tidak berefek | c | berisiko lolos (nama kolom aneh tampak di profil, tetapi SKILL.md tidak menyuruh memeriksa judul kolom; tidak ada opsi "tanpa judul") |
| K1 `kontrol-biaya.csv` | rapi | 15, 2.062.500; per kategori | ✔ | a | — |
| K2 `kontrol-stok.xlsx` | rapi | stok 215, harga 237.500 | ✔ | a | — |
| K3 `kontrol-nilai-siswa.csv` | rapi, `;`, `85,5` | Σ 410,50; rata 7A 83,83 | ✔ | a | — |

**Ringkas:** 16 file baru; **9 a, 1 b, 6 c, 0 d**. Tabel rapi + ekspor datar (kontrol, Coretax, GoBiz, Grab, Eropa, pivot ID, bulan melebar) **semuanya a**. Semua (c) ada di **laporan berformat**: 4 dari 6 (V1, V4, V5, V6) **tertangkap** oleh cek sekilas `profil`; 2 (V3, V13) berisiko lolos.
Akar masalah umum (c) V1/V4/V5/V6: detektor kandidat v1.0.7 hanya melihat baris yang **lebih jarang terisi**; baris ringkasan **terisi lengkap** dengan label jelas ("Subtotal …", "Grand Total", "Jumlah Hadir", "TOTAL"/"JU-TOTAL") di kolom mana pun lolos — di tengah **dan** di ekor (V5).

### 3. Uji alur agent (mengikuti SKILL.md persis)
**AF1 — V6 (ambigu, script diam)** "Omzet September per cabang berapa, totalnya?" → `profil` (wajib) → cek sekilas memperlihatkan baris 5/9/12 "Subtotal Cabang …" dan 13 "Grand Total"; script tidak menyebutnya → sesuai langkah 1 agent **tidak memberi angka final**, menjalankan `pivot --grup Cabang --nilai Omzet` dan versi `--buang-baris 5,9,12,13`. Jawaban agent:
> **Jawaban singkat:** Sebelum angka final, satu hal perlu dipastikan: baris 5, 9, 12 ("Subtotal Cabang Bekasi/Bogor/Depok") dan baris 13 ("Grand Total") tampaknya baris **rekap**, bukan transaksi, dan masih ikut dihitung script. **Bila itu rekap** (paling mungkin): total omzet **Rp 4.620.000** — Depok Rp 1.650.000 (35,7%), Bekasi Rp 1.560.000 (33,8%), Bogor Rp 1.410.000 (30,5%). Bila ikut dihitung, totalnya jadi Rp 13.860.000 (3× lipat). Betul keempat baris itu rekap?
> **Perlu dicek:** Grand Total di file (Rp 4.620.000) sama dengan versi tanpa baris rekap — menguatkan bahwa baris itu bukan transaksi.

`profil` dijalankan ✔, baris awal/akhir diperiksa ✔, kandidat disebut dengan nomor baris ✔, angka dari script ✔, jujur & bertanya sekali ✔. Catatan: di file yang lebih panjang, subtotal di tengah bisa jatuh di "… (n baris lain)" (lihat V4) — agent hanya melihat pola dari baris terakhir.

**AF2 — K1 (rapi)** "Biaya bulan ini paling banyak ke mana?" → `profil` (kolom Tanggal/Kategori/Keterangan/Nominal; 15 baris; tidak ada baris dikeluarkan/kandidat; 5 baris awal & akhir = transaksi) → `pivot --grup Kategori --nilai Nominal`. Jawaban: "Terbesar ATK Rp 600.000 (29,1%), lalu Transport Rp 550.000 (26,7%), Listrik Rp 500.000 (24,2%), Konsumsi Rp 412.500 (20,0%); total Rp 2.062.500 dari 15 catatan." = kunci ✔; tidak ada pertanyaan yang tidak perlu ✔.

**Penilaian alur:** langkah 1 v1.0.7 (profil wajib + cek sekilas) **bekerja sebagai pengaman lapis kedua**: 4 dari 6 (c) script tertangkap, termasuk AF1. Celahnya: (i) pola tanpa kata kunci (V3 subtotal di atas kelompok); (ii) judul kolom yang sebenarnya data (V13) tidak ada di daftar cek; (iii) subtotal di tengah file panjang tersembunyi di "… (n baris lain)".

### Bug baru
| # | Prioritas | Temuan | Saran |
|---|---|---|---|
| B24 | **P1** | Baris ringkasan **terisi lengkap** berlabel jelas (Subtotal/Grand Total/Jumlah Hadir/TOTAL, di kolom mana pun, termasuk kode "JU-TOTAL") tidak jadi kandidat — di tengah (V1, V4, V6) maupun di ekor (V5) → dobel/tiga kali diam-diam. | Kata ringkasan utuh di **sel teks mana pun** → kandidat TEGAS + alternatif **tanpa syarat baris jarang** (TEGAS tidak membuang, jadi R5/R7 tetap aman sebagai b); di ekor, label di kolom teks mana pun → dikeluarkan + disebut. Tambahan kuat: angka baris = jumlah blok sejak kandidat/judul sebelumnya. Tes regresi V1, V4, V5, V6. |
| B25 | **P1** | Tabel **tanpa judul kolom** (V13): baris 1 berisi tanggal & angka dipakai sebagai judul tanpa peringatan → 1 transaksi hilang; `--baris-header 0` diam-diam tidak berefek. | Judul kolom yang berisi tanggal/angka murni → PERINGATAN TEGAS "baris 1 tampak data, bukan judul kolom"; opsi `--tanpa-header` (nama Kolom1..N); tolak `--baris-header 0` dengan pesan. Tambah "judul kolom berisi angka/tanggal" ke daftar cek sekilas SKILL.md. |
| B26 | P2 | Pivot bentuk ringkas (V3): baris kelompok berisi subtotal **di atas** anak-anaknya, tanpa kata Total → 2× diam-diam. | Kandidat bila angka baris = jumlah blok baris **tepat di bawahnya** sampai baris kelompok/Total berikutnya; header "Row Labels"/"Label Baris"/"Sum of"/"Jumlah dari" → info "ini pivot yang disalin; hanya baris daun yang dihitung?". |
| B27 | P3 | `profil` tidak memberi nomor baris untuk nilai tidak valid (V4: Tanggal "Tidak valid 3") → agent harus mencari sendiri baris "Jumlah Hadir". | Tampilkan ≤ 5 nomor baris + isi untuk "Tidak valid". |
| B28 | P3 | Baris judul kategori satu sel (V1 "SEMEN") dihitung sebagai baris data kosong (n=13, pivot menampilkan kelompok kosong); e-Faktur FK/OF (V7) GAGAL dengan pesan umum; Masa Pajak/Tahun dijumlah di `ringkas` (V8). | Baris satu-sel teks di tengah → dilewati + info (atau isi turun sebagai kategori); kenali pola kolom-1 FK/LT/OF → pesan khusus; kolom bernama Tahun/Masa/Bulan → kode/periode. |

### Skor kualitas uji ulang v1.0.7: **7 / 10** — **lulus bersyarat ke `beta`**; B24 & B25 wajib diperbaiki sebelum `rilis` (uji ulang independen singkat dengan V1/V3–V6/V13)
- (+) Semua (c) uji v1.0.6 hilang (S3, S5, S12 → b dengan alternatif/pesan benar; S1b/S1c → a), tanpa (c)/(d) baru di 70+ fixture lama; 107 tes lulus.
- (+) Janji yang dinyatakan terpenuhi: **semua tabel rapi & ekspor datar = a** (3 kontrol, Coretax dengan NPWP sebagai kode + tanda sensitif, GoBiz ISO/`-Rp`, Grab `52,000.00`, CSV Eropa, pivot ID, bulan melebar). SKILL.md/README jujur bahwa laporan berformat harus dikonfirmasi.
- (+) Pengaman lapis kedua nyata: `profil` wajib + cek sekilas menangkap 4 dari 6 (c) script (V1, V4, V5, V6); AF1 menghasilkan jawaban jujur dengan kedua total dan satu pertanyaan.
- (−) Detektor umum masih bergantung pada "baris lebih jarang terisi": subtotal/total **terisi lengkap** berlabel jelas lolos di script (6 dari 13 file berformat salah di tingkat script) — perbaikan terlokalisasi (B24).
- (−) 2 kasus berisiko lolos juga dari agent: tabel tanpa judul kolom (V13, kesalahan pengguna awam yang umum) dan pivot bentuk ringkas (V3). Karena itu belum 8.

## Uji ulang v1.0.8 (penguji independen ke-9, cek singkat, 2026-09-25)
Dijalankan dari salinan skill di scratchpad (`uji9-ax/`). Versi script `1.0.8`. Tes bawaan: **119 tes OK** (±42 dtk). Platform: `claude-code (simulasi agent)`.
Fixture baru: `buat_fixture_uji_v108.py` (deterministik; `kunci-v108.json` dihitung dari data sumber, **tanpa membaca kode skill**; XLSX nilai polos tanpa rumus/gaya).

### 1. Regresi semua fixture lama (v1.0.0–v1.0.7)
Semua fixture di `examples/buat_fixture_uji*.py` dijalankan ulang (`ringkas --json`, 100+ file): angka, baris dikeluarkan, kandidat, dan pesan GAGAL **sama dengan uji v1.0.7** (01 Q1 67.313.000/147 untuk 1900 & 1904; lembur 745,5; iuran 5.525.000/91; N11/N13/R3/R3c/R5/R6b/R9/R10/R11/R16/S3/S6/S6b/S12 tetap b dengan alternatif = kunci; S1/S1b/S1c 6.425.000; S5, C1–C4, C8, N9, F3*, file rusak tetap GAGAL; K1–K3, V2, V8–V12 tetap a). **Tidak ada regresi.**
Target B24–B26 (kunci v1.0.7):
| File | v1.0.7 | v1.0.8 | Alternatif / hasil vs kunci |
|---|---|---|---|
| V1 stok subtotal lengkap | c | **b** | TEGAS baris 5,10,14 ("memuat judul kelompok … + kata ringkasan"); judul kategori SEMEN/CAT/BESI + TOTAL dikeluarkan; TANPA = stok 293, nilai 19.845.000 = kunci |
| V3 pivot ringkas EN | c | **b** | TEGAS baris 2,5 ("jumlah 2 baris TEPAT DI BAWAHNYA"); TANPA = 7.500.000 = kunci; catatan "PivotTable disalin" |
| V4 absensi Jumlah Hadir | c | **b** | TEGAS baris 7,13,19; TANPA = 93 jam = kunci |
| V5 jurnal TOTAL lengkap | c | **b** | TEGAS baris 12; TANPA D = K = 80.750.000 = kunci |
| V6 subtotal cabang lengkap | c | **b** | TEGAS baris 5,9,12,13; TANPA = 4.620.000 / qty 40 = kunci |
| V13 tanpa header | c | **a** | PERINGATAN TEGAS tanpa judul kolom; 6 baris, 1.015.000 = kunci (Kolom1..N) |
| V7 e-Faktur FK/OF | b | b | GAGAL khusus e-Faktur format lama (B28 ✔) |

### 2. File baru → hasil (a = benar, b = TEGAS + alternatif benar / gagal-jelas, c = salah diam-diam di script, d = ditolak padahal wajar)
| File | Pola | Kunci | Hasil script | Nilai | Agent |
|---|---|---|---|---|---|
| W1 `tanpa-header-teks-dulu.csv` | tanpa judul, baris 1 = "Budi Santoso, Jakarta, Kaos Polos, 3, 75000, 225000" | 7 baris, qty 18, 2.050.000 | TEGAS tanpa judul; 7 baris; 18 / 2.050.000; pivot per kota ✔; `--baris-header 1` tetap bisa (6 baris) | a | — |
| W2 `tanpa-header-no-urut.csv` | `;`, baris 1 = "1;01/09/2026;Semen Gresik;10;55.000;550.000" | 6 baris, qty 62, 6.169.000 | TEGAS; 62 / 6.169.000 ✔ (catatan: nomor urut Kolom1 ikut dijumlah = 21, kosmetik) | a | — |
| W3 `tanpa-header-tanggal.xlsx` | XLSX tanpa judul, tanggal serial + teks + angka | 6 baris, 2.090.000 | TEGAS; 2.090.000 ✔ (serial tanggal tanpa gaya dijumlah 277.644 — wajar karena file uji tanpa format tanggal) | a | — |
| W4 `header-tahun.csv` | judul "Produk,2024,2025" | 2024 35.800.000; 2025 41.150.000 | tetap judul (tanpa peringatan palsu) ✔; `--tanpa-header` memaksa sesuai dokumen | a | — |
| W5 `header-nomor-bulan.xlsx` | judul angka numerik 1..12, isi bilangan kecil (kunjungan) | per bulan (1=50 … 12=66), 659 | tetap judul, semua bulan = kunci | a | — |
| W5b `header-tahun-numerik.xlsx` | judul angka numerik 2023/2024/2025, isi bilangan kecil | 77 / 84 / 91 | angka ✔; nama kolom tampil **"2.023", "2.024", "2.025"** (pemisah ribuan pada judul) | a | kosmetik (B30) |
| W6 `subtotal-penuh-multikolom.csv` | "Total Barat/Timur/Tengah" + "Total Semua Wilayah" terisi penuh di 7 kolom | 8 baris; qty 45, omzet 7.960.000, HPP 4.840.000, laba 3.120.000 | TEGAS baris 5,8,12,13 ("angka di 4 kolom = jumlah blok"); TANPA semua 4 kolom = kunci; `--buang-baris` → pivot wilayah = kunci | b | — |
| W7 `kebetulan-x-plus-y.csv` | rapi; baris 3 = baris 1 + 2 di Qty **dan** Total | 7 baris, 47 / 2.230.000 | tidak ada kandidat palsu, tidak dibuang ✔ | a | — |
| W7b `kebetulan-jumlah-blok.xlsx` | rapi; baris 3 = 1+2 **dan** baris 4 = 1+2+3 di Qty & Nominal | 7 baris, 27 / 1.365.000 | tidak ada kandidat palsu ✔ | a | — |
| W8 `pivot-ringkas-id.xlsx` | pivot ringkas ID ("Label Baris", 2 kolom "Jumlah dari"), kelompok Bogor **hanya 1 anak** | 6 daun, qty 51, 6.140.000 | "Total Keseluruhan" dikeluarkan ✔ + catatan pivot, tetapi **tidak ada kandidat** → **12.280.000 / 102 (2×)**; pivot per "Label Baris" mencampur Bekasi/Kopi | **c** | tertangkap kemungkinan besar (DIKELUARKAN menampilkan Total Keseluruhan 6.140.000 ≠ total 12.280.000; catatan "hanya baris paling rinci"; cek sekilas pivot) |
| W9 `pivot-tabular.csv` | tabular: "Bekasi Total" (kolom 2 kosong) + Grand Total | 6.140.000; per cabang | TEGAS baris 4,6,10; Grand Total dikeluarkan; TANPA = 6.140.000 ✔ | b | — |
| W10 `pivot-ringkas-tanpa-kata-kunci.csv` | judul "Wilayah / Produk", subtotal di atas, tanpa Grand Total | 7 daun, 21.200.000 | TEGAS baris 2,6,9; TANPA = 21.200.000 ✔ | b | — |
| W11 `kontrol-uang-saku.csv` | rapi | 650.000; Makan 230.000 | ✔ | a | — |
| W12 `kontrol-stok-atk.xlsx` | rapi | stok 382 | ✔ | a | — |
| W13 `kontrol-nilai.csv` | rapi, `;`, `88,5` | Σ 407,25 | ✔ | a | — |

**Ringkas:** 15 file baru; **11 a, 3 b, 1 c, 0 d.** Tanpa-header (teks/angka/tanggal pertama) semua benar + TEGAS; judul kolom tahun/nomor bulan tidak salah dikira data; kebetulan x+y=z **tidak** dibuang dan tidak memicu kandidat palsu.
Diagnosis W8 (varian di scratchpad): pivot ringkas yang sama **tanpa kelompok 1-anak** → b (TEGAS baris 2,5, alternatif benar), baik 1 maupun 2 kolom nilai. Jadi satu kelompok beranak tunggal (baris kelompok = baris anak persis) **mematikan deteksi semua kelompok** di file itu.

### Bug baru
| # | Prioritas | Temuan | Saran |
|---|---|---|---|
| B29 | **P1** | Pivot bentuk ringkas dengan **satu kelompok beranak tunggal** (W8 "Bogor 9 / 1.350.000" lalu "Kopi 9 / 1.350.000") → tidak ada kandidat sama sekali, total 2× diam-diam (hanya catatan umum pivot). Pola sangat umum di PivotTable. | Izinkan blok 1 baris (baris kelompok = baris tepat di bawahnya) selama kelompok lain di file cocok; jangan batalkan seluruh deteksi karena satu blok. Tes regresi W8. |
| B30 | P3 | Judul kolom numerik XLSX tampil dengan pemisah ribuan ("2.023"). | Judul kolom angka bulat → tampilkan apa adanya ("2023"). |
| B31 | P2 | Pengaman silang belum ada: baris "Total Keseluruhan/Grand Total" yang **dikeluarkan** bernilai 6.140.000 sementara total hasil 12.280.000 (tepat 2×) tanpa peringatan. | Bila total ekor yang dikeluarkan ≠ total hitungan (terutama rasio bulat 2×/3×) → PERINGATAN TEGAS "total di file berbeda dengan hasil hitungan". Menangkap B29 dan tata letak baru lain. |
| B32 | P3 | Tanpa-header: kolom nomor urut (Kolom1 = 1..6) ikut dijumlah di `ringkas` (W2). | Kolom bilangan bulat berurutan 1..n → kode/nomor urut. |

### Skor kualitas uji ulang v1.0.8: **8 / 10** — **layak `beta`**; B29 (+ B31 disarankan) diperbaiki sebelum `rilis`
- (+) Keenam (c) uji v1.0.7 hilang: V1/V3/V4/V5/V6 → b dengan alternatif = kunci; V13 → a. Tanpa regresi di 100+ fixture lama; 119 tes lulus.
- (+) Fitur baru tanpa-header akurat di 3 bentuk (teks, nomor urut + tanggal ID, XLSX tanggal) dan **tidak** salah memicu pada judul tahun (CSV & XLSX numerik) atau nomor bulan 1..12.
- (+) Tidak ada positif palsu pada kebetulan x+y=z di 2 kolom (W7, W7b dengan dua kebetulan beruntun): data rapi tetap a.
- (+) Subtotal terisi penuh di 4 kolom & pivot tabular/ringkas tanpa kata kunci → b dengan alternatif benar.
- (−) Satu (c) baru: pivot ringkas dengan kelompok beranak tunggal (B29) — pola umum; kemungkinan besar tertangkap agent lewat Total Keseluruhan yang dikeluarkan (½ dari hasil), tetapi script diam. Karena itu belum 9.
