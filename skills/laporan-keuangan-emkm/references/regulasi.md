# Dasar Aturan — Laporan Keuangan SAK EMKM

**Berlaku per:** 23 September 2026 (dicek saat skill dibuat); dicek ulang ke situs IAI 14 Oktober 2026. Standar akuntansi bisa diperbarui IAI; cek ulang sumber di bawah bila ragu.

## SAK EMKM (Standar Akuntansi Keuangan Entitas Mikro, Kecil, dan Menengah)
- Diterbitkan Dewan Standar Akuntansi Keuangan Ikatan Akuntan Indonesia (DSAK IAI); disahkan 24 Oktober 2016, berlaku efektif sejak 1 Januari 2018 (penerapan dini diperkenankan). Per pengecekan 14 Oktober 2026, IAI menyatakan belum ada revisi. Tetap berlaku untuk UMKM.
- **Laporan keuangan minimum:** (1) Laporan Posisi Keuangan pada akhir periode, (2) Laporan Laba Rugi selama periode, (3) Catatan atas Laporan Keuangan.
- **Laporan Arus Kas bukan bagian dari laporan minimum SAK EMKM** (tidak ada bab tersendiri di daftar bab SAK EMKM). Skill ini menyertakannya sebagai **pelengkap praktis** (metode langsung, basis kas), misalnya untuk lampiran pengajuan KUR/bank, dan output script menandainya "tambahan, tidak diwajibkan SAK EMKM".
- **Dasar pengukuran:** biaya historis. **Asumsi dasar:** dasar akrual dan kelangsungan usaha.
- **Konsep entitas bisnis:** transaksi usaha dipisahkan dari transaksi pribadi pemilik → pengambilan pribadi dicatat sebagai **prive** (pengurang ekuitas), bukan beban.
- **Pos Laporan Posisi Keuangan** yang dapat disajikan: kas dan setara kas, piutang, persediaan, aset tetap, utang usaha, utang bank, ekuitas. SAK EMKM tidak menentukan format/urutan; aset dapat diurutkan menurut likuiditas dan liabilitas menurut jatuh tempo.
- **Pos Laporan Laba Rugi** minimum: pendapatan, beban keuangan, beban pajak.
- **Catatan atas Laporan Keuangan** memuat: pernyataan bahwa laporan disusun sesuai SAK EMKM, ikhtisar kebijakan akuntansi, dan informasi tambahan/rincian pos tertentu.
- Aset tetap diukur sebesar biaya perolehan dan disusutkan (skill ini memakai metode garis lurus tanpa nilai sisa bila pengguna memberi umur manfaat).

Sumber:
- IAI — Tentang SAK EMKM: https://web.iaiglobal.or.id/SAK-IAI/Tentang%20SAK%20EMKM
- IAI — Produk SAK EMKM Disahkan (tanggal pengesahan & status revisi): https://web.iaiglobal.or.id/SAK-IAI/Produk%20SAK%20EMKM%20Disahkan
- IAI — SAK EMKM Efektif per 1 Januari 2018 (daftar bab: Penyajian, Posisi Keuangan, Laba Rugi, Catatan, dst.): https://web.iaiglobal.or.id/SAK-EMKM-Efektif/SAK%20EMKM%20Efektif%20Per%201%20Januari%202018
- Teks SAK EMKM (IAI), halaman pos laporan posisi keuangan: https://www.iaiglobal.or.id/v03/files/file_sak/emkm/files/basic-html/page21.html
- Catatan riset internal kurator (tidak disertakan dalam paket)

## Terkait pajak (hanya konteks, skill ini TIDAK menghitung pajak)
- PPh final UMKM 0,5% (PP 55/2022 sebagaimana diubah PP 20/2026): pembayaran PPh yang tercatat di buku kas disajikan sebagai "Beban pajak penghasilan". Perhitungan pajak → skill `pph-final-umkm` atau konsultan/DJP.
- PPN yang dipungut PKP bukan pendapatan dan penyetorannya bukan beban; karena itu kata "PPN" tidak diklasifikasi otomatis dan harus ditanyakan.

## Disclaimer wajib di output
"Laporan ini disusun dari data yang Anda berikan dan mengacu pada SAK EMKM. Ini BUKAN laporan yang telah diaudit akuntan publik dan bukan nasihat pajak."

## Kapan arahkan ke profesional
- Laporan untuk tender pemerintah/BUMN, investor besar, atau bank yang mensyaratkan laporan audit/reviu akuntan.
- Usaha berbentuk PT non-perorangan atau yang sudah wajib memakai SAK EP / SAK Indonesia.
- Ada transaksi valuta asing, sewa pembiayaan/leasing kompleks, konsolidasi beberapa usaha, atau sengketa pajak.
- Perlakuan PB1/PBJT (titipan/utang pajak daerah vs beban) pada laporan yang akan diaudit atau direviu bank: minta akuntan memeriksa pilihan akunnya.
