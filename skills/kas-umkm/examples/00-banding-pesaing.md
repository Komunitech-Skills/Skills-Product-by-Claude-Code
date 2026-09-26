# Uji banding pesaing — kas-umkm vs skill/aplikasi sejenis

Penguji independen Akun B, 2026-09-26. Pesaing hanya **dibaca untuk dinilai** (halaman publik), tidak diunduh/dijalankan, tidak disalin.

## Pencarian
- Kata kunci: "BukuWarung BukuKas aplikasi catat kas UMKM 2026"; "clawhub/skills.sh cash book bookkeeping expense tracker agent skill SKILL.md".
- Sumber: clawskills.sh (registri ClawHub), VoltAgent/awesome-openclaw-skills, Play Store, artikel jurnal.id / mekari.com / idntimes.com.

## Pesaing yang dinilai
| Pesaing | Jenis | Ringkasan (dari halaman publik) |
|---|---|---|
| **aholake-expense-tracker** (ClawHub, ±456 unduhan, v1.0.0) | skill agent + Python | Catat pengeluaran ke tabel Markdown per bulan, kategori/tag, `summary` per kategori. Tidak ada pemasukan, akun, saldo, opname, impor. VirusTotal menandai "Suspicious". |
| **smart-expense-tracker** (ClawHub, ±355 unduhan, v1.0.0) | skill agent | Keuangan pribadi di JSON lokal (budget, streak, bill split). Bukan buku kas usaha; tidak ada multi-akun/pindah dana/opname/impor bank; tidak ada tes terdokumentasi. |
| bookkeeping-basics (ClawHub) | skill panduan | Teks panduan pembukuan umum solopreneur (AS); tanpa script. |
| **BukuWarung** / BukuKas (kini LummoSHOP) | aplikasi HP (bukan skill) | Catat pemasukan/pengeluaran, utang-piutang + pengingat WA, laporan unduh; gratis tapi data di server vendor, butuh akun & internet. |

## Skenario 01 dijalankan berdampingan (dinilai dari kemampuan yang terdokumentasi)
Pesaing skill tidak dijalankan (keamanan: tidak menjalankan script pihak ketiga; salah satunya ditandai "Suspicious"). Penilaian berdasarkan apakah fitur yang dibutuhkan skenario 01 ada.

| Kebutuhan skenario 01 | aholake-expense-tracker | smart-expense-tracker | BukuWarung | **kas-umkm** |
|---|---|---|---|---|
| Uang masuk (penjualan) | tidak | ya (pribadi) | ya | ya |
| Saldo per akun laci/BRI/GoPay, QRIS ke rekening | tidak | tidak | sebagian (satu buku) | **ya** |
| Pindah dana tidak dihitung beban | tidak | tidak | tidak jelas | **ya** |
| Prive terpisah + peringatan | tidak | tidak (budget pribadi) | tidak | **ya** |
| Hitung laci per pecahan + selisih | tidak | tidak | tidak | **ya** |
| Impor mutasi bank / rekap kasir | tidak | tidak | tidak | **ya** |
| Ekspor ke laporan SAK EMKM & proyeksi kas | tidak | tidak | laporan sederhana | **ya** |
| Data lokal tanpa akun/internet | ya | ya | tidak | ya |
| Bahasa & konteks Indonesia (Rupiah, "1,2jt", QRIS) | tidak | tidak | ya | ya |
| Tes otomatis | tidak diketahui | tidak diketahui | — | 59 tes lulus |
| Kelebihan pesaing | sederhana, Markdown mudah dibaca | budget & streak | utang-piutang + pengingat WA, UI HP | (utang-piutang ada di skill lain: buku-piutang/tagih-piutang) |

## Nilai (1–10, skenario 01)
aholake-expense-tracker 3 · smart-expense-tracker 3 · BukuWarung 6 (aplikasi matang, tetapi tanpa opname/pindah dana/lokal) · **kas-umkm 9**.

**Kesimpulan: kas-umkm unggul jelas.** Pelajaran dari pesaing: BukuWarung kuat di kemudahan HP & pengingat WA; kas-umkm sudah menutupnya lewat chat + ringkasan Telegram OpenClaw dan skill piutang terpisah.

Sumber:
- https://clawskills.sh/skills/aholake-aholake-expense-tracker
- https://clawskills.sh/skills/mkpareek0315-smart-expense-tracker
- https://clawskills.sh/skills/jk-0001-bookkeeping-basics
- https://github.com/VoltAgent/awesome-openclaw-skills
- https://play.google.com/store/apps/details?id=com.bukuwarung
- https://www.jurnal.id/id/aplikasi-buku-kas/
- https://mekari.com/blog/aplikasi-umkm/
