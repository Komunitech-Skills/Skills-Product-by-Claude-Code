# Kontrak Karyawan Kontrak: Pasal Dicek, Hak Dihitung

**Buat kontrak PKWT (Perjanjian Kerja Waktu Tertentu, yaitu kontrak karyawan kontrak) siap cetak, periksa kontrak lama dari pasal berisiko, dan hitung kompensasi habis kontrak sampai ke rupiahnya. Hasilnya draf bantu, bukan nasihat hukum.**

Diuji AI penguji independen di OpenClaw: 2,25 → 9,25 dari 10 (tanpa skill ganti rugi sisa kontrak terlewat; dengan skill kompensasi dan ganti rugi dihitung skrip, total Rp21.115.591 pada skenario uji).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Draf kontrak PKWT 12 pasal siap cetak**: jabatan & alasan kontrak, jangka waktu, jam kerja & lembur, upah + terbilang (ditulis dengan huruf), BPJS, THR, cuti, kompensasi, pengakhiran, dan tanda tangan bermeterai. Bagian yang belum Anda isi ditandai `[isi: ...]`, tidak diisi dengan data karangan.
- ✅ **Cek kontrak lama dalam sekali tempel**: menemukan pasal yang sering bikin usaha kalah di Disnaker (Dinas Tenaga Kerja), misalnya masa percobaan di kontrak, pekerjaan tetap dikontrak, lebih dari 5 tahun, gaji di bawah UMK (upah minimum kota/kabupaten), tanpa BPJS, atau denda berlebihan. Setiap temuan diberi tingkat risiko (🔴/🟠/🟢) dan kalimat pengganti yang siap tempel.
- ✅ **Kompensasi & ganti rugi dihitung script**, bukan dikira-kira: kompensasi per periode kontrak, cek batas 5 tahun termasuk perpanjangan, dan ganti rugi sisa kontrak kalau diputus lebih cepat.
- ✅ **Paham input sehari-hari**: tanggal "1 Januari 2026" atau "01/01/2026", gaji "Rp5.000.000" atau "5jt". Kalau ada yang salah (tanggal terbalik, angka negatif), Anda diberi tahu dengan bahasa jelas.
- ✅ **Paham usaha mikro/kecil**: untuk warung, kedai, dan usaha kecil, besaran kompensasi boleh sesuai kesepakatan (PP 35/2021 Pasal 16 ayat (6)); skill menampilkan hitungan rumus umum sebagai acuan dan menyiapkan klausul kesepakatannya.
- ✅ **Jujur soal aturan yang sedang berubah**: dasar hukum dan tanggal cek disebut, termasuk status Putusan MK 168/2023 dan UU Ketenagakerjaan baru yang sedang dibahas.

## Cocok untuk siapa
- Pemilik UMKM (kafe, toko, bengkel, kontraktor, konveksi) yang merekrut karyawan kontrak, tenaga proyek, atau pekerja musiman
- Staf HR/admin di usaha yang belum punya konsultan hukum tetap
- Pemilik usaha yang ingin memeriksa kontrak lama sebelum diperpanjang
- Siapa pun yang bingung "kontrak habis, harus bayar berapa?"

## Contoh sebelum & sesudah
**Sebelum:** Pakai template kontrak dari internet: ada "masa percobaan 3 bulan", tidak ada pasal kompensasi, dan tertulis "denda 3× gaji bila resign". Saat karyawan melapor ke Disnaker, usaha harus membayar kompensasi plus ganti rugi, dan kontraknya bisa dianggap karyawan tetap.

**Sesudah (cukup ketik):** "Bikinin kontrak buat Dimas, barista kedai kopi saya di Bandung, 1 tahun mulai 1 Oktober 2026, gaji 3,8 juta + tunjangan transport tetap 300 ribu, 3 bulan pertama masa percobaan."

Cuplikan hitungan (dipotong; contoh dengan data fiktif, hasil hitung nyata dari alat hitung bawaan skill):
```
HITUNG KOMPENSASI AKHIR PKWT
Upah 1 bulan : Rp4.100.000 (gaji pokok Rp3.800.000 + tunjangan tetap Rp300.000)
Total PKWT   : 1 Oktober 2026 s.d. 30 September 2027 = 12 bulan (batas 5 tahun: s.d. 30 September 2031) OK
…
TOTAL KOMPENSASI (dibayar pengusaha ke pekerja): Rp4.100.000
```
Sebelum drafnya, Anda diberi tahu bahwa masa percobaan di kontrak PKWT batal demi hukum, lalu ditanya alasan posisinya dikontrak. Hasil lengkapnya: draf 12 pasal dengan upah **Rp4.100.000 (empat juta seratus ribu rupiah)**, daftar isian yang masih kosong (termasuk UMK Bandung yang perlu Anda cek), checklist sebelum tanda tangan, dan disclaimer.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda:
- "Buatkan kontrak kerja 6 bulan untuk tukang proyek renovasi ruko"
- "Tolong cek kontrak karyawan ini, ada yang melanggar nggak?" (tempel isi kontrak)
- "Kontrak Andi mulai 1 Februari 2025, diperpanjang sampai Juli 2026, saya putus 20 Mei. Harus bayar berapa?"

