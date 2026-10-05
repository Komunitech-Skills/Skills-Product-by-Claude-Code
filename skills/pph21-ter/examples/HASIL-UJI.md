# HASIL UJI — pph21-ter

- Tanggal: 2026-09-23
- Penguji: agent penguji independen (simulasi, Claude Code)
- Folder kerja: `/tmp/uji-pph21-ter/`, `/tmp/uji-pph/` (tidak ada file repo lain yang diubah)

## Verifikasi independen angka (wajib)
Kalkulator penguji ditulis sendiri (tidak mengimpor script skill) langsung dari PDF resmi di `research/sources/dokumen/`:
1. **Tabel TER**: teks PDF PP 58/2023 (hasil pindai/OCR) diurai dua cara — angka `Rp…` dengan perbaikan OCR dan terbilang "(lima juta empat ratus ribu rupiah)" — lalu dicocokkan silang. Hasil: A 44 baris, B 40, C 41, harian 2; **identik** dengan `scripts/ter_tabel.json`.
2. **Aturan** dari teks PMK 168/2023 (Pasal 8–10, 12, 15–16, Lampiran I.2) dan PMK 105/2025 (Pasal 2–5, Lampiran B).
3. **Contoh resmi** dihitung ulang dengan kalkulator penguji: Penjelasan PP 58 (Rp 515.000), Tuan A (Rp 14.595.000), B (−Rp 2.975.000), C (Rp 580.000, disetahunkan), D (−Rp 3.620.000; PT AB −Rp 4.395.000), E (Rp 1.200.000), F (K/3 Rp 3.300.000), K/L/M/Z (harian), N (Rp 870.000), PMK 105 Tuan A/B/C — **semua cocok**. Catatan: tabel ringkas PMK 105/2025 Lampiran B contoh Tuan C mencantumkan total Rp 1.822.500, padahal hitungannya sendiri Rp 1.812.500 (salah ketik di PMK; skill & penguji sama-sama Rp 1.812.500).
4. **Uji acak massal** (skill vs penguji): 4.000 kasus bulanan (semua PTKP, bruto di batas tiap baris ±1 dan ±1.000, s.d. Rp 2 M), 2.500 kasus setahun (penuh, pegawai baru, berhenti, disetahunkan, dengan THR/bonus acak & iuran), 4.000 kasus harian/borongan (sekitar Rp 450 rb, Rp 2,5 jt, s.d. Rp 20 M/hari), 1.000 kasus DTP (batas Rp 10 jt, mulai tengah tahun), 500 CSV gaji bervariasi + zakat. **Selisih: 0.**
5. **Koreksi pembuat soal anualisasi** diverifikasi dari teks PMK 168/2023 Lampiran I.2 angka 6 huruf a vs c dan Pasal 15 ayat (3): pegawai resign/baru yang tetap subjek pajak dalam negeri **tidak disetahunkan** (PTKP penuh); disetahunkan hanya bila kewajiban pajak subjektif mulai/berakhir. Skill benar.
6. Uji input rusak: `Rp 1.500.000`, `1.500.000,50`, `0`, `10jt`, `15,5jt`, `Rp 10.000.000,-` terbaca benar; `1,250,000.50` & `abc` & `K/4` & CSV kosong/tanpa kolom `bulan` → pesan ERROR jelas, kode 2.

## Skor

| Kriteria | Skor (1–10) |
|---|---:|
| Pemicu (description tepat) | 9 |
| Kemudahan awam | 8 |
| Kualitas output | 9 |
| Akurasi (angka/fakta) | 10 |
| Penanganan input kurang | 9 |
| Penanganan di luar cakupan | 9 |
| Keamanan | 10 |
| **SKOR AKHIR** | **9** |

Uji A/B: dengan skill jelas lebih baik (angka pasti & dapat diaudit, tabel bulanan, lebih potong, DTP). Uji banding pesaing: menang telak (pesaing MIT punya tabel TER B/C salah pada 74% kasus B/C).

Audit keamanan: hanya library standar; tidak ada jaringan, `subprocess` hanya di file uji untuk menjalankan script sendiri, tidak membaca kredensial, tidak ada teks injeksi. Aman.

## Cacat
**Berat:** tidak ada.

**Sedang:** tidak ada.

**Ringan:**
1. Output `setahun` (fungsi `cmd_setahun`, daftar `hasil["catatan"]` di `scripts/pph21.py`) tidak mengingatkan bahwa premi JKK, JKM, BPJS Kesehatan bagian perusahaan wajib masuk bruto — padahal pengguna awam biasanya menyebut "gaji" saja. Saran: tambahkan catatan yang sama seperti di `cmd_bulan`, atau peringatan bila `--data` tidak memuat kolom premi.
2. Ringkasan DTP (`total_dtp_dibayar_tunai`) menjumlah DTP positif saja (benar secara kas), sedangkan tabel Lampiran B PMK 105 menampilkan total bersih. Saran: di `teks_setahun` tampilkan dua angka — "DTP dibayar tunai" dan "PPh terutang setahun (DTP)" — agar tidak membingungkan saat dicocokkan dengan contoh resmi.
3. `parse_angka` membaca `1.5` sebagai Rp 1,5 dan `-5jt` ditolak argparse dengan pesan bahasa Inggris. Dampak kecil; saran: di SKILL.md bagian Batasan sebutkan "untuk negatif/format aneh, script menolak" dan tangkap error argparse.
4. Pembulatan belum dicocokkan dengan Coretax (sudah diakui di SKILL.md). Saran: bila ada akses, uji 5–10 kasus di simulasi Coretax dan catat di `references/regulasi.md`.
5. SKILL.md "Kapan TIDAK digunakan": tambahkan satu frasa bahwa pesangon/uang pensiun sekaligus dikenai PPh 21 final (PP 68/2009), bukan TER, supaya pengarahan agent konsisten.

