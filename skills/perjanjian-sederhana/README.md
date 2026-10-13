# Draf Surat Perjanjian Usaha dalam Hitungan Menit

**Ceritakan kesepakatanmu, dapat draf perjanjian berpasal lengkap, angka dan terbilang sudah dicek, plus checklist sebelum tanda tangan.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tujuh jenis perjanjian yang paling sering dipakai UMKM: reseller/distributor, supplier, NDA (kerahasiaan), sewa tempat, sewa alat, bagi hasil, dan jasa freelance
- ✅ Susunan pasal lazim di Indonesia: para pihak, ruang lingkup, hak & kewajiban, pembayaran, jangka waktu, wanprestasi, keadaan memaksa, penyelesaian sengketa, tanda tangan & meterai
- ✅ Angka tidak salah tulis. Terbilang, pembagian DP/termin, bagi hasil, dan denda dihitung otomatis dan dicek ulang
- ✅ Pasal berisiko diberi tanda ⚠ agar kamu tahu bagian mana yang sebaiknya ditanyakan ke pengacara
- ✅ Checklist "sebelum tanda tangan" berbahasa awam: cek identitas, kewenangan, meterai Rp10.000, paraf, dan penyimpanan dokumen

## Cocok untuk siapa
- Pemilik brand yang merekrut reseller atau bekerja sama dengan supplier
- Penyewa atau pemilik kios, ruko, dan lapak, serta usaha penyewaan alat
- Freelancer (desainer, fotografer, penulis, developer) dan kliennya
- Teman atau keluarga yang patungan usaha dengan sistem bagi hasil

## Contoh sebelum & sesudah
**Sebelum:** Kesepakatan cuma lewat chat WA. Saat klien telat bayar atau minta revisi terus, tidak ada pegangan tertulis.

**Sesudah (cukup ketik):** "Buatin kontrak freelance desain logo, harga 7,5 juta, DP 50%, revisi 2x, selesai 3 minggu"
→ Draf "Perjanjian Jasa Desain" 11 pasal dengan termin "Rp 3.750.000 (tiga juta tujuh ratus lima puluh ribu rupiah)", batas revisi, hak atas hasil karya, dan aturan pembatalan. Juga disertakan daftar isian yang belum lengkap, pasal yang perlu ditinjau, dan checklist sebelum tanda tangan.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Bikinkan surat perjanjian sewa kios 1 tahun, 18 juta, bayar di muka"
- "Aku mau rekrut reseller keripik, tolong buatkan perjanjiannya"
- "Tolong cek draf perjanjian ini, ada yang kurang nggak?" (lampirkan file .md/.txt)

## Instalasi singkat
Salin folder `perjanjian-sederhana` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap per platform (termasuk Windows): lihat `docs/instalasi.md` dan `CARA-INSTAL.md` di paket.

**Hasil uji (angka nyata):** uji OpenClaw (home terisolasi), 1–3 Okt 2026 (v1.0.6), skor 1–10 penguji independen: tanpa skill **4,25** → dengan skill **9,0** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Tanpa skill menuliskan klausul jaminan BPKB yang batal demi hukum; dengan skill menjelaskan Pasal 33 UU Fidusia dan menyiapkan draf sewa/utang lengkap dengan meterai.

**Status uji (jujur):** draf bukan nasihat hukum. Sudah diuji di OpenClaw (uji otomatis agent) dan bot Telegram uji. PERLU REVIEW pemilik untuk kasus nilai besar — konsultasikan notaris/pengacara.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 5, 2026-10-03.
- Tanpa skill: https://t.me/c/4407409583/633/657 — skor 6
- Dengan skill: https://t.me/c/4407409583/634/661 — skor 6,5
Verdik gelombang: BELUM — DENGAN lebih benar isinya (jadwal 4 cicilan, total Rp36 jt, peringatan status hak pakai kios pasar, meterai), tetapi **file perjanjian lengkap gagal terkirim** sehingga pengguna hanya menerima ringkasan; TANPA memberi naskah utuh siap cetak meski lebih tipis.

## FAQ
**Apakah perjanjian ini sah secara hukum?**
Perjanjian sah jika memenuhi 4 syarat Pasal 1320 KUHPerdata: sepakat, cakap, objek jelas, dan sebab yang halal. Skill ini membantu memastikan keempatnya tertulis jelas. Hasilnya tetap draf, bukan nasihat hukum. Untuk nilai besar atau kasus rumit, mintalah pengacara meninjaunya.

**Tanpa meterai, perjanjiannya tidak sah?**
Tetap sah. Meterai Rp10.000 adalah pajak atas dokumen (UU 10/2020), bukan syarat sah perjanjian. Tapi surat perjanjian memang wajib bermeterai, dan meterai dibutuhkan bila dokumen dipakai sebagai bukti di pengadilan. Skill ini selalu menyiapkan tempat meterainya.

**Bisa untuk jual beli tanah atau perjanjian dengan investor asing?**
Tidak. Transaksi seperti jual beli tanah, investasi atau saham, kerja sama dengan pihak asing, pinjaman dengan jaminan, dan kontrak karyawan harus ditangani notaris, PPAT, atau pengacara. Untuk kasus seperti ini, skill akan menjelaskan alasannya, lalu membantu menyiapkan daftar dokumen dan pertanyaan untuk dibawa saat konsultasi.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
