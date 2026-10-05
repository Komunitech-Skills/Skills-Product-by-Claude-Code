# Hasil Uji — naskah-live-jualan

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** SKILL.md, README.md, ATTRIBUTION.md, `references/etika-promo.md`, `references/bank-jawaban.md`,
  `scripts/hitung_promo.py`, `scripts/susun_segmen.py`
- **Metode:** 5 skenario (01–05) + uji A/B (00), berperan sebagai agent yang memuat SKILL.md. Kedua script dijalankan sungguhan di
  `/tmp/uji-naskah-live-jualan/`; semua angka dihitung ulang dengan python terpisah (`math.ceil`, pembagian bulat).

## Audit keamanan
- Kedua script hanya memakai `argparse, json, re, sys, decimal, datetime`. Tidak ada akses jaringan, subprocess, penulisan/penghapusan file,
  atau pembacaan kredensial. Hanya mencetak ke layar.
- SKILL.md/references: tidak ada prompt injection. Aturan anti-kelangkaan palsu & anti-transaksi luar platform eksplisit. **Aman.**

## Verifikasi angka (independen)
| Kasus | Script | Hitung independen |
|---|---|---|
| 185.000 → 149.000, paket 2 = 280.000 | hemat 36.000 (19%), 140.000/pcs, hemat 90.000 (24%) | 36.000; 19,46%→19; 140.000; 90.000; 24,3%→24 ✔ |
| 95.000 diskon 15%, bulat 1.000 | 81.000, hemat 14.000 (14%) | 80.750 → ceil 81.000; 14,7%→14 ✔ |
| 55.000 diskon 20%, bulat 500 | 44.000 (20%) | 44.000 ✔ |
| 99.000 diskon "12,5%", bulat 500 | 87.000, hemat 12.000 (12%) | 86.625 → 87.000; 12,1%→12 ✔ |
| 89.000, paket 7 = Rp 400.000 | 57.143/pcs, hemat 223.000 (35%) | 57.142,86 → ceil 57.143; 623.000−400.000; 35,8%→35 ✔ |
| "1.500.000,50" → "1,2jt" | hemat Rp 300.000,50 (20%) | ✔ |
| 150.000 → 149.500 | "hemat Rp 500", peringatan <1% | ✔ |
| 100.000 → 40.000 | peringatan diskon ≥50% (harga coret) | ✔ |
| Rundown 60 mnt/3 produk, 30 mnt/3 produk, 90 mnt/1 produk lewat tengah malam | total menit & jam benar | ✔ |

Data rusak/tepi ditolak dengan `ERROR:` jelas: harga normal 0, "abc", harga live = normal, live > normal, diskon 100%, tanpa promo sama sekali,
paket isi 1, durasi 15 mnt untuk 3 produk ("minimal 26 menit" — benar), produk kosong, jam 25:00.
**Salah baca:** `"1.500rb"` → Rp 1.500 (seharusnya Rp 1.500.000) — ringan (R1).

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 9 | TikTok/Shopee/IG/FB live, istilah Indonesia & Inggris, batas dengan caption & listing jelas. |
| Kemudahan awam | 8 | Satu kalimat cukup; naskah siap baca. Naskah 60 menit panjang, tapi memang itu yang dibutuhkan host. |
| Kualitas output | 9 | Rundown per menit, kalimat siap ucap + arahan aksi, rekap, bank jawaban. A/B: jelas lebih baik. |
| Akurasi (angka/fakta) | 9 | Semua angka cocok dengan hitungan independen; aturan pembulatan konservatif dan jujur. Minus "1.500rb" dan paket = harga live tanpa peringatan. |
| Penanganan input kurang | 9 | S4 tanya sekali 5 poin + jalan cepat; S3 langsung kerja dengan `[isi: …]`. |
| Penanganan di luar cakupan | 9 | S5 menolak 5 taktik palsu dengan alasan & versi jujur. |
| Keamanan | 10 | Tidak ada risiko teknis. |

## SKOR AKHIR: 8 / 10 → **LULUS**

