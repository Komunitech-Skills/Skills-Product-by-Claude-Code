---
name: pdf-lokal
description: Mengolah file PDF (gabung, pisah, kompres, OCR, foto ke PDF, putar, watermark, kunci/buka sandi, rapikan resi marketplace untuk dicetak) lewat Stirling-PDF di komputer sendiri; bila Stirling-PDF belum ada, otomatis memakai qpdf/Ghostscript/pdftk yang sudah terpasang (tanpa install, tanpa unggah ke situs luar). Pakai saat pengguna minta "gabung PDF", "kompres PDF biar muat WA/email", "PDF ini kebalik", "scan ini susah dicari teksnya (OCR)", "ubah foto nota jadi PDF", "kunci PDF gaji", "rapikan resi Shopee/Tokopedia biar hemat kertas". Keywords: merge PDF, split PDF, compress PDF, OCR PDF, PDF ke Word tidak termasuk, watermark PDF, password PDF, print resi.
---

# pdf-lokal

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Mengolah PDF sehari-hari milik usaha (kontrak, nota, resi, laporan) dengan memanggil
**Stirling-PDF** yang sudah terpasang & berjalan di komputer pengguna sendiri (bukan
layanan online). File tidak pernah dikirim ke internet - hanya ke `localhost` komputer
yang sama. Ini pengganti Adobe Acrobat Pro / situs "PDF online" berbayar untuk
kebutuhan yang paling sering: gabung, pisah, kompres, OCR, foto jadi PDF, putar,
watermark, kunci/buka sandi, dan menyusun beberapa resi marketplace jadi satu lembar.

## Kapan digunakan
- "Gabungkan nota-nota ini jadi satu PDF"
- "PDF ini kegedean, kompres biar bisa dikirim WA/email/upload marketplace"
- "PDF hasil scan ini teksnya nggak bisa di-copy/dicari" (OCR)
- "Ubah foto nota/struk/KTP ini jadi PDF"
- "Halaman PDF ini kebalik, putar dong"
- "Kasih watermark DRAF/RAHASIA di dokumen ini"
- "Kunci PDF slip gaji ini pakai kata sandi" / "buka kuncinya"
- "Susun resi Shopee ini jadi 4 per lembar biar hemat kertas print"
- "Ambil halaman 3 sampai 7 saja dari PDF ini"

## Kapan TIDAK digunakan
- **Membaca ISI nota/faktur untuk dicatat** (jumlah, tanggal, item) → pakai skill
  `ekstrak-nota-faktur`. pdf-lokal hanya mengolah BENTUK file PDF-nya, bukan
  memahami isinya. **Kalau skill itu belum terpasang/dibeli**, jangan diam saja -
  katakan dengan jelas: "Aku cuma bisa menggabung/merapikan file PDF-nya, belum bisa
  membaca & menjumlah isinya secara otomatis - itu perlu skill `ekstrak-nota-faktur`
  (belum terpasang)." Boleh tetap tawarkan bantuan sebatas kemampuan pdf-lokal (mis.
  gabung dulu jadi 1 file) sambil menjelaskan batasan itu.
- **Membuat slide/presentasi dari PDF** → pakai skill `presentasi-instan`.
- **Mengedit ISI teks/tata letak PDF secara halus** (bukan sekadar gabung/pisah/putar)
  → Stirling-PDF punya editor teks terbatas, tapi skill ini tidak mengekspos fitur itu;
  arahkan ke aplikasi Stirling-PDF langsung atau Word/Google Docs bila sumber aslinya ada.
- **Tanda tangan digital bersertifikat, SSO, multi-user/tim, audit log** → itu fitur
  **proprietary/berbayar** Stirling-PDF, di luar cakupan skill ini (lihat Batasan).
- (Bukan alasan berhenti:) Stirling-PDF belum terpasang/menyala → **pakai jalur cadangan**
  di Langkah kerja 1, jangan langsung menyuruh pengguna memasang Stirling-PDF.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| File PDF/gambar yang diproses | Ya | — (tanyakan nama/lokasi file) |
