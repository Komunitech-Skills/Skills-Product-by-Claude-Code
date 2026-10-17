# Gaji Nggak Numpang Lewat Lagi

**Atur anggaran keluarga, dana darurat, pelunasan utang, dan tabungan untuk DP rumah, sekolah anak, haji, sampai pensiun — dalam Rupiah, dihitung lewat skrip, dengan bahasa sehari-hari.**

Diuji AI penguji independen di OpenClaw: 6,5 → 9,0 dari 10 (hitungan benar di kedua sisi; pembedanya dengan skill kiriman untuk ibu dan biaya sekolah anak tidak disentuh, sedangkan tanpa skill disarankan mengurangi kiriman ibu).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Anggaran bulanan yang pas untuk keluarga Indonesia** — kiriman orang tua, arisan, zakat/perpuluhan/sedekah (opsional), cicilan motor/KPR, THR dibagi 12, dan jebakan top-up e-wallet sudah dipikirkan. Setiap rupiah punya tugas sampai sisa Rp0.
- ✅ **Tahu kapan utang lunas (simulasi)** — metode Avalanche (paling hemat) vs Snowball (paling cepat terasa menang), lengkap dengan jadwal per bulan, total bunga, dan selisih biayanya.
- ✅ **Bongkar bunga flat** — leasing "cuma 12% flat" (tenor 2 tahun) ternyata ±21,6% efektif per tahun. Bandingkan pinjaman dengan angka yang jujur.
- ✅ **Alarm bahaya** — cicilan minimum yang tidak menutup bunga, bunga di atas batas OJK/BI (tanda pinjol ilegal), dan larangan tegas gali lubang tutup lubang, plus kontak resmi OJK.
- ✅ **Target jelas per bulan** — "DP rumah 60 juta 5 tahun lagi" → berapa yang harus ditabung tiap bulan, dengan asumsi inflasi tertulis.

## Cocok untuk siapa
- Karyawan & PNS yang gajinya "habis sebelum tanggal tua"
- Pasangan muda yang baru menggabungkan keuangan dan punya anak
- Pekerja lepas, driver ojol, pedagang dengan penghasilan tidak tetap
- Siapa pun yang punya beberapa cicilan (kartu kredit, paylater, KTA/kredit tanpa agunan, pinjol legal) dan ingin keluar dari utang
- **Bukan untuk:** keuangan usaha (pakai `arus-kas-13minggu` / `laporan-keuangan-emkm`), THR karyawan (`hitung-thr`), atau mencari saran saham/kripto/reksa dana tertentu.

## Contoh sebelum & sesudah
**Sebelum (tanpa skill):** "Coba terapkan 50/30/20 dan lunasi utang berbunga tertinggi dulu." — saran umum, tanpa angka, tanpa memperhitungkan kiriman ortu dan THR, tidak tahu kapan lunas.

**Sesudah:** Keluarga Dimas & Rina (empat utang, tambahan pelunasan Rp1 juta per bulan) mendapat hasil seperti ini.

Cuplikan bagian rencana pelunasan utang (dipotong; contoh buatan pembuat skill dengan data fiktif dari `examples/uji-pembuat-01-keluarga-muda-cicilan.md`):
```
| Metode | Urutan | Semua lunas | Total bunga | Utang pertama lunas |
| **Avalanche** | Paylater → Kartu kredit → KTA → Pinjam kakak | bulan ke-15 | **Rp3.345.301** | bulan ke-3 |
| Snowball | Pinjam kakak → Paylater → Kartu kredit → KTA | bulan ke-15 | Rp3.501.409 | bulan ke-2 |

Avalanche lebih hemat **Rp156.108**.
```
Hasil lengkapnya juga memuat anggaran per pos yang dibandingkan dengan pola 60/20/20 dan 5 langkah konkret minggu ini.

