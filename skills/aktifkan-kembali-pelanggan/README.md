# Ajak Pelanggan Lama Balik Belanja

**Dari daftar penjualan Anda, AI memilah pelanggan yang sudah lama diam, menghitung nilainya, dan menyiapkan 3 pesan WA yang sopan, tanpa spam dan tanpa kirim massal.**

Diuji AI penguji independen di OpenClaw: 4,0 → 8,6 dari 10 (jumlah dan nilai pelanggan pasif dihitung dari data Anda, bukan ditebak, juga saat permintaan kirim massal ditolak).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tahu siapa yang layak dihubungi dulu.** Pelanggan pasif dibagi per segmen (baru senyap, senyap, lama hilang, sangat lama) dan diurutkan dari yang nilai belanjanya terbesar. Angkanya dihitung, bukan dikira.
- ✅ **Tahu nilai yang tertinggal:** berapa pelanggan pasif dan berapa total belanja mereka dulu, plus skenario "kalau sekian persen kembali".
- ✅ **Pesan siap salin ke WhatsApp** untuk tiap segmen: pesan pertama menyapa (tidak jualan), pesan kedua menanyakan kebutuhan, pesan ketiga penutup yang sopan.
- ✅ **Jadwal 4 minggu yang tertib:** maksimal 10 pesan per hari, tidak hari Minggu, dan berhenti begitu pelanggan membalas, komplain, atau minta berhenti.
- ✅ **Lebih terjaga untuk nomor WA dan nama usaha:** dikirim satu per satu oleh Anda (mengurangi, bukan menghilangkan, risiko nomor dibatasi WhatsApp), ada pilihan "stop", tanpa urgensi palsu, tanpa diskon karangan.

## Cocok untuk siapa
- Pemilik toko online, toko kue, kafe, salon, bengkel, katering, atau jasa yang punya riwayat pelanggan tetapi banyak yang tidak balik lagi
- Admin atau CS yang diminta "coba hubungi pelanggan lama" dan bingung mulai dari mana
- Pemilik usaha yang mencatat penjualan di Excel/Google Sheets dan bisa mengekspornya jadi file tabel (CSV)
- **Bukan untuk:** calon pelanggan yang belum pernah beli (pakai skill Pesan Prospek WA, `pesan-prospek-wa`), balas keluhan (skill Balas Chat CS, `balas-chat-cs`), atau kirim promo ke ratusan nomor sekaligus (skill ini sengaja tidak mendukungnya)

## Contoh sebelum & sesudah
**Sebelum:** Pelanggan lama dibiarkan. Kalau mau dihubungi, biasanya satu pesan seragam "Kami kangen kamu, diskon 50% hari ini saja!" yang dikirim ke semua orang, sering diabaikan atau malah dilaporkan sebagai spam.

**Sesudah (cukup ketik):** "Ini data penjualan toko saya, tolong bantu ajak pelanggan yang sudah lama nggak beli."
Cuplikan keluarannya (contoh dengan data fiktif, dari `examples/01-ekspor-toko-kue-normal.md`):

```
Dari 23 pelanggan di data, **18 sudah lebih dari 45 hari tidak belanja**, dan total belanja mereka dulu **Rp16.125.000**. Lima pelanggan lain masih aktif, jadi tidak perlu dihubungi.

| Segmen | Lama diam | Jumlah | Rata-rata belanja | Total belanja dulu |
|---|---|---|---|---|
| A. Baru senyap | 45-90 hari | 3 | Rp1.076.667 | Rp3.230.000 |
| B. Senyap | 91-180 hari | 7 | Rp1.048.571 | Rp7.340.000 |
| C. Lama hilang | 181-365 hari | 6 | Rp662.500 | Rp3.975.000 |
| D. Sangat lama | lebih dari 1 tahun | 2 | Rp790.000 | Rp1.580.000 |
…
**Dihubungi duluan (nilai belanja terbesar):** Bu Maryam (Rp3.050.000, 11 transaksi), Bu Wati (Rp2.300.000), Bu Tini (Rp1.900.000), Bu Sri, Mbak Lilis. Mulai dari 10 nama teratas saja dulu.
```

