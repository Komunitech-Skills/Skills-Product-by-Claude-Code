# Analisis Pesaing Strategis, Tahu Cara Menang

**Peta saingan, skor berbobot, SWOT, dan kartu jawaban penjual dalam satu permintaan.**

## Manfaat
- Peta pesaing lengkap: saingan langsung, tidak langsung, dan kebiasaan pelanggan (mis. cuci sendiri)
- Matriks perbandingan rapi: layanan, harga, kanal, promo, ulasan, positioning, semua bersumber dan bertanggal
- Skor berbobot dihitung script (bukan dikira-kira) plus peta posisi teks yang menunjukkan celah pasar
- Battlecard siap pakai untuk penjual/CS: jawaban jujur saat pelanggan bilang "di sebelah lebih murah"
- Daftar 3-5 tindakan dengan pemilik, tenggat, dan ukuran berhasil, plus jadwal pantau ringan

## Cocok untuk siapa
- Pemilik usaha lokal: laundry, kuliner, salon, toko, bengkel, katering, jasa
- Penjual online yang tokonya mulai sepi dan tidak tahu sebabnya
- Pemilik yang menyiapkan tim penjualan/CS dengan jawaban seragam dan sopan

## Contoh sebelum & sesudah
**Sebelum:** Pemilik laundry kiloan hanya bilang "saingan makin banyak". Tidak tahu kenapa pelanggan pindah, dan mau menurunkan harga.
**Sesudah:** cukup ketik "Laundry kiloan saya Rp7.000/kg, ada 3 saingan yang saya tahu, saya harus apa?" Hasilnya: skor Kita 3,50 vs saingan tertinggi 3,75; ternyata harga justru keunggulan, yang kalah adalah kemudahan pesan (belum ada WA Bisnis) dan kecepatan. Tindakan: pasang WA Bisnis + katalog, tambah opsi kilat, paket langganan kos-kosan. Contoh lengkap: `examples/contoh-laundry-kiloan.md`.

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.4):** rata-rata nilai 6,8 tanpa skill menjadi 8,1 dengan skill (skala 10). Pada kasus katering nasi box, skor dihitung script (Kita 3,10, Bu Tini 3,80, Sehati 3,60) dan kemudahan pesan (selisih -1,67 dari rata-rata saingan) langsung jadi prioritas; tanpa skill, AI salah simulasi dengan mengklaim skor naik ke 3,5 sudah melewati saingan yang 3,6. Catatan jujur: keunggulan paling jelas ada di analisis itu; saat diminta mengintip akun saingan secara otomatis, AI tanpa skill pun sudah menolak dengan benar. Rincian: `examples/00-openclaw-sebelum-sesudah.md`. Codex, Claude Code, dan Cursor belum diuji langsung (format skill-nya sama).

## Cara pakai
Setelah terpasang, ketik biasa ke AI agent kamu:
- "Analisis saingan warung kopi saya, ini tiga yang saya tahu."
- "Buatkan battlecard buat admin toko saya melawan Toko X."
- "SWOT usaha katering saya dibanding katering di kecamatan sebelah."

Skill ini hanya memakai halaman publik tanpa login. Kalau AI tidak bisa membuka halaman, kamu cukup menempel teks atau screenshot. Tidak butuh API key atau akun; hitungan memakai Python bawaan (tanpa Python pun tetap jalan secara manual).

## Aturan etika (dibangun ke dalam skill)
Tanpa scraping di balik login, tanpa ulasan palsu, tanpa klaim menjatuhkan yang tidak bisa dibuktikan. Ringkasan dasar hukum (UU ITE, UU 5/1999, UU Perlindungan Konsumen, UU PDP) ada di hasil; ini bukan nasihat hukum.

## Instalasi singkat
Salin folder `analisis-pesaing-strategis` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): `CARA-INSTAL.md` / `docs/instalasi.md` di dalam paket.

## FAQ
**Apakah AI bisa mengintip data internal pesaing atau omzet mereka?**
Tidak, dan skill ini menolaknya. Hanya data publik dan pengamatan sebagai pembeli biasa. Yang belum diketahui ditulis "belum diketahui" beserta cara mencarinya.

**Kalau saya baru buka dan belum punya data pelanggan?**
Tetap bisa. Cukup sebut 3-5 usaha sejenis di sekitar kamu; skill membantu mengumpulkan data dan menandai mana yang masih kosong. Skor dengan data kurang dari 70% diberi peringatan.

**Bisa memantau pesaing otomatis tiap hari?**
Tidak. Skill ini memberi jadwal cek ulang 1-3 bulan (15 menit) dan daftar pemicu. Pantauan otomatis/terjadwal di luar cakupan.

## Atribusi
Diadaptasi dari karya berlisensi MIT (Corey Haines, Pawel Huryn), lihat `ATTRIBUTION.md`. Tidak berafiliasi dengan mereka.
