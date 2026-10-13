# Aplikasi Gaji Bulanan UMKM, Dijalankan AI

**Hitung gaji semua karyawan, BPJS, PPh 21, dan slip cukup lewat chat. Data tetap di komputer kamu, tanpa biaya bulanan.**

## Manfaat
- ✅ **Tutup gaji sebulan dalam beberapa menit.** Tulis bonus, kasbon, dan lembur bulan ini, lalu AI menghitung gaji semua karyawan sekaligus: gaji kotor, potongan BPJS karyawan, iuran BPJS perusahaan, PPh 21, dan gaji bersih.
- ✅ **Tahu persis berapa yang harus dibayar.** Setiap bulan keluar ringkasan "Yang harus dibayar/disetor": total transfer gaji, setoran BPJS Kesehatan, BPJS Ketenagakerjaan, PPh 21, dan total biaya gaji perusahaan.
- ✅ **Desember dan karyawan resign tidak bikin pusing.** PPh 21 bulan terakhir wajib dihitung ulang setahun. Aplikasi mengambil sendiri data Januari sampai bulan lalu dari riwayatnya, lalu mengecek ulang hasilnya dengan kalkulator PPh 21 terpisah sebagai bahan bukti potong.
- ✅ **Gaji yang sudah final tidak bisa diubah diam-diam.** Setelah dikunci, perubahan hanya lewat revisi dengan alasan tertulis. Selisih per karyawan tercatat, dan file transfer revisi hanya berisi kekurangannya.
- ✅ **Slip dan file transfer siap pakai.** Slip per karyawan siap dikirim satu per satu, dan file CSV daftar transfer bisa kamu unggah sendiri ke internet banking. NIK dan nomor rekening selalu disamarkan. Pengingat tanggal gajian dan batas setor pajak/BPJS bisa dikirim ke Telegram kamu.

## Cocok untuk siapa
- Pemilik toko, bengkel, rumah makan, klinik, konveksi, atau kantor kecil dengan 5–50 karyawan
- Admin/keuangan yang masih menghitung gaji, BPJS, dan PPh 21 di Excel setiap bulan
- Usaha yang sudah memakai skill `absensi-lokal`: lembur langsung masuk ke gaji
- Pemilik yang tidak mau data gaji karyawannya disimpan di server pihak lain

## Contoh sebelum & sesudah
**Sebelum:** Setiap tanggal 25 admin menyalin file Excel bulan lalu, mengubah bonus dan kasbon, menghitung lembur dan BPJS dengan rumus sendiri, lalu menebak tarif PPh 21. Di bulan Desember, PPh 21 selalu kacau karena data Januari–November tercecer. Slip dibuat satu per satu, dan transfer diketik manual.

**Sesudah (cukup ketik):** "Gaji September: Sari kasbon 250 ribu, Rina bonus sejuta, lembur ambil dari file absensi ini."
→ AI menunjukkan lembur yang terbaca dari file absensi (Sari alpa 2 hari **tidak** dipotong otomatis). Setelah kamu balas "ya", keluar tabel gaji 4 karyawan: gaji bersih total Rp 22.170.368, setor BPJS Kesehatan Rp 1.012.500, BPJS Ketenagakerjaan Rp 1.811.850, PPh 21 Rp 167.147. Kamu periksa, bilang "kunci". Slip dan file transfer langsung jadi. Semua angka dihitung script, bukan ditebak AI.

**Hasil uji (angka nyata):** uji banding tanpa vs dengan skill oleh agen penguji independen (26 Sep 2026; 12 karyawan fiktif; simulasi Claude Code).
- Tanpa skill: penguji yang sangat teliti butuh ±1 jam untuk mendapat angka yang benar. Agen umum biasanya terjebak, misalnya memakai batas upah JP lama Rp 10.547.400 (berlaku s.d. Februari 2026), PPh 21 Eka kurang potong (Rp 900.000, yang benar Rp 1.092.420), atau Lina yang resign 14 September dihitung biasa (seharusnya kelebihan potong Rp 931.100 dikembalikan). Tidak ada riwayat bulan lalu, slip, atau file transfer.
- Dengan skill: 12 dari 12 karyawan cocok dengan hitungan independen di semua komponen, dalam ±6 perintah dan kurang dari 1 menit waktu script. Lina dihitung ulang setahun dengan benar, lalu slip dan file transfer langsung jadi.
- Skor penguji independen: 8 dari 10 pada uji pertama, 9 dari 10 setelah perbaikan; uji ulang terakhir (v1.0.11, 5 Okt 2026) tetap 9 dari 10.

## Cara pakai
Setelah terpasang, ketik permintaan biasa ke AI agent kamu, misalnya:
- "Mulai pakai aplikasi gaji. Ini daftar karyawan saya" (kirim nama, status PTKP, gaji pokok, tunjangan, tanggal masuk)
- "Hitung gaji September. Andi bonus 500 ribu, Sari kasbon 250 ribu"
- "Kunci gaji September, buatkan slip dan file transfernya"
- "Joko resign tanggal 14 November" / "Ada karyawan baru, Dewi, masuk 15 Oktober"
- "THR Lebaran masuk gaji Maret, hari rayanya 10 Maret 2027"
- "Gaji Agustus salah, lembur Andi terlewat. Revisi."
- "Ingatkan saya tanggal gajian dan batas setor pajak lewat Telegram" (OpenClaw)

Setiap perubahan penting selalu ditunjukkan dulu, dan baru disimpan setelah kamu setuju.

