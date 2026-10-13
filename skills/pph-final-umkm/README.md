# Hitung Pajak UMKM 0,5% Tiap Bulan

**Masukkan omzet, langsung tahu pajak per bulan dan kapan batas Rp500 juta terlewati.**

## Manfaat
- ✅ Tabel pajak per bulan lengkap dengan omzet kumulatif dan batas setor
- ✅ Otomatis menerapkan Rp500 juta pertama bebas pajak untuk orang pribadi, termasuk bulan saat batas terlewati
- ✅ Mencatat PPh 22 yang dipotong marketplace supaya tidak tercecer
- ✅ Mengingatkan bila omzet mendekati batas Rp4,8 miliar
- ✅ Angka dihitung script, bukan dikira-kira, dan disertai dasar aturan

## Cocok untuk siapa
- Penjual online, warung, katering, dan UMKM perorangan yang memakai tarif 0,5%
- PT perorangan dan koperasi
- Admin atau keluarga yang membantu mengurus pajak usaha

## Contoh sebelum & sesudah
**Sebelum:** Menjumlah omzet di buku, bingung bulan mana mulai bayar pajak dan berapa persisnya.

**Sesudah (cukup ketik):** "Omzet saya Jan 45jt, Feb 60jt, Mar 80jt, Apr 120jt, Mei 150jt, Jun 90jt. Pajaknya berapa?"
→ Tabel per bulan: Januari–Mei Rp0 (masih dalam Rp500 juta), Juni hanya Rp45 juta yang kena pajak → PPh Rp225.000, setor paling lambat 15 Juli.

**Hasil uji A/B (simulasi agent, 23 September 2026):** olshop perorangan dengan omzet Januari–Agustus 2026 sebesar Rp551.000.000. Angka inti sama-sama benar (Januari–Juli Rp0, Agustus Rp255.000), tetapi tanpa skill tidak ada tabel per bulan dan tanggal setor, dan jawabannya menyatakan pasti bahwa tarif 0,5% "maksimal 7 tahun", padahal batas itu mungkin berubah oleh PP 20/2026 dan belum terverifikasi. Dengan skill status aturan itu disebut jujur dan kamu diarahkan ke DJP. Angka skill juga cocok dengan hitungan independen pada 400 kasus acak (0 selisih). Rincian: `examples/00-pembanding-tanpa-skill.md` dan `examples/HASIL-UJI.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Hitung PPh final UMKM saya dari file omzet-2026.csv."
- "PT perorangan saya omzet Agustus 120 juta, pajaknya berapa?"
- "Sisa omzet bebas pajak saya tahun ini tinggal berapa?"

## Instalasi singkat
Salin folder `pph-final-umkm` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

## FAQ
**Apakah hasil ini bisa langsung dipakai untuk setor pajak?**
Hasilnya adalah hitungan bantu. Setoran dan pelaporan tetap lewat Coretax/DJP. Untuk kasus khusus, konfirmasi ke DJP (Kring Pajak 1500200) atau konsultan pajak.

**Saya CV, masih bisa pakai tarif 0,5%?**
Aturan baru (PP 20/2026) mengeluarkan CV, firma, dan PT biasa dari skema ini dengan masa transisi. Skill akan menghitung simulasinya, tapi pastikan dulu ke DJP apakah usahamu masih boleh memakai 0,5%.

**PPh 22 yang dipotong Shopee/Tokopedia mengurangi pajak saya?**
Pungutan itu dicatat di tabel sebagai informasi. Cara memperhitungkannya dengan PPh final perlu ditanyakan ke DJP atau konsultan, jadi skill tidak menguranginya otomatis.

> **Catatan penting:** alat bantu hitung, bukan nasihat pajak. Dasar aturan (berlaku per 23 September 2026): PP 55/2022 sebagaimana diubah PP 20/2026 (PPh final 0,5%; omzet Rp500 juta pertama bebas untuk orang pribadi; batas omzet Rp4,8 miliar); batas setor tanggal 15 bulan berikutnya dan digeser ke hari kerja bila libur (PMK 81/2024 Pasal 94 dan 100); PPh 22 marketplace PMK 37/2025 (berlaku 1 Agustus 2026). Batas jangka waktu tarif 0,5% dan masa transisi CV/firma/PT belum terverifikasi, jadi tidak disampaikan sebagai kepastian. PPh dibulatkan ke bawah dan pembulatan ini belum dicocokkan dengan Coretax; bila berbeda, ikuti Coretax. Kepastian: DJP (Kring Pajak 1500200) atau konsultan pajak.

## Catatan revisi 1.0.3 (2026-10-01)
- Batas setor yang jatuh di hari libur (Sabtu, Minggu, libur nasional, cuti bersama 2026–2027) kini otomatis digeser ke hari kerja berikutnya sesuai PMK 81/2024 Pasal 100, dan wajib disebut AI di balasan (temuan uji OpenClaw: 15 Nov 2026 hari Minggu tidak disebut).
- Opsi `--tahun-terdaftar`: menghitung batas jangka waktu tarif 0,5% menurut PP 55/2022 Pasal 59 (orang pribadi 7 tahun; mis. NPWP 2021 → s.d. 2027), dengan peringatan bahwa perubahan oleh PP 20/2026 belum diverifikasi.
- Instruksi: script dijalankan dari subfolder `scripts/` di folder skill; catatan & dasar aturan disalin apa adanya ke chat. 5 tes otomatis baru (`tests/`).
