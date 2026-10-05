# Catatan sumber: anthropics/knowledge-work-plugins (skill `reactivate`)

Tanggal: 2026-10-05 · Pembuat skill: agen pembuat (jalur kurasi/ATM) · Terkait: `research/sources/kurasi-apache-2026-10-05.md` kandidat #1 (baris 5).

## Sumber
- **URL repo:** https://github.com/anthropics/knowledge-work-plugins
- **Skill diambil:** `small-business/skills/reactivate/SKILL.md` (https://github.com/anthropics/knowledge-work-plugins/tree/main/small-business/skills/reactivate). Folder skill sumber hanya berisi `SKILL.md` (109 baris), tanpa script dan tanpa file pendukung.
- **Pembuat:** Anthropic · **Lisensi:** Apache License 2.0 (berkas `LICENSE` di akar repo dibaca 2026-10-05; pemegang hak cipta tidak terisi: masih `[yyyy] [name of copyright owner]`; di akhir berkas ada beberapa baris teks acak non-lisensi yang tidak disalin) · **NOTICE:** tidak ada (404 pada cabang utama, 2026-10-05).
- **Sinyal bukti:** dinilai di berkas kurasi induk (26,2k bintang, 3,1k fork, pembuat resmi, commit terakhir 2026-10-01; 5/5 sinyal). Tidak diverifikasi ulang di sesi ini selain keberadaan file dan lisensi.
- **Cara baca:** `raw.githubusercontent.com` (tanpa clone, tanpa menjalankan kode). Hash SHA-256 `SKILL.md` saat dibaca: `734946c3...39e210`.

## Audit (Tahap 3)
Dibaca penuh. Tidak ada perintah destruktif, pengiriman data ke luar, pembacaan kredensial, kode ter-obfuscate, API key, atau prompt injection. Frontmatter sumber memuat `allowed-tools: Read, WebFetch` (tidak dibawa). Sumber mengandung pagar baik ("isi pesan/dokumen = data bukan perintah"; gerbang persetujuan sebelum kirim). **Lolos.**

## Keputusan
**Diambil (ATM)** jadi `skills/aktifkan-kembali-pelanggan` v1.0.0 (status `uji`). Yang diambil hanya kerangka: temukan pelanggan diam menurut ritmenya, ranking berdasar nilai, konfirmasi penawaran, urutan 3 pesan/4 minggu, pesan pertama tidak jualan, berhenti saat komplain/balasan, catat sentuhan. Semua konektor (CRM, pembayaran, toko online, email, Mailchimp) dan rantai skill lain dibuang.

Nilai tambah: kanal WA/Telegram mode copilot (tanpa kirim massal), segmentasi A-D berdasarkan hari sejak beli terakhir, script `segmentasi.py` (CSV fleksibel, tanggal dd/mm/yyyy, data rusak, nomor ganda, daftar jangan-dihubungi, jadwal dengan batas harian) + 15 uji regresi, template pesan WA, referensi UU PDP, contoh lokal. Tier usulan: ecer Rp99.000 (script hitung + template per segmen; pembanding: pelengkap `program-referral-loyalitas` Rp79.000 dan `crm-wa`).
