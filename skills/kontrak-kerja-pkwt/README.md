# Kontrak Karyawan Kontrak Aman, Tanpa Salah Pasal

**Buat kontrak PKWT siap cetak, cek kontrak lama dari pasal berbahaya, dan hitung kompensasi habis kontrak sampai ke rupiahnya.**

## Manfaat
- ✅ **Draf kontrak PKWT 12 pasal siap cetak**: jabatan & alasan kontrak, jangka waktu, jam kerja & lembur, upah + terbilang, BPJS, THR, cuti, kompensasi, pengakhiran, dan tanda tangan bermeterai. Bagian yang belum kamu isi ditandai `[isi: ...]`, tidak diisi dengan data karangan.
- ✅ **Cek kontrak lama dalam sekali tempel**: menemukan pasal yang sering bikin usaha kalah di Disnaker, misalnya masa percobaan di kontrak, pekerjaan tetap dikontrak, lebih dari 5 tahun, gaji di bawah UMK, tanpa BPJS, atau denda berlebihan. Setiap temuan diberi tingkat risiko (🔴/🟠/🟢) dan kalimat pengganti yang siap tempel.
- ✅ **Kompensasi & ganti rugi dihitung script**, bukan dikira-kira: kompensasi per periode kontrak, cek batas 5 tahun termasuk perpanjangan, dan ganti rugi sisa kontrak kalau diputus lebih cepat.
- ✅ **Paham input sehari-hari**: tanggal "1 Januari 2026" atau "01/01/2026", gaji "Rp5.000.000" atau "5jt". Kalau ada yang salah (tanggal terbalik, angka negatif), kamu diberi tahu dengan bahasa jelas.
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
