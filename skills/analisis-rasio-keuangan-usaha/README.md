# Cek Kesehatan Keuangan Usaha Anda

**Kirim neraca & laba rugi, AI langsung menjawab: usaha Anda sehat, waspada, atau bahaya, dan apa yang harus diperbaiki dulu.**

*Diuji AI penguji independen di OpenClaw: 7 → 9 dari 10 pada uji ulang v1.0.5 (13 Okt 2026, skenario sama dengan uji sebelumnya; uji 1 Okt 2026 seri 8 → 8, lalu 8 → 9 setelah perbaikan v1.0.4). Pembedanya: kas dibandingkan langsung dengan utang bank yang jatuh tempo, risiko likuiditas (kemampuan membayar utang yang segera jatuh tempo) ditandai SEDANG, dan saran pertama mengurus perpanjangan utang; tanpa skill laporan menyimpulkan "aman jangka pendek".*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Rapor keuangan lengkap sekali jalan.** 15+ rasio (angka perbandingan untuk menilai kemampuan bayar tagihan, keuntungan, utang, serta perputaran stok & piutang) dihitung program hitung kecil (skrip) di komputer Anda, bukan kira-kira.
- ✅ **Dinilai sesuai jenis usaha Anda.** Warung/toko, jasa, dan produksi/kuliner punya patokan berbeda. Warung tidak dicap "bahaya" hanya karena asetnya banyak di stok.
- ✅ **Bahasa awam.** Setiap angka punya arti sehari-hari, misalnya "Dari tiap Rp 100.000 penjualan, laba bersih Rp 5.000" atau "Barang rata-rata diam di rak ±36 hari".
- ✅ **Saran tindakan yang bisa langsung dikerjakan,** diurutkan dari yang paling mendesak.
- ✅ **Siap sebelum ke bank.** Cek kesiapan angka untuk KUR (Kredit Usaha Rakyat) atau kredit lain, termasuk apakah cicilan yang direncanakan masih terkejar dibanding laba.

## Cocok untuk siapa
- Pemilik warung, toko, laundry, bengkel, katering, konveksi yang ingin tahu kondisi usahanya secara jujur.
- UMKM yang sudah punya laporan SAK EMKM (standar laporan keuangan untuk usaha kecil, misalnya dari skill Komunitech **Laporan Keuangan SAK EMKM**) dan ingin tahu "lalu artinya apa?".
- Pendamping UMKM, konsultan, atau admin keuangan yang membantu banyak usaha kecil.
- Calon peminjam KUR yang ingin tahu posisinya sebelum datang ke bank.

## Contoh sebelum & sesudah
**Sebelum:** Pemilik laundry melihat omzet naik 20% tapi uang terasa seret. Neraca ada, tapi tidak tahu harus melihat angka yang mana.

**Sesudah (cukup ketik):** "Ini angka laundry saya 2024 dan 2025, kenapa uang seret padahal omzet naik?"
Cuplikan hasil (rasio lancar = kemampuan membayar tagihan jangka pendek; DER = perbandingan utang dengan modal sendiri; prive = uang usaha yang diambil pemilik untuk pribadi; contoh buatan pembuat skill, hasil asli skrip dengan data fiktif, selengkapnya di `examples/02-laundry-tren-dua-tahun.md`):
```
Pada 2025, usaha UNTUNG Rp 23.760.000 (11,0% dari penjualan). Dari 10 rasio yang dinilai terhadap ambang usaha jasa: 4 baik, 5 waspada, 1 bahaya. Paling mendesak: Rasio lancar 0,89x.
...
| Pos / rasio | 2024 | 2025 | Perubahan terakhir |
| Rasio lancar (current ratio) | 1,30x | 0,89x | memburuk (turun) |
| DER (utang ÷ modal) | 0,70x | 1,39x | memburuk (naik) |
| Penjualan / pendapatan usaha bersih | Rp 180.000.000 | Rp 216.000.000 | membaik (naik) +20,0% |
| Laba (rugi) bersih | Rp 27.000.000 | Rp 23.760.000 | memburuk (turun) -12,0% |
...
## Saran tindakan (urut prioritas)
1. **Rasio lancar (current ratio)** — Utang jangka pendek hampir/melebihi aset lancar. Tunda pembelian aset & prive besar, negosiasikan tempo pemasok lebih panjang, tagih piutang lebih cepat, dan hindari menutup utang dengan utang baru.
```

