# Hitung Pajak UMKM 0,5% Tiap Bulan

**Masukkan omzet, langsung tahu pajak per bulan dan kapan batas Rp500 juta terlewati.**

*Diuji AI penguji independen di OpenClaw: 8 → 9 dari 10 (satu skenario; uji pertama skill sempat kalah 7 lawan 8, lalu 9 setelah perbaikan. Angka pajak sama-sama benar; dengan skill ada tabel per bulan lengkap dengan tanggal setor, dan aturan yang belum pasti disebut apa adanya).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tabel PPh final (pajak penghasilan tetap 0,5% dari omzet) per bulan lengkap dengan omzet kumulatif (dijumlah sejak Januari) dan batas setor
- ✅ Otomatis menerapkan Rp500 juta pertama bebas pajak untuk orang pribadi, termasuk bulan saat batas terlewati
- ✅ Mencatat PPh 22 (pajak yang dipungut marketplace dari penjual) supaya tidak tercecer
- ✅ Mengingatkan bila omzet mendekati batas Rp4,8 miliar
- ✅ Angka dihitung program kecil (script), bukan dikira-kira, dan disertai dasar aturan

## Cocok untuk siapa
- Penjual online, warung, katering, dan UMKM perorangan yang memakai tarif 0,5%
- PT perorangan dan koperasi
- Admin atau keluarga yang membantu mengurus pajak usaha

## Contoh sebelum & sesudah
**Sebelum:** Menjumlah omzet di buku, bingung bulan mana mulai bayar pajak dan berapa persisnya.

**Sesudah (cukup ketik):** "Saya jualan baju online, atas nama pribadi (bukan PT). Omzet 2026: Jan 38jt, Feb 42jt, Mar 55jt, Apr 61jt, Mei 70jt, Jun 88jt, Jul 95jt, Agu 102jt. Pajaknya berapa per bulan?"

*Cuplikan hasil nyata dari `examples/01-olshop-pribadi-lewat-500-juta.md` (baris Februari–Juli dan catatan dasar aturan dipotong):*
```
| Bulan | Omzet | Omzet kumulatif | Omzet kena pajak | PPh final 0,5% | PPh 22 marketplace (info) | Setor paling lambat | Keterangan |
|---|---:|---:|---:|---:|---:|---|---|
| Januari | Rp 38.000.000 | Rp 38.000.000 | Rp 0 | Rp 0 | - | 2026-02-15 | masih dalam Rp500 juta bebas |
…
| Agustus | Rp 102.000.000 | Rp 551.000.000 | Rp 51.000.000 | Rp 255.000 | - | 2026-09-15 | melewati Rp500 juta; hanya Rp 51.000.000 yang kena pajak |
| **Total** | **Rp 551.000.000** | | | **Rp 255.000** | - | | |

**Penjelasan singkat:** Januari–Juli Anda belum bayar PPh final karena omzet kumulatif masih di bawah Rp500 juta. Di **Agustus** omzet kumulatif menjadi Rp551 juta, jadi **hanya Rp51 juta** (bagian di atas Rp500 juta) yang kena 0,5% → **Rp255.000**. Mulai September, seluruh omzet tiap bulan kena 0,5%.
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Hitung PPh final UMKM saya dari file omzet-2026.csv."
- "PT perorangan saya omzet Agustus 120 juta, pajaknya berapa?"
- "Sisa omzet bebas pajak saya tahun ini tinggal berapa?"

## Instalasi singkat
Salin folder `pph-final-umkm` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** penguji AI independen, skor 1–10, dua sumber yang terpisah.
- **Uji OpenClaw, 1 Oktober 2026** (angka dari `examples/00-openclaw-sebelum-sesudah.md`, satu skenario orang pribadi dengan NPWP, yaitu nomor pokok wajib pajak, sejak 2021): skor tanpa skill 8 → dengan skill 7 pada uji pertama (skill kalah), lalu 9 setelah perbaikan v1.0.3. Selisih akhir +1 poin dan terutama pada tabel per bulan dengan tanggal setor serta sikap jujur soal batas 7 tahun, bukan angka pajaknya (kedua sisi sama-sama benar). Usaha berbentuk badan dan aturan PP 20/2026 belum diuji di OpenClaw.
- **Uji simulasi agent (perbandingan tanpa dan dengan skill), 23 September 2026** (`examples/00-pembanding-tanpa-skill.md` dan `examples/HASIL-UJI.md`): olshop perorangan dengan omzet Januari–Agustus 2026 sebesar Rp551.000.000. Angka inti sama-sama benar (Januari–Juli Rp0, Agustus Rp255.000), tetapi tanpa skill tidak ada tabel per bulan dan tanggal setor, dan jawabannya menyatakan pasti bahwa tarif 0,5% "maksimal 7 tahun", padahal batas itu mungkin berubah oleh PP 20/2026 dan belum terverifikasi. Dengan skill status aturan itu disebut jujur dan Anda diarahkan ke DJP (Direktorat Jenderal Pajak). Angka skill juga cocok dengan hitungan independen pada 400 kasus acak (0 selisih).

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Apakah hasil ini bisa langsung dipakai untuk setor pajak?**
Hasilnya adalah hitungan bantu. Setoran dan pelaporan tetap lewat Coretax (sistem pajak online) atau DJP. Untuk kasus khusus, konfirmasi ke DJP (Kring Pajak 1500200) atau konsultan pajak.

**Saya CV, masih bisa pakai tarif 0,5%?**
Aturan baru (PP 20/2026) mengeluarkan CV, firma, dan PT biasa dari skema ini dengan masa transisi. Skill akan menghitung simulasinya, tapi pastikan dulu ke DJP apakah usaha Anda masih boleh memakai 0,5%.

**PPh 22 yang dipotong Shopee/Tokopedia mengurangi pajak saya?**
Pungutan itu dicatat di tabel sebagai informasi. Cara memperhitungkannya dengan PPh final perlu ditanyakan ke DJP atau konsultan, jadi skill tidak menguranginya otomatis.

> **Catatan penting:** alat bantu hitung, bukan nasihat pajak. Dasar aturan (PP = Peraturan Pemerintah, PMK = Peraturan Menteri Keuangan; berlaku per 23 September 2026): PP 55/2022 sebagaimana diubah PP 20/2026 (PPh final 0,5%; omzet Rp500 juta pertama bebas untuk orang pribadi; batas omzet Rp4,8 miliar); batas setor tanggal 15 bulan berikutnya dan digeser ke hari kerja bila libur (PMK 81/2024 Pasal 94 dan 100); PPh 22 marketplace PMK 37/2025 (berlaku 1 Agustus 2026). Batas jangka waktu tarif 0,5% dan masa transisi CV/firma/PT belum terverifikasi, jadi tidak disampaikan sebagai kepastian. PPh dibulatkan ke bawah dan pembulatan ini belum dicocokkan dengan Coretax; bila berbeda, ikuti Coretax. Kepastian: DJP (Kring Pajak 1500200) atau konsultan pajak.

## Riwayat perubahan

Versi terkini: **1.0.3**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
