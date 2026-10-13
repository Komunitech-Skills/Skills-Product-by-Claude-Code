# Foto Nota Jadi Tabel Excel, Sudah Dicek

**Kirim foto nota, struk, atau faktur pajak. Dapat tabel rapi, hitungan yang sudah dicek, dan rekap pengeluaran.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tidak perlu mengetik ulang nota satu per satu. Hasilnya tabel dan CSV yang bisa langsung ditempel ke Excel atau Google Sheets
- ✅ Hitungan dicek otomatis: harga × jumlah, subtotal, PPN, total, sampai terbilang. Selisih sekecil apa pun terlihat
- ✅ Sesuai aturan PPN terbaru (12% dengan DPP nilai lain 11/12). Faktur yang menagih PPN terlalu besar langsung ditandai
- ✅ Foto buram tidak ditebak. Kolom yang tidak terbaca ditandai jelas supaya Anda cek sendiri
- ✅ Banyak nota sekaligus jadi rekap pengeluaran per kategori, per toko, dan per bulan

## Cocok untuk siapa
- Pemilik usaha yang tiap bulan menumpuk nota belanja bahan dan operasional
- Admin keuangan yang harus menginput nota dan faktur pajak supplier ke spreadsheet
- Karyawan yang mengurus reimburse, dan freelancer yang mencatat pengeluaran

## Contoh sebelum & sesudah
**Sebelum:** Mengetik 30 nota ke Excel butuh 1–2 jam. Kesalahan PPN di faktur supplier sering lolos karena tidak ada yang menghitung ulang.

**Sesudah (cukup ketik):** "Tolong masukkan 6 foto nota ini ke Excel dan cek angkanya."
→ Tabel 6 dokumen dengan status masing-masing, lalu:
- "Invoice jasa website: PPN ditulis Rp 960.000 (12% penuh). Untuk jasa biasa seharusnya Rp 880.000. Tanyakan ke penjual."
- "Kuitansi Pak Darto: terbilang tertulis enam juta tujuh ratus ribu, padahal angkanya Rp 6.750.000."
- "Nota Toko Bu Yati: total tidak terbaca (terlihat 3?1.500). Mohon cek nota aslinya."
- Rekap: total pengeluaran, PPN, per kategori, per toko, dan CSV siap tempel.

**Hasil uji (OpenClaw, uji otomatis agent, 1 Oktober 2026):** rata-rata nilai 6,0 tanpa skill menjadi 9,0 dengan skill (skala 10). Invoice jasa cetak dengan "PPN 12% = Rp 180.000" atas DPP Rp 1.500.000 dinyatakan sesuai oleh agent tanpa skill; dengan skill ditemukan PPN seharusnya Rp 165.000 (total Rp 1.665.000, kelebihan Rp 15.000). Pada faktur yang fotonya buram ("92?.000"), digit tidak ditebak: ditandai TIDAK TERBACA, lalu dibandingkan dengan hasil hitung yang jelas diberi label "dihitung, bukan dibaca". Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Setelah terpasang, kirim foto atau teks dokumen ke AI agent Anda, lalu ketik permintaan biasa, misalnya:
- "Ketik ulang nota-nota ini ke tabel Excel."
- "Cek faktur pajak dari supplier ini, PPN-nya sudah benar?"
- "Rekap pengeluaran bulan September dari foto-foto struk ini, per kategori."
- "Buatkan CSV pakai pemisah titik koma."

## Instalasi singkat
Salin folder `ekstrak-nota-faktur` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

## FAQ
**AI agent saya harus bisa membaca foto?**
Ya, untuk foto dibutuhkan AI agent yang bisa melihat gambar (kebanyakan agent sekarang bisa). Jika tidak, Anda bisa menempelkan teks nota atau hasil scan PDF.

**Kalau fotonya buram, apakah angkanya dikira-kira?**
Tidak. Angka yang tidak terbaca ditulis "TIDAK TERBACA" dan tidak ikut dijumlah. Anda akan diberi tahu bagian mana yang perlu dicek atau difoto ulang.

**Apakah skill ini bisa memastikan faktur pajak asli?**
Tidak. Skill ini mengecek hitungan dan format nomor, lalu memberi peringatan bila ada yang janggal. Keaslian faktur tetap dicek lewat Coretax atau QR code resmi, dan untuk urusan kredit PPN atau SPT silakan hubungi konsultan pajak atau Kring Pajak 1500200.

> **Catatan penting:** alat bantu mengetik ulang dan mengecek hitungan, bukan nasihat pajak. Dasar aturan PPN (berlaku per 23 September 2026): UU HPP dan PMK 131/2024, yaitu PPN 12% × DPP nilai lain 11/12 untuk barang/jasa non-mewah dan 12% dari harga penuh hanya untuk barang mewah. Pembulatan belum dicocokkan dengan Coretax; bila berbeda, ikuti Coretax. Format NPWP, NITKU, dan nomor faktur hanya diperiksa sebagai peringatan (belum diverifikasi dari dokumen resmi), dan skill tidak memutuskan PPN bisa dikreditkan. Kepastian: Kring Pajak 1500200 atau konsultan pajak.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
