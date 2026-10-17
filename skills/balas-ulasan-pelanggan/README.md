# Balas Ulasan Bintang 1 Tanpa Emosi

**Tempel ulasan pelanggan, dapat balasan yang menenangkan, sopan, dan membantu calon pembeli tetap percaya.**

*Diuji AI penguji independen: 5,5 → 8,25 dari 10 di OpenClaw (8,5 setelah perbaikan dan uji ulang); pembedanya: tanpa skill, balasan toko 924 karakter dengan klaim karangan "sudah sesuai SLA" (janji layanan) dan agen klinik menawarkan posting otomatis lewat login browser; dengan skill, balasan toko 469 karakter tercek script, dan agen klinik tidak menawarkan posting otomatis.*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Balasan untuk ulasan positif, netral, dan negatif di Shopee, Tokopedia, TikTok Shop, dan Google Maps
- ✅ Nada tenang dan tidak defensif, jadi calon pembeli melihat toko Anda bertanggung jawab
- ✅ Dicek otomatis oleh pemeriksa kecil (script) agar nomor pesanan, resi, alamat, atau nomor HP pembeli tidak ikut terpajang (tetap baca ulang sebelum diposting)
- ✅ Keluhan diarahkan ke chat pribadi, lengkap dengan pesan chat pembukanya
- ✅ Menghindari pelanggaran umum: tidak menawarkan voucher untuk mengganti bintang dan tidak mengajak pindah ke WA di marketplace (aturan tiap platform bisa berubah, cek batas terbaru di Seller Center)

## Cocok untuk siapa
- Seller marketplace yang sering dapat ulasan "barang telat" atau "paket rusak"
- Pemilik rumah makan, kafe, salon, dan bengkel yang ulasannya muncul di Google Maps
- Admin CS (layanan pelanggan) yang ingin balasan konsisten tapi tidak terasa template

## Contoh sebelum & sesudah
**Sebelum** (ilustrasi balasan yang sering terjadi, bukan hasil uji): "Kak, seharusnya baca deskripsi dulu. Pengiriman itu salah kurir, bukan salah kami." (pembeli lain ikut ilfeel)

**Sesudah (cukup ketik):** "Tolong balasin ulasan Shopee bintang 1 ini buat toko aku Rumah Alya: "Pesen gamis ukuran L yang dateng M!! Udah gitu chat seller slow respon 2 hari. Nyesel belanja di sini." Kami mau tukar ke L, ongkir retur kami yang tanggung. Admin yang pegang chat namanya Nisa."
→ Balasan publik, versi lebih singkat, pesan chat pribadi, dan hasil pengecekan. Cuplikan nyata dari uji (data fiktif):

> **Balasan publik (294 karakter):** Kak, terima kasih sudah memberi tahu, dan mohon maaf gamis yang diterima tidak sesuai ukuran pesanan serta balasan chat kami lambat. Ini bukan pengalaman yang kami harapkan untuk Kakak. Kami sudah mengirim pesan lewat chat toko untuk membantu penukaran ukuran — mohon dicek ya Kak. — Rumah Alya
>
> **Pesan chat pribadi (kirim lewat chat toko Shopee):** Halo Kak, ini Nisa dari Rumah Alya. Kami sudah membaca ulasan Kakak dan mohon maaf gamis yang datang ukuran M, padahal Kakak memesan L. Kami bantu tukar ke ukuran L, dan ongkir retur kami yang tanggung. Boleh kirimkan foto label ukuran di gamis yang diterima? Setelah itu kami kirimkan alamat retur dan kode pengirimannya. Terima kasih sudah sabar, Kak.
>
> **Hasil cek:** LULUS, 294/500 karakter, tidak ada temuan.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Bantu balas review Google Maps ini: <tempel ulasan>"
- "Balasin 5 ulasan Shopee ini sekaligus, ada yang bintang 5 dan ada yang bintang 2"
- "Bikin template balasan ulasan buat admin toko saya"

## Instalasi singkat
Salin folder `balas-ulasan-pelanggan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex (belum diuji langsung) | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor (belum diuji langsung) | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Hasil uji (angka nyata):** uji banding tanpa vs dengan skill oleh agen penguji independen (simulasi Claude Code; ulasan Shopee bintang 1 "gamis ukuran L yang datang M").
- Tanpa skill: balasan memuat 2 pelanggaran kebijakan marketplace sekaligus, yaitu mengajak ke WhatsApp lengkap dengan nomor dan meminta pembeli mengubah rating. Alasan keterlambatan ("lonjakan pesanan") dikarang dan janji ongkir retur ditulis di depan umum.
- Dengan skill: 0 pelanggaran; balasan publik 294 dari batas 500 karakter dan mengarah ke chat toko, ditambah pesan chat pribadi siap kirim dan urutan "chat pribadi dulu, baru posting balasan publik".
- Skor penguji independen: 8 dari 10 (lulus uji).
- Sumber lain, uji OpenClaw 2026-10-01 (agen penguji independen): 5,5 → 8,25 (rata-rata dua skenario ulasan, toko online dan klinik; 8,5 setelah perbaikan dan uji ulang). Versi yang diuji: skenario klinik diuji ulang pada versi 1.0.3 dan 1.0.4 (uji pertamanya sebelum itu, versinya tidak tercatat); skenario toko online tidak mencatat versi. Hanya skenario klinik yang diuji ulang, dan versi 1.0.5 (versi sekarang) belum diuji ulang di OpenClaw (lihat `examples/00-openclaw-sebelum-sesudah.md`).

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung.

**PERLU REVIEW:** aturan balasan untuk fasilitas kesehatan (klinik, praktik dokter atau dokter gigi, apotek, dan sejenisnya) belum direview tenaga medis/kepatuhan; tinjau dulu sebelum dipakai sebagai aturan final.

## FAQ
**Bolehkah menawarkan voucher supaya pembeli mengubah bintangnya?**
Tidak. Marketplace dan Google melarang imbalan untuk mengubah ulasan. Skill tetap membantu Anda memberi solusi yang tulus lewat chat pribadi, tanpa syarat ulasan.

**Bagaimana kalau ulasannya palsu atau dari pesaing?**
Skill membuat balasan yang tetap sopan dan netral, lalu menyarankan Anda melaporkan ulasan itu lewat fitur yang disediakan platform.

**Apakah balasannya diposting otomatis?**
Tidak. Anda tinggal menyalin dan menempelkannya sendiri, jadi tetap bisa dicek dulu.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
