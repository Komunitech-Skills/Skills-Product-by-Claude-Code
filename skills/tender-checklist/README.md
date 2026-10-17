# Cek Syarat Tender Pemerintah Sebelum Dokumen Dikirim

**Asisten persiapan tender pemerintah untuk UMKM: bantu cek layak ikut, kelengkapan dokumen, jadwal mundur supaya tidak telat, dan hitungan harga lewat skrip.**

Diuji AI penguji independen di OpenClaw: 7,25 → 9,0 dari 10 (hitungan dasar benar di kedua sisi; pembedanya jadwal hari kerja, jaminan pelaksanaan, pengingat PPh 22, dan skenario PPN yang tidak keliru).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tahu layak ikut atau tidak dalam beberapa menit** — cek kualifikasi usaha kecil, KBLI (kode bidang usaha) di NIB (nomor induk berusaha), NPWP/PKP (Pengusaha Kena Pajak), SBU/SKK (sertifikat usaha dan keahlian konstruksi), pengalaman, dan sisa kemampuan paket.
- ✅ **Checklist dokumen siap centang** per metode: tender, pengadaan langsung, e-katalog/e-purchasing (belanja lewat katalog pemerintah).
- ✅ **Jadwal mundur otomatis** dari batas unggah (H-7, H-5, H-3, H-2, H-1), menghitung hari kerja & libur yang Anda sebut.
- ✅ **Harga penawaran diperiksa script**: volume × harga, PPN 12% × 11/12 (bila PKP), total, terbilang, persen terhadap HPS (harga perkiraan sendiri dari panitia), dan peringatan otomatis bila melebihi HPS atau di bawah 80% HPS.
- ✅ **20 kesalahan yang paling sering menggugurkan** — ditunjukkan yang relevan dengan paket Anda.

## Cocok untuk siapa
- Pemilik CV/PT kecil, koperasi, atau usaha perorangan yang ingin mulai ikut pengadaan pemerintah di LPSE/SPSE (situs lelang online pemerintah).
- Admin tender yang ingin memeriksa ulang dokumen & harga sebelum unggah.
- Penyedia di e-katalog/toko daring pemerintah yang ingin rapi soal harga & dokumen.

## Contoh sebelum & sesudah
**Sebelum:** total di Excel salah karena satu baris terlewat, terbilang tidak sama dengan angka, dan unggah jam 13.55 untuk batas 14.00 — gagal karena server padat. Penawaran gugur.

**Sesudah (cukup ketik):** "Batas unggah 15 Oktober jam 14.00, HPS 45 juta, ini rincian harga saya: ..."

Cuplikan hasil (dipotong; contoh dengan data fiktif, keluaran nyata skrip dari `examples/uji-pembuat-01-atk-usaha-kecil.md`):
```
Subtotal (DPP)                     : Rp39.750.000
PPN (tidak dipungut: bukan PKP)    : Rp0
TOTAL PENAWARAN                    : Rp39.750.000
Terbilang: Tiga Puluh Sembilan Juta Tujuh Ratus Lima Puluh Ribu Rupiah

HPS                                : Rp45.000.000
Penawaran terhadap HPS             : 88,33%
Batas 80% HPS                      : Rp36.000.000
…
[ ] H-7          Selasa, 6 Oktober 2026
      Kumpulkan dokumen: NIB & KBLI (OSS), NPWP, status PKP, akta & pengesahan, …
…
[ ] H-1          Rabu, 14 Oktober 2026
      UNGGAH penawaran lengkap di SPSE (jangan tunggu hari terakhir). …
```
Hasil lengkapnya juga memuat rincian harga per baris, jadwal H-5 sampai H, checklist dokumen, dan daftar kesalahan yang paling sering menggugurkan penawaran.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Saya mau ikut tender pengadaan seragam di LPSE provinsi, apa saja yang harus disiapkan?"
- "Cek rincian penawaran ini, HPS Rp250 juta, saya PKP." (tempel tabel)
- "Bikinin jadwal persiapan, batas unggah 20 November jam 15.00, tanggal 25 libur."
- "CV saya KBLI 41012, SBU kecil, lagi pegang 3 proyek. Masih bisa ikut tender konstruksi?"

**Catatan akses portal resmi (dicek 15 Oktober 2026):**
- Akses tender resmi lewat LPSE masing-masing di ekosistem INAPROC (**spse.inaproc.id**). SPSE versi 4.5 **meminta kode TOTP** (verifikasi dua langkah/2FA dari aplikasi autentikator di HP) saat login — siapkan HP-nya dan coba login jauh sebelum hari unggah.
- Data kualifikasi usaha dan riwayat kinerja penyedia dikelola di **SIKaP**, yang sejak **15 Desember 2025** diakses lewat **sikap.inaproc.id** (alamat lama sikap.lkpp.go.id kini berisi pengumuman pindah alamat).
- Skill ini tidak masuk ke portal mana pun; ia hanya mengingatkan langkah yang perlu Anda cek sendiri.

