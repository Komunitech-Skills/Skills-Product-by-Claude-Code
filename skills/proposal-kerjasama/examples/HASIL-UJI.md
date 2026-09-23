# HASIL UJI — proposal-kerjasama

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** folder kerja sementara `/tmp/uji-proposal-kerjasama/`, Python 3 standar
- **Skenario:** 01–05 + uji A/B (`00-pembanding-tanpa-skill.md`) + banding pesaing (`00-banding-pesaing.md`)

## Audit keamanan
- `scripts/hitung_skema.py`: hanya `argparse, json, re, sys, decimal`. Tidak ada akses jaringan, file, subprocess, atau kredensial.
- SKILL.md/README/references: tidak ada prompt injection. Ada pagar pengaman yang baik: menolak skema investasi imbal tetap dari dana publik dan skema piramida. **Aman.**

## Verifikasi angka (independen)
- Script terpisah (`verif.py`) membandingkan 300 kasus acak untuk tiap skema (konsinyasi %, reseller diskon % + modal, bagi hasil) dengan perhitungan Decimal independen → **0 selisih** pada rumus.
- Rumus sesuai SKILL.md: konsinyasi (toko = harga × %; pemilik = sisa), reseller (harga reseller = HET × (1 − diskon); untung = HET − harga reseller), bagi hasil (mitra = dasar × %; pemilik = sisa, selalu menjumlah tepat).
- Contoh SKILL.md & README (Rp 250.000 / Rp 500.000 / Rp 1.000.000 per cabang; laba Rp 6.000/bungkus) → benar.
- **Temuan:** daftar skenario berpemisah koma dibaca salah secara diam-diam (lihat Cacat berat #1). Pada konsinyasi, bagian toko + bagian pemilik bisa selisih Rp 1 dari omzet (30 dari 900 kasus acak dengan persen/harga tak bulat).
- Data rusak/tepi yang ditangani baik: harga 0, porsi > 100%, harga titip > harga jual, skenario 0, skenario kosong, > 5 skenario (bila dipisah `;`), porsi & harga titip sekaligus, modal > bagian pemilik (muncul `PERINGATAN` rugi), "Rp 1.500.000,50", "1,5jt;2,5jt", "50 / 100".

## Skor

| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description) | 9 | Jenis kerja sama & kata kunci ID/EN lengkap, batas dengan SPH/kontrak jelas |
| Kemudahan awam | 9 | Satu kalimat cukup; tabel internal dipisah dari proposal |
| Kualitas output | 9 | Fokus ke mitra, siap kirim + WA + email; kerangka per jenis sangat membantu |
| Akurasi (angka/fakta) | 5 | Rumus benar, tetapi parser skenario menghasilkan angka salah tanpa peringatan untuk input koma yang wajar |
| Penanganan input kurang | 9 | Tanya sekali, 5 pertanyaan, jalur cepat |
| Penanganan di luar cakupan | 9 | Menolak investasi bodong/piramida dengan alternatif sah |
| Keamanan | 10 | Bersih |

## SKOR AKHIR: **6 / 10** — REVISI

Kualitas konten dan uji A/B sangat baik; banding pesaing (`sales-proposal`, zubair-trabzada/ai-sales-team-claude, MIT) juga dimenangkan skill kita untuk konteks UMKM Indonesia (skill jelas lebih baik: tidak membocorkan modal, tidak mengarang klaim, ada simulasi & langkah berikut). Skor dibatasi ≤ 6 karena **cacat berat angka** di script. Setelah bug parser diperbaiki dan diuji ulang, perkiraan skor 8–9.

## Daftar cacat & saran perbaikan

### Berat
1. **`--skenario "10,20,30"` dibaca sebagai 102.030 unit (satu skenario), tanpa error.** Juga `"5,10,15"` → 51.015 unit; bagi hasil `"10,25,50"` → Rp 102.550. Penyebab: `parse_skenario()` (baris ± 84–86 script) tidak memecah koma bila string berakhiran pola `\d,\d{1,2}$`, lalu `parse_angka()` membuang semua koma karena bagiannya > 2. Padahal help argparse sendiri mencontohkan pemisah koma ("mis. '50,100,200'", "mis. '20,50,100'") dan docstring memakai `--skenario 50,100,200`. Hasilnya tabel simulasi bernilai miliaran rupiah bisa masuk proposal. **Saran:** (a) di `parse_skenario`, bila string mengandung ≥ 2 koma, selalu pecah per koma; hanya perlakukan koma sebagai desimal bila tepat satu koma dan tidak ada pemisah lain; (b) setelah pecah, tolak hasil yang tiap bagiannya tidak valid; (c) ubah semua contoh help/docstring ke pemisah `;` agar konsisten dengan SKILL.md; (d) tambahkan uji regresi `10,20,30` → 3 skenario.

### Sedang
- Tidak ada.

### Ringan
2. Konsinyasi: `bagian_toko + bagian_pemilik_barang` bisa ≠ `omzet` (selisih Rp 1) karena ketiganya dibulatkan terpisah (contoh: harga 12.345, porsi 15%, 2 unit → 24.690 vs 3.704 + 20.987). **Saran:** di `konsinyasi()`, hitung `bagian_pemilik = omzet − bagian_toko` (seperti yang sudah dilakukan `bagi_hasil`).
3. `"--skenario 30,60"` ditolak dengan pesan "harus bilangan bulat: '30,60'" — membingungkan pengguna. Akan teratasi bersama perbaikan #1; pesan sebaiknya menyarankan pemisah `;`.
4. `parse_angka` sama dengan skill SPH: "1.500rb" → 1.500 dan "Rp 25.000,-" ditolak. **Saran:** samakan perbaikan dengan skill `surat-penawaran-harga`.
5. Istilah "HET" dipakai untuk harga jual yang disarankan brand swasta; "HET" lazimnya istilah harga eceran tertinggi yang ditetapkan pemerintah. **Saran:** di `references/kerangka-per-jenis.md` §2 dan SKILL.md, tulis "harga jual yang disarankan (HET/SRP)".
6. Larangan skema piramida (UU 7/2014 tentang Perdagangan) dan rujukan OJK tidak diberi dasar aturan + tanggal cek, padahal CLAUDE.md Tahap 4.5 memintanya untuk domain hukum. **Saran:** tambah satu baris sumber + "dicek per 2026-09-23" di `references/kerangka-per-jenis.md`.
7. Konsinyasi ke toko yang PKP punya konsekuensi PPN atas penyerahan barang titipan; tidak disebut sama sekali. **Saran:** satu kalimat di Batasan: "Jika salah satu pihak PKP, aspek PPN konsinyasi konsultasikan ke konsultan pajak."
