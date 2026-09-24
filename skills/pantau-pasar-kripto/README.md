# Pantau Kripto Tanpa Ikut Deg-Degan Pantau Layar

**Harga, berita, riset, dan jurnal trading kripto Anda -- rapi & terjadwal, tanpa satu pun rekomendasi beli/jual.**

## Manfaat
- ✅ **Notifikasi ambang otomatis** -- dikabari hanya kalau harga naik/turun sesuai batas
  yang ANDA tentukan sendiri, bukan dipantau manual tiap saat.
- ✅ **Ringkasan pagi siap baca** -- harga, perubahan 24 jam, dan berita bertautan sumber,
  langsung ke Telegram/WhatsApp Anda.
- ✅ **Checklist riset proyek (DYOR)** -- fakta bersumber (tim, tokenomics, audit, status
  legal), bukan opini atau "sinyal" siapa pun.
- ✅ **Jurnal trading rapi & P/L dihitung pasti** -- untung/rugi dihitung dari angka yang
  Anda catat sendiri (metode FIFO, sudah termasuk biaya), bukan diperkirakan.
- ✅ **Aman dari risiko bot trading** -- tidak pernah minta API key exchange, tidak pernah
  mengeksekusi order. Keputusan tetap 100% di tangan Anda.

## Cocok untuk siapa
- Pemilik/investor kripto yang ingin dikabari perubahan harga tanpa buka aplikasi terus.
- Siapa pun yang ingin riset proyek kripto lebih sistematis sebelum memutuskan sendiri.
- Trader yang ingin jurnal rapi + hitungan untung/rugi yang bisa dipercaya, bukan kira-kira.
- **Bukan untuk** yang mencari bot auto-trading atau sinyal beli/jual -- skill ini justru
  menolak permintaan itu (lihat FAQ).

## Contoh sebelum & sesudah
**Sebelum:** buka aplikasi exchange berkali-kali sehari cuma untuk cek harga, lupa update
jurnal, dan susah menilai untung/rugi sebenarnya karena beli di beberapa harga berbeda.

**Sesudah (cukup ketik):** *"Pantau BTC dan ETH, kabari kalau turun lebih dari 5%, kirim
ringkasan pagi jam 7 ke Telegram, dan rapikan jurnal trading saya."*
→ Dapat notifikasi otomatis hanya saat ambang terlewati (dengan sumber & jam data jelas),
ringkasan pagi dengan berita bertautan, dan hasil hitung P/L jurnal yang sudah termasuk
biaya transaksi -- semua dengan disclaimer "bukan nasihat investasi" di setiap keluaran.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Pantau BTC dan ETH, kabari kalau turun lebih dari 5%."
- "Kirim ringkasan harga & berita kripto tiap jam 7 pagi ke Telegram saya."
- "Riset proyek [nama koin] ini, saya mau tahu fakta-faktanya."
- "Rapikan jurnal trading saya, hitung untung/rugi bulan ini."

## Instalasi singkat
Salin folder `pantau-pasar-kripto` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Ini bot auto-trading, kan?**
Bukan. Skill ini murni memberi informasi (harga, berita, hasil riset, hitungan jurnal).
Skill ini secara sengaja **menolak** meminta/menyimpan API key exchange dan tidak pernah
mengeksekusi order -- semua keputusan beli/jual tetap Anda lakukan sendiri di aplikasi
exchange Anda.

**Kenapa tidak ada rekomendasi beli/jual atau target harga?**
Karena itu bukan tugas skill informasi. Rekomendasi investasi butuh izin & tanggung jawab
yang tidak bisa diberikan oleh AI generik, dan kesalahan sinyal = kerugian uang nyata.
Skill ini fokus pada yang bisa dipastikan: data harga dengan sumber jelas, checklist fakta
riset, dan hitungan P/L dari angka yang Anda catat sendiri.

**Sumber harganya dari mana, dan bagaimana kalau datanya gagal diambil?**
CoinGecko (`simple/price`, publik tanpa API key) dan Indodax (`ticker`, publik tanpa API
key) -- keduanya terdokumentasi resmi, lihat `references/sumber-data.md`. Kalau sumber
gagal diambil, skill memakai data cache terakhir dengan peringatan jelas (jam data +
"data basi"), dan **tidak pernah mengarang angka**. Kalau tidak ada cache sama sekali,
Anda diberi tahu apa adanya, bukan diberi angka palsu.
