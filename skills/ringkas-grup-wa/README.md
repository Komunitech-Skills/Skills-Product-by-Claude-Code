# Ringkas Grup WA, Langsung Tahu Mana yang Perlu Dibalas

**Kirim ekspor chat grup, dalam semenit tahu mana yang perlu ditanggapi — tanpa scroll ratusan pesan.**

## Manfaat
- ✅ Memilah otomatis: **Perlu Perhatian** (pertanyaan ke Anda, keputusan, tenggat, uang, komplain) vs **Info** vs **Obrolan**.
- ✅ **Daftar tindakan** siap tindak lanjut: siapa mengerjakan apa, kapan tenggatnya.
- ✅ **Kutipan asli + jam** untuk tiap poin penting, jadi mudah dicek langsung di grup — tidak ada isi yang dikarang.
- ✅ Grup ramai (ratusan pesan/hari)? Otomatis dipilah **per hari**.
- ✅ Bisa **menyamarkan nama & nomor** anggota kalau isinya sensitif, sebelum diproses AI (upaya terbaik — AI agent Anda akan menyebutkan bila ada kata yang perlu dicek manual sebelum dibagikan).
- ✅ 100% dari fitur **ekspor chat resmi WhatsApp** — tidak ada nomor bot, tidak ada risiko blokir, tidak ada yang "mendengar" grup Anda diam-diam.

## Cocok untuk siapa
- Pemilik usaha/tim yang ikut banyak grup kerja, proyek, atau komunitas dan sering ketinggalan info penting.
- Ketua RT/komunitas/organisasi yang perlu ringkasan diskusi grup untuk rapat berikutnya.
- Siapa pun yang baru buka HP setelah lama offline dan grup sudah ratusan pesan.

**Bukan untuk:** memantau chat/grup orang lain tanpa izin mereka (mis. menyadap karyawan atau pasangan) — skill ini menolak permintaan seperti itu.

## Contoh sebelum & sesudah
**Sebelum:** scroll manual 200+ pesan grup toko, khawatir kelewat pertanyaan penting soal pembayaran supplier atau perubahan harga.

**Sesudah (cukup ketik):** "Ringkas grup toko dari file ekspor ini, yang perlu saya tanggapi aja."
→ Dalam beberapa detik dapat daftar 2 hal yang butuh keputusan Anda (lengkap kutipan & jam), daftar tugas siapa-kapan, dan sisanya cukup dihitung sebagai info/obrolan.

## Cara pakai

### 1. Ekspor chat dari WhatsApp (sekali per ringkasan, ±30 detik)

**Di Android:**
1. Buka grup WA yang mau diringkas.
2. Ketuk ⋮ (titik tiga di pojok kanan atas) → **Lainnya** → **Ekspor chat**.
3. Pilih **"Tanpa Media"** (lebih cepat & filenya kecil).
4. Kirim file `.zip`/`.txt` yang muncul ke chat AI agent Anda, atau simpan ke folder yang bisa diakses AI agent (mis. folder Unduhan).

**Di iPhone:**
1. Buka grup WA yang mau diringkas.
2. Ketuk nama grup di atas → gulir ke bawah → **Ekspor Chat**.
3. Pilih **"Tanpa Media"**.
4. Pilih cara kirim (mis. simpan ke Files, kirim ke email/AirDrop ke komputer, atau ke chat AI agent Anda bila didukung).

### 2. Minta diringkas

Cukup ketik ke AI agent Anda, misalnya:
- "Ringkas grup ini, yang perlu saya tanggapi aja."
- "Rekap grup kerja 3 hari terakhir."
- "Apa yang saya lewatkan di grup sejak kemarin jam 5 sore?"

Kalau grup sangat sensitif (ada anggota keluarga/pelanggan/pasien), tambahkan: "samarkan nama anggotanya" — nama & nomor akan diganti "Anggota 1, Anggota 2, ..." sebelum diproses.

## Instalasi singkat
Salin folder `ringkas-grup-wa` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ

**Apakah skill ini bisa memantau grup secara langsung/otomatis, bukan cuma dari file ekspor?**
Bisa, tapi itu jalur terpisah yang lebih rumit (bot dengan nomor WhatsApp khusus ikut masuk ke grup) dan **wajib** diberitahukan ke anggota grup. Jalur file ekspor (bawaan skill ini) jauh lebih sederhana, tanpa risiko nomor diblokir, dan cocok untuk hampir semua kebutuhan. Tanyakan ke AI agent Anda kalau memang butuh mode langsung — ada panduannya, tapi disarankan hanya untuk pengguna yang sudah nyaman dengan konfigurasi teknis atau lewat jasa pendampingan.

**Apakah isi chat saya dikirim ke server Komunitech?**
Tidak. Skill ini berjalan di komputer/AI agent Anda sendiri. File ekspor diproses secara lokal oleh script Python, lalu ringkasannya diproses oleh penyedia AI yang Anda pakai (mis. Anthropic/OpenAI) — sama seperti percakapan biasa dengan AI agent Anda.

**Kalau grup sangat aktif (ribuan pesan sebulan), apakah tetap bisa dipakai?**
Bisa. Minta rentang waktu tertentu (mis. "3 hari terakhir" atau "sejak kemarin sore") supaya hasilnya tetap ringkas dan relevan; untuk grup sangat ramai, hasil otomatis dipecah per hari.

## Catatan revisi 1.0.5 (2026-10-01)
- Temuan uji ulang OpenClaw: jumlah butir salah hitung ("(6)" padahal 5; "tiga lainnya" padahal 4) dan pelanggan tertulis "vendor".
- Kini jumlah butir wajib dihitung ulang dari daftar final / keluaran script, dan peran pihak disalin dari chat.

## Catatan revisi 1.0.4 (2026-10-01)
Perbaikan dari uji OpenClaw asli (ringkasan grup WA gudang):
- Tenggat yang sudah lewat kini ditandai **"⏰ LEWAT TENGGAT — cek status"**. Script membaca tanggal di pesan (29/9, 5 Okt, hari ini/besok/lusa, nama hari) dan membandingkannya dengan tanggal hari ini; rencana yang tanggalnya sudah lewat tidak lagi ditulis "sudah beres".
- Ringkasan menyebut tanggal chat terakhir dan tanggal hari ini.
- Path script ditulis jelas (subfolder `scripts/`); AI dilarang mencari file ke seluruh disk.
