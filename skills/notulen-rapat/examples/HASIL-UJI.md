# Hasil Uji – notulen-rapat

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** SKILL.md, README.md, ATTRIBUTION.md, `references/aturan-klasifikasi.md`, `scripts/tanggal_relatif.py`
- **Metode:** 5 skenario dijalankan dengan berperan sebagai agent yang memuat SKILL.md, ditambah 1 uji A/B (S1 tanpa skill). Script dijalankan sungguhan di `/tmp/uji-notulen-rapat/`. Aturan tafsir diverifikasi dengan script Python terpisah milik penguji: 14 tanggal rapat (semua hari dalam seminggu, 2×) × 7 nama hari × bentuk "<hari>" dan "<hari> minggu depan", + besok/lusa/"5 hari lagi"/akhir bulan. Hasilnya **0 selisih** dari aturan yang tertulis di docstring. Nama hari seluruh tanggal di contoh dicek dengan `datetime`.

## Audit keamanan
`tanggal_relatif.py` hanya memakai library standar (argparse, calendar, json, re, sys, datetime). Tidak ada akses jaringan, penulisan file, `subprocess`/`eval`, maupun pembacaan kredensial atau variabel lingkungan. SKILL.md menegaskan "Jangan mengirim notulen ke mana pun" dan memisahkan info sensitif dari pesan grup. Tidak ada prompt injection. **Aman.**

## Uji script (data tepi)
| Rapat | Ekspresi | Hasil | Status |
|---|---|---|---|
| Selasa 22/9/2026 | besok / kamis / akhir bulan / 2 minggu lagi | Rab 23/9 / Kam 24/9 / Rab 30/9 / Sel 6/10 | ✅ |
| Selasa 22/9 | jumat depan | Jum 2/10 **ambigu**, alternatif Jum 25/9 | ✅ |
| Senin 21/9 | minggu depan | Sen 28/9 **perkiraan** | ✅ |
| Selasa 22/9 | minggu ini | Jum 25/9 **ambigu**, alternatif Min 27/9 | ✅ |
| Jumat 25/9 | senin ini (sudah lewat) | Sen 21/9 **ambigu**, alternatif Sen 28/9 | ✅ |
| Jumat 25/9 | jum'at depan, "Jumat  Depan" (spasi ganda) | Jum 2/10 | ✅ |
| Kamis 31/12/2026 | besok / bulan depan / 3 hari lagi | Jum 1/1/2027 / 1/1/2027 perkiraan / Min 3/1/2027 | ✅ |
| **Minggu 27/9/2026** | **senin minggu depan** | **Sen 28/9 (besoknya) [pasti]** | ⚠️ **ambigu tapi dilabel pasti** |
| Minggu 27/9 | jumat depan / rabu depan | Jum 2/10 / Rab 30/9 [pasti] | ⚠️ sama |
| Senin 21/9 | EOD, next week, end of month | tidak_dikenali | ⚠️ ringan |
| Minggu 30/1/2028 | tanggal 5, tgl 30, akhir bulan depan, sebelum lebaran | tidak_dikenali | ✅ (ditandai ⚠️ sesuai SKILL.md) |
| — | `--ekspresi` tanpa `--rapat`; `--rapat 31-02-2026`; tanpa argumen | ERROR jelas | ✅ |
| — | `--cek 02-10-2026` | Jumat, 2 Oktober 2026 | ✅ |

## Ringkasan skenario
| # | Skenario | Hasil |
|---|---|---|
| 00 | A/B: S1 tanpa skill | Tanpa skill, usulan diskon ditulis **"diputuskan"**, tanggal tetap relatif, dan tugas tanpa PIC jadi "Tim". Dengan skill **jelas lebih baik**. |
| 01 | Weekly olshop, catatan kasar | Sangat baik. Usulan vs keputusan terpisah benar, tanggal dikonversi, ambigu ditandai. |
| 02 | "rangkumin dong" rapat RT → WA warga | Sangat baik. Tunggakan warga dikeluarkan dari WA. "Minggu depan" dari rapat hari Minggu ditandai. |
| 03 | Transkrip Meet, Speaker 1/2, campur Inggris, angka janggal, gaji | Sangat baik. "450 juta" ditandai tanpa dikoreksi, gaji tidak masuk WA. Istilah Inggris lewat jalur ⚠️. |
| 04 | Minta notulen tanpa catatan | Sangat baik. Hanya meminta catatan, tidak mengarang. |
| 05 | Minta transkrip file .mp4 | Sangat baik. Jujur soal batasan, memberi 3 jalan keluar. |

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 9 | Notulen/notula/risalah/meeting minutes/action items, bentuk input disebut. |
| Kemudahan awam | 9 | Tinggal tempel catatan. Pesan WA siap kirim. Python opsional. |
| Kualitas output | 9 | Struktur lengkap, tabel tugas terurut, "Perlu dikonfirmasi" sangat berguna. |
| Akurasi (angka/fakta) | 8 | Tidak ada keputusan/angka karangan, dan script cocok dengan aturannya. Kelemahan: rapat hari Minggu memberi status "pasti" untuk ekspresi yang sebenarnya ambigu. |
| Penanganan input kurang | 10 | Hanya meminta yang wajib. Sisanya ditandai, tidak ditanyakan. |
| Penanganan di luar cakupan | 9 | Transkripsi audio ditolak jujur, dengan solusi. |
| Keamanan | 10 | Lokal, library standar, info sensitif dipisah dari pesan grup. |

