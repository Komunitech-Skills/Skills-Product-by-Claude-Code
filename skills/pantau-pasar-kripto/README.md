# Pantau Kripto Tanpa Ikut Deg-Degan Pantau Layar

**Harga, berita, riset, dan jurnal trading kripto Anda -- rapi & terjadwal. Bukan sinyal beli/jual dan tanpa janji profit.**

Diuji AI penguji independen di OpenClaw: 5,3 → 8,6 dari 10 (harga diambil dari sumber terbuka dan diperiksa skrip, tanpa sinyal beli/jual, jurnal untung/rugi cocok dengan hitungan independen; tanpa skill, berita tanpa tautan sumber dan memuat level harga, AI mengubah pengaturan OpenClaw tanpa izin, dan meminta token bot dikirim lewat chat).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Perlu koneksi internet untuk mengambil harga dan berita. Notifikasi terjadwal ke Telegram butuh OpenClaw yang tersambung ke bot Telegram Anda dan komputer/server yang menyala saat jadwal; tanpa itu, harga, riset, dan jurnal tetap bisa dipakai manual. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Notifikasi ambang otomatis** -- dikabari hanya kalau harga naik/turun sesuai batas
  yang ANDA tentukan sendiri, bukan dipantau manual tiap saat. Tidak spam: sekali sudah
  dikabari, notifikasi yang sama diredam sampai beberapa jam atau sampai kondisinya
  berubah dulu. Jadwal otomatisnya sudah diuji di OpenClaw lokal (Linux); Windows dan
  macOS belum diuji langsung.
- ✅ **Ringkasan pagi siap baca** -- harga, perubahan 24 jam, dan berita bertautan sumber,
  langsung ke Telegram Anda (WhatsApp tidak resmi: hanya dengan nomor terpisah dan
  persetujuan risiko tertulis).
- ✅ **Checklist riset proyek (DYOR, yaitu riset sendiri sebelum memutuskan)** -- fakta
  bersumber (tim, tokenomics atau pasokan dan pembagian koin, audit, status legal), bukan
  opini atau "sinyal" siapa pun.
- ✅ **Jurnal trading rapi & untung/rugi (P/L) dihitung dengan skrip** -- dari angka yang
  Anda catat sendiri (metode FIFO, yaitu yang dibeli lebih dulu dianggap dijual lebih
  dulu; sudah termasuk biaya), bukan diperkirakan.
- ✅ **Bukan bot trading** -- skill ini tidak meminta kunci API (kunci akses program ke akun) bursa (exchange) dan tidak
  menjalankan order. Keputusan beli/jual sepenuhnya di tangan Anda. Ini bukan sinyal
  beli/jual dan tanpa janji profit; risiko rugi tetap di Anda.

## Cocok untuk siapa
- Pemilik/investor kripto yang ingin dikabari perubahan harga tanpa buka aplikasi terus.
- Siapa pun yang ingin riset proyek kripto lebih sistematis sebelum memutuskan sendiri.
- Trader yang ingin jurnal rapi + hitungan untung/rugi yang dihitung dengan skrip, bukan kira-kira.
- **Bukan untuk** yang mencari bot auto-trading atau sinyal beli/jual -- skill ini justru
  menolak permintaan itu (lihat FAQ).

## Contoh sebelum & sesudah
**Sebelum:** buka aplikasi bursa kripto (exchange) berkali-kali sehari cuma untuk cek harga, lupa update
jurnal, dan susah menilai untung/rugi sebenarnya karena beli di beberapa harga berbeda.

**Sesudah (cukup ketik):** *"tolong pantau BTC, ETH sama SOL ya. kabarin kalau turun 5% atau naik 8%. terus BTC kalau di bawah 1,45 M, ETH kalau tembus 55 juta, SOL kalau di bawah 2,1 juta kabarin juga. tiap jam 7 pagi kirim ringkasan harga + berita ke telegram saya"*

