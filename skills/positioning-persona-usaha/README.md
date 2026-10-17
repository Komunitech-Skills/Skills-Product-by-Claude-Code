# Persona & Positioning Usaha: Beda, Jelas, Laku

**Berhenti jualan ke semua orang: tahu siapa target Anda dan kenapa mereka memilih usaha Anda.**

Cukup satu kalimat tentang usaha Anda. AI menyusun target pasar, persona pelanggan (gambaran satu pelanggan ideal lengkap dengan kebiasaannya), positioning (posisi usaha Anda di benak pelanggan: apa bedanya dan untuk siapa), tagline, dan teks siap tempel untuk bio, listing (halaman produk di marketplace), caption, dan chat WhatsApp.

Diuji AI penguji independen di OpenClaw: 6,25 → 8,75 dari 10 (pembedanya bio Instagram yang dihitung karakternya agar pas 150 karakter, dan tagline yang menjanjikan "pasti turun 5 kg, sudah BPOM" ditolak dengan dasar hukum lalu diganti tagline yang aman).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tahu **1 segmen** (kelompok pembeli) yang dikejar duluan, dengan skor yang dihitung (bukan dikira-kira).
- ✅ Persona pelanggan ala Indonesia: kota/daerah, kisaran daya beli, kanal WA/Shopee/TikTok, gaya bahasa, keberatan.
- ✅ Pembeda dari pesaing yang spesifik dan bisa dibuktikan, bukan "kualitas terbaik".
- ✅ Positioning + 5 pilihan tagline + bio IG/TikTok yang sudah dihitung karakternya.
- ✅ Tidak membuatkan testimoni palsu dan menolak klaim berisiko (mis. janji khasiat); ada ceklis klaim dan uji 7 hari.

## Cocok untuk siapa
- Pemilik UMKM (fashion, kuliner, kecantikan non-klaim medis, kerajinan, jasa) yang merasa "brand saya mirip yang lain".
- Freelancer dan profesional yang mau menjelaskan keunggulannya dalam satu kalimat.
- Tim kecil yang sedang menyiapkan konten, iklan, atau rencana marketing.

## Contoh sebelum & sesudah
**Sebelum:** "Jual katering rumahan, target semua orang, masakan enak, harga terjangkau."

**Sesudah (cukup ketik):** "Aku jualan rantangan/katering harian rumahan di Semarang, daerah Tembalang & Banyumanik. Harga Rp 27 ribu per porsi, paket langganan 5 hari Rp 125 ribu. Pesan lewat WA, antar sendiri jam 10-11 siang. Pembeli sekarang kebanyakan karyawan dan anak kos yang kerja. Pesaing: warteg, GoFood/GrabFood, katering lain di grup FB. Nama usaha Rantang Bu Wulan. Tolong bikin persona dan positioning."

Cuplikan balasan (usaha fiktif; dari `examples/01-uji-katering-rantang-semarang.md`; contoh lain: `examples/contoh-fiktif-toko-hijab.md`):
```
Ringkasan 5 baris
- Segmen utama 90 hari: Karyawan perantau & anak kos yang kerja (skor 79,0/100). Segmen kedua yang hampir setara: keluarga muda suami-istri bekerja (78,0) — diuji kecil, tidak dikejar dulu.
- Persona: Dimas, 26, staf admin gudang di Banyumanik, asal Pati, ngekos.
- Positioning: makan siang rumahan yang diantar tiap hari kerja, supaya tidak perlu mikir menu dan tidak boros ongkir aplikasi.
- Tagline rekomendasi: "Makan rumahan, tanpa mikir menu."
- Langkah pertama: tanya 5 pelanggan langganan lewat WA (pertanyaan di bagian 8), lalu uji 2 tagline di status WA 3 hari.
```
Balasan lengkapnya memuat tabel skor segmen, persona, pembeda dari pesaing, pilihan tagline, dan teks siap tempel.

