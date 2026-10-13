# Riwayat perubahan — gaji-umkm

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.6 (2026-10-01)
- AI tidak lagi berhenti untuk menanyakan tanggal masuk di giliran terpisah (temuan uji OpenClaw). Bila nama, status, dan gaji pokok sudah ada, AI langsung menghitung dengan default wajar (tanggal masuk 1 Januari tahun berjalan, JKK 0,24%, ikut semua BPJS) dan menyebut asumsinya. Semua hal yang perlu dicek — tanggal masuk, **UMK daerah**, tarif JKK — digabung dalam **satu** pesan.
- Pemakaian pertama: angka langsung keluar di balasan pertama lewat mesin hitung yang sama (hitungan sementara, tanpa menyimpan), lalu database dibuat setelah Anda setuju.
- Instruksi: script dijalankan dari subfolder `scripts/` di folder skill (tidak mencari ke seluruh disk). Script aplikasi tidak berubah; uji regresi tetap lulus.

## Catatan revisi 1.0.7 (2026-10-02)
- Mesin THR (`scripts/mesin/thr.py`) disinkronkan dengan `hitung-thr` 1.0.6: peringatan untuk tanggal masuk di masa depan, karyawan yang masuk setelah hari raya ditandai belum berhak (tidak lagi menghentikan seluruh hitungan THR), dan teks pengumuman grup menegaskan rincian THR dikirim pribadi. Angka THR tidak berubah; sha256 baru dicatat di `SUMBER.json`.

## Catatan revisi 1.0.10 (2026-10-05)
- Pemeriksaan ulang PPh 21 DTP terhadap teks PMK 105/2025 (Pasal 2 ayat 1, Pasal 5, Pasal 6 ayat 6, Lampiran B): gaji bersih di slip **sudah benar** (PPh 21 dipotong, DTP dengan nilai sama dibayar tunai, setoran bagian DTP Rp 0). Catatan DTP di slip kini menulis jelas PPh dipotong, DTP dibayar tunai, dan setoran ke negara Rp 0.
- Salinan mesin disinkronkan dengan skill sumber: `payroll.py` (slip-gaji-bpjs 1.0.6), `pph21.py` (pph21-ter 1.0.5, koreksi uang diterima DTP), `thr.py` (hitung-thr 1.0.9); sha256 baru di `scripts/mesin/SUMBER.json`. Tambah tes `UjiDTP` dan `references/dtp-pmk105.md`. **PERLU REVIEW konsultan pajak.**

## Catatan revisi 1.0.11 (2026-10-05)
- Data JSON rekap (`total`) kini memisahkan tiga angka PPh 21 dengan nama yang jelas: `pph21_dipotong` = total PPh 21 yang **dipotong** dari gaji (termasuk bagian DTP), `pph21_dtp` = bagian DTP yang dibayar tunai ke karyawan dan tidak disetor, `pph21_disetor_ke_negara` = perkiraan setoran. Sebelumnya `pph21_dipotong` berisi jumlah yang disetor. `setor_pph21` tetap ada dengan nilai sama seperti sebelumnya (kompatibel). Rekap periode lama yang tersimpan diubah otomatis ke arti baru saat dibaca.
- Teks rekap bila ada karyawan DTP kini menulis "PPh 21 dipotong dari gaji bulan ini … (termasuk DTP …)" lalu "Setor PPh 21 ke negara". Angka gaji bersih & setoran tidak berubah. Mesin hitung (`scripts/mesin/`) tidak diubah. **PERLU REVIEW konsultan pajak.**
