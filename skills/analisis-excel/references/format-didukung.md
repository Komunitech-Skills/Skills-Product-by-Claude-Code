# Format yang Didukung & Aturan Pembacaan

Referensi rinci perilaku `scripts/analisis.py`. Semua aturan ini diuji di `tests/uji_regresi.py`.

## File
| Jenis | Didukung | Catatan |
|---|---|---|
| `.xlsx`, `.xlsm` | Ya | Dibaca langsung (zipfile + xml.etree). Makro **tidak** dijalankan. |
| `.csv`, `.tsv`, `.txt` | Ya | Encoding & pemisah dideteksi otomatis |
| `.xls` (Excel 97–2003), file berkata sandi | Tidak | Pesan: buka di Excel → Save As .xlsx/CSV UTF-8 |
| `.ods` (LibreOffice) | Tidak | Pesan: Save As .xlsx/CSV |
| Google Sheets | Lewat unduhan | *File → Download → .xlsx atau .csv* |

Deteksi jenis berdasarkan **isi file**, bukan nama (CSV yang ternyata XLSX tetap terbaca; ".xlsx"
yang isinya bukan Excel ditolak dengan pesan jelas).

## XLSX
- **Sheet:** default sheet pertama yang terlihat; `--sheet "Nama"` atau `--sheet 2`. Sheet
  tersembunyi ditandai. Sheet tidak ada → daftar sheet yang tersedia.
- **Gabung beberapa sheet (v1.0.1):** `--sheet semua` (semua sheet terlihat; sheet tersembunyi
  dilewati + dicatat) atau `--sheet "Q1,Q2,Q3"` (nama/nomor, boleh sheet tersembunyi). Tiap sheet
  dideteksi header & baris Total-nya sendiri (Total dibuang per sheet), lalu digabung dengan kolom
  tambahan **`Sheet`** (asal sheet). Judul kolom dicocokkan per nama (tidak peka huruf besar-kecil,
  urutan boleh beda). Sheet yang kurang/lebih kolom tetap digabung bila ≥ 50% kolomnya sama
  (kolom hilang = kosong, kolom tambahan diabaikan) + peringatan; bila < 50% → sheet **tidak**
  digabung + peringatan. Nomor baris ditulis `Sheet:baris` (mis. `Q2:68`). Peringatan per sheet
  diberi awalan `Sheet 'Q2': …`. Nama sheet yang memang mengandung koma tetap bisa dipilih utuh;
  di dalam daftar pakai nomornya (`--sheet "1,5"`) — pesan GAGAL menyarankannya (v1.0.2).
- **Acuan struktur (v1.0.2):** sheet yang judul kolomnya cocok dengan sheet terbanyak (seri: yang
  paling depan), bukan otomatis sheet pertama — sheet `Ringkasan`/`Rekap`/`Cover` berstruktur beda
  dilewati + peringatan, dan catatan menyebut acuan yang dipakai. Paksa dengan `--acuan "<nama sheet>"`
  (harus salah satu sheet yang digabung).
- **Sheet rekap/ringkasan (v1.0.3):** dengan `--sheet semua`, sheet dilewati + peringatan "TIDAK
  digabung: tampak sheet REKAP/RINGKASAN (alasan)" bila (a) namanya mengandung Ringkasan/Rangkuman/
  Rekap/Recap/Total/Summary/Ikhtisar/Resume/Pivot/Dashboard, (b) jumlah salah satu kolom angkanya (atau
  semua kolom angkanya) = jumlah gabungan sheet lain (selisih ≤ 0,5%, minimal 2 sheet lain, barisnya
  lebih sedikit), atau (c) 2–16 baris yang tiap barisnya berlabel bulan/triwulan berbeda sementara sheet
  lain ≥ 2× lebih panjang. `--sertakan "Nama"` (atau `--acuan`) memaksa ikut + peringatan. Pada daftar
  eksplisit (`--sheet "A,B,C"`) sheet tidak dilewati, hanya diperingatkan.
