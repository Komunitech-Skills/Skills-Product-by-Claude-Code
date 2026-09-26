# Kontrak Karyawan Kontrak Aman, Tanpa Salah Pasal

**Buat kontrak PKWT siap cetak, cek kontrak lama dari pasal berbahaya, dan hitung kompensasi habis kontrak sampai ke rupiahnya.**

## Manfaat
- ✅ **Draf kontrak PKWT 12 pasal siap cetak**: jabatan & alasan kontrak, jangka waktu, jam kerja & lembur, upah + terbilang, BPJS, THR, cuti, kompensasi, pengakhiran, dan tanda tangan bermeterai. Bagian yang belum kamu isi ditandai `[isi: ...]`, tidak diisi dengan data karangan.
- ✅ **Cek kontrak lama dalam sekali tempel**: menemukan pasal yang sering bikin usaha kalah di Disnaker, misalnya masa percobaan di kontrak, pekerjaan tetap dikontrak, lebih dari 5 tahun, gaji di bawah UMK, tanpa BPJS, atau denda berlebihan. Setiap temuan diberi tingkat risiko (🔴/🟠/🟢) dan kalimat pengganti yang siap tempel.
- ✅ **Kompensasi & ganti rugi dihitung script**, bukan dikira-kira: kompensasi per periode kontrak, cek batas 5 tahun termasuk perpanjangan, dan ganti rugi sisa kontrak kalau diputus lebih cepat.
- ✅ **Paham input sehari-hari**: tanggal "1 Januari 2026" atau "01/01/2026", gaji "Rp5.000.000" atau "5jt". Kalau ada yang salah (tanggal terbalik, angka negatif), kamu diberi tahu dengan bahasa jelas.
- ✅ **Paham usaha mikro/kecil**: untuk warung, kedai, dan usaha kecil, besaran kompensasi boleh sesuai kesepakatan (PP 35/2021 Pasal 16 ayat (6)); skill menampilkan hitungan rumus umum sebagai acuan dan menyiapkan klausul kesepakatannya.
- ✅ **Jujur soal aturan yang sedang berubah**: dasar hukum dan tanggal cek selalu disebut, termasuk status Putusan MK 168/2023 dan UU Ketenagakerjaan baru yang sedang dibahas.

## Cocok untuk siapa
- Pemilik UMKM (kafe, toko, bengkel, kontraktor, konveksi) yang merekrut karyawan kontrak, tenaga proyek, atau pekerja musiman
- Staf HR/admin di usaha yang belum punya konsultan hukum tetap
- Pemilik usaha yang ingin memeriksa kontrak lama sebelum diperpanjang
- Siapa pun yang bingung "kontrak habis, harus bayar berapa?"

## Contoh sebelum & sesudah
**Sebelum:** Pakai template kontrak dari internet: ada "masa percobaan 3 bulan", tidak ada pasal kompensasi, dan tertulis "denda 3× gaji bila resign". Saat karyawan melapor ke Disnaker, usaha harus membayar kompensasi plus ganti rugi, dan kontraknya bisa dianggap karyawan tetap.

**Sesudah (cukup ketik):** "Bikinin kontrak buat Dimas, barista kedai kopi saya di Bandung, 1 tahun mulai 1 Oktober 2026, gaji 3,8 juta + tunjangan transport tetap 300 ribu, 3 bulan pertama masa percobaan."
→ Kamu diberi tahu bahwa masa percobaan di kontrak PKWT batal demi hukum, lalu ditanya alasan posisinya dikontrak. Hasilnya: draf 12 pasal dengan upah **Rp4.100.000 (empat juta seratus ribu rupiah)**, perkiraan kompensasi akhir **Rp4.100.000**, batas maksimal kontrak sampai 30 September 2031, daftar isian yang masih kosong (termasuk UMK Bandung yang perlu kamu cek), checklist sebelum tanda tangan, dan disclaimer.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu:
- "Buatkan kontrak kerja 6 bulan untuk tukang proyek renovasi ruko"
- "Tolong cek kontrak karyawan ini, ada yang melanggar nggak?" (tempel isi kontrak)
- "Kontrak Andi mulai 1 Februari 2025, diperpanjang sampai Juli 2026, saya putus 20 Mei. Harus bayar berapa?"

Script hitung butuh Python 3 (biasanya sudah ada di Mac/Linux; di Windows ketik `python` atau `py`). Tanpa Python pun skill tetap bisa dipakai, karena rumusnya ditulis lengkap dan agent akan memberi label "dihitung manual".

## Instalasi singkat
Salin folder `kontrak-kerja-pkwt` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah kontrak dari skill ini pasti sah dan aman?**
Draf disusun mengikuti UU 13/2003 sebagaimana diubah UU 6/2023, PP 35/2021, dan Putusan MK 168/PUU-XXI/2023 (dicek 25 September 2026). Hasilnya tetap draf, bukan nasihat hukum. Keabsahan juga bergantung pada fakta di lapangan, misalnya apakah pekerjaannya memang bersifat sementara. Untuk kasus penting, mintalah Disnaker atau konsultan hukum ketenagakerjaan meninjaunya.

