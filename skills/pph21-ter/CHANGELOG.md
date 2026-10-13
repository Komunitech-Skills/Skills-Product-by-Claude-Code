# Riwayat perubahan — pph21-ter

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.6 (2026-10-13)
- Batasan di SKILL.md ditambah satu aturan: setiap tarif/aturan disebut dengan dasar aturan + tahun; angka hanya dari script/input pengguna; nilai yang tidak diberikan pengguna ditandai asumsi (tanpa label "wajar/umum/lazim" yang tidak bersumber).
- Contoh uji `examples/01`: asumsi BPJS Kesehatan diberi dasar (iuran pemberi kerja 4% + pekerja 1%, Perpres 82/2018; dasar upah maksimal sesuai ketentuan). Angka PPh 21 dicek ulang dengan script: tidak berubah.

## Catatan revisi 1.0.5 (2026-10-05)
- **Koreksi PPh 21 DTP (PMK 105/2025):** versi 1.0.4 menulis "PPh 21 dipotong Rp 0" dan "uang diterima = gaji + DTP" (contoh Rp 6.045.000). Setelah teks resmi dibaca ulang (Pasal 2 ayat 1, Pasal 5, Pasal 6 ayat 6, Lampiran B), mekanisme yang benar: PPh 21 tetap dipotong, DTP dengan nilai sama dibayar tunai ke pegawai, sehingga pegawai menerima **Rp 6.000.000** (gaji tidak berkurang pajak), dan setoran ke negara untuk bagian DTP Rp 0. Script kini mencetak empat baris: PPh dipotong, DTP tunai, setoran ke negara, uang diterima. Ringkasan dasar hukum: `references/dtp-pmk105.md`. **PERLU REVIEW konsultan pajak.**

## Catatan revisi 1.0.4 (2026-10-01)
> **DIKOREKSI di 1.0.5 (2026-10-05):** butir DTP di bawah ini **keliru** dan dibiarkan hanya sebagai riwayat. Menurut PMK 105/2025, PPh 21 DTP **tetap dipotong** (bukan Rp 0) lalu nilai yang sama dibayar tunai, sehingga pegawai gaji Rp 6.000.000 **menerima Rp 6.000.000**, bukan Rp 6.045.000. Lihat "Catatan revisi 1.0.5" di atas dan `references/dtp-pmk105.md`.

- ~~Dari uji OpenClaw sebelum/sesudah: untuk karyawan penerima **PPh 21 DTP 2026**, jawaban sempat menyebut gaji diterima "Rp 6.000.000 utuh", padahal PMK 105/2025 Pasal 5 mewajibkan PPh 21 DTP **dibayarkan tunai** ke karyawan (yang benar Rp 6.045.000). Kini hitungan satu bulan (`bulan`) juga mendukung `--dtp` dan mencetak tiga baris wajib: PPh 21 dipotong dari gaji (Rp 0), DTP yang wajib dibayar tunai, dan **uang yang diterima pegawai**; AI wajib mengutip baris itu dari script. Hitungan setahun dengan DTP juga menegaskan hal yang sama.~~ *(dikoreksi di 1.0.5: yang benar PPh 21 dipotong Rp 45.000, DTP tunai Rp 45.000, diterima Rp 6.000.000 sesuai PMK 105/2025)*
- Istilah seperti KLU, TER, Masa Pajak Terakhir, dan DTP kini dijelaskan dengan bahasa sehari-hari saat pertama muncul.