## Instalasi singkat
Salin folder `tender-checklist` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Script hanya butuh Python bawaan; tanpa Python pun skill tetap bekerja memakai rumus yang tertulis.

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, 1 Okt 2026 (v1.0.7; angka dari `examples/00-openclaw-sebelum-sesudah.md`), skor 1–10: tanpa skill **7,25** → dengan skill **9,0** (selisih +1,75, lulus acuan kami). Contoh tender meubel (HPS Rp248,5 juta): dengan skill total penawaran **Rp234.487.500** (PPN efektif 11%), jaminan pelaksanaan dan jadwal hari kerja dihitung skrip; tanpa skill memberi dua skenario PPN (11% dan 12%), padahal skenario 12% keliru untuk barang non-mewah.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-01; muat CLI) dan Claude Code (simulasi agent). Sudah diuji di bot Telegram asli: 17 Oktober 2026 dengan versi 1.0.9, lulus acuan kami (uji 16 Oktober 2026 dengan versi 1.0.8 belum lulus; lihat bagian berikut). Codex dan Cursor belum uji platform asli. PERLU REVIEW: klarifikasi penawaran di bawah 80% HPS, pengecualian pengalaman usaha kecil baru, dan sisa kemampuan paket (dari Peraturan LKPP 12/2021, sumber sekunder) — cocokkan dengan dokumen pemilihan paket Anda.

## Bukti uji di bot Telegram

Uji terbaru: 17 Oktober 2026, versi 1.0.9, di bot OpenClaw asli (grup uji Komunitech), dengan pesan yang sama untuk kedua sisi (tanpa skill dan dengan skill): pemilik CV usaha kecil yang sudah PKP ingin ikut tender Pengadaan ATK Dinas Pendidikan kabupaten (HPS Rp185 juta, pagu Rp190 juta, pascakualifikasi), lengkap dengan jadwal dan rincian harga. Skor 1–10 dari penilai independen: tanpa skill **6** → dengan skill **8,5** (selisih +2,5), **lulus acuan kami** (dengan skill minimal 8 dan selisih minimal 1,5).

Kedua sisi menyebut batas unggah sudah lewat; bedanya, dengan skill Anda tetap mendapat total penawaran lengkap dengan PPN (Rp44.142.480, atau 23,86% dari HPS, jauh di bawah ambang 80% yang memicu klarifikasi kewajaran harga), daftar dokumen yang bisa dicentang, daftar hal yang bisa menggugurkan penawaran, dasar aturan dan penafian, serta pengingat bahwa bendahara memungut PPN dan memotong PPh 22 saat membayar. Tanpa skill, PPN tidak dihitung dan Anda malah disuruh mengecek tarifnya sendiri; total, persen HPS, jaminan, dan pengingat PPh 22 tidak ada. Semua angka dengan skill sudah dihitung ulang terpisah dan benar.

Catatan jujur: masih ada singkatan yang tidak dijelaskan (LDK, SPSE, SIKaP, TOTP, DPP); kalimat asumsi "HPS belum termasuk PPN" di akhir tidak sejalan dengan perbandingan total termasuk PPN terhadap HPS (perbandingan yang dipakai sudah benar); dan harga tinta Rp1,25 juta per botol serta paper clip 1,5 lusin tidak dipertanyakan, padahal versi tanpa skill justru menangkapnya. Ini satu pesan uji per sisi, bukan uji berulang. Uji sebelumnya: 16 Oktober 2026 dengan versi 1.0.8 dan kasus yang sama, tanpa skill **5** → dengan skill **7,5**, belum lulus acuan kami karena daftar dokumen tidak muncul serta dasar aturan dan pengingat PPh 22 hilang; itu diperbaiki di versi 1.0.9.

**Perbaikan versi 1.0.9:** jawaban di chat kini wajib utuh dalam satu balasan dengan urutan tetap — tenggat & jadwal, kelayakan, cek harga (termasuk persen HPS, ambang 80%, jaminan penawaran dan jaminan pelaksanaan yang ditulis terpisah, serta pengingat potongan PPN/PPh 22 oleh bendahara), daftar dokumen (tetap diberikan walau batas unggah sudah lewat), awas gugur, lalu dasar aturan & penafian.

## FAQ
**Apakah dengan skill ini saya otomatis menang tender?**
Skill ini membantu mengurangi risiko gugur karena kesalahan administrasi, dokumen, jadwal, dan hitungan, tetapi tidak bisa menentukan pemenang. Menang-kalah tetap ditentukan evaluasi pokja (kelompok kerja pemilihan, yaitu panitia tender) dan harga pesaing.

**Aturannya kan sering berubah?**
Ringkasan aturan dicek per 25 September 2026 dan pasal Perpres 16/2018 jo. 12/2021 jo. 46/2025 dicocokkan dengan naskah konsolidasi resmi LKPP pada 26 September 2026 (jaminan penawaran kini hanya untuk konstruksi & pekerjaan terintegrasi; jaminan pelaksanaan juga berlaku untuk e-purchasing), lengkap dengan sumbernya. Butir yang belum bisa dicocokkan tetap ditandai PERLU REVIEW. Tanggal berlaku Perpres 46/2025 (diundangkan dan berlaku **30 April 2025**) dicek ulang ke JDIH BPK pada 15 Oktober 2026. Acuan utama tetap dokumen pemilihan di SPSE — skill mengingatkan hal ini.

**Bisa dipakai untuk "mengatur" pemenang atau pinjam bendera?**
Skill ini dirancang menolak permintaan persekongkolan, pinjam bendera, dokumen palsu, atau gratifikasi karena melanggar hukum (UU 5/1999, UU Tipikor) dan dapat berujung daftar hitam. Sebagai gantinya skill menawarkan jalur yang sah.

## Riwayat perubahan

Versi terkini: **1.0.9**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