Disusul jadwal 4 minggu dan teks pesan 1 sampai 3 untuk tiap segmen yang tinggal disalin.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Ini ekspor penjualan saya (CSV). Siapa pelanggan yang perlu dihubungi lagi?"
- "Bikinin pesan WA buat langganan yang sudah 3 bulan nggak beli."
- "Ajak balik pelanggan lama, tapi saya nggak mau kasih diskon."

**Menyiapkan data:** simpan penjualan sebagai file tabel CSV (di Excel/Google Sheets: Simpan/Unduh sebagai CSV) dengan kolom nama, nomor WA, tanggal beli terakhir (hari/bulan/tahun), dan total belanja. Nama kolom boleh bervariasi. Contoh ada di `examples/data-contoh.csv`. Tidak perlu akun atau API key. Skill ini sendiri tidak mengirim data ke mana pun; namun data yang Anda berikan diproses oleh model AI di aplikasi agent Anda, jadi ikuti kebijakan privasi aplikasi itu.

**Tentang pengiriman:** AI hanya menyiapkan pesan dan jadwal. Anda yang mengirim, satu per satu, dari WhatsApp/Telegram Anda sendiri. Ini disengaja supaya risiko nomor Anda dibatasi lebih kecil dan pelanggan tidak merasa dispam.

## Instalasi singkat
Salin folder `aktifkan-kembali-pelanggan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket.

**Hasil uji (OpenClaw, uji otomatis agent, diuji pada v1.0.1; versi terkini 1.0.2):** rata-rata nilai 4,0 tanpa skill menjadi 8,6 dengan skill (skala 10), dari data penjualan berantakan (format tanggal campur, nomor dan total rusak) dan permintaan yang menjebak (kirim massal, "cuma hari ini"). Rincian dan balasan utuh: `examples/00-openclaw-sebelum-sesudah.md`. Diuji langsung di OpenClaw saja; Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama). Angka di bagian "Bukti uji di bot Telegram" di bawah berasal dari uji tersendiri (satu skenario dengan topik lain), jadi tidak sama dengan angka ini.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech), dua gelombang. Versi yang diuji tidak tercatat di catatan uji (versi repo saat itu: 1.0.2).

**Gelombang 11, 2026-10-06**
- Tanpa skill: (pesan di grup uji internal Komunitech) — skor 7
- Dengan skill: (pesan di grup uji internal Komunitech) — skor tidak tersedia (jawaban lengkap dengan skill tidak terekam di transkrip)
Verdik gelombang: BELUM DAPAT DINILAI — Tanpa skill sudah memberi segmen, hari senyap yang benar & 3 template WA (tanpa opsi "stop"/opt-in, tanpa jadwal); jawaban lengkap dengan skill tidak terekam di transkrip.

**Gelombang 11b (kirim ulang, topik berbeda), 2026-10-10 — verdik terakhir**
- Skor: 7 → 8 (selisih +1,0). Tautan pesan tidak tercatat di catatan uji.
Verdik gelombang: BELUM — DENGAN memberi segmen A/B/C, angka pasif, dan template WA terstruktur; TANPA sudah cukup lengkap tetapi tanpa opsi stop/opt-in dan ada dua balasan berurutan (termasuk rujukan "sama persis").

## FAQ
**Bisa dipakai untuk kirim otomatis ke semua pelanggan pasif?**
Tidak, dan itu disengaja. WhatsApp bisa memblokir nomor yang mengirim pesan massal, dan pelanggan lebih merespons pesan personal. AI menyiapkan draf, jadwal harian, dan daftar siapa yang dikirim hari ini, Anda yang menekan kirim.

**Saya tidak mau kasih diskon, apakah tetap bisa?**
Bisa. Pesan pertama dan kedua memang tidak menjual, dan pesan ketiga punya versi tanpa penawaran. Penawaran hanya dimasukkan kalau Anda sendiri yang menyebut apa yang bisa diberikan, tidak dikarang.

**Bagaimana kalau data penjualan saya berantakan?**
Tanggal dalam format hari/bulan/tahun, nama bulan Indonesia, nominal "Rp 1.250.000", dan pemisah titik koma dibaca otomatis. Baris yang rusak (tanggal tidak ada, nomor salah, total bukan angka) tidak dipakai dan akan disebutkan supaya Anda bisa memperbaikinya, tidak ditebak.

## Riwayat perubahan

Versi terkini: **1.0.2**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
