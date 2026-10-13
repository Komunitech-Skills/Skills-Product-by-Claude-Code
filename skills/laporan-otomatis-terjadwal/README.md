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
→ AI menyiapkan jadwal, menguji sekali dengan data asli, lalu setiap Senin pagi laporan seperti ini masuk sendiri ke Telegram (contoh nyata dari uji skill, kedai kopi, 62 baris transaksi seminggu):
```
*Laporan Penjualan Mingguan*
Senin 14 - Minggu 20 Sep 2026

Total omzet: Rp 2.778.000
Transaksi: 62 baris penjualan
Rata-rata omzet/hari: Rp 396.857
Hari terbaik: Minggu 20/09 (Rp 524.000)
Hari terendah: Rabu 16/09 (Rp 270.000)

*Produk terlaris*
- Matcha Latte -- 39 pcs -- Rp 858.000
- Roti Bakar Coklat -- 38 pcs -- Rp 570.000
- Croissant -- 26 pcs -- Rp 520.000

⚠️ 7 transaksi berstatus Batal tidak dihitung.
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

## Catatan revisi 1.1.9 (2026-10-13)
- Uji bot Telegram asli: balasan untuk pengguna awam masih memuat kata internal (token, Gateway, nama perintah mentah). Kini ada aturan bahasa di Format output SKILL.md: pakai "kunci akses", "bot", "jadwal", "pengaturan"; perintah teknis hanya bila diminta. Logika dan script tidak berubah.

## Catatan revisi 1.1.8 (2026-10-12)
- Uji Telegram: file CSV ada di folder pribadi pengguna (`~/laporan/masuk/...`) tetapi agent hanya mencari di folder kerja agent lalu menolak. Kini pencarian berurutan: folder yang disebut pengguna, folder kerja agent, lalu folder pribadi (`laporan/masuk`, `Dokumen/Laporan-AI/masuk`, Documents, Downloads). Bila tetap tidak ketemu, agent menampilkan contoh laporan (berlabel CONTOH) dan bertanya satu kali di mana filenya, bukan menolak.
- SKILL.md dirampingkan (checklist & batasan diringkas) agar tetap di bawah 300 baris; logika script tidak berubah.

## Catatan revisi 1.1.7 (2026-10-01)
- Uji ulang OpenClaw 2026-10-01: satu sesi mencoba kirim pesan uji Telegram tanpa "ya" lalu kehabisan waktu; sesi lain mengintip secrets/database OpenClaw. Kini ada **Aturan aksi** di awal SKILL.md: tidak ada kirim pesan (termasuk uji kirim) dan tidak ada jadwal sebelum "ya" atas ringkasan rencana (isi laporan, jam, kanal tujuan, plus satu uji kirim).
- Cek kanal hanya lewat `openclaw channels status` (perintah resmi, tidak menampilkan kredensial) atau bertanya ke pemilik; dilarang membaca file kredensial/secrets/token/`openclaw.json`/database/log OpenClaw.
- Kanal belum siap atau perintah ditolak → panduan singkat lalu berhenti, tanpa mencoba-coba; maksimal satu cek kanal per giliran agar alur ringkas dan tidak kehabisan waktu.

## Catatan revisi 1.1.6 (2026-10-01)
- Uji OpenClaw 2026-10-01: agent sempat langsung memanggil `cron.add`. Kini urutan wajib sebelum membuat jadwal (CLI maupun tool `cron.add`): cek kanal tujuan tersedia (`openclaw channels status`), tampilkan ringkasan jadwal, tunggu "ya" — "lanjut" sebelum ringkasan bukan persetujuan.
- Label hitungan penjualan diperbaiki: "57 nota / 110 pcs" (atau "N baris penjualan" bila tidak ada kolom nota), bukan "57 item". Total pcs dihitung dengan script dari hasil `rekap-penjualan-csv` (`--top 1000`).
