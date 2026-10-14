# Bundle tematik (usulan — harga final diputuskan pemilik)

Satu file `.txt` = satu bundle (satu nama skill per baris), dipakai oleh
`python3 scripts/build.py --pembeli "..." --bundle <nama>`. Skill ber-tier `vip`
tidak boleh masuk bundle ecer (dicek otomatis oleh build.py).

| Bundle | Isi (jumlah skill) | Total harga ecer usulan | Harga bundle usulan | Untuk siapa |
|---|---|---|---|---|
| paket-toko-online | 16 | Rp1.575.000 | Rp449.000 | Seller marketplace & toko online |
| paket-admin-keuangan | 15 | Rp1.446.000 | Rp449.000 | Admin/pemilik yang mengurus invoice, piutang, pajak UMKM |
| paket-gaji-hr | 8 | Rp972.000 | Rp349.000 | Usaha dengan karyawan (gaji, PPh 21, THR, absensi) |
| paket-kafe-warung | 10 | Rp1.060.000 | Rp349.000 | Kafe, warung, kedai (kasir lokal + stok + konten) |
| paket-kantor | 8 | Rp593.000 | Rp199.000 | Admin kantor & sekretaris |
| paket-klinik | 7 | Rp594.000 | Rp249.000 | Klinik pratama/gigi/kecantikan, praktik mandiri |
| paket-konsultan-freelancer | 10 | Rp940.000 | Rp349.000 | Konsultan, agensi, freelancer B2B |
| paket-karyawan-ai-openclaw | 5 | Rp347.000 | Rp199.000 | Pengguna OpenClaw pemula (starter kit, privasi, laporan, ringkas grup) |
| paket-strategi-produk-marketing | 14 | Rp1.566.000 | Rp599.000 | Pemilik usaha/tim yang mengembangkan & memasarkan produk (positioning, merek & penawaran, pesaing, harga, peluncuran, uji pasar, konten & iklan, referral & loyalitas, masukan pelanggan, analitik web, newsletter, papan masukan) |
| paket-kantor-manajemen | 20 | Rp1.783.000 | Rp599.000 | Kantor/usaha yang ingin AI mengelola administrasi & manajemen harian lewat OpenClaw (subset solusi VIP kantor-manajemen) |

_Catatan: angka jumlah skill & total harga ecer disinkronkan 2026-10-03 dari isi `bundles/*.txt` dan `catalog.csv`; kolom harga bundle tidak diubah._

Dasar usulan: ±50% dari total harga ecer (acuan `research/harga.md`) supaya bundle
jelas lebih hemat, namun tetap di bawah langganan SaaS 1–2 bulan yang digantikan.
Skill yang diusulkan eksklusif VIP (perjanjian-sederhana, laporan-keuangan-emkm,
pantau-pasar-kripto, laporan-harian-usaha) sengaja tidak dimasukkan.

Semua bundle sudah diuji `build.py --izinkan-draft` (2026-09-24) dan berhasil.
Penjualan nyata menunggu: status skill `rilis` + `tier_final`/`harga_final_idr` dari pemilik.

**Harga final disetujui pemilik (2026-09-30):** `paket-strategi-produk-marketing` = **Rp599.000** (14 skill; strategi-merek-usaha & program-referral-loyalitas ditambahkan 2026-09-30, strategi-konten-iklan ditambahkan 2026-10-01, harga tetap),
`paket-kantor-manajemen` = **Rp599.000** (hitung-thr 2026-10-02, slip-gaji-bpjs & pph21-ter 2026-10-03; kini 20 skill, harga tetap). Bundle lain masih usulan.

**Keputusan pemilik 2026-10-03 (via Telegram):**
- `paket-klinik` tetap memuat `balas-chat-cs` (7 skill, Rp249.000): **disetujui**.
- `paket-toko-online` + `balas-chat-cs`, `crm-wa` (kini **16 skill**, termasuk `rencana-restok-barang` per keputusan 71); `paket-kantor-manajemen` + `slip-gaji-bpjs`, `pph21-ter` (kini 20 skill). Harga bundle tetap: **disetujui pemilik 2026-10-03**.
- `caption-sosmed-umkm` dan `brainstorming-ide-usaha` diarsipkan (status `arsip`); `caption-sosmed-umkm` dikeluarkan dari `paket-kafe-warung` (kini **10 skill** setelah keputusan 71, harga tetap Rp349.000).
- Jumlah & total ecer di tabel untuk bundle yang berubah dihitung ulang dari `harga_usulan_idr` (`paket-kafe-warung` sebelumnya tercatat 7/Rp694.000, tidak sesuai isi file; kini disinkronkan).

**Keputusan otomatis 71 (2026-10-14, mode no. 30):** tiga skill baru yang lulus uji sebelum/sesudah ditempatkan ke bundle tanpa mengubah harga bundle: `panduan-wawancara-kerja` → `paket-gaji-hr` (kini 8 skill); `rencana-restok-barang` → `paket-toko-online` (16) & `paket-kafe-warung`; `bandingkan-pemasok-vendor` → `paket-admin-keuangan` (15) & `paket-kafe-warung` (kini 10). Status ketiganya `beta` (build bundle menolak anggota `lulus`); tampil di bot Telegram uji direncanakan gelombang 17. Batalkan dengan "batal 71".

Bundle baru (2026-09-29, harga bundle belum diusulkan — menunggu pemilik):
- `paket-kantor-manajemen` (20 skill) adalah **subset** dari `solusi-vip/kantor-manajemen/`.
  Mencakup PANDUAN Bab 2-4 dan 5c-5e, 5f-5h, 5i, 5j-k, 5m. **Tidak** mencakup 5a-5b dan
  `jadwal-openclaw.md` §1, §2, §6 (butuh `laporan-harian-usaha`, tier vip) maupun 5l/§9
  (pilih `frappe-books-usaha` ATAU `dolibarr-usaha`, perlu aplikasi terpasang). Paket lengkap
  = akses VIP.
- Paket kripto (`solusi-vip/kripto-keuangan/`) **khusus VIP**: tidak ada bundle ecer karena
  intinya, `pantau-pasar-kripto`, bertier vip. Skill pendukungnya (`atur-keuangan-pribadi`,
  `notebook-riset-lokal`, `asisten-tulis-riset`) bisa dibeli ecer satuan.
