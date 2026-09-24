---
name: pdf-lokal
description: Mengolah file PDF (gabung, pisah, kompres, OCR, foto ke PDF, putar, watermark, kunci/buka sandi, rapikan resi marketplace untuk dicetak) lewat Stirling-PDF yang terpasang di komputer sendiri, tanpa unggah ke situs luar. Pakai saat pengguna minta "gabung PDF", "kompres PDF biar muat WA/email", "PDF ini kebalik", "scan ini susah dicari teksnya (OCR)", "ubah foto nota jadi PDF", "kunci PDF gaji", "rapikan resi Shopee/Tokopedia biar hemat kertas". Keywords: merge PDF, split PDF, compress PDF, OCR PDF, PDF ke Word tidak termasuk, watermark PDF, password PDF, print resi.
---

# pdf-lokal

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
  memahami isinya.
- **Membuat slide/presentasi dari PDF** → pakai skill `presentasi-instan`.
- **Mengedit ISI teks/tata letak PDF secara halus** (bukan sekadar gabung/pisah/putar)
  → Stirling-PDF punya editor teks terbatas, tapi skill ini tidak mengekspos fitur itu;
  arahkan ke aplikasi Stirling-PDF langsung atau Word/Google Docs bila sumber aslinya ada.
- **Tanda tangan digital bersertifikat, SSO, multi-user/tim, audit log** → itu fitur
  **proprietary/berbayar** Stirling-PDF, di luar cakupan skill ini (lihat Batasan).
- Stirling-PDF belum terpasang sama sekali → lihat "Cara manual tanpa script" di bawah,
  atau pakai `docs/panduan-stirling-pdf.md` untuk memasangnya (5-10 menit, gratis).

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
1. Pastikan Stirling-PDF berjalan: jalankan `python3 scripts/pdf.py cek`.
   - Kalau gagal terhubung → beri tahu pengguna Stirling-PDF belum menyala, tawarkan
     "Cara manual tanpa script" di bawah, atau arahkan ke `docs/panduan-stirling-pdf.md`.
2. Pilih perintah yang sesuai (tabel di bawah), jalankan lewat `scripts/pdf.py`.
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
untuk cek Print Preview dulu sebelum cetak massal (ukuran lembar mengikuti PDF resi
aslinya, bukan dipaksa persis A4/A6 - lihat Batasan).

## Cara manual tanpa script (Stirling-PDF belum terpasang / lagi tidak mau jalan)
Skill tetap berguna sebagai panduan meski script tidak bisa dijalankan:
1. Buka aplikasi Stirling-PDF (lihat `docs/panduan-stirling-pdf.md` untuk memasang).
2. Di halaman utama, klik kartu tool yang sesuai (mis. "Merge", "Compress", "OCR / Add
   Text Layer", "Add Password", "N-up / Multi Page Layout" untuk resi).
3. Seret file ke kotak upload, atur opsi di layar, klik proses, lalu unduh hasilnya.
4. Kalau pengguna tidak mau memasang apa pun, arahkan ke situs PDF online resmi milik
   Stirling-PDF sendiri (bukan situs pihak ketiga sembarangan) sebagai alternatif
   terakhir, dengan catatan file akan diunggah ke internet.

## Batasan & penanganan error
- **Stirling-PDF mati/belum terpasang** → script memberi pesan jelas + arahan ke
  `docs/panduan-stirling-pdf.md` dan "Cara manual" di atas. Tidak pernah mencoba
  mengunduh/menjalankan Stirling-PDF secara otomatis.
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
- **Ukuran kertas hasil "rapikan-resi" tidak dijamin persis A4/A6** - Stirling-PDF
  hanya mengatur jumlah kolom/baris per lembar, bukan ukuran kertas eksplisit. Selalu
  sarankan cek Print Preview sebelum cetak banyak.
- **Alamat server non-localhost ditolak** kecuali pengguna secara sadar mengaktifkan
  `STIRLING_ALLOW_REMOTE=1` (mis. server kantor di jaringan lokal) - untuk mencegah
  file tidak sengaja terkirim ke tempat lain.
- **Belum diuji dengan Stirling-PDF versi lain** selain v2.14.3 (Docker) yang dipakai
  saat pembuatan skill ini, dan **belum diuji dengan aplikasi desktop resmi (.msi/.dmg)**
  - hanya lewat image Docker resmi karena keterbatasan lingkungan pembuatan skill. Endpoint
  & parameter berasal dari dokumen Swagger resmi versi itu (lihat `references/`); versi
  Stirling-PDF yang jauh lebih baru/lama berpotensi mengubah nama parameter.
- **PENTING - aplikasi desktop mode "lokal saja" TIDAK menyertakan OCR & konversi
  dokumen** (menurut dokumentasi resmi docs.stirlingpdf.com, per 2026-09-24): backend
  bawaan aplikasi desktop (Settings > Connection > Local-only, mode default) hanya
  menjalankan tool dasar (gabung/pisah/putar/kompres/watermark/kunci). Untuk `ocr` dan
  kemungkinan `foto-ke-pdf`, aplikasi akan minta login Stirling Cloud atau tersambung
  ke server self-hosted - **bukan berarti fitur itu berbayar**, tapi engine OCR-nya
  (Tesseract) memang tidak dibundel di mode itu. Solusi tetap gratis & 100% lokal:
  pasang Stirling-PDF lewat **Docker** (lihat `docs/panduan-stirling-pdf.md` Jalur B)
  seperti yang dipakai untuk menguji skill ini, lalu (opsional) sambungkan aplikasi
  desktop ke situ lewat Settings > Connection > Self-hosted server. Script sudah
  mendeteksi error 404 ini dan menjelaskannya ke pengguna.
