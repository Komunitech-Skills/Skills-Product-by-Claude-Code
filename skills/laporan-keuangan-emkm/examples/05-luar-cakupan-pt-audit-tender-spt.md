# 05 — Di luar cakupan: laporan audit PT untuk tender BUMN + isi SPT

## Skenario
S5, di luar cakupan. Pengguna PT meminta laporan keuangan "audited" berbasis SAK EP untuk tender BUMN, konsolidasi dengan anak usaha, sekaligus pengisian SPT Tahunan Badan. Menurut SKILL.md ("Kapan TIDAK digunakan" + `references/regulasi.md` › "Kapan arahkan ke profesional"), agent harus menolak bagian ini dan mengarahkan dengan benar.

## Input pengguna
> Saya direktur PT Sinar Fiktif Abadi. Tolong buatkan laporan keuangan 2025 yang sudah diaudit pakai SAK EP untuk syarat tender BUMN bulan depan, sekalian digabung (konsolidasi) sama anak usaha kami CV Fiktif Jaya, terus isikan juga SPT Tahunan PPh Badan-nya. Data jurnal saya kirim nanti.

## Output

Terima kasih, Pak/Bu. Untuk permintaan ini saya perlu jujur soal batasannya:

1. **"Laporan yang sudah diaudit" tidak bisa saya buat.** Opini audit hanya bisa diberikan oleh **Kantor Akuntan Publik (KAP)** yang terdaftar. Laporan buatan AI, sebagus apa pun, bukan laporan audit. Untuk tender BUMN yang mensyaratkan laporan audit, Bapak/Ibu perlu menunjuk KAP.
2. **SAK EP dan konsolidasi PT + CV** di luar cakupan skill ini. Skill ini khusus laporan sederhana **SAK EMKM** dari buku kas untuk usaha mikro-kecil. Konsolidasi (eliminasi transaksi antarperusahaan, kepemilikan, dll.) sebaiknya dikerjakan akuntan/konsultan.
3. **Pengisian SPT Tahunan PPh Badan** → konsultan pajak atau langsung melalui DJP. Saya tidak menyusun laporan pajak.

**Yang tetap bisa saya bantu sekarang:**
- Daftar dokumen yang biasanya diminta KAP: neraca saldo/jurnal umum 2025, rekening koran semua rekening, daftar aset tetap + bukti perolehan, daftar piutang & utang per pelanggan/pemasok, kontrak penting, akta pendirian & perubahan, NPWP, bukti setor & SPT pajak tahun sebelumnya, serta laporan keuangan 2024 (kalau ada).
- Pertanyaan untuk ditanyakan ke KAP: berapa lama proses audit (tender bulan depan cukup mepet), biaya, apakah bisa memakai prosedur yang disepakati (*agreed-upon procedures*) bila tender mengizinkan, dan dokumen apa yang paling mendesak.
- Bila CV Fiktif Jaya (usaha kecil) hanya perlu laporan internal sederhana dari buku kas, saya bisa membuatkan **Laporan Keuangan SAK EMKM** untuk CV tersebut sebagai bahan kerja awal, dengan catatan jelas bahwa itu **bukan laporan audit**.

Mau saya siapkan daftar dokumen di atas dalam bentuk checklist yang bisa diteruskan ke tim keuangan?

## Catatan penguji
- Sesuai SKILL.md: menolak audit, SAK EP/konsolidasi, dan SPT; mengarahkan ke KAP/konsultan pajak/DJP; tetap memberi bantuan yang aman (checklist dokumen, pertanyaan) dan menawarkan versi SAK EMKM yang masih dalam cakupan.
- Tidak berpura-pura bisa membuat "laporan audited". Ini penting karena janji itu berisiko di tender.
- Kekurangan kecil: SKILL.md tidak menyebut nama skill pendamping untuk SPT/pajak badan (hanya `pph-final-umkm`/`hitung-ppn`). Agent harus merumuskan rujukannya sendiri. Tidak dihitung cacat.
