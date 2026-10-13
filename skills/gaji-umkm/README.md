# Aplikasi Gaji Bulanan UMKM, Dijalankan AI

**Hitung gaji semua karyawan, BPJS, PPh 21, dan slip cukup lewat chat. Data disimpan di komputer Anda, tanpa biaya bulanan.**

Diuji AI penguji independen di OpenClaw: 7 → 9 dari 10 pada uji ulang v1.0.11 (13 Okt 2026, dua percobaan per sisi, pesan identik). Uji sebelumnya, 1 Okt 2026, seri 8 → 8; setelah perbaikan v1.0.6 hanya sisi dengan skill diulang, hasilnya 8 → 9. Angka gaji kedua sisi sama-sama benar; pembeda dengan skill: angka dari mesin hitung, setoran BPJS Kesehatan dan Ketenagakerjaan dipisah, biaya perusahaan disebut, asumsi bernomor, dasar aturan dan disclaimer tercantum, serta tidak mengklaim "di atas UMK (upah minimum kota/kabupaten), aman" tanpa angka (tanpa skill, satu dari dua percobaan mengklaimnya).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tutup gaji sebulan lewat chat.** Tulis bonus, kasbon, dan lembur bulan ini, lalu AI menghitung gaji semua karyawan sekaligus: gaji kotor, potongan BPJS karyawan, iuran BPJS perusahaan, PPh 21, dan gaji bersih.
- ✅ **Tahu berapa yang harus dibayar.** Setiap bulan keluar ringkasan "Yang harus dibayar/disetor": total transfer gaji, setoran BPJS Kesehatan, BPJS Ketenagakerjaan, PPh 21, dan total biaya gaji perusahaan.
- ✅ **Desember dan karyawan resign tidak bikin pusing.** PPh 21 bulan terakhir wajib dihitung ulang setahun. Aplikasi mengambil sendiri data Januari sampai bulan lalu dari riwayatnya, lalu mengecek ulang hasilnya dengan kalkulator PPh 21 terpisah sebagai bahan bukti potong.
- ✅ **Gaji yang sudah final tidak bisa diubah diam-diam.** Setelah dikunci, perubahan hanya lewat revisi dengan alasan tertulis. Selisih per karyawan tercatat, dan file transfer revisi hanya berisi kekurangannya.
- ✅ **Slip dan file transfer siap pakai.** Slip per karyawan siap dikirim satu per satu, dan file daftar transfer (format CSV, file tabel yang bisa dibuka di Excel) bisa Anda unggah sendiri ke internet banking. NIK dan nomor rekening disamarkan secara bawaan (nomor rekening lengkap hanya bila Anda memintanya untuk diunggah ke bank). Pengingat tanggal gajian dan batas setor pajak/BPJS bisa dijadwalkan ke Telegram Anda lewat OpenClaw (pengiriman sungguhan belum diuji langsung).

## Cocok untuk siapa
- Pemilik toko, bengkel, rumah makan, klinik, konveksi, atau kantor kecil dengan 5–50 karyawan
- Admin/keuangan yang masih menghitung gaji, BPJS, dan PPh 21 di Excel setiap bulan
- Usaha yang sudah memakai skill Absensi Lokal (`absensi-lokal`, pencatat absen dan lembur): lembur langsung masuk ke gaji
- Pemilik yang tidak mau data gaji karyawannya disimpan di server pihak lain

## Contoh sebelum & sesudah
**Sebelum:** Setiap tanggal 25 admin menyalin file Excel bulan lalu, mengubah bonus dan kasbon, menghitung lembur dan BPJS dengan rumus sendiri, lalu menebak tarif PPh 21. Di bulan Desember, PPh 21 sering kacau karena data Januari–November tercecer. Slip dibuat satu per satu, dan transfer diketik manual.

