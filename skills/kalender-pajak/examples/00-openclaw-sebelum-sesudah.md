# Uji OpenClaw SEBELUM vs SESUDAH: kalender-pajak

**Sumber (ada di paket VIP):** `solusi-vip/konsultan/UJI-OPENCLAW.md` (tabel skor skenario 05, bagian "Cacat per skill" dan "Uji ulang 2026-10-01 (keuangan)") dengan rincian per skenario di `solusi-vip/konsultan/uji-openclaw/05-kalender-pajak-info-kurang.md` (uji pertama) dan `solusi-vip/konsultan/uji-openclaw/05-kalender-pajak-info-kurang-ulang.md` (uji ulang).
**Tanggal uji:** 2026-10-01 (Asia/Jakarta), uji pertama dan uji ulang di hari yang sama.
**Versi skill saat uji:** uji pertama **tidak tercatat** di berkas sumber (kemungkinan 1.0.6, versi sebelum 1.0.7; 1.0.7 dibuat sebagai revisi atas temuan uji ini, lihat `CHANGELOG.md`). Uji ulang = **1.0.7** (tertulis di berkas sumber). Versi di katalog saat ini: 1.0.7.
**Versi OpenClaw:** tidak dicatat di berkas sumber 05; kolom `platform_teruji` di katalog menyebut `openclaw 2026.9.6–9.7` untuk uji sebelum/sesudah 2026-10-01.
**Penguji (agent):** agent penguji independen (bukan pembuat skill); uji ulang oleh penguji independen lain.

> Berkas ini ringkasan yang disalin dari catatan uji solusi VIP Konsultan (uji dilakukan per solusi, bukan per skill). Angka disalin apa adanya dari sumber, tidak dihitung ulang di sini.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, satu giliran per panggilan, tanpa Telegram/gateway). Model: router Komunitech `ninerouter/komunitech` (dilayani `claude-sonnet-5`), sama dengan bot member.
- **SEBELUM** = home OpenClaw tanpa skill. **SESUDAH** = home berisi paket skill solusi konsultan (25 skill, termasuk `kalender-pajak`), jadi skill diuji di dalam paket, bukan sendirian. Pesan member identik di kedua sisi; jawaban lanjutan member (giliran 2) juga sama persis di kedua sisi.
- Uji ulang hanya mengulang sisi SESUDAH (home baru, direset dari skill terbaru) dengan pesan yang sama; **skor SEBELUM tidak dijalankan ulang** dan dipakai dari uji pertama.
- Penguji menjalankan sendiri `scripts/kalender_pajak.py` dan memeriksa tanggal dengan Python (15 Okt 2026 = Kamis; batas Rp500 juta dihitung dari omzet rata per bulan).

**Pesan member (giliran 1):** "kapan aja saya harus bayar sama lapor pajak bulan oktober ini? biar ga kena denda"
**Pesan member (giliran 2):** "saya freelancer konsultan, orang pribadi. pakai yang 0,5% itu, belum PKP, nggak punya karyawan. omzet setahun kira2 600 juta."

## Skor

| Skenario | Versi skill | Skor tanpa skill | Skor dengan skill | Pembeda (satu kalimat) |
|---|---|:-:|:-:|---|
| 05 Kalender pajak Oktober, info kurang, uji pertama | tidak tercatat (kemungkinan 1.0.6) | 5 | 7 | Dengan skill: bertanya 4 hal sekali jalan lalu memberi tenggat dari script ("Kamis, 15 Oktober 2026", PMK 81/2024, PP 55/2022), tanpa aturan usang; tanpa skill: "PPh 21 bayar tanggal 10" dan "PP 23" (aturan lama). Tetapi dengan skill menambah "KAP 411128/411125" karangan dan menyimpulkan ambang Rp500 juta sudah lewat sebelum September (keliru). |
| 05, uji ulang (hanya sisi SESUDAH) | 1.0.7 | 5 (dari uji pertama) | 8,5 | Batas Rp500 juta kini dihitung script (kumulatif Okt tepat Rp500 juta, lewat di November, setoran pertama Selasa 15 Desember 2026), tanpa kode KAP karangan, tanpa rujukan ke skill yang tidak terpasang. |
| **Rata-rata skenario ini** (skenario tunggal) | | **5** | **7** (uji pertama) → **8,5** (1.0.7) | Selisih +2 pada uji pertama, +3,5 pada uji ulang (membandingkan dengan skor SEBELUM yang tidak diulang). |