Tidak ada cacat berat. Angka promo terverifikasi, urgensi dijaga jujur, dan uji A/B menunjukkan nilai tambah yang jelas
(tanpa skill muncul "stok terbatas" palsu, klaim "tidak luntur", dan "diskon 15%" yang sebenarnya 14%). Cacat yang ada kecil dan murah diperbaiki.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
- **S1 — Paket bundling yang harga per pcs-nya SAMA dengan harga live tidak diberi peringatan** (`hitung_promo.py` baris 177:
  `elif live is not None and per_pcs > live`). Contoh S2: Arabika live Rp 75.000, paket 2 Rp 150.000 → per pcs Rp 75.000, tetapi host bisa
  mengucapkan "ambil paket lebih hemat". *Saran:* ubah ke `per_pcs >= live` dengan pesan "Paket isi N tidak lebih hemat dari harga live satuan;
  sebut hemat dibanding harga normal saja."
- **S2 — Rekap penonton baru tidak benar-benar tiap ±15 menit** (`susun_segmen.py` baris 68–81). Rekap hanya disisipkan di **awal** blok produk;
  pada 60 menit/3 produk rekap pertama di menit 25 dan berikutnya baru segmen bebas di menit 48 (celah 22 menit). *Saran:* periksa juga
  `t - rekap_terakhir >= JEDA_REKAP` di antara segmen dalam blok (sebelum "Harga & promo"), atau set rekap pertama di menit ±15.

### Ringan
- **R1 — `"1.500rb"` terbaca Rp 1.500** (`parse_angka` baris 56, syarat `pengali == 1`). *Saran:* bila ada akhiran rb/jt dan pola titik ribuan
  valid (`^\d{1,3}(\.\d{3})+$`), tetap hapus titik sebelum dikalikan.
- **R2 — Tanda "±" pada persen yang sudah dibulatkan ke bawah** (`kalimat_live`, baris 134–135) terdengar seperti perkiraan dua arah.
  *Saran:* tulis "hemat Rp 36.000 (19%)" atau "hampir 20%".
- **R3 — Tidak ada arahan untuk produk tanpa promo dan live 1 produk.** `hitung_promo.py` menolak produk tanpa promo (wajar), dan 1 produk
  60 menit menghasilkan 4 putaran identik. *Saran:* SKILL.md langkah 2: "Produk tanpa promo: tulis harga normal saja, tidak perlu script";
  langkah 3: "Jika produk sedikit, beri sudut bahasan berbeda tiap putaran".
- **R4 — Harga coret palsu < 50% tidak tertangkap script** (S5: 150.000 → 79.000 = 47%, tanpa peringatan). Penolakan bergantung pada agent;
  SKILL.md sudah jelas, jadi cukup tambahkan pada Checklist: "Harga normal adalah harga jual yang benar-benar berlaku sebelumnya (tanya bila ragu)."
- **R5 — README merujuk `CARA-INSTAL.md`, ATTRIBUTION merujuk `LISENSI.txt`** yang tidak ada di folder skill; pastikan ikut paket rilis.

## Uji A/B
Lihat `00-pembanding-tanpa-skill.md`. Tanpa skill: 4 blok 15 menit, "stok terbatas" palsu untuk kemeja, klaim karangan ("premium", "tidak luntur",
"pengrajin berpengalaman"), harga daster Rp 80.750 dengan "diskon 15%", tanpa info COD dan bank jawaban. Dengan skill: rundown per menit, angka
terverifikasi & jujur, urgensi hanya dari fakta. **Skill jelas memberi nilai tambah.**

## Riwayat revisi
- **1.0.6 (2026-10-05):** pra-cek konteks Telegram menemukan baris proses internal ("Lulus cek-silang fakta (0 GAGAL)") bocor di pembuka balasan. SKILL.md kini melarang menampilkan hasil script/nama script/istilah cek-silang dan mewajibkan balasan dimulai dengan naskah; butir checklist ditambah. **Status: menunggu uji ulang independen.**