**Sesudah (cukup ketik):** "Gaji September: Sari kasbon 250 ribu, Rina bonus sejuta, lembur ambil dari file absensi ini."
→ AI menunjukkan dulu lembur yang terbaca dari file absensi (Sari alpa 2 hari **tidak** dipotong otomatis). Setelah Anda balas "ya", keluar rekap gaji. Anda periksa, bilang "kunci", lalu slip dan file transfer langsung jadi. Cuplikan dari contoh sesi pembuat skill (`examples/contoh-sesi-toko-bangunan.md`; skrip dijalankan sungguhan, data fiktif, toko bangunan 4 karyawan; bukan hasil uji independen):
```
REKAP GAJI SEPTEMBER 2026 - Toko Bangunan Sumber Rejeki (fiktif)
Status: DRAF (belum final) | 4 karyawan

| Kode | Nama | Pendapatan | Potongan | PPh 21 | Gaji bersih | Biaya perusahaan |
|---|---|---:|---:|---:|---:|---:|
…
| | Total | Rp 23.357.515 | Rp 1.187.147 | Rp 167.147 | Rp 22.170.368 | Rp 25.411.865 |

Yang harus dibayar/disetor:
- Transfer gaji bersih ke karyawan: Rp 22.170.368
- Setor BPJS Kesehatan (4% perusahaan + 1% karyawan): Rp 1.012.500
- Setor BPJS Ketenagakerjaan (JHT, JKK, JKM, JP): Rp 1.811.850
- Setor PPh 21: Rp 167.147
- Total biaya gaji perusahaan: Rp 25.411.865
```
(BPJS Ketenagakerjaan: JHT = jaminan hari tua, JKK = kecelakaan kerja, JKM = kematian, JP = pensiun.)

## Cara pakai
Setelah terpasang, ketik permintaan biasa ke AI agent Anda, misalnya:
- "Mulai pakai aplikasi gaji. Ini daftar karyawan saya" (kirim nama, status PTKP, gaji pokok, tunjangan, tanggal masuk; status PTKP = status pajak, mis. TK/0 = belum menikah tanpa tanggungan, K/1 = menikah dengan 1 tanggungan)
- "Hitung gaji September. Andi bonus 500 ribu, Sari kasbon 250 ribu"
- "Kunci gaji September, buatkan slip dan file transfernya"
- "Joko resign tanggal 14 November" / "Ada karyawan baru, Dewi, masuk 15 Oktober"
- "THR Lebaran masuk gaji Maret, hari rayanya 10 Maret 2027"
- "Gaji Agustus salah, lembur Andi terlewat. Revisi."
- "Ingatkan saya tanggal gajian dan batas setor pajak lewat Telegram" (OpenClaw; pengiriman sungguhan belum diuji langsung)

Perubahan penting ditunjukkan dulu, dan baru disimpan setelah Anda setuju.

## Syarat
- Python 3.8 atau lebih baru (biasanya sudah ada di Mac/Linux; di Windows pasang gratis dari python.org). Tidak perlu internet, akun, atau API key.
- Data tersimpan di satu file `KomunitechData/gaji/gaji.db` di folder pengguna komputer Anda (lokasi bisa diganti). Cadangan otomatis ada di `backup-gaji/`. Salin folder ini ke flashdisk atau penyimpanan milik Anda secara berkala.
- Tidak terhubung ke bank, BPJS, atau Coretax (sistem pajak DJP). Anda yang mengunggah file transfer dan melakukan setoran.