Dalam uji perbandingan simulasi (`examples/00-pembanding-tanpa-skill.md`), AI tanpa skill memakai patokan perusahaan besar (mis. rasio cepat 1,5 untuk warung) dan menghitung di kepala. Pada uji di OpenClaw, AI biasa sudah menghitung rasio dasar dengan benar; nilai tambah skill ada di patokan sesuai jenis usaha dan skala, angka dari skrip, serta bahasa awam.

## Cara pakai
Setelah terpasang, ketik permintaan biasa ke AI agent Anda:
- "Usaha saya sehat nggak? Ini neraca dan laba rugi tahun ini."
- "Analisis laporan keuangan dari skill Laporan Keuangan SAK EMKM tadi, bandingkan dengan bulan lalu."
- "Kalau saya ambil KUR cicilan 1,5 juta per bulan, dari sisi angka aman nggak?"

Belum punya neraca? Susun dulu dengan skill **Laporan Keuangan SAK EMKM** (`laporan-keuangan-emkm`) dari buku kas, lalu minta analisis rasionya.

## Instalasi singkat
Salin folder `analisis-rasio-keuangan-usaha` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Skrip hanya butuh Python bawaan, tanpa instalasi tambahan dan tanpa akun atau API key. Kalau Python tidak ada, AI tetap bisa menghitung manual dengan rumus di `references/ambang-wajar.md` dan akan memberi tahu bahwa hasilnya belum diverifikasi skrip.

**Hasil uji (angka nyata):**
- **Uji OpenClaw, 1 Oktober 2026** (penguji AI independen; angka dari `examples/00-openclaw-sebelum-sesudah.md`, satu skenario rasio keuangan untuk bahan rapat komisaris, bagian dari uji paket Kantor & Manajemen): nilai tanpa skill 8 dan dengan skill 8, jadi seri: untuk laporan yang rapi, AI biasa sudah pandai menghitung rasio dasar. Setelah perbaikan v1.0.4, uji ulang dengan skill bernilai 9 (skala 10): skill menandai bahwa utang bank jatuh tempo ≤ 12 bulan (Rp900 juta) lebih besar dari kas (Rp420 juta), dengan seluruh angka dari skrip. Pembeda skill ada di angka yang dihitung skrip, patokan sesuai jenis dan skala usaha, serta bahasa awam.
- Uji ulang v1.0.5 (13 Okt 2026, OpenClaw 2026.10.2, penguji independen, pesan identik dengan uji pertama, angka dicek ulang dengan Python): tanpa skill **7** → dengan skill **9** (LULUS). Pembeda: kas Rp420 juta dibandingkan dengan utang bank jatuh tempo Rp900 juta → risiko likuiditas SEDANG; tanpa skill "aman jangka pendek". Asumsi jenis usaha kini tertulis jelas.

**Status uji (jujur):** diuji di OpenClaw (satu skenario, terakhir 13 Okt 2026 pada v1.0.5) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Apakah patokan "wajar" ini standar resmi bank/OJK?**
Bukan. Patokannya pedoman praktis yang disusun dari buku rujukan analisis laporan keuangan (Kasmir), contoh tolok ukur industri, dan bunga KUR yang berlaku. Semua sumber dicatat di `references/ambang-wajar.md`. Setiap bank punya penilaian internal sendiri.

**Kalau skill bilang "ANGKA CUKUP SEHAT", berarti KUR saya pasti cair?**
Tidak. Skill ini hanya membaca angka. Bank juga menilai riwayat kredit (SLIK OJK, catatan kredit Anda di OJK), karakter, agunan, legalitas, dan prospek usaha. Untuk simulasi cicilan dan daftar dokumen, pakai skill **Pengajuan KUR** (`pengajuan-kur`).

**Data saya dikirim ke mana?**
Skrip berjalan di komputer Anda sendiri dan tidak mengakses internet. Angka yang Anda tempel ke chat tetap diproses layanan AI yang Anda pakai, seperti biasa.

---
*Disclaimer: hasil analisis membantu memahami kondisi keuangan usaha. Hasil ini bukan nasihat investasi, bukan penilaian kredit, dan bukan laporan audit. Untuk keputusan besar, konsultasikan dengan akuntan atau pendamping UMKM.*

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
