# Studio Video Pendek AI
**Tagline:** Satu kalimat, jadi paket produksi video 15-60 detik siap rekam.

## Manfaat
- Hook, naskah per adegan, dan teks di layar selesai dalam hitungan menit, bukan berjam-jam.
- Durasi dihitung, bukan ditebak: naskah pas 30 detik, tidak kepanjangan.
- Shot list untuk rekam HP **atau** prompt siap tempel untuk alat video AI apa pun pilihan Anda.
- Sulih suara Bahasa Indonesia yang enak didengar, plus caption dan hashtag.
- Checklist label konten AI dan etika, supaya akun aman dan pembeli tidak merasa tertipu.

## Cocok untuk siapa
Pemilik UMKM, penjual online, kreator, admin media sosial, dan profesional yang ingin konsisten membuat TikTok/Reels/Shorts tanpa tim produksi. Tidak perlu instal apa pun.

## Cara pakai
Cukup ketik: "Bikin video 30 detik untuk [produk], harga [Rp...], jualan lewat [WA/marketplace]." Jika info kurang, skill bertanya sekali. Anda merekam/membuat video sendiri lalu mengunggah **manual** (skill tidak memposting otomatis).

## Sebelum / sesudah
- Sebelum: "Bingung mau ngomong apa, akhirnya video 2 menit bertele-tele dan sepi penonton."
- Sesudah: naskah 6 adegan 28 detik, hook jelas, teks di layar, caption dan checklist label. Contoh lengkap: `examples/contoh-pembuat-kopi-aren.md`. (Perbandingan tanpa skill vs dengan skill akan ditambahkan setelah uji independen.)

## Yang tidak dilakukan (demi keamanan Anda)
Tidak meniru wajah/suara orang lain, tidak membuat testimoni palsu, tidak membuat klaim kesehatan/keuangan menyesatkan, tidak memposting otomatis. Ingin memakai klon wajah/suara **diri sendiri**? Ikuti `references/checklist-klon-diri.md`.

## Instalasi singkat
Salin folder `studio-video-pendek-ai` ke folder skill platform Anda (OpenClaw, Codex, Claude Code, Cursor). Lokasi tepatnya per platform ada di `docs/instalasi.md` dalam paket. Script hitung durasi opsional: `python3 scripts/durasi_naskah.py naskah.txt --target 30` (Windows: `python` atau `py`). Uji: `python3 tests/uji_regresi.py`.

## FAQ
**Apakah skill ini membuat file videonya?** Tidak. Skill menulis rencana, naskah, dan prompt; video dibuat dengan HP Anda atau alat video AI yang Anda pilih.
**Alat AI apa yang harus dipakai?** Bebas. Prompt-nya generik dan bisa ditempel di alat teks-ke-video atau gambar-ke-video mana pun; skill tidak berafiliasi dengan merek tertentu.
**Apakah wajib memberi label AI?** Aturan TikTok, YouTube, dan Meta meminta pengungkapan untuk konten AI yang tampak nyata. Ringkasan bertanggal ada di `references/label-ai.md`; selalu cek halaman resmi platform karena aturan berubah.

Catatan: perkiraan durasi memakai 150 kata/menit (bisa diubah); ukur ulang dengan rekaman asli. Skill ini bukan nasihat hukum.
