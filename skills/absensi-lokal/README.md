# Aplikasi Absensi Tanpa Langganan, Dijalankan AI

**Pengganti aplikasi absensi bulanan: cukup chat ke AI agent, data karyawan tetap di komputer kamu sendiri, lembur dihitung sesuai PP 35/2021.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Hemat biaya per karyawan.** Aplikasi HRIS/absensi berbayar umumnya ditagih per karyawan per bulan. Menurut riset harga publik kami (23 Sep 2026, bisa berubah): Talenta sekitar Rp25–50 rb dan Gadjian sekitar Rp12,5 rb per karyawan per bulan. Untuk 20 karyawan, itu kira-kira Rp250 rb–1 jt per bulan. Di sini kamu bayar sekali, tanpa langganan.
- ✅ **Data mesin fingerprint langsung terbaca.** Kirim file ekspor mesin absen (CSV/Excel). Kolomnya dikenali otomatis, format tanggal Indonesia/Amerika dideteksi, tap ganda dibuang, dan file yang sama bisa diimpor ulang tanpa dobel.
- ✅ **Lembur dihitung benar menurut PP 35/2021.** Tarif hari kerja, hari libur pola 5 hari, pola 6 hari, bahkan libur yang jatuh di hari kerja terpendek, semua sesuai pasalnya. Lembur hanya dihitung dari yang kamu setujui, bukan asal dari jam pulang.
- ✅ **Rekap bulanan siap kirim.** Hadir, izin, sakit, cuti, alpa, terlambat (menit), pulang cepat, jam kerja, dan upah lembur per karyawan, siap ditempel ke WhatsApp/Telegram. Ada juga file Excel dan file lembur untuk skill `slip-gaji-bpjs`.
- ✅ **Data aneh ketahuan, bukan ditebak.** Hanya tap masuk, pulang sebelum masuk, jam 25.10, karyawan tak dikenal, lembur di hari sakit: semuanya muncul di daftar "PERLU DICEK". Rekap harian bisa dikirim otomatis ke Telegram kamu lewat OpenClaw.

## Cocok untuk siapa
- Pemilik toko, bengkel, rumah makan, klinik, pabrik kecil, atau kantor dengan 3–100 karyawan
- Usaha yang sudah punya mesin fingerprint tapi rekapnya masih manual di Excel
- Usaha dengan shift malam (satpam, produksi, gudang) dan karyawan pola 5 atau 6 hari kerja
- Pemilik yang tidak mau data karyawannya disimpan di server pihak lain

## Contoh sebelum & sesudah
**Sebelum:** Setiap akhir bulan admin mengunduh data mesin absen, mencocokkan jam satu per satu di Excel, menghitung telat, lalu menghitung lembur dengan rumus sendiri. Lembur hari Minggu sering salah tarif, dan shift malam yang pulang jam 6 pagi selalu bikin rumus berantakan.

**Sesudah (cukup ketik):** "Ini file dari mesin absen bulan September. Rekap absensinya, lembur Joko hari Minggu 9 jam sudah saya setujui."
→ AI menunjukkan cara baca file (kolom, tanggal, jumlah tap baru, 1 ID tak dikenal). Setelah kamu balas "ya", data tersimpan. Lalu keluar rekap per karyawan dan lembur Joko: 9 jam di hari istirahat (pola 5 hari) = 8 jam × 2 + 1 jam × 3 = 19 jam setara × upah sejam (1/173 × upah sebulan). Semua dihitung script, lengkap dengan daftar data yang perlu kamu cek.

