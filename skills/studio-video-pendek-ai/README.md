# Paket Video Pendek Siap Rekam

**Satu kalimat jadi hook, naskah, teks layar, dan caption — durasi dihitung, bukan ditebak.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Hook, naskah per adegan, dan teks di layar selesai dalam hitungan menit, bukan berjam-jam.
- ✅ Durasi dihitung, bukan ditebak: naskah pas 30 detik, tidak kepanjangan.
- ✅ Shot list untuk rekam HP **atau** prompt siap tempel untuk alat video AI apa pun pilihan Anda.
- ✅ Sulih suara Bahasa Indonesia yang enak didengar, plus caption dan hashtag.
- ✅ Checklist label konten AI dan etika, supaya akun aman dan pembeli tidak merasa tertipu.

## Cocok untuk siapa
Pemilik UMKM, penjual online, kreator, admin media sosial, dan profesional yang ingin konsisten membuat TikTok/Reels/Shorts tanpa tim produksi. Tidak perlu instal apa pun.

## Contoh sebelum & sesudah
**Sebelum:** "Bingung mau ngomong apa, akhirnya video 2 menit bertele-tele dan sepi penonton."

**Sesudah (cukup ketik):** "Bikin video 30 detik keripik pisang coklat Kripis Bu Ani Rp25.000, order lewat WA, saya tidak mau tampil."
→ Durasi sulih suara **28,5 dtk** (target 30), hanya fakta dari Anda (dicek script), harga ditulis cara baca, checklist label AI ikut — tanpa klaim "stok terbatas" atau "coklat melimpah" yang tidak pernah Anda sebut. Contoh lengkap: `examples/contoh-pembuat-kopi-aren.md`.

## Cara pakai
Cukup ketik: "Bikin video 30 detik untuk [produk], harga [Rp...], jualan lewat [WA/marketplace]." Jika info kurang, skill bertanya sekali. Anda merekam/membuat video sendiri lalu mengunggah **manual** (skill tidak memposting otomatis).

## Yang tidak dilakukan (demi keamanan Anda)
Tidak meniru wajah/suara orang lain, tidak membuat testimoni palsu, tidak membuat klaim kesehatan/keuangan menyesatkan, tidak memposting otomatis. Ingin memakai klon wajah/suara **diri sendiri**? Ikuti `references/checklist-klon-diri.md`.

## Instalasi singkat
Salin folder `studio-video-pendek-ai` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket. Script hitung durasi opsional: `python3 scripts/durasi_naskah.py naskah.txt --target 30` (Windows: `python` atau `py`). Uji: `python3 tests/uji_regresi.py`.

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.0.3), skor 1–10: tanpa skill **6,5** → dengan skill **8,5** (LULUS). Keripik pisang coklat 30 dtk: durasi sulih suara **28,5 dtk** dari target 30; TANPA klaim stok terbatas/coklat melimpah yang tidak disebut pengguna. Sumber: `examples/00-openclaw-sebelum-sesudah.md`, `promosi/sebelum-sesudah.jsonl`.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-02; muat CLI). Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli. Skill tidak membuat file video — hanya rencana/naskah/prompt.

## FAQ
**Apakah skill ini membuat file videonya?** Tidak. Skill menulis rencana, naskah, dan prompt; video dibuat dengan HP Anda atau alat video AI yang Anda pilih.

**Alat AI apa yang harus dipakai?** Bebas. Prompt-nya generik dan bisa ditempel di alat teks-ke-video atau gambar-ke-video mana pun; skill tidak berafiliasi dengan merek tertentu.

**Apakah wajib memberi label AI?** Aturan TikTok, YouTube, dan Meta meminta pengungkapan untuk konten AI yang tampak nyata. Ringkasan bertanggal ada di `references/label-ai.md`; selalu cek halaman resmi platform karena aturan berubah.

Catatan: perkiraan durasi memakai 150 kata/menit (bisa diubah); ukur ulang dengan rekaman asli. Skill ini bukan nasihat hukum.
