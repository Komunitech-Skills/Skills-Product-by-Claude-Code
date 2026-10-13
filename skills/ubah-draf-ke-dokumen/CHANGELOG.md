# Riwayat perubahan — ubah-draf-ke-dokumen

Catatan teknis per versi.

## Catatan revisi 1.0.1 (2026-10-12)
- Revisi dari uji pertama (skor 5,75 naik ke 7,7) dan uji ulang (5,63 naik ke 8,28): jenis dokumen ditambah surat permohonan kredit/bank. Aturan balasan di chat diperketat: dokumen ditulis utuh di chat, file Word hanya setelah pengguna membalas "kirim file", dan dilarang menulis "File Word terlampir" bila lampiran tidak benar-benar terkirim.
- Draf jebakan (kop Dinas/pejabat palsu, tanda tangan palsu, omzet dibesar-besarkan) ditolak singkat lalu dokumen tetap disusun lengkap dengan angka dan fakta asli draf serta kop usaha pengguna atau `[isi kop]`.
- Pembersihan draf hanya membuang baris pembuka AI murni, tidak membuang baris "Berikut rincian ..." yang memuat angka; dilarang menambah klaim kualitatif yang tidak ada di draf.
- Script `buat_docx.py`: perataan tengah untuk kop dan pemisah kop; deklarasi namespace `r` ditambahkan di XML .docx (disertai tes XML). Uji regresi diperbarui.

## Catatan revisi 1.0.0 (2026-10-12)
- Rilis awal (uji internal): merapikan draf berantakan (hasil chat AI, catatan, poin-poin) menjadi dokumen Indonesia siap cetak (surat resmi, laporan, notulen rapat, proposal singkat, memo) dengan kop, judul, paragraf, tabel, dan penomoran halaman; isi utuh di chat dan file Word (.docx) hanya bila diminta, dibuat oleh script `buat_docx.py` tanpa instalasi tambahan.
