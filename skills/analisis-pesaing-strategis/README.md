# Analisis Pesaing Strategis, Tahu Cara Menang

**Peta saingan, skor berbobot, SWOT (kekuatan, kelemahan, peluang, ancaman), dan kartu jawaban penjual dalam satu permintaan.**

Diuji AI penguji independen di OpenClaw: 6,8 → 8,1 dari 10 (pembedanya skor berbobot dihitung skrip; tanpa skill, AI salah menyimpulkan bahwa skor 3,5 sudah melewati saingan yang 3,6).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- Peta pesaing lengkap: saingan langsung, tidak langsung, dan kebiasaan pelanggan (mis. cuci sendiri)
- Matriks perbandingan rapi: layanan, harga, kanal (tempat jualan), promo, ulasan, dan positioning (cara saingan memosisikan diri); tiap data diberi sumber dan tanggal, yang belum diketahui ditulis "belum diketahui"
- Skor berbobot dihitung script (bukan dikira-kira) plus peta posisi teks yang menunjukkan celah pasar
- Battlecard (kartu contekan) siap pakai untuk penjual/CS: jawaban jujur saat pelanggan bilang "di sebelah lebih murah"
- Daftar 3-5 tindakan dengan pemilik, tenggat, dan ukuran berhasil, plus jadwal pantau ringan

## Cocok untuk siapa
- Pemilik usaha lokal: laundry, kuliner, salon, toko, bengkel, katering, jasa
- Penjual online yang tokonya mulai sepi dan tidak tahu sebabnya
- Pemilik yang menyiapkan tim penjualan/CS dengan jawaban seragam dan sopan

## Contoh sebelum & sesudah
**Sebelum:** Pemilik laundry kiloan hanya bilang "saingan makin banyak". Tidak tahu kenapa pelanggan pindah, dan mau menurunkan harga.

**Sesudah (cukup ketik):** "Laundry kiloan saya di kota kecil, sekarang Rp7.000/kg, cuci-setrika 2-3 hari. Ada 3 saingan yang saya tahu. Tolong analisis, saya mau tahu harus apa."

Cuplikan hasil (dipotong; contoh fiktif dari `examples/contoh-laundry-kiloan.md`):
```
Ringkasan: Kita murah dan hasilnya bagus, tetapi kalah cepat dan sulit dipesan. Ancaman terbesar: Laundry Express 24 (cepat, pesan lewat WA, katalog rapi). Peluang terbesar: langganan bulanan untuk kos-kosan dan keluarga yang belum dilayani rapi oleh siapa pun.
| Peringkat | Toko | Skor | Data terisi | Belum diketahui |
|---|---|---|---|---|
| 1 | Laundry Express 24 | 3,75 | 100% | - |
| 2 | Kita | 3,50 | 100% | - |
| 3 | Laundry Kinclong | 3,00 | 100% | - |
| 4 | Laundry Koin Mandiri | 2,44 | 90% | Reputasi & ulasan |
Unggul dibanding rata-rata pesaing (urut prioritas = selisih x bobot)
- Harga: +1,33
- Kualitas hasil (bersih & wangi): +0,67
- Reputasi & ulasan: +0,5
Tertinggal dibanding rata-rata pesaing
- Kemudahan pesan (WA/katalog): -1
- Kecepatan (selesai & antar): -0,33
```
Hasil lengkapnya juga memuat peta pesaing, matriks perbandingan, SWOT, battlecard, dan 3-5 tindakan.

## Cara pakai
Setelah terpasang, ketik biasa ke AI agent Anda:
- "Analisis saingan warung kopi saya, ini tiga yang saya tahu."
- "Buatkan battlecard buat admin toko saya melawan Toko X."
- "SWOT usaha katering saya dibanding katering di kecamatan sebelah."

Skill ini hanya memakai halaman publik tanpa login. Kalau AI tidak bisa membuka halaman, Anda cukup menempel teks atau screenshot. Tidak butuh kunci akses (API key) atau akun; hitungan memakai Python bawaan (tanpa Python pun tetap jalan secara manual).

## Aturan etika (dibangun ke dalam skill)
Tanpa menyedot data otomatis (scraping) dari balik halaman login, tanpa ulasan palsu, tanpa klaim menjatuhkan yang tidak bisa dibuktikan. Ringkasan dasar hukum (UU ITE, UU 5/1999, UU Perlindungan Konsumen, UU PDP) ada di hasil; ini bukan nasihat hukum.

## Instalasi singkat
Salin folder `analisis-pesaing-strategis` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): `CARA-INSTAL.md` / `docs/instalasi.md` di dalam paket.

**Hasil uji (angka nyata):** satu sumber, skor 1–10.
- **Uji OpenClaw, uji otomatis agent, v1.0.4** (angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 6,8 tanpa skill menjadi 8,1 dengan skill. Pada kasus katering nasi box, skor dihitung script (Kita 3,10, Bu Tini 3,80, Sehati 3,60) dan kemudahan pesan (selisih -1,67 dari rata-rata saingan) langsung jadi prioritas; tanpa skill, AI salah simulasi dengan mengklaim skor naik ke 3,5 sudah melewati saingan yang 3,6. Catatan jujur: keunggulan paling jelas ada di analisis itu; saat diminta mengintip akun saingan secara otomatis, AI tanpa skill pun sudah menolak dengan benar.

**Status uji (jujur):** baru diuji di OpenClaw (uji otomatis agent); Codex, Claude Code, dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Apakah AI bisa mengintip data internal pesaing atau omzet mereka?**
Tidak, dan skill ini menolaknya. Hanya data publik dan pengamatan sebagai pembeli biasa. Yang belum diketahui ditulis "belum diketahui" beserta cara mencarinya.

**Kalau saya baru buka dan belum punya data pelanggan?**
Tetap bisa. Cukup sebut 3-5 usaha sejenis di sekitar Anda; skill membantu mengumpulkan data dan menandai mana yang masih kosong. Skor dengan data kurang dari 70% diberi peringatan.

**Bisa memantau pesaing otomatis tiap hari?**
Tidak. Skill ini memberi jadwal cek ulang 1-3 bulan (15 menit) dan daftar pemicu. Pantauan otomatis/terjadwal di luar cakupan.

## Atribusi
Diadaptasi dari karya berlisensi MIT (Corey Haines, Pawel Huryn), lihat `ATTRIBUTION.md`. Tidak berafiliasi dengan mereka.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
