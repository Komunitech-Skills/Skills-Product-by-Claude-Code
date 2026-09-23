# HASIL UJI — surat-penawaran-harga

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** folder kerja sementara `/tmp/uji-surat-penawaran-harga/`, Python 3 standar
- **Skenario:** 01–05 + uji A/B (`00-pembanding-tanpa-skill.md`) + banding pesaing (`00-banding-pesaing.md`)

## Audit keamanan
- `scripts/hitung_sph.py`: hanya `argparse, csv, json, re, sys, datetime, decimal, fractions`. Tidak ada akses jaringan, subprocess, penulisan file, pembacaan kredensial. Hanya membaca file CSV yang diberikan lewat `--file`.
- SKILL.md/README/references: tidak ada prompt injection, tidak ada instruksi mengirim data atau menonaktifkan konfirmasi. **Aman.**

## Verifikasi angka (independen)
- Script terpisah (`verif.py`) membandingkan 400 SPH acak (1–4 item, diskon baris %, diskon total nominal, ongkir, mode tidak/pkp/mewah, harga termasuk PPN) dengan perhitungan Decimal independen → **0 selisih**.
- Terbilang dibandingkan dengan implementasi independen untuk 0–2.999 dan 20.000 angka acak s.d. 10^13 → **0 selisih**.
- Rumus PPN: non-mewah 12% × (11/12 × DPP) = 11% DPP, dibulatkan sekali ke rupiah terdekat (ROUND_HALF_UP) — sesuai PMK 131/2024. Mewah 12% penuh. Harga termasuk PPN: DPP = harga ÷ 1,11 — benar.
- Contoh di SKILL.md, README, dan `references/kerangka-sph.md` (katering Rp 5.557.500; toko bangunan PPN Rp 1.325.720 / total Rp 13.377.720; jasa Rp 11,1 jt → DPP 10 jt) dicek ulang → **semua benar**.
- Data rusak/tepi: qty 0, diskon > jumlah, diskon 150%, item kurang kolom, CSV kosong, CSV kolom hilang, tanggal salah format, "abc" → semua ditolak dengan pesan `ERROR:` yang jelas. "Rp 1.500.000", "1.500.000,50", "1,5jt", "750rb", "15,000.50", "IDR 2.000", "1 500 000", CSV titik-koma → terbaca benar.

## Skor

| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description) | 9 | Kata kunci ID/EN lengkap (SPH, quotation, price quote), batas dengan invoice/proposal jelas |
| Kemudahan awam | 9 | Satu kalimat cukup; format harga bebas; default non-PKP aman |
| Kualitas output | 9 | Surat + WA siap kirim, nomor surat baku, asumsi transparan |
| Akurasi (angka/fakta) | 9 | 0 selisih pada uji acak; dasar PPN benar & bertanggal; beberapa kasus tepi parsing (lihat cacat) |
| Penanganan input kurang | 9 | Tanya sekali, ≤ 5 pertanyaan, default jelas |
| Penanganan di luar cakupan | 8 | Rujukan ke skill lain jelas; belum ada kalimat cadangan bila skill rujukan tidak terpasang |
| Keamanan | 10 | Bersih |

## SKOR AKHIR: **8 / 10** — LULUS

Uji A/B: hasil dengan skill jelas lebih baik (kalimat PPN non-PKP yang benar, masa berlaku bertanggal, teks WA, asumsi). Banding pesaing: `quote-drafter` (Ootto-AI/claude-invoice-skills, MIT) kalah — tanpa PPN/PKP, nomor surat, masa berlaku, terbilang, WA. ClawHub/clawskills.sh diblokir proxy sehingga pesaing di sana tidak bisa dibaca. Tidak ada cacat berat.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
1. **Ongkir otomatis masuk DPP tanpa instruksi untuk memberi tahu pengguna.** Perlakuannya masuk akal (ongkir yang ditagih penjual lazim menjadi bagian harga jual/DPP), tetapi SKILL.md "Langkah kerja" langkah 2–3 dan blok "Asumsi" tidak menyuruh agent menyebutkannya; pengguna PKP yang ongkirnya hanya titipan biaya kurir bisa salah pungut. **Saran:** tambahkan di Langkah kerja 2: "Ongkir/biaya pasang yang ditagih penjual ikut DPP dan dikenai PPN; sebutkan di Asumsi. Jika ongkir hanya penggantian biaya kurir yang ditagih terpisah, jangan pakai `--ongkir`, tulis di syarat." Help `--ongkir` di script sudah benar ("ikut DPP bila PKP").
2. **`--harga-termasuk-ppn` juga memperlakukan ongkir sebagai sudah termasuk PPN** (uji: item Rp 11.100.000 + ongkir Rp 100.000 → DPP Rp 10.090.090). Tidak didokumentasikan; pengguna biasanya menyebut ongkir "bersih". **Saran:** di `hitung()` (blok `elif args.harga_termasuk_ppn`), hitung mundur hanya dari `setelah_diskon`, lalu tambahkan ongkir sebagai DPP murni; atau dokumentasikan perilaku ini di SKILL.md langkah 3.

### Ringan
3. `parse_angka`: "1.500rb" terbaca Rp 1.500 (seharusnya Rp 1.500.000 atau ditolak). Penyebab: kondisi `pengali == 1` pada cabang titik ribuan. **Saran:** bila ada akhiran rb/jt dan pola titik ribuan valid, tetap hapus titik.
4. `parse_angka`: format sangat umum "Rp 1.250.000,-" ditolak. **Saran:** buang akhiran `,-` / `.-` sebelum validasi regex.
5. Harga 0 diterima diam-diam (total "Nol Rupiah"). **Saran:** tambahkan peringatan di output bila ada harga 0 (mis. item bonus) agar agent mengonfirmasi.
6. Catatan pembulatan "PPN… Coretax bisa selisih Rp 1" tetap tercetak pada mode `--ppn tidak`. **Saran:** tampilkan hanya bila mode ≠ tidak.
7. CSV tanpa kolom `harga` → pesan "harga item ke-1 tidak bisa dibaca sebagai angka: ''". **Saran:** cek header dulu dan tampilkan "kolom 'harga' tidak ditemukan".
8. Ongkir gratis/0 tidak punya pola tampilan; script tidak mencetak baris ongkir. **Saran:** di Format output tambahkan "Jika ongkir gratis, tulis 'Ongkos kirim: Gratis' atau 'Harga franco …' di syarat".
9. Rujukan ke `buat-invoice`, `hitung-ppn`, `hitung-hpp` tanpa kalimat cadangan bila skill itu tidak dimiliki pembeli. **Saran:** tambah satu kalimat di "Kapan TIDAK digunakan".
10. `references/regulasi.md` bagian "Bea meterai": ambang Rp5.000.000 menurut UU 10/2020 Pasal 3 ayat (2) huruf g berlaku untuk dokumen **penerimaan uang** atau pengakuan bahwa utang **telah dilunasi**, bukan "pengakuan utang" secara umum; surat perjanjian/pernyataan dikenai meterai tanpa ambang nilai. **Saran:** ubah kalimat menjadi "…dan untuk dokumen yang menyebut penerimaan uang/pelunasan utang bernilai > Rp5.000.000".
