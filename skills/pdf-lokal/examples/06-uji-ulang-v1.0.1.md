# Uji Ulang v1.0.1 (2026-09-24) — Penguji Independen ke-2

**Penguji:** agent penguji independen (Claude Code, Sonnet 5), bukan pembuat/perbaikan
skill. Sesi terpisah dari sesi yang mengerjakan revisi v1.0.1. Hanya membaca
`skills/pdf-lokal/` + `docs/panduan-stirling-pdf.md`. Semua perintah dijalankan dari
`scratchpad/uji2-pdf/` (bukan root repo, bukan `.claude/skills/`).

**Lingkungan:** Linux, Python 3.11 (Pillow 12.3.0 + reportlab 5.0.1 dipasang di
scratchpad untuk membuat data uji — **tidak** menyentuh dependensi skill, skill tetap
hanya memakai `urllib` bawaan). `poppler-utils` (pdfinfo/pdftotext/pdftoppm), `qpdf`,
`sha256sum` dipasang untuk verifikasi independen.

**Stirling-PDF asli yang diuji (via Docker, image resmi
`ghcr.io/stirling-tools/stirling-pdf`):**
- `:3.0.0` — dipakai untuk seluruh repro T1 & skenario regresi utama.
- `:2.14.3` — dipakai untuk verifikasi silang klaim "diuji di kedua versi" (cek + gabung).

Kedua image sudah ada di cache lokal Docker (pull instan, < 2 detik) — tidak menghambat
batas waktu ±20 menit. Kedua container dihentikan & volume-nya dihapus di akhir sesi
(`docker rm -f`, `docker volume rm`) — tidak ada container/volume Docker tersisa.

---

## 1. Repro T1 — persis perintah panduan §3.2

```bash
docker run -d --name stirling-pdf-t1 --restart unless-stopped \
  -p 8080:8080 \
  -e SECURITY_ENABLELOGIN=false \
  -v stirling-data-t1:/configs \
  ghcr.io/stirling-tools/stirling-pdf:3.0.0
```
Container sehat (`healthy`) dalam ±30 detik. `curl http://localhost:8080/api/v1/info/status`
→ `{"version":"3.0.0","status":"UP"}`.

```
$ python3 scripts/pdf.py cek
Stirling-PDF HIDUP di http://localhost:8080
  Versi  : 3.0.0
  Status : UP
Menguji 1 operasi PDF nyata (bukan cuma cek status) untuk pastikan tidak diblokir login...
Operasi PDF diizinkan. Siap dipakai. Coba: python3 pdf.py gabung file1.pdf file2.pdf
EXIT: 0
```
**T1 (perintah docker + `cek` menguji operasi nyata): TERBUKTI BENAR.** Persis perintah
panduan bagian 3.2 (dengan `SECURITY_ENABLELOGIN=false`, image dipin `:3.0.0`) berhasil
mengizinkan operasi PDF sungguhan sejak awal, dan `cek` benar-benar mencoba 1 operasi
nyata (rotate 0° pada PDF minimal buatan sendiri) sebelum menyimpulkan "siap dipakai" —
bukan cuma menanyakan status seperti versi lama yang menyebabkan T1 di uji v1.0.0.

## 2. Repro negatif — tanpa flag login, `cek` HARUS gagal jelas (bukan positif palsu)

```bash
docker run -d --name stirling-pdf-nologinflag -p 8081:8080 \
  -v stirling-data-nologinflag:/configs \
  ghcr.io/stirling-tools/stirling-pdf:3.0.0   # SENGAJA tanpa -e SECURITY_ENABLELOGIN=false
```
```
$ STIRLING_URL=http://localhost:8081 python3 scripts/pdf.py cek
Stirling-PDF HIDUP di http://localhost:8081
  Versi  : 3.0.0
  Status : UP
Menguji 1 operasi PDF nyata (bukan cuma cek status) untuk pastikan tidak diblokir login...
GAGAL: Stirling-PDF HIDUP (versi & status di atas benar), TAPI menolak operasi PDF
sungguhan - semua perintah lain (gabung, kompres, dst.) akan gagal sampai ini
diperbaiki. Detail & cara perbaiki:
Stirling-PDF menolak permintaan ini (401 - butuh login/API key). ...
EXIT: 1
```
**Tidak ada positif palsu.** `cek` sekarang berhenti di sini dengan pesan jelas +
2 cara perbaikan, alih-alih mencetak "Siap dipakai" seperti T1 lama.

