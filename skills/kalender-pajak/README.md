# Kalender Pajak Anti Telat Setor & Lapor

**Tenggat setor dan lapor pajak usaha Anda dalam satu kalender — digeser otomatis kalau jatuh di hari libur. Alat bantu jadwal, bukan nasihat pajak.**

Diuji penguji independen: tanggal yang benar 13 → 20 dari 20 pada skenario warung perorangan (pembedanya tanggal yang digeser karena libur dan batas unggah faktur pajak tanggal 20); skor penguji 8 dari 10.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Daftar tanggal setor & lapor setahun sesuai kondisi usaha Anda (UMKM 0,5%, PKP/PPN, punya karyawan, potong PPh 23; PKP = Pengusaha Kena Pajak) — untuk PKP termasuk batas unggah faktur pajak keluaran tgl 20
- ✅ Tanggal otomatis digeser ke hari kerja bila jatuh di Sabtu, Minggu, libur nasional, atau cuti bersama 2026–2027 — lengkap dengan alasannya
- ✅ File kalender (.ics, format umum aplikasi kalender) siap impor ke Google Calendar, Outlook, atau kalender HP — dengan pengingat H-3 & H-1 (di Google Calendar, pakai opsi acara pengingat terpisah; lihat FAQ)
- ✅ Checklist bulanan untuk admin + ringkasan "apa yang jatuh tempo 2 minggu ke depan"
- ✅ Bisa dijadwalkan kirim pengingat otomatis ke Telegram lewat OpenClaw (belum diuji langsung)

## Cocok untuk siapa
- Pemilik UMKM dan toko online yang membayar PPh final 0,5%
- CV/PT kecil yang sudah PKP dan punya karyawan
- Admin keuangan, bookkeeper, dan freelancer yang mengurus pajak beberapa klien
- Orang pribadi yang ingin tidak lupa SPT Tahunan (laporan pajak tahunan)

## Contoh sebelum & sesudah
**Sebelum:** Mencatat "setor tanggal 15, lapor tanggal 20" di kertas — lalu bingung waktu tanggal 15 jatuh di hari Minggu atau libur Lebaran, dan lupa PPN harus dilapor akhir bulan.

**Sesudah (cukup ketik):** "Saya CV PKP, karyawan 3, sering potong PPh 23. Jadwal pajak Oktober–Desember dong."

Hasilnya tabel 21 tenggat. Cuplikan (dipotong; keluaran nyata skrip untuk profil contoh di atas):
```
| Tanggal | Kegiatan | Keterangan |
| Selasa, 20 Oktober 2026 | UNGGAH faktur pajak keluaran bulan Sep 2026 (batas persetujuan DJP) | - |
| Senin, 2 November 2026 | SETOR & LAPOR PPN masa Sep 2026 | bergeser dari 31 Okt (31 Okt: Sabtu; 1 Nov: Minggu) |
…
| Senin, 21 Desember 2026 | LAPOR SPT Masa PPh 21/26 masa Nov 2026 | bergeser dari 20 Des (20 Des: Minggu) |
```

## Cara pakai
Setelah terpasang, ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatkan kalender pajak 2027 untuk usaha saya, saya jualan online pribadi pakai PPh 0,5%."
- "Pajak apa saja yang jatuh tempo 2 minggu ke depan? PT saya PKP dan punya karyawan."
- "Bikinin file .ics pengingat pajak untuk Google Calendar."
- "Ingatkan saya tiap bulan lewat Telegram." (belum diuji langsung)

## Instalasi singkat
Salin folder `kalender-pajak` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Script memakai Python standar (tanpa instal paket apa pun); tanpa Python pun skill tetap bisa menyusun jadwal dari tabel aturan.

**Hasil uji (angka nyata):** satu sumber, uji independen oleh agent penguji, Sep 2026 (v1.0.7; `examples/HASIL-UJI.md`; ini bukan skor sebelum/sesudah OpenClaw). **108 tenggat** Okt 2026–Des 2027 dengan **0 selisih** dari verifikasi manual; uji A/B skenario warung perorangan (OP) — tanpa skill **13/20** tanggal benar → dengan skill **20/20**. Skor penguji: **8/10**, LULUS (setelah perbaikan batas unggah faktur tanggal 20).

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-01; muat CLI) dan Claude Code (simulasi agent). **Belum** uji bot Telegram asli untuk skill ini. Codex dan Cursor belum uji platform asli. PERLU REVIEW: beberapa pasal PMK dari sumber sekunder.

## FAQ
**Apakah tanggalnya pasti benar?**
Tanggal disusun dari aturan PMK 81/2024 dan daftar libur resmi (SKB 3 Menteri) 2026 & 2027 (pasal tenggat dicocokkan dengan naskah resmi PMK 81/2024 di pajak.go.id, 26 September 2026). Batas SPT Tahunan tidak bergeser walau jatuh di hari libur, jadi lapor lebih awal. DJP kadang mengumumkan perpanjangan khusus, jadi tetap pantau pengumuman DJP. Untuk kasus khusus, tanyakan ke konsultan pajak atau AR (petugas pajak pendamping di kantor pajak) Anda.

**Apakah skill ini menghitung berapa pajak saya?**
Tidak — skill ini khusus jadwal. Untuk besarannya gunakan skill "Hitung Pajak UMKM 0,5%", "PPh 21 TER" (PPh 21 tarif efektif bulanan), atau "Hitung PPN".

**Apakah pengingat H-3 & H-1 pasti muncul di Google Calendar?**
Belum tentu. Apple Calendar dan Outlook biasanya memakai pengingat bawaan file, tetapi Google Calendar sering mengabaikannya dan memakai notifikasi default kalender. Solusinya: atur notifikasi default kalender Google Anda (mis. 3 hari & 1 hari sebelumnya), atau minta agent membuat file "dengan acara pengingat terpisah" — hasilnya muncul sebagai acara "Pengingat H-3/H-1" di kalender. Kalau file diimpor ulang, Google bisa membuat acara dobel; paling rapi impor ke kalender khusus "Pajak" supaya mudah dihapus dan diimpor lagi.

**Bagaimana untuk tahun 2028?**
Skill tetap membuat jadwal, tetapi menampilkan peringatan karena daftar libur 2028 belum terbit. Setelah SKB 3 Menteri terbit, cukup tambahkan daftar liburnya (atau tunggu pembaruan skill). Daftar libur yang Anda tambahkan sendiri ditandai "data libur dari pengguna" dan peringatan tetap tampil sampai data resmi masuk ke skill.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
