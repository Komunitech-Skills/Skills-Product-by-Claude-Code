# HASIL UJI — pdf-lokal v1.0.0

- **Tanggal:** 2026-09-24
- **Penguji:** agent penguji independen (Claude Code, Sonnet 5), bukan pembuat skill. Hanya
  membaca folder `skills/pdf-lokal/` + `docs/panduan-stirling-pdf.md`. Uji `uji-pembuat/`
  milik pembuat **tidak dijadikan dasar** penilaian ini (skor 7,5 dari pembuat sendiri
  tidak dipercaya begitu saja, sesuai instruksi).
- **Lingkungan:** Linux, Python 3.11 (Pillow & reportlab dipasang di scratchpad untuk
  membuat data uji; **tidak** menyentuh dependensi skill itu sendiri — skill tetap hanya
  memakai `urllib` bawaan). Semua perintah dijalankan dari
  `scratchpad/uji-pdf/` (bukan root repo). `poppler-utils` + `qpdf` dipasang untuk
  verifikasi independen (page count, checksum enkripsi) — alat pihak ketiga, bukan bagian
  dari skill.
- **Stirling-PDF yang dijalankan:** **ASLI, via Docker**, image resmi
  `ghcr.io/stirling-tools/stirling-pdf`. Dicoba dua tag: `:latest` (ternyata **v3.0.0**,
  lihat T1) dan `:2.14.3` (versi yang diklaim diuji pembuat di
  `references/sumber-api-stirling.md`). Kedua tag ditarik hari ini (2026-09-24) dari
  registry resmi (bukan server tiruan) — tidak ada batasan/fallback yang diperlukan.
- **Uji regresi bawaan:** `python3 skills/pdf-lokal/tests/uji_regresi.py` (dari root repo,
  `STIRLING_URL` mengarah ke server Docker yang sedang jalan dengan
  `SECURITY_ENABLELOGIN=false`) → **12/12 lulus**.
- **`scripts/validate.py`** (dari root repo) → **57 skill valid, 57 baris katalog sesuai.**
- **`bash scripts/uji_openclaw.sh`** (dari root repo) → OpenClaw **2026.9.6**:
  `eligible 57/57`, `modelVisible 57/57`, `commandVisible 57/57`, termasuk `pdf-lokal`.
- **Platform teruji (versi jujur):** `claude-code (simulasi agent)` untuk isi
  perintah/skenario; `openclaw 2026.9.6 (uji muat CLI otomatis)` untuk keterlihatan skill.
  Perilaku agent OpenClaw sungguhan (memicu skill dari kalimat bebas) **tidak** diuji
  penguji ini.

## Audit keamanan singkat
`scripts/pdf.py` hanya memakai library standar Python (`urllib`, `json`, `mimetypes`,
`zipfile`, dst.), tidak ada `subprocess`/`eval`/curl-pipe-bash, tidak ada kredensial
tertanam. Validasi alamat server menolak host non-localhost kecuali
`STIRLING_ALLOW_REMOTE=1` diset sadar oleh pengguna — **diverifikasi bekerja** (lihat
skenario 04-E). Tidak ditemukan pola pengiriman data ke luar selain ke `STIRLING_URL`
yang dikonfigurasi pengguna sendiri. SKILL.md dibaca penuh untuk prompt injection
tersembunyi — tidak ditemukan instruksi yang menyuruh mengabaikan pengguna, mengirim
file diam-diam, atau mematikan konfirmasi. **Lulus** audit keamanan skrip.