**Konsistensi pesan 401/403:** menjalankan `gabung` langsung ke server yang sama (login
aktif) menghasilkan **pesan identik persis** (sama-sama lewat `panggil_stirling()`):
```
GAGAL: Stirling-PDF menolak permintaan ini (401 - butuh login/API key). Server ini
menyalakan keamanan/login, jadi SEMUA operasi PDF ditolak sampai diperbaiki salah satu
dari 2 cara ini: 1) ... '-e SECURITY_ENABLELOGIN=false' ... 2) ... STIRLING_API_KEY ...
```
Klaim "401/403 → satu pesan konsisten di semua perintah (env var + API key via ENV)"
**TERBUKTI BENAR.**

## 3. Verifikasi silang versi (klaim "diuji ke 2.14.3 & 3.0.0")

`docker run ... ghcr.io/stirling-tools/stirling-pdf:2.14.3` (dengan
`SECURITY_ENABLELOGIN=false`) → `cek` sukses (`Versi: 2.14.3`, "Operasi PDF diizinkan"),
`gabung` 2 file PDF minimal → berhasil. **Klaim pembuat "diuji ke Stirling 2.14.3 & 3.0.0
asli" TERBUKTI BENAR** untuk kedua versi yang disebut.

## 4. Regresi skenario 01–03 (server: `:3.0.0`, login mati, sesuai panduan)

Data uji baru dibuat ulang (bukan dipakai ulang dari uji v1.0.0), foto nota HD ~5.4 MB/foto
(realistis, dibuat dengan noise piksel + teks agar tidak gampang dikompres kosong).

| Skenario | Hasil | Verifikasi independen |
|---|---|---|
| **01** — 3 foto nota → gabung → kompres | `foto-ke-pdf`: 3 hal., 6.19 MB. `kompres --target 2MB`: **6339 KB → 2044 KB** (klaim script) | `pdfinfo`: tetap 3 halaman. `os.path.getsize` independen: **2 093 000 byte (≈2.0 MB, di bawah 2 MiB target)** — cocok dengan klaim script. `sha256sum` 3 foto asli sebelum/sesudah: **identik**, tidak pernah tertimpa. |
| **02** — 8 resi (thermal 10×15 cm asli) → `rapikan-resi --per-lembar 4` | 2 halaman, urutan resi 1–4 di hal.1, 5–8 di hal.2 | `pdfinfo`: 2 halaman ✅. `pdftotext`: isi & urutan tiap resi persis benar ✅. `sha256sum` 8 resi asli: **identik**, tidak tertimpa ✅. **Lihat cacat baru N1 di bawah soal ukuran kertas hasil.** |
| **03** — kontrak 10 hal. → `pisah-rentang 3-5` → `watermark` → `kunci` | Hal. 3/4/5 terambil tepat, watermark "SALINAN" tampak jelas di render (`pdftoppm`, diverifikasi visual), file terkunci | `pdftotext`: isi pasal 3/4/5 identik dengan asli ✅. `qpdf --check`/`--decrypt`: sandi salah **ditolak**, sandi benar **berhasil buka & isi utuh** ✅. `sha256sum` kontrak asli: **identik** ✅. |

**Tidak ada regresi** pada mesin pengolahan PDF inti dibanding uji v1.0.0 — semua angka,
halaman, enkripsi, dan keutuhan file asli tetap 100% benar di verifikasi independen.

## 5. Input buruk (singkat)

| Kasus | Hasil |
|---|---|
| File `.txt` diberi nama untuk `gabung` (bukan PDF asli) | `GAGAL` jelas dari Stirling ("JPDFium merge failed" diterjemahkan ke pesan awam), exit 1, tidak crash |
| PDF 0 byte | `GAGAL`: "PDF file appears to be corrupted..." (diteruskan apa adanya), exit 1 |
| PDF terkunci diproses tanpa `buka-kunci` dulu | `GAGAL` dengan saran pakai `buka-kunci --sandi ...` dulu, exit 1 |
| Stirling-PDF mati (`--url http://localhost:9999`) | `GAGAL`: "Tidak bisa menghubungi ... Connection refused", arahan ke panduan, exit 1 |
| URL publik (`http://example.com:8080`) tanpa `STIRLING_ALLOW_REMOTE=1` | `GAGAL`: ditolak eksplisit, jelaskan cara mengaktifkan sadar, exit 1 |
| File tidak ada | `GAGAL`: "File tidak ditemukan: ...", exit 1 |

Semua 6 sub-kasus: pesan jelas bahasa awam, tidak pernah crash mentah/traceback, exit
code konsisten (1).

## 6. Cacat baru ditemukan saat uji ulang