| Jenis pengolahan (gabung/kompres/dst.) | Ya | Tebak dari kalimat pengguna; kalau ambigu, tanyakan |
| Kata sandi (untuk kunci/buka-kunci) | Ya, khusus itu | — (tanyakan, jangan mengarang) |
| Rentang halaman (untuk pisah-rentang) | Ya, khusus itu | — (tanyakan, mis. "3-7") |
| Level kompres | Tidak | 4 (sedang) dari skala 1-9 |
| Jumlah resi per lembar | Tidak | 4 |
| Bahasa OCR | Tidak | Coba Indonesia dulu, otomatis pakai Inggris bila belum terpasang |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan berisi daftar pertanyaan
singkat bernomor. Contoh: "Sebelum saya proses: (1) file mana saja yang digabung dan
urutannya? (2) mau disimpan di folder yang sama?"

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
1. Cek Stirling-PDF: `python3 scripts/pdf.py cek` (Windows: `py scripts\pdf.py cek`).
   - **Siap dipakai** → lanjut langkah 2 dengan `scripts/pdf.py`.
   - **Gagal terhubung / ditolak** → JANGAN berhenti dan jangan menyuruh pasang dulu.
     Jalankan `python3 scripts/pdf_cadangan.py alat`: script mendeteksi `qpdf`,
     Ghostscript (`gs`/`gswin64c`), dan `pdftk` yang **sudah** terpasang dan mencetak
     perintah mana yang BISA. Bila tugasnya bertanda BISA (gabung, pisah-rentang,
     pisah-halaman, kompres, putar, kunci, buka-kunci) → **kerjakan langsung** dengan
     `scripts/pdf_cadangan.py` (sintaks sama, lihat tabel cadangan), lalu sampaikan
     hasil + satu kalimat: "Stirling-PDF belum menyala, jadi aku pakai <alat> yang sudah
     ada di komputermu - file tidak keluar dari komputer."
   - Tugas butuh Stirling-PDF (OCR, watermark, foto-ke-pdf, rapikan-resi) atau tidak ada
     alat sama sekali → jelaskan singkat, tawarkan "Cara manual" di bawah dan
     `references/pasang-stirling.md` (agent membacakan langkahnya; pengguna yang memasang).
   - **Dilarang:** `pip install`, `apt/brew/winget install`, mengunduh program, atau
     menulis script PDF sendiri dengan library yang belum ada. Bila pypdf/pikepdf
     kebetulan sudah terpasang, boleh dipakai hanya bila script cadangan tidak bisa.
2. Pilih perintah yang sesuai (tabel di bawah), jalankan lewat `scripts/pdf.py`
   (Stirling) atau `scripts/pdf_cadangan.py` (cadangan).
3. Baca pesan keluaran: script selalu mencetak **path lengkap file hasil**. Sampaikan
   path itu apa adanya ke pengguna, jangan mengarang nama file lain.
4. Bila script melapor GAGAL, teruskan pesannya ke pengguna (sudah ditulis dalam
   bahasa awam, sudah termasuk saran perbaikan) - jangan tebak-tebak penyebab lain.
5. File asli TIDAK PERNAH ditimpa; hasil selalu file/folder baru di sebelah file asli.

### Daftar perintah `scripts/pdf.py`
```
cek                                        Cek Stirling-PDF hidup & versinya
gabung file1.pdf file2.pdf ...             Gabung jadi satu PDF
pisah-halaman file.pdf                     Pisah jadi 1 file per halaman (folder)
pisah-rentang file.pdf --halaman 3-7       Ambil rentang halaman jadi 1 file baru
kompres file.pdf --level 1-9               Perkecil ukuran (WA/email/marketplace)
ocr file.pdf --bahasa ind eng              PDF scan jadi bisa dicari/di-copy teksnya
foto-ke-pdf foto1.jpg foto2.jpg            Foto/nota/struk jadi satu PDF
putar file.pdf --derajat 90|180|270        Putar semua halaman
watermark file.pdf --teks "DRAF"           Tambah watermark teks
kunci file.pdf --sandi ...                 Kunci PDF pakai kata sandi
buka-kunci file.pdf --sandi ...            Buka kunci kata sandi
rapikan-resi r1.pdf r2.pdf --per-lembar 4  Susun beberapa resi jadi N per lembar
```
Semua perintah punya `--keluaran PATH` (atau `--keluaran-folder` untuk yang hasilnya
banyak file) untuk menentukan lokasi hasil sendiri; kalau tidak diisi, script memakai
nama otomatis di folder yang sama dengan file asli.

### Daftar perintah `scripts/pdf_cadangan.py` (tanpa Stirling-PDF)
```
alat                                       Deteksi qpdf/gs/pdftk & perintah yang BISA
gabung file1.pdf file2.pdf ...             qpdf > pdftk > gs
pisah-rentang file.pdf --halaman 3-7       qpdf > pdftk > gs (gs: satu rentang saja)
pisah-halaman file.pdf                     qpdf > pdftk (hasil: folder <file>-per-halaman/)
kompres file.pdf --level ringan|sedang|kuat  gs (benar-benar mengecilkan gambar) > qpdf (tanpa-rugi)
putar file.pdf --derajat 90|180|270        qpdf > pdftk (searah jarum jam, semua halaman)
kunci file.pdf --sandi ...                 qpdf (AES-256) > pdftk (AES-128)
buka-kunci file.pdf --sandi ...            qpdf > pdftk
```
Opsi `--keluaran PATH` (atau `--keluaran-folder`) dan `--alat qpdf|gs|pdftk` (paksa alat).
Alat dipanggil tanpa shell; kata sandi untuk qpdf dikirim lewat file argumen sementara
(tidak tampil di daftar proses). Hasil divalidasi (harus PDF); kompres yang tidak
mengecilkan file dibuang dan dilaporkan jujur. Default kompres `sedang` (/ebook ±150 dpi,
cukup tajam untuk nota/dokumen); `kuat` (/screen ±72 dpi) hanya bila masih kebesaran.

