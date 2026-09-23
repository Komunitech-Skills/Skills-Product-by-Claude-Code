# HASIL UJI — slip-gaji-bpjs v1.0.1 (uji ulang)

- Tanggal: 2026-09-23
- Penguji: agent penguji independen (simulasi, Claude Code)
- Versi diuji: **v1.0.1** (commit `1ead12f`), menggantikan hasil uji v1.0.0 (skor 6, REVISI)
- Folder kerja: `/tmp/uji-slip-gaji-bpjs/`, `/tmp/uji-pph/`

## Verifikasi independen
Kalkulator payroll & PPh 21 penguji ditulis sendiri (tidak mengimpor script skill). Tabel TER diurai sendiri dari PDF PP 58/2023, aturan dari PMK 168/2023, PMK 105/2025, dan PP 35/2021.

| Uji | Jumlah kasus | Selisih |
|---|---:|---:|
| Slip bulanan acak: gaji, tunjangan tetap/tidak tetap, lembur hari kerja (pecahan jam) & hari libur pola 5/6 hari, bonus, kasbon, UMK, 5 tarif JKK, batas JP Feb vs Sep 2026 (regresi v1.0.0) | 3.000 | 0 |
| Desember/bulan berhenti: data Jan s.d. bulan lalu acak, `jumlah_bulan_kerja` atau `bulan_mulai` (pegawai baru), dengan/tanpa DTP, dengan/tanpa `bruto_tetap_januari` | 2.024 | 0 |
| Desember/berhenti tanpa `jumlah_bulan_kerja`/`bulan_mulai` → wajib ERROR (kode 2) | 976 | 0 |
| DTP masa Mei 2026/2027, gaji di sekitar Rp 10 jt, dengan/tanpa `bruto_tetap_januari`: status DTP, PPh, PPh disetor | 1.000 | 0 |

Hasil kasus lama:
- **Cacat berat v1.0.0 (DTP untuk gaji Rp 15 jt):** kini DTP ditolak dengan ⚠️ "TIDAK memenuhi syarat… lebih dari Rp 10.000.000 (PMK 105/2025 Pasal 4 ayat 2 huruf b)", dan "Setor PPh 21: Rp 1.089.270". **Tertutup.**
- **Cacat sedang v1.0.0 (Desember pegawai masuk September):** tanpa `bulan_mulai` → ERROR yang jelas; dengan `--bulan-mulai 9` → pengembalian Rp 2.726.150 (benar; v1.0.0 memberi Rp 2.832.650). **Tertutup.**
- Contoh S1–S3 tidak berubah angkanya (regresi 0). Contoh S4 diperbarui (menambahkan `--bulan-mulai 1`).
- Uji otomatis skill: `test_payroll.py` OK.

Sumber aturan (tetap dari uji v1.0.0): PP 35/2021 Pasal 31–33 dibaca langsung. Iuran BPJS TK (JHT 3,7/2%, JKK, JKM 0,3%, JP 2/1%) dari artikel resmi bpjsketenagakerjaan.go.id. Batas JP Rp 11.086.300 mulai Maret 2026 dari akun resmi @BPJSTKinfo dan SE B/1226/022026 (dikutip bsc.co.id). Perpres 64/2020 tidak dibaca ulang penguji.

## Skor

| Kriteria | Skor (1–10) |
|---|---:|
| Pemicu (description tepat) | 9 |
| Kemudahan awam | 8 |
| Kualitas output | 9 |
| Akurasi (angka/fakta) | 9 |
| Penanganan input kurang | 9 |
| Penanganan di luar cakupan | 9 |
| Keamanan | 10 |
| **SKOR AKHIR** | **9** |

- Uji A/B (`00-pembanding-tanpa-skill.md`): dengan skill jelas lebih baik.
- Banding pesaing (`00-banding-pesaing.md`): menang telak.
- Audit keamanan: tetap aman. Hanya library standar; tidak ada jaringan, kredensial, atau perintah destruktif di script produk.

## Cacat tersisa
**Berat:** tidak ada.

**Sedang:** tidak ada.

**Ringan:**
1. Bila `bruto_tetap_januari` kosong, syarat DTP dicek memakai gaji bulan berjalan (ada ⚠️). Karyawan yang naik gaji setelah Januari (contoh resmi PMK 105 Tuan B) bisa ditolak DTP padahal berhak. Saran: di SKILL.md bagian Langkah, minta agent menanyakan gaji tetap Januari bila `dtp=ya` dan gaji bulan ini > Rp 10 jt.
2. Dasar iuran BPJS Kesehatan = gaji pokok + tunjangan tetap masih berstatus "Sekunder" di `references/regulasi.md`. Saran: verifikasi ke peraturan BPJS Kesehatan.
3. Pembulatan iuran dan PPh belum dicocokkan dengan aplikasi BPJS/Coretax (sudah diakui di skill).

## Status
**LULUS** (skor 9).
