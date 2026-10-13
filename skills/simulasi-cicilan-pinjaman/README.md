# Tahu Harga Asli Cicilan Sebelum Tanda Tangan

**"Bunganya cuma 0,8% sebulan" — sebenarnya berapa? Hitung cicilan, total bunga, dan bunga efektif dalam satu kalimat.**

Diuji AI penguji independen di bot Telegram asli: 6 → 8,5 dari 10 (tanpa skill menaksir bunga kredit HP "kira-kira 44-45%" setahun padahal ±41,7%; dengan skill bunga flat 0,8% sebulan terlihat setara ±17,25% per tahun).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Cicilan per bulan, total bayar, total bunga, dan **total harga lewat kredit vs harga tunai** — langsung jelas
- ✅ **Bunga efektif setara per tahun** (bunga yang dihitung dari sisa utang) yang sudah memasukkan biaya admin, provisi (biaya pencairan), dan asuransi, sehingga penawaran bunga "flat" (dihitung dari pokok awal terus) dan efektif bisa dibandingkan dengan adil
- ✅ Jadwal angsuran (pokok, bunga, sisa utang) dan perbandingan flat vs anuitas (cicilan tetap dengan bunga dari sisa utang) dalam rupiah
- ✅ Cocok untuk motor, mobil, HP, KPR (kredit rumah, termasuk bunga tetap yang kemudian mengambang), leasing (kredit lewat perusahaan pembiayaan), koperasi, KTA (pinjaman tanpa agunan), paylater (bayar nanti), sampai pinjaman harian
- ✅ **Batas cicilan yang masih aman** dari gaji bersih Anda (patokan hati-hati maks. 30% gaji, asumsi yang bisa diubah, bukan aturan resmi semua lembaga), plus peringatan bila cicilan terasa berat; angkanya dihitung lewat skrip, bukan dikira

## Cocok untuk siapa
- Karyawan, ibu rumah tangga, dan pelaku usaha yang mau ambil kredit motor, HP, mobil, atau rumah
- Siapa saja yang bingung membandingkan dua penawaran kredit
- Staf penjualan dealer/koperasi yang ingin membuat simulasi dan brosur kredit yang transparan

## Contoh sebelum & sesudah
**Sebelum:** "Motor 25 juta, DP 20%, 3 tahun, bunga 0,8% per bulan flat, admin 1 juta." AI biasa menjawab cicilan Rp715.556 per bulan dan bilang "aman" — tanpa memberi tahu berapa mahal sebenarnya.

**Sesudah:** cicilan yang sama, ditambah fakta yang biasanya tidak terlihat. Cuplikan keluaran uji (v1.0.1, dipotong; `examples/01-motor-flat-admin-gaji.md`):

> **Simulasi cicilan motor — Rp25.000.000, 36 bulan**
> Cicilan: **Rp715.556/bulan** (36 kali, terakhir Rp715.540) · Total bayar Rp25.760.000 · Total bunga Rp5.760.000
> Bunga 0,8%/bulan flat = **efektif setara ±17,25%/tahun**; dengan biaya admin **±20,97%/tahun** …
>
> | Hal | Angka |
> |---|---|
> | Harga tunai / DP | Rp25.000.000 / Rp5.000.000 |
> | Pokok pinjaman | Rp20.000.000 |
> | Biaya di muka | Rp1.000.000 (admin) |
> | Total biaya pinjaman | Rp6.760.000 |
> | Total harga lewat kredit | Rp31.760.000 (lebih mahal Rp6.760.000 = 27,0% dari tunai) |

Hasil lengkapnya juga memuat perbandingan dengan anuitas dan batas cicilan aman dari gaji (patokan asumsi, bisa diubah).

## Cara pakai
Ketik permintaan biasa ke AI agent Anda, misalnya:
- "Motor 25 juta, DP 20%, 3 tahun, bunga 0,8% per bulan. Cicilannya berapa? Mahal nggak?"
- "Pinjam 30 juta, cicilannya 1,5 juta selama 24 bulan. Bunganya sebenarnya berapa persen?"
- "Gaji bersih 6 juta, sudah ada cicilan 500 ribu. Maksimal aman cicil berapa?"

## Instalasi singkat
Salin folder `simulasi-cicilan-pinjaman` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Tidak perlu akun, API key, atau instalasi tambahan; hitungan memakai Python standar dan berjalan di komputer Anda.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech): gelombang 14, 2026-10-12.
- Tanpa skill: (pesan di grup uji internal Komunitech) — skor 6
- Dengan skill: (pesan di grup uji internal Komunitech) — skor 8,5
Verdik gelombang: LULUS — Tanpa skill hanya menyebut cicilan Rp715.556 dan menaksir bunga kredit HP "kira-kira 44-45%" setahun (seharusnya ±41,7%); dengan skill terlihat 0,8% flat = ±17,25% per tahun (±20,97% dengan admin), motor jadi 27% lebih mahal dari tunai, dan brosur "bunga 0%" dibuatkan versi jujur.

## FAQ
**Apakah angkanya pasti sama dengan tabel dari bank/leasing?**
Rumusnya standar dan dibulatkan per rupiah, tetapi tiap lembaga bisa memakai pembulatan dan biaya yang berbeda. Pakai hasil ini untuk memahami dan membandingkan; angka final tetap dari tabel angsuran resmi.

**Apa bedanya bunga flat dan efektif?**
Flat menghitung bunga dari pinjaman awal sampai lunas; efektif menghitung dari sisa utang. Pada angka yang sama, flat jauh lebih mahal — misalnya flat 0,8% per bulan setara bunga efektif sekitar 17% per tahun.

**Bisa menyarankan bank atau aplikasi pinjaman yang paling murah?**
Tidak. Skill ini tidak menyebut atau merekomendasikan merek. Kirimkan angka dari penawaran yang Anda terima, dan AI akan membandingkannya dengan bunga efektif setara dan total biaya.

## Riwayat perubahan

Versi terkini: **1.0.3**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
