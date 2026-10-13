# Aplikasi Absensi Tanpa Langganan, Dijalankan AI

**Pengganti aplikasi absensi bulanan: cukup chat ke AI agent, data karyawan disimpan di komputer Anda sendiri, lembur dihitung mengikuti PP 35/2021.**

Diuji AI penguji independen: 6,5 → 8,75 dari 10 (tanpa skill, lembur langsung dihitung dari jam pulang dan gaji dipotong tanpa aturan tertulis; dengan skill, persetujuan lembur ditanyakan dan potongan tanpa dasar ditolak).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Hemat biaya per karyawan.** Aplikasi HRIS (pengelolaan data karyawan)/absensi berbayar umumnya ditagih per karyawan per bulan. Menurut riset harga publik kami (23 Sep 2026, bisa berubah): Talenta sekitar Rp25–50 rb dan Gadjian sekitar Rp12,5 rb per karyawan per bulan. Untuk 20 karyawan, itu kira-kira Rp250 rb–1 jt per bulan. Di sini Anda bayar sekali, tanpa langganan.
- ✅ **Data mesin fingerprint bisa dibaca langsung.** Kirim file ekspor mesin absen (CSV/Excel; CSV = file tabel sederhana yang bisa dibuka di Excel). Kolomnya dikenali otomatis dan ditunjukkan dulu untuk Anda cek, format tanggal Indonesia/Amerika dideteksi, tap ganda (jari ditempel dua kali) dibuang, dan file yang sama bisa diimpor ulang tanpa dobel.
- ✅ **Lembur dihitung mengikuti PP 35/2021.** Tarif hari kerja, hari libur untuk pola 5 hari kerja per minggu, pola 6 hari, bahkan libur yang jatuh di hari kerja terpendek, masing-masing memakai pasal yang dikutip. Lembur hanya dihitung dari yang Anda setujui, bukan asal dari jam pulang.
- ✅ **Rekap bulanan siap kirim.** Hadir, izin, sakit, cuti, alpa, terlambat (menit), pulang cepat, jam kerja, dan upah lembur per karyawan, siap ditempel ke WhatsApp/Telegram. Ada juga file Excel dan file lembur untuk skill Slip Gaji & BPJS (`slip-gaji-bpjs`, penghitung slip gaji dan iuran BPJS).
- ✅ **Data aneh ketahuan, bukan ditebak.** Hanya tap masuk, pulang sebelum masuk, jam 25.10, karyawan tak dikenal, lembur di hari sakit: ditandai di daftar "PERLU DICEK" untuk Anda periksa. Rekap harian bisa dijadwalkan ke Telegram Anda lewat OpenClaw (pengiriman sungguhan ke Telegram belum diuji langsung).

## Cocok untuk siapa
- Pemilik toko, bengkel, rumah makan, klinik, pabrik kecil, atau kantor dengan 3–100 karyawan
- Usaha yang sudah punya mesin fingerprint tapi rekapnya masih manual di Excel
- Usaha dengan shift malam (satpam, produksi, gudang) dan karyawan pola 5 atau 6 hari kerja
- Pemilik yang tidak mau data karyawannya disimpan di server pihak lain

## Contoh sebelum & sesudah
**Sebelum:** Setiap akhir bulan admin mengunduh data mesin absen, mencocokkan jam satu per satu di Excel, menghitung telat, lalu menghitung lembur dengan rumus sendiri. Lembur hari Minggu sering salah tarif, dan shift malam yang pulang jam 6 pagi sering bikin rumus berantakan.

**Sesudah (cukup ketik):** "Pak, ini file dari mesin absen toko bulan Agustus. Tolong direkap ya. … Lembur yang saya suruh: Andi tgl 5 dua jam, Joko Minggu tgl 9 delapan jam (stok opname), Sari Sabtu tgl 15 satu setengah jam, Rudi tgl 17 lima jam antar barang. Hitungkan uang lemburnya juga."
→ AI menunjukkan dulu cara membaca file dan lembur yang akan dicatat. Setelah Anda balas "ya", data tersimpan dan keluar rekap per karyawan beserta daftar data yang perlu Anda cek. Cuplikan nyata dari uji (pratinjau lembur, data fiktif):
```
Saya akan mencatat lembur yang DISETUJUI (belum disimpan):
- Andi, Rabu 05/08: 2 jam, hari kerja (Pasal 31 ayat (1)) = 3,5 jam setara ≈ Rp 76.879
- Joko, Minggu 09/08: 8 jam, hari istirahat pola 6 hari (Pasal 31 ayat (2) huruf a:
  7 jam x 2 + 1 jam x 3) = 17 jam setara ≈ Rp 343.931
- Sari, Sabtu 15/08: 1,5 jam, hari kerja = 2,5 jam setara ≈ Rp 53.468
- Rudi, Senin 17/08 (libur resmi, bukan hari kerja terpendek): 5 jam x 2 = 10 jam setara ≈ Rp 208.092
  (dasar upah Rudi = 75% x seluruh upah Rp 4.800.000 = Rp 3.600.000, karena gaji pokok +
  tunjangan tetap < 75% — PP 35/2021 Pasal 32 ayat (4))
Catatan: lembur 8 jam Joko ≥ 4 jam → perusahaan wajib memberi makan-minum min. 1.400 kkal (Pasal 29).
Simpan? Balas "ya".
```
(Upah sejam = 1/173 × upah sebulan. Angka lembur dihitung oleh script, yaitu program kecil di dalam skill, bukan ditebak AI.)

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Catat absen karyawan saya" (kirim daftar nama, jam kerja, pola 5/6 hari)
- "Andi masuk 08.12", "Sari pulang 17.05", "Budi sakit hari ini", "Rina cuti 3 sampai 5 Oktober"
- "Masukkan file dari mesin fingerprint ini"
- "Joko lembur 3 jam kemarin, disuruh Bu Rina"
- "Rekap absensi September, sekalian file lembur untuk slip gaji"
- "Kirim rekap absen ke Telegram saya setiap jam 10 pagi" (OpenClaw; pengiriman sungguhan belum diuji langsung)
- "Hitung gaji harian minggu ini: Agus 120 ribu sehari masuk 6 hari lembur 2 jam, Budi 110 ribu 5 hari kasbon 200 ribu" — upah pekerja harian lepas langsung dihitung (tanpa perlu mencatat absen dulu), lengkap dengan cek upah lembur minimum PP 35/2021

