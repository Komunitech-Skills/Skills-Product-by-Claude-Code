# Cek Kesehatan Keuangan Usaha dalam 1 Menit

**Kirim neraca & laba rugi, AI langsung menjawab: usaha kamu sehat, waspada, atau bahaya, dan apa yang harus diperbaiki dulu.**

## Manfaat
- ✅ **Rapor keuangan lengkap sekali jalan.** 15+ rasio (likuiditas, keuntungan, utang, perputaran stok & piutang) dihitung script dengan angka pasti, bukan kira-kira.
- ✅ **Dinilai sesuai jenis usahamu.** Warung/toko, jasa, dan produksi/kuliner punya patokan berbeda. Warung tidak dicap "bahaya" hanya karena asetnya banyak di stok.
- ✅ **Bahasa awam.** Setiap angka punya arti sehari-hari, misalnya "Dari tiap Rp 100.000 penjualan, laba bersih Rp 5.000" atau "Barang rata-rata diam di rak ±36 hari".
- ✅ **Saran tindakan yang bisa langsung dikerjakan,** diurutkan dari yang paling mendesak.
- ✅ **Siap sebelum ke bank.** Cek kesiapan angka untuk KUR/kredit, termasuk apakah cicilan yang direncanakan masih aman dibanding laba.

## Cocok untuk siapa
- Pemilik warung, toko, laundry, bengkel, katering, konveksi yang ingin tahu kondisi usahanya secara jujur.
- UMKM yang sudah punya laporan SAK EMKM (misalnya dari skill `laporan-keuangan-emkm`) dan ingin tahu "lalu artinya apa?".
- Pendamping UMKM, konsultan, atau admin keuangan yang membantu banyak usaha kecil.
- Calon peminjam KUR yang ingin tahu posisinya sebelum datang ke bank.

## Contoh sebelum & sesudah
**Sebelum:** Pemilik laundry melihat omzet naik 20% tapi uang terasa seret. Neraca ada, tapi tidak tahu harus melihat angka yang mana.

**Sesudah (cukup ketik):** "Ini angka laundry saya 2024 dan 2025, kenapa uang seret padahal omzet naik?"
→ AI menjawab dengan angka: rasio lancar turun dari 1,30 ke 0,89 (utang jangka pendek sudah melebihi aset lancar), utang dibanding modal naik dari 0,70 ke 1,39, dan laba justru turun 12%. Lalu tiga saran konkret: tunda pembelian alat dan prive besar, negosiasi tempo, jangan ambil pinjaman baru dulu. Hasil lengkap ada di `examples/02-laundry-tren-dua-tahun.md`.

Tanpa skill ini, AI biasanya memberi penjelasan umum tentang rasio, memakai patokan perusahaan besar (mis. rasio cepat 1,5 untuk warung), menghitung di kepala, dan tidak menangani modal negatif atau pembagian nol dengan benar.

## Cara pakai
Setelah terpasang, ketik permintaan biasa ke AI agent kamu:
- "Usaha saya sehat nggak? Ini neraca dan laba rugi tahun ini."
- "Analisis laporan keuangan dari laporan-keuangan-emkm tadi, bandingkan dengan bulan lalu."
- "Kalau saya ambil KUR cicilan 1,5 juta per bulan, dari sisi angka aman nggak?"

Belum punya neraca? Susun dulu dengan skill **laporan-keuangan-emkm** dari buku kas, lalu minta analisis rasionya.

## Instalasi singkat
Salin folder `analisis-rasio-keuangan-usaha` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` di dalam paket. Script hanya butuh Python bawaan, tanpa instalasi tambahan dan tanpa akun atau API key. Kalau Python tidak ada, AI tetap bisa menghitung manual dengan rumus di `references/ambang-wajar.md` dan akan memberi tahu bahwa hasilnya belum diverifikasi script.

## FAQ
**Apakah patokan "wajar" ini standar resmi bank/OJK?**
Bukan. Patokannya pedoman praktis yang disusun dari buku rujukan analisis laporan keuangan (Kasmir), contoh tolok ukur industri, dan bunga KUR yang berlaku. Semua sumber dicatat di `references/ambang-wajar.md`. Setiap bank punya penilaian internal sendiri.

**Kalau skill bilang "ANGKA CUKUP SEHAT", berarti KUR saya pasti cair?**
Tidak. Skill ini hanya membaca angka. Bank juga menilai riwayat kredit (SLIK OJK), karakter, agunan, legalitas, dan prospek usaha. Untuk simulasi cicilan dan checklist dokumen, pakai skill **pengajuan-kur**.

**Data saya dikirim ke mana?**
Tidak ke mana-mana. Script berjalan di komputermu sendiri dan tidak mengakses internet.

---
*Disclaimer: hasil analisis membantu memahami kondisi keuangan usaha. Hasil ini bukan nasihat investasi, bukan penilaian kredit, dan bukan laporan audit. Untuk keputusan besar, konsultasikan dengan akuntan atau pendamping UMKM.*

## Catatan revisi 1.0.4 (2026-10-01)
Perbaikan dari uji OpenClaw asli (bahan rapat komisaris):
- Utang bank yang jatuh tempo ≤ 12 bulan kini dicatat terpisah dan **dibandingkan langsung dengan kas**. Bila utangnya lebih besar dari kas, hasil menyebut risiko likuiditas (mis. "SEDANG") beserta alasannya, rasio kas tidak lagi hijau, dan saran pertama adalah mengurus jadwal/perpanjangan pinjaman.
- Kesimpulan likuiditas selalu bertingkat (rendah / rendah–sedang / sedang / tinggi). Tidak ada lagi kalimat "tidak ada risiko gagal bayar".
- Skala usaha (mikro/kecil/menengah/besar) dihitung dari penjualan setahun; usaha menengah ke atas memakai ambang kas & cakupan bunga yang lebih ketat.
- Jenis usaha yang dipilih AI sendiri wajib ditulis sebagai asumsi. Path script ditulis jelas; AI dilarang mencari ke seluruh disk.