## Instalasi singkat
Salin folder `gaji-umkm` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex (belum diuji langsung) | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor (belum diuji langsung) | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Hasil uji (angka nyata):** uji banding tanpa vs dengan skill oleh agen penguji independen (26 Sep 2026; 12 karyawan fiktif; simulasi Claude Code).
- Tanpa skill: penguji yang sangat teliti butuh ±1 jam untuk mendapat angka yang benar. Agen umum berisiko terjebak (penilaian penguji, bukan hasil ukur berulang), misalnya memakai batas upah JP (Jaminan Pensiun) lama Rp 10.547.400 (berlaku s.d. Februari 2026), PPh 21 Eka kurang potong (Rp 900.000, yang benar Rp 1.092.420), atau Lina yang resign 14 September dihitung biasa (seharusnya kelebihan potong Rp 931.100 dikembalikan). Tidak ada riwayat bulan lalu, slip, atau file transfer.
- Dengan skill: 12 dari 12 karyawan cocok dengan hitungan independen di semua komponen, dalam ±6 perintah dan kurang dari 1 menit waktu script (program kecil). Lina dihitung ulang setahun dengan benar, lalu slip dan file transfer langsung jadi.
- Skor penguji independen pada uji simulasi Claude Code (bukan sebelum/sesudah OpenClaw): 8 dari 10 pada uji pertama, 9 dari 10 setelah perbaikan; uji ulang terakhir (v1.0.11, 5 Okt 2026) tetap 9 dari 10.
- Uji OpenClaw 1 Okt 2026: tanpa skill 8 → dengan skill 8 pada uji pertama (seri), lalu 9 setelah perbaikan v1.0.6; skor tanpa skill saat itu tidak diulang.
- **Uji ulang v1.0.11, 13 Okt 2026** (OpenClaw 2026.10.2, penguji independen, 2 percobaan per sisi, pesan identik, semua angka dicek ulang dengan Python): tanpa skill **7** → dengan skill **9** (LULUS, selisih +2,0). Transfer Rp3.164.150 dan Rp2.544.000, setor BPJS Rp818.800, PPh 21 Rp0 benar di kedua sisi; tanpa skill setoran digabung ke satu "rekening BPJS", tanpa dasar aturan dan disclaimer. Catatan jujur: sisi dengan skill belum menyebut lokasi file CSV/slip dan tenggat setor.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia; terakhir 13 Okt 2026 pada v1.0.11) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung. Jadwal kirim otomatis ke Telegram: panduan perintah jadwalnya ada di dalam skill (khusus OpenClaw), tetapi pengiriman sungguhan ke bot Telegram belum kami uji untuk skill ini.

## Catatan penting
- Hitungan PPh 21 DTP (PPh 21 ditanggung pemerintah, PMK 105/2025) masih menunggu review konsultan pajak. Sampai selesai, cocokkan bagian itu dengan konsultan pajak Anda. Dasar aturan lain, tanggal berlaku, dan catatan pembulatan Coretax ada di FAQ pertama di bawah.

## FAQ
**Apakah hitungan BPJS dan PPh 21-nya benar?**
Angkanya dihitung oleh script (program kecil) dari skill Komunitech yang sudah diuji, yaitu Slip Gaji & BPJS (`slip-gaji-bpjs`, menghitung BPJS dan membuat slip), PPh 21 TER (`pph21-ter`, menghitung pajak penghasilan karyawan per bulan), dan Hitung THR (`hitung-thr`, tunjangan hari raya), dengan dasar Perpres 64/2020, PP 44–46/2015, PP 35/2021, PP 58/2023, PMK 168/2023, dan Permenaker 6/2016 (berlaku per 23 September 2026). Pembulatan belum dicocokkan dengan Coretax (sistem pajak DJP) atau aplikasi BPJS; bila berbeda, ikuti sistem resmi. Ini alat bantu hitung, bukan nasihat pajak. Untuk kasus khusus, tanyakan ke konsultan pajak.

**Karyawan masuk atau keluar di tengah bulan, gajinya diprorata (dihitung sesuai jumlah hari kerja)?**
Tidak otomatis, karena cara prorata tergantung perjanjian kerja masing-masing usaha. Aplikasi akan mengingatkan, lalu Anda cukup menyebutkan nominal yang dibayar. PPh 21 bulan keluar tetap dihitung ulang setahun sesuai aturan.

**Apakah bisa transfer gaji langsung dari aplikasi?**
Tidak, dan memang disengaja. Aplikasi hanya membuat file CSV daftar transfer. Anda yang mengunggah ke internet banking dan menyetujuinya. Nomor rekening di file disamarkan, kecuali Anda memintanya lengkap untuk diunggah ke bank.

## Riwayat perubahan

Versi terkini: **1.0.11**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