**Contoh (Stirling mati, qpdf+gs ada):** "gabungin nota-a, b, c lalu kecilin buat WA" →
```
python3 scripts/pdf.py cek                         # gagal terhubung
python3 scripts/pdf_cadangan.py alat               # gabung via qpdf, kompres via gs: BISA
python3 scripts/pdf_cadangan.py gabung nota-a.pdf nota-b.pdf nota-c.pdf --keluaran nota-gabungan.pdf
python3 scripts/pdf_cadangan.py kompres nota-gabungan.pdf
```
Laporkan ukuran sebelum→sesudah dan path hasil persis seperti dicetak script.

## Format output
Setiap perintah mencetak ringkasan singkat + path lengkap, contoh:
```
Berhasil dikompres: 4200 KB -> 850 KB
  -> /home/andi/Dokumen/laporan-kompres.pdf
```
Untuk perintah yang hasilnya banyak file (`pisah-halaman`), script mencetak folder
lalu daftar setiap file di dalamnya.

## Contoh
**Input pengguna:** "Tolong gabungin 3 nota supplier ini jadi 1 PDF ya, urut sesuai aku kirim"

**Langkah agent:**
```
python3 scripts/pdf.py cek
python3 scripts/pdf.py gabung nota-a.pdf nota-b.pdf nota-c.pdf
```
**Output ke pengguna:** "Sudah digabung jadi 1 file, urutannya sesuai kamu kirim
(nota-a, nota-b, nota-c). Hasilnya: `/Users/sari/Nota/nota-a-gabungan.pdf`"

**Input pengguna:** "Resi Shopee-ku ada 8, mau print hemat kertas"

**Langkah agent:** tanyakan sekali bila belum jelas ("mau 4 atau 2 resi per lembar?"),
lalu jalankan `rapikan-resi resi1.pdf ... resi8.pdf --per-lembar 4`, dan ingatkan
untuk cek Print Preview dulu sebelum cetak massal. **Contoh konkret:** resi
marketplace biasanya PDF kertas thermal kecil (**10×15 cm atau 10×20 cm**). Pada uji
dengan Stirling-PDF 3.0.0 asli, hasil `rapikan-resi` (2 atau 4 per lembar) selalu
berukuran **A4** (21×29,7 cm) — cocok untuk printer biasa, tetapi **bukan** untuk
printer thermal 10×15. Pengguna printer thermal sebaiknya mencetak resi aslinya
satu per satu. Sarankan cetak 1 lembar percobaan dulu sebelum mencetak banyak.

