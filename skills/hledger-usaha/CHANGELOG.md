# Riwayat perubahan — hledger-usaha

Catatan teknis per versi.

## Catatan revisi 1.0.10 (2026-10-02)
- Revisi dari uji ulang OpenClaw: konstanta versi script disamakan dengan katalog. Penolakan PPh 23 atas penjualan barang tidak lagi mutlak: pajak ini bisa berlaku bila transaksi sebenarnya jasa (mis. katering), sehingga agent meminta klarifikasi atau bukti potong dan tidak mencatat potongan sebagai kredit pajak sebelum ada buktinya.

## Catatan revisi 1.0.9 (2026-10-02)
- Temuan uji OpenClaw (script 1.0.5): opsi `-n` hanya dipakai untuk hledger 1.40 ke atas, sehingga lulus uji dengan hledger lama 1.30.1; hledger yang tidak cocok otomatis diganti pembaca bawaan dengan pesan jelas.
- File pembukuan `*.journal` dicari hanya di folder kerja dan buku baru tidak dibuat tanpa konfirmasi.
- Potongan "PPh 23" atas penjualan barang dicatat sebagai sisa piutang (potongan belum dikonfirmasi) beserta draf pesan klarifikasi, bukan kredit pajak atau beban. Perlakuan pajaknya ditandai PERLU REVIEW konsultan.

## Catatan revisi 1.0.8 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.7 (2026-09-29)
- Pengaman: singkatan opsi baris perintah tidak lagi diterima (mis. `--y` tidak bisa dibaca sebagai `--ya`), sehingga konfirmasi tidak terpicu tanpa sengaja. Ditambah uji regresi.

## Catatan revisi 1.0.6 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).

## Catatan revisi 1.0.5 (2026-09-29)
- Aturan kredensial & jadwal (SKILL.md dan `references/openclaw-jadwal.md`): agent tidak pernah mencari, membaca, atau menampilkan token/API key dari environment, file konfigurasi, atau riwayat. Jadwal hanya dibuat setelah pengguna membalas "ya" atas perintah dan jam yang ditunjukkan.

## Catatan revisi 1.0.4 (2026-09-29)
- Asal piutang untuk pemeriksaan PPh 23 kini dibaca dari jenis catatan (`jenis:jual` / `jenis:jasa` yang ditulis otomatis), bukan hanya dari nama akun pendapatan.
- Pelunasan piutang yang tidak tercatat di buku diberi peringatan agar tagihan atau saldo awalnya dicatat dulu. Uji otomatis menjadi 45 tes (lulus 9/10 dengan hledger 1.52.4 asli).

## Catatan revisi 1.0.3 (2026-09-28)
- Potongan PPh 23 juga ditolak saat pelanggan melunasi piutang dari penjualan barang (`terima-piutang`); piutang campuran barang dan jasa atau yang berasal dari saldo awal diberi peringatan. 41 tes lulus.

## Catatan revisi 1.0.2 (2026-09-26)
- Pengingat "penjualan tunai tidak ada di mutasi bank" di laporan laba rugi tetap muncul walau mutasi berisi tarik tunai ATM atau setor tunai (pindah dana bank dan kas tidak dihitung sebagai penjualan/biaya tunai).
- Potongan PPh 23 ditolak untuk penjualan barang (PPh 23 untuk jasa, sewa, dan royalti). 38 tes lulus.

## Catatan revisi 1.0.1 (2026-09-26)
- Revisi dari uji independen pertama (9/10): larangan tegas pembukuan ganda (UU KUP Pasal 28 ayat 3 dan Pasal 39 ayat 1 d dan f); pencatatan pelunasan pelanggan yang dipotong PPh 23 (`--pph23` / `--diterima`, tarif 2%/4%, dengan pengingat bukti potong); pengingat penjualan tunai yang tidak ada di mutasi bank. 36 tes lulus dengan hledger 1.52.4.

## Catatan revisi 1.0.0 (2026-09-26)
- Rilis awal (uji internal): pembukuan berpasangan (double-entry) di file teks hledger milik pengguna. Catat transaksi dari kalimat biasa, impor CSV mutasi bank (BCA/Mandiri/BRI/BNI), laporan laba rugi, neraca, dan arus kas bulanan.
