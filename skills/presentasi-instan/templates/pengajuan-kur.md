# Template: Presentasi Pengajuan KUR / Kredit Bank

**Kapan dipakai:** melengkapi pengajuan Kredit Usaha Rakyat (KUR) atau kredit modal
kerja/investasi ke bank, untuk presentasi ke petugas/analis kredit (bukan pengganti
dokumen resmi bank).

**Nada:** faktual, rapi, meyakinkan kelayakan usaha — bank menilai kemampuan bayar
(kapasitas), bukan mimpi besar.

**Jumlah slide wajar:** 8–12.

> **Catatan penting:** setiap bank/penyalur KUR punya syarat dan format dokumen resmi
> sendiri (KTP, NPWP, surat izin usaha, laporan keuangan, dsb.). Presentasi ini adalah
> **pelengkap**, bukan pengganti formulir resmi. Sebutkan ini ke pengguna dan arahkan
> untuk mengecek syarat terbaru ke bank/penyalur KUR yang dituju.

## Struktur slide

1. **Sampul** — nama usaha, nama pemilik, jenis usaha, logo (jika ada).
2. **Profil usaha** — jenis usaha, lama berjalan (mis. "berjalan 3 tahun"), lokasi, jumlah karyawan.
3. **Produk/layanan** — apa yang dijual, foto produk jika ada.
4. **Omzet & histori penjualan** — data omzet bulanan/tahunan terakhir (bisa diambil dari skill `rekap-penjualan-csv` atau `laporan-keuangan-emkm` jika sudah ada), format Rupiah.
5. **Aset usaha** — daftar aset yang dimiliki (peralatan, kendaraan, stok, tempat usaha) beserta perkiraan nilai — ini memperkuat kapasitas usaha.
6. **Tujuan pinjaman** — untuk apa dana dipakai (modal kerja/pembelian alat/perluasan), spesifik dan realistis.
7. **Jumlah pinjaman diajukan & rencana pengembalian** — nominal (Rupiah), lama tenor yang diinginkan, cicilan per bulan dan rasio cicilan-terhadap-laba (WAJIB dihitung lewat skill `pengajuan-kur`/`scripts/simulasi_kur.py`, bukan diperkirakan — lihat SKILL.md bagian "Angka pinjaman/cicilan"; kalau tidak tersedia, tulis `[isi]` + catatan), dan dari mana sumber pengembaliannya (proyeksi omzet/kas).
8. **Proyeksi usaha setelah pinjaman** — perkiraan kenaikan omzet/kapasitas produksi setelah dana cair, dengan asumsi yang disebutkan jelas.
9. **Legalitas usaha** — NIB, izin usaha, NPWP jika ada (sebutkan status, jangan mengarang nomor).
10. **Penutup** — ringkasan kelayakan usaha, kontak pemilik usaha.

## Wajib ada
- Semua nominal (omzet, aset, pinjaman) wajib format Rupiah yang benar dan berdasarkan
  data yang diberikan pengguna — **jangan pernah mengarang angka omzet atau aset**.
- Cicilan per bulan dan rasio cicilan-terhadap-laba **wajib** dihitung lewat skill
  `pengajuan-kur` (atau `scripts/simulasi_kur.py`-nya), tidak boleh dikira-kira. Kalau
  skill itu tidak terpasang di environment, tulis `[isi]` pada angka tersebut disertai
  catatan bahwa cicilan perlu dihitung dengan alat simulasi KUR resmi.
- Disclaimer bahwa ini pelengkap presentasi, bukan pengganti dokumen resmi bank, dan
  syarat KUR (plafon, bunga/margin, syarat usaha) berubah dari waktu ke waktu — arahkan
  ke bank/penyalur KUR resmi atau situs kur.ekon.go.id untuk info terbaru.

## Kesalahan umum yang dihindari
- Melebih-lebihkan proyeksi omzet tanpa dasar — bank akan mengecek histori transaksi/kas riil.
- Tidak menyebutkan sumber pengembalian pinjaman — ini justru poin utama yang dinilai analis kredit.
