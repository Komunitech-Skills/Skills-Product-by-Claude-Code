# Siap Ajukan KUR Tanpa Bingung

**Hitung cicilan, cek sanggup bayar atau tidak, dan siapkan dokumen serta profil usaha — sebelum datang ke bank.**

Diuji AI penguji independen di OpenClaw: 6,0 → 9,0 dari 10 (tanpa skill menyebut "flat 6%" itu murah dan menyarankan agunan tambahan; dengan skill dijelaskan bahwa "flat 6%" setara ±11% efektif, batas 2 kali akad (perjanjian kredit) KUR (Kredit Usaha Rakyat) Mikro dagang, dan hak tanpa agunan tambahan sampai Rp100 juta).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Simulasi cicilan **anuitas** (bunga dihitung dari sisa pinjaman) **vs flat** (bunga dihitung dari pinjaman awal terus) dengan penjelasan sederhana kenapa flat bisa jauh lebih mahal
- ✅ Tahu sejak awal cicilan itu berapa persen dari laba — dengan peringatan jelas kalau terlalu berat (patokan umum 30% dari laba, bukan aturan bank) — plus perkiraan **plafon (jumlah pinjaman) maksimal yang masih terjangkau** untuk usaha Anda
- ✅ Profil usaha & rencana penggunaan dana siap salin, jumlahnya dicek otomatis
- ✅ Cek otomatis terhadap aturan KUR yang berlaku per September 2026 (Permenko Perekonomian 1/2026, peraturan menteri tentang KUR): jenis KUR, bunga acuan, batas tenor (lama cicilan), kapan wajib NPWP (nomor pokok wajib pajak), dan hak **tanpa agunan tambahan (jaminan) s.d. Rp100 juta**
- ✅ Checklist dokumen lengkap: syarat resmi dan yang perlu dicek ke bank penyalur dipisahkan jelas

## Cocok untuk siapa
- Pemilik usaha mikro/kecil yang pertama kali mau mengajukan KUR
- Pengusaha yang ingin menambah modal tapi takut cicilan memberatkan
- Pendamping UMKM, koperasi, atau admin yang membantu banyak pelaku usaha

## Contoh sebelum & sesudah
**Sebelum:** Datang ke bank tanpa persiapan, bingung ditanya rencana penggunaan dana, dan baru sadar cicilannya berat setelah akad.

**Sesudah (cukup ketik):** "Saya punya bengkel las “Las Contoh Jaya” di Bekasi, udah jalan 4 tahun, punya NIB, karyawan 3 orang. Laba bersih sekitar 6 juta sebulan. Mau ajukan KUR BRI 100 juta 5 tahun buat beli mesin las & mesin bending 70 juta sama stok besi 30 juta. Tolong siapin semua yang perlu, sama cicilannya berapa, kuat nggak saya?" (NIB = Nomor Induk Berusaha)

Cuplikan hasil (contoh dengan data fiktif; dipotong dari `examples/01-bengkel-las-100jt.md`):
> ### 1. Simulasi cicilan (Rp 100.000.000, 60 bulan)
> | | Anuitas (efektif) — yang berlaku untuk KUR | Flat 6% (ilustrasi) |
> |---|---:|---:|
> | Cicilan/bulan | **Rp 1.933.280** | Rp 2.166.667 |
> | Total bunga | Rp 15.996.809 | Rp 30.000.000 |
> | Total dibayar | Rp 115.996.809 | Rp 130.000.000 |
>
> …
>
> ### 2. Kemampuan bayar
> Laba bersih Rp 6.000.000/bulan → cicilan **32,2%** dari laba → 🟡 **BERAT, perlu hati-hati**. Sisa laba Rp 4.066.720/bulan.

Hasil lengkapnya juga memuat rencana penggunaan dana, profil usaha siap salin, dan checklist dokumen.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Bantu saya siapkan pengajuan KUR 30 juta untuk warung sembako"
- "Bank menawarkan bunga flat 0,5% per bulan, itu mahal nggak dibanding efektif?"
- "Dengan laba 5 juta sebulan, maksimal saya aman pinjam berapa?"

## Instalasi singkat
Salin folder `pengajuan-kur` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw (lingkungan uji terpisah), 1 Okt 2026 (v1.2.3), skor 1–10 penguji independen: tanpa skill **6,0** → dengan skill **9,0** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Contoh bengkel laba Rp6,5 jt/bulan, KUR Rp75 jt: cicilan anuitas **Rp2.281.645** (=35,1% laba, BERAT), plafon aman ±Rp64 jt; "flat 6%" dijelaskan setara ±11% efektif vs KUR resmi 6% efektif.

**Status uji (jujur):** tidak menjamin persetujuan bank; angka acuan Permenko 1/2026 — konfirmasi ke bank penyalur. Sudah diuji di OpenClaw (uji otomatis agent) dan bot Telegram uji.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech): gelombang 7, 2026-10-05.
- Tanpa skill: (pesan di grup uji internal Komunitech) — skor 6
- Dengan skill: (pesan di grup uji internal Komunitech) — skor 8,5
Verdik gelombang: LULUS — dengan skill AI menghitung cicilan anuitas 6% efektif (Rp2.281.645, 35,1% dari laba), plafon aman 30% (±Rp64,1 jt), memperingatkan bahwa "flat 6%" setara ±11% efektif, dan menyebut hak tanpa agunan tambahan (Pasal 20); sedangkan tanpa skill AI keliru menganggap KUR berbunga "flat 6%" sehingga cicilan terhitung Rp176.688 per bulan lebih besar (Rp2,46 jt, 38% dari laba).

## FAQ
**Apakah skill ini menjamin KUR saya disetujui?**
Tidak. Keputusan sepenuhnya ada di bank. Skill ini membantu Anda datang lebih siap dan tahu kemampuan bayar sendiri.

**Suku bunga KUR berapa?**
Menurut Permenko Perekonomian 1/2026 (dicek September 2026): KUR Super Mikro 3%, KUR Mikro & Kecil sektor produksi 6% efektif per tahun. Untuk sektor perdagangan, bunganya naik bertahap sesuai pinjaman ke berapa. Skill memakai angka ini sebagai acuan dan mengingatkan Anda untuk konfirmasi ke bank penyalur, karena aturan bisa berubah.

**Apakah data saya dikirim ke bank?**
Tidak. Skill tidak mengisi formulir atau mengirim data ke mana pun. Hitungan berjalan di komputer Anda sendiri.

## Riwayat perubahan

Versi terkini: **1.2.3**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
