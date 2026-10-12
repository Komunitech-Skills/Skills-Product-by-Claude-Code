# Siap Ajukan KUR Tanpa Bingung

**Hitung cicilan, cek sanggup bayar atau tidak, dan siapkan dokumen serta profil usaha — sebelum datang ke bank.**

## Manfaat
- ✅ Simulasi cicilan **anuitas vs flat** dengan penjelasan sederhana kenapa flat bisa jauh lebih mahal
- ✅ Tahu sejak awal cicilan itu berapa persen dari laba — dengan peringatan jelas kalau terlalu berat
- ✅ Hitung **plafon maksimal yang masih aman** untuk usahamu
- ✅ Profil usaha & rencana penggunaan dana siap salin, jumlahnya dicek otomatis
- ✅ Cek otomatis terhadap aturan KUR terbaru (Permenko Perekonomian 1/2026): jenis KUR, bunga acuan, batas tenor, kapan wajib NPWP, dan hak **tanpa agunan tambahan s.d. Rp100 juta**
- ✅ Checklist dokumen lengkap: syarat resmi dan yang perlu dicek ke bank penyalur dipisahkan jelas

## Cocok untuk siapa
- Pemilik usaha mikro/kecil yang pertama kali mau mengajukan KUR
- Pengusaha yang ingin menambah modal tapi takut cicilan memberatkan
- Pendamping UMKM, koperasi, atau admin yang membantu banyak pelaku usaha

## Contoh sebelum & sesudah
**Sebelum:** Datang ke bank tanpa persiapan, bingung ditanya rencana penggunaan dana, dan baru sadar cicilannya berat setelah akad.

**Sesudah (cukup ketik):** "Usaha kue saya laba 7,5 juta sebulan. Mau pinjam KUR 50 juta 3 tahun untuk oven, bahan baku, dan etalase. Cicilannya berapa? Aman nggak?"
→ Cicilan Rp 1.521.097 per bulan dengan bunga acuan KUR Mikro 6% efektif (diberi label: konfirmasi ke bank). Kamu juga dapat:
- penjelasan kenapa "flat 6%" jauh lebih mahal (setara efektif ±11%)
- rasio cicilan 20,3% dari laba (🟢 aman)
- rencana dana Rp 50.000.000 yang rapi
- profil usaha siap salin dan checklist dokumen

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Bantu saya siapkan pengajuan KUR 30 juta untuk warung sembako"
- "Bank menawarkan bunga flat 0,5% per bulan, itu mahal nggak dibanding efektif?"
- "Dengan laba 5 juta sebulan, maksimal saya aman pinjam berapa?"

## Instalasi singkat
Salin folder `pengajuan-kur` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 7, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/732/742 — skor 6
- Dengan skill: https://t.me/c/4407409583/733/745 — skor 8,5
Verdik gelombang: LULUS — DENGAN menghitung cicilan anuitas 6% efektif (Rp2.281.645, 35,1% dari laba), plafon aman 30% (±Rp64,1 jt), memperingatkan bahwa "flat 6%" setara ±11% efektif, dan menyebut hak tanpa agunan tambahan (Pasal 20); TANPA keliru menyebut KUR "flat 6%" sehingga cicilan dibesarkan Rp176.688 per bulan (Rp2,46 jt, 38%).

## FAQ
**Apakah skill ini menjamin KUR saya disetujui?**
Tidak. Keputusan sepenuhnya ada di bank. Skill ini membantu kamu datang lebih siap dan tahu kemampuan bayar sendiri.

**Suku bunga KUR berapa?**
Menurut Permenko Perekonomian 1/2026 (dicek September 2026): KUR Super Mikro 3%, KUR Mikro & Kecil sektor produksi 6% efektif per tahun. Untuk sektor perdagangan, bunganya naik bertahap sesuai pinjaman ke berapa. Skill memakai angka ini sebagai acuan dan selalu mengingatkan kamu untuk konfirmasi ke bank penyalur, karena aturan bisa berubah.

**Apakah data saya dikirim ke bank?**
Tidak. Skill tidak mengisi formulir atau mengirim data ke mana pun. Hitungan berjalan di komputermu sendiri.

## Catatan revisi 1.2.3 (2026-10-01)
- Balasan chat kini diawali **ringkasan singkat** (cicilan, aman/berat, alternatif, dokumen inti); rincian lengkap ditawarkan bila dibutuhkan.
- Bila dana dipakai untuk alat (investasi) dan stok (modal kerja), skill menghitung **opsi pisah akad** dengan tenor berbeda (mis. investasi 60 bulan) beserta cicilan dan rasio kemampuan bayarnya.
