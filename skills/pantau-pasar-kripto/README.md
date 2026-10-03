# Pantau Kripto Tanpa Ikut Deg-Degan Pantau Layar

**Harga, berita, riset, dan jurnal trading kripto Anda -- rapi & terjadwal, tanpa satu pun rekomendasi beli/jual.**

## Manfaat
- ✅ **Notifikasi ambang otomatis** -- dikabari hanya kalau harga naik/turun sesuai batas
  yang ANDA tentukan sendiri, bukan dipantau manual tiap saat. Tidak spam: sekali sudah
  dikabari, notifikasi yang sama diredam sampai beberapa jam atau sampai kondisinya
  berubah dulu.
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

**Notifikasi otomatisnya jalan di semua komputer?**
Sudah terbukti jalan di macOS/Linux (diuji langsung terhadap OpenClaw). Untuk Windows,
langkah pembuatan jadwalnya sedikit berbeda dan belum diuji di komputer Windows
sungguhan -- kalau Anda memakai Windows, agent akan menjelaskan status ini dan mengujinya
bersama Anda dulu sebelum jadwal diaktifkan. Semua jadwal juga butuh komputer/server yang
menyala saat jam jadwalnya (dijelaskan detail saat setup).

**Sumber harganya dari mana, dan bagaimana kalau datanya gagal diambil?**
CoinGecko (`simple/price`, publik tanpa API key) dan Indodax (`ticker`, publik tanpa API
key) -- keduanya terdokumentasi resmi, lihat `references/sumber-data.md`. Kalau sumber
gagal diambil, skill memakai data cache terakhir dengan peringatan jelas (jam data +
"data basi"), dan **tidak pernah mengarang angka**. Kalau tidak ada cache sama sekali,
Anda diberi tahu apa adanya, bukan diberi angka palsu.

## Riwayat versi
- **Catatan revisi 1.0.7 (2026-10-03)** — dari uji gabungan paket solusi VIP kripto-keuangan:
  (1) saat alert dipasang, script menampilkan status **setiap** ambang — "SUDAH TERLEWATI"
  bila harga sekarang sudah melewati ambang Anda (mis. BTC sudah di bawah ambang bawah), atau
  "belum terlewati" + jaraknya; (2) angka ambang **hanya dari Anda** — AI tidak lagi memakai
  default ±5% atau mengarang ambang; koin yang hanya untuk ringkasan pagi boleh tanpa ambang;
  (3) tautan berita redirect Google News diganti URL artikel asli, atau ditandai "tautan asli
  belum didapat"; (4) bila jadwal belum bisa dipasang, AI cek sekali lalu memberi draf jadwal —
  tidak menyelidiki disk/config/gateway sendiri.
- **Catatan revisi 1.0.6 (2026-10-01)** — dari uji ulang OpenClaw: (1) **perbaikan pajak**:
  estimasi PPh final kini **hanya dihitung script jurnal** dan hanya atas **nilai transaksi
  JUAL** sesuai PMK 50/2025 (0,21% di exchange dalam negeri berizin OJK, 1% di exchange luar
  negeri; beli tidak kena PPh; PPN atas penyerahan kripto tidak dipungut sejak 1 Agustus 2025).
  Versi 1.0.5 sempat menghitung atas beli + jual (Rp48.951; benar Rp18.585 pada kasus uji) dan
  menebak pajak sudah termasuk fee — kini AI dilarang menebak dan meminta Anda mengecek kolom
  pajak di riwayat transaksi exchange; (2) setiap berita/fakta riset wajib ber-URL lengkap ke
  artikel/halaman yang dikutip (bukan beranda atau "via Google News"); (3) jam data dihitung
  ke WIB lewat script baru `scripts/jam_wib.py` (sebelumnya jam UTC pernah tertulis sebagai
  WIB, selisih 7 jam); (4) data alokasi token hanya dari sumber resmi proyek dengan tanggal
  sumber, atau dinyatakan "belum bisa dicek".
- **Catatan revisi 1.0.5 (2026-10-01)** — dari uji OpenClaw solusi VIP kripto-keuangan:
  (1) tabel harga memakai **satu mata uang acuan** untuk persen 24 jam (tidak lagi campur
  Rupiah/USD) dan selalu menyebut sumber + jam data; (2) hasil riset koin untuk chat dibuat
  ringkas (±1.500–2.500 karakter, rincian lengkap bila diminta) dan setiap sumber berupa
  tautan lengkap; (3) jurnal trading kini **menandai biaya transaksi yang janggal** (di atas
  1% nilai transaksi atau jauh berbeda dari transaksi lain, mis. fee jual 0,4% vs 0,2%) tanpa
  mengubah hitungan untung/rugi; (4) saat menolak permintaan sinyal, AI menyebut singkat bahwa
  perdagangan kripto diawasi OJK (POJK 27/2024), cara cek legalitas platform, dan kanal lapor
  Satgas PASTI / Kontak OJK 157.