## Cara pakai
Setelah terpasang, cukup cerita dengan kalimat biasa:
- "Gaji saya 7 juta, istri 3 juta, bantu atur anggaran bulanan."
- "Utang kartu kredit 12 juta dan paylater 3 juta, mana dulu yang dilunasi?"
- "Freelancer, pengeluaran pokok 5 juta, dana darurat berapa?"
- "Mau umrah berdua 4 tahun lagi, nabung berapa sebulan?"

Kalau data kurang, AI bertanya sekali saja. Angka dihitung oleh script Python bawaan (tanpa instalasi tambahan, tanpa internet); kalau script tidak bisa dijalankan, AI memakai rumus tertulis yang sama.

## Instalasi singkat
Salin folder `atur-keuangan-pribadi` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** skor 1–10. Uji di bot Telegram asli ada di bagian "Bukti uji di bot Telegram" di bawah.
- **Uji OpenClaw otomatis agent, 1–2 Oktober 2026** (v1.0.11; angka dari `examples/00-openclaw-sebelum-sesudah.md`): tanpa skill **6,5** → dengan skill **9,0** (selisih +2,5, lulus acuan kami). Contoh gaji bersih Rp6,5 juta vs pengeluaran Rp8 juta: dengan skill pos fleksibel dipangkas tanpa menyentuh kiriman ibu dan sekolah anak; tanpa skill disarankan mengurangi kiriman ibu.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-01; muat CLI) dan bot Telegram asli. Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli. Skill orisinal Komunitech (terinspirasi proyek open-source berlisensi MIT; atribusi di `ATTRIBUTION.md`). Bukan nasihat keuangan berlisensi.

## Bukti uji di bot Telegram

Diuji di bot Telegram uji (bot OpenClaw asli di grup uji internal Komunitech), 2 Oktober 2026, dengan pesan yang sama untuk dua sisi (tanpa skill dan dengan skill). Uji ini tampil di bot tanpa skor angka, dan versi skill yang diuji tidak tercatat (lebih lama dari 1.0.7), jadi tidak ada angka "tanpa skill → dengan skill" maupun vonis lulus acuan kami untuk uji ini.

Dengan skill, anggaran dihitung skrip sehingga setiap rupiah punya tugas dan sisanya nol rupiah. Tanpa skill, bot menyusun anggaran dan dana darurat 6–9 kali pengeluaran tanpa hitungan yang pasti.

Catatan jujur: pada uji ini THR sempat terhitung dua kali (dimasukkan ke pemasukan bulanan, lalu masih disuruh disimpan lagi). Hal itu diperbaiki di versi 1.0.7 dan diuji ulang di OpenClaw, belum di bot Telegram. Uji lain: uji OpenClaw otomatis 1–2 Oktober 2026, 6,5 → 9,0 (lihat di atas).

## FAQ
**Apakah skill ini menyarankan investasi tertentu?**
Tidak. Skill ini tidak merekomendasikan beli/jual saham, kripto, reksa dana, emas, atau produk bank/fintech tertentu. Imbal hasil hanya dipakai sebagai asumsi yang Anda tentukan sendiri.

**Data keuangan saya dikirim ke mana?**
Tidak ke mana-mana oleh skill ini. Script berjalan di komputer Anda, tanpa internet, dan tidak menyimpan file.

**Apakah hasilnya pasti tepat?**
Rumus hitungannya sudah diverifikasi secara independen, tetapi hasilnya simulasi: bunga bisa berubah, ada denda/biaya admin, dan hidup tidak selalu sesuai rencana. Ini **bukan nasihat keuangan**; untuk kasus rumit, konsultasikan ke perencana keuangan bersertifikat. Aturan OJK/BI dicek 26 September 2026.

**Bunga KTA saya "0,9% per bulan", apakah dihitung benar?**
Ya. Sebutkan satuannya (per bulan/per tahun). Kalau satuannya tidak jelas, AI akan menanyakan dulu — karena 0,9% per bulan flat (tenor 24 bulan) ternyata setara ±19,5% per tahun efektif, sedangkan 0,9% per tahun hanya ±1,7%.

## Riwayat perubahan

Versi terkini: **1.0.13**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
