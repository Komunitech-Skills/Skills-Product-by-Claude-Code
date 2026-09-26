# Kalender Pajak Anti Telat Setor & Lapor

**Semua tenggat pajak usaha Anda dalam satu kalender — sudah digeser otomatis kalau jatuh di hari libur.**

## Manfaat
- ✅ Daftar tanggal setor & lapor setahun sesuai kondisi usaha Anda (UMKM 0,5%, PKP/PPN, punya karyawan, potong PPh 23) — untuk PKP termasuk batas unggah faktur pajak keluaran tgl 20
- ✅ Tanggal otomatis digeser ke hari kerja bila jatuh di Sabtu, Minggu, libur nasional, atau cuti bersama 2026–2027 — lengkap dengan alasannya
- ✅ File kalender (.ics) siap impor ke Google Calendar, Outlook, atau kalender HP — dengan pengingat H-3 & H-1 (di Google Calendar, pakai opsi acara pengingat terpisah; lihat FAQ)
- ✅ Checklist bulanan untuk admin + ringkasan "apa yang jatuh tempo 2 minggu ke depan"
- ✅ Bisa dijadwalkan kirim pengingat otomatis ke Telegram lewat OpenClaw

## Cocok untuk siapa
- Pemilik UMKM dan toko online yang membayar PPh final 0,5%
- CV/PT kecil yang sudah PKP dan punya karyawan
- Admin keuangan, bookkeeper, dan freelancer yang mengurus pajak beberapa klien
- Orang pribadi yang ingin tidak lupa SPT Tahunan

## Contoh sebelum & sesudah
**Sebelum:** Mencatat "setor tanggal 15, lapor tanggal 20" di kertas — lalu bingung waktu tanggal 15 jatuh di hari Minggu atau libur Lebaran, dan lupa PPN harus dilapor akhir bulan.

**Sesudah (cukup ketik):** "Saya CV PKP, karyawan 3, sering potong PPh 23. Jadwal pajak Oktober–Desember dong."
→ Tabel 21 tenggat, misalnya: *Selasa, 20 Oktober 2026 — UNGGAH faktur pajak keluaran bulan September*; *Senin, 2 November 2026 — SETOR & LAPOR PPN masa September (bergeser dari 31 Okt karena Sabtu–Minggu)*; *Senin, 21 Desember 2026 — LAPOR SPT Masa PPh 21 masa November (20 Des hari Minggu)*.

## Cara pakai
Setelah terpasang, ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatkan kalender pajak 2027 untuk usaha saya, saya jualan online pribadi pakai PPh 0,5%."
- "Pajak apa saja yang jatuh tempo 2 minggu ke depan? PT saya PKP dan punya karyawan."
- "Bikinin file .ics pengingat pajak untuk Google Calendar."
- "Ingatkan saya tiap bulan lewat Telegram."

## Instalasi singkat
Salin folder `kalender-pajak` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket. Script memakai Python standar (tanpa instal paket apa pun); tanpa Python pun skill tetap bisa menyusun jadwal dari tabel aturan.

## FAQ
**Apakah tanggalnya pasti benar?**
Tanggal disusun dari aturan PMK 81/2024 dan daftar libur SKB 3 Menteri 2026 & 2027 (dicek 25 September 2026). DJP kadang mengumumkan perpanjangan khusus, jadi tetap pantau pengumuman DJP. Untuk kasus khusus, tanyakan ke konsultan pajak atau AR Anda.

**Apakah skill ini menghitung berapa pajak saya?**
Tidak — skill ini khusus jadwal. Untuk besarannya gunakan skill "Hitung Pajak UMKM 0,5%", "PPh 21 TER", atau "Hitung PPN".

**Apakah pengingat H-3 & H-1 pasti muncul di Google Calendar?**
Belum tentu. Apple Calendar dan Outlook biasanya memakai pengingat bawaan file, tetapi Google Calendar sering mengabaikannya dan memakai notifikasi default kalender. Solusinya: atur notifikasi default kalender Google Anda (mis. 3 hari & 1 hari sebelumnya), atau minta agent membuat file "dengan acara pengingat terpisah" — hasilnya muncul sebagai acara "Pengingat H-3/H-1" di kalender. Kalau file diimpor ulang, Google bisa membuat acara dobel; paling rapi impor ke kalender khusus "Pajak" supaya mudah dihapus dan diimpor lagi.

**Bagaimana untuk tahun 2028?**
Skill tetap membuat jadwal, tetapi menampilkan peringatan karena daftar libur 2028 belum terbit. Setelah SKB 3 Menteri terbit, cukup tambahkan daftar liburnya (atau tunggu pembaruan skill). Daftar libur yang Anda tambahkan sendiri ditandai "data libur dari pengguna" dan peringatan tetap tampil sampai data resmi masuk ke skill.

## Riwayat versi
- **1.0.2** (25 Sep 2026) — perbaikan kecil dari uji ulang: batas unggah faktur (tgl 20) atau tenggat lain yang tidak bergeser dan jatuh di hari libur kini menyebut hari kerja sebelumnya (mis. 20 Mei 2027 → unggah paling aman Jumat 14 Mei 2027); SPT Tahunan yang jatuh di hari libur menampilkan dua kemungkinan tanggal (dasar Ps. 173 ayat 1 masih PERLU REVIEW); file libur buatan sendiri dilabeli "data libur dari pengguna" dan peringatan tahun tanpa data resmi tetap tampil. Tidak ada tanggal tenggat yang berubah.
- **1.0.1** (25 Sep 2026) — revisi temuan uji independen: tambah batas unggah faktur pajak keluaran tgl 20 untuk PKP (PER-11/PJ/2025); klaim pengingat Google Calendar & impor ulang diluruskan + opsi acara pengingat terpisah; keterangan libur berkoma tidak terpotong; mode "N hari ke depan" menyebut tenggat berikutnya; label alasan geser lebih jelas; output menyebut cakupan periode & sumber data libur; dasar pasal pergeseran setor diperbaiki (Ps. 100 PMK 81/2024).
- **1.0.0** (25 Sep 2026) — versi awal.

_Bukan nasihat pajak. Hasil adalah alat bantu jadwal; setoran dan pelaporan tetap lewat Coretax/DJP._