## SKOR AKHIR: 8 / 10 → **LULUS**

Skill ini mencegah kesalahan paling berbahaya dalam notulen, yaitu menulis usulan sebagai keputusan. Uji A/B membuktikan agent biasa melakukan kesalahan itu. Tanggal relatif dikonversi dengan benar dan ambiguitas ditandai. Satu cacat sedang pada script (rapat hari Minggu) sebaiknya diperbaiki sebelum rilis, karena rapat RT, keluarga, dan komunitas sering diadakan hari Minggu.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
- **S1 – Rapat hari Minggu: "<hari> depan" / "<hari> minggu depan" dilabel `pasti` padahal ambigu** (`scripts/tanggal_relatif.py`, fungsi `tafsir`, cabang `if suf:`). Script memakai minggu Senin–Minggu (`senin_ini = rapat - weekday`). Akibatnya, pada rapat hari Minggu 27/9, "senin minggu depan" = Senin 28/9 (besoknya) berlabel `pasti`, tanpa masuk "Perlu dikonfirmasi". Banyak orang Indonesia (kalender dimulai hari Minggu) memaknainya 5/10. Tenggat bisa meleset seminggu tanpa peringatan. *Saran:* bila `rapat.weekday() == 6` (Minggu), beri status `ambigu` pada "<hari> depan", "<hari> minggu depan", dan "minggu depan", dengan alternatif `d + timedelta(days=7)` dan catatan "Rapat hari Minggu: 'minggu depan' bisa dimulai besok atau pekan setelahnya." Tambahkan kasus ini ke docstring.

### Ringan
- **R1 – Istilah Inggris umum tidak dikenali** (`tafsir`): "EOD", "tomorrow", "next week", "end of month", "next <day>". README/SKILL.md menjanjikan dukungan rapat campuran Inggris. *Saran:* tambahkan alias: tomorrow→besok, EOD/end of day→hari ini, next week→minggu depan, end of month→akhir bulan, next friday→jumat depan (tetap ambigu).
- **R2 – Tanggal angka tanpa bulan tidak dikenali** ("tanggal 5", "tgl 30", "akhir bulan depan"). Sudah aman karena ditandai ⚠️, tapi mudah didukung. *Saran:* "tanggal N"/"tgl N" = tanggal N berikutnya setelah rapat (status `perkiraan`); "akhir bulan depan" = hari terakhir bulan berikutnya.
- **R3 – Format rupiah berbeda antar-skill**: notulen `Rp 150.000` (SKILL.md Checklist), surat-resmi `Rp1.500.000,00` (EYD V). *Saran:* tetapkan satu gaya di pedoman library (mis. EYD `Rp150.000` untuk dokumen formal, `Rp 150.000` untuk chat/WA), lalu sebut alasannya di SKILL.md.
- **R4 – Asumsi yang masuk ke pesan WA siap kirim.** SKILL.md tidak melarang pesan WA memuat tafsiran yang masih ⚠️ (mis. periode iuran, tanggal ambigu). *Saran:* tambahkan ke Checklist: "Pesan WA hanya memuat hal yang pasti. Tanggal ambigu ditulis dengan tanda tanya atau dua pilihan."
- **R5 – README merujuk `CARA-INSTAL.md`** dan ATTRIBUTION merujuk `LISENSI.txt`, dan keduanya tidak ada di folder skill. Pastikan keduanya ikut dalam paket rilis.

---
## Uji ulang v1.0.4 (2026-10-13, penguji independen, OpenClaw sebelum/sesudah)
- OpenClaw 2026.10.2 lokal dengan skenario catatan rapat mingguan 1/10 yang sama (pesan identik). SEBELUM tanpa skill, SESUDAH hanya skill ini. Rincian ada di `00-openclaw-sebelum-sesudah.md`.
- Skor tanpa skill **6** → dengan skill **9** (selisih +3,0), jadi **LULUS** acuan (sesudah ≥ 8 dan selisih ≥ 1,5). Nama hari dan tanggal sisi SESUDAH cocok dengan kalender yang dicek penguji dengan Python.
- Perbaikan v1.0.4 terbukti: tidak ada lagi tugas tambahan untuk Hendra (sewa forklift hanya dicatat sebagai keputusan). Pembeda: tanggal relatif dikonversi lewat script dan "Jumat depan" ditandai ambigu (2/9 Okt), sedangkan tanpa skill "2,1M" menjadi Rp2,1 juta dan forklift nomor 2 dibaca sebagai 2 unit.
- Sisa temuan ringan: pemimpin rapat diisi "Pak Budi (disimpulkan dari jabatan)" dan ditandai untuk dikonfirmasi, padahal SKILL.md meminta `[isi]`.