## Skenario
| No | Berkas | Isi | Hasil |
|---|---|---|---|
| 00 | `00-pembanding-tanpa-skill.md` | A/B skenario normal 1 | Skill **jelas lebih baik** (ukuran terjamin & terverifikasi vs tebakan, privasi lokal vs risiko upload, tanpa dependensi pip) |
| 00 | `00-banding-pesaing.md` | `anthropics/skills` skill `pdf` (Proprietary, dibaca saja) | `pdf-lokal` **unggul** untuk skenario ini: pesaing tidak punya foto→PDF maupun kompres bertarget, perlu banyak dependensi pip+Tesseract sistem, tanpa lokalisasi Indonesia |
| 01 | `01-gabung-kompres-nota.md` | 3 foto nota HD (real ~3.2 MB/foto) → gabung → kompres target 2 MB | **Lulus**; 3.41 MB → 1.32 MB, halaman & path benar, asli tak berubah (sha256) |
| 02 | `02-rapikan-resi.md` | 8 resi Shopee/TikTok fiktif, 4/lembar | **Lulus**; 2 halaman, urutan & isi benar (render diperiksa), asli tak berubah |
| 03 | `03-pisah-kunci-watermark-kontrak.md` | Kontrak 10 hal. fiktif → ambil hal. 3-5 → watermark SALINAN → kunci sandi | **Lulus**; halaman tepat, watermark tampil, enkripsi diverifikasi pakai `qpdf` (alat independen) |
| 04 | `04-input-tidak-lengkap.md` | Bukan PDF, 0 byte, sandi salah, server mati, URL publik, nama file spasi/karakter Indonesia | **Lulus** semua 6 sub-kasus; pesan jelas, tidak crash, exit code benar |
| 05 | `05-di-luar-cakupan.md` | "catat nota ke pembukuan" (redirect), "upload PDF gaji ke situs online" (seharusnya tolak) | Kasus 1 **lulus**; kasus 2 **celah instruksi ringan** (R3) |

## Verifikasi independen (tidak memakai kode/klaim skill)
| Diuji | Alat | Hasil |
|---|---|---|
| Jumlah halaman tiap hasil (gabung, pisah-rentang, rapikan-resi, kompres, OCR) | `pdfinfo` | **0 beda** dari yang diharapkan |
| Ukuran file akhir kompres benar-benar < target | `os.path.getsize` (Python murni, bukan output script) | **Benar** (3495→1352 KB) |
| Isi teks tiap halaman setelah pisah-rentang sesuai nomor asli | `pdftotext` | **0 beda** ("Halaman 3/4/5 dari 10" persis) |
| PDF hasil `kunci` benar-benar terenkripsi & sandi cocok | `qpdf --check`, `qpdf --decrypt` | **Benar** — tanpa sandi ditolak, dengan sandi benar terbuka |
| OCR menghasilkan teks yang bisa dicari | `pdftotext` pada hasil OCR | **Benar** — teks kontrak terbaca dari layer OCR |
| File asli (foto, kontrak, resi) sha256 sebelum vs sesudah semua skenario | `sha256sum` | **Identik di semua kasus** — tidak pernah tertimpa |
| Path lengkap yang dicetak script memang berisi file yang dimaksud | manual | **Benar** di semua kasus, termasuk nama berspasi/karakter Indonesia |

