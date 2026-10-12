# Cek Layak Investasi Sebelum Keluar Uang

**Beli mesin, buka cabang, atau beli mobil usaha? Ketahui kapan balik modal dan seberapa aman, dengan hitungan pasti.**

## Manfaat
- ✅ Jawaban tegas: **layak / kurang layak / tidak layak**, lengkap dengan alasan dan syarat agar tetap layak
- ✅ Tahu **kapan balik modal** (biasa dan memperhitungkan nilai waktu uang), NPV pada patokan 12% **dan uji ketat 20%**, IRR, dan omzet minimal per bulan
- ✅ Uji "kalau meleset": omzet turun 10–20% atau biaya naik 10% — dan **batas aman** sebelum rencana jadi rugi
- ✅ Cocok untuk investasi penghematan juga (beli mobil box vs sewa ekspedisi, beli mesin vs maklon)
- ✅ Pajak (PPh final 0,5% atau PPh badan) dan nilai jual kembali alat bisa ikut dihitung; semua angka dihitung, bukan dikira

## Cocok untuk siapa
- Pemilik kafe, warung, toko, bengkel, konveksi, katering yang mau menambah alat atau cabang
- Pengusaha yang ingin membandingkan dua pilihan sebelum belanja modal
- Pendamping UMKM, konsultan, dan admin keuangan yang menyiapkan studi kelayakan sederhana

## Contoh sebelum & sesudah
**Sebelum:** "Kayaknya mesin espresso 45 juta cepat balik modal, jualan nambah 6 juta sebulan." Tidak ada hitungan bahan baku, biaya rutin, atau risiko kalau sepi.

**Sesudah (cukup ketik):** "Mau beli mesin espresso 45 juta. Tambahan jualan 6 juta sebulan, bahan baku 40%, listrik+servis+part-time 1,2 juta sebulan, mesin bekas laku 5 juta setelah 5 tahun, saya bayar PPh final 0,5%. Layak nggak?"
→ **LAYAK**: balik modal 1 tahun 7 bulan; NPV Rp60.356.969; imbal hasil 57,3% per tahun (patokan 12%). Omzet turun 20% pun masih layak; omzet minimal ±Rp3,65 juta/bulan. Plus asumsi yang dipakai dan 1–3 pertanyaan untuk mempertajam hitungan.

Contoh lain di folder `examples/`: buka cabang Rp250 juta (**kurang layak**: turun 10% saja sudah rugi) dan mobil box Rp180 juta vs sewa ekspedisi (**kurang layak**: bergantung harga jual kembali).

## Cara pakai
Ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buka cabang modal 250 juta, omzet tahun pertama 380 juta, kapan balik modal?"
- "Lebih untung beli mobil box 180 juta atau tetap sewa 6,5 juta sebulan?"
- "Mesin bordir 85 juta, minimal harus menghasilkan berapa sebulan supaya layak?"

## Instalasi singkat
Salin folder `kelayakan-investasi-usaha` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket. Tidak perlu akun, API key, atau instalasi tambahan; hitungan memakai Python standar dan berjalan di komputermu.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 11, 2026-10-06.
- Tanpa skill: https://t.me/c/4407409583/908/950 — skor 6,5
- Dengan skill: https://t.me/c/4407409583/909/952 — skor 9
Verdik gelombang: LULUS — Keduanya benar soal payback ±1 th 1 bln, tetapi hanya dengan skill ada NPV/IRR/payback terdiskonto, uji meleset −10%/−20%/+10%, batas aman, asumsi diskonto & disclaimer, semuanya cocok dengan hitungan ulang.

## FAQ
**Apakah hasilnya menjamin usaha saya untung?**
Tidak. Hasil tergantung perkiraan omzet dan biaya yang kamu masukkan. Karena itu skill selalu menunjukkan skenario "kalau meleset" dan batas aman. Ini alat bantu, bukan nasihat keuangan.

**Kenapa patokannya 12% per tahun?**
Itu asumsi awal: bunga KUR 6% efektif ditambah tambahan risiko usaha 6%. Kamu bisa menggantinya dengan bunga pinjamanmu sendiri atau hasil minimal yang kamu inginkan, dan skill akan menghitung ulang.

**Bisa untuk menilai saham, kripto, atau reksa dana?**
Tidak. Skill ini khusus investasi di usaha sendiri (alat, cabang, kendaraan, renovasi). Kalau kamu bertanya "pasti untung berapa kalau di kripto?", AI akan menolak janji untung dengan sopan, menyarankan penasihat keuangan berizin OJK, lalu menawarkan hitungan rencana usahamu.

## Catatan versi
- **1.0.1 (2026-10-05):** pertanyaan kripto/trading/deposito/"pasti untung" kini tetap memakai skill dengan pola penolakan tetap + arahan ke hitungan usaha; `--nilai-sisa` dan `--nilai-residu` disatukan (hasil identik, omzet impas konsisten); opsi `--jenis penghematan`/`pemasukan` untuk label hasil; NPV uji ketat 20% selalu ditampilkan; rujukan bunga KUR disamakan (Permenko Perekonomian No. 1 Tahun 2026 Pasal 37 & 44); disclaimer wajib di semua balasan.
- **1.0.0 (2026-10-05):** rilis awal.

---
Sebagian rumus dan kasus uji diturunkan dari numpy-financial (BSD-3-Clause, © NumPy Developers) — lihat `ATTRIBUTION.md`. Komunitech tidak berafiliasi dengan NumPy.
