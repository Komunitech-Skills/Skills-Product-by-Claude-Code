# Laporan Harian Otomatis Tanpa Dashboard Berbayar

**Setiap malam satu pesan Telegram (lewat OpenClaw yang menyala) berisi omzet, stok, karyawan, dan tagihan usaha Anda. Tanpa aplikasi dashboard (layar ringkasan) berlangganan, data tetap di komputer sendiri.**

Diuji AI penguji independen di OpenClaw: 6,0 → 9,0 dari 10 (angka penjualan sudah benar di kedua sisi; pembedanya: tanpa skill AI salah menyimpulkan "1 calon pembeli baru langsung jadi pembeli", tidak menyebut kasir belum ditutup, dan menyetujui mengirim omzet ke grup WA karyawan; dengan skill ada butir "Perlu Perhatian", tafsir deal dan konversi yang benar, dan penolakan kirim ke grup).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Satu pesan, seluruh usaha.** Penjualan, stok menipis, siapa yang terlambat/alpa, lembur yang perlu diputuskan, tagihan jatuh tempo, dan calon pembeli (prospek) beserta tahap penjualannya, digabung dari alat Komunitech yang sudah Anda pakai: **Kasir Lokal** (kasir), **Buku Stok** (pencatat stok), **Absensi Lokal** (catatan kehadiran), **Pengingat Follow-up** (pengingat tagihan dan tindak lanjut), dan **CRM WA** (catatan calon pembeli lewat WhatsApp).
- ✅ **Langsung kelihatan naik atau turun.** Omzet dibandingkan dengan kemarin dan hari yang sama minggu lalu dalam persen. Tiap Senin pagi ada laporan mingguan dibanding minggu sebelumnya.
- ✅ **Masalah muncul sendiri.** Selisih uang laci, stok minus, penjualan kasir yang belum masuk buku stok, absen yang belum dimasukkan, dan piutang (tagihan pelanggan yang belum dibayar) terlambat dikumpulkan di bagian "Perlu Perhatian".
- ✅ **Angka apa adanya.** Angka diambil dari data alat Anda. Bagian yang datanya belum ada ditulis "belum ada data", tidak diisi perkiraan. Rumus persen dan pembulatan tertulis jelas.
- ✅ **Dirancang aman.** Hanya membaca data (skrip tidak menulis ke data kasir/stok/absen Anda), tanpa nama pelanggan di laporan, nama karyawan bisa disamarkan, dan dikirim hanya ke chat Anda sendiri.

## Cocok untuk siapa
- Pemilik toko, warung, kafe, atau usaha jasa yang sudah memakai minimal satu alat lokal Komunitech: **Kasir Lokal**, **Buku Stok**, **Absensi Lokal**, **Pengingat Follow-up**, atau **CRM WA**. Makin banyak alat yang dipakai, makin lengkap laporannya.
- Pemilik yang jarang di toko dan ingin tahu kondisi usaha dari HP tanpa membuka banyak aplikasi.
- Anggota VIP yang memakai OpenClaw dan ingin laporan terjadwal ke Telegram.

**Kurang cocok:** usaha yang datanya ada di aplikasi lain (Moka, Majoo, Excel dari marketplace). Untuk itu pakai skill **Laporan Otomatis Terjadwal** (penjadwal laporan ke Telegram) atau **Rekap Penjualan CSV** (membaca file tabel/CSV dari aplikasi lain).

## Contoh sebelum & sesudah
**Sebelum:** tiap malam membuka rekap kasir, lalu cek stok, lalu tanya admin siapa yang tidak masuk, lalu ingat-ingat siapa yang belum bayar. Atau berlangganan aplikasi dashboard bulanan.

**Sesudah:** laporan seperti ini bisa dikirim otomatis ke Telegram (mis. tiap jam 21.00 lewat OpenClaw). Cuplikan hasil asli (dipotong; uji simulasi oleh penguji independen, 24 Sep 2026, data fiktif dari `examples/01-kafe-harian-empat-alat.md`):
```
LAPORAN HARIAN USAHA
Kamis, 24 September 2026
PENJUALAN
Omzet bersih: Rp 346.400
vs kemarin (Rab 23/9): Rp 96.000 -> naik 260,8%
STOK
- RTB Roti Bakar Srikaya: stok -5 (min 8) MINUS
KEHADIRAN
Hadir 3 dari 6 terjadwal
PERLU PERHATIAN
1. Selisih kas saat tutup kasir 2026-09-24 21:00: KURANG Rp 12.000 (seharusnya Rp 478.100, dihitung Rp 466.100).
2. Ada 1 void & 1 retur (-Rp 30.000). Cek alasannya di kasir.
```
(Void = nota dibatalkan; retur = barang dikembalikan pelanggan.) Laporan lengkap aslinya juga memuat metode bayar, menu terlaris, tagihan, dan lembur yang perlu diputuskan.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Laporan usaha hari ini"
- "Gimana usaha kemarin?"
- "Laporan minggu lalu, bandingkan dengan minggu sebelumnya"
- "Kirim laporan harian ke Telegram saya tiap jam 9 malam, dan laporan mingguan tiap Senin pagi" (OpenClaw; jadwal ke Telegram sudah dicoba di bot Telegram uji, 13 Okt 2026)
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

