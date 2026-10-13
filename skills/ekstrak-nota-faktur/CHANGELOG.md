# Riwayat perubahan — ekstrak-nota-faktur

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.4 (2026-10-01)
- Bila PPN atau total buram tetapi DPP/subtotal terbaca, kolom **PPN Seharusnya** dan **Total Seharusnya** tetap terisi dari hitungan sebagai pembanding (total tetap tidak ikut rekap sampai dicocokkan).
- Digit buram ditulis dengan `?` (mis. `92?.000`) dan ditandai jelas `[cek: 92?.000]`; script memberi tahu apakah hitungannya sesuai pola yang terlihat.
- Kategori pengeluaran yang ditebak kini selalu disebut sebagai asumsi.
