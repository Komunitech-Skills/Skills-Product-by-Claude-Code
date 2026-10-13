# Klon Diri untuk Konten (Avatar & Suara Sendiri)
**Tagline:** Tampil konsisten di video tanpa shooting terus, aman dan berizin.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- Tahu **alat mana** yang cocok dan berapa biayanya dalam Rupiah (perbandingan bertanggal, jujur soal kekurangan).
- Hitung otomatis apakah paket cukup untuk jumlah video Anda (script, angka dihitung, bukan dikira).
- Formulir persetujuan tertulis siap pakai untuk diri sendiri maupun staf/talent.
- Panduan rekam sampel dan naskah latihan Bahasa Indonesia supaya klon terdengar natural.
- Alur konten bulanan + label AI + langkah bila Anda ditiru orang lain.

## Cocok untuk siapa
Pemilik UMKM, kreator, konsultan, dan profesional yang ingin tampil rutin di TikTok/Reels/Shorts tanpa rekam ulang tiap hari. **Bukan** untuk meniru orang lain, testimoni palsu, atau konten politik/penipuan.

## Contoh sebelum/sesudah
- Sebelum: "Harus dandan, cari cahaya, rekam 20 kali; akhirnya seminggu tidak posting."
- Sesudah: satu sesi rekam sampel, lalu tulis naskah dan render per video, ditinjau, diberi label AI, diunggah manual. Contoh: `examples/01-toko-hijab-12-video.md`. Perbandingan tanpa skill vs dengan skill: `examples/00-pembanding-tanpa-skill.md`.

## Cara pakai
Ketik: "Saya mau bikin avatar AI diri sendiri untuk [usaha], [jumlah] video/bulan, anggaran Rp[...]." Skill bertanya sekali bila info kurang.
Hitung paket: `python3 scripts/rencana_konten_avatar.py --paket paket.json --video 12 --menit 0.75 --kurs 16500 --anggaran 500000` (Windows: `python` atau `py`; format di `examples/contoh-paket.json`, angka paket isi dari halaman harga resmi). Uji: `python3 tests/uji_regresi.py`.

## Instalasi singkat
Salin folder `klon-diri-konten` ke folder skill platform Anda (OpenClaw, Codex, Claude Code, Cursor). Lokasi per platform: `docs/instalasi.md` dalam paket. Tidak butuh API key. Pasangkan dengan skill `studio-video-pendek-ai` untuk naskah.

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.0.5), skor 1–10: tanpa skill **7,75** → dengan skill **8,5** (LULUS). Contoh 12 video × 45 detik + cadangan revisi 25% = **11,25 menit**; HeyGen Creator perkiraan **Rp478.500** muat budget Rp600.000 + gerbang persetujuan & label AI. Sumber: `examples/00-openclaw-sebelum-sesudah.md`, `promosi/sebelum-sesudah.jsonl`.

**Status uji (jujur):** sudah diuji OpenClaw sebelum/sesudah otomatis (2026-10-02). Harga alat = perkiraan bertanggal (cek situs resmi). Tidak merender video; Codex/Cursor belum uji platform asli.

## FAQ
**Apakah skill membuat klon atau video?** Tidak. Skill memandu keputusan, persetujuan, rekam sampel, dan hitungan; render dilakukan di alat pilihan Anda, dan unggah dilakukan manual oleh Anda.
**Boleh klon wajah/suara karyawan atau artis?** Karyawan/talent hanya dengan persetujuan tertulis (formulir tersedia). Artis/tokoh atau siapa pun tanpa izin: tidak.
**Apakah harganya pasti?** Tidak. Harga di `references/pilihan-alat.md` adalah perkiraan bertanggal 2026-09-29; cek halaman resmi.

Skill ini tidak berafiliasi dengan HeyGen, ElevenLabs, CapCut, D-ID, Synthesia, TikTok, YouTube, Meta, atau proyek open-source yang disebut. Bukan nasihat hukum.
