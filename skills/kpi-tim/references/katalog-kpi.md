# Katalog KPI untuk UMKM Indonesia

Dipakai saat pengguna bertanya "KPI apa yang cocok untuk ...?" atau saat menyusun rencana KPI.
KPI bertanda ★ adalah **set bawaan** di `scripts/skor_kpi.py katalog` / `template` (4 KPI per
peran, bobot usulan total 100). Sisanya adalah alternatif yang bisa ditukar.

**Target di bawah hanya contoh.** Target yang adil = data rata-rata 3 bulan terakhir orang/usaha
itu + kenaikan wajar (mis. 5–10%), bukan angka dari internet. Bila belum ada data, pakai 1 bulan
pertama sebagai "bulan pengukuran" (tanpa penilaian), baru pasang target.

Kolom:
- **Arah**: `naik` = makin tinggi makin baik; `turun` = makin rendah makin baik.
- **Frek.**: seberapa sering realisasi dicatat (H = harian, M = mingguan, B = bulanan).
- **Sumber data**: skill Komunitech atau catatan yang menghasilkan angka realisasi. "log" =
  `templates/log-operasional-contoh.csv` lalu `skor_kpi.py rekap-log`.

## 1. Sales (penjualan lapangan / online / WA)

| KPI | Rumus | Satuan | Arah | Frek. | Sumber data |
|---|---|---|---|---|---|
| ★ Omzet penjualan | jumlah nilai penjualan periode (setelah retur) | Rp | naik | M/B | `kasir-lokal rekap`, `rekap-penjualan-csv`, `crm-wa rekap` (nilai deal) |
| ★ Jumlah closing | jumlah prospek yang masuk tahap deal | deal | naik | M/B | `crm-wa rekap` |
| ★ Konversi prospek | deal ÷ prospek baru × 100 (boleh tulis `14/50` di realisasi) | % | naik | B | `crm-wa rekap` |
| ★ Follow-up tepat waktu | follow-up dilakukan sesuai jadwal ÷ jadwal follow-up × 100 | % | naik | M | `crm-wa hari-ini` / daftar terlambat |
| Pelanggan baru | jumlah pelanggan/toko pertama kali order | toko | naik | B | `crm-wa`, `buku-piutang` (pelanggan baru) |
| Rata-rata nilai order | omzet ÷ jumlah transaksi | Rp | naik | B | `kasir-lokal rekap`, `rekap-penjualan-csv` |
| Piutang tertagih tepat waktu (untuk sales yang juga menagih) | pembayaran ≤ jatuh tempo ÷ tagihan jatuh tempo × 100 | % | naik | B | `buku-piutang umur` |

## 2. Customer Service (CS / admin chat)

| KPI | Rumus | Satuan | Arah | Frek. | Sumber data |
|---|---|---|---|---|---|
| ★ Waktu respons pertama | rata-rata menit dari chat masuk sampai balasan pertama (jam kerja) | menit | turun | H/M | log (`cara` = rata-rata), catatan `agen-cs-toko` |
| ★ Komplain selesai ≤ 2 hari | komplain selesai ≤ 2×24 jam ÷ komplain masuk × 100 | % | naik | M | log (`cara` = persen, nilai ya/tidak) |
| ★ Rating kepuasan | rata-rata bintang ulasan periode | skala 1–5 | naik | B | `analisis-ulasan`, ulasan marketplace |
| ★ Chat terjawab hari yang sama | chat dijawab di hari yang sama ÷ chat masuk × 100 | % | naik | M | log |
| Chat → pesanan | pesanan dari chat ÷ chat pertanyaan produk × 100 | % | naik | B | `crm-wa`, log |

Jangan jadikan **jumlah komplain masuk** sebagai KPI CS: itu dipengaruhi gudang/produk, bukan
kerja CS (KPI harus bisa dikendalikan orangnya).

## 3. Produksi (pabrik kecil, konveksi, makanan)

| KPI | Rumus | Satuan | Arah | Frek. | Sumber data |
|---|---|---|---|---|---|
| ★ Output produksi | unit barang jadi lolos QC | unit | naik | H/M | log (`cara` = jumlah) |
| ★ Tingkat reject | unit reject ÷ unit diproduksi × 100 (tulis `12/600`) | % | turun | M | catatan QC |
| ★ Produksi tepat jadwal | order produksi selesai ≤ tanggal rencana ÷ total order × 100 | % | naik | M | log (persen) |
| ★ Kecelakaan kerja | jumlah kejadian cedera/nyaris celaka | kejadian | turun (target 0) | B | `laporan-insiden-usaha` |
| Pemakaian bahan vs standar | bahan terpakai ÷ standar resep/BOM × 100 | % | turun | B | `hitung-hpp`, `buku-stok` |
| Mesin berhenti tak terencana | jam mesin mati di luar jadwal | jam | turun | M | log |

