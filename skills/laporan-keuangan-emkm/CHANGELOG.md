# Riwayat perubahan — laporan-keuangan-emkm

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.3.5 (2026-10-15)
- Tindak lanjut verifikasi rujukan aturan (SAK EMKM, situs IAI, dicek 14 Oktober 2026): README, SKILL.md, dan `references/regulasi.md` kini menegaskan Laporan Arus Kas = **pelengkap praktis**, bukan laporan wajib SAK EMKM (yang wajib: Laporan Posisi Keuangan, Laporan Laba Rugi, Catatan atas Laporan Keuangan).
- `references/regulasi.md`: tambah tanggal pengesahan SAK EMKM (24 Oktober 2016), status belum ada revisi per 14 Oktober 2026, dua tautan sumber IAI, dan arahan ke akuntan untuk perlakuan PB1/PBJT pada laporan yang diaudit/direviu bank.
- Konstanta VERSI skrip disamakan (1.3.5); hitungan tidak berubah.

## Catatan revisi 1.3.4 (2026-10-13)
- `references/regulasi.md`: rujukan ke catatan riset internal diganti kalimat yang berdiri sendiri; konstanta VERSI skrip disamakan; cara kerja tidak berubah.

## Catatan revisi 1.3.3 (2026-10-01)
- Modal (ekuitas) negatif kini selalu diperiksa: skill menanyakan aset lama yang belum dicatat dan utang, tidak lagi menyebutnya "wajar".
- Tambah **Laporan Arus Kas** (operasi/investasi/pendanaan) dan ekspor **siap cetak** (`--html`, buka di browser → simpan PDF, ada kolom tanda tangan) serta CSV arus kas.
- Permintaan "mark-up omzet" untuk pinjaman ditolak tegas, dijelaskan risikonya, dan diganti tawaran laporan jujur yang rapi (termasuk dari estimasi pemilik bila tidak ada catatan).
