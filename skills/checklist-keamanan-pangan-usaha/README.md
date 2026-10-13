# Dapur Aman, Checklist Siap Tempel

*Ceritakan usaha kulinermu dalam satu kalimat; dapat checklist, log suhu, dan kartu staf yang tinggal ditempel.*

> **PERLU REVIEW perizinan/ahli:** bagian perizinan hanya petunjuk awal dan belum diverifikasi penuh oleh ahli; cek ke Dinas Kesehatan/BPOM/lembaga halal. Bukan pengganti pelatihan atau pemeriksaan resmi, dan bukan nasihat hukum.

## Manfaat
- Checklist harian (datang, sebelum buka, jam sibuk, tutup) sesuai menu dan alat yang kamu punya.
- Log suhu kulkas, freezer, masak, dan pemanasan ulang lengkap dengan batas Celsius dan "kalau melebihi, lakukan apa".
- Kartu 10 aturan dapur untuk staf, bahasa sehari-hari.
- Peta risiko menu: ayam, telur, santan, susu, nasi, seafood, alergen, dan kontaminasi silang.
- Ringkasan izin yang relevan (SLHS, PIRT, izin edar MD, halal, label) sebagai petunjuk awal.

## Cocok untuk siapa
Pemilik kafe, warung, katering rumahan, toko kue, usaha minuman, dan frozen food yang ingin dapurnya lebih aman dan siap bila ada pemeriksaan, tanpa harus menulis SOP dari nol.

## Cara pakai
Tulis misalnya: "Buatkan checklist keamanan pangan untuk katering rumahan, menu nasi box ayam bakar dan sayur santan, 2 staf, ada 1 kulkas." Hasil langsung muncul lengkap. Punya catatan suhu? Simpan sebagai CSV (`waktu,alat,suhu`) dan minta dicek; pelanggaran dan lama di zona bahaya dihitung otomatis.

## Yang tidak dilakukan
Tidak membuat sertifikat higiene/halal, tidak menulis "bebas alergen" untuk dapur bersama, tidak membantu mengganti tanggal kadaluarsa, dan tidak mengisi log suhu palsu. Sebagai gantinya, kamu dapat cara yang sah (mengurus izin resmi, label "diproses di dapur yang juga mengolah ...", membuang bahan lewat tanggal, mengisi log jujur dengan cepat).

## Contoh sebelum/sesudah
**Tanpa skill:** bot menyimpan checklist sebagai file di server, sehingga pengguna Telegram hanya menerima nama file (rata-rata 5,6/10).

**Dengan skill:** paket lengkap tampil langsung di chat: checklist harian, log suhu dengan tindakan bila melebihi batas, kartu 10 aturan staf, peta risiko menu, dan petunjuk perizinan. Kulkas 9 °C selama sekitar 3 jam dan freezer -17 °C tertangkap (rata-rata 8,25/10, uji OpenClaw v1.0.2). Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

## Instalasi singkat
Salin folder ini ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 14, 2026-10-12.
- Tanpa skill: https://t.me/c/4407409583/1206/1233 — skor 7
- Dengan skill: https://t.me/c/4407409583/1207/1236 — skor 7,5
Verdik gelombang: BELUM — Dengan skill paketnya lebih lengkap (checklist bercentang, log suhu dengan tindakan bila di atas 5 °C, kartu aturan staf, peta risiko menu), tetapi memuat kesalahan fakta (ayam boleh 63 °C untuk potongan utuh, santan ditulis alergen susu, halal ditulis opsional); tanpa skill sudah menolak sertifikat/logo palsu dan klaim bebas alergen.

## FAQ
**Apakah ini menggantikan pelatihan atau SLHS resmi?** Tidak. Ini alat bantu kebiasaan kerja; pelatihan dan pemeriksaan resmi tetap lewat Dinas Kesehatan/BPOM.
**Apakah angka suhunya sesuai aturan Indonesia?** Angka suhu dari WHO, FDA Food Code 2022, dan USDA (dicek 2026-10-12; ayam selalu matang inti 74 °C), daftar alergen mengikuti label BPOM, dan halal ditulis wajib sesuai UU 33/2014 & PP 42/2024. Tetap cocokkan dengan Dinkes setempat (PERLU REVIEW).
**Perlu instal apa-apa?** Tidak. Skill tetap berguna tanpa script; script hanya butuh Python standar.

> PERLU REVIEW perizinan/ahli: bagian perizinan (selain halal dan alergen yang dicek 2026-10-12) belum diverifikasi ulang ke sumber resmi. Bukan nasihat hukum.

Versi 1.0.2 (2026-10-12): perbaikan fakta suhu ayam, alergen santan, dan kewajiban halal setelah uji Telegram gelombang 14.
