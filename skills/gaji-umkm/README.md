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

Panduan lengkap (termasuk Windows) ada di `docs/instalasi.md` di dalam paket.

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
