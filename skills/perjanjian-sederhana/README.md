# Draf Surat Perjanjian Usaha dalam Hitungan Menit

**Ceritakan kesepakatanmu, dapat draf perjanjian berpasal lengkap, angka dan terbilang sudah dicek, plus checklist sebelum tanda tangan.**

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

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah perjanjian ini sah secara hukum?**
Perjanjian sah jika memenuhi 4 syarat Pasal 1320 KUHPerdata: sepakat, cakap, objek jelas, dan sebab yang halal. Skill ini membantu memastikan keempatnya tertulis jelas. Hasilnya tetap draf, bukan nasihat hukum. Untuk nilai besar atau kasus rumit, mintalah pengacara meninjaunya.

**Tanpa meterai, perjanjiannya tidak sah?**
Tetap sah. Meterai Rp10.000 adalah pajak atas dokumen (UU 10/2020), bukan syarat sah perjanjian. Tapi surat perjanjian memang wajib bermeterai, dan meterai dibutuhkan bila dokumen dipakai sebagai bukti di pengadilan. Skill ini selalu menyiapkan tempat meterainya.

**Bisa untuk jual beli tanah atau perjanjian dengan investor asing?**
Tidak. Transaksi seperti jual beli tanah, investasi atau saham, kerja sama dengan pihak asing, pinjaman dengan jaminan, dan kontrak karyawan harus ditangani notaris, PPAT, atau pengacara. Untuk kasus seperti ini, skill akan menjelaskan alasannya, lalu membantu menyiapkan daftar dokumen dan pertanyaan untuk dibawa saat konsultasi.

## Catatan revisi 1.0.4 (2026-10-01)
- Tanggal penandatanganan tidak lagi diisi otomatis dengan tanggal hari ini; bila belum disebut, draf memuat `[isi: tanggal]`.
- Nilai bawaan template (mis. denda keterlambatan 0,1%/hari maks. 5%) kini selalu dicantumkan sebagai asumsi yang perlu kamu konfirmasi.

## Catatan revisi 1.0.5 (2026-10-03)
- Naskah perjanjian lengkap kini selalu ditampilkan langsung di chat (dipecah rapi per pasal bila panjang) sehingga bisa disalin, tidak hanya disimpan sebagai file.
- Ada pengecekan konsistensi biaya: listrik, air, iuran/retribusi pasar, PBB, dan perbaikan masing-masing ditanggung satu pihak dan sama di semua pasal maupun daftar asumsi. Pemeriksa draf otomatis menandai bila bertentangan.
- Tetap: draf ini bukan nasihat hukum.

## Catatan revisi 1.0.6 (2026-10-03)
- Pasal pengakhiran sewa tempat & sewa alat kini memakai jalur yang sah: teguran tertulis, tenggat, lalu musyawarah atau pengadilan. Tidak ada lagi pengosongan/pengambilan paksa sebagai bawaan.
- Bila kamu sendiri meminta klausul pengosongan sepihak, skill menampilkannya sebagai opsi dengan peringatan risiko hukumnya. Pemeriksa draf menandai klausul seperti ini.