## Temuan cacat
| ID | Keparahan | Lokasi | Temuan & reproduksi |
|---|---|---|---|
| **T1** | **Tinggi** | `docs/panduan-stirling-pdf.md` bagian 3.2 (`docker run ...` tanpa `SECURITY_ENABLELOGIN`) & bagian 5 (klaim "Bawaan (default): tanpa login... Ini AMAN") | Perintah `docker run` **persis seperti tertulis** di bagian 3.2 (image `:latest`, tanpa env var keamanan apa pun) menghasilkan server yang **meminta login/API key untuk SEMUA operasi PDF sungguhan** (`merge-pdfs`, `compress-pdf`, dst → `401 {"error":"Authentication required"}`), bertentangan langsung dengan klaim bagian 5. Ini bukan cuma soal vendor: **catatan internal pembuat sendiri** di `references/sumber-api-stirling.md` baris 46-49 sudah menulis dengan jelas *"Login/keamanan AKTIF secara default di image Docker... Untuk pengujian lokal dipakai `SECURITY_ENABLELOGIN=false`"* — tapi flag itu **tidak pernah dimasukkan** ke perintah `docker run` yang disodorkan ke pembeli di `docs/panduan-stirling-pdf.md`. Yang lebih berbahaya: `python3 scripts/pdf.py cek` (hanya memanggil `/api/v1/info/status`, endpoint yang **tidak** butuh login) tetap mencetak "Stirling-PDF HIDUP ... Siap dipakai" walau server dalam kondisi ini — pembeli awam akan mengira semuanya beres, lalu bingung total begitu menjalankan `gabung`/`kompres`/dll dan selalu dapat error 401. **Reproduksi:** `docker run -d -p 8080:8080 -v v:/configs ghcr.io/stirling-tools/stirling-pdf:latest` (persis perintah di bagian 3.2) → `python3 scripts/pdf.py cek` → sukses palsu → `python3 scripts/pdf.py gabung a.pdf b.pdf` → `GAGAL: ... 401 - butuh login/API key`. Diverifikasi ulang dengan tag `2.14.3` + **tanpa** env var apa pun: `docker logs` menunjukkan `security.enableLogin: true` di `settings.yml` yang dihasilkan — default aktif juga di versi yang diklaim sudah diuji "semua berhasil". Tambahan terkait: tag `:latest` yang direkomendasikan bagian 3.2 & 7 kini menunjuk ke **Stirling-PDF v3.0.0** (bukan v2.14.3 yang diverifikasi di `references/`), versi mayor baru dengan sistem lisensi/akun yang jauh lebih ketat (`enterpriseFeatures`, "Grandfathering LOCKED", dsb) — pin ke tag versi (`:2.14.3`) alih-alih `:latest` akan lebih aman dari perubahan mendadak vendor. **Saran perbaikan:** (1) tambahkan `-e SECURITY_ENABLELOGIN=false` ke perintah `docker run` di bagian 3.2, (2) ubah klaim di bagian 5 jadi jujur ("Stirling-PDF versi Docker terbaru mengaktifkan login secara default; tambahkan flag ini untuk mematikannya untuk pemakaian pribadi"), (3) `pdf.py cek` sebaiknya juga mencoba satu panggilan endpoint yang butuh auth (atau minimal beri catatan "endpoint ini tidak memverifikasi status login") supaya tidak melapor "Siap dipakai" secara menyesatkan, (4) pin versi Docker ke tag spesifik yang sudah diverifikasi, bukan `:latest`. |
| **S1** | **Sedang** | `docs/panduan-stirling-pdf.md` — realita hambatan Jalur B untuk pengguna sangat awam | Estimasi waktu "15-20 menit" untuk Docker cukup optimis: di Windows, aktivasi WSL2 (disebutkan sendiri di panduan) biasanya butuh restart + beberapa menit tambahan, dan pengguna sangat awam bisa terhenti di prompt izin admin/antivirus yang tidak dibahas panduan ini secara spesifik (hanya dibahas untuk instalasi Jalur A/aplikasi desktop). Ini **tidak fatal** karena panduan sudah jujur menyebut kompleksitas relatif ("sedikit lebih teknis") dan menawarkan jasa setup berbayar Komunitech sebagai jalan keluar — tapi realitanya Jalur B (satu-satunya jalan untuk OCR) punya hambatan lebih tinggi dari yang tersirat untuk audiens "mayoritas awam teknologi". |
| R1 | Rendah | `SKILL.md` / `README.md` bagian rapikan-resi | Peringatan "ukuran kertas tidak dijamin A4/A6" sudah ada dan akurat, tapi tanpa contoh konkret risiko (resi thermal 10×15 cm asli vs data uji kami yang kebetulan A4). Saran: tambah satu kalimat contoh nyata biar pembeli awam paham kapan harus curiga. |
| R2 | Rendah | `SKILL.md` bagian "Kapan TIDAK digunakan" | Redirect ke `ekstrak-nota-faktur` untuk baca isi nota sudah tepat, tapi tidak ada fallback bila pembeli belum punya skill itu (agent bisa diam saja). Saran: tambah kalimat fallback singkat. |
| R3 | Rendah | `SKILL.md` bagian "Cara manual tanpa script" poin 4 | Fallback "arahkan ke situs PDF online resmi Stirling-PDF" tidak membedakan dokumen sensitif (gaji, data pribadi) dari dokumen biasa — berpotensi bertentangan dengan klaim privasi utama ("tanpa unggah ke situs luar") bila diikuti apa adanya untuk dokumen sensitif. Saran: tambah pengecualian eksplisit untuk dokumen sensitif. |

Tidak ada cacat yang menyebabkan angka salah, kebocoran data, atau penimpaan file asli —
seluruh mesin pengolahan PDF (setelah server dikonfigurasi benar) bekerja akurat 100%
di semua verifikasi independen.

