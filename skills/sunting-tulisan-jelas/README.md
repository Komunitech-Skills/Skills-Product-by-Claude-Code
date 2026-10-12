# Sunting Tulisan Kerja Jadi Jelas

**Tempel tulisan yang kepanjangan atau berbelit; dapat versi jelas, pendek, siap kirim, lengkap dengan angka sebelum dan sesudah.**

## Manfaat
- ✅ Email ke klien, pengumuman karyawan, deskripsi produk, pesan WA, dan laporan jadi mudah dipahami dalam sekali baca
- ✅ Inti tulisan pindah ke depan; kalimat 70 kata dipecah jadi kalimat yang masuk akal
- ✅ Kata pengisi dan jargon ("dalam rangka", "sosialisasi", "optimalisasi") diganti bahasa sehari-hari
- ✅ **Fakta tidak diubah**: angka, tanggal, harga, nama, dan janji dicocokkan satu per satu; yang meragukan diberi tanda `[cek: ...]`
- ✅ Hasil disertai angka nyata: jumlah kata, rata-rata kata per kalimat, kalimat terlalu panjang

## Cocok untuk siapa
- Pemilik usaha dan admin yang menulis email, pengumuman, atau pesan ke pelanggan dan karyawan
- Tim yang menulis panduan kerja atau laporan ke atasan
- Penjual online yang ingin deskripsi produk lebih rapi dan tidak muluk
- **Bukan untuk:** membuat surat resmi lengkap berkop (pakai `surat-resmi`), SOP dari nol (`sop-writer`), menghapus "bau AI" (`tulisan-tanpa-kesan-ai`), atau menambah klaim yang tidak ada buktinya

## Contoh sebelum & sesudah
**Sebelum (72 kata dalam satu kalimat, dari contoh email ke klien):** "Sehubungan dengan adanya pesanan kemasan kardus Bapak sebanyak 5.000 pcs ..., dengan ini kami ingin menyampaikan bahwa pada dasarnya proses produksi yang sedianya dijadwalkan selesai pada tanggal 10 Oktober 2026 dikarenakan adanya keterlambatan pengiriman bahan kertas dari pihak supplier kami maka pengerjaannya akan mengalami penyesuaian jadwal ..."

**Sesudah (cukup ketik: "Tolong rapikan email ini ke klien, kepanjangan" + tempel):** "Pengiriman kemasan kardus Bapak (PO-0412, 5.000 pcs) mundur dari 10 Oktober menjadi 17 Oktober 2026. Pemasok kertas kami terlambat mengirim bahan, sehingga produksi ikut tertunda."

Ukuran pada contoh itu: **165 kata menjadi 97**, kalimat lebih dari 25 kata **3 menjadi 0**, kata pengisi/jargon **11 menjadi 0**, semua angka dan tanggal utuh. Lima contoh lengkap ada di folder `examples/`.

## Cara pakai
Setelah terpasang, ketik permintaan biasa lalu tempel tulisannya:
- "Tolong perjelas pengumuman ini, karyawan saya banyak yang bingung."
- "Ringkas deskripsi produk ini buat Shopee."
- "Sunting email ini ke klien, tapi jangan ubah angkanya."
- "Edit for clarity: ..."

Kamu tidak perlu mengisi apa pun dulu. Pembaca dianggap pelanggan/karyawan awam dan nadanya sopan sehari-hari; kalau meleset, ketik koreksinya. Maksimal tiga pertanyaan singkat diajukan setelah hasil muncul.

## Instalasi singkat
Salin folder `sunting-tulisan-jelas` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket. Angka keterbacaan memakai Python 3 biasa (tanpa instalasi tambahan); kalau Python tidak ada, skill tetap menyunting dan menghitung perkiraan.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 14, 2026-10-12.
- Tanpa skill: https://t.me/c/4407409583/1198/1208 — skor 7
- Dengan skill: https://t.me/c/4407409583/1199/1210 — skor 7,5
Verdik gelombang: BELUM — Kedua sisi sama-sama merapikan dan menolak klaim BPOM/10.000 pelanggan/garansi tanpa bukti; dengan skill email lebih ringkas dan dibuka dengan permintaan maaf, tetapi satu angka keterbacaan (12,5 kata per kalimat, seharusnya 15,0) tidak cocok dengan teks yang diberikan.

## FAQ
**Apakah isi tulisan saya akan berubah?**
Tidak. Yang berubah susunan dan pilihan kata. Angka, tanggal, harga, nama, dan janji dicocokkan ulang; kalau ada yang meragukan atau kurang, kamu ditanya, bukan ditebak.

**Bisa dipakai untuk membuat tulisan lebih meyakinkan dengan menambah klaim?**
Tidak untuk klaim yang tidak ada buktinya (jumlah pelanggan, sertifikat, testimoni karangan). Skill ini memperjelas fakta yang kamu punya. Kalau kamu punya bukti, tambahkan, dan akan dimasukkan dengan rapi.

**Apa bedanya dengan skill "tulisan-tanpa-kesan-ai"?**
Itu menghapus ciri tulisan buatan AI. Skill ini membuat tulisan apa pun lebih jelas dan ringkas. Keduanya bisa dipakai berurutan.

## Atribusi
Prinsip menulis jelas diadaptasi dari kursus *Technical Writing One & Two* oleh Google (https://developers.google.com/tech-writing), lisensi CC BY 4.0, ditulis ulang dan diubah untuk Bahasa Indonesia dengan contoh baru. Google tidak berafiliasi dengan atau mendukung skill ini. Rincian: `ATTRIBUTION.md`.