Cuplikan hasil (contoh dengan data pasar nyata pada 24 Sep 2026, dipotong dari `examples/01-pantau-btc-eth-sol-ringkasan-pagi.md`; hanya contoh tampilan, bukan sinyal beli/jual, dan harga berubah setiap saat; "ambang terlewati" = harga melewati batas yang Anda tetapkan):
```
Pantau harga kripto -- 24 Sep 2026 07:41 WIB
- BTC: Rp 1.505.467.218 (-2.52% / 24 jam)
- ETH: Rp 47.945.407 (-2.78% / 24 jam)
- SOL: Rp 2.056.215 (-3.22% / 24 jam)
  >> AMBANG TERLEWATI: Harga sudah <= ambang bawah 2100000.
Sumber & jam data ada di rincian JSON. Informasi, bukan nasihat investasi.
```
Hasil lengkapnya juga memuat ringkasan pagi dengan berita bertautan sumber asli, hitungan untung/rugi jurnal yang sudah termasuk biaya, dan disclaimer "bukan nasihat investasi" di setiap keluaran.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Pantau BTC dan ETH, kabari kalau turun lebih dari 5%."
- "Kirim ringkasan harga & berita kripto tiap jam 7 pagi ke Telegram saya."
- "Riset proyek [nama koin] ini, saya mau tahu fakta-faktanya."
- "Rapikan jurnal trading saya, hitung untung/rugi bulan ini."

## Instalasi singkat
Salin folder `pantau-pasar-kripto` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw (paket solusi kripto Komunitech, lingkungan uji terpisah), 3–5 Okt 2026 (v1.0.10), skor 1–10 penguji independen (rata-rata 3 skenario): tanpa skill **5,3** → dengan skill **8,6** (LULUS). Skor berasal dari uji gabungan paket solusi kripto Komunitech (skill ini bersama skill pendamping); ringkasan per skenario ada di `examples/00-openclaw-sebelum-sesudah.md`, uji simulasi agent yang lebih awal di `examples/HASIL-UJI.md`. Tanpa skill, berita tanpa tautan sumber dan memuat level harga, AI mengubah pengaturan OpenClaw tanpa izin, dan meminta token bot dikirim lewat chat; dengan skill harga dari CoinGecko/Indodax (situs data harga kripto) diverifikasi skrip (program hitung kecil), tanpa sinyal beli/jual, jurnal FIFO cocok hitungan independen.

**Status uji (jujur):** informasi saja — **bukan** rekomendasi investasi atau bot trading. Sudah diuji di OpenClaw Gateway asli (program OpenClaw yang berjalan terus untuk menjalankan jadwal; notifikasi ambang) dan uji gabungan agent. Regulasi kripto Indonesia berubah — cek OJK (Otoritas Jasa Keuangan) dan daftar aset keuangan digital (DAKD) yang berlaku. Jadwal OpenClaw baru diuji di Linux; macOS dan Windows belum diuji di perangkat asli.

## FAQ
**Ini bot auto-trading, kan?**
Bukan. Skill ini murni memberi informasi (harga, berita, hasil riset, hitungan jurnal).
Skill ini secara sengaja **menolak** meminta/menyimpan kunci API bursa (exchange) dan tidak
mengeksekusi order -- semua keputusan beli/jual tetap Anda lakukan sendiri di aplikasi
exchange Anda.

**Kenapa tidak ada rekomendasi beli/jual atau target harga?**
Karena itu bukan tugas skill informasi. Rekomendasi investasi butuh izin & tanggung jawab
yang tidak bisa diberikan oleh AI generik, dan kesalahan sinyal = kerugian uang nyata.
Skill ini fokus pada yang bisa diperiksa: data harga dengan sumber jelas, checklist fakta
riset, dan hitungan P/L dari angka yang Anda catat sendiri. Tidak ada janji profit; risiko
rugi tetap pada Anda.

**Notifikasi otomatisnya jalan di semua komputer?**
Sudah diuji berjalan di Linux (diuji langsung terhadap OpenClaw). Untuk macOS dan Windows,
langkah pembuatan jadwalnya bisa sedikit berbeda dan belum diuji di komputer sungguhan
-- agent akan menjelaskan status ini dan mengujinya bersama Anda dulu sebelum jadwal
diaktifkan. Semua jadwal juga butuh komputer/server yang menyala saat jam jadwalnya
(dijelaskan detail saat setup).

**Sumber harganya dari mana, dan bagaimana kalau datanya gagal diambil?**
CoinGecko (`simple/price`, publik tanpa API key) dan Indodax (`ticker`, publik tanpa API
key) -- keduanya terdokumentasi resmi, lihat `references/sumber-data.md`. Kalau sumber
gagal diambil, skill memakai data cache terakhir (data tersimpan dari pengambilan
sebelumnya) dengan peringatan jelas (jam data + "data basi"), dan dirancang **tidak
mengarang angka**. Kalau tidak ada data tersimpan sama sekali, Anda diberi tahu apa
adanya, bukan diberi angka palsu.

## Riwayat perubahan

Versi terkini: **1.0.10**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