**Katanya ada UU Ketenagakerjaan baru. Skill ini masih berlaku?**
Mahkamah Konstitusi memerintahkan UU Ketenagakerjaan baru paling lambat sekitar akhir Oktober 2026. Per 25 September 2026, RUU Pelindungan Ketenagakerjaan belum disahkan, jadi skill memakai aturan yang berlaku saat ini dan selalu menyebut status ini. Setelah UU baru terbit, skill akan ditinjau ulang dan pembeli akan mendapat pembaruan.

**Bisa untuk karyawan tetap atau menghitung pesangon PHK?**
Tidak. Skill ini khusus kontrak kerja waktu tertentu (PKWT), termasuk harian lepas. Untuk karyawan tetap, PHK, dan pesangon, skill akan menjelaskan bedanya lalu menyarankan kamu berkonsultasi ke Disnaker atau konsultan hukum. Untuk THR, slip gaji, dan surat peringatan, gunakan skill Komunitech `hitung-thr`, `slip-gaji-bpjs`, dan `surat-peringatan-karyawan`.

## Riwayat versi
- **1.0.3 (26 September 2026)** — disesuaikan dengan naskah resmi PP 35/2021 (semua angka rupiah metode bawaan tidak berubah):
  - **Usaha mikro & kecil:** sesuai PP 35/2021 Pasal 16 ayat (6), besaran uang kompensasi bagi pekerja di usaha mikro/kecil ditentukan **kesepakatan** pengusaha dan pekerja. Skill kini menanyakan apakah usahamu usaha mikro/kecil; script punya opsi `--usaha-mikro-kecil` yang menampilkan rumus umum sebagai **acuan** (bukan kewajiban); template punya klausul kompensasi versi kesepakatan; checklist periksa tidak lagi menandai kompensasi kesepakatan UMK sebagai pelanggaran.
  - Rujukan pasal dirapikan: upah lembur sejam 1/173 = PP 35/2021 Pasal 32 ayat (2); aturan "rata-rata 12 bulan terakhir" adalah Pasal 33 ayat (2) dan hanya untuk upah lembur, bukan kompensasi PKWT.
- **1.0.2 (25 September 2026)** — perbaikan kecil dari uji ulang independen (semua angka rupiah metode bawaan tidak berubah):
  - Keterangan sisa kontrak kini menampilkan pecahan yang benar-benar dipakai, mis. "(3 − 1,5357) = 1,4643 bulan"; jumlah hari kalender hanya sebagai informasi (sebelumnya tertulis "1 bulan 16 hari" yang tidak cocok dengan 1,4643).
  - Bila berhenti tepat di hari terakhir periode berjalan, tidak lagi tercetak rentang tanggal terbalik; ditulis "tidak ada sisa di periode berjalan" (Rp0).
  - Opsi `--metode bulan-penuh` dihapus karena membuat masa dijalani + sisa kontrak tidak sama dengan panjang kontrak; kini hanya satu cara hitung yang konsisten.
  - Upah tertulis "4,5" kini disarankan Rp4.500.000 (4,5 juta), bukan Rp5.000.
  - Checklist THR diperjelas: THR dikecualikan = risiko tinggi 🔴; THR tidak disebut = risiko sedang 🟠.
- **1.0.1 (25 September 2026)** — revisi temuan uji independen:
  - Ganti rugi pengakhiran dini (Pasal 62): sisa kontrak kini = panjang periode − masa yang sudah dijalani, sehingga keduanya selalu berjumlah tepat panjang kontrak (sebelumnya bisa selisih hingga ±2,8 hari upah). Contoh skenario utama (Rp4.150.000/orang; Rp5.000.000 + Rp1.250.000 + ganti rugi Rp15.000.000) tidak berubah.
  - Checklist jam kerja diperbaiki: 6 hari kerja = 7 jam/hari dan 40 jam/minggu, 5 hari kerja = 8 jam/hari dan 40 jam/minggu (PP 35/2021 Pasal 21).
  - Peringatan baru bila beberapa kontrak pendek (< 1 bulan) berurutan tanpa jeda sehingga kompensasi Rp0, lengkap dengan dua kemungkinan tafsir.
  - Menerima penulisan "Rp 5.000.000,-" dan "Rp5.000.000,00", periode tanpa spasi "1/1/2026-31/12/2026"; peringatan bila upah terlalu kecil (kemungkinan salah ketik).
  - Panduan untuk beberapa pekerja sekaligus dan untuk tanggal mulai yang belum diketahui.
- **1.0.0 (25 September 2026)** — rilis draf pertama.