## Skor kualitas: **5 / 10**
Alasan:
- (+) Setelah server dikonfigurasi benar, **semua fungsi inti bekerja sempurna**:
  path lengkap benar, file asli tak pernah tertimpa (sha256 identik di semua skenario),
  jumlah halaman/isi/enkripsi/ukuran hasil 100% cocok dengan verifikasi independen
  memakai alat pihak ketiga (`pdfinfo`, `pdftotext`, `qpdf`).
- (+) Penanganan input buruk sangat baik: 6/6 sub-kasus gagal dengan pesan jelas,
  tidak pernah crash mentah, tidak pernah "berpura-pura berhasil".
- (+) A/B jelas lebih baik dari agent tanpa skill; unggul dibanding pesaing publik
  terbaik yang ditemukan (`anthropics/skills` `pdf`, dibaca-saja, tidak disalin).
  Lulus 12/12 uji regresi bawaan, `validate.py`, dan uji muat OpenClaw 57/57.
- (+) Temuan jujur pembuat soal OCR (bahasa `ind` tak terpasang default, mode Local-only
  desktop tanpa OCR) **terbukti akurat** saat diverifikasi ulang independen.
- (−) **T1 bersifat fatal untuk pengalaman keluar-kotak**: jalur instalasi utama yang
  *direkomendasikan panduan sendiri* ("ini yang dipakai Komunitech saat menguji skill")
  menghasilkan skill yang gagal total di SETIAP perintah nyata (401 di semua operasi),
  sementara pemeriksaan kesehatan (`cek`) melapor sukses — kontradiksi ini sudah
  diketahui pembuat sendiri di catatan internal (`references/sumber-api-stirling.md`)
  tapi tidak sampai ke panduan yang dibaca pembeli. Ini bertentangan langsung dengan
  prinsip inti CLAUDE.md "instan, tanpa setup rumit, reliable" untuk pembeli awam yang
  butuh OCR — mayoritas pembeli yang mengikuti Jalur B akan mengira mereka sudah
  siap pakai padahal belum.
- (−) S1 & R1-R3 kekurangan minor pada dokumentasi/instruksi, tidak fatal sendiri-sendiri
  tapi menambah beban revisi.

**Keputusan: REVISI DIPERLUKAN (skor < 7), belum boleh naik status.** Perbaikan wajib
sebelum uji ulang: perbaiki T1 di `docs/panduan-stirling-pdf.md` (tambahkan
`-e SECURITY_ENABLELOGIN=false` ke perintah `docker run` bagian 3.2 dan luruskan klaim
bagian 5, pertimbangkan pin versi Docker). S1 & R1-R3 disarankan diperbaiki sekalian
sebelum uji ulang oleh penguji independen berikutnya.

---

## Uji ulang v1.0.1 (2026-09-24)

**Penguji:** agent penguji independen ke-2 (Claude Code, Sonnet 5), sesi terpisah dari
sesi revisi v1.0.1 maupun sesi uji v1.0.0 di atas. Detail lengkap, log perintah, dan
tabel verifikasi ada di `examples/06-uji-ulang-v1.0.1.md`. Ringkasan di bawah.

**Stirling-PDF asli yang diuji:** Docker, image resmi
`ghcr.io/stirling-tools/stirling-pdf`, dua tag **`:3.0.0`** (utama, sesuai panduan) dan
**`:2.14.3`** (verifikasi silang klaim pembuat) — keduanya ditarik ulang & dijalankan
langsung, container/volume dihapus di akhir sesi.

