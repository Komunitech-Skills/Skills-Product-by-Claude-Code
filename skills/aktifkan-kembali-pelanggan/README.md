# Ajak Pelanggan Lama Balik Belanja

**Dari daftar penjualan Anda, AI memilah pelanggan yang sudah lama diam, menghitung nilainya, dan menyiapkan 3 pesan WA yang sopan, tanpa spam dan tanpa kirim massal.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tahu siapa yang layak dihubungi dulu.** Pelanggan pasif dibagi per segmen (baru senyap, senyap, lama hilang, sangat lama) dan diurutkan dari yang nilai belanjanya terbesar. Angkanya dihitung, bukan dikira.
- ✅ **Tahu nilai yang tertinggal:** berapa pelanggan pasif dan berapa total belanja mereka dulu, plus skenario "kalau sekian persen kembali".
- ✅ **Pesan siap salin ke WhatsApp** untuk tiap segmen: pesan pertama menyapa (tidak jualan), pesan kedua menanyakan kebutuhan, pesan ketiga penutup yang sopan.
- ✅ **Jadwal 4 minggu yang aman:** maksimal 10 pesan per hari, tidak hari Minggu, dan berhenti begitu pelanggan membalas, komplain, atau minta berhenti.
- ✅ **Aman untuk nomor WA dan nama usaha:** dikirim satu per satu oleh Anda, ada opsi "stop", tanpa urgensi palsu, tanpa diskon karangan.

## Cocok untuk siapa
- Pemilik toko online, toko kue, kafe, salon, bengkel, katering, atau jasa yang punya riwayat pelanggan tetapi banyak yang tidak balik lagi
- Admin atau CS yang diminta "coba hubungi pelanggan lama" dan bingung mulai dari mana
- Pemilik usaha yang mencatat penjualan di Excel/Google Sheets dan bisa mengekspornya jadi CSV
- **Bukan untuk:** calon pelanggan yang belum pernah beli (pakai `pesan-prospek-wa`), balas keluhan (`balas-chat-cs`), atau kirim promo ke ratusan nomor sekaligus (skill ini sengaja tidak mendukungnya)

## Contoh sebelum & sesudah
**Sebelum:** Pelanggan lama dibiarkan. Kalau mau dihubungi, biasanya satu pesan seragam "Kami kangen kamu, diskon 50% hari ini saja!" yang dikirim ke semua orang, sering diabaikan atau malah dilaporkan sebagai spam.

**Sesudah (cukup ketik):** "Ini data penjualan toko saya, tolong bantu ajak pelanggan yang sudah lama nggak beli."
→ Dari 23 pelanggan di contoh data, 18 pasif dengan total belanja dulu Rp16.125.000. Anda langsung dapat daftar siapa dulu (Bu Maryam, Bu Wati, Bu Tini...), jadwal 4 minggu, dan teks pesan per segmen yang tinggal disalin. Contoh lengkap ada di `examples/`.

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.1):** rata-rata nilai 4,0 tanpa skill menjadi 8,6 dengan skill (skala 10). Rincian dan balasan utuh: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Ini ekspor penjualan saya (CSV). Siapa pelanggan yang perlu dihubungi lagi?"
- "Bikinin pesan WA buat langganan yang sudah 3 bulan nggak beli."
- "Ajak balik pelanggan lama, tapi saya nggak mau kasih diskon."

**Menyiapkan data:** simpan penjualan sebagai CSV dengan kolom nama, nomor WA, tanggal beli terakhir (hari/bulan/tahun), dan total belanja. Nama kolom boleh bervariasi. Contoh ada di `examples/data-contoh.csv`. Tidak perlu akun atau API key. Data tetap di komputer Anda.

**Tentang pengiriman:** AI hanya menyiapkan pesan dan jadwal. Anda yang mengirim, satu per satu, dari WhatsApp/Telegram Anda sendiri. Ini disengaja supaya nomor Anda aman dan pelanggan tidak merasa dispam.

## Instalasi singkat
Salin folder `aktifkan-kembali-pelanggan` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 11, 2026-10-06.
- Tanpa skill: https://t.me/c/4407409583/902/938 — skor 7
- Dengan skill: https://t.me/c/4407409583/903/940 — skor: lihat catatan gelombang
Verdik gelombang: BELUM DAPAT DINILAI — Tanpa skill sudah memberi segmen, hari senyap yang benar & 3 template WA (tanpa opsi "stop"/opt-in, tanpa jadwal); jawaban lengkap dengan skill tidak terekam di transkrip. Kirim ulang gelombang 11b (10 Okt 2026, topik berbeda, tautan tidak tercatat di log ini): 7 menjadi 8, BELUM.

## FAQ
**Bisa dipakai untuk kirim otomatis ke semua pelanggan pasif?**
Tidak, dan itu disengaja. WhatsApp bisa memblokir nomor yang mengirim pesan massal, dan pelanggan lebih merespons pesan personal. AI menyiapkan draf, jadwal harian, dan daftar siapa yang dikirim hari ini, Anda yang menekan kirim.

**Saya tidak mau kasih diskon, apakah tetap bisa?**
Bisa. Pesan pertama dan kedua memang tidak menjual, dan pesan ketiga punya versi tanpa penawaran. Penawaran hanya dimasukkan kalau Anda sendiri yang menyebut apa yang bisa diberikan, tidak pernah dikarang.

**Bagaimana kalau data penjualan saya berantakan?**
Tanggal dalam format hari/bulan/tahun, nama bulan Indonesia, nominal "Rp 1.250.000", dan pemisah titik koma dibaca otomatis. Baris yang rusak (tanggal tidak ada, nomor salah, total bukan angka) tidak dipakai dan akan disebutkan supaya Anda bisa memperbaikinya, tidak ditebak.

## Riwayat perubahan

Versi terkini: **1.0.2**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
