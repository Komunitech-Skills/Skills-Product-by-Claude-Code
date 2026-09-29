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

Dasar usulan: ±50% dari total harga ecer (acuan `research/harga.md`) supaya bundle
jelas lebih hemat, namun tetap di bawah langganan SaaS 1–2 bulan yang digantikan.
Skill yang diusulkan eksklusif VIP (perjanjian-sederhana, laporan-keuangan-emkm,
pantau-pasar-kripto, laporan-harian-usaha) sengaja tidak dimasukkan.

Semua bundle sudah diuji `build.py --izinkan-draft` (2026-09-24) dan berhasil.
Penjualan nyata menunggu: status skill `rilis` + `tier_final`/`harga_final_idr` dari pemilik.

Bundle baru (2026-09-29, harga bundle belum diusulkan — menunggu pemilik):
- `paket-kantor-manajemen` (16 skill): pendamping `solusi-vip/kantor-manajemen/`. Sengaja tanpa
  `laporan-harian-usaha` (tier vip) serta `frappe-books-usaha`/`dolibarr-usaha` (butuh aplikasi
  terpasang; pembeli memilih salah satu).
- `paket-kripto-keuangan` (5 skill): pendamping `solusi-vip/kripto-keuangan/`. Sengaja tanpa
  `pantau-pasar-kripto` (tier vip); tanpa auto-trading dan tanpa rekomendasi beli/jual.
