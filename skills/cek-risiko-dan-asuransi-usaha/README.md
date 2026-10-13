# Cek Risiko Usaha, Tahu Perlu Asuransi atau Tidak

*Tagline: peta risiko usaha Anda dan dana darurat yang masuk akal, dalam satu tabel.*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- Tahu risiko mana yang paling berbahaya untuk warung, toko, bengkel, kafe, atau jasa Anda.
- Langkah murah yang bisa dilakukan minggu ini, sebelum membeli apa pun.
- Jelas mana yang memang layak dialihkan ke asuransi dan mana yang tidak.
- Target dana darurat usaha dihitung pasti dari biaya tetap Anda.
- Daftar pertanyaan siap bawa ke agen asuransi terdaftar.

## Cocok untuk siapa
Pemilik usaha kecil yang bingung apakah perlu asuransi, dan profesional yang membantu mereka. Tidak perlu paham istilah asuransi.

## Cara pakai
Ketik satu kalimat, mis. "Kafe saya di ruko dekat sungai, 3 karyawan, apa risikonya dan perlu asuransi apa?" Hasil langsung berupa tabel; di akhir ada maksimal 3 pertanyaan.

## Sebelum / sesudah
Uji A/B (skenario toko kelontong di Semarang Utara yang sering kena rob; satu pesan yang sama, jawaban model tanpa dan dengan skill; uji oleh agent, bukan uji OpenClaw):

- **Tanpa skill:** daftar risiko umum, perkiraan premi dan tarif iuran BPJS dari ingatan, arisan ikut dihitung sebagai biaya tetap tanpa catatan, dana darurat hanya berupa rentang ("11,5 sampai 23 juta"), tanpa skor dan tanpa keputusan "perlu asuransi atau tidak" per risiko.
- **Dengan skill:** 9 risiko diberi skor dan tingkat, tiap risiko ada keputusan asuransinya (utang pelanggan macet ditulis "tidak ada asuransi umum, pakai langkah lain"), dana darurat dihitung pasti, hasilnya "kurang Rp4.050.000, sisihkan Rp675.000 per bulan selama 6 bulan", tanpa merek dan tanpa premi karangan.
- Penilaian penguji independen: 6 dari 10 (tanpa skill) menjadi 8,5 dari 10 (dengan skill). Bahan lengkap: `examples/00-pembanding-tanpa-skill.md`.
- Uji otomatis agent di OpenClaw (v1.0.2): rata-rata 6,6 tanpa skill menjadi 9,0 dengan skill. Rincian: `examples/00-openclaw-v1.0.2-sebelum-sesudah.md`.

## Instalasi
Lihat `docs/instalasi.md` untuk OpenClaw, Codex, Claude Code, dan Cursor. Script opsional memakai Python standar (`python3`; Windows `python`/`py`).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 14, 2026-10-12.
- Tanpa skill: https://t.me/c/4407409583/1204/1225 — skor 6,5
- Dengan skill: https://t.me/c/4407409583/1205/1228 — skor 8,5
Verdik gelombang: LULUS — Tanpa skill menyarankan dana darurat Rp94,8 juta tanpa hitung kekurangan dan keliru menyebut kas Rp8 juta "kurang dari separuh" biaya sebulan; dengan skill peta risiko berskor, target Rp47,4 juta, kekurangan Rp39,4 juta (±Rp6,57 juta per bulan selama 6 bulan), tanda mana yang perlu asuransi, dan jalur aduan OJK 157 bila klaim ditolak.

## FAQ
1. **Apakah ini nasihat asuransi?** Bukan. Ini alat bantu awam; polis dibeli lewat perusahaan asuransi berizin OJK dan agen yang terdaftar.
2. **Bisakah memilihkan merek asuransi terbaik?** Tidak. Skill memberi kriteria dan pertanyaan, bukan merek.
3. **Apakah klaim pasti cair?** Tidak ada yang bisa menjamin; skill membantu menyiapkan dokumentasi.

Terkait: `laporan-insiden-usaha` (kejadian yang sudah terjadi), `kas-umkm` (keuangan harian).