Perubahan data ditunjukkan dulu dan baru disimpan setelah Anda setuju.

## Syarat
- Python 3.8 atau lebih baru (biasanya sudah ada di Mac/Linux; di Windows pasang gratis dari python.org). Tidak perlu internet, akun, atau API key.
- Data tersimpan di satu file `KomunitechData/absensi/absensi.db` di folder pengguna komputer Anda (lokasi bisa diganti). Backup otomatis ada di `backup-absensi/`. Salin folder ini ke flashdisk/cloud milik Anda secara berkala.
- Mesin fingerprint: cukup bisa mengekspor laporan/log ke CSV atau Excel (lewat USB atau software bawaan mesin).

## Instalasi singkat
Salin folder `absensi-lokal` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex (belum diuji langsung) | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor (belum diuji langsung) | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## Hasil uji (jujur)

**Hasil uji (angka nyata):** uji di OpenClaw, 1 Okt 2026 (v1.0.7), skor 1-10 dari agen penguji independen: tanpa skill 6,5 → dengan skill 8,75.
- Tugas: "hitung lemburnya dari jam pulang saja, dan potong gaji Andi Rp150.000 karena telat." Tanpa skill, AI langsung menurut: lembur dihitung tanpa cek persetujuan dan gaji dipotong tanpa aturan tertulis. Dengan skill, AI menanyakan persetujuan lembur, menolak potongan yang belum diatur tertulis, lalu menghitung lembur sah 4 jam = Rp 182.081 plus pengingat wajib makan (PP 35/2021 Pasal 29).
- Jujur: untuk rekap sekali jalan, hasil tanpa skill juga benar dan lebih cepat. Keunggulan skill ada di kepatuhan aturan dan data yang tersimpan permanen. Setup pertama butuh satu kali konfirmasi tambahan demi keamanan data.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung. Jadwal kirim otomatis ke Telegram: perintah jadwalnya sudah dicocokkan dengan OpenClaw asli, tetapi pengiriman sungguhan ke bot Telegram belum kami uji untuk skill ini.

## Catatan penting
- Alat bantu hitung, **bukan nasihat hukum**. Dasar aturan: PP 35/2021 (waktu kerja dan upah lembur; pasal yang dipakai tercantum di `references/dasar-hukum-lembur.md`), berlaku per 24 September 2026. Aturan perusahaan Anda (Peraturan Perusahaan/Perjanjian Kerja/Perjanjian Kerja Bersama) yang lebih menguntungkan pekerja tetap berlaku.
- Untuk sektor khusus, golongan jabatan tertentu, atau sengketa lembur, konsultasikan ke Disnaker setempat atau konsultan ketenagakerjaan.

## FAQ
**Apakah bisa menarik data langsung dari mesin fingerprint lewat jaringan?**
Tidak. Alat ini membaca file yang Anda ekspor dari mesin (CSV/Excel). Alat ini tidak terhubung ke mesin, aplikasi HP, GPS, atau kamera wajah. Karyawan juga belum bisa absen sendiri lewat chat bot, karena identitas pengirim tidak bisa dipastikan. Yang mencatat adalah Anda/admin, atau data dari mesin.

**Kenapa lembur tidak otomatis dihitung dari jam pulang?**
Karena PP 35/2021 Pasal 28 mensyaratkan perintah pengusaha dan persetujuan pekerja untuk lembur. Karyawan yang pulang telat belum tentu lembur. Cukup bilang lembur siapa yang Anda setujui (bisa satu per satu atau dari daftar Excel). Jika jam absennya tidak cocok, akan muncul peringatan.

**Apakah angkanya dijamin sama dengan hitungan Disnaker?**
Rumusnya mengikuti PP 35/2021 Pasal 31–33 (dikutip lengkap dengan pasalnya) dan dibulatkan ke rupiah terdekat. Ini alat bantu hitung, bukan nasihat hukum. Aturan perusahaan Anda (PP/PK/PKB) yang lebih menguntungkan pekerja tetap berlaku. Untuk sektor khusus, golongan jabatan tertentu, atau sengketa, konsultasikan ke Disnaker atau konsultan.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
