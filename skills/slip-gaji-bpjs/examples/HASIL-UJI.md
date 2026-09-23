# HASIL UJI — slip-gaji-bpjs

- Tanggal: 2026-09-23
- Penguji: agent penguji independen (simulasi, Claude Code)
- Folder kerja: `/tmp/uji-slip-gaji-bpjs/`, `/tmp/uji-pph/`

## Verifikasi independen
- **Kalkulator payroll penguji** (tidak mengimpor script skill; TER dari tabel yang diurai sendiri dari PDF PP 58/2023): 3.000 slip acak — gaji Rp 1,5–40 jt dan sekitar batas JP, tunjangan tetap/tidak tetap (termasuk kasus dasar lembur 75%), lembur hari kerja pecahan jam, lembur hari libur pola 5 & 6 hari, bonus, kasbon, UMK/tanpa UMK, 5 tarif JKK, periode Februari 2026 (batas JP lama) dan September 2026 (baru). Dibandingkan: lembur, bruto pajak, PPh 21, iuran BPJS Kes & JP karyawan, THP, biaya perusahaan. **Selisih: 0.** Desember (hitung ulang) juga dicek manual (contoh S4 cocok).
- **Aturan yang dibaca penguji sendiri:** PP 35/2021 Pasal 31–33 (teks JDIH Kemnaker: pengali lembur, 1/173, dasar 75%) — sesuai. PMK 168/2023 Pasal 5 ayat (3) & Pasal 7 (premi JKK/JKM/BPJS Kes perusahaan masuk bruto; JHT/JP perusahaan bukan objek) — sesuai.
- **Batas upah JP 2026 Rp 11.086.300 mulai Maret 2026:** dikonfirmasi dari balasan akun resmi @BPJSTKinfo (hasil pencarian) dan artikel yang mengutip SE BPJS Ketenagakerjaan No. B/1226/022026 (bsc.co.id). Halaman artikel resmi bpjsketenagakerjaan.go.id (dibaca lewat curl) mengonfirmasi JHT 3,7%/2%, JKK 0,24/0,54/0,89/1,27/1,74%, JKM 0,3%, JP 2%/1%, tetapi masih mencantumkan batas JP lama "Rp 10.547.000" (salah ketik & belum diperbarui) — sudah dicatat benar di `references/regulasi.md`. Perpres 64/2020 (BPJS Kes 4%/1%, batas Rp 12 jt, batas bawah UMK) tidak dibaca ulang penguji; mengikuti catatan pembuat.
- Input rusak: CSV kosong, tanpa kolom wajib, PTKP K/4, angka format Inggris, Desember tanpa data → ERROR jelas, tidak ada file setengah jadi.

## Skor

| Kriteria | Skor (1–10) |
|---|---:|
| Pemicu (description tepat) | 9 |
| Kemudahan awam | 8 |
| Kualitas output | 9 |
| Akurasi (angka/fakta) | 7 |
| Penanganan input kurang | 8 |
| Penanganan di luar cakupan | 9 |
| Keamanan | 10 |
| **SKOR AKHIR** | **6** |

Skor akhir dibatasi ≤ 6 karena ada 1 cacat berat (angka PPh 21 salah pada input yang masuk akal). Tanpa cacat itu, skill ini layak 9. Uji A/B: jelas lebih baik dari tanpa skill. Banding pesaing: menang telak.

Audit keamanan: hanya library standar, tanpa jaringan/kredensial/perintah destruktif; `shutil.rmtree` hanya di file uji untuk folder sementaranya sendiri. Aman. Catatan privasi di SKILL.md sudah ada.

## Cacat
**Berat**
1. **PPh 21 DTP diterapkan tanpa cek syarat Rp 10 juta.** `scripts/payroll.py` fungsi `hitung_karyawan`: `dtp = ya_tidak(r.get("dtp"), ...)` lalu `dtp_tunai = pph_dipotong if dtp else Decimal(0)` — hanya tahun 2026 yang dicek. Uji: `--gaji-pokok 15jt --dtp ya` → seluruh PPh 21 Rp 1.089.270 dijadikan DTP dan "Setor PPh 21: Rp 0", tanpa peringatan. Padahal PMK 105/2025 Pasal 4 ayat (2) huruf b mensyaratkan bruto tetap & teratur ≤ Rp 10.000.000 pada Januari 2026 (atau bulan pertama kerja). Skill saudara `pph21-ter` sudah mengeceknya. Risiko nyata: perusahaan tekstil/pariwisata mengisi `dtp=ya` untuk semua baris CSV → kurang setor pajak. **Saran:** tambah kolom `bruto_tetap_januari` (default = gaji pokok + tunjangan tetap bulan ini dengan peringatan), tolak/abaikan DTP bila > Rp 10 jt dengan pesan jelas; di SKILL.md bagian Input & Checklist tulis syarat ≤ Rp 10 jt untuk kolom `dtp`.

**Sedang**
2. **Jumlah bulan kerja Desember default = nomor bulan.** `hitung_karyawan`: `n = int(angka(r.get("jumlah_bulan_kerja"), ..., Decimal(bulan)))`. Karyawan yang masuk di tengah tahun (mis. September) dihitung 12 bulan → batas biaya jabatan Rp 6 jt, bukan 4 × Rp 500 rb → PPh Desember terlalu kecil, tanpa peringatan (uji: masuk September, gaji Rp 20 jt, bruto Sep–Nov Rp 62 jt → script mengembalikan Rp 2.832.650; yang benar dengan 4 bulan kerja Rp 2.726.150, selisih Rp 106.500). **Saran:** wajibkan `jumlah_bulan_kerja` (atau `bulan_mulai`) di Masa Pajak Terakhir, atau beri ⚠️ bila tidak diisi; tambahkan pertanyaan "mulai kerja bulan apa?" di SKILL.md bagian Input baris Desember.

**Ringan**
3. Upah harian (PP 35/2021 Pasal 33: upah sehari × 25 atau × 21 untuk upah sebulan dasar lembur) tidak didukung dan tidak disebut di Batasan. Saran: tambah satu baris di "Batasan".
4. Dasar iuran BPJS Kesehatan = gaji pokok + tunjangan tetap masih berstatus "Sekunder" di `references/regulasi.md`; saran: verifikasi ke Perpres 82/2018 Pasal 1/Peraturan BPJS Kesehatan dan perbarui status.
5. Ringkasan rekap tidak menampilkan rincian jam setara lembur; agent harus menjelaskan sendiri. Saran: tambahkan satu baris "Lembur: X jam setara × upah sejam" di `slip_md`.
6. Pembulatan iuran/PPh belum dicocokkan dengan aplikasi BPJS/Coretax (sudah diakui).

## Status
**REVISI** (skor 6) — perbaiki cacat berat nomor 1 (dan sebaiknya nomor 2), lalu uji ulang; perkiraan skor setelah perbaikan: 9.
