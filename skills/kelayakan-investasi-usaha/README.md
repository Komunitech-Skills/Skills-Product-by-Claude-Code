# Cek Layak Investasi Sebelum Keluar Uang

**Beli mesin, buka cabang, atau beli mobil usaha? Ketahui kapan balik modal dan seberapa kuat rencananya kalau hasil meleset, dengan hitungan yang transparan.**

Diuji AI penguji independen di bot Telegram asli: 6,5 → 9 dari 10 (keduanya benar soal balik modal, tetapi hanya dengan skill ada NPV, IRR, uji "kalau meleset", dan batas aman).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Jawaban tegas: **layak / kurang layak / tidak layak**, lengkap dengan alasan dan syarat agar tetap layak
- ✅ Tahu **kapan balik modal** (biasa dan memperhitungkan nilai waktu uang), NPV (untung bersih dalam uang hari ini) pada patokan 12% **dan uji ketat 20%**, IRR (imbal hasil per tahun), dan omzet minimal per bulan
- ✅ Uji "kalau meleset": omzet turun 10–20% atau biaya naik 10% — dan **batas aman** sebelum rencana jadi rugi
- ✅ Cocok untuk investasi penghematan juga (beli mobil box vs sewa ekspedisi, beli mesin vs maklon)
- ✅ Pajak (PPh final 0,5% atau pajak penghasilan badan) dan nilai jual kembali alat bisa ikut dihitung; angkanya dihitung lewat skrip, bukan dikira

## Cocok untuk siapa
- Pemilik kafe, warung, toko, bengkel, konveksi, katering yang mau menambah alat atau cabang
- Pengusaha yang ingin membandingkan dua pilihan sebelum belanja modal
- Pendamping UMKM, konsultan, dan admin keuangan yang menyiapkan studi kelayakan sederhana

## Contoh sebelum & sesudah
**Sebelum:** "Kayaknya mesin espresso 45 juta cepat balik modal, jualan nambah 6 juta sebulan." Tidak ada hitungan bahan baku, biaya rutin, atau risiko kalau sepi.

**Sesudah (cukup ketik):** "Mau beli mesin espresso 45 juta. Tambahan jualan 6 juta sebulan, bahan baku 40%, listrik+servis+part-time 1,2 juta sebulan, mesin bekas laku 5 juta setelah 5 tahun, saya bayar PPh final 0,5%. Layak nggak?"

Cuplikan contoh keluaran (dipotong; angkanya dicocokkan dengan hitungan independen; `examples/01-mesin-kopi-45jt.md`):

**Mesin espresso Rp45 juta: LAYAK (dengan asumsi di bawah)**
Modal kembali dalam ±1 tahun 7 bulan, dan imbal hasilnya 57,3% per tahun — jauh di atas patokan 12%.

| Ukuran | Hasil | Arti |
|---|---|---|
| Balik modal | 1 tahun 7 bulan | modal kembali dari uang bersih |
| NPV | Rp60.356.969 | kelebihan untung setara uang hari ini, patokan 12% |
| NPV uji ketat 20% | Rp42.062.397 | tetap positif dengan patokan 20%/tahun |
| IRR | 57,3%/tahun | layak bila > 12% |

**Kalau meleset (NPV):** omzet −10% → Rp44.914.108 · omzet −20% → Rp29.471.247 · biaya +10% → Rp44.784.336. Ketiganya tetap layak.
**Syarat:** omzet tambahan tidak turun lebih dari 39,1% (minimal ±Rp3.654.956/bulan) dan biaya tidak naik lebih dari 38,8%.

Hasil asli juga memuat asumsi yang dipakai dan 1–3 pertanyaan untuk mempertajam hitungan.

Contoh lain di folder `examples/`: buka cabang Rp250 juta (**kurang layak**: turun 10% saja sudah rugi) dan mobil box Rp180 juta vs sewa ekspedisi (**kurang layak**: bergantung harga jual kembali).

## Cara pakai
Ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buka cabang modal 250 juta, omzet tahun pertama 380 juta, kapan balik modal?"
- "Lebih untung beli mobil box 180 juta atau tetap sewa 6,5 juta sebulan?"
- "Mesin bordir 85 juta, minimal harus menghasilkan berapa sebulan supaya layak?"

## Instalasi singkat
Salin folder `kelayakan-investasi-usaha` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Tidak perlu akun, API key, atau instalasi tambahan; hitungan memakai Python standar dan berjalan di komputer Anda.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 11, 2026-10-06.
- Tanpa skill: https://t.me/c/4407409583/908/950 — skor 6,5
- Dengan skill: https://t.me/c/4407409583/909/952 — skor 9
Verdik gelombang: LULUS — Keduanya benar soal payback ±1 th 1 bln, tetapi hanya dengan skill ada NPV/IRR/payback terdiskonto, uji meleset −10%/−20%/+10%, batas aman, asumsi diskonto & disclaimer, semuanya cocok dengan hitungan ulang.

- Pilot 26 (kirim ulang 4 pesan di topik baru, 2026-10-12, dijalankan Akun C): skor 6,5 → 9, verdik LULUS — hasil sama dengan gelombang 11 dan 11b (`koordinasi/telegram-gelombang-11b-pilot-2026-10-12.md`; tautan pesan tidak tercatat di log).

## FAQ
**Apakah hasilnya menjamin usaha saya untung?**
Tidak. Hasil tergantung perkiraan omzet dan biaya yang Anda masukkan. Karena itu skill menampilkan skenario "kalau meleset" dan batas aman. Ini alat bantu, bukan nasihat keuangan.

**Kenapa patokannya 12% per tahun?**
Itu asumsi awal: bunga KUR 6% efektif ditambah tambahan risiko usaha 6%. Anda bisa menggantinya dengan bunga pinjaman Anda sendiri atau hasil minimal yang Anda inginkan, dan skill akan menghitung ulang.

**Bisa untuk menilai saham, kripto, atau reksa dana?**
Tidak. Skill ini khusus investasi di usaha sendiri (alat, cabang, kendaraan, renovasi). Kalau Anda bertanya "pasti untung berapa kalau di kripto?", AI diarahkan menolak janji untung dengan sopan, menyarankan penasihat keuangan berizin OJK, lalu menawarkan hitungan rencana usaha Anda.

## Riwayat perubahan

Versi terkini: **1.0.3**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
