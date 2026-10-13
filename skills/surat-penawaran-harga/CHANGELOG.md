# Riwayat perubahan — surat-penawaran-harga

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.5 (2026-10-01)
- Temuan uji ulang OpenClaw: kota "Jakarta" dikarang di surat padahal tidak diberikan.
- Kini kota/tanggal/nomor yang tidak diberikan menjadi `[isi: …]` atau asumsi tercantum; default wajib masuk daftar asumsi.

## Catatan revisi 1.0.4 (2026-10-01)
- Temuan uji ulang OpenClaw: surat hanya disimpan ke file (tidak tampil di chat, teks WA tidak dibuat), PIC ditulis `[Nama PIC]`, dan non-PKP ditulis "belum kena PPN".
- Kini balasan chat wajib memuat isi surat lengkap + teks WA siap kirim; file hanya tambahan. PIC tidak diketahui → "Bapak/Ibu Bagian Pengadaan". Non-PKP → "Harga final; penjual bukan PKP sehingga tidak memungut PPN." (catatan script diperbarui + 1 tes baru).

## Catatan revisi 1.0.3 (2026-10-01)
- Temuan uji OpenClaw: teks WA menulis "Surat penawaran resmi (PDF) terlampir" padahal tidak ada file yang dibuat.
- Teks WA kini tidak boleh menyebut lampiran yang tidak benar-benar dikirim. Surat lengkap disediakan sebagai versi siap cetak (markdown, bisa disimpan sebagai `SPH-<nomor>.md`); skill menyebut terus terang bahwa PDF tidak dibuat dan memberi cara menyimpannya sebagai PDF lewat Word/Google Docs. Script tidak berubah.
