# Riwayat perubahan — slip-gaji-bpjs

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.8 (2026-10-15)
- Rujukan tarif JKK dicocokkan dengan **PP 6/2025** (ubah PP 37/2021 tentang JKP; ditetapkan & berlaku 7 Feb 2025), sesuai temuan verifikasi aturan C28: Pasal 11 ayat (5) mengalihkan 0,14% dari iuran JKK untuk JKP sehingga porsi JKK murni 0,10/0,40/0,75/1,13/1,60%. Angka 0,10–1,60% dan pengalihan 0,14% ini **sudah ada sejak PP 37/2021** Pasal 11 ayat (5) huruf a; PP 6/2025 mempertahankannya, menghapus rekomposisi JKM 0,10% (huruf b), dan menurunkan iuran JKP dari 0,46% ke 0,36%. Tarif yang dibayar perusahaan **tetap 0,24/0,54/0,89/1,27/1,74%** (PP 44/2015 Pasal 16; artikel resmi BPJS Ketenagakerjaan 17 Des 2025), jadi **angka slip tidak berubah**.
- Script: peringatan ⚠️ khusus bila pengguna mengisi tarif JKK 0,10/0,40/0,75/1,13/1,60% (porsi murni, bukan tarif tagihan) beserta tarif yang benar; pesan tarif tidak standar kini menyebut PP 6/2025; disclaimer menambah PP 6/2025. Tambah 2 tes regresi (29 tes lolos).
- `references/regulasi.md`: baris JKK & JKP diperbarui (JKP 0,36% = 0,22% pemerintah + 0,14% rekomposisi JKK, tanpa iuran tambahan), sumber [12] PP 6/2025 (JDIH Kemnaker); catatan cek versi Perpres 82/2018 jo. 64/2020 jo. 59/2024 untuk iuran & plafon BPJS Kesehatan (PERLU REVIEW); catatan artikel BPJSTK [4] → pakai surat B/1226/022026 untuk batas JP 2026.
- SKILL.md & README: catatan JKK/JKP PP 6/2025 di input, rumus, checklist, dan dasar aturan; versi terkini 1.0.8.
- Koreksi putaran kedua (penguji independen): frasa "sejak PP 6/2025" di README, `references/regulasi.md`, dan docstring `payroll.py` diganti "menurut PP 6/2025 Pasal 11 ayat (5)" dengan keterangan bahwa rekomposisi JKK 0,14% sudah ada sejak PP 37/2021; "bukan tarif tagihan baru" → "bukan tarif tagihan"; tambah sumber [13] PP 37/2021 (JDIH Kemnaker, halaman 9 dibaca 2026-10-15); peringatan ⚠️ tarif porsi murni kini menyebut PP 37/2021 Pasal 11 ayat (5) (tes ditambah satu pemeriksaan teks; angka & rumus tidak berubah).

## Catatan revisi 1.0.7 (2026-10-12)
- Di Telegram/WhatsApp, slip gaji kini **tampil langsung di chat** (teks rapi tanpa tabel): semua slip untuk 1–3 karyawan, atau 3 slip pertama + rekap total bila lebih dari 3. File siap cetak dilampirkan bila bisa; bila tidak, cukup balas "kirim file". Rumus dan angka tidak berubah.

## Catatan revisi 1.0.6 (2026-10-05)
- Pemeriksaan ulang PPh 21 DTP terhadap teks PMK 105/2025 (Pasal 2 ayat 1, Pasal 5, Pasal 6 ayat 6, Lampiran B): hitungan slip **sudah benar** sejak awal (PPh 21 tetap dipotong, DTP dengan nilai sama dibayar tunai, take home pay tidak berkurang karena pajak, setoran PPh 21 bagian DTP Rp 0). Yang diperbaiki: catatan di slip (Markdown & HTML) kini menulis jelas PPh dipotong, DTP dibayar tunai, dan **setoran ke negara Rp 0** per karyawan; tambah tes regresi dan ringkasan dasar hukum `references/dtp-pmk105.md`. **PERLU REVIEW konsultan pajak.**
