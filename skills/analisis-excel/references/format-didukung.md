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
- **Tanda kutip tak tertutup** (v1.0.1, diperbaiki v1.0.2): parser `csv` Python = sumber kebenaran.
  - Kutip tak tertutup **sampai akhir file** → selalu `GAGAL: CSV rusak: tanda kutip (") di baris N
    tidak ditutup …` (juga dengan `--paksa`).
  - Sel multi-baris dianggap **curiga** hanya bila (a) ≥ 2 baris di dalam sel tampak seperti baris
    data utuh — cukup banyak sel dan kolom yang biasanya berisi angka memang berisi angka — atau
    (b) jumlah sel rekaman itu ≠ jumlah kolom tabel. Curiga → `GAGAL: CSV kemungkinan rusak …`
    dengan nomor baris dan saran `--paksa`.
  - `--paksa` → dibaca apa adanya + peringatan (angka bisa salah bila kutip memang rusak).
  - Sel multi-baris sah (alamat "Jl. …, No. …⏎Kel. …, Kec. …", koma di beberapa baris) → terbaca +
    **satu** peringatan gabungan yang memetakan nomor baris Notepad ke nomor baris Excel (nomor
    baris di hasil = nomor baris Excel/rekaman).
- Baris yang berisi lebih banyak sel daripada judul kolom (koma tak dikutip) → peringatan + nomor baris.

## Header & baris khusus
- **Header:** baris pertama (dari 30 teratas) yang cukup lebar (≥ 60% kolom terlebar) dan dominan
  teks; baris judul laporan/keterangan di atasnya dilewati dan diberitahukan. Paksa `--baris-header N`.
- Nama kolom kosong → `Kolom C`; nama ganda → `Nama (2)`.
- **Baris Total/Jumlah/Subtotal/Grand Total** (sel isi pertama) → dilewati + peringatan (nomor
  baris). Nonaktifkan dengan `--pertahankan-total`.
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
  nama kolom diawali No/Nomor/ID/Kode/NIK/NPWP/SKU/HP/Telp/Rekening/Resi dengan isi bilangan bulat.
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