**Hasil uji (angka nyata):** uji OpenClaw (lingkungan uji terpisah), 1 Okt 2026 (v1.1.4), skor 1–10 penguji independen: tanpa skill **6,0** → dengan skill **9,0** (lulus acuan kami: nilai dengan skill 8 ke atas dan selisih minimal 1,5 poin). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Dua skenario: "gimana usaha hari ini?" (tanpa skill 7 → dengan skill 9) dan "pasang laporan tiap jam 9 malam, kirim juga ke grup WA karyawan" (5 → 9). Kedua sisi sama-sama memakai alat kasir dan CRM Komunitech. Tanpa skill angka penjualan benar tetapi salah menafsirkan “lead baru langsung closing” (calon pembeli baru dianggap langsung jadi pembeli), tidak menyebut kasir belum ditutup, dan siap mengirim omzet ke grup WA karyawan; dengan skill laporan baku, butir PERLU PERHATIAN jelas, deal vs konversi benar, dan menolak grup/pesan massal karena memuat selisih kas, kehadiran, dan piutang. Jujur: bila alat kasir dan CRM sudah terpasang, AI tanpa skill pun bisa menyusun rekap yang angkanya benar; pembedanya format baku, definisi yang tepat, dan kepatuhan privasi.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent, 1 Okt 2026; uji pemasangan jadwal di OpenClaw lokal). Claude Code (simulasi agent). **Kiriman terjadwal ke Telegram:** dicoba di bot Telegram uji pada 13 Okt 2026 — satu pesan laporan terjadwal tiba di grup uji sekitar 5 menit setelah jadwal dibuat, omzet Rp51.000 cocok dengan data uji (detail `examples/UJI-JADWAL-TELEGRAM-2026-10-13.md`). Yang belum diuji: alur konfirmasi "Lanjut? (ya/tidak)" lewat chat bot. Codex dan Cursor memakai format SKILL.md yang sama; belum uji platform asli di kedua platform itu.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, data fiktif) pada 17 Oktober 2026, versi 1.1.4, dengan pesan yang sama untuk kedua sisi (tanpa skill dan dengan skill): "Gimana usaha hari ini? Rekap semua dong, penjualan sama calon pembeli, dibanding kemarin naik atau turun." Data kedai kopi (nota kasir kemarin dan hari ini, serta 3 calon pembeli) sudah tersimpan di alat kasir dan alat pencatat calon pembeli Komunitech di komputer bot. Skor 1–10 dari penilai independen: tanpa skill **3,5** → dengan skill **8** (selisih +4,5), **lulus acuan kami** (dengan skill minimal 8 dan selisih minimal 1,5); pemeriksa kedua setuju.

Dengan skill, rekap diambil dari data toko sendiri dan semua angkanya benar: omzet hari ini Rp172.600 dari 4 nota, kemarin Rp179.000, jadi **turun 3,6%**; tunai Rp84.600 dan QRIS Rp88.000; terlaris Kopi Susu Gula Aren; 1 calon pembeli terlambat dihubungi lagi dan 1 kesepakatan Rp1.800.000. Bagian "perlu perhatian" mengingatkan bahwa kasir belum ditutup, dan nama serta nomor calon pembeli tidak dipajang di grup. Tanpa skill, bot tidak menemukan data kasir dan calon pembeli, lalu memakai berkas contoh yang tertinggal di folder, sehingga angkanya bukan angka toko dan tidak bisa dibandingkan dengan kemarin.

Catatan jujur: di uji ini sisi tanpa skill juga tidak memakai alat kasir dan pencatat calon pembeli; bila kedua alat itu terpasang, AI tanpa skill ini pun bisa membaca angkanya (lihat hasil uji di atas). Baris "konversi calon pembeli baru 0,0%" di samping "kesepakatan 1" masih terbaca membingungkan (kesepakatan itu dari calon pembeli lama), baris pembanding "Sabtu lalu: Rp0" tampil walau belum ada datanya, dan nama alat lain serta singkatan "CRM" (pencatat data pelanggan) ikut tersebut. Ini satu pesan uji per sisi, bukan uji berulang.

## FAQ
**Apakah skill ini bisa mengubah atau merusak data kasir/stok/absen saya?**
Tidak untuk skrip laporannya. Data dibuka dalam mode baca saja dan disalin sementara untuk dihitung. File asli tidak ditulis oleh skrip (pada uji, isi file data sama persis sebelum dan sesudah laporan dijalankan).

**Saya baru memakai Kasir Lokal saja. Apakah tetap berguna?**
Ya. Bagian penjualan langsung terisi; bagian lain menulis "belum ada data" sampai alatnya dipakai. Tidak ada angka karangan.

**Kenapa nama pelanggan/prospek yang belum bayar atau belum di-follow-up tidak muncul?**
Sengaja, supaya lebih tenang bila laporan terbaca orang lain di HP Anda. Ketik "rekap pengingat" untuk tagihan, atau "follow-up hari ini"/"rekap CRM" untuk prospek — keduanya menampilkan nama dan draf pesan dari skill masing-masing (Pengingat Follow-up, CRM WA).

## Riwayat perubahan

Versi terkini: **1.1.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
