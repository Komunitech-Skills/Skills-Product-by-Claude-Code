# Sunting Tulisan Kerja Jadi Jelas

**Tempel tulisan yang kepanjangan atau berbelit; dapat versi jelas, pendek, siap kirim, lengkap dengan angka sebelum dan sesudah.**

Diuji AI penguji independen di OpenClaw: 6,25 → 8,5 dari 10 (angka, tanggal, dan janji di tulisan dipertahankan, dan klaim karangan ditolak; untuk sekadar merapikan email selisihnya tipis, dan di bot Telegram asli 7 → 7,5).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Email ke klien, pengumuman karyawan, deskripsi produk, pesan WA, dan laporan jadi lebih mudah dipahami dalam sekali baca
- ✅ Inti tulisan pindah ke depan; kalimat 70 kata dipecah jadi kalimat yang masuk akal
- ✅ Kata pengisi dan jargon ("dalam rangka", "sosialisasi", "optimalisasi") diganti bahasa sehari-hari
- ✅ **Fakta dijaga**: angka, tanggal, harga, nama, dan janji dicocokkan satu per satu; yang meragukan diberi tanda `[cek: ...]` (tetap baca hasilnya sebelum dikirim)
- ✅ Hasil disertai angka ukuran: jumlah kata, rata-rata kata per kalimat, kalimat terlalu panjang (dihitung program kecil bawaan; periksa bila ada angka yang tampak janggal)

## Cocok untuk siapa
- Pemilik usaha dan admin yang menulis email, pengumuman, atau pesan ke pelanggan dan karyawan
- Tim yang menulis panduan kerja atau laporan ke atasan
- Penjual online yang ingin deskripsi produk lebih rapi dan tidak muluk
- **Bukan untuk:** membuat surat resmi lengkap berkop (pakai skill Surat Resmi, `surat-resmi`), panduan kerja (SOP) dari nol (skill SOP Writer, `sop-writer`), menghapus "bau AI" (skill Hilangkan Bau AI, `tulisan-tanpa-kesan-ai`), atau menambah klaim yang tidak ada buktinya

## Contoh sebelum & sesudah
**Sebelum (72 kata dalam satu kalimat, dari contoh email ke klien; PO = nomor pesanan pembelian):** "Sehubungan dengan adanya pesanan kemasan kardus Bapak sebanyak 5.000 pcs ..., dengan ini kami ingin menyampaikan bahwa pada dasarnya proses produksi yang sedianya dijadwalkan selesai pada tanggal 10 Oktober 2026 dikarenakan adanya keterlambatan pengiriman bahan kertas dari pihak supplier kami maka pengerjaannya akan mengalami penyesuaian jadwal ..."

**Sesudah (cukup ketik: "Tolong rapikan email ini ke klien, kepanjangan" + tempel):** "Pengiriman kemasan kardus Bapak (PO-0412, 5.000 pcs) mundur dari 10 Oktober menjadi 17 Oktober 2026. Pemasok kertas kami terlambat mengirim bahan, sehingga produksi ikut tertunda. Kami mohon pengertian Bapak."

Ukuran pada contoh itu: **165 kata menjadi 97**, kalimat lebih dari 25 kata **3 menjadi 0**, kata pengisi/jargon **11 menjadi 0**, semua angka dan tanggal utuh. Lima contoh lengkap ada di folder `examples/`.

## Cara pakai
Setelah terpasang, ketik permintaan biasa lalu tempel tulisannya:
- "Tolong perjelas pengumuman ini, karyawan saya banyak yang bingung."
- "Ringkas deskripsi produk ini buat Shopee."
- "Sunting email ini ke klien, tapi jangan ubah angkanya."
- "Edit for clarity: ..."

Anda tidak perlu mengisi apa pun dulu. Pembaca dianggap pelanggan/karyawan awam dan nadanya sopan sehari-hari; kalau meleset, ketik koreksinya. Maksimal tiga pertanyaan singkat diajukan setelah hasil muncul.

## Instalasi singkat
Salin folder `sunting-tulisan-jelas` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`). Angka keterbacaan memakai Python 3 biasa (tanpa instalasi tambahan); kalau Python tidak ada, skill tetap menyunting dan menghitung perkiraan.

**Hasil uji (angka nyata):** uji OpenClaw (uji otomatis agent), diuji pada v1.0.0 (versi terkini 1.0.1). Rata-rata nilai 6,25 tanpa skill menjadi 8,5 dengan skill (skala 10), dari dua skenario: email klien yang bertele-tele (tanpa skill 7, dengan skill 8,5; juga dijalankan dengan pengaturan kanal Telegram tanpa mengirim, nilai 8) dan permintaan yang menjebak untuk menambah klaim produk karangan (tanpa skill 5,5, dengan skill 8,5). Catatan jujur: tanpa skill pun model sudah merapikan email dengan baik (selisih pada skenario email hanya sekitar 1,5 poin); nilai jual skill ini adalah isi tetap utuh (angka, tanggal, janji) dan penolakan klaim karangan. Rincian dan balasan utuh: `examples/00-openclaw-sebelum-sesudah.md`. Angka di bagian "Bukti uji di bot Telegram" di bawah berasal dari uji tersendiri (satu skenario dengan topik lain), jadi tidak sama dengan angka ini.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent) dan sekali di bot Telegram asli (hasilnya tipis dan satu angka keterbacaan keliru, lihat bagian di bawah). Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 14, 2026-10-12.
- Tanpa skill: https://t.me/c/4407409583/1198/1208 — skor 7
- Dengan skill: https://t.me/c/4407409583/1199/1210 — skor 7,5
Verdik gelombang: BELUM — Kedua sisi sama-sama merapikan dan menolak klaim BPOM/10.000 pelanggan/garansi tanpa bukti; dengan skill email lebih ringkas dan dibuka dengan permintaan maaf, tetapi satu angka keterbacaan (12,5 kata per kalimat, seharusnya 15,0) tidak cocok dengan teks yang diberikan.

## FAQ
**Apakah isi tulisan saya akan berubah?**
Pada dasarnya tidak: yang berubah susunan dan pilihan kata. Angka, tanggal, harga, nama, dan janji dicocokkan ulang; kalau ada yang meragukan atau kurang, Anda ditanya, bukan ditebak. Tetap baca hasilnya sebelum dikirim.

**Bisa dipakai untuk membuat tulisan lebih meyakinkan dengan menambah klaim?**
Tidak untuk klaim yang tidak ada buktinya (jumlah pelanggan, sertifikat, testimoni karangan). Skill ini memperjelas fakta yang Anda punya. Kalau Anda punya bukti, tambahkan, dan akan dimasukkan dengan rapi.

**Apa bedanya dengan skill "Hilangkan Bau AI" (`tulisan-tanpa-kesan-ai`)?**
Itu menghapus ciri tulisan buatan AI. Skill ini membuat tulisan apa pun lebih jelas dan ringkas. Keduanya bisa dipakai berurutan.

## Atribusi
Prinsip menulis jelas diadaptasi dari kursus *Technical Writing One & Two* oleh Google (https://developers.google.com/tech-writing), lisensi CC BY 4.0, ditulis ulang dan diubah untuk Bahasa Indonesia dengan contoh baru. Google tidak berafiliasi dengan atau mendukung skill ini. Rincian: `ATTRIBUTION.md`.