## Status
**LULUS** (skor 9).

## Riwayat revisi 1.0.5 (2026-10-05) — menunggu uji ulang independen; PERLU REVIEW konsultan pajak
- Pemicu: penilai independen Telegram gelombang 7 (`koordinasi/telegram-gelombang-7-2026-10-05.md`, cacat no. 1): uang diterima pegawai DTP ditulis gaji + DTP (Rp 6.045.000).
- Pembuat membaca ulang teks PMK 105/2025: Pasal 2 ayat 1 ("wajib dipotong"), Pasal 5 ayat 1 ("harus dibayarkan secara tunai"), ayat 5 ("telah dipotong dan diberikan insentif"), Pasal 6 ayat 6 ("wajib menyetorkan PPh 21 yang telah dipotong" bila insentif gugur), Lampiran B (Tuan A: 8.000.000 − 120.000 + DTP 120.000 = 8.000.000). Temuan **benar**.
- Perubahan: `scripts/pph21.py` — `bulan`: PPh dipotong = PPh TER, DTP tunai = nilai sama, kunci baru `pph21_disetor_ke_negara` (Rp 0 bila DTP), diterima = bruto − premi − PPh + DTP − potongan; `setahun`: teks "tetap DIPOTONG" + baris setoran Rp 0 + kunci ringkasan `pph21_disetor_ke_negara`; `harian`: teks DTP diperjelas. SKILL.md langkah 3, format output, checklist; `references/dtp-pmk105.md` (baru), `references/regulasi.md` baris 20; README.
- Angka: TK/0 Rp 6.000.000 DTP → dipotong Rp 45.000, DTP Rp 45.000, setoran Rp 0, **diterima Rp 6.000.000** (sebelumnya Rp 6.045.000); tanpa DTP Rp 5.955.000.
- Tes: `scripts/test_pph21.py` diperbarui (+1 tes Lampiran B Tuan A), 42 tes OK.
- Contoh `00-openclaw-sebelum-sesudah.md` diberi catatan koreksi (penilaiannya memakai acuan lama).

## Uji ulang DTP PMK 105/2025 — 2026-10-05

Penguji independen (bukan pembuat; tidak mengubah kode/SKILL.md). Teks PMK 105/2025 dibaca langsung: Pasal 2 ayat 1 (PPh 21 **wajib dipotong**), Pasal 2 ayat 3 (Masa Pajak Januari–Desember 2026), Pasal 3 (industri alas kaki, tekstil & pakaian jadi, furnitur, kulit, pariwisata + KLU Lampiran A, 133 baris), Pasal 4 ayat 2–4 (pegawai tetap: bruto tetap & teratur Januari 2026/bulan pertama kerja **≤ Rp10.000.000**; tidak tetap: rata-rata ≤ Rp500.000/hari atau ≤ Rp10.000.000 bila bulanan), Pasal 5 ayat 1–2 (DTP **dibayar tunai**, bukan penghasilan kena pajak), Pasal 5 ayat 5 (kelebihan DTP tidak dikembalikan), Pasal 6 ayat 4–6 (lapor SPT Masa paling lambat 31 Januari 2027, lewat batas → PPh yang telah dipotong wajib disetor), Lampiran B (Tuan A 8.000.000 − 120.000 + 120.000 = 8.000.000; Tuan B K/1). Kesimpulan mekanisme: **dipotong = PPh TER/Pasal 17, DTP tunai = nilai sama, setoran ke negara Rp 0, diterima = bruto − potongan lain** (bukan bruto + DTP).

Metode: kalkulator independen Python `Decimal` milik penguji (tabel TER ditulis ulang, tidak mengimpor script skill), dicocokkan dulu dengan Lampiran B PMK 105/2025 (Tuan A Desember 540.000 / setahun 1.860.000; Tuan B Desember 480.000 / setahun 4.050.000 — cocok). Lalu CLI skill dijalankan (`--format json`/`--json`) dan dibandingkan per kolom: dipotong, DTP tunai, disetor ke negara, diterima.