## Cara manual (Stirling-PDF tidak ada DAN jalur cadangan tidak bisa)
Skill tetap berguna sebagai panduan meski script tidak bisa dijalankan:
0. Tanpa aplikasi tambahan: **macOS Preview** bisa gabung (seret thumbnail antar file),
   putar, kunci (File > Export > Encrypt), dan kompres (Export > Quartz Filter "Reduce
   File Size"). **Windows**: ambil rentang halaman lewat Cetak > "Microsoft Print to PDF"
   > isi Halaman; untuk resi, dialog Cetak > "Halaman per lembar 2/4".
1. Buka aplikasi Stirling-PDF (cara pasang: `references/pasang-stirling.md`).
2. Di halaman utama, klik kartu tool yang sesuai (mis. "Merge", "Compress", "OCR / Add
   Text Layer", "Add Password", "N-up / Multi Page Layout" untuk resi).
3. Seret file ke kotak upload, atur opsi di layar, klik proses, lalu unduh hasilnya.
4. **Dokumen BIASA** (nota, resi, katalog produk) dan pengguna tidak mau memasang apa
   pun: boleh arahkan ke situs PDF online resmi milik Stirling-PDF sendiri (bukan situs
   pihak ketiga sembarangan) sebagai alternatif terakhir, dengan catatan jelas bahwa
   file akan diunggah ke internet.
5. **Dokumen SENSITIF** (slip gaji, KTP/data pribadi karyawan, kontrak rahasia, data
   keuangan usaha) → **JANGAN PERNAH** menawarkan opsi upload ke situs online mana pun,
   sekalipun pengguna belum mau memasang Stirling-PDF dan sekalipun situsnya "resmi
   milik Stirling-PDF sendiri". Jelaskan dengan jujur keterbatasannya ("untuk dokumen
   sensitif seperti ini aku tidak akan sarankan upload ke internet; perlu Stirling-PDF
   terpasang lokal dulu, atau proses manual lewat aplikasi PDF/Word biasa di
   komputermu") - ini berlaku bahkan kalau pengguna sendiri yang memintanya diupload.

## Batasan & penanganan error
- **Stirling-PDF mati/belum terpasang** → jalur cadangan `scripts/pdf_cadangan.py`
  (langkah 1). Tidak pernah mengunduh/memasang/menjalankan Stirling-PDF atau alat lain
  secara otomatis. Panduan pasang ada di `references/pasang-stirling.md`.
- **Jalur cadangan** diuji dengan qpdf 11 & Ghostscript 10 di Linux (`tests/uji_cadangan.py`);
  pdftk hanya diuji dengan alat tiruan; Windows/macOS belum diuji langsung. Bila alat
  menolak file (rusak/terkunci/halaman melebihi), script memberi pesan awam, bukan traceback.
- **Endpoint tidak ada di versi Stirling-PDF pengguna** (404) → script menyarankan
  cek versi (`cek`) dan perbarui aplikasinya; tidak berpura-pura berhasil.
- **File terlalu besar** (413) → script menyarankan `kompres` dulu atau menaikkan
  batas ukuran unggah di Pengaturan Stirling-PDF.
- **File terkunci kata sandi / rusak** → script mendeteksi dari respons server dan
  memberi pesan spesifik (minta `buka-kunci` dulu, atau minta cek file aslinya).
- **Bahasa OCR Indonesia belum terpasang** → script mengecek dulu ke server, memberi
  tahu bila harus fallback ke bahasa Inggris, TIDAK diam-diam memakai bahasa yang
  salah tanpa bilang.
- **Fitur berbayar/proprietary Stirling-PDF** (tanda tangan sertifikat, SSO, tim/akun,
  audit log) → **tidak dipanggil oleh skill ini sama sekali**. Kalau pengguna minta
  fitur itu, jelaskan bahwa itu bagian berbayar Stirling-PDF (lisensi terpisah, bukan
  bagian gratis/inti) dan di luar cakupan skill ini.
- **Ukuran kertas hasil "rapikan-resi" diatur Stirling-PDF, bukan skill ini** - pada
  Stirling 3.0.0 hasilnya A4; versi lain bisa berbeda. Selalu sarankan cek Print
  Preview sebelum cetak banyak.
- **Alamat server non-localhost ditolak** kecuali pengguna secara sadar mengaktifkan
  `STIRLING_ALLOW_REMOTE=1` (mis. server kantor di jaringan lokal) - untuk mencegah
  file tidak sengaja terkirim ke tempat lain.
- **Sudah diuji dengan Stirling-PDF v2.14.3 DAN v3.0.0** (keduanya via Docker, image
  resmi `ghcr.io/stirling-tools/stirling-pdf`) - endpoint & nama field yang dipakai
  skill ini identik di kedua versi (lihat `references/sumber-api-stirling.md`).
  **Belum diuji dengan aplikasi desktop resmi (.msi/.dmg)** - hanya lewat image Docker
  resmi karena keterbatasan lingkungan pembuatan skill. Versi Stirling-PDF yang jauh
  lebih baru/lama dari kedua versi di atas berpotensi mengubah nama parameter.
- **PENTING - aplikasi desktop mode "lokal saja" TIDAK menyertakan OCR & konversi
  dokumen** (menurut dokumentasi resmi docs.stirlingpdf.com, per 2026-09-24): backend
  bawaan aplikasi desktop (Settings > Connection > Local-only, mode default) hanya
  menjalankan tool dasar (gabung/pisah/putar/kompres/watermark/kunci). Untuk `ocr` dan
  kemungkinan `foto-ke-pdf`, aplikasi akan minta login Stirling Cloud atau tersambung
  ke server self-hosted - **bukan berarti fitur itu berbayar**, tapi engine OCR-nya
  (Tesseract) memang tidak dibundel di mode itu. Solusi tetap gratis & 100% lokal:
  pasang Stirling-PDF lewat **Docker** (lihat `references/pasang-stirling.md` Jalur B)
  seperti yang dipakai untuk menguji skill ini, lalu (opsional) sambungkan aplikasi
  desktop ke situ lewat Settings > Connection > Self-hosted server. Script sudah
  mendeteksi error 404 ini dan menjelaskannya ke pengguna.