- **Cek dobel hitung umum (v1.0.3):** ≥ 3 sheet digabung dan di satu kolom angka total gabungan ≈ 2 ×
  total tanpa satu sheet → "PERINGATAN kemungkinan DOBEL HITUNG" + total tanpa sheet itu.
- **Teks:** shared strings (termasuk rich text per-karakter; teks fonetik `rPh` diabaikan), inline
  string, hasil rumus teks.
- **Angka:** dibaca sebagai Decimal dari teks tersimpan, dibulatkan ke 15 digit signifikan seperti
  tampilan Excel (mis. `0.30000000000000004` → `0,3`).
- **Tanggal:** sel angka dengan format tanggal (format bawaan 14–22, 27–36, 45–47, 50–58, atau
  format kustom berisi d/m/y/h/s). Sistem 1900: serial 1 = 1 Jan 1900; serial 60 = 29 Feb 1900 yang
  **tidak pernah ada** (bug warisan Lotus 1-2-3) → ditandai tidak valid + peringatan; serial ≥ 61
  dihitung dari 30 Des 1899. Sistem 1904 (Mac lama) dideteksi dari `workbookPr date1904`. Jam
  diabaikan (hanya tanggal). Serial < 1 berformat waktu → teks "HH:MM".
- **Boolean** → teks `TRUE`/`FALSE`. **Galat** (`#N/A`, `#DIV/0!`, …) → kosong + peringatan.
- **Rumus tanpa nilai tersimpan** → kosong + peringatan (daftar sel). Rumus dengan nilai tersimpan
  → nilai tersimpan dipakai (rumus tidak dihitung ulang).
- **Sel gabungan:** gabungan vertikal/blok berisi teks → teks disalin ke seluruh rentang;
  gabungan mendatar satu baris (judul) → tidak disalin; berisi angka → tidak disalin.
- **Keamanan:** XML sheet > 800 MB setelah ekstraksi ditolak (lindungi dari zip bomb).

## CSV
- **Encoding:** UTF-8, UTF-8 BOM, UTF-16 (BOM), selain itu cp1252/ANSI Excel Windows (dengan
  peringatan). Paksa dengan `--encoding latin-1` dsb.
- **Pemisah:** `,` `;` tab `|` dipilih dari konsistensi jumlah kolom; baris `sep=;` di awal file
  (ekspor Excel) dihormati. Paksa dengan `--pemisah ";"`.
