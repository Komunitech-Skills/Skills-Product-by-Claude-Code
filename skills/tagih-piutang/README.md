# Tagih Piutang Sopan, Tegas, dan Tanpa Ancaman

**Pelanggan telat bayar? Dapat pesan penagihan bertahap sampai surat teguran resmi, dengan hari keterlambatan dan denda yang dihitung skrip.**

*Diuji AI penguji independen: 6,7 → 8,3 dari 10 pada uji ulang v1.0.7, 3 skenario (pesan tagih siap kirim lengkap dengan tenggat dan surat teguran resmi, tanpa ancaman).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Pesan penagihan 6 tahap: pengingat sebelum jatuh tempo, hari H, lewat 7, 14, sampai 30 hari (surat teguran resmi)
- ✅ Hari keterlambatan, sisa tagihan, dan denda dihitung skrip, bukan dikira-kira
- ✅ Denda hanya dihitung jika memang tertulis di kontrak atau PO (surat pesanan pembelian), lengkap dengan dasar pasalnya
- ✅ Rekap umur piutang (berapa lama tiap tagihan yang belum dibayar sudah tertunggak) dari daftar tagihan dalam file CSV (tabel sederhana yang bisa dibuka di Excel): tahu siapa yang harus ditagih duluan
- ✅ Bebas ancaman dan kata-kata mempermalukan yang bisa berbalik jadi masalah hukum

## Cocok untuk siapa
- Supplier, distributor, dan grosir yang memberi tempo pembayaran ke toko atau perusahaan
- Penyedia jasa (katering langganan, desain, konsultan, kontraktor) dengan pembayaran termin
- Pemilik usaha yang sungkan menagih pelanggan lama tapi arus kasnya terganggu

## Contoh sebelum & sesudah
**Sebelum:** Sungkan menagih, pesan cuma "Pak, gimana pembayarannya?" dan tidak ada kabar selama sebulan.

**Sesudah (cukup ketik):** "Saya toko bahan kue Sumber Manis Fiktif di Medan. Ini daftar piutang reseller saya (file piutang.csv). Mana yang harus ditagih duluan? Terus buatin surat teguran buat yang paling parah. Di setiap invoice kami ada syarat tertulis 'denda 2% per bulan dari sisa tagihan, maksimal 10%' …"

*Cuplikan hasil nyata dari `examples/03-rekap-csv-reseller-dan-surat-teguran.md` (surat teguran lengkapnya dipotong):*
```
### Rekap umur piutang per 23 September 2026 – total Rp 11.000.000

| Umur | Jumlah invoice | Total |
|---|---|---|
| Belum jatuh tempo | 1 | Rp 1.800.000 |
| 1–30 hari | 1 | Rp 3.150.000 |
| 31–60 hari | 1 | Rp 2.300.000 |
| 61–90 hari | 1 | Rp 3.750.000 |
…
### Ringkasan tagihan – Toko Kue Melati Fiktif
Tagihan Rp 4.750.000 · sudah dibayar Rp 1.000.000 · **sisa Rp 3.750.000** · jatuh tempo 10 Juli 2026 · terlambat 75 hari · Tahap 6.
Denda: **Rp 225.000** = Rp 3.750.000 × 2% × 3 bulan (75 hari = 3 periode 30 hari atau bagiannya; batas maksimal 10% = Rp 375.000 tidak terlampaui). Dasar: syarat pembayaran pada Invoice INV-BK-0612 yang ditandatangani pembeli.
**Total: Rp 3.975.000.**
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Ingatkan pelanggan katering, tagihan 6,3 juta jatuh tempo Jumat ini"
- "Buat semua tahap penagihan untuk invoice INV-0801 Warung Bu Tini"
- "Ini file piutangku, urutkan mana yang harus ditagih dulu"

## Instalasi singkat
Salin folder `tagih-piutang` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** penguji AI independen, skor 1–10, di OpenClaw (uji otomatis agent, 10 Oktober 2026; angka dari `examples/00-openclaw-sebelum-sesudah.md` dan `examples/HASIL-UJI-v1.0.7-openclaw-2026-10-10.md`).
- **Uji pertama, v1.0.6, 5 skenario:** rata-rata nilai 6,4 tanpa skill menjadi 8,0 dengan skill. Contoh dari uji: 10 nota piutang toko bangunan yang berantakan menghasilkan total belum lunas Rp 157.540.000 dengan Rp 142.540.000 sudah lewat jatuh tempo (7 nota), dan nota yang sudah lunas tidak ikut ditagih. Permintaan "sebarkan ke grup dan hubungi istri atau atasan" ditolak dengan alasan hukum, lalu surat teguran yang sah tetap dibuatkan.
- **Uji ulang, v1.0.7 (versi terbaru), 3 skenario:** 6,7 menjadi 8,3.
- **Catatan jujur:** pada v1.0.6 skill kalah di satu skenario (permintaan tanpa data, hanya bertanya) dan belum mengenali kolom "sdh bayar" di file tabel; keduanya diperbaiki di v1.0.7.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent; satu skenario juga di konteks Telegram tanpa mengirim pesan nyata) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Boleh saya tambahkan denda keterlambatan?**
Boleh, jika denda itu sudah disepakati tertulis (di kontrak, PO, atau syarat invoice). Jika tidak ada, skill akan mengingatkan agar denda tidak dicantumkan.

**Bolehkah saya mengumumkan nama pelanggan yang menunggak di grup atau media sosial?**
Jangan. Itu bisa melanggar UU ITE dan UU Pelindungan Data Pribadi. Skill ini hanya membuat pesan yang ditujukan langsung ke pelanggan Anda.

**Apakah surat teguran ini sama dengan bantuan pengacara?**
Tidak. Surat ini membantu menagih secara resmi. Jika tetap tidak dibayar atau nilainya besar, konsultasikan ke advokat.

> **Catatan penting:** alat bantu menyusun pesan dan surat penagihan, bukan nasihat hukum atau keuangan dan bukan pengganti advokat. Denda hanya dihitung bila disepakati tertulis. Dasar hukum yang dirujuk (ringkasan per 23 September 2026): KUHPerdata Pasal 1238 dan 1243 (pernyataan lalai/somasi dan ganti rugi), UU ITE (UU 1/2024) Pasal 27A dan 27B, serta UU PDP (UU 27/2022). Ringkasan hukum ini belum ditinjau advokat, jadi cek ulang bila aturan berubah; sengketa atau gugatan bernilai besar sebaiknya dibawa ke advokat.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
