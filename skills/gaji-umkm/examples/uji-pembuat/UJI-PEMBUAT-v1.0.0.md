# Uji pembuat gaji-umkm v1.0.0 (26 September 2026)

> Catatan uji dari **pembuat**, bukan penguji independen. Skor kualitas, uji A/B, dan uji banding pesaing
> (Tahap 6) belum dilakukan dan wajib dikerjakan agent/sesi terpisah.

## Otomatis: `python3 tests/uji_regresi.py` → 29 tes, semua lulus (Python 3.11, Linux)
| Kelompok | Yang dibuktikan |
|---|---|
| Mesin | `scripts/mesin/*` identik byte-per-byte dengan script asli `slip-gaji-bpjs`, `pph21-ter`, `hitung-thr` di repo; sha256 cocok dengan `SUMBER.json`; mesin yang diubah (1 spasi) ditolak |
| Pencocokan massal | 60 karyawan acak (8 status PTKP, gaji Rp 2,5–30 jt, tunjangan tetap/tidak tetap, BPJS kes/tk/jp/tidak, JKK 5 tarif, pola 5/6 hari, lembur hari kerja & libur termasuk `p`, bonus, kasbon, zakat) di Februari, Maret (batas JP berganti), dan September 2026: semua komponen pendapatan, potongan, iuran, PPh 21, gaji bersih, biaya perusahaan **sama persis** dengan `payroll.py` asli yang diberi CSV susunan tes sendiri. Total rekap = jumlah per karyawan |
| Contoh resmi skill sumber | Contoh SKILL.md slip-gaji-bpjs (Budi K/1): lembur Rp 794.798, PPh 21 Rp 53.707, THP Rp 6.521.091, biaya Rp 7.474.498 |
| Desember | 3 karyawan Januari–Desember (bonus Maret, bonus Desember, masuk 20 April): PPh 21 setahun = hitungan Pasal 17 manual di tes; Desember = `payroll.py` asli dengan total Jan–Nov dari tes; `pph21-tahunan` "cocok" dengan `pph21.py` asli; masuk April → `bulan_mulai` 4, batas biaya jabatan Rp 500.000 × 9 |
| Keluar tengah bulan | Joko keluar 14/11: November = Masa Pajak Terakhir (`berhenti`), gaji penuh + peringatan, prorata hanya dari isian pemilik; angka sama dengan `payroll.py` asli; tidak ikut Desember; `pph21-tahunan` cocok |
| Masuk tengah bulan | Tidak ikut bulan sebelum masuk (isi ditolak); peringatan "gaji PENUH"; `--gaji-pokok-dibayar` dipakai dan peringatan hilang |
| Data kurang | Desember tanpa data Jan–Nov → ditolak dengan daftar bulan; `saldo-awal` + November final → bisa; saldo awal sampai bulan ≥ periode ditolak |
| Revisi berantai | Revisi Juni setelah Desember final → peringatan; Desember direvisi ikut berubah; `pph21-tahunan` tetap cocok |
| THR | Jumlah THR sama dengan `thr.py` asli (≥12 bulan penuh, kontrak proporsional, <1 bulan = 0) dan masuk ke Bonus/THR payroll; tanggal bayar di luar periode ditolak |
| Data rusak | Impor 7 baris dengan 6 salah (K/4, negatif, format Inggris, 31/02, NIK 12 angka, rekening `1,23457E+12`) → tidak ada yang disimpan; file kosong/judul saja/kolom kurang/.xlsx/tidak ada; jam lembur huruf, `p` di hari kerja, periode 2026-13, nama tak dikenal, nama kembar (pilihan), lembur jam + rupiah bersamaan, lembur libur 13 jam (ditolak mesin, tidak ada hasil tersimpan), nama berisi koma/titik koma/kutip |
| Absensi-lokal | CSV `--csv-gaji` buatan tes dan **file asli dari `absensi.py`** terbaca; lembur dihitung ulang benar; alpa tidak dipotong tanpa dasar; dengan `--dasar-potongan` potongan = hari alpa × tarif dan tampil terpisah di slip |
| Kunci & revisi | Transfer draf ditolak; final ditolak bila data berubah sejak dihitung; isi/hitung/final pada periode final ditolak; revisi wajib alasan; hasil lama tetap ada; selisih tercatat; transfer revisi = selisih saja |
| Privasi | NIK & rekening tidak pernah muncul utuh di keluaran daftar/hitung/rekap/slip/final/transfer/pengingat/ubah; `--rekening-lengkap` hanya di file CSV |
| Pengingat | 15/11/2026 (Minggu) → Senin 16/11; tgl 10 BPJS Kes, tgl 20 lapor; tanpa nama karyawan; angka = rekap final |
| Backup/restore | Pratinjau tidak mengubah; restore menyimpan database lama; database rusak dipindah (tidak dihapus); cadangan palsu/tidak ada ditolak; `init` tidak menimpa |

## Manual
- Sesi lengkap toko bangunan (`examples/contoh-sesi-toko-bangunan.md`) + skenario setahun (saldo awal Jan–Agu, karyawan baru 15/10, keluar 14/11, THR Natal 2 karyawan, Desember): `pph21-tahunan` 5/5 cocok.
- Angka Andi, Joko, Rina dicek manual (lihat contoh sesi).
- Template `karyawan-contoh.csv` + `komponen-contoh.csv` terbaca dan terhitung.

## Belum diuji
- Windows/macOS (script hanya library standar; path & encoding ditulis lintas OS).
- Jadwal OpenClaw & pengiriman Telegram (pola disalin dari crm-wa).
- Periode setelah Februari 2027 butuh `atur --batas-jp` dari pengumuman BPJS (perilaku `slip-gaji-bpjs`).