## Syarat
- Python 3.8 atau lebih baru (biasanya sudah ada di Mac/Linux; di Windows pasang gratis dari python.org). Tidak perlu internet, akun, atau API key.
- Data tersimpan di satu file `KomunitechData/gaji/gaji.db` di folder pengguna komputermu (lokasi bisa diganti). Cadangan otomatis ada di `backup-gaji/`. Salin folder ini ke flashdisk atau penyimpanan milikmu secara berkala.
- Tidak terhubung ke bank, BPJS, atau Coretax. Kamu yang mengunggah file transfer dan melakukan setoran.

## Instalasi singkat
Salin folder `gaji-umkm` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung. Jadwal kirim otomatis ke Telegram: perintah jadwalnya sudah dicocokkan dengan OpenClaw asli, tetapi pengiriman sungguhan ke bot Telegram belum kami uji untuk skill ini.

## Catatan penting
- Hitungan PPh 21 DTP (PMK 105/2025) masih menunggu review konsultan pajak. Sampai selesai, cocokkan bagian itu dengan konsultan pajakmu. Dasar aturan lain, tanggal berlaku, dan catatan pembulatan Coretax ada di FAQ pertama di bawah.

## FAQ
**Apakah hitungan BPJS dan PPh 21-nya benar?**
Angkanya dihitung oleh script dari skill Komunitech `slip-gaji-bpjs`, `pph21-ter`, dan `hitung-thr` yang sudah diuji, dengan dasar Perpres 64/2020, PP 44–46/2015, PP 35/2021, PP 58/2023, PMK 168/2023, dan Permenaker 6/2016 (berlaku per 23 September 2026). Pembulatan belum dicocokkan dengan Coretax atau aplikasi BPJS; bila berbeda, ikuti sistem resmi. Ini alat bantu hitung, bukan nasihat pajak. Untuk kasus khusus, tanyakan ke konsultan pajak.

**Karyawan masuk atau keluar di tengah bulan, gajinya diprorata?**
Tidak otomatis, karena cara prorata tergantung perjanjian kerja masing-masing usaha. Aplikasi akan mengingatkan, lalu kamu cukup menyebutkan nominal yang dibayar. PPh 21 bulan keluar tetap dihitung ulang setahun sesuai aturan.

**Apakah bisa transfer gaji langsung dari aplikasi?**
Tidak, dan memang disengaja. Aplikasi hanya membuat file CSV daftar transfer. Kamu yang mengunggah ke internet banking dan menyetujuinya. Nomor rekening di file disamarkan, kecuali kamu memintanya lengkap untuk diunggah ke bank.

## Catatan revisi 1.0.6 (2026-10-01)
- AI tidak lagi berhenti untuk menanyakan tanggal masuk di giliran terpisah (temuan uji OpenClaw). Bila nama, status, dan gaji pokok sudah ada, AI langsung menghitung dengan default wajar (tanggal masuk 1 Januari tahun berjalan, JKK 0,24%, ikut semua BPJS) dan menyebut asumsinya. Semua hal yang perlu dicek — tanggal masuk, **UMK daerah**, tarif JKK — digabung dalam **satu** pesan.
- Pemakaian pertama: angka langsung keluar di balasan pertama lewat mesin hitung yang sama (hitungan sementara, tanpa menyimpan), lalu database dibuat setelah Anda setuju.
- Instruksi: script dijalankan dari subfolder `scripts/` di folder skill (tidak mencari ke seluruh disk). Script aplikasi tidak berubah; uji regresi tetap lulus.

## Catatan revisi 1.0.7 (2026-10-02)
- Mesin THR (`scripts/mesin/thr.py`) disinkronkan dengan `hitung-thr` 1.0.6: peringatan untuk tanggal masuk di masa depan, karyawan yang masuk setelah hari raya ditandai belum berhak (tidak lagi menghentikan seluruh hitungan THR), dan teks pengumuman grup menegaskan rincian THR dikirim pribadi. Angka THR tidak berubah; sha256 baru dicatat di `SUMBER.json`.

## Catatan revisi 1.0.10 (2026-10-05)
- Pemeriksaan ulang PPh 21 DTP terhadap teks PMK 105/2025 (Pasal 2 ayat 1, Pasal 5, Pasal 6 ayat 6, Lampiran B): gaji bersih di slip **sudah benar** (PPh 21 dipotong, DTP dengan nilai sama dibayar tunai, setoran bagian DTP Rp 0). Catatan DTP di slip kini menulis jelas PPh dipotong, DTP dibayar tunai, dan setoran ke negara Rp 0.
- Salinan mesin disinkronkan dengan skill sumber: `payroll.py` (slip-gaji-bpjs 1.0.6), `pph21.py` (pph21-ter 1.0.5, koreksi uang diterima DTP), `thr.py` (hitung-thr 1.0.9); sha256 baru di `scripts/mesin/SUMBER.json`. Tambah tes `UjiDTP` dan `references/dtp-pmk105.md`. **PERLU REVIEW konsultan pajak.**

## Catatan revisi 1.0.11 (2026-10-05)
- Data JSON rekap (`total`) kini memisahkan tiga angka PPh 21 dengan nama yang jelas: `pph21_dipotong` = total PPh 21 yang **dipotong** dari gaji (termasuk bagian DTP), `pph21_dtp` = bagian DTP yang dibayar tunai ke karyawan dan tidak disetor, `pph21_disetor_ke_negara` = perkiraan setoran. Sebelumnya `pph21_dipotong` berisi jumlah yang disetor. `setor_pph21` tetap ada dengan nilai sama seperti sebelumnya (kompatibel). Rekap periode lama yang tersimpan diubah otomatis ke arti baru saat dibaca.
- Teks rekap bila ada karyawan DTP kini menulis "PPh 21 dipotong dari gaji bulan ini … (termasuk DTP …)" lalu "Setor PPh 21 ke negara". Angka gaji bersih & setoran tidak berubah. Mesin hitung (`scripts/mesin/`) tidak diubah. **PERLU REVIEW konsultan pajak.**