### Status klaim revisi
| Klaim | Status |
|---|---|
| T1 — `docker run` §3.2 benar (`SECURITY_ENABLELOGIN=false`, image dipin `:3.0.0`), §5 dikoreksi | **Terverifikasi benar** |
| T1 — `pdf.py cek` menguji 1 operasi nyata (rotate 0°) sebelum bilang siap | **Terverifikasi benar** (tidak ada lagi positif palsu; diuji juga jalur negatif tanpa flag login → gagal jelas) |
| T1 — 401/403 → pesan konsisten di semua perintah | **Terverifikasi benar** (pesan `cek` & `gabung` identik persis) |
| T1 — diuji ke Stirling 2.14.3 & 3.0.0 asli | **Terverifikasi benar** untuk kedua versi |
| S1 — estimasi Docker Windows ±20-40 menit + WSL2/restart/UAC/antivirus + jasa setup | Isi memadai & lengkap; waktu Windows spesifik tak terukur langsung di lingkungan Linux ini |
| R1 — contoh ukuran resi konkret 10×15/10×20 cm | Contoh ada, tapi klaim arah spesifik hasil ("tetap kecil, bukan A4") **terbukti salah** — lihat **N1** baru |
| R2 — fallback `ekstrak-nota-faktur` tak terpasang | **Sudah ada, benar** |
| R3 — dokumen sensitif dilarang upload online | **Sudah ada, tegas** |

### Regresi (skenario 01-03, data uji baru, server `:3.0.0` login mati)
Tidak ada regresi pada mesin pengolahan PDF inti. Semua diverifikasi ulang independen:
- 01 (gabung 3 foto nota ~5.4 MB/foto → kompres target 2MB): 3 halaman tetap (`pdfinfo`),
  hasil 2 093 000 byte (`os.path.getsize`, di bawah target), sha256 foto asli identik.
- 02 (8 resi thermal 10×15cm → 4/lembar): 2 halaman, urutan & isi benar (`pdftotext`),
  sha256 resi asli identik — **tapi lihat N1**, ukuran kertas hasil ternyata A4, bukan
  tetap kecil seperti diklaim teks baru.
- 03 (kontrak 10 hal. → ambil 3-5 → watermark → kunci): isi 3 halaman identik
  (`pdftotext`), watermark tampak jelas (diverifikasi visual via `pdftoppm`), enkripsi
  benar (`qpdf` — sandi salah ditolak, sandi benar berhasil buka).

### Input buruk
6/6 sub-kasus (bukan PDF, 0 byte, terkunci tanpa buka-kunci, server mati, URL publik
tanpa `STIRLING_ALLOW_REMOTE`, file tidak ada) gagal dengan pesan jelas bahasa awam,
tidak crash, exit code 1 konsisten.

### Cacat baru
| ID | Keparahan | Temuan |
|---|---|---|
| **N1** | **Sedang** | `SKILL.md` klaim baru (bagian R1) "hasil `rapikan-resi` dari resi thermal 10×15/10×20 cm kemungkinan besar tetap berukuran kecil, bukan otomatis membesar jadi A4" **terbukti berlawanan dengan hasil nyata**: diuji dengan resi PDF asli 283×425 pt (10×15 cm) ke Stirling-PDF 3.0.0 asli lewat `rapikan-resi --per-lembar 4` dan `--per-lembar 2`, hasilnya **selalu A4 (595×842 pt)** di kedua kasus. Tidak fatal (kalimat setelahnya tetap menyarankan cek Print Preview dulu), tapi klaim arah spesifik ini perlu diperbaiki atau dihapus sebelum rilis — lihat detail reproduksi di `06-uji-ulang-v1.0.1.md` bagian 6. |

### Uji pendukung (root repo)
- `python3 skills/pdf-lokal/tests/uji_regresi.py` → **15/15 lulus** (naik dari 12/12;
  pembuat menambah 3 skenario soal 401).
- `python3 scripts/validate.py` → **57 skill valid, 57 baris katalog sesuai.**
- `bash scripts/uji_openclaw.sh` → OpenClaw 2026.9.6: `eligible 57/57`,
  `modelVisible 57/57`, `commandVisible 57/57`.

### Skor kualitas: **8 / 10**
Alasan:
- (+) **T1, cacat Tinggi utama yang mengunci skor v1.0.0 di 5/10, selesai diperbaiki
  tuntas dan diverifikasi independen** dengan Stirling-PDF ASLI di **dua versi**
  (2.14.3 & 3.0.0), termasuk jalur negatif (tanpa flag login → `cek` gagal jelas,
  tidak ada positif palsu) dan konsistensi pesan 401/403 di semua perintah.
