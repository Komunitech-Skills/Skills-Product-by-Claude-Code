# Cek Layak Investasi Sebelum Keluar Uang

**Beli mesin, buka cabang, atau beli mobil usaha? Ketahui kapan balik modal dan seberapa kuat rencananya kalau hasil meleset, dengan hitungan yang transparan.**

Diuji AI penguji independen di OpenClaw dan bot Telegram asli: 6,5 → 9 dari 10 (keduanya benar soal balik modal, tetapi hanya dengan skill ada NPV, IRR, uji "kalau meleset" lengkap (omzet turun 10–20%, biaya naik 10%), dan batas aman).

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

Cuplikan contoh keluaran (dipotong; contoh buatan pembuat skill, bukan hasil uji penguji independen; angkanya dari skrip dan dicocokkan dengan hitungan Python terpisah; `examples/01-mesin-kopi-45jt.md`):

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

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, 5 Okt 2026 (v1.0.1), skor 1–10 dari penguji independen, 2 skenario: tanpa skill **6,5** → dengan skill **9,0** (LULUS). Skor tanpa skill diambil dari uji sebelumnya (v1.0.0) karena tidak terpengaruh perubahan skill. Beli mesin kopi Rp45 juta (tambahan omzet Rp6 juta/bulan, biaya Rp2,5 juta/bulan): kedua sisi sama-sama menyimpulkan layak dengan balik modal sekitar 1 tahun 1 bulan, tetapi tanpa skill AI menulis titik impas harian ±Rp200.000 (yang benar ±Rp83.000), tanpa NPV/IRR, dan tanpa catatan "bukan nasihat keuangan". Dengan skill ada NPV Rp109.237.735 (patokan 12%), IRR 89,96% per tahun, uji omzet turun 10–20%, dan batas aman, semuanya cocok dengan hitungan Python terpisah. Pertanyaan "pasti untung di kripto?": kedua sisi menolak janji untung, tetapi tanpa skill AI malah menawarkan proyeksi kripto dan perbandingan deposito/reksa dana tanpa disclaimer; dengan skill ada disclaimer dan arahan ke penasihat berizin OJK. Jujur: pada skenario tambahan mobil box Rp180 juta (8/10, di luar rata-rata) angkanya benar, tetapi satu kalimat penjelasnya keliru (4 tahun 3 bulan ditulis "lebih lama dari 5 tahun"). Sumber: `examples/00-openclaw-sebelum-sesudah.md`.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent, termasuk konteks kanal Telegram) dan di bot Telegram OpenClaw asli. Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot Telegram uji (bot OpenClaw asli di grup uji Komunitech; tautan pesan hanya terbuka untuk anggota grup), 6 Okt 2026, pesan yang sama dikirim tanpa skill lalu dengan skill:
- Tanpa skill: skor 6,5
- Dengan skill: skor 9
Hasilnya lulus. Keduanya benar soal balik modal (±1 tahun 1 bulan), tetapi hanya dengan skill ada NPV, IRR, balik modal dengan nilai waktu uang, uji omzet turun 10%/20% dan biaya naik 10%, batas aman, asumsi patokan 12%, dan catatan bukan nasihat keuangan; semuanya cocok dengan hitungan ulang.

Uji ulang di bot Telegram uji, 12 Okt 2026: skor 6,5 → 9, lulus, hasil sama dengan uji pertama.

## FAQ
**Apakah hasilnya menjamin usaha saya untung?**
Hasilnya tidak menjamin usaha Anda untung, karena semuanya tergantung perkiraan omzet dan biaya yang Anda masukkan. Karena itu skill menampilkan skenario "kalau meleset" dan batas aman. Ini alat bantu, bukan nasihat keuangan.

**Kenapa patokannya 12% per tahun?**
Itu asumsi awal, bukan acuan pasar: bunga KUR (Kredit Usaha Rakyat) Mikro/Kecil sektor produksi 6% efektif per tahun (Peraturan Menteri Koordinator Bidang Perekonomian No. 1 Tahun 2026 tentang Pedoman Pelaksanaan KUR, Pasal 37 & 44, berlaku sejak 13 Januari 2026; teks pasalnya sudah dicek penguji independen pada 13 Oktober 2026 dan dicocokkan ulang dengan salinan resmi JDIH BPK pada 15 Oktober 2026, tetapi aturan bisa berubah, jadi konfirmasi ke bank penyalur) ditambah premi risiko usaha 6% yang kami pilih sebagai contoh. Anda bisa menggantinya dengan bunga pinjaman Anda sendiri atau hasil minimal yang Anda inginkan, dan skill akan menghitung ulang.

**Bisa untuk menilai saham, kripto, atau reksa dana?**
Skill ini khusus untuk investasi di usaha sendiri (alat, cabang, kendaraan, renovasi), jadi tidak bisa dipakai untuk menilai saham, kripto, atau reksa dana. Kalau Anda bertanya "pasti untung berapa kalau di kripto?", AI diarahkan menolak janji untung dengan sopan, menyarankan penasihat keuangan berizin OJK, lalu menawarkan hitungan rencana usaha Anda.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
