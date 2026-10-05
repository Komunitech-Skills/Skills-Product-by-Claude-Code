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
