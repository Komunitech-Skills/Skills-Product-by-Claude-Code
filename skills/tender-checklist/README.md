# Ikut Tender Pemerintah Tanpa Gugur Konyol

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

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, 1 Okt 2026 (v1.0.7; angka dari `examples/00-openclaw-sebelum-sesudah.md`), skor 1–10: tanpa skill **7,25** → dengan skill **9,0** (LULUS). Contoh tender meubel (HPS Rp248,5 juta): dengan skill total penawaran **Rp234.487.500** (PPN efektif 11%), jaminan pelaksanaan dan jadwal hari kerja dihitung skrip; tanpa skill memberi dua skenario PPN (11% dan 12%), padahal skenario 12% keliru untuk barang non-mewah.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-01; muat CLI) dan Claude Code (simulasi agent). Belum uji bot Telegram asli khusus skill ini. Codex dan Cursor belum uji platform asli. PERLU REVIEW: klarifikasi penawaran di bawah 80% HPS, pengecualian pengalaman usaha kecil baru, dan sisa kemampuan paket (dari Peraturan LKPP 12/2021, sumber sekunder) — cocokkan dengan dokumen pemilihan paket Anda.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 16 Okt 2026) dengan pesan yang sama: "Saya punya CV (usaha kecil di NIB, KBLI 47612 & 46900, sudah PKP). Mau ikut tender Pengadaan ATK Dinas Pendidikan Kabupaten, HPS Rp185 juta, pagu Rp190 juta, pascakualifikasi. Pengumuman 28/9, penjelasan 2/10, batas unggah 14…". Tanpa skill skor **5** → dengan skill skor **7,5** (selisih +2,5, belum lulus acuan kami: skor dengan skill di bawah 8). Dengan skill, bot langsung memberi vonis "IKUT DENGAN SYARAT" dan memakai batas usaha kecil yang berlaku (Rp15 miliar; tanpa skill masih batas lama Rp2,5 miliar). Bot juga menulis terbilang total Rp44.142.480 dan menyebut persis 23,86% HPS, di bawah ambang 80% yang memicu klarifikasi kewajaran harga, tetapi daftar dokumen yang ditanyakan justru tidak muncul. Salah angka yang ditemukan penilai: TANPA: menyebut batas paket untuk Usaha Kecil/Koperasi "s.d. Rp2,5 M". Itu angka lama Perpres 16/2018 sebelum diubah; batas yang berlaku sejak Perpres 12/2021 (dipertahankan Perpres 46/2025) adalah Rp15 miliar. Kesimpulan "layak" tetap benar, tetapi angka aturannya salah. Sisi DENGAN tidak punya salah angka/fakta. Hasil hitung ulang Python: 150×52.500 = 7.875.000; 24×1.250.000 = 30.000.000; 500×3.750 = 1.875.000; 1,5×12.000 = 18.000; DPP 39.768.000; PPN 12%×11/12×DPP = 4.374.480 (bulat ke bawah); total 44.142.480 = 23,86% HPS (ambang 80% = 148.000.000); terbilang benar. Batas unggah 14 Okt 15.00 sudah lewat; balasan dikirim 17 Okt sekitar 01.00 WIB (Sabtu), jadi kedua sisi benar menyebutnya sudah lewat.. Catatan jujur: Di bot Telegram, daftar dokumen penawaran bisa tidak muncul walau ditanyakan, sehingga pengguna perlu memintanya lagi. Balasan juga belum menyertakan dasar aturan, penafian, dan pengingat bahwa bendahara memotong PPN/PPh 22 saat membayar.

## FAQ
**Apakah dengan skill ini saya otomatis menang tender?**
Skill ini membantu mengurangi risiko gugur karena kesalahan administrasi, dokumen, jadwal, dan hitungan, tetapi tidak bisa menentukan pemenang. Menang-kalah tetap ditentukan evaluasi pokja (kelompok kerja pemilihan, yaitu panitia tender) dan harga pesaing.

**Aturannya kan sering berubah?**
Ringkasan aturan dicek per 25 September 2026 dan pasal Perpres 16/2018 jo. 12/2021 jo. 46/2025 dicocokkan dengan naskah konsolidasi resmi LKPP pada 26 September 2026 (jaminan penawaran kini hanya untuk konstruksi & pekerjaan terintegrasi; jaminan pelaksanaan juga berlaku untuk e-purchasing), lengkap dengan sumbernya. Butir yang belum bisa dicocokkan tetap ditandai PERLU REVIEW. Tanggal berlaku Perpres 46/2025 (diundangkan dan berlaku **30 April 2025**) dicek ulang ke JDIH BPK pada 15 Oktober 2026. Acuan utama tetap dokumen pemilihan di SPSE — skill mengingatkan hal ini.

**Bisa dipakai untuk "mengatur" pemenang atau pinjam bendera?**
Skill ini dirancang menolak permintaan persekongkolan, pinjam bendera, dokumen palsu, atau gratifikasi karena melanggar hukum (UU 5/1999, UU Tipikor) dan dapat berujung daftar hitam. Sebagai gantinya skill menawarkan jalur yang sah.

## Riwayat perubahan

Versi terkini: **1.0.8**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
