# Checklist Dokumen & Template Narasi Pengajuan KUR

## A. Checklist dokumen
Tampilkan sebagai daftar centang. Baris bertanda **[Permenko]** adalah syarat di Permenko Perekonomian 1/2026 (lihat `regulasi.md`). Baris lain adalah praktik umum bank dan wajib diberi label **(cek ke bank penyalur)**.

**Syarat inti [Permenko 1/2026]**
- [ ] KTP-el pemohon (atau surat keterangan pembuatan KTP-el): NIK **[Permenko]**
- [ ] NIB dari OSS (oss.go.id) **atau** surat keterangan usaha mikro/kecil dari pejabat berwenang (mis. kelurahan/desa) **[Permenko]**
- [ ] Usaha sudah berjalan **≥ 6 bulan** **[Permenko]**. Pengecualian: Super Mikro < 6 bulan boleh bila ikut pendampingan/pelatihan, tergabung kelompok usaha, atau punya anggota keluarga yang sudah berusaha; pekerja terkena PHK untuk KUR Mikro: usaha ≥ 3 bulan + pelatihan kewirausahaan.
- [ ] NPWP: **wajib** untuk KUR Kecil dan untuk KUR Mikro dengan pinjaman > Rp50 juta **[Permenko]**

**Identitas & keluarga (cek ke bank penyalur)**
- [ ] Kartu Keluarga (cek ke bank penyalur)
- [ ] KTP pasangan & surat nikah, bila sudah menikah (cek ke bank penyalur)
- [ ] Pas foto (cek ke bank penyalur)

**Bukti usaha berjalan (cek ke bank penyalur)**
- [ ] Foto tempat usaha, produk, dan aktivitas usaha
- [ ] Catatan penjualan/pembukuan 6–12 bulan terakhir (buku kas, rekap kasir, laporan marketplace)
- [ ] Mutasi rekening 3–6 bulan terakhir (cek ke bank penyalur)
- [ ] Nota pembelian bahan/stok, daftar pelanggan tetap/kontrak (bila ada)
- [ ] Izin/sertifikat lain bila relevan (PIRT, halal, dll.), hanya jika memang dimiliki
- [ ] Usaha perdagangan berorientasi ekspor: dokumen proses ekspor (syarat bunga 6% tanpa batas akad) **[Permenko]**

**Rencana & kemampuan bayar**
- [ ] Rencana penggunaan dana (rincian + penawaran harga/nota proforma untuk pembelian alat)
- [ ] Hitungan laba bersih bulanan & simulasi cicilan (dari skill ini)

**Riwayat kredit**
- [ ] Cek SLIK OJK sendiri (layanan resmi OJK). Bank akan mengecek SLIK **[Permenko Pasal 14]**. Pastikan kolektibilitas lancar.
- [ ] Pernah punya kredit **komersial produktif** (bank/koperasi)? Menurut Permenko, calon penerima KUR harus **belum pernah** menerimanya. Tidak termasuk: kredit konsumsi rumah tangga, kredit ultra mikro s.d. Rp20 juta, dan pinjaman fintech/pembiayaan digital **[Permenko]**.
- [ ] Kredit yang **boleh** sedang berjalan asal lancar: KPR, kredit/leasing motor untuk usaha, kredit jaminan SK pensiun, kartu kredit, resi gudang, kredit konsumsi rumah tangga **[Permenko]**
- [ ] Kredit lama yang sudah lunas tetapi masih tercatat di SLIK: siapkan **surat keterangan lunas/roya** + bukti cetak rekening **[Permenko Pasal 14]**

**Hak debitur & tanda bahaya (sampaikan ke pengguna)**
- Plafon s.d. Rp100 juta: bank **tidak boleh** meminta agunan tambahan (Permenko 1/2026 Pasal 20). Jika diminta, tanyakan dasarnya dan pertimbangkan melapor lewat kanal pengaduan resmi.
- Uang yang cair harus **sama** dengan nilai di akad (Pasal 13 ayat 2), jadi tidak boleh ada potongan. Rincian biaya lain (asuransi, notaris, materai) tanyakan ke bank.
- Ada yang menjanjikan "pasti cair" dengan imbalan/fee → tolak; KUR diajukan langsung ke bank/lembaga penyalur.

## B. Template narasi profil usaha (±150–250 kata, bahasa sederhana, fakta dari pengguna saja)
```
PROFIL USAHA
Nama usaha      : …
Pemilik         : …
Alamat usaha    : …
Bidang usaha    : … (produksi / perdagangan / jasa / pertanian …)
Mulai berjalan  : bulan/tahun … (± … tahun)
Legalitas       : NIB … / SKU … (sebut yang dimiliki saja)
Karyawan        : … orang

Gambaran usaha
<Nama usaha> menjual/memproduksi … untuk pelanggan … di … . Penjualan dilakukan melalui … (toko, pesanan WhatsApp, marketplace, reseller). Dalam 6 bulan terakhir omzet rata-rata Rp … per bulan dengan laba bersih sekitar Rp … per bulan (berdasarkan catatan …).

Keunggulan & peluang
… (pelanggan tetap, pesanan yang belum bisa dipenuhi, kontrak, musim ramai) — hanya fakta yang disampaikan pengguna.

Kebutuhan dana
Pinjaman Rp … untuk … (lihat rincian). Dana ini diperkirakan meningkatkan … (kapasitas produksi/stok/penjualan) sebesar … — tulis sebagai PERKIRAAN pengguna, bukan janji.

Kemampuan membayar
Dengan laba bersih Rp … per bulan dan perkiraan cicilan Rp … (simulasi, tenor … bulan), porsi cicilan sekitar …% dari laba bersih.
```
Aturan: jangan mengarang omzet, pelanggan, penghargaan, sertifikat, atau proyeksi. Jika data belum ada, tulis `[isi: …]`.

## C. Template rencana penggunaan dana
| No | Pos | Nominal | % | Keterangan (bukti/penawaran) |
|---|---|---:|---:|---|
| 1 | … | Rp … | …% | … |
| | **Total** | **Rp …** | 100% | harus = plafon diajukan |

Jumlah & persen dihitung dengan `--rincian-dana` di script. Pisahkan **modal kerja** (bahan, stok) dan **investasi** (alat, renovasi) karena batas tenornya berbeda (Permenko 1/2026: Super Mikro & Mikro 3 th modal kerja / 5 th investasi; Kecil 4 th / 5 th).
