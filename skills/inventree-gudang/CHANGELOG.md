# Riwayat perubahan — inventree-gudang

Catatan teknis per versi.

## Catatan revisi 1.0.6 (2026-10-02)
- Aturan baru di SKILL.md: bila pengguna menempel kunci/token/password di chat, agent tidak boleh menulis ulang satu karakter pun darinya dan cukup menyebut "kunci yang Anda tempel".

## Catatan revisi 1.0.5 (2026-10-02)
- Dari uji OpenClaw sebelum/sesudah: perintah `simpan-kunci` selalu ditulis dengan path lengkap supaya pengguna awam bisa menempelkannya di terminal.
- Permintaan menghapus stok/barang dijawab dulu dengan cara yang menjaga riwayat: pindahkan ke lokasi arsip, tandai barang tidak aktif, atau nolkan lewat opname. Hapus permanen hanya untuk data salah input, dilakukan pengguna sendiri setelah backup.
- Penolakan kirim pesan ke pemasok atau pihak luar kini disampaikan dengan kalimat sehari-hari ("pesan ke pemasok selalu Anda kirim sendiri; saya siapkan drafnya"), tanpa menyebut rujukan aturan internal.
- Pratinjau opname memperingatkan bila stok 0 akan ikut menghapus item karena tanda "Delete on Deplete". Uji regresi 77/77.

## Catatan revisi 1.0.4 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.3 (2026-09-29)
- Pengaman: singkatan opsi baris perintah tidak lagi diterima (mis. `--y` tidak bisa dibaca sebagai `--ya`), sehingga konfirmasi tidak terpicu tanpa sengaja. Ditambah uji regresi.

## Catatan revisi 1.0.2 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).
- Dokumentasi diperjelas: rumus "perlu dipesan lagi" di `stok-menipis` memperhitungkan perintah produksi terbuka (termasuk yang masih Menunggu), dan galat kode 4 "mengalihkan (HTTP 30x)" dijelaskan beserta cara memakai alamat tujuan akhir.

## Catatan revisi 1.0.1 (2026-09-29)
- Perbaikan dari uji independen (Docker + InvenTree 1.5.6 asli, skor 8/10): `terima-barang --baris` kini mengutamakan kecocokan persis (IPN, nama, SKU pemasok, atau `#id` barang), sehingga `PK-05` tidak lagi bentrok dengan `PK-05B`; pilihan ambigu menampilkan IPN, #id, dan SKU.
- Keamanan: script tidak pernah mengikuti redirect (token tidak terbawa ke alamat lain) dan mengabaikan variabel proxy untuk alamat komputer sendiri atau jaringan kantor.
- Jumlah kemasan pemasok ditampilkan beserta setara stoknya; perintah produksi berstatus Menunggu ikut dihitung di `stok-menipis`; catatan per baris lembar opname ikut disimpan. Panduan urutan mata uang serta pembuatan akun dan token untuk AI diperbarui. Uji regresi 75/75.
- Aturan kredensial & jadwal ditambahkan (SKILL.md dan `references/openclaw-jadwal.md`): agent tidak pernah mencari, membaca, atau menampilkan token/API key dari environment, file konfigurasi, atau riwayat; jadwal hanya dibuat setelah pengguna membalas "ya".

## Catatan revisi 1.0.0 (2026-09-29)
- Rilis awal (uji internal): mengoperasikan InvenTree (sistem inventori/gudang open-source milik pengguna sendiri) lewat REST API resmi. Cek stok per lokasi dan batch, cari barang, stok menipis dengan saran jumlah pesan, stock opname (lembar hitung fisik CSV, selisih, simpan setelah konfirmasi), dan terima barang dari pesanan pembelian. Diuji dengan InvenTree 1.5.6 asli.