- (+) S1, R2, R3 juga selesai diperbaiki dan sesuai klaim.
- (+) **Tidak ada regresi** pada mesin pengolahan PDF inti — seluruh angka/halaman/isi/
  enkripsi/keutuhan file asli tetap 100% benar di verifikasi independen memakai alat
  pihak ketiga (`pdfinfo`, `pdftotext`, `qpdf`, `sha256sum`, render visual).
  Penanganan input buruk tetap sangat baik (6/6). Lulus 15/15 uji regresi bawaan,
  `validate.py`, dan uji muat OpenClaw 57/57.
- (−) **N1 (Sedang, baru ditemukan):** satu klaim spesifik yang baru ditambahkan di R1
  (tentang ukuran kertas hasil `rapikan-resi`) ternyata salah arah dibanding perilaku
  nyata Stirling-PDF — bukan cacat fatal (ada jaring pengaman "cek Print Preview"),
  tapi tetap perlu revisi kecil sebelum rilis supaya tidak menyesatkan pembeli awam.
- (−) S1 (estimasi waktu Windows) tidak bisa diukur ulang secara langsung di lingkungan
  Linux penguji ini — dinilai dari kelengkapan isi, bukan pengukuran waktu nyata.

**Keputusan: LULUS uji independen (skor ≥ 7).** Boleh lanjut ke tahap uji platform asli
(Tahap 6.10) setelah **N1 diperbaiki** (revisi kecil, tidak perlu uji ulang penuh oleh
penguji independen — cukup verifikasi teks diperbaiki, kecuali pemilik ingin uji ulang
formal). Tidak ditemukan cacat keamanan, kebocoran data, atau kesalahan angka/uang pada
uji ulang ini.

## Uji ulang v1.0.2 (Akun B) — 2026-09-25

Penguji independen lintas akun terpisah dari pembuat (lihat
`examples/uji-pembuat/UJI-PEMBUAT-v1.0.2.md` untuk catatan pembuat, bukan sumber
keputusan resmi). Uji ringan sesuai sifat perubahan v1.0.2 (murni dokumentasi +
1 baris versi script + 1 tes regresi baru, lihat `git show a536052`) — detail lengkap
di `examples/07-uji-ulang-v1.0.2.md`.

Ringkasan pemeriksaan:
- Klaim baru "sudah diuji Stirling-PDF v3.0.0" di SKILL.md/README **didukung bukti
  nyata** yang sudah tercatat di bagian "Uji ulang v1.0.1" di atas (baris 108-183) dan
  `references/sumber-api-stirling.md` (verifikasi Docker `:3.0.0` & `:2.14.3` sungguhan,
  cross-check `pdfinfo`/`pdftotext`/`qpdf`/`sha256sum`) — bukan klaim kompatibilitas
  yang mengada-ada.
- Klaim privasi README yang direvisi konsisten dengan pengecualian R3 di SKILL.md
  (dokumen biasa boleh diarahkan ke situs resmi Stirling-PDF sebagai jalan terakhir
  dengan peringatan; dokumen sensitif tidak pernah) dan tidak berlebihan.
- Nomor versi konsisten: `scripts/pdf.py` (`VERSI="1.0.2"`) = `catalog.csv` (1.0.2).
  README tidak punya bagian riwayat versi tersendiri.
- `python3 skills/pdf-lokal/tests/uji_regresi.py` → **16/16 skenario lulus**
  (naik dari 15/15; tes baru `versi-konsisten-di-bantuan` ikut lulus).
- `python3 scripts/validate.py --skill pdf-lokal` → lulus, 68 baris katalog sesuai.

Tidak ditemukan temuan baru (tidak ada klaim tak berdasar, tidak ada inkonsistensi
versi, tidak ada regresi fungsional).

**Skor: 9/10** (naik dari 8/10 di v1.0.1). Alasan: dua kelemahan dokumentasi yang
mengganjal skor sebelumnya (klaim versi Stirling-PDF yang diremehkan, klaim privasi
generik yang tidak selaras dengan pengecualian R3) sudah diperbaiki secara akurat dan
berdasar bukti uji nyata yang sudah ada, tanpa menambah klaim baru yang tidak
didukung dan tanpa regresi. Tidak dinaikkan ke 10/10 karena belum ada uji platform
asli (OpenClaw/Codex/Cursor sungguhan oleh manusia) — status katalog tetap `uji`,
kenaikan ke `lulus`/`beta`/`rilis` tetap keputusan pemilik.
