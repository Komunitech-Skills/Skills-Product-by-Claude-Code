# Kurasi: internal-comms (anthropics/skills) → laporan-status-kantor — 2026-09-24

Tindak lanjut kandidat #7 di `research/sources/kurasi-terbukti-2026-09-23.md` (§2 tabel,
ditandai "ATM" non-prioritas puncak). Sesi ini menyelesaikan ATM tersebut.

## Data sumber
- **Nama**: `internal-comms`
- **URL**: https://github.com/anthropics/skills/tree/main/skills/internal-comms
- **Pembuat**: Anthropic, PBC (repo resmi organisasi)
- **Metode pengambilan**: `git clone --depth 1 --filter=blob:none --sparse` ke
  `/tmp/oc-audit/repo`, `git sparse-checkout set skills/internal-comms` (read-only, tidak
  ada script dijalankan). Juga diverifikasi silang via `raw.githubusercontent.com`.
- **Commit yang diambil**: `34040c9c568585f6929bedeaad110ad08f079624`, tanggal commit
  terakhir repo `2026-09-10` (klon dangkal hanya mengambil commit HEAD saat itu; tidak bisa
  memastikan ini commit terakhir yang menyentuh folder `internal-comms` secara spesifik,
  tapi cukup untuk memastikan isi & lisensi terkini).
- **Tanggal ditinjau ulang**: 2026-09-24.
- **Isi folder sumber**: `SKILL.md` (32 baris), `LICENSE.txt` (201 baris), `examples/`
  berisi 4 file (`3p-updates.md` 46 baris, `company-newsletter.md` 65 baris,
  `faq-answers.md` 29 baris, `general-comms.md` 15 baris). Tidak ada `scripts/`, tidak ada
  file `NOTICE`.

