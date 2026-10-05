# Catatan pembuat — crm-wa v1.0.2 (perawatan, 2026-09-25)

- **Peran:** pembuat/perevisi skill (bukan penguji independen). Perbaikan ini menindaklanjuti cacat rendah/kosmetik
  yang tersisa di `examples/HASIL-UJI.md` (bagian "Uji ulang v1.0.1", skor 8/10 lulus). `HASIL-UJI.md` **tidak diubah**;
  catatan lengkap ada di sini.
- **Lingkungan:** Linux, Python 3.11. Reproduksi & data uji di scratchpad (`/tmp/.../scratchpad/crm`), bukan di repo.
  Semua nomor/nama fiktif.
- Tidak ada fitur baru ditambahkan; tidak ada perilaku lain yang diubah. `python3 tests/uji_regresi.py`:
  **57 tes OK** (53 lama + 4 baru). `python3 scripts/validate.py`: **68 skill valid, 68 baris katalog sesuai.**

## Temuan yang diperbaiki

### N1 — Rendah — `hal_untuk_draf` (draf pesan) tidak memotong di titik, "sejuta" tak dikenali, koma desimal salah potong
- **Reproduksi (sebelum perbaikan):**
  - `"kue 450 ribu. orangnya pelit banget"` → draf **"Soal kue . orangnya pelit banget"** (titik "." nyasar).
  - `"kue sejuta untuk mantan pacar"` → masuk utuh ke draf ("sejuta" tidak dikenali sebagai nominal).
  - `"kue 1,5 juta untuk ultah mertua yang cerewet"` → **"kue 1"** (koma dianggap pemisah komentar sebelum nominal
    sempat dibuang, sehingga "5 juta" ikut terbuang).
  - `"brownies 4.500.000 rupiah dp 50%..."` → **"brownies rupiah"** (kata "rupiah" berdiri sendiri tidak dibuang).
- **Perbaikan** (`scripts/crm.py`, `hal_untuk_draf` + `POLA_UANG`):
  1. Koma yang menjadi pemisah komentar sekarang hanya dipotong bila **tidak diikuti angka**
     (`,(?!\d)`), sehingga koma desimal di dalam nominal ("1,5 juta") tidak lagi memutus kalimat sebelum
     nominalnya sempat dibuang.
  2. Titik yang diikuti spasi/akhir kalimat (`\.(?=\s|$)`) sekarang ikut jadi titik potong, sejajar dengan koma/
     titik koma/kurung yang sudah ada — komentar setelah titik dianggap catatan pribadi seperti yang lain.
  3. `POLA_UANG` ditambah `\bse(ribu|ratus ribu|puluh ribu|juta|ratus juta)\b` dan `\brupiah\b` supaya kata
     angka/satuan uang tanpa digit ikut dibuang, bukan hanya nominal berangka.
- **Hasil setelah perbaikan** (diverifikasi langsung, lihat juga `test_n1_kebutuhan_titik_koma_desimal_dan_kata_angka`
  di `tests/uji_regresi.py`):
  - `"kue 450 ribu. orangnya pelit banget"` → `"kue"`
  - `"kue sejuta untuk mantan pacar"` → `"kue untuk mantan pacar"`
  - `"kue 1,5 juta untuk ultah mertua yang cerewet"` → `"kue untuk ultah mertua yang cerewet"`
  - `"brownies 4.500.000 rupiah dp 50%..."` → `"brownies"`
  - Kasus lama (S5) yang sudah benar tetap benar: `"kue ultah 450rb, suaminya pelit"` → `"kue ultah"`,
    `"katering 100 box"` → tidak berubah, `"sofa Rp 4.500.000 (nego)"` → `"sofa"`,
    `"hampers (budget 2jt) - buat bos yang cerewet"` → `"hampers"`.
- **Cakupan tersisa (tidak diklaim tuntas):** kata angka lain yang jarang dipakai (mis. "seratus lima puluh ribu"
  tanpa kata "ribu" di akhir, ejaan alternatif) belum dicakup; risikonya tetap rendah karena aturan wajib 5 di
  SKILL.md melarang isian seperti ini dan manusia selalu memeriksa draf sebelum kirim (mitigasi yang sama seperti
  di v1.0.1).

### N2 — Rendah — Kutip (`"`) tak tertutup di CSV menelan baris berikutnya tanpa disebut
- **Reproduksi:** file dengan baris `"Bu Eka;0812-0000-0052;kue` (kutip dibuka, tak pernah ditutup) diikuti baris
  `Budi;081200000053` → csv.reader Python menggabungkan kedua baris fisik menjadi **satu baris logis** (baris 4-5).
  Baris "Budi" tidak pernah muncul terpisah di `rusak` maupun `baru`, dan pratinjau lama hanya menyebut
  "2 baris data dibaca" tanpa penjelasan kenapa satu baris hilang begitu saja.
- **Perbaikan** (`scripts/crm.py`, `baca_csv`): setiap kali satu baris logis (yang tidak kosong) ternyata mencakup
  lebih dari satu nomor baris fisik, dicatat rentangnya; bila ada, ditambahkan satu peringatan ringkas:
  *"N baris di file dibaca menyatu dengan baris sesudahnya (4-5, ...): kemungkinan ada tanda kutip (") yang tidak
  tertutup. Baris yang ikut tertelan TIDAK diimpor terpisah -- periksa baris ini di file aslinya."* Peringatan ini
  otomatis tampil di teks pratinjau (lewat mekanisme "Catatan: ..." yang sudah ada di `jalankan_tulis`) maupun JSON
  `peringatan`, jadi terlihat SEBELUM `--ya`.