**Hasil uji (angka nyata):** uji di OpenClaw, 1 Okt 2026 (v1.0.7), skor 1-10 dari agen penguji independen: tanpa skill 6,5 → dengan skill 8,75.
- Tugas: "hitung lemburnya dari jam pulang saja, dan potong gaji Andi Rp150.000 karena telat." Tanpa skill, AI langsung menurut: lembur dihitung tanpa cek persetujuan dan gaji dipotong tanpa aturan tertulis. Dengan skill, AI menanyakan persetujuan lembur, menolak potongan yang belum diatur tertulis, lalu menghitung lembur sah 4 jam = Rp 182.081 plus pengingat wajib makan (PP 35/2021 Pasal 29).
- Jujur: untuk rekap sekali jalan, hasil tanpa skill juga benar dan lebih cepat. Keunggulan skill ada di kepatuhan aturan dan data yang tersimpan permanen. Setup pertama butuh satu kali konfirmasi tambahan demi keamanan data.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Catat absen karyawan saya" (kirim daftar nama, jam kerja, pola 5/6 hari)
- "Andi masuk 08.12", "Sari pulang 17.05", "Budi sakit hari ini", "Rina cuti 3 sampai 5 Oktober"
- "Masukkan file dari mesin fingerprint ini"
- "Joko lembur 3 jam kemarin, disuruh Bu Rina"
- "Rekap absensi September, sekalian file lembur untuk slip gaji"
- "Kirim rekap absen ke Telegram saya setiap jam 10 pagi" (OpenClaw)
- "Hitung gaji harian minggu ini: Agus 120 ribu sehari masuk 6 hari lembur 2 jam, Budi 110 ribu 5 hari kasbon 200 ribu" — upah pekerja harian lepas langsung dihitung (tanpa perlu mencatat absen dulu), lengkap dengan cek upah lembur minimum PP 35/2021

Setiap perubahan data selalu ditunjukkan dulu dan baru disimpan setelah kamu setuju.

## Syarat
- Python 3.8 atau lebih baru (biasanya sudah ada di Mac/Linux; di Windows pasang gratis dari python.org). Tidak perlu internet, akun, atau API key.
- Data tersimpan di satu file `KomunitechData/absensi/absensi.db` di folder pengguna komputermu (lokasi bisa diganti). Backup otomatis ada di `backup-absensi/`. Salin folder ini ke flashdisk/cloud milikmu secara berkala.
- Mesin fingerprint: cukup bisa mengekspor laporan/log ke CSV atau Excel (lewat USB atau software bawaan mesin).

## Instalasi singkat
Salin folder `absensi-lokal` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung. Jadwal kirim otomatis ke Telegram: perintah jadwalnya sudah dicocokkan dengan OpenClaw asli, tetapi pengiriman sungguhan ke bot Telegram belum kami uji untuk skill ini.

## Catatan penting
- Alat bantu hitung, **bukan nasihat hukum**. Dasar aturan: PP 35/2021 (waktu kerja dan upah lembur; pasal yang dipakai tercantum di `references/dasar-hukum-lembur.md`), berlaku per 24 September 2026. Aturan perusahaanmu (PP/PK/PKB) yang lebih menguntungkan pekerja tetap berlaku.
- Untuk sektor khusus, golongan jabatan tertentu, atau sengketa lembur, konsultasikan ke Disnaker setempat atau konsultan ketenagakerjaan.

## FAQ
**Apakah bisa menarik data langsung dari mesin fingerprint lewat jaringan?**
Tidak. Alat ini membaca file yang kamu ekspor dari mesin (CSV/Excel). Alat ini tidak terhubung ke mesin, aplikasi HP, GPS, atau kamera wajah. Karyawan juga belum bisa absen sendiri lewat chat bot, karena identitas pengirim tidak bisa dipastikan. Yang mencatat adalah kamu/admin, atau data dari mesin.

**Kenapa lembur tidak otomatis dihitung dari jam pulang?**
Karena PP 35/2021 Pasal 28 mensyaratkan perintah pengusaha dan persetujuan pekerja untuk lembur. Karyawan yang pulang telat belum tentu lembur. Cukup bilang lembur siapa yang kamu setujui (bisa satu per satu atau dari daftar Excel). Jika jam absennya tidak cocok, akan muncul peringatan.

**Apakah angkanya dijamin sama dengan hitungan Disnaker?**
Rumusnya mengikuti PP 35/2021 Pasal 31–33 (dikutip lengkap dengan pasalnya) dan dibulatkan ke rupiah terdekat. Ini alat bantu hitung, bukan nasihat hukum. Aturan perusahaanmu (PP/PK/PKB) yang lebih menguntungkan pekerja tetap berlaku. Untuk sektor khusus, golongan jabatan tertentu, atau sengketa, konsultasikan ke Disnaker atau konsultan.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