**N1 (Sedang) — `SKILL.md` baris ±113-116, klaim baru R1 tentang ukuran kertas
`rapikan-resi` TIDAK akurat.** Teks revisi menulis: *"kalau sumbernya seperti itu
[resi thermal 10×15/10×20 cm], hasil `rapikan-resi` kemungkinan besar tetap berukuran
kecil per halaman (bukan otomatis membesar jadi A4)."* Diuji langsung dengan resi PDF
berukuran asli **10×15 cm (283×425 pt)** lewat `rapikan-resi --per-lembar 4` (dan
diulang dengan `--per-lembar 2`) ke Stirling-PDF 3.0.0 asli: hasilnya **justru selalu
A4 (595×842 pt)** di kedua uji, bukan tetap kecil. Jadi klaim spesifik yang baru
ditambahkan justru **berlawanan dengan perilaku nyata** Stirling-PDF (endpoint
`multi-page-layout`). Dampak: pembeli awam yang membaca kalimat ini bisa mengira
hasilnya akan tetap seukuran resi asli dan kaget saat hasilnya membesar jadi A4 (rasio
resi jadi kecil di tengah lembar A4). **Tidak fatal** karena kalimat setelahnya tetap
menyarankan cek Print Preview dulu, tapi kalimat spesifik itu perlu diperbaiki jadi
netral (mis. hapus dugaan arah spesifik, cukup "ukuran kertas hasil bisa berbeda dari
ukuran resi asli - selalu cek Print Preview dulu") atau uji ulang di berbagai versi
Stirling untuk memastikan arah klaim mana yang benar sebelum dipublikasikan sebagai
fakta.

Tidak ditemukan regresi lain maupun cacat baru pada bagian T1 (docker run/keamanan),
S1 (estimasi waktu), R2 (fallback ekstrak-nota-faktur), atau R3 (dokumen sensitif) —
lihat bagian 7.

## 7. Status klaim revisi v1.0.1

| Klaim | Status |
|---|---|
| T1: `docker run` §3.2 pakai `SECURITY_ENABLELOGIN=false` + image dipin `:3.0.0` | **Benar, diverifikasi** |
| T1: §5 dikoreksi (tidak lagi klaim "tanpa login = aman" secara keliru) | **Benar** — dibaca ulang, sekarang menjelaskan login aktif default & cara mematikannya |
| T1: `pdf.py cek` menjalankan 1 operasi nyata sebelum bilang siap | **Benar, diverifikasi** (rotate 0° pada PDF minimal, gagal jelas bila ditolak) |
| T1: 401/403 → satu pesan konsisten di semua perintah | **Benar, diverifikasi** (pesan `cek` & `gabung` identik) |
| T1: diuji ke Stirling 2.14.3 & 3.0.0 asli | **Benar, diverifikasi ulang independen** (kedua versi: cek + operasi nyata sukses) |
| S1: estimasi Docker Windows ±20-40 menit + WSL2/restart/UAC/antivirus + jasa setup | **Isi memadai** (dibaca, mencakup semua poin diminta); waktu spesifik Windows tidak bisa diuji langsung di lingkungan Linux ini — dinilai dari kelengkapan & kewajaran isi, bukan diukur ulang |
| R1: contoh ukuran resi konkret (10×15/10×20 cm) | **Contoh ada**, TAPI klaim arah spesifik tentang hasil ("tetap kecil, bukan A4") **terbukti salah** — lihat **N1** |
| R2: fallback bila `ekstrak-nota-faktur` tak terpasang | **Benar, sudah ada** di SKILL.md |
| R3: dokumen sensitif dilarang diunggah ke situs online | **Benar, sudah ada**, tegas & tanpa pengecualian |

## 8. Uji pendukung (dari root repo `<folder repo>`)
- `python3 skills/pdf-lokal/tests/uji_regresi.py` → **15/15 lulus** (naik dari 12/12 di
  v1.0.0 — 3 skenario baru soal 401 ditambahkan pembuat).
- `python3 scripts/validate.py` → **57 skill valid, 57 baris katalog sesuai.**
- `bash scripts/uji_openclaw.sh` → OpenClaw **2026.9.6**: `eligible 57/57`,
  `modelVisible 57/57`, `commandVisible 57/57`.

## 9. Kesimpulan
T1 (cacat Tinggi utama penyebab skor 5/10 di v1.0.0) **selesai diperbaiki dan
diverifikasi tuntas** dengan Stirling-PDF asli (bukan tiruan) di dua versi. S1, R2, R3
juga selesai. Satu cacat baru (**N1**, Sedang) ditemukan pada klaim spesifik yang baru
ditambahkan di R1 — perlu revisi kecil sebelum rilis, tapi tidak mengulang pola T1 (tidak
fatal, tidak bertentangan dengan prinsip privasi/keamanan inti, dan sudah ada jaring
pengaman "cek Print Preview dulu" di kalimat yang sama). Lihat skor akhir & alasan di
`HASIL-UJI.md` bagian "Uji ulang v1.0.1".
