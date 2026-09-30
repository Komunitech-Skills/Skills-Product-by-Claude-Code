# Bundle tematik (usulan — harga final diputuskan pemilik)

Satu file `.txt` = satu bundle (satu nama skill per baris), dipakai oleh
`python3 scripts/build.py --pembeli "..." --bundle <nama>`. Skill ber-tier `vip`
tidak boleh masuk bundle ecer (dicek otomatis oleh build.py).

| Bundle | Isi (jumlah skill) | Total harga ecer usulan | Harga bundle usulan | Untuk siapa |
|---|---|---|---|---|
| paket-toko-online | 10 | Rp1.040.000 | Rp449.000 | Seller marketplace & toko online |
| paket-admin-keuangan | 11 | Rp1.040.000 | Rp449.000 | Admin/pemilik yang mengurus invoice, piutang, pajak UMKM |
| paket-gaji-hr | 6 | Rp694.000 | Rp349.000 | Usaha dengan karyawan (gaji, PPh 21, THR, absensi) |
| paket-kafe-warung | 7 | Rp694.000 | Rp349.000 | Kafe, warung, kedai (kasir lokal + stok + konten) |
| paket-kantor | 5 | Rp296.000 | Rp199.000 | Admin kantor & sekretaris |
| paket-klinik | 5 | Rp495.000 | Rp249.000 | Klinik pratama/gigi/kecantikan, praktik mandiri |
| paket-konsultan-freelancer | 8 | Rp742.000 | Rp349.000 | Konsultan, agensi, freelancer B2B |
| paket-karyawan-ai-openclaw | 5 | Rp347.000 | Rp199.000 | Pengguna OpenClaw pemula (starter kit, privasi, laporan, ringkas grup) |
| paket-strategi-produk-marketing | 11 | Rp1.339.000 | Rp599.000 | Pemilik usaha/tim yang mengembangkan & memasarkan produk (positioning, pesaing, harga, peluncuran, uji pasar, masukan pelanggan, analitik web, newsletter, papan masukan) |
| paket-kantor-manajemen | 17 | Rp1.386.000 | Rp599.000 | Kantor/usaha yang ingin AI mengelola administrasi & manajemen harian lewat OpenClaw (subset solusi VIP kantor-manajemen) |

Dasar usulan: ±50% dari total harga ecer (acuan `research/harga.md`) supaya bundle
jelas lebih hemat, namun tetap di bawah langganan SaaS 1–2 bulan yang digantikan.
Skill yang diusulkan eksklusif VIP (perjanjian-sederhana, laporan-keuangan-emkm,
pantau-pasar-kripto, laporan-harian-usaha) sengaja tidak dimasukkan.

Semua bundle sudah diuji `build.py --izinkan-draft` (2026-09-24) dan berhasil.
Penjualan nyata menunggu: status skill `rilis` + `tier_final`/`harga_final_idr` dari pemilik.

**Harga final disetujui pemilik (2026-09-30):** `paket-strategi-produk-marketing` = **Rp599.000**,
`paket-kantor-manajemen` = **Rp599.000**. Bundle lain masih usulan.

Bundle baru (2026-09-29, harga bundle belum diusulkan — menunggu pemilik):
- `paket-kantor-manajemen` (16 skill) adalah **subset** dari `solusi-vip/kantor-manajemen/`.
  Mencakup PANDUAN Bab 2-4 dan 5c-5e, 5f-5h, 5i, 5j-k, 5m. **Tidak** mencakup 5a-5b dan
  `jadwal-openclaw.md` §1, §2, §6 (butuh `laporan-harian-usaha`, tier vip) maupun 5l/§9
  (pilih `frappe-books-usaha` ATAU `dolibarr-usaha`, perlu aplikasi terpasang). Paket lengkap
  = akses VIP.
- Paket kripto (`solusi-vip/kripto-keuangan/`) **khusus VIP**: tidak ada bundle ecer karena
  intinya, `pantau-pasar-kripto`, bertier vip. Skill pendukungnya (`atur-keuangan-pribadi`,
  `notebook-riset-lokal`, `asisten-tulis-riset`) bisa dibeli ecer satuan.
