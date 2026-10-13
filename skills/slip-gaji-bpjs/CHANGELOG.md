# Riwayat perubahan — slip-gaji-bpjs

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.7 (2026-10-12)
- Di Telegram/WhatsApp, slip gaji kini **tampil langsung di chat** (teks rapi tanpa tabel): semua slip untuk 1–3 karyawan, atau 3 slip pertama + rekap total bila lebih dari 3. File siap cetak dilampirkan bila bisa; bila tidak, cukup balas "kirim file". Rumus dan angka tidak berubah.

## Catatan revisi 1.0.6 (2026-10-05)
- Pemeriksaan ulang PPh 21 DTP terhadap teks PMK 105/2025 (Pasal 2 ayat 1, Pasal 5, Pasal 6 ayat 6, Lampiran B): hitungan slip **sudah benar** sejak awal (PPh 21 tetap dipotong, DTP dengan nilai sama dibayar tunai, take home pay tidak berkurang karena pajak, setoran PPh 21 bagian DTP Rp 0). Yang diperbaiki: catatan di slip (Markdown & HTML) kini menulis jelas PPh dipotong, DTP dibayar tunai, dan **setoran ke negara Rp 0** per karyawan; tambah tes regresi dan ringkasan dasar hukum `references/dtp-pmk105.md`. **PERLU REVIEW konsultan pajak.**
