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
