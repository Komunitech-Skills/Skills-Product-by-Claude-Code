# Laporan Bisnis Otomatis ke HP Tiap Pagi

**Rekap penjualan, kas, stok, atau piutang -- terkirim sendiri ke Telegram/WA tanpa kamu buka Excel.**

## Manfaat
- ✅ Sekali disiapkan, laporan terkirim otomatis sesuai jadwal (harian/mingguan/bulanan)
- ✅ Angka penting di baris paling atas, siap dibaca di HP dalam 10 detik
- ✅ Angka selalu dihitung dari data asli (pakai ulang skill rekap-penjualan-csv, laporan-keuangan-emkm, arus-kas-13minggu, tagih-piutang) -- tidak pernah dikarang
- ✅ Kalau data sumber belum diekspor, kamu diberi tahu jujur -- bukan dikirimi angka nol
- ✅ Default ke Telegram (resmi, aman); WhatsApp hanya opsional dengan peringatan risiko jelas

## Cocok untuk siapa
- Pemilik usaha yang ingin tahu omzet/kas/stok tiap pagi tanpa buka laptop
- Admin yang capek membuat rekap manual tiap Senin/tanggal 1
- Siapa pun yang sudah punya file ekspor CSV rutin dari kasir, marketplace, bank, atau aplikasi stok

## Contoh sebelum & sesudah
**Sebelum:** Buka Excel tiap Senin pagi, hitung omzet manual, ketik ulang ke WA -- 30-60 menit.

**Sesudah (cukup ketik):** "Buatkan laporan penjualan otomatis tiap Senin jam 7 pagi, kirim ke Telegram saya."
→ AI menyiapkan jadwal, menguji sekali dengan data asli, lalu setiap Senin pagi laporan seperti ini masuk sendiri ke Telegram:
```
*Laporan Penjualan Harian*
2026-09-21 s/d 2026-09-22

Total omzet: Rp 469.000
Jumlah transaksi: 4
Rata-rata omzet/hari: Rp 234.500

*Produk terlaris*
- Kopi Susu -- 22 pcs -- Rp 330.000
- Roti Bakar -- 5 pcs -- Rp 75.000
- Teh Manis -- 8 pcs -- Rp 64.000
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatkan laporan penjualan otomatis tiap Senin pagi, kirim ke Telegram."
- "Kirimi saya rekap kas mingguan."
- "Ingatkan stok yang menipis tiap hari jam 7."
- "Kirim ringkasan keuangan bulanan tanggal 1."

AI akan menanyakan sumber data & tujuan kirim (maksimal 5 pertanyaan, sekali saja), menunjukkan
contoh laporan pertama, lalu mengaktifkan jadwalnya setelah kamu setuju.

**Penting:** jadwal ini hanya jalan kalau komputer/laptop tempat OpenClaw berjalan menyala saat
jam terjadwal. Panduan opsi (laptop yang biasa menyala, mini PC 24 jam, VPS, atau jasa setup
Komunitech) dijelaskan otomatis saat jadwal pertama kamu diaktifkan.

## Instalasi singkat
Salin folder `laporan-otomatis-terjadwal` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

Catatan: penjadwalan otomatis (`openclaw automations`) hanya berjalan di **OpenClaw**, karena
hanya OpenClaw yang punya Gateway yang menyala terus dan bisa mengirim pesan terjadwal ke
Telegram/WhatsApp. Di platform lain (Codex/Claude Code/Cursor), skill ini tetap bisa dipakai
untuk menghitung & menyusun laporan sekali jalan, tapi pengirimannya harus manual.

## FAQ
**Data usaha saya aman?**
Semua perhitungan jalan di komputermu sendiri. Yang keluar hanya teks laporan yang dikirim ke
Telegram/WhatsApp pilihanmu sendiri -- tidak ada data yang dikirim ke server Komunitech.

**Kalau saya lupa ekspor data minggu itu, apa laporannya kirim angka nol?**
Tidak. Skill ini selalu mengecek dulu apakah file datanya ada dan berisi. Kalau belum ada, kamu
akan diberi tahu dengan jelas apa yang perlu disiapkan -- bukan dikirimi angka nol yang salah.

**Kenapa defaultnya Telegram, bukan WhatsApp?**
OpenClaw memakai WhatsApp Web (tidak resmi, lewat scan QR), yang menurut Syarat Layanan WhatsApp
berisiko diblokir kalau dipakai mengirim pesan otomatis. Telegram memakai bot resmi tanpa risiko
itu. WhatsApp tetap bisa dipakai untuk laporan ke dirimu sendiri, di nomor terpisah, setelah kamu
membaca & menyetujui peringatan risikonya.
