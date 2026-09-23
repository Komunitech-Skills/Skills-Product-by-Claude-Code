# HASIL UJI — hitung-thr

- Tanggal: 2026-09-23
- Penguji: agent penguji independen (simulasi, Claude Code)
- Folder kerja: `/tmp/uji-hitung-thr/`, `/tmp/uji-pph/`

## Verifikasi independen
- **Sumber dibaca langsung:** Permenaker 6/2016 (pindaian JDIH Kemnaker, halaman 3–6: Pasal 2, 3, 4, 5, 6, 7, 8) dan SE Menaker M/3/HK.04.00/III/2026 (2 Maret 2026). Semua fakta di `references/regulasi.md` baris 1–13 sesuai teks. PPh 21 dari PMK 168/2023 & tabel PP 58/2023 (lihat HASIL-UJI `pph21-ter`).
- **Kalkulator THR penguji** (tidak mengimpor script skill): 3.000 kasus acak — tetap/kontrak/harian/satuan, masa kerja 0–26 bulan (banyak di sekitar 1 dan 12 bulan), hari raya acak Maret–November 2027, PHK 1–60 hari sebelum hari raya (PKWTT vs PKWT), upah harian 1–14 bulan data, PTKP acak, bruto bulan bayar ada/tidak. Dibandingkan THR dan tambahan PPh 21: **0 selisih** terhadap konvensi skill.
- Contoh di SKILL.md (Budi Rp 5.500.000 / tambahan PPh Rp 286.500; Rina Rp 3.200.000 / Rp 120.000) cocok.
- Input rusak: CSV kosong, tanggal mulai setelah hari raya, jenis tak dikenal → ERROR jelas; `Rp 4.500.000,50` terbaca benar.

## Skor

| Kriteria | Skor (1–10) |
|---|---:|
| Pemicu (description tepat) | 9 |
| Kemudahan awam | 9 |
| Kualitas output | 9 |
| Akurasi (angka/fakta) | 6 |
| Penanganan input kurang | 9 |
| Penanganan di luar cakupan | 9 |
| Keamanan | 10 |
| **SKOR AKHIR** | **6** |

Dibatasi ≤ 6 karena 2 cacat berat pada angka PPh 21. Besaran THR sendiri akurat. Uji A/B: jelas lebih baik dari tanpa skill. Banding pesaing: menang.

Audit keamanan: library standar saja, tanpa jaringan/kredensial/perintah destruktif; `subprocess` hanya di file uji. Pengumuman sengaja tanpa nominal pribadi. Aman.

## Cacat
**Berat**
1. **PPh 21 atas THR karyawan yang sudah berhenti dihitung dengan TER + gaji fiktif.** `scripts/thr.py` fungsi `hitung_karyawan`, blok "PPh 21 atas THR": untuk PKWTT yang di-PHK ≤ 30 hari sebelum hari raya dan THR dibayar di bulan setelah bulan berhenti, script tetap menghitung `TER(reguler + THR) − TER(reguler)` dengan `reguler` = gaji pokok + tunjangan tetap, padahal karyawan sudah tidak menerima gaji. Menurut PMK 168/2023 (definisi Mantan Pegawai Pasal 1; Pasal 12 ayat 8; Pasal 16 ayat 6; contoh resmi Tuan O di Lampiran), PPh 21-nya = **tarif Pasal 17 × bruto THR**. Uji: gaji Rp 20 jt, PHK 20 Feb 2027, THR dibayar 3 Mar 2027 → script Rp 4.600.000, benar **Rp 1.000.000** (lebih potong Rp 3,6 jt). **Saran:** bila `tanggal_berhenti` ada dan bulan bayar > bulan berhenti, hitung `tc.pasal17(thr)` (dibulatkan ke bawah) dengan label "Mantan Pegawai (Pasal 17 × bruto)"; bila bulan bayar = bulan berhenti, arahkan ke hitung ulang (sudah ada).
2. **DTP diterapkan tanpa cek tahun dan batas Rp 10 juta.** Blok yang sama: `dtp = ya_tidak(r.get("dtp"), ...)` langsung membuat tambahan PPh 21 = 0. Uji: THR Lebaran **10 Maret 2027** (dibayar Maret 2027), gaji Rp 20 jt, `--dtp ya` → "Rp 4.600.000 (DTP)" dan THR diterima utuh. PMK 105/2025 Pasal 2 ayat (3) hanya berlaku Masa Pajak Januari–Desember **2026**, dan Pasal 4 ayat (2) huruf b mensyaratkan bruto tetap ≤ Rp 10 jt. **Saran:** tolak DTP bila bulan bayar bukan tahun 2026 atau upah tetap > Rp 10 jt (atau kolom `bruto_tetap_januari` > Rp 10 jt), dengan pesan jelas; samakan dengan pengecekan di `pph21-ter`.

**Sedang**
3. **Konvensi masa kerja "bulan penuh" bisa kurang 1 bulan tepat di hari ulang bulan.** `bulan_penuh()`: mulai 11 Maret 2026, hari raya 10 Maret 2027 → 11 bulan (THR 11/12), padahal 11 Mar 2026–10 Mar 2027 sudah 12 bulan kerja utuh bila hari pertama dihitung (docstring sendiri menyebut "tanggal mulai dihitung hari pertama"). Begitu juga mulai 1 Januari & hari raya 31 Januari → 0 bulan (tidak berhak). Aturan tidak mengatur pecahan bulan, tetapi konvensi ini merugikan pekerja di batas dan rawan diprotes. **Saran:** hitung inklusif (`if sampai.day + 1 < mulai.day: n -= 1`, dengan penanganan akhir bulan), atau beri ⚠️ bila masa kerja kurang ≤ 3 hari dari bulan berikutnya/12 bulan, dan sebutkan di SKILL.md bagian Rumus.

**Ringan**
4. THR Desember/bulan berhenti hanya diarahkan ke skill lain; saran: pakai `ter_core.hitung_masa_terakhir` (sudah ada di folder yang sama) dengan kolom opsional `bruto_sd_bulan_lalu`, `pph21_sd_bulan_lalu`, `iuran_sd_bulan_lalu` agar skill mandiri.
5. Pekerja harian/satuan: PPh 21 tidak dihitung sama sekali (hanya diarahkan). Saran: minimal hitung dengan TER bulanan bila upah dibayar bulanan (PMK 168 Pasal 16 ayat 2 huruf c).
6. Denda keterlambatan dirujuk ke Permenaker 6/2016 Pasal 10; sejak 2021 denda THR juga diatur di PP 36/2021 tentang Pengupahan (yang dirujuk SE 2026; pasalnya belum dibaca penguji). Saran: verifikasi dan tambahkan rujukan PP 36/2021 di `references/regulasi.md` baris 12.

## Status
**REVISI** (skor 6) — perbaiki cacat berat 1 & 2 (dan sebaiknya 3), lalu uji ulang; perkiraan skor setelah perbaikan: 9.