Target 0 kecelakaan memakai aturan "nol kejadian" (lihat `aturan-skor.md`). Hati-hati: KPI ini
bisa membuat orang **menyembunyikan** kejadian. Pertimbangkan KPI pendamping "laporan nyaris
celaka dilaporkan" (arah naik) supaya melapor dihargai.

## 4. Gudang

| KPI | Rumus | Satuan | Arah | Frek. | Sumber data |
|---|---|---|---|---|---|
| ★ Akurasi stok | (1 − |selisih opname| ÷ jumlah dicek) × 100, atau SKU tanpa selisih ÷ SKU dicek × 100 | % | naik | B | `buku-stok opname` |
| ★ Pesanan dikemas hari yang sama | pesanan masuk sebelum jam potong yang dikemas hari itu ÷ pesanan × 100 | % | naik | H/M | `buku-stok impor-pesanan`, `resi-picking`, log |
| ★ Salah kirim | pesanan salah barang/varian/jumlah | pesanan | turun | M | log komplain, retur |
| ★ Item stok habis | SKU aktif dengan stok 0 saat dicek | SKU | turun | M | `buku-stok laporan menipis` |
| Barang rusak di gudang | nilai barang rusak ÷ nilai persediaan × 100 | % | turun | B | `buku-stok` |
| Waktu bongkar barang masuk | rata-rata jam dari barang datang sampai tercatat | jam | turun | M | log |

## 5. Keuangan

| KPI | Rumus | Satuan | Arah | Frek. | Sumber data |
|---|---|---|---|---|---|
| ★ Hari tutup buku | hari kerja setelah akhir bulan sampai laporan bulanan selesai | hari | turun | B | `laporan-keuangan-emkm`, `hledger-usaha` |
| ★ Piutang lewat 30 hari | piutang umur > 30 hari ÷ total piutang × 100 | % | turun | B | `buku-piutang umur` |
| ★ Tagihan terkirim tepat waktu | faktur dikirim ≤ 1 hari setelah barang dikirim ÷ total faktur × 100 | % | naik | B | `buat-invoice`, `buku-piutang` |
| ★ Selisih kas | total |selisih| hitung fisik vs catatan kas | Rp | turun | M/B | `kas-umkm opname` |
| Rekonsiliasi bank selesai | rekening direkonsiliasi tepat waktu ÷ rekening × 100 | % | naik | B | `rekonsiliasi-bank` |
| Pajak dilapor tepat waktu | kewajiban dilapor ≤ tenggat ÷ total kewajiban × 100 | % | naik | B | `kalender-pajak` |

## 6. Marketing

| KPI | Rumus | Satuan | Arah | Frek. | Sumber data |
|---|---|---|---|---|---|
| ★ Leads masuk | prospek baru tercatat (chat/form) | lead | naik | M | `crm-wa` (sumber lead), `laporan-iklan-mingguan` |
| ★ Biaya per lead (CPL) | belanja iklan ÷ lead | Rp | turun | M | `laporan-iklan-mingguan` |
| ★ ROAS | omzet dari iklan ÷ belanja iklan | x | naik | M | `laporan-iklan-mingguan` |
| ★ Konten terbit sesuai kalender | konten terbit ÷ konten direncanakan × 100 | % | naik | M | `kalender-konten-30hari`, `konten-mingguan` |
| Lead → pelanggan | lead jadi pembeli ÷ lead × 100 | % | naik | B | `crm-wa` |

Hindari "jumlah likes/followers" sebagai KPI utama: mudah naik tanpa menambah penjualan.

## 7. Admin kantor

