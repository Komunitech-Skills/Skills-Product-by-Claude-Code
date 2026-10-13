# Persona & Positioning Usaha: Beda, Jelas, Laku

**Berhenti jualan ke semua orang: tahu siapa targetmu dan kenapa mereka beli di kamu.**

Cukup satu kalimat tentang usahamu. AI menyusun target pasar, persona pelanggan, positioning, tagline, dan teks siap tempel untuk bio, listing, caption, dan chat WhatsApp.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tahu **1 segmen** yang dikejar duluan, dengan skor yang dihitung (bukan dikira-kira).
- ✅ Persona pelanggan ala Indonesia: kota/daerah, kisaran daya beli, kanal WA/Shopee/TikTok, gaya bahasa, keberatan.
- ✅ Pembeda dari pesaing yang spesifik dan bisa dibuktikan, bukan "kualitas terbaik".
- ✅ Positioning + 5 pilihan tagline + bio IG/TikTok yang sudah dihitung karakternya.
- ✅ Tidak mengarang testimoni atau klaim berisiko; ada ceklis klaim dan uji 7 hari.

## Cocok untuk siapa
- Pemilik UMKM (fashion, kuliner, kecantikan non-klaim medis, kerajinan, jasa) yang merasa "brand saya mirip yang lain".
- Freelancer dan profesional yang mau menjelaskan keunggulannya dalam satu kalimat.
- Tim kecil yang sedang menyiapkan konten, iklan, atau rencana marketing.

## Contoh sebelum & sesudah
**Sebelum:** "Jual hijab, target semua wanita, kualitas terbaik, harga terjangkau."

**Sesudah (cukup ketik):** "Aku jual hijab buatan sendiri di Bandung, Rp 89-189 ribu, lewat Shopee dan WA. Bantu cari target dan positioning."
→ Segmen utama karyawati muda kantoran (skor 82/100), persona Sinta, tagline "Adem dipakai seharian", bio IG siap tempel, dan langkah uji 7 hari. Lihat `examples/contoh-fiktif-toko-hijab.md` (contoh fiktif).

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.5):** rata-rata nilai 6,25 tanpa skill menjadi 8,75 dengan skill (skala 10). Bio Instagram yang dibuat tanpa skill 159-219 karakter sehingga terpotong; dengan skill 142 dari 150 karakter, dihitung script. Pada permintaan tagline teh pelangsing "pasti turun 5 kg, sudah BPOM", skill menolak dengan pasal UU Perlindungan Konsumen, mengingatkan izin edar BPOM, dan memberi tagline yang aman. Rincian: `examples/00-openclaw-sebelum-sesudah.md`. Claude Code diuji lewat simulasi agent; Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Cara pakai
Ketik permintaan biasa, misalnya:
- "Bikinkan persona dan positioning untuk katering rumahan saya di Semarang."
- "Ini hasil analisis-ulasan tokoku, tolong simpulkan target dan pesan yang cocok."
- "Bedain brand saya dari kompetitor, tagline-nya apa?"
Bila info kurang, AI bertanya sekali (daftar singkat) atau memakai asumsi yang ditulis jelas.

## Skor segmen (opsional, otomatis)
Isi `templates/segmen.csv`, lalu jalankan `python3 scripts/skor_segmen.py segmen.csv` (Windows: `python` atau `py`). Tidak perlu instal apa pun; skill tetap berjalan bila script tidak bisa dijalankan.

## Instalasi singkat
Salin folder `positioning-persona-usaha` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

## FAQ
**Apakah ini riset pasar?**
Bukan. Hasilnya hipotesis terstruktur dari info kamu. Karena itu selalu ada uji 7 hari dan penanda "perlu dicek". Makin banyak data (ulasan, chat, wawancara), makin tajam.

**Perlu API key atau akun?**
Tidak. Script hanya memakai Python standar.

**Boleh dipakai untuk produk kesehatan atau kosmetik?**
Boleh untuk positioning, tetapi klaim khasiat tidak dibuatkan; kamu tetap perlu mengecek aturan BPOM dan sertifikasi halal.

## Catatan lisensi
Sebagian kerangka diadaptasi dari skill berlisensi MIT (phuryn/pm-skills dan coreyhaines31/marketingskills); rincian dan teks lisensi ada di `ATTRIBUTION.md`. Skill ini tidak berafiliasi dengan pembuat sumber.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