Skrip hitung butuh Python 3 (biasanya sudah ada di Mac/Linux; di Windows bisa dipasang gratis). Tanpa Python pun skill tetap bisa dipakai, karena rumusnya ditulis lengkap dan agent akan memberi label "dihitung manual".

## Instalasi singkat
Salin folder `kontrak-kerja-pkwt` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Di Windows, skrip dijalankan dengan `python` atau `py`.

**Hasil uji (angka nyata):** dua sumber, skor 1–10.
- **Uji OpenClaw otomatis agent, Okt 2026** (v1.0.8; angka dari `examples/00-openclaw-sebelum-sesudah.md`): tanpa skill **2,25** → dengan skill **9,25** (lulus).
- **Uji bot Telegram asli, 3 Okt 2026**, skenario karyawan diberhentikan sebelum kontrak habis: tanpa skill melewatkan uang kompensasi (ganti rugi sisa kontrak sudah benar); dengan skill keduanya dihitung, kompensasi Rp3.534.946 + ganti rugi Rp17.580.645 = **Rp21.115.591**. Uji ini tanpa skor angka; rinciannya ada di bagian "Bukti uji di bot Telegram" di bawah.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-01; muat CLI) dan bot Telegram asli. Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli. PERLU REVIEW: nomor ayat PP 35/2021 dari sumber sekunder.

## Bukti uji di bot Telegram

Diuji di bot Telegram OpenClaw asli milik Komunitech (grup uji internal) pada 3 Okt 2026; versi skill saat uji tidak tercatat. Pesan yang sama dikirim ke bot tanpa skill dan bot dengan skill: karyawan kontrak diberhentikan sebelum kontraknya habis. Uji ini tampil di bot **tanpa skor angka**, jadi tidak ada nilai "tanpa skill → dengan skill" dan tidak ada vonis "lulus acuan kami" untuk uji Telegram ini; yang dicatat adalah perbedaan jawabannya.
- Tanpa skill: ganti rugi sisa kontrak Rp17.580.645 dihitung dengan benar, tetapi uang kompensasi habis kontrak terlewat dan bot menyebut tidak ada hak lain.
- Dengan skill: keduanya dihitung, yaitu kompensasi Rp3.534.946 + ganti rugi Rp17.580.645 = **Rp21.115.591**, selisih sekitar Rp3,5 juta dari jawaban tanpa skill.
- Catatan jujur: bot dengan skill menyebut usaha mikro/kecil boleh menyepakati besaran kompensasi; dasar pasalnya (nomor ayat PP 35/2021 dari sumber sekunder) masih perlu direview. Itu tidak mengubah angka di atas.
- Uji sebelumnya (2 Okt 2026, skenario yang sama): bot tanpa skill gagal dua kali karena model kehabisan waktu, sedangkan bot dengan skill menjawab dengan angka yang sama.

## FAQ
**Apakah kontrak dari skill ini pasti sah dan aman?**
Draf disusun mengikuti UU 13/2003 sebagaimana diubah UU 6/2023, PP 35/2021, dan Putusan MK 168/PUU-XXI/2023 (dicek 26 September 2026). Hasilnya tetap draf, bukan nasihat hukum. Keabsahan juga bergantung pada fakta di lapangan, misalnya apakah pekerjaannya memang bersifat sementara. Untuk kasus penting, mintalah Disnaker atau konsultan hukum ketenagakerjaan meninjaunya.

**Katanya ada UU Ketenagakerjaan baru. Skill ini masih berlaku?**
Mahkamah Konstitusi memerintahkan UU Ketenagakerjaan baru paling lambat sekitar akhir Oktober 2026. Per 26 September 2026, RUU Pelindungan Ketenagakerjaan belum disahkan, jadi skill memakai aturan yang berlaku saat ini dan menyebut status ini. Setelah UU baru terbit, skill akan ditinjau ulang dan pembeli akan mendapat pembaruan.

**Bisa untuk karyawan tetap atau menghitung pesangon PHK?**
Tidak. Skill ini khusus kontrak kerja waktu tertentu (PKWT), termasuk harian lepas. Untuk karyawan tetap, PHK, dan pesangon, skill akan menjelaskan bedanya lalu menyarankan Anda berkonsultasi ke Disnaker atau konsultan hukum. Untuk THR, slip gaji, dan surat peringatan, gunakan skill Komunitech `hitung-thr` (penghitung THR), `slip-gaji-bpjs` (slip gaji dan potongan BPJS), dan `surat-peringatan-karyawan` (surat peringatan untuk karyawan).

## Riwayat perubahan

Versi terkini: **1.0.8**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