## Cara pakai
Ketik permintaan biasa, misalnya:
- "Bikinkan persona dan positioning untuk katering rumahan saya di Semarang."
- "Ini hasil analisis ulasan tokoku (dari skill Analisis Ulasan), tolong simpulkan target dan pesan yang cocok."
- "Bedain brand saya dari kompetitor, tagline-nya apa?"
Bila info kurang, AI bertanya sekali (daftar singkat) atau memakai asumsi yang ditulis jelas. Skor segmen dihitung otomatis oleh skrip bawaan (cara menjalankannya sendiri ada di bagian Instalasi).

## Instalasi singkat
Salin folder `positioning-persona-usaha` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

Skor segmen otomatis (opsional): isi `templates/segmen.csv`, lalu jalankan `python3 scripts/skor_segmen.py segmen.csv` (Windows: `python` atau `py`). Tidak perlu instal apa pun; skill tetap berjalan bila skrip tidak bisa dijalankan.

**Hasil uji (angka nyata):**
- **Uji OpenClaw, uji otomatis agent, v1.0.5** (angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 6,25 tanpa skill menjadi 8,75 dengan skill. Bio Instagram yang dibuat tanpa skill 159-219 karakter sehingga terpotong; dengan skill 142 dari 150 karakter, dihitung script. Pada permintaan tagline teh pelangsing "pasti turun 5 kg, sudah BPOM", skill menolak dengan pasal UU Perlindungan Konsumen, mengingatkan izin edar BPOM, dan memberi tagline yang aman.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent dan satu pesan di bot OpenClaw asli, Telegram, 16 Okt 2026) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech) pada 16 Okt 2026, skill versi 1.0.6. Pesan yang sama dikirim ke dua kondisi, tanpa skill dan dengan skill: pemilik katering rantangan harian rumahan di Semarang (daerah Tembalang dan Banyumanik) dengan harga Rp27 ribu per porsi, paket langganan 5 hari Rp125 ribu, pesan lewat WA, antar sendiri jam 10–11 siang, minta persona dan positioning. Skor 1–10 dari penilai independen: tanpa skill **5** → dengan skill **8,5** (selisih +3,5, lulus acuan kami). Hanya versi dengan skill yang memilih satu target utama (karyawan kantoran, skor 86 lawan 82 untuk anak kos yang bekerja), membuat tokoh pembeli lengkap dengan pemicu dan keberatannya, memberi bio WhatsApp 100 karakter dan judul grup Facebook yang siap tempel, tidak mengarang klaim "higienis", dan mengingatkan untuk cek izin ke Dinas Kesehatan. Versi tanpa skill mengarang klaim "lebih higienis", "menu konsisten", dan "tanpa ongkir dan biaya aplikasi" yang tidak pernah disebut pemilik usaha, sehingga nilainya dibatasi maksimal 5. Catatan jujur: pemilihan karyawan kantoran sebagai target utama hanyalah perkiraan (skor 86 lawan 82 hampir seri dan bukan data pasar), jadi perlu dibuktikan dengan bertanya ke pelanggan sendiri; tokoh pembeli (Mbak Dian) rekaan, dan judul grup Facebook "Mulai 27rb/porsi" belum memakai harga langganan yang setara Rp25.000 per porsi. Rincian persona, tabel pembeda, dan uji 7 hari baru muncul bila Anda membalas "lengkap". Uji sebelumnya (OpenClaw di komputer penguji, v1.0.5, kasus lain): 6,25 → 8,75.

## FAQ
**Apakah ini riset pasar?**
Bukan. Hasilnya hipotesis (dugaan yang perlu diuji) terstruktur dari info Anda. Karena itu hasilnya disertai uji 7 hari dan penanda "perlu dicek". Makin banyak data (ulasan, chat, wawancara), makin tajam.

**Perlu API key atau akun?**
Tidak. Script hanya memakai Python standar.

**Boleh dipakai untuk produk kesehatan atau kosmetik?**
Boleh untuk positioning, tetapi klaim khasiat tidak dibuatkan; Anda tetap perlu mengecek aturan BPOM dan sertifikasi halal.

## Catatan lisensi
Sebagian kerangka diadaptasi dari skill berlisensi MIT (phuryn/pm-skills dan coreyhaines31/marketingskills); rincian dan teks lisensi ada di `ATTRIBUTION.md`. Skill ini tidak berafiliasi dengan pembuat sumber.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
