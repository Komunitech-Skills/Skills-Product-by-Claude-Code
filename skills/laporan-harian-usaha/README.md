# Laporan Harian Otomatis Tanpa Dashboard Berbayar

**Setiap malam satu pesan Telegram (lewat OpenClaw yang menyala) berisi omzet, stok, karyawan, dan tagihan usaha Anda. Tanpa aplikasi dashboard (layar ringkasan) berlangganan, data tetap di komputer sendiri.**

Diuji AI penguji independen di OpenClaw: 6,0 → 9,0 dari 10 (angka penjualan sudah benar di kedua sisi; pembedanya laporan baku dengan butir "Perlu Perhatian", tafsir deal dan konversi calon pembeli yang benar, dan penolakan mengirim omzet ke grup WA karyawan).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Satu pesan, seluruh usaha.** Penjualan, stok menipis, siapa yang terlambat/alpa, lembur yang perlu diputuskan, tagihan jatuh tempo, dan calon pembeli (prospek) beserta tahap penjualannya, digabung dari alat Komunitech yang sudah Anda pakai: **Kasir Lokal** (kasir), **Buku Stok** (pencatat stok), **Absensi Lokal** (catatan kehadiran), **Pengingat Follow-up** (pengingat tagihan dan tindak lanjut), dan **CRM WA** (catatan calon pembeli lewat WhatsApp).
- ✅ **Langsung kelihatan naik atau turun.** Omzet dibandingkan dengan kemarin dan hari yang sama minggu lalu dalam persen. Tiap Senin pagi ada laporan mingguan dibanding minggu sebelumnya.
- ✅ **Masalah muncul sendiri.** Selisih uang laci, stok minus, penjualan kasir yang belum masuk buku stok, absen yang belum dimasukkan, dan piutang terlambat dikumpulkan di bagian "Perlu Perhatian".
- ✅ **Angka apa adanya.** Angka diambil dari data alat Anda. Bagian yang datanya belum ada ditulis "belum ada data", tidak diisi perkiraan. Rumus persen dan pembulatan tertulis jelas.
- ✅ **Dirancang aman.** Hanya membaca data (skrip tidak menulis ke data kasir/stok/absen Anda), tanpa nama pelanggan di laporan, nama karyawan bisa disamarkan, dan dikirim hanya ke chat Anda sendiri.

## Cocok untuk siapa
- Pemilik toko, warung, kafe, atau usaha jasa yang sudah memakai minimal satu alat lokal Komunitech: **Kasir Lokal**, **Buku Stok**, **Absensi Lokal**, **Pengingat Follow-up**, atau **CRM WA**. Makin banyak alat yang dipakai, makin lengkap laporannya.
- Pemilik yang jarang di toko dan ingin tahu kondisi usaha dari HP tanpa membuka banyak aplikasi.
- Anggota VIP yang memakai OpenClaw dan ingin laporan terjadwal ke Telegram.

**Kurang cocok:** usaha yang datanya ada di aplikasi lain (Moka, Majoo, Excel dari marketplace). Untuk itu pakai skill **Laporan Otomatis Terjadwal** (penjadwal laporan ke Telegram) atau **Rekap Penjualan CSV** (membaca file tabel/CSV dari aplikasi lain).

## Contoh sebelum & sesudah
**Sebelum:** tiap malam membuka rekap kasir, lalu cek stok, lalu tanya admin siapa yang tidak masuk, lalu ingat-ingat siapa yang belum bayar. Atau berlangganan aplikasi dashboard bulanan.

**Sesudah (otomatis jam 21.00 di Telegram; contoh dengan data fiktif):**
```
LAPORAN HARIAN USAHA
Kamis, 24 September 2026

PENJUALAN
Omzet bersih: Rp 69.000
Nota: 2 (+1 dibatalkan) | rata-rata Rp 34.500
vs kemarin (Rab 23/9): Rp 36.000 -> naik 91,7%
Per metode bayar: Tunai Rp 51.000, QRIS Rp 18.000

STOK
- RB Roti Bakar - Coklat: stok -5 (min 5) MINUS
- KH Kopi Hitam: stok 4 (min 10) MENIPIS

KEHADIRAN
Hadir 2 dari 5 terjadwal | Terlambat: Andi 08.12 | Alpa: Rina

TAGIHAN & FOLLOW-UP
- #2 piutang Rp 12.500.000, lewat 3 hari

PROSPEK
Prospek baru: 1 | Follow-up terlambat 1, hari ini 2 | Deal: 1 senilai Rp 6.000.000

PERLU PERHATIAN
1. Selisih kas saat tutup kasir: KURANG Rp 11.000
2. Penjualan kasir hari ini belum diimpor ke buku stok
3. 1 follow-up prospek CRM terlambat
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Laporan usaha hari ini"
- "Gimana usaha kemarin?"
- "Laporan minggu lalu, bandingkan dengan minggu sebelumnya"
- "Kirim laporan harian ke Telegram saya tiap jam 9 malam, dan laporan mingguan tiap Senin pagi" (OpenClaw; pengiriman ke Telegram baru dicoba oleh agent, belum oleh manusia)
- "Samarkan nama karyawan di laporan"

## Instalasi singkat
Salin folder `laporan-harian-usaha` ke folder skills AI agent Anda, **di folder yang sama** dengan alat Komunitech yang Anda pakai (mis. `kasir-lokal`, `buku-stok`):

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

Butuh **Python 3.8+** (gratis di python.org; Mac/Linux biasanya sudah ada). Tidak butuh internet, akun, atau API key. Laporan terjadwal ke Telegram butuh OpenClaw yang menyala di komputer yang sama dengan data toko (panduan langkah demi langkah ada di `references/openclaw-jadwal.md`; Komunitech juga menyediakan jasa setup).

**Hasil uji (angka nyata):** uji OpenClaw (lingkungan uji terpisah), 1 Okt 2026 (v1.1.4), skor 1–10 penguji independen: tanpa skill **6,0** → dengan skill **9,0** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Tanpa skill angka penjualan benar tetapi salah menafsirkan “lead baru langsung closing” (calon pembeli baru dianggap langsung jadi pembeli) dan siap mengirim omzet ke grup WA karyawan; dengan skill laporan baku, butir PERLU PERHATIAN jelas, deal vs konversi benar, dan menolak grup/pesan massal sesuai kebijakan kanal.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent, 2026-10-01; uji CLI + gateway lokal automations). Claude Code (simulasi agent). Pengiriman laporan ke Telegram dicoba oleh agent di gateway lokal (hasil: terkirim ke chat pemilik), belum diuji manusia di bot Telegram sungguhan. Codex dan Cursor memakai format SKILL.md yang sama; belum uji platform asli di kedua platform itu.

## FAQ
**Apakah skill ini bisa mengubah atau merusak data kasir/stok/absen saya?**
Tidak. Data dibuka dalam mode baca saja dan disalin sementara untuk dihitung. File asli tidak ditulis oleh skrip (sudah diuji otomatis).

**Saya baru memakai Kasir Lokal saja. Apakah tetap berguna?**
Ya. Bagian penjualan langsung terisi; bagian lain menulis "belum ada data" sampai alatnya dipakai. Tidak ada angka karangan.

**Kenapa nama pelanggan/prospek yang belum bayar atau belum di-follow-up tidak muncul?**
Sengaja, supaya lebih tenang bila laporan terbaca orang lain di HP Anda. Ketik "rekap pengingat" untuk tagihan, atau "follow-up hari ini"/"rekap CRM" untuk prospek — keduanya menampilkan nama dan draf pesan dari skill masing-masing (Pengingat Follow-up, CRM WA).
