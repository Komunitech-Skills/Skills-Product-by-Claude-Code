# Cek Risiko Usaha, Tahu Perlu Asuransi atau Tidak

*Tagline: peta risiko usaha Anda dan dana darurat yang masuk akal, dalam satu tabel.*

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

## Instalasi
Lihat `docs/instalasi.md` untuk OpenClaw, Codex, Claude Code, dan Cursor. Script opsional memakai Python standar (`python3`; Windows `python`/`py`).

## FAQ
1. **Apakah ini nasihat asuransi?** Bukan. Ini alat bantu awam; polis dibeli lewat perusahaan asuransi berizin OJK dan agen yang terdaftar.
2. **Bisakah memilihkan merek asuransi terbaik?** Tidak. Skill memberi kriteria dan pertanyaan, bukan merek.
3. **Apakah klaim pasti cair?** Tidak ada yang bisa menjamin; skill membantu menyiapkan dokumentasi.

Terkait: `laporan-insiden-usaha` (kejadian yang sudah terjadi), `kas-umkm` (keuangan harian).
