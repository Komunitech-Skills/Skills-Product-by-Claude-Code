# Uji Banding Pesaing (Wajib, pedoman kurasi Komunitech tahap 6)

Skill pesaing dibaca penuh untuk dinilai, **tidak disalin** ke produk kami.

## Pesaing dicari & dipakai
- **petergyang/no-ai-slop** (MIT, sumber ATM skill kami — dibaca ulang `SKILL.md` + `eval.md` versi
  terbaru di GitHub `main` branch pada 2026-09-26 untuk evaluasi banding, bukan untuk disalin lagi).
  Kata kunci pencarian: "no ai slop skill", "humanize writing AI detector skill", "AI slop editor
  prompt Indonesia" — hasil lain (mis. berbagai "AI humanizer" generik) tidak dicek detail karena
  fokusnya alat berbayar/website, bukan skill/prompt portabel yang bisa dibandingkan langsung untuk
  Bahasa Indonesia.
- Tidak ditemukan skill/prompt publik humanize khusus **Bahasa Indonesia** yang sepadan (terverifikasi
  populer/dipakai) — ini menguatkan posisi nilai tambah skill kami (lihat `ATTRIBUTION.md`).

## Skenario yang dijalankan berdampingan
Sama seperti Uji A/B (`00-pembanding-tanpa-skill.md`): caption IG promo kopi penuh gaya AI.

## Cara kerja no-ai-slop (ringkasan hasil baca, bukan kutipan produk kami)
Dua mode ("Edit"/"Detect", mirip struktur "Perbaiki"/"Periksa" kami — ini bagian yang memang diadaptasi
dan tercatat di ATTRIBUTION.md). Deteksi patennya berpusat pada **daftar kata & frasa bahasa Inggris**
yang eksplisit dilarang (kata seperti "leverage/delve/foster/utilize" dst.) dan pola struktural umum
(kontras biner, pembuka basa-basi generik, penutup rekap, weasel attribution, em-dash berlebihan, dll.)
yang dijelaskan lewat prinsip, bukan regex/daftar per bahasa. Ada `eval.md` sebagai checklist verifikasi
sebelum output final — mekanisme ini yang jadi inspirasi struktur verifikasi ulang kami di Langkah kerja
Perbaiki #6.

## Simulasi hasil no-ai-slop pada draf Bahasa Indonesia yang sama
no-ai-slop tidak punya daftar kata/frasa khas Indonesia (semua contoh "kata yang harus dibuang" adalah
kata Inggris) — jadi diterapkan sebagai agent yang memakai **prinsip strukturalnya saja** (bukan daftar
katanya) ke draf Indonesia:

```
Kopi susu gula aren kami dibuat dari biji kopi pilihan dari petani lokal. Promo minggu ini: beli 2
gratis 1, buruan sebelum kehabisan!
```

Penilaian manual terhadap draf ini pakai prinsip no-ai-slop sendiri:
- Prinsip "portability test" & "throat-clearing openers" berhasil menangkap & memangkas pembuka basa-
  basi dan klaim superlatif secara umum (karena itu prinsip lintas-bahasa yang memang berlaku).
- **Tapi**: tidak ada mekanisme yang secara spesifik menandai "Yuk simak" sebagai ajakan generik khas
  Indonesia, "Semoga bermanfaat/menyenangkan" sebagai penutup klise Indonesia, atau tiga-serangkai
  "cepat, mudah, dan terpercaya" — karena daftar frasa eksplisit no-ai-slop 100% berbahasa Inggris.
  Efeknya di simulasi: kalimat penutup ("Semoga hari kalian menyenangkan ya! 🙏") ikut terpotong habis
  tanpa penjelasan pola spesifik apa yang kena — hasilnya benar tapi **tanpa daftar "Yang diubah" per
  pola bernama** sejelas skill kami, karena tidak ada nama pola Indonesia untuk dirujuk.
- Tidak ada script pembantu/skor otomatis sama sekali (no-ai-slop murni instruksi teks untuk agent,
  tidak menyertakan kode) — semua deteksi 100% bergantung pembacaan agent tanpa alat bantu verifikasi
  independen seperti `scripts/cek_pola.py` kami.
- Tidak ada pembedaan konteks platform (caption IG vs email vs WA) — instruksinya berlaku umum untuk
  "draft" apa pun, tidak menyebut norma emoji/format per platform seperti tabel Input kami.

## Tabel banding
| Aspek | no-ai-slop (pesaing) | tulisan-tanpa-kesan-ai (kami) |
|---|---|---|
| Bahasa target | Inggris (daftar kata & pola 100% Inggris) | Bahasa Indonesia (17 pola bernama, ditulis dari nol) |
| Berlaku untuk draf Indonesia | Hanya lewat prinsip umum, kehilangan pola khas ID (basa-basi, tiga-serangkai, penutup klise ID) | Menangkap pola khas ID langsung dengan nama & contoh |
| Alat bantu otomatis (script) | Tidak ada | Ada, `scripts/cek_pola.py`, teruji 25 kasus + skor |
| Checklist verifikasi ulang | Ada (`eval.md`), jadi inspirasi struktur kami | Ada (Langkah kerja Perbaiki #6, dicocokkan ulang ke daftar pola) |
| Konteks platform (IG/marketplace/WA/email) | Tidak dibedakan | Dibedakan eksplisit (tabel Input & Langkah kerja #2) |
| Risiko hukum iklan Indonesia (klaim superlatif) | Tidak disebut | Dikaitkan eksplisit ke UU Perlindungan Konsumen |
| Dokumentasi pembeli awam (README, FAQ, instalasi) | Tidak — target pengguna teknis | Ada, README lengkap bahasa awam |

## Kesimpulan
Untuk draf **Bahasa Indonesia** (target pasar produk ini), skill kami menang telak: pola khas Indonesia
tertangkap dengan nama spesifik + contoh lokal, ada alat verifikasi otomatis (script + skor
terreproduksi), dan konteks platform Indonesia (marketplace, WA) dibedakan — semua ini tidak ada di
no-ai-slop karena memang tidak dirancang untuk Bahasa Indonesia. Untuk draf **Inggris**, no-ai-slop
tetap kuat sebagai skill khusus bahasa itu, tapi itu di luar cakupan produk kami. Nilai tambah ATM
(dicatat di ATTRIBUTION.md) terbukti nyata di skenario ini, bukan sekadar klaim di atas kertas.
