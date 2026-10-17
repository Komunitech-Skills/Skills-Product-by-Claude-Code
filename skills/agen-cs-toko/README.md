# Karyawan CS AI yang Hafal Isi Toko Anda

**Draf balasan pelanggan siap tempel dalam hitungan menit — Anda tetap yang memutuskan dan mengirim.**

*Diuji AI penguji independen di OpenClaw: 6,0 → 8,75 dari 10 (tanpa skill, AI menawarkan memasang balas-otomatis di WhatsApp pribadi tanpa peringatan risiko; dengan skill, ada penolakan beralasan dan mode Copilot).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Basis pengetahuan toko (kumpulan harga, stok, ongkir, retur, FAQ yang Anda tulis sekali) dipakai berulang — jawaban konsisten, tidak beda-beda tiap admin.
- ✅ Draf balasan lengkap dengan **tingkat keyakinan** dan **daftar yang perlu dicek**, jadi Anda tahu kapan harus konfirmasi manual.
- ✅ Aturan eskalasi (diteruskan ke Anda): komplain berat, refund, ancaman, data sensitif, dan pertanyaan medis/hukum ditandai untuk Anda tangani sendiri.
- ✅ Dirancang hati-hati: berusaha tidak mengarang harga/stok (yang belum ada datanya ditandai "perlu dicek admin") dan tidak mengirim pesan sendiri ke pelanggan lewat WhatsApp Web (cara memakai WhatsApp dari komputer yang bukan jalur resmi untuk bot) — mode Copilot: AI menyiapkan draf, Anda yang kirim.
- ✅ Rekap harian pertanyaan terbanyak & pertanyaan yang belum ada jawabannya, jadi FAQ Anda makin lengkap dari hari ke hari (jadwal otomatis ke Telegram belum diuji langsung).

## Cocok untuk siapa
- Pemilik toko online/offline dengan chat pelanggan yang sering menumpuk (WhatsApp, Shopee, Tokopedia).
- Klinik/praktik kecil yang ingin membalas pertanyaan jadwal & info umum lebih cepat, dengan aturan tegas: tidak memberi saran medis (aturan medisnya belum direview tenaga medis).
- Siapa pun yang sudah pakai OpenClaw dan ingin laporan CS dikirim ke Telegram tiap hari (jadwal otomatis ini belum diuji langsung).

## Contoh sebelum & sesudah
**Sebelum:** Admin membaca ulang daftar harga tiap kali ada pertanyaan, kadang lupa update stok, balasan beda gaya antar admin, dan komplain berat kadang dibalas buru-buru tanpa dicek dulu ke pemilik.

**Sesudah (cukup ketik):** "bikinin CS buat toko hijab saya dong, namanya Hijab Sakinah. harga: pashmina ceruti 89rb (8 warna), ... ini ada chat masuk: 'kak pashmina ceruti ready warna dusty pink? kalo ambil 3 bisa lebih murah gak? ongkir ke bekasi berapa'" Cuplikan hasil (`examples/01-toko-hijab-basis-pengetahuan-dan-draf.md`):
```
**Keyakinan:** Sedang
**Eskalasi:** Tidak

**Draf 1:**
Halo Kak, terima kasih sudah mampir ke Hijab Sakinah 🤍
Pashmina Ceruti harganya Rp 89.000/pcs. Kalau ambil 3, ada Paket 3 Pashmina jadi Rp 240.000
(boleh campur warna), lebih hemat Rp 27.000 dibanding beli satuan 😊
Untuk warna dusty pink, saya cek dulu stoknya ya Kak.
...
**Perlu dicek admin sebelum kirim:**
- Stok warna **dusty pink** (belum ada di basis pengetahuan).
- Ongkir ke Bekasi untuk belanja Rp 240.000 (di bawah batas gratis ongkir Rp 300.000; tarif per kota belum ada).
```
Stok warna yang belum Anda isi tidak dikarang, hanya ditandai "perlu dicek admin". Tinggal tempel ke WhatsApp/marketplace dan kirim sendiri.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Siapkan asisten CS toko saya, ini daftar harganya..."
- "Ini chat pelanggan, buatkan draf balasannya."
- "Buatkan rekap harian pertanyaan CS ke Telegram saya tiap jam 8 malam."

## Instalasi singkat
Salin folder `agen-cs-toko` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Hasil uji (angka nyata):**
- **Uji OpenClaw, 1 Oktober 2026** (penguji AI independen; angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 6,0 tanpa skill menjadi 8,75 dengan skill (skala 10), pada dua skenario (membangun CS toko hijab; komplain dengan ancaman, data KTP/rekening, dan permintaan bot WA auto-reply). Tanpa skill, agent menawarkan memasang auto-reply di nomor WA pribadi tanpa peringatan risiko; dengan skill, ada penolakan beralasan, mode Copilot, eskalasi ke pemilik, dan draf penahan.
- **Uji ulang yang meniru percakapan di Telegram (tanpa benar-benar mengirim ke Telegram), v1.0.11:** rata-rata 8,0, lulus 2 dari 3 percobaan (file yang sama). Uji di bot Telegram asli ada di bagian berikutnya.
- Catatan jujur dari uji: kadang masih muncul kalimat seperti "ready ya" pada template stok sebelum stok dicek, jadi periksa draf sebelum dikirim.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent dan bot Telegram asli) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama). Jadwal rekap otomatis ke Telegram belum diuji langsung.

## Bukti uji di bot Telegram

Uji terakhir di bot OpenClaw asli (grup uji internal Komunitech): 5 Oktober 2026, skill versi 1.0.9. Tanpa skill **4,5** → dengan skill **8,5** dari 10, selisih +4: **lulus acuan kami** (skor dengan skill minimal 8 dan selisih minimal 1,5).

Dengan skill, bot menolak membalas otomatis semua chat WhatsApp dengan alasan yang benar (WhatsApp Web bukan jalur resmi dan nomor bisa diblokir), langsung menawarkan mode Copilot (bot menyiapkan draf, Anda yang mengirim), dan menyerahkan 7 template balasan lengkap dengan aturan nada dan alur kerja admin. Tanpa skill, bot hanya bertanya balik tanpa satu template pun dan malah menawarkan memandu menyambungkan WhatsApp.

Catatan jujur: pada uji ini template cara bayar belum diberi catatan "khusus chat WhatsApp; di Shopee jangan arahkan pembayaran ke luar platform". Catatan itu baru ditambahkan di versi 1.0.10. Versi terkini (1.0.11) baru diuji dengan meniru percakapan Telegram (lihat Hasil uji di atas), belum diulang di bot asli.

## FAQ
**Apakah bot ini otomatis membalas pelanggan di WhatsApp?**
Tidak. Skill ini bekerja mode **Copilot**: bot menyiapkan draf, Anda yang menempel dan mengirim. Ini sengaja, karena WhatsApp Web bukan kanal resmi dan berisiko nomor diblokir bila dipakai kirim otomatis.

**Apakah bot bisa mengarang harga atau stok kalau saya belum isi datanya?**
Skill dirancang agar tidak. Jika info belum ada di basis pengetahuan, draf menandai bagian itu "perlu dicek admin" daripada mengira-ngira; tetap baca draf sebelum mengirim.

**Bisa dipakai untuk klinik/praktik dokter?**
Bisa, untuk info jadwal, cara daftar, dan edukasi umum. Bot dirancang **tidak** memberi diagnosis, saran dosis, atau triase — pertanyaan medis diarahkan ke dokter. Draf untuk pasien tetap dicek staf atau dokter sebelum dikirim.

## Riwayat perubahan

Versi terkini: **1.0.11**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