| KPI | Rumus | Satuan | Arah | Frek. | Sumber data |
|---|---|---|---|---|---|
| ★ Tugas selesai tepat waktu | tugas selesai ≤ tenggat ÷ tugas bertenggat × 100 | % | naik | M | `vikunja-tugas`, `notulen-rapat`, `ringkas-grup-wa` |
| ★ Kesalahan input data | kesalahan ditemukan saat cek (nota, stok, data karyawan) | kesalahan | turun | B | cek atasan, daftar "PERLU DICEK" `absensi-lokal` |
| ★ Nota diarsip lengkap | nota/faktur terarsip ÷ nota periode × 100 | % | naik | B | `arsip-nota` |
| ★ Kehadiran tepat waktu | hari masuk tepat waktu ÷ hari kerja × 100 | % | naik | B | `absensi-lokal rekap` |
| Surat/dokumen selesai ≤ 1 hari | dokumen selesai ≤ 1 hari ÷ permintaan × 100 | % | naik | M | log |

**Kehadiran** hanya cocok sebagai KPI kecil (bobot ≤ 15%). Ketepatan hadir adalah kewajiban
dasar, bukan hasil kerja; aturan disiplin tetap lewat tata tertib (lihat `surat-peringatan-karyawan`).

## 8. Kurir / sopir

| KPI | Rumus | Satuan | Arah | Frek. | Sumber data |
|---|---|---|---|---|---|
| ★ Pengiriman tepat waktu | paket sampai ≤ janji ÷ paket dikirim × 100 | % | naik | M | log (persen) |
| ★ Paket gagal kirim | paket kembali/gagal ÷ paket dikirim × 100 | % | turun | M | log |
| ★ Jumlah pengiriman | paket/drop terkirim | paket | naik | M | log, `resi-picking` |
| ★ Setoran COD pas | hari setoran COD pas & tepat waktu ÷ hari ada COD × 100 | % | naik | M | `kas-umkm` |
| Biaya BBM per drop | biaya BBM ÷ jumlah drop | Rp | turun | B | `kas-umkm` |

Keterlambatan karena macet/banjir/rute di luar kendali kurir: catat di kolom `catatan` dan
bahas di 1:1. Jangan menambah KPI "kecepatan" yang mendorong mengebut.

## 9. Kasir

| KPI | Rumus | Satuan | Arah | Frek. | Sumber data |
|---|---|---|---|---|---|
| ★ Hari tanpa selisih kas | hari tutup kasir tanpa selisih ÷ hari bertugas × 100 | % | naik | M/B | `kasir-lokal tutup-kasir` |
| ★ Transaksi per shift | rata-rata transaksi per shift | transaksi | naik | M | `kasir-lokal rekap` |
| ★ Void tanpa alasan sah | void/retur tanpa alasan tercatat | kali | turun | M | `kasir-lokal` (void/retur beralasan) |
| ★ Kehadiran tepat waktu | seperti admin | % | naik | B | `absensi-lokal rekap` |
| Penjualan produk tambahan | transaksi dengan produk tawaran ÷ transaksi × 100 | % | naik | M | `kasir-lokal` |

"Transaksi per shift" dipengaruhi ramai-sepinya toko. Bandingkan antar-shift yang setara saja,
dan bobotnya jangan terbesar.

## 10. KPI divisi & perusahaan

Kosongkan kolom `orang` untuk KPI milik divisi (mis. "Pengiriman tepat waktu" untuk seluruh
Gudang & Pengiriman). Bila ada KPI divisi, skor divisi = skor KPI divisi (bobot per divisi
wajib 100); rata-rata individu tetap ditampilkan terpisah. Skor perusahaan = rata-rata divisi
(bobot sama) atau `--bobot-divisi`.

## 11. Merancang KPI yang adil (baca sebelum memasang target)

1. **3–5 KPI per orang.** Lebih dari 7 membuat orang tidak tahu mana yang penting.
2. **Bisa dikendalikan orangnya.** CS tidak dinilai dari jumlah komplain yang disebabkan gudang.
3. **Seimbang jumlah & mutu.** Pasangkan "jumlah pengiriman" dengan "gagal kirim", "output" dengan
   "reject", supaya orang tidak mengejar jumlah dengan mengorbankan mutu.
4. **Target dari data, disepakati bersama.** Tunjukkan data 3 bulan lalu, diskusikan targetnya
   dengan orangnya. Target yang dipaksakan cenderung diakali.
5. **Satu sumber data yang disepakati.** Tulis sumbernya di kolom `sumber` (mis. `crm-wa`).
6. **Hasil kerja, bukan pengawasan.** KPI tidak butuh pelacak lokasi, rekaman layar, atau membaca
   chat pribadi karyawan. Ukur keluaran kerja, bukan gerak-gerik orang.
7. **Ulas tiap 3 bulan.** Ganti KPI yang tidak lagi relevan atau ternyata mudah diakali.
