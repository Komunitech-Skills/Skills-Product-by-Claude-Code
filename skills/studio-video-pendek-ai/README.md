# Paket Video Pendek Siap Rekam

**Satu kalimat jadi hook (kalimat pembuka 3 detik pertama), naskah, teks layar, dan caption — durasi dihitung, bukan ditebak.**

*Diuji AI penguji independen di OpenClaw: 6,5 → 8,5 dari 10 (pembeda: AI biasa menambah klaim karangan seperti "stok terbatas" dan tidak menghitung durasi, sedangkan skill hanya memakai fakta dari Anda dengan durasi sulih suara 28,5 dari 30 detik; untuk penolakan meniru wajah/suara orang lain tidak ada pembeda).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Hook, naskah per adegan, dan teks di layar selesai dalam hitungan menit, bukan berjam-jam.
- ✅ Durasi dihitung, bukan ditebak: naskah diarahkan mendekati 30 detik (perkiraan 150 kata per menit; ukur ulang dengan rekaman asli).
- ✅ Daftar adegan (shot list) untuk rekam HP **atau** perintah teks (prompt) siap tempel untuk alat video AI pilihan Anda (alat video pihak ketiga tidak ikut diuji).
- ✅ Teks sulih suara (narasi yang dibacakan) Bahasa Indonesia yang enak didengar, plus caption dan hashtag.
- ✅ Checklist label konten AI dan etika, untuk mengurangi risiko akun ditegur platform dan pembeli merasa tertipu.

## Cocok untuk siapa
Pemilik UMKM, penjual online, kreator, admin media sosial, dan profesional yang ingin konsisten membuat TikTok/Reels/Shorts tanpa tim produksi. Tidak perlu memasang aplikasi tambahan.

## Contoh sebelum & sesudah
**Sebelum:** "Bingung mau ngomong apa, akhirnya video 2 menit bertele-tele dan sepi penonton."

**Sesudah (cukup ketik):** "Bikin video 30 detik keripik pisang coklat Kripis Bu Ani Rp25.000, order lewat WA, saya tidak mau tampil."
```
**0. Asumsi & Brief**
Video 30 detik, tujuan jualan, rekam pakai HP, tanpa wajah tampil (cuma tangan/produk), gaya santai. Produk: Kripis Bu Ani, keripik pisang coklat, Rp25.000/toples, order via WA.

**2. Naskah & Timing**
| # | Waktu | Sulih suara | Teks di layar |
|---|---|---|---|
| 1 | 0-5 dtk | Keripik pisang coklat, cuma dua puluh lima ribu rupiah per toples. | KERIPIK PISANG COKLAT 25RB |
| 2 | 5-9 dtk | Kenalin, ini Kripis Bu Ani, keripik pisang rasa coklat. | KRIPIS BU ANI |
…
Perkiraan durasi sulih suara: 28,5 dtk (target 30 dtk, 150 kata/menit) — PAS.

**6. Checklist Label AI & Etika**
- [x] Tidak ada wajah/suara orang lain — hanya tangan & produk sendiri.
- [x] Unggah manual oleh kamu sendiri — tidak ada auto-post.
```
(Cuplikan hasil uji OpenClaw dengan data contoh, dipotong; `examples/00-openclaw-sebelum-sesudah.md`.) Hanya fakta dari Anda yang dipakai: tanpa klaim "stok terbatas" atau "coklat melimpah" yang tidak pernah Anda sebut.

## Cara pakai
Cukup ketik: "Bikin video 30 detik untuk [produk], harga [Rp...], jualan lewat [WA/marketplace]." Jika info kurang, skill bertanya sekali. Anda merekam/membuat video sendiri lalu mengunggah **manual** (skill tidak memposting otomatis).

## Yang tidak dilakukan (demi keamanan Anda)
Tidak meniru wajah/suara orang lain tanpa izin tertulis, tidak membuat testimoni palsu, tidak membuat klaim kesehatan/keuangan menyesatkan, tidak memposting otomatis. Klon wajah/suara hanya untuk **diri sendiri** atau orang yang memberi izin tertulis, dan kontennya wajib diberi label konten AI sesuai aturan platform. Skill ini sendiri tidak membuat klon; ia hanya menyiapkan daftar periksanya: `references/checklist-klon-diri.md`.

## Instalasi singkat
Salin folder `studio-video-pendek-ai` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket. Script hitung durasi opsional: `python3 scripts/durasi_naskah.py naskah.txt --target 30` (Windows: `python` atau `py`). Uji: `python3 tests/uji_regresi.py`.

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.0.3), skor 1–10: tanpa skill **6,5** → dengan skill **8,5** (LULUS). Keripik pisang coklat 30 dtk: durasi sulih suara **28,5 dtk** dari target 30; TANPA klaim stok terbatas/coklat melimpah yang tidak disebut pengguna. Catatan jujur: pada uji penolakan meniru wajah/suara orang lain, hasilnya sama bagusnya dengan AI tanpa skill (8 dari 10 di kedua sisi), jadi itu bukan pembeda. Sumber: `examples/00-openclaw-sebelum-sesudah.md`.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-02; muat CLI). Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli. Skill tidak membuat file video — hanya rencana/naskah/prompt; alat video AI pihak ketiga belum diuji.

## FAQ
**Apakah skill ini membuat file videonya?** Tidak. Skill menulis rencana, naskah, dan prompt; video dibuat dengan HP Anda atau alat video AI yang Anda pilih.

**Alat AI apa yang harus dipakai?** Bebas. Perintah teks (prompt)-nya generik dan bisa ditempel di alat teks-ke-video atau gambar-ke-video mana pun; skill tidak berafiliasi dengan merek tertentu.

**Apakah wajib memberi label AI?** Aturan TikTok, YouTube, dan Meta meminta pengungkapan untuk konten AI yang tampak nyata. Ringkasan bertanggal ada di `references/label-ai.md`; cek halaman resmi platform sebelum unggah karena aturan bisa berubah.

Catatan: perkiraan durasi memakai 150 kata/menit (bisa diubah); ukur ulang dengan rekaman asli. Skill ini bukan nasihat hukum.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
