# Riwayat perubahan — surat-penawaran-harga

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.6 (2026-10-15)
- Temuan verifikasi aturan 2026-10-15: catatan bea meterai di `references/regulasi.md` masih bersumber artikel sekunder dengan tanda "perlu review".
- Kini dirujuk langsung ke teks resmi UU 10/2020 tentang Bea Meterai (PDF pajak.go.id, diakses 2026-10-15): objek Pasal 3 ayat (2) huruf a & g, tarif tetap Rp10.000 Pasal 5, saat terutang surat perjanjian Pasal 8 ayat (1) huruf a. Tanda "perlu review" dihapus. Isi surat, script, dan angka tidak berubah.

## Catatan revisi 1.0.5 (2026-10-01)
- Temuan uji ulang OpenClaw: kota "Jakarta" dikarang di surat padahal tidak diberikan.
- Kini kota/tanggal/nomor yang tidak diberikan menjadi `[isi: …]` atau asumsi tercantum; default wajib masuk daftar asumsi.

## Catatan revisi 1.0.4 (2026-10-01)
- Temuan uji ulang OpenClaw: surat hanya disimpan ke file (tidak tampil di chat, teks WA tidak dibuat), PIC ditulis `[Nama PIC]`, dan non-PKP ditulis "belum kena PPN".
- Kini balasan chat wajib memuat isi surat lengkap + teks WA siap kirim; file hanya tambahan. PIC tidak diketahui → "Bapak/Ibu Bagian Pengadaan". Non-PKP → "Harga final; penjual bukan PKP sehingga tidak memungut PPN." (catatan script diperbarui + 1 tes baru).

## Catatan revisi 1.0.3 (2026-10-01)
- Temuan uji OpenClaw: teks WA menulis "Surat penawaran resmi (PDF) terlampir" padahal tidak ada file yang dibuat.
- Teks WA kini tidak boleh menyebut lampiran yang tidak benar-benar dikirim. Surat lengkap disediakan sebagai versi siap cetak (markdown, bisa disimpan sebagai `SPH-<nomor>.md`); skill menyebut terus terang bahwa PDF tidak dibuat dan memberi cara menyimpannya sebagai PDF lewat Word/Google Docs. Script tidak berubah.
