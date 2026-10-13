# Draf Surat Perjanjian Usaha Berpasal Lengkap

**Ceritakan kesepakatan Anda, dapat draf perjanjian berpasal lengkap, angka dan terbilang sudah dicek, plus checklist sebelum tanda tangan.**

Diuji AI penguji independen di OpenClaw: 4,25 → 9,0 dari 10 (pembedanya: tanpa skill menuliskan klausul jaminan BPKB, yaitu surat kepemilikan motor, yang batal demi hukum; dengan skill dijelaskan Pasal 33 UU Fidusia, aturan jaminan atas barang bergerak seperti kendaraan, dan draf sewa/utang dilengkapi meterai).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tujuh jenis perjanjian yang paling sering dipakai UMKM: reseller/distributor, supplier, NDA (kerahasiaan), sewa tempat, sewa alat, bagi hasil, dan jasa freelance
- ✅ Susunan pasal lazim di Indonesia: para pihak, ruang lingkup, hak & kewajiban, pembayaran, jangka waktu, wanprestasi (ingkar janji), keadaan memaksa, penyelesaian sengketa, tanda tangan & meterai
- ✅ Angka dihitung dengan skrip dan dicek ulang supaya lebih kecil kemungkinan salah tulis: terbilang, pembagian DP (uang muka)/termin (pembayaran bertahap), bagi hasil, dan denda
- ✅ Pasal berisiko diberi tanda ⚠ agar Anda tahu bagian mana yang sebaiknya ditanyakan ke pengacara
- ✅ Checklist "sebelum tanda tangan" berbahasa awam: cek identitas, kewenangan, meterai Rp10.000, paraf, dan penyimpanan dokumen

## Cocok untuk siapa
- Pemilik brand yang merekrut reseller atau bekerja sama dengan supplier
- Penyewa atau pemilik kios, ruko, dan lapak, serta usaha penyewaan alat
- Freelancer (desainer, fotografer, penulis, developer) dan kliennya
- Teman atau keluarga yang patungan usaha dengan sistem bagi hasil

## Contoh sebelum & sesudah
**Sebelum:** Kesepakatan cuma lewat chat WA. Saat klien telat bayar atau minta revisi terus, tidak ada pegangan tertulis.

**Sesudah (cukup ketik):** "bikinin dong surat perjanjian freelance, aku desain feed IG buat klien kafe 3 bulan, 4,5jt. cepet ya"

Cuplikan hasil (dari uji simulasi Claude Code, data fiktif; dipotong dari `examples/03-bikinin-dong-freelance-feed-ig.md`):
> **⚠ Draf ini bukan nasihat hukum.** Kontrak jasa desain feed Instagram 3 bulan, Rp 4.500.000. …
>
> …
>
> ## Pasal 3
>
> ### Biaya Jasa dan Pembayaran
>
> (1) Biaya jasa untuk seluruh Pekerjaan adalah Rp 4.500.000 (empat juta lima ratus ribu rupiah).
>
> (2) Pembayaran dilakukan secara bertahap:
>
> a. uang muka 50% sebesar Rp 2.250.000 (dua juta dua ratus lima puluh ribu rupiah) paling lambat saat Perjanjian ditandatangani;
>
> b. pelunasan 50% sebesar Rp 2.250.000 (dua juta dua ratus lima puluh ribu rupiah) paling lambat 3 (tiga) hari kerja setelah seluruh desain bulan ketiga disetujui.

Hasil lengkapnya berisi 11 pasal, daftar isian yang belum lengkap, pasal yang perlu ditinjau, dan checklist sebelum tanda tangan.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Bikinkan surat perjanjian sewa kios 1 tahun, 18 juta, bayar di muka"
- "Aku mau rekrut reseller keripik, tolong buatkan perjanjiannya"
- "Tolong cek draf perjanjian ini, ada yang kurang nggak?" (lampirkan file .md/.txt)

## Instalasi singkat
Salin folder `perjanjian-sederhana` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw (lingkungan uji terpisah), 1–3 Okt 2026 (v1.0.6), skor 1–10 penguji independen: tanpa skill **4,25** → dengan skill **9,0** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Tanpa skill menuliskan klausul jaminan BPKB yang batal demi hukum; dengan skill menjelaskan Pasal 33 UU Fidusia dan menyiapkan draf sewa/utang lengkap dengan meterai.

**Status uji (jujur):** draf bukan nasihat hukum. Sudah diuji di OpenClaw (uji otomatis agent) dan bot Telegram uji; Codex dan Cursor belum diuji langsung (format skill-nya sama). Untuk kasus bernilai besar, PERLU REVIEW notaris/pengacara sebelum dipakai.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 5, 2026-10-03.
- Tanpa skill: https://t.me/c/4407409583/633/657 — skor 6
- Dengan skill: https://t.me/c/4407409583/634/661 — skor 6,5
Verdik gelombang: BELUM — DENGAN lebih benar isinya (jadwal 4 cicilan, total Rp36 jt, peringatan status hak pakai kios pasar, meterai), tetapi **file perjanjian lengkap gagal terkirim** sehingga pengguna hanya menerima ringkasan; TANPA memberi naskah utuh siap cetak meski lebih tipis.

Kekurangan ini diperbaiki di versi 1.0.5–1.0.6 (naskah utuh tampil di chat, biaya dicek konsisten, tanpa pengosongan sepihak sebagai bawaan); sudah diuji ulang di OpenClaw lokal, belum diuji ulang di bot Telegram.

## FAQ
**Apakah perjanjian ini sah secara hukum?**
Perjanjian sah jika memenuhi 4 syarat Pasal 1320 KUHPerdata: sepakat, cakap, objek jelas, dan sebab yang halal. Skill ini membantu agar keempatnya tertulis jelas. Hasilnya tetap draf, bukan nasihat hukum. Untuk nilai besar atau kasus rumit, mintalah pengacara meninjaunya.

**Tanpa meterai, perjanjiannya tidak sah?**
Umumnya tetap sah, asalkan keempat syarat di atas terpenuhi. Meterai Rp10.000 adalah pajak atas dokumen (UU 10/2020), bukan syarat sah perjanjian. Tapi surat perjanjian memang wajib bermeterai, dan meterai dibutuhkan bila dokumen dipakai sebagai bukti di pengadilan. Skill ini menyiapkan tempat meterai pada draf (periksa lagi sebelum dicetak).

**Bisa untuk jual beli tanah atau perjanjian dengan investor asing?**
Sebaiknya jangan. Transaksi seperti jual beli tanah, investasi atau saham, kerja sama dengan pihak asing, pinjaman dengan jaminan, dan kontrak karyawan harus ditangani notaris, PPAT (pejabat pembuat akta tanah), atau pengacara. Untuk kasus seperti ini, skill akan menjelaskan alasannya, lalu membantu menyiapkan daftar dokumen dan pertanyaan untuk dibawa saat konsultasi.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
