# Tahu Harga Asli Cicilan Sebelum Tanda Tangan

**"Bunganya cuma 0,8% sebulan" — sebenarnya berapa? Hitung cicilan, total bunga, dan bunga efektif dalam satu kalimat.**

## Manfaat
- ✅ Cicilan per bulan, total bayar, total bunga, dan **total harga lewat kredit vs harga tunai** — langsung jelas
- ✅ **Bunga efektif setara per tahun** yang sudah memasukkan admin, provisi, dan asuransi, sehingga penawaran flat dan efektif bisa dibandingkan dengan adil
- ✅ Jadwal angsuran (pokok, bunga, sisa utang) dan perbandingan flat vs anuitas dalam rupiah
- ✅ Cocok untuk motor, mobil, HP, KPR (termasuk fixed lalu floating), leasing, koperasi, KTA, paylater, sampai pinjaman harian
- ✅ **Cicilan maksimal aman** dari gaji bersihmu, plus peringatan bila cicilan terasa berat — semua angka dihitung, bukan dikira

## Cocok untuk siapa
- Karyawan, ibu rumah tangga, dan pelaku usaha yang mau ambil kredit motor, HP, mobil, atau rumah
- Siapa saja yang bingung membandingkan dua penawaran kredit
- Staf penjualan dealer/koperasi yang ingin membuat simulasi dan brosur kredit yang transparan

## Contoh sebelum & sesudah
*(akan diisi dari hasil uji)*

## Cara pakai
Ketik permintaan biasa ke AI agent kamu, misalnya:
- "Motor 25 juta, DP 20%, 3 tahun, bunga 0,8% per bulan. Cicilannya berapa? Mahal nggak?"
- "Pinjam 30 juta, cicilannya 1,5 juta selama 24 bulan. Bunganya sebenarnya berapa persen?"
- "Gaji bersih 6 juta, sudah ada cicilan 500 ribu. Maksimal aman cicil berapa?"

## Instalasi singkat
Salin folder `simulasi-cicilan-pinjaman` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket. Tidak perlu akun, API key, atau instalasi tambahan; hitungan memakai Python standar dan berjalan di komputermu.

## FAQ
**Apakah angkanya pasti sama dengan tabel dari bank/leasing?**
Rumusnya standar dan dibulatkan per rupiah, tetapi tiap lembaga bisa memakai pembulatan dan biaya yang berbeda. Pakai hasil ini untuk memahami dan membandingkan; angka final tetap dari tabel angsuran resmi.

**Apa bedanya bunga flat dan efektif?**
Flat menghitung bunga dari pinjaman awal sampai lunas; efektif menghitung dari sisa utang. Pada angka yang sama, flat jauh lebih mahal — misalnya flat 0,8% per bulan setara bunga efektif sekitar 17% per tahun.

**Bisa menyarankan bank atau aplikasi pinjaman yang paling murah?**
Tidak. Skill ini tidak menyebut atau merekomendasikan merek. Kirimkan angka dari penawaran yang kamu terima, dan AI akan membandingkannya dengan bunga efektif setara dan total biaya.

---
Sebagian rumus dan kasus uji diturunkan dari numpy-financial (BSD-3-Clause, © NumPy Developers) — lihat `ATTRIBUTION.md`. Komunitech tidak berafiliasi dengan NumPy. Simulasi, bukan penawaran atau nasihat keuangan.
