# Riwayat perubahan — ekstrak-nota-faktur

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.5 (2026-10-16)
- Revisi dari uji di bot Telegram asli (gelombang 18): di kanal chat (Telegram/WhatsApp) berkas hasil (CSV/Excel) yang diminta pengguna WAJIB dilampirkan sebagai dokumen bila kanal bisa mengirim file. Bila tidak bisa, jalur/folder kerja tidak disebut dan cukup ditawarkan "balas 'kirim file'" (pola sama dengan skill lain). Sebelumnya berkas hanya tersimpan di folder kerja sehingga pengguna chat tidak menerimanya.
- Tampilan di chat: tanpa tabel Markdown; satu baris padat per dokumen. Bila CSV ikut ditampilkan di chat, pakai pemisah tab dan buang kolom yang kosong di semua baris.
- Judul kolom CSV "Subtotal Dihitung Script" dan "DPP Dihitung Script" diganti "Subtotal Hitung Ulang" dan "DPP Hitung Ulang" (tidak menyebut kata "script" ke pengguna). Isi kolom dan rumus hitung PPN/pembulatan tidak berubah. Contoh lama di `examples/` masih memakai judul kolom yang lama.
- Contoh disegarkan (2026-10-16): keluaran script di `examples/01`–`04` dijalankan ulang dengan v1.0.5 (kolom "Hitung Ulang"/"Seharusnya", F2 contoh 02 kini COCOK, `TIDAK_TERBACA` seragam) dan tiap contoh 01–04 diberi bagian "Versi kanal chat" tanpa tabel Markdown; `05` diperiksa, tidak berubah. Skor/verdik uji tidak berubah; rincian di `examples/HASIL-UJI.md` bagian "Contoh disegarkan ke v1.0.5". `00-*.md` dibiarkan sebagai catatan uji historis.

## Catatan revisi 1.0.4 (2026-10-01)
- Bila PPN atau total buram tetapi DPP/subtotal terbaca, kolom **PPN Seharusnya** dan **Total Seharusnya** tetap terisi dari hitungan sebagai pembanding (total tetap tidak ikut rekap sampai dicocokkan).
- Digit buram ditulis dengan `?` (mis. `92?.000`) dan ditandai jelas `[cek: 92?.000]`; script memberi tahu apakah hitungannya sesuai pola yang terlihat.
- Kategori pengeluaran yang ditebak kini selalu disebut sebagai asumsi.