| # | Kasus (CLI `pph21.py`) | Dipotong | DTP tunai | Disetor | Diterima | Selisih |
|---|---|---:|---:|---:|---:|---:|
| 1 | `bulan` TK/0 Rp6.000.000 `--dtp` | 45.000 | 45.000 | 0 | 6.000.000 | 0 |
| 2 | `bulan` TK/0 Rp6.000.000 tanpa DTP (sektor tidak memenuhi → tanpa `--dtp`) | 45.000 | 0 | 45.000 | 5.955.000 | 0 |
| 3 | `bulan` K/1 Rp9.500.000 `--dtp` (TER B 1,5%) | 142.500 | 142.500 | 0 | 9.500.000 | 0 |
| 4 | `bulan` TK/0 tepat Rp10.000.000 `--dtp` (memenuhi, ≤) | 200.000 | 200.000 | 0 | 10.000.000 | 0 |
| 5 | `bulan` TK/0 Rp10.000.001 `--dtp` (ditolak otomatis) | 200.000 | 0 | 200.000 | 9.800.001 | 0 |
| 6 | `bulan` K/1 Rp15.000.000 (bonus) `--bruto-tetap 10jt --dtp` (Lampiran B Tuan B Januari) | 900.000 | 900.000 | 0 | 15.000.000 | 0 |
| 7 | `bulan` TK/0 Rp6.000.000 `--dtp --tahun 2027` (di luar masa) | 45.000 | 0 | 45.000 | 5.955.000 | 0 |
| 8 | `bulan` K/1 Rp9.500.000 `--dtp --potongan-lain 380rb` | 142.500 | 142.500 | 0 | 9.120.000 | 0 |
| 9 | `setahun` TK/0 Rp8.000.000 `--dtp` (Lampiran B Tuan A) — Desember Pasal 17 | Des 540.000; setahun 1.860.000 | 1.860.000 | 0 | 8.000.000/bln | 0 |
| 10 | `setahun` K/1 CSV Tuan B `--dtp` (bonus Jan & Mar, naik 12 jt Okt) | Des 480.000; s.d. Nov 3.570.000; setahun 4.050.000 | 4.050.000 | 0 | = bruto | 0 |
| 11 | `setahun` K/1 CSV Tuan B tanpa DTP | setahun 4.050.000 | 0 | 4.050.000 | – | 0 |
| 12 | `harian` Rp480.000 × 20 hari `--dtp` (≤ Rp500.000/hari) | 48.000 | 48.000 | 0 | 9.600.000 | 0 |
| 13 | `harian` Rp600.000 × 10 hari `--dtp` (> Rp500.000/hari → tidak DTP) | 30.000 | 0 | 30.000 | – | 0 |

Teks keluaran `bulan --dtp` memuat empat baris wajib (dipotong, DTP tunai, setoran Rp 0, diterima) dan menulis "BUKAN gaji + DTP"; `harian --dtp` menulis "PPh tetap dipotong … dibayar tunai kembali … setoran Rp 0". Sektor/KLU tidak dicek script (sesuai desain); SKILL.md mewajibkan konfirmasi pengguna.

Lain-lain: `test_pph21.py` 42 tes OK · `python3 scripts/validate.py` ✅ 117 skill · `bash scripts/uji_openclaw.sh` (instalasi uji terpisah `/tmp/uji-openclaw`, bukan bot produksi) OpenClaw 2026.9.8: 117/117 eligible/modelVisible/commandVisible. SKILL.md & README bagian utama tidak lagi menulis gaji + DTP sebagai diterima.

**Total selisih: 0 dari 13 kasus.**

Cacat (ringan): README "Catatan revisi 1.0.4" masih berbunyi "(yang benar Rp 6.045.000)" dan "PPh 21 dipotong dari gaji (Rp 0)" tanpa tanda bahwa kalimat itu sudah dikoreksi di 1.0.5 — membingungkan pembeli yang membaca riwayat; sarankan diberi coret/keterangan "dikoreksi di 1.0.5". Bukti A/B `00-openclaw-sebelum-sesudah.md` dinilai dengan acuan lama (sudah diberi catatan koreksi) → skor sebelum/sesudah perlu uji ulang OpenClaw sebelum dipromosikan lagi.

**Skor: 9/10. Verdik: LULUS uji ulang angka DTP** (tetap **PERLU REVIEW konsultan pajak**; pembulatan belum dicocokkan dengan Coretax).

## Riwayat revisi README (2026-10-05, tanpa naik versi) — menunggu cek penguji
- Menindaklanjuti cacat ringan uji ulang DTP: butir DTP di README "Catatan revisi 1.0.4" kini dicoret dan diberi tanda **DIKOREKSI di 1.0.5** (diterima Rp 6.000.000 sesuai PMK 105/2025, bukan Rp 6.045.000; PPh tetap dipotong, bukan Rp 0).
- Dicek ulang file lain yang memuat "6.045.000": `SKILL.md` & `references/dtp-pmk105.md` menyebutnya sebagai contoh yang **salah**; `scripts/test_pph21.py` memastikan angka itu **tidak** muncul; `examples/00-openclaw-sebelum-sesudah.md` sudah diberi banner KOREKSI di atas (riwayat asli dibiarkan); riwayat di file ini sudah bertanda "sebelumnya". Script tidak berubah → versi tetap 1.0.5.
