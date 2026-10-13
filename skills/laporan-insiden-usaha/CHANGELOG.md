# Riwayat perubahan — laporan-insiden-usaha

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.3 (2026-10-13)
- Batasan di SKILL.md: aturan anti-karangan diperluas dari angka ke tindakan (tindakan yang "sudah dilakukan" hanya dari input pengguna; selebihnya `[isi: ...]`). Temuan audit contoh: `examples/01` memuat tindakan "menghubungi 15 pelanggan / membalas 5 komplain" yang tidak ada di input; kini diganti `[isian: tindakan yang sudah Anda lakukan]`. Logika langkah kerja tidak berubah.

## Catatan revisi 1.0.2 (2026-10-01)
Hasil uji sebelum/sesudah di OpenClaw (`examples/00-openclaw-sebelum-sesudah.md`):
- **Cabang khusus insiden data pribadi** (Langkah 6 + `references/insiden-data-pribadi.md`): fakta UU 27/2022 Pasal 46 ditulis jelas (tertulis, paling lambat 3×24 jam, ke subjek data & lembaga; isi minimal ayat 2), tenggat dihitung dari jam ketahuan, draf pemberitahuan per pelanggan terdampak, catatan untuk lembaga (bila kanal resmi tersedia, tanpa mengarang alamat). Ditandai PERLU REVIEW HUKUM.
- Bila pemilik ingin tidak memberi tahu pelanggan, skill mengoreksi dengan sopan (tanpa menakut-nakuti) dan status tetap "Masih ditangani".
- Hubungi proaktif **semua** yang terdampak, bukan hanya yang sudah komplain.
- Kanal permintaan maaf mengikuti asal pelanggan (chat marketplace per pesanan / WA pribadi), bukan broadcast/status WA.
