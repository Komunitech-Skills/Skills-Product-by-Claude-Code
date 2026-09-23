# 00 — Uji A/B: S1 dengan skill vs tanpa skill

**Permintaan (sama):** slip gaji September 2026 untuk 3 karyawan CV Contoh Maju Jaya (lihat `01-slip-gaji-3-karyawan.md`), UMK 5.396.761, JKK 0,54%, lembur Budi 2+3 jam hari kerja dan 8 jam hari Minggu.

Metode: jawaban "tanpa skill" disimulasikan penguji sebagai AI agent biasa, tanpa membuka SKILL.md/script. Agent biasa umumnya menghitung benar komponen yang "terkenal" (BPJS 1%/2%/1%, lembur 1/173), tetapi melewatkan detail aturan. Angka di kolom kiri dihitung ulang oleh penguji dengan pendekatan umum itu (TER dari tabel yang benar, agar adil).

## Berdampingan

| Aspek | Tanpa skill (AI agent biasa) | Dengan skill `slip-gaji-bpjs` |
|---|---|---|
| Bentuk hasil | Tabel ringkas di chat per karyawan | Rekap + 3 file: slip MD, slip HTML siap cetak (satu slip per halaman, kolom tanda tangan), rekap CSV untuk Excel |
| Bruto untuk PPh 21 | Gaji + tunjangan + lembur saja (premi JKK/JKM/BPJS Kes perusahaan **tidak** dimasukkan) | Termasuk premi JKK, JKM, BPJS Kes 4% (PMK 168/2023 Pasal 5 ayat 3) |
| PPh 21 Budi / Siti / Dewi | Rp 51.710 / Rp 13.750 / Rp 288.836 | **Rp 53.707 / Rp 28.793 / Rp 361.850** (benar, diverifikasi independen) |
| BPJS Kesehatan Siti (upah tetap di bawah UMK) | 1% × Rp 5.100.000 = Rp 51.000 | 1% × UMK Rp 5.396.761 = **Rp 53.968** (batas bawah UMK, Perpres 64/2020 Pasal 32) + peringatan upah di bawah UMK |
| THP Budi / Siti / Dewi | Rp 6.523.088 / Rp 5.282.250 / Rp 10.594.632 | **Rp 6.521.091 / Rp 5.264.239 / Rp 10.521.618** |
| Biaya total perusahaan & setoran BPJS/PPh | Sering tidak dihitung | Dihitung per orang dan total setoran |
| Batas JP 2026 | Tergantung ingatan (sering masih Rp 10.547.400 atau lebih lama) | Otomatis sesuai periode (Rp 11.086.300 mulai Maret 2026) |
| Desember/berhenti kerja | Biasanya tetap pakai TER (salah) | Wajib hitung ulang, script menolak bila data Jan–Nov kosong |

## Penilaian singkat
Tanpa skill, PPh 21 ketiga karyawan **kurang potong** (Dewi Rp 73.014/bulan, Siti Rp 15.043/bulan) dan iuran BPJS Kesehatan Siti kurang — kesalahan yang baru ketahuan saat pemeriksaan/rekonsiliasi. Dengan skill, angka benar, ada peringatan UMK, dan dokumen siap cetak. **Skill jelas lebih baik.**