## Lisensi
`LICENSE.txt` dibaca penuh dan diverifikasi: teks **Apache License, Version 2.0** standar,
identik dengan boilerplate resmi apache.org, dengan baris penutup:
```
Copyright 2026 Anthropic, PBC.
Licensed under the Apache License, Version 2.0 (the "License");
```
Ini **berbeda** dari skill `docx`/`xlsx`/`pptx`/`pdf`/dll. di repo yang sama, yang
`LICENSE.txt`-nya berisi teks **Proprietary** ("© 2025 Anthropic, PBC. All rights
reserved... may not extract, reproduce, distribute, sublicense... create derivative
works") — lihat temuan §1 `kurasi-terbukti-2026-09-23.md`. `internal-comms` memang termasuk
kelompok kecil skill anthropics/skills yang berlisensi Apache-2.0 (bersama
`brand-guidelines`, `claude-api`, `mcp-builder`), **boleh dipakai komersial dengan
atribusi + pemberitahuan perubahan file**, sesuai Tahap 2 CLAUDE.md.

Tidak ada file `NOTICE` di folder sumber, jadi tidak ada kewajiban menyalin isi NOTICE
(Bagian 4(d) hanya berlaku "if the Work includes a NOTICE text file").

## Hasil audit keamanan (Tahap 3 CLAUDE.md)
Seluruh isi `SKILL.md` dan ke-4 file `examples/*.md` dibaca penuh sebelum dipakai sebagai
inspirasi struktural.
- Tidak ada script sama sekali (folder `scripts/` tidak ada) → tidak ada risiko
  `curl | bash`, kode ter-obfuskasi, atau dependensi mencurigakan.
- Tidak ada perintah shell destruktif.
- Tidak ada pengiriman data ke server pihak ketiga secara tersembunyi. Instruksi
  "gunakan Slack/Google Drive/Email/Calendar jika tersedia" adalah instruksi ke AGENT untuk
  memakai *tool/konektor milik pengguna sendiri* (pola tool-use standar), bukan panggilan
  jaringan yang ditanam skill.
- Diperiksa pola prompt injection tersembunyi: "ignore previous/prior instructions",
  "disregard", "secretly", "without informing/telling the user", "do not tell the user",
  "bypass" — **nihil kecocokan** di kelima file.
- Tidak ada kredensial/API key/token/data pribadi tertanam.
- **Hasil: LULUS audit keamanan.** Konsisten dengan temuan awal di
  `kurasi-terbukti-2026-09-23.md` §4.

## Penilaian sinyal bukti (Tahap 2 CLAUDE.md)
- Pembuat kredibel ✓ (Anthropic, organisasi resmi, repo `anthropics/skills`).
- Kualitas isi ✓ — 4 contoh format konkret dengan aturan jelas (3P, newsletter, FAQ,
  general), meski ringkas.
- Popularitas per-skill individual tidak terukur terpisah dari bintang repo besar
  (`anthropics/skills` sebagai satu repo, bukan per-folder skill) → sinyal ini lemah.
- Umur & perawatan: bagian dari repo resmi yang aktif dipelihara, bukan skill baru
  sekumpulan yang dirilis mendadak.
- **Total ≈2–3 sinyal dari 5** — di ambang bawah "≥3 sinyal" yang disyaratkan CLAUDE.md
  untuk kurasi. Karena pembuatnya organisasi resmi kredibel (Anthropic) dan tidak ada
  tanda AI slop (bukan puluhan skill dirilis serentak, isi spesifik bukan generik), **tetap
  diproses sebagai ATM** sesuai catatan awal, dengan syarat nilai tambah Komunitech harus
  jadi MAYORITAS isi produk jadi (bukan sekadar terjemahan) — dipenuhi (lihat di bawah).

## Keputusan
**ATM DILANJUTKAN** → `skills/laporan-status-kantor/` (status `draft`, tier usulan `ecer`,
harga usulan Rp 49.000).

## Proporsi isi sumber vs baru
Sumber total ≈187 baris (SKILL.md + 4 file examples), mencakup 4 jenis komunikasi. Hasil
Komunitech: SKILL.md (≈190 baris) + README.md + 9 file `templates/` + 1 file
`references/` (total >1.000 baris), mencakup **9 jenis** komunikasi kantor Indonesia:
3 varian audiens 3P (atasan/pemilik, tim, klien — dipisah karena aturan isi berbeda,
sumber hanya 1 file generik), laporan harian WFH/WFO, newsletter kantor kecil, pengumuman
internal (libur nasional/cuti bersama/jam kerja/THR — TANPA menghitung nominal), FAQ
karyawan, memo/surat edaran internal, laporan insiden 5W1H. Yang diambil dari sumber murni
gagasan struktural tingkat tinggi (pengelompokan jenis komunikasi, format 3P tiga bagian,
gagasan newsletter/FAQ) — bukan teks. Rincian lengkap ada di
`skills/laporan-status-kantor/ATTRIBUTION.md`.

## Nilai tambah besar yang membedakan dari sumber
1. Tiga template 3P terpisah per audiens dengan aturan isi berbeda (klien dilarang
   membocorkan masalah internal; tim boleh lebih teknis; atasan hanya kendala yang perlu
   keputusan) — sumber tidak membedakan sama sekali.
2. 5 jenis komunikasi baru tidak ada di sumber (laporan harian, pengumuman internal, memo/
   surat edaran, laporan insiden 5W1H, plus pemecahan 3P jadi 3 varian).
3. 100% lokalisasi Indonesia: format WA/Telegram sebagai kanal default (`*tebal*`, bullet
   pendek), dua nada budaya kantor (sopan-formal vs santai-profesional), bilingual ID/EN,
   konteks THR/libur nasional/cuti bersama Indonesia (dengan pagar eksplisit: tidak
   menghitung/mengarang tanggal atau nominal).
4. Sumber butuh integrasi Slack/Google Drive/Email/Calendar korporat besar (tidak relevan
   untuk UMKM/kantor kecil Indonesia yang jadi target); versi ini bekerja murni dari bahan
   yang ditempel/diketik pengguna, sesuai prinsip "tanpa setup" CLAUDE.md.
5. Pagar anti-mengarang data eksplisit di setiap langkah (tandai `[isi: ...]`, tanya sekali)
   dan perlindungan data pribadi karyawan (UU PDP) — tidak dibahas sumber.

## Keterbatasan / PERLU REVIEW
- Belum ada `examples/` (sesuai instruksi: diisi oleh penguji independen terpisah, bukan
  pembuat skill).
- Belum ada uji A/B, uji banding pesaing, uji platform asli, atau skor kualitas — status
  masih `draft`; Tahap 6 (pengujian) perlu dilakukan agent penguji terpisah sebelum naik ke
  `uji`/`lulus`.
- Harga usulan Rp 49.000 mengikuti perkiraan awal sesi kurasi 2026-09-23 (belum dicek ulang
  ke `research/harga.md` secara rinci per skill ini) — perlu ditinjau saat Tahap 7.
- `api.github.com` diblokir di sesi ini sehingga jumlah bintang/fork repo `anthropics/skills`
  tidak diverifikasi ulang via API (dipakai angka dari sesi kurasi 2026-09-23 yang berasal
  dari halaman web).