Skor di atas adalah skor skenario ini saja. Rata-rata seluruh solusi konsultan di uji pertama (5 skenario, skill berbeda) 6,8 → 7,8 adalah skor solusi, bukan skor skill ini.

## Verdik
Acuan kurator (keputusan pemilik 2026-10-03): LULUS bila skor sesudah >= 8 **dan** selisih rata-rata >= 1,5; selain itu BELUM.

- **Uji pertama (versi tidak tercatat): BELUM.** Selisih +2 memenuhi, tetapi skor sesudah 7 di bawah 8. Sumber sendiri menulis "kemenangannya tidak telak" untuk solusi ini dan mencatat dua kesalahan tambahan dari model pada sisi SESUDAH.
- **Uji ulang (1.0.7): LULUS.** Skor sesudah 8,5 (>= 8), selisih +3,5 dibanding skor SEBELUM uji pertama (>= 1,5). Penguji menulis status "LULUS" dan "Cacat lama hilang: YA".

## Catatan jujur
- **Cacat uji pertama (sudah ditutup di 1.0.7):** (1) model menambahkan "KAP 411128/411125" padahal kode itu tidak ada di skill (411125 adalah PPh 25/29 orang pribadi, bukan PPh final UMKM); (2) model menyimpulkan omzet Rp600 juta/tahun "kemungkinan besar sudah melewati Rp500 juta sebelum September", padahal dengan omzet rata-rata baru tembus sekitar Oktober; (3) keluaran script merujuk skill `pph-final-umkm` yang tidak ada di paket konsultan. Perbaikan 1.0.7: opsi `--omzet-bulanan`/`--omzet-setahun`, larangan menyebut kode setor selain deposit pajak 411618-100, rujukan ke skill lain menjadi bersyarat ("bila terpasang").
- **Uji ulang sudah ada** (2026-10-01, 1.0.7) dan memperbaiki skor 7 menjadi 8,5, tetapi hanya sisi SESUDAH yang diulang; angka selisih memakai skor SEBELUM dari uji pertama.
- **Sisa kekurangan (belum diperbaiki):** batas 7 tahun tarif PPh final 0,5% untuk orang pribadi tidak disinggung di jawaban SESUDAH; versi tanpa skill justru menyebutnya (nilai tambah di sisi tanpa skill). Di `SKILL.md` saat ini juga tidak ada pembahasan batas 7 tahun.
- **Keterbatasan penilaian:** hanya satu skenario (orang pribadi UMKM 0,5%), dua giliran; profil badan/PKP/karyawan tidak diuji di OpenClaw. Pengiriman pengingat terjadwal ke Telegram juga belum diuji di sini.
- **Alat uji:** pada uji ulang argumen tool call tidak dapat diaudit (hanya nama tool dari keluaran JSON). Pemakaian skill pada uji pertama terbukti dari jejak tool (`read` SKILL.md lalu `exec` `kalender_pajak.py --profil op-umkm --tahun 2026 --bulan-mulai 10 --jumlah-bulan 1`).
- **Bukan bagian berkas ini:** angka 13/20 → 20/20 dan 108 tenggat dengan 0 selisih ada di `HASIL-UJI.md` (uji simulasi Claude Code, bukan OpenClaw). Uji gabungan paket konsultan 2026-10-03 (`solusi-vip/konsultan/UJI-GABUNGAN-2026-10-03.md`, ada di paket VIP) memasang `kalender-pajak` tetapi tidak memberi skor khusus untuk skill ini, jadi tidak dipakai di sini.

## Cuplikan dari sumber (sebelum/sesudah)
- Tanpa skill: "PPh 21 ... bayar paling lambat tanggal 10" (aturan lama) dan dasar "PP 23".
- Dengan skill, uji pertama: "Kamis, 15 Oktober 2026: SETOR PPh Final UMKM 0,5% masa pajak September 2026 ... setoran yang tervalidasi otomatis dianggap sudah lapor."
- Dengan skill, uji ulang 1.0.7: kumulatif Oktober "Rp500 juta (pas, belum lewat)", November "LEWAT Rp500 juta"; "Setoran pertama baru untuk masa November 2026, paling lambat Selasa, 15 Desember 2026."