- **INVARIAN JUMLAH KOLOM (v1.0.4, dilonggarkan aman di v1.0.5)** — pengaman utama angka CSV, sederhana & bisa dijelaskan:
  setelah dibaca parser `csv` Python, **setiap baris data wajib punya jumlah kolom = jumlah judul
  kolom** (sampai judul terakhir yang berisi).
  - Toleransi: sel **kosong** berlebih di ujung kanan (padding Excel `Ani,5000,,`), dan judul yang juga
    diikuti sel kosong (`Nama;Nominal;;`).
  - **Kolom opsional di ujung kanan (v1.0.5):** baris yang kekurangan sel **hanya di kolom paling kanan**
    diterima (sel hilang = kosong) + info "N baris tidak punya sel untuk kolom paling kanan ('Catatan')",
    bila (a) kolom-kolom yang hilang itu kosong/tidak ada di ≥ 50% baris data lain, **dan** (b) setiap sel
    yang ada cocok tipe kolomnya (angka di kolom angka, tanggal di kolom tanggal, teks di kolom teks; tipe
    diukur dari baris yang lebih panjang). Contoh: kolom "Catatan" yang hanya diisi sebagian dan komanya
    tidak diketik. Bila kolom yang hilang biasanya terisi ("kolom 'Jumlah' tidak ada, padahal biasanya
    terisi") atau ada isi yang bergeser ("angka '18000' masuk kolom 'Barang' yang biasanya teks") → tetap
    GAGAL.
  - Baris dengan kolom **kurang** ("hanya 3 dari 4 kolom") atau kolom **lebih yang berisi** ("3 kolom
    terisi, padahal judul kolom hanya 2") → `GAGAL: Jumlah kolom tidak cocok di N baris data …`
    dengan nomor baris Excel (+ baris Notepad bila bergeser karena sel multi-baris) dan isi ringkas.
  - `--paksa` → dibaca apa adanya + "PERINGATAN TEGAS (--paksa): N baris data jumlah kolomnya tidak
    sama … total/rata-rata MUNGKIN SALAH".
  - Hanya baris data yang diperiksa: baris judul laporan di atas header, baris ringkasan (Total/
    Jumlah/Rata-rata/Saldo…, juga tanpa label), blok catatan di bawah tabel, dan baris pengulang judul
    tidak diperiksa (lihat "Header & baris khusus"). Catatan di **tengah** tabel (ada baris data utuh
    sesudahnya) tetap diperiksa → GAGAL bila kolomnya kurang.
  - Pesan GAGAL menyebut kemungkinan penyebab dalam bahasa awam (sel kosong/terlewat di tengah baris,
    koma di teks tanpa kutip, tanda kutip nyasar, catatan di tengah tabel) dan cara memperbaikinya.
  - Menangkap: sel terlewat (angka jatuh ke kolom teks), koma di teks/angka tanpa kutip, dan hampir
    semua kutip nyasar (rekaman gabungan punya jumlah sel berbeda, mis. alamat sah + satu kutip nyasar).
- **Tanda kutip tak tertutup sampai akhir file** → selalu `GAGAL: CSV rusak: tanda kutip (") di baris
  N tidak ditutup …` (juga dengan `--paksa`).
- **Kutip nyasar yang lolos invarian** (tertutup di baris lain dan jumlah sel kebetulan cocok): tiap
  baris lanjutan sel multi-baris dibaca sendirian; bila jumlah field-nya ≈ jumlah kolom dan kolom
  angka/tanggal di posisinya berisi angka/tanggal → `GAGAL: CSV kemungkinan rusak … kemungkinan N
  baris data HILANG` (`--paksa` → PERINGATAN TEGAS). v1.0.4: cek ini **hanya** untuk kolom yang
  biasanya satu baris (sel multi-baris di kolom itu ≤ 2 atau ≤ 10% baris). Kolom yang memang berisi
  alamat/catatan berbaris-baris tidak dicurigai → tidak ada penolakan palsu. Heuristik lama "≥ 2 baris
  di dalam sel tampak seperti data" dihapus (penyebab penolakan palsu C5).
- Kolom yang biasanya satu baris tetapi punya 1–2 sel multi-baris (≥ 10 baris data) → peringatan lunak
  "cek baris N, mungkin ada tanda kutip nyasar; bila memang catatan, abaikan".
- Sel multi-baris sah → terbaca + **satu info** (bukan peringatan) yang memetakan nomor baris Notepad
  ke nomor baris Excel (nomor baris di hasil = nomor baris Excel/rekaman).
- XLSX tidak terkena invarian (tidak ada pemisah/kutip); sel di kolom tanpa judul → peringatan.

## Header & baris khusus
- **Header:** baris pertama (dari 30 teratas) yang cukup lebar (≥ 60% kolom terlebar) dan dominan
  teks; baris judul laporan/keterangan di atasnya dilewati dan diberitahukan. Paksa `--baris-header N`.
- Nama kolom kosong → `Kolom C`; nama ganda → `Nama (2)`.
- **Baris ringkasan & catatan (v1.0.6 — PRINSIP: keluarkan otomatis HANYA bila tidak ambigu).**
  Versi 1.0.3–1.0.5 menebak dengan aturan label/angka dan ikut membuang data asli (kategori "Rata-rata",
  transaksi yang kebetulan = jumlah di atasnya). Sejak 1.0.6:
  1. **Dikeluarkan otomatis** (disebut di peringatan "BARIS DIKELUARKAN … (alasan): isi", paling atas):
     - **XLSX, sel berumus agregat** `SUM/SUBTOTAL/AVERAGE/COUNT/MIN/MAX/AGGREGATE` atas rentang baris
       LAIN (teks rumus dibaca dari `<f>`, termasuk rumus bersama). Rumus per baris (`=SUM(B5:D5)`) dan saldo
       berjalan (`=SUM($C$2:C5)`, rentangnya memuat baris itu) bukan ringkasan. Nilai POLOS yang kebetulan
       sama dengan jumlah **tidak** dianggap ringkasan.
     - **Blok EKOR**: akhiran tabel yang tiap barisnya (i) berlabel ringkasan — label di **sel teks
       pertama** baris: Total/Jumlah/Subtotal/Grand Total/Rata-rata/Saldo Akhir/Mutasi Kredit/Debet, "Total …"
       di sel isi pertama, "Jumlah pesanan:"; Min/Maks/Median bila satu-satunya teks —, (ii) berawalan
       Catatan/Keterangan/Ket/NB/Note/Sumber/Dicetak/`*` (walau berisi angka, mis. "Catatan: retur,,150000"),
       atau (iii) teks saja yang bergaya catatan atau dipisah baris kosong dari data.
     - **Blok KEPALA**: baris "Saldo Awal"/Opening balance tepat di bawah judul kolom (mutasi bank); judul
       laporan di atas header dilewati oleh deteksi header.
     - Baris yang diminta pengguna: `--buang-baris 5,9` (gabungan sheet: `"TW1:7"`).
  2. **Kandidat — TETAP DIHITUNG**, dengan "PERINGATAN TEGAS — Kemungkinan baris ringkasan ikut terhitung:
     baris N (isi — alasan) … Bila benar ringkasan, ulangi dengan --buang-baris N[,M]. Total alternatif:
     kolom 'X': DENGAN baris itu … / TANPA baris itu …" (JSON: `kemungkinan_ringkasan`, `total_alternatif`):
     - baris berlabel ringkasan di **tengah/atas** tabel (Subtotal per cabang/hari, produk bernama persis
       "TOTAL", kategori "Rata-rata" di kolom pertama);
     - baris angka **tanpa label** (hanya angka di kolom angka, ada kolom yang biasanya terisi ≥ 80% kosong)
       yang setiap angkanya = jumlah baris di atasnya (sejak kandidat/baris dikeluarkan terakhir — kelompok 1
       baris pun — atau seluruhnya) atau rata-ratanya (≥ 3 nilai); di ekor tabel juga min/maks dan agregat
       yang menyertakan baris kandidat sebelumnya (SUM lalu AVERAGE). Toleransi Rp1.
     Kategori di kolom kedua dst. ("Pegawai 02 | Rata-rata", "KLM-002 | Total") bukan label sama sekali.
  3. `--pertahankan-baris N` → baris N dihitung sebagai data dan tidak dicurigai; `--pertahankan-total` →
     tidak ada baris yang dikeluarkan/dicurigai (semua dihitung apa adanya).
  "Saldo" saja (baris saldo di buku kas) tetap data.
- Baris yang mengulang judul kolom (hasil salin-tempel) dan baris kosong → dilewati.

## Tipe kolom
Ditentukan dari isi (≥ 70% nilai terisi cocok):
- **tanggal** — `2026-09-25`, `25/09/2026`, `25-09-26`, `25.09.2026`, `25 Sep 2026`,
  `25 September 2026`, `Kamis, 25 September 2026`, `Sep 25, 2026`, `1 Agustus 2026`, jam di
  belakang diabaikan. Nama bulan Indonesia & Inggris (termasuk Agt/Nop/Peb).
  Urutan hari/bulan: bila ada hari > 12 → pasti; bila semua ≤ 12 → dibaca hari/bulan (Indonesia) +
  peringatan "ambigu"; paksa `--urutan-tanggal mdy`.
- **angka** — `15000`, `Rp 15.000`, `Rp. 25000`, `IDR 25.000`, `Rp 15.000,-`, `1.234.567,89`,
  `15,000.50`, `(5.000)` = negatif, `-Rp 5.000`, `5.000-`, `12,5%`, spasi ribuan `1 234 567`.
  Gaya desimal (Indonesia vs Inggris) ditentukan per kolom dari bukti (mis. `12,5` atau
  `1.234,56` → koma desimal). Tanpa bukti: satu pemisah + tepat 3 digit = ribuan (`1.234` =
  seribu dua ratus tiga puluh empat). Ditolak (tidak valid): `15.000.00`, `15000.500`, `1,5E+06`,
  mata uang lain (`US$ 5`).
- **kode** — angka yang bukan untuk dijumlah: nol di depan (`0812…`), ≥ 11 digit (No HP/NIK), atau
  nama kolom diawali No/Nomor/ID/Kode/NIK/NPWP/SKU/HP/Telp/Rekening/Resi — atau (v1.0.5) diakhiri
  Code/Kode/ID/No/Nomor/Number/Ref ("Transaction Code", "Order ID", "Reference No.") — dengan isi
  bilangan bulat.
- **teks** — selain itu. Spasi dirapikan; beda huruf besar-kecil **dan spasi** (`4 A` = `4A` = `4a`)
  digabung ke penulisan yang paling sering muncul (dilaporkan: jumlah & contoh). `--filter` dan
  `banding --grup` memakai aturan yang sama.
- **uang** (label tampilan `Rp`) — kolom angka yang namanya mengandung harga/total/biaya/nominal/
  omzet/gaji/nilai transaksi/… (bukan qty/pcs/stok/%), atau ≥ 30% isinya bertulisan Rp/IDR.
- Paksa tipe: `--tipe "Kolom=angka|tanggal|teks|kode"`.

## Data sensitif
Kolom bernama NIK/KTP/NPWP/No HP/Telepon/WA/Email/Alamat/Rekening/Gaji/Diagnosis/Agama/Tanggal
lahir/Password/PIN, atau isinya mayoritas email/16 digit/No HP (`08…`, `+628…`) → peringatan UU PDP
(No. 27/2022), contoh isi disembunyikan di `profil`, tidak ditampilkan sebagai label di `top` per baris.

Sejak v1.0.1 isi kolom pribadi bertipe teks/kode yang muncul sebagai **label** di `pivot`, `top`,
`banding --grup`, dan `--kolom-pivot` **disamarkan**: NIK `3201•••••••••408`, HP `0812•••••890`,
email `a•••@contoh.id`, lainnya 3 huruf pertama + `•••`. Pengelompokan tetap memakai nilai lengkap
(dua NIK berbeda tetap dua baris). `--tampilkan-pribadi` menampilkan nilai lengkap + peringatan
tegas. Bila kolom **nilai** sensitif (gaji/upah) ditampilkan per orang/baris → peringatan
"data SENSITIF". `bersihkan` tetap menulis data lengkap ke file milik pengguna sendiri.

## Hitungan baris & peringatan di semua subperintah (v1.0.1)
- `pivot`/`top`: kolom **Baris** = semua baris di kelompok. Bila ada sel nilai kosong/tidak terbaca,
  ditambahkan kolom **Nilai terisi** (di ujung kanan) = baris yang angkanya dihitung (pembagi
  rata-rata) + peringatan dengan nomor baris sel kosong.
- Baris duplikat persis kini diperingatkan juga di `ringkas`, `pivot`, `tren`, `top`, `banding`
  (tetap ikut dihitung; sarannya `bersihkan --buang-duplikat`).
- Kolom teks berisi nama bulan (Juli, Agustus, …) diurut kronologis, bukan abjad.
- `pivot` jumlah dengan nilai negatif (retur) → catatan mengapa kolom "% dari total" tidak ada.

## Batas
| Hal | Batas |
|---|---|
| Ukuran file | 50 MB (lebih → ditolak, kecuali `--paksa`) |
| Baris | nyaman ≤ 300.000 (lebih → peringatan lambat) |
| Kolom pivot silang | 15 nilai berbeda |
| Tren harian | rentang ≤ 400 hari |
| Python | 3.8+ tanpa paket tambahan (Windows/macOS/Linux) |

## Kode keluar
`0` berhasil · `2` masalah input (pesan `GAGAL:` di stderr) · `3` kesalahan tak terduga (tetap
tanpa traceback; sarankan simpan ulang sebagai CSV UTF-8).