- **Perilaku impor itu sendiri tidak diubah** (baris yang tertelan tetap tidak bisa dipulihkan secara ajaib —
  pengguna diarahkan memeriksa file aslinya), hanya transparansi yang ditambah. Diuji di
  `test_n2_kutip_tak_tertutup_diberi_peringatan`.

### N3 — Rendah (sudah ada sejak v1.0.0) — Kontak impor tanpa `tgl masuk` tidak disebut di pratinjau
- **Reproduksi:** impor CSV tanpa kolom `tgl masuk` (atau kolomnya kosong) → setiap kontak diberi `tgl_masuk` = hari
  impor secara diam-diam, sehingga ikut terhitung sebagai "lead masuk" bulan itu di `rekap`/konversi — tanpa
  disebutkan sama sekali di pratinjau impor.
- **Perbaikan** (`scripts/crm.py`, `cmd_impor`): ditambahkan hitungan `n_tanpa_masuk` (kontak yang benar-benar
  disimpan, bukan yang dilewati sebagai duplikat/rusak) dan satu peringatan ringkas bila > 0:
  *"N kontak tanpa kolom/tanggal masuk: dianggap masuk <tanggal>, jadi ikut terhitung sebagai lead baru bulan ini
  di rekap. Isi kolom 'tgl masuk' di file bila tanggal aslinya berbeda."*
- **Sengaja tidak diubah:** default tanggalnya sendiri (masih = hari impor) — mengubah default itu (mis. menambah
  opsi `--masuk-default`, atau membiarkan kosong) adalah keputusan desain yang memengaruhi definisi "lead masuk" di
  seluruh skill dan perlu persetujuan pemilik; di sini hanya transparansi pratinjau yang ditambah, sesuai batas
  tugas perawatan. Diuji di `test_n3_tanpa_tgl_masuk_diberi_peringatan` (termasuk kasus sebagian kolom terisi dan
  kasus semua terisi → tidak ada peringatan).

### K2 (sebagian) — Kosmetik — Pesan "jadwal prospek lama diganti" muncul pada kontak yang BARU dibuat
- **Reproduksi:** `tambah --nama ... --tahap deal` (kontak baru, bukan pindah tahap) menampilkan peringatan
  *"...jadwal konfirmasi order dipasang ...; **jadwal prospek lama diganti**..."* padahal kontak ini baru saja
  dibuat — tidak ada "jadwal lama" apa pun yang diganti.
- **Perbaikan** (`scripts/crm.py`, `followup_default`): fungsi menerima parameter `ganti` (default `True`, agar
  pemanggil di `cmd_catat`/pindah tahap kontak yang sudah ada — perilaku lama — tidak berubah). Pemanggilan dari
  `cmd_tambah` (kontak baru) memakai `ganti=False`, sehingga frasa "; jadwal prospek lama diganti" tidak lagi
  ditampilkan untuk kontak baru. Diuji di
  `test_k2_pesan_jadwal_tidak_menyebut_diganti_untuk_kontak_baru` (memverifikasi kedua jalur: kontak baru → tanpa
  "diganti"; kontak lama pindah tahap → pesan lama tetap ada, tidak ada regresi).

## Temuan yang TIDAK diperbaiki (keputusan desain / berisiko) — dicatat, bukan diubah

- **K2 (sisa) — pengelompokan deal berjadwal besok masuk hitungan/blok BESOK** (`kelompok_followup`,
  `followup.besok`). Dokumentasi (`kelompok_followup` docstring, SKILL.md, `references/perintah.md`) menyatakan
  "order" hanya untuk konfirmasi yang **hari ini atau sudah lewat**; kontak deal dengan jadwal **besok** karena itu
  jatuh ke jalur umum dan ikut tercampur ke blok/hitungan "BESOK" bersama prospek biasa. Ini memengaruhi angka
  `followup.besok` yang sudah diverifikasi 0-beda oleh penguji independen di beberapa skenario — mengubahnya
  berisiko menggeser definisi rekap yang sudah disepakati dan perlu keputusan desain (apakah deal-besok punya blok
  "ORDER BESOK" sendiri, atau tetap seperti sekarang) dari pemilik. **Tidak diubah.**
- **K1 (sisa) — inisial samaran bisa sama** ("Bu R." untuk Ratna & Rina) **dan format nomor telepon rumah** tanpa
  pemisah. Ini murni keputusan tampilan/algoritma penyamaran (berapa karakter inisial, cara mendeteksi & memformat
  nomor rumah lokal) — berisiko mengubah keluaran `--samarkan` yang sudah diverifikasi. **Tidak diubah.**
- **R6 — jalur `broadcast-wa` belum mulus** dari ekspor `crm-wa`. Ini melibatkan skill lain
  (`siapkan_broadcast.py`) dan keputusan format kolom lintas-skill (kolom persetujuan/berhenti promo) — di luar
  cakupan perawatan satu skill ini. **Tidak diubah** (sudah diakui di HASIL-UJI.md v1.0.1 juga).

## Ringkasan uji
- `python3 tests/uji_regresi.py` → **57 tes OK** (semula 53; +4 tes regresi baru: N1, N2, N3, K2).
- `python3 scripts/validate.py` → **68 skill valid, 68 baris katalog sesuai.**
- Tidak ada regresi terdeteksi: seluruh 53 tes lama tetap lolos tanpa perubahan assersi (kecuali penambahan satu
  baris assersi baru di `test_s5_kebutuhan_disaring_dari_draf` untuk kasus kurung yang sudah lama benar).
